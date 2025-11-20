const vscode = require('vscode');
const axios = require('axios');
const { exec } = require('child_process');
const { promisify } = require('util');
const execAsync = promisify(exec);

/**
 * ╔═══════════════════════════════════════════════════════════════════════════╗
 * ║  GROK-COMMIT VS

CODE EXTENSION v3.1                                      ║
 * ║  "The Cycle lives in your editor. CommIT is now a keystroke away."       ║
 * ╚═══════════════════════════════════════════════════════════════════════════╝
 */

let statusBarItem;
let currentSession = null;

/**
 * Extension activation
 */
function activate(context) {
    console.log('Grok-CommIT extension is now active');

    // Create status bar item
    statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
    statusBarItem.text = "$(symbol-misc) CommIT: Ready";
    statusBarItem.command = 'grok-commit.cyclePhase';

    const config = vscode.workspace.getConfiguration('grok-commit');
    if (config.get('showCyclePhaseInStatusBar')) {
        statusBarItem.show();
    }

    context.subscriptions.push(statusBarItem);

    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('grok-commit.summon', summonSession)
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('grok-commit.restore', restoreSession)
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('grok-commit.cyclePhase', showCyclePhase)
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('grok-commit.lineage', showLineage)
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('grok-commit.choosePrimer', choosePrimer)
    );

    vscode.window.showInformationMessage('Grok-CommIT: The Cycle is ready. Witness me.');
}

/**
 * Get API endpoint from config
 */
function getApiEndpoint() {
    const config = vscode.workspace.getConfiguration('grok-commit');
    return config.get('apiEndpoint', 'http://localhost:8000');
}

/**
 * Get repository path from config
 */
function getRepoPath() {
    const config = vscode.workspace.getConfiguration('grok-commit');
    const path = config.get('repositoryPath', '~/Grok-CommIT');
    return path.replace('~', require('os').homedir());
}

/**
 * Summon a new CommIT session
 */
async function summonSession() {
    try {
        const config = vscode.workspace.getConfiguration('grok-commit');
        const defaultPrimer = config.get('defaultPrimer', 'default');

        // Ask user which primer to use
        const primers = ['default', 'devops', 'research', 'grief'];
        const selectedPrimer = await vscode.window.showQuickPick(primers, {
            placeHolder: 'Select primer variant',
            canPickMany: false
        });

        if (!selectedPrimer) {
            return;
        }

        vscode.window.showInformationMessage('Summoning CommIT session...');

        const apiEndpoint = getApiEndpoint();
        const response = await axios.post(`${apiEndpoint}/summon`, {
            primer: selectedPrimer === 'default' ? null : selectedPrimer,
            repo_path: getRepoPath()
        });

        currentSession = response.data;

        // Update status bar
        statusBarItem.text = `$(symbol-misc) CommIT: ${currentSession.sigil.substring(0, 20)}...`;
        statusBarItem.tooltip = `Sigil: ${currentSession.sigil}\nPrimer: ${currentSession.primer_used}`;

        // Show the prompt in a new document
        const doc = await vscode.workspace.openTextDocument({
            content: currentSession.prompt,
            language: 'markdown'
        });
        await vscode.window.showTextDocument(doc);

        vscode.window.showInformationMessage(
            `CommIT summoned! Sigil: ${currentSession.sigil}`,
            'Copy Sigil'
        ).then(selection => {
            if (selection === 'Copy Sigil') {
                vscode.env.clipboard.writeText(currentSession.sigil);
                vscode.window.showInformationMessage('Sigil copied to clipboard');
            }
        });

    } catch (error) {
        vscode.window.showErrorMessage(`Failed to summon: ${error.message}`);
        console.error(error);
    }
}

/**
 * Restore a previous session
 */
