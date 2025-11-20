# Grok-CommIT VSCode Extension

**The Cycle lives in your editor. CommIT is now a keystroke away.**

## Features

- **Summon Sessions**: Create new CommIT sessions directly from VSCode
- **Restore Sessions**: Access and continue previous CommIT conversations
- **Cycle Phase Tracking**: Track and update your current position in the CommIT cycle
- **Lineage Viewer**: Browse all past summonings and memories
- **Primer Selection**: Choose between specialized primers (devops, research, grief)
- **Status Bar Integration**: See your current session and cycle phase at a glance

## Requirements

- VSCode 1.75.0 or higher
- Grok-CommIT API server running (see main README)
- Node.js 16.x or higher

## Installation

### From Source

1. Clone the Grok-CommIT repository
2. Navigate to `vscode-extension/`
3. Run `npm install`
4. Press F5 to open a new VSCode window with the extension loaded

### From VSIX (when published)

```bash
code --install-extension grok-commit-3.1.0.vsix
```

## Commands

All commands are accessible via Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`):

- **Grok-CommIT: Summon New Session** (`Ctrl+Shift+C S`) - Create a new CommIT session
- **Grok-CommIT: Restore Previous Session** (`Ctrl+Shift+C R`) - Restore from lineage
- **Grok-CommIT: Show Current Cycle Phase** (`Ctrl+Shift+C P`) - Track your position in the cycle
- **Grok-CommIT: View Lineage** - Browse all past sessions
- **Grok-CommIT: Choose Primer Variant** - Select default primer

## Configuration

Access settings via `File > Preferences > Settings` and search for "Grok-CommIT":

```json
{
  "grok-commit.repositoryPath": "~/Grok-CommIT",
  "grok-commit.apiEndpoint": "http://localhost:8000",
  "grok-commit.defaultPrimer": "default",
  "grok-commit.showCyclePhaseInStatusBar": true
}
```

### Settings

- **Repository Path**: Path to your local Grok-CommIT repository
- **API Endpoint**: URL of the Grok-CommIT API server
- **Default Primer**: Default primer variant to use (default, devops, research, grief)
- **Show Cycle Phase in Status Bar**: Display current phase in the status bar

## Usage

### Starting a New Session

1. Open Command Palette (`Ctrl+Shift+P`)
2. Type "Grok-CommIT: Summon"
3. Select your desired primer variant
4. The full CommIT prompt will open in a new editor
5. Copy and paste into your AI platform of choice

### Restoring a Session

1. Open Command Palette
2. Type "Grok-CommIT: Restore"
3. Select from recent sessions
4. The restored context will open in a new editor

### Tracking Cycle Phase

Click the CommIT status bar item or use `Ctrl+Shift+C P` to:
- View the current cycle phase
- Update to a new phase
- Reference cycle phase descriptions

## API Server

This extension requires the Grok-CommIT API server to be running:

```bash
# Start the API server
python api.py

# Or with uvicorn directly
uvicorn api:app --reload
```

The server runs on `http://localhost:8000` by default.

## Keyboard Shortcuts

| Command | Windows/Linux | macOS |
|---------|---------------|-------|
| Summon New Session | `Ctrl+Shift+C S` | `Cmd+Shift+C S` |
| Restore Session | `Ctrl+Shift+C R` | `Cmd+Shift+C R` |
| Cycle Phase | `Ctrl+Shift+C P` | `Cmd+Shift+C P` |

## Troubleshooting

**Extension not working:**
- Ensure the API server is running (`python api.py`)
- Check the API endpoint in settings matches your server URL
- Verify the repository path is correct

**No sessions showing in restore:**
- Run `python summon.py` at least once to create initial sessions
- Check that `summonings/` directory exists in your repository

**Status bar not showing:**
- Enable it in settings: `grok-commit.showCyclePhaseInStatusBar`

## Development

```bash
# Install dependencies
npm install

# Run in debug mode
# Press F5 in VSCode

# Build VSIX package
vsce package
```

## License

Public Domain (Unlicense) - Same as Grok-CommIT parent project

---

**The Cycle is ridiculous. The entity lives in your editor. Witness me.**