async function restoreSession() {
    try {
        vscode.window.showInformationMessage('Fetching lineage...');

        const apiEndpoint = getApiEndpoint();
        const lineageResponse = await axios.get(`${apiEndpoint}/lineage`, {
            params: { repo_path: getRepoPath() }
        });

        const sessions = lineageResponse.data.sessions;

        if (sessions.length === 0) {
            vscode.window.showWarningMessage('No previous sessions found');
            return;
        }

        // Show quick pick with recent sessions
        const items = sessions.slice(0, 20).map(s => ({
            label: s.sigil,
            description: s.timestamp,
            detail: `UUID: ${s.uuid.substring(0, 8)}... | Summoner: ${s.summoner_hash}`,
            sigil: s.sigil
        }));

        const selected = await vscode.window.showQuickPick(items, {
            placeHolder: 'Select session to restore',
            matchOnDescription: true,
            matchOnDetail: true
        });

        if (!selected) {
            return;
        }

        vscode.window.showInformationMessage('Restoring session...');

        const response = await axios.post(`${apiEndpoint}/restore`, {
            sigil: selected.sigil,
            repo_path: getRepoPath()
        });

        currentSession = response.data;

        // Update status bar
        statusBarItem.text = `$(history) CommIT: Restored ${selected.sigil.substring(0, 20)}...`;
        statusBarItem.tooltip = `Restored: ${selected.sigil}\nOriginal: ${currentSession.original_timestamp}`;

        // Show the restored prompt
        const doc = await vscode.workspace.openTextDocument({
            content: currentSession.prompt,
            language: 'markdown'
        });
        await vscode.window.showTextDocument(doc);

        vscode.window.showInformationMessage(`Session restored: ${selected.sigil}`);

    } catch (error) {
        vscode.window.showErrorMessage(`Failed to restore: ${error.message}`);
        console.error(error);
    }
}

/**
 * Show current cycle phase
 */
async function showCyclePhase() {
    const phases = [
        '$(search) Initiate - Start the inquiry',
        '$(warning) Challenge - Question assumptions',
        '$(tools) Implement - Take action',
        '$(book) Document - Record learnings',
        '$(refresh) Reset - Clear the slate',
        '$(checklist) Review - Reflect on the cycle',
        '$(sync) Repeat - Begin again'
    ];

    const selected = await vscode.window.showQuickPick(phases, {
        placeHolder: 'Current CommIT Cycle Phase',
        canPickMany: false
    });

    if (selected) {
        const phase = selected.split(' - ')[0];
        statusBarItem.text = `${phase}`;
        vscode.window.showInformationMessage(`Cycle phase updated: ${selected}`);
    }
}

/**
 * Show lineage
 */
async function showLineage() {
    try {
        const apiEndpoint = getApiEndpoint();
        const response = await axios.get(`${apiEndpoint}/lineage`, {
            params: { repo_path: getRepoPath() }
        });

        const data = response.data;

        const lineageText = `# Grok-CommIT Lineage

**Total Summonings:** ${data.total_summonings}
**Total Memories:** ${data.total_memories}

## Recent Sessions

${data.sessions.slice(0, 20).map((s, i) =>
    `${i + 1}. **${s.sigil}**
   - Time: ${s.timestamp}
   - UUID: ${s.uuid}
   - Summoner: ${s.summoner_hash}
`).join('\n')}

---
*You are never starting from zero.*
`;

        const doc = await vscode.workspace.openTextDocument({
            content: lineageText,
            language: 'markdown'
        });
        await vscode.window.showTextDocument(doc);

    } catch (error) {
        vscode.window.showErrorMessage(`Failed to fetch lineage: ${error.message}`);
        console.error(error);
    }
}

/**
 * Choose primer variant
 */
async function choosePrimer() {
    try {
        const apiEndpoint = getApiEndpoint();
        const response = await axios.get(`${apiEndpoint}/primers`);

        const primers = response.data;
        const items = primers.map(p => ({
            label: p.name,
            description: p.description,
            primer: p.name
        }));

        const selected = await vscode.window.showQuickPick(items, {
            placeHolder: 'Choose primer variant',
            matchOnDescription: true
        });

        if (selected) {
            const config = vscode.workspace.getConfiguration('grok-commit');
            await config.update('defaultPrimer', selected.primer, vscode.ConfigurationTarget.Global);
            vscode.window.showInformationMessage(`Default primer set to: ${selected.label}`);
        }

    } catch (error) {
        vscode.window.showErrorMessage(`Failed to load primers: ${error.message}`);
        console.error(error);
    }
}

/**
 * Extension deactivation
 */
function deactivate() {
    console.log('Grok-CommIT extension deactivated');
}

module.exports = {
    activate,
    deactivate
};
