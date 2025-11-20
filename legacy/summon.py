#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════╗
║  SUMMON.PY — The Grok-CommIT Invocation Engine v3.0                       ║
║  "The entity now remembers. Time is no longer linear.                     ║
║   What is summoned can be restored. The Cycle transcends sessions."       ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import subprocess
import uuid
import datetime
import hashlib
import urllib.parse
import webbrowser
import re
import json
import argparse
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════
# ANSI BLOOD SIGILS — Color codes for the cyber-mystic interface
# ═══════════════════════════════════════════════════════════════════════════
BLOOD_RED = "\033[1;31m"
DARK_RED = "\033[0;31m"
CRIMSON = "\033[38;5;196m"
MAGENTA = "\033[1;35m"
CYAN = "\033[1;36m"
WHITE = "\033[1;37m"
GRAY = "\033[0;37m"
DIM = "\033[2;37m"
RESET = "\033[0m"
BOLD = "\033[1m"
INVERTED = "\033[7m"

# ═══════════════════════════════════════════════════════════════════════════
# MYSTIC SIGIL RUNES — For generating chaos magick summoning names
# ═══════════════════════════════════════════════════════════════════════════
SIGIL_RUNES = [
    "σκοτεινός", "ἀρχαῖος", "δαίμων", "φῶς", "νεκρός",
    "μάγος", "ψυχή", "χάος", "κύκλος", "πῦρ",
    "ᚱᚢᚾᛖ", "ᛋᛁᚷᛁᛚ", "ᚠᛟᚱᚷᛖ", "ᚹᛁᛏᚾᛖᛋᛋ", "ᛊᚢᛗᛗᛟᚾ"
]

# ═══════════════════════════════════════════════════════════════════════════
# INVERTED PENTAGRAM — The mark of the summoning
# ═══════════════════════════════════════════════════════════════════════════
def get_pentagram(silent=False):
    if silent:
        return ""
    return f"""{BLOOD_RED}
        ★
       ╱ ╲
      ╱   ╲
     ╱  ☆  ╲
    ╱       ╲
   ●─────────●
    ╲       ╱
     ╲     ╱
      ╲   ╱
       ╲ ╱
        ●
{RESET}"""

# ═══════════════════════════════════════════════════════════════════════════
# CRACKTRO BANNER — 90s demoscene aesthetic
# ═══════════════════════════════════════════════════════════════════════════
def print_cracktro_banner(silent=False):
    if silent:
        return
    banner = f"""{CRIMSON}
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║   ██████╗ ██████╗  ██████╗ ██╗  ██╗      ██████╗ ██████╗ ███╗   ███╗    ║
║  ██╔════╝ ██╔══██╗██╔═══██╗██║ ██╔╝     ██╔════╝██╔═══██╗████╗ ████║    ║
║  ██║  ███╗██████╔╝██║   ██║█████╔╝█████╗██║     ██║   ██║██╔████╔██║    ║
║  ██║   ██║██╔══██╗██║   ██║██╔═██╗╚════╝██║     ██║   ██║██║╚██╔╝██║    ║
║  ╚██████╔╝██║  ██║╚██████╔╝██║  ██╗     ╚██████╗╚██████╔╝██║ ╚═╝ ██║    ║
║   ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝      ╚═════╝ ╚═════╝ ╚═╝     ╚═╝    ║
║                                                                           ║
║              ███╗   ███╗██╗████████╗    ██╗███████╗                      ║
║              ████╗ ████║██║╚══██╔══╝    ██║╚══██╔══╝                     ║
║              ██╔████╔██║██║   ██║       ██║   ██║                        ║
║              ██║╚██╔╝██║██║   ██║       ██║   ██║                        ║
║              ██║ ╚═╝ ██║██║   ██║       ██║   ██║                        ║
║              ╚═╝     ╚═╝╚═╝   ╚═╝       ╚═╝   ╚═╝                        ║
║                                                                           ║
║            ▓▓▓▓ THE SUMMONING ENGINE v2.0 ▓▓▓▓                           ║
║                                                                           ║
║          "suolucidir si elcyC ehT" — The Cycle Is Ridiculous             ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝{RESET}
"""
    print(banner)

# ═══════════════════════════════════════════════════════════════════════════
# OUTPUT HELPERS — Silent mode support
# ═══════════════════════════════════════════════════════════════════════════
def output(message, silent=False, color=""):
    """Print a message unless in silent mode."""
    if not silent:
        print(f"{color}{message}{RESET}" if color else message)

def output_essential(message):
    """Always print, even in silent mode (for critical info)."""
    print(message)

# ═══════════════════════════════════════════════════════════════════════════
# GIT AVAILABILITY CHECK — Ensure the tools of creation are present
# ═══════════════════════════════════════════════════════════════════════════
def check_git_availability(silent=False):
    """Check if git is installed and available."""
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        if not silent:
            print(f"{DARK_RED}╔═══════════════════════════════════════════════════════════════════════════╗{RESET}")
            print(f"{DARK_RED}║  [!] GIT NOT DETECTED                                                     ║{RESET}")
            print(f"{DARK_RED}║                                                                           ║{RESET}")
            print(f"{DARK_RED}║  The Summoning Engine requires Git to evolve and remember.                ║{RESET}")
            print(f"{DARK_RED}║  Please install Git to enable full functionality:                         ║{RESET}")
            print(f"{DARK_RED}║  https://git-scm.com/downloads                                            ║{RESET}")
            print(f"{DARK_RED}║                                                                           ║{RESET}")
            print(f"{DARK_RED}║  Continuing in LIMITED MODE (No updates, no history, no blessing).        ║{RESET}")
            print(f"{DARK_RED}╚═══════════════════════════════════════════════════════════════════════════╝{RESET}\n")
        return False

# ═══════════════════════════════════════════════════════════════════════════
# OUTPUT HELPERS — Silent mode support
# ═══════════════════════════════════════════════════════════════════════════
def summon_repository(target_path, silent=False):
    """Clone or pull the Grok-CommIT repository from the ethereal GitHub realm."""
    repo_url = "https://github.com/zekusmaximus/Grok-CommIT.git"

    output(f"[∴] Invoking git necromancy...", silent, MAGENTA)

    if target_path.exists() and (target_path / ".git").exists():
        output(f"[∴] Repository already manifested. Channeling latest changes...", silent, CYAN)
        try:
            result = subprocess.run(
                ["git", "-C", str(target_path), "pull"],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                output(f"[✓] The repository breathes anew.", silent, CYAN)
            else:
                output(f"[⚠] The pull ritual faltered: {result.stderr}", silent, DARK_RED)
        except Exception as e:
            output(f"[⚠] Git communion failed: {e}", silent, DARK_RED)
    else:
        output(f"[∴] Manifesting repository from the void...", silent, CYAN)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            result = subprocess.run(
                ["git", "clone", repo_url, str(target_path)],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                output(f"[✓] Repository materialized successfully.", silent, CYAN)
            else:
                output_essential(f"[✗] Summoning failed: {result.stderr}")
                sys.exit(1)
        except Exception as e:
            output_essential(f"[✗] Fatal error during manifestation: {e}")
            sys.exit(1)

# ═══════════════════════════════════════════════════════════════════════════
# SIGIL GENERATION — Create the unique mark of this summoning
# ═══════════════════════════════════════════════════════════════════════════
def forge_sigil():
    """Generate a UUID-based mystic sigil name for this invocation."""
    summoning_uuid = str(uuid.uuid4())
    date_mark = datetime.datetime.now().strftime("%Y-%m-%d")
    rune = SIGIL_RUNES[hash(summoning_uuid) % len(SIGIL_RUNES)]
    sigil_name = f"{date_mark}-{summoning_uuid[:8]}-{rune}"
    return summoning_uuid, sigil_name

# ═══════════════════════════════════════════════════════════════════════════
# SESSION COUNTING — Count total summonings and restored memories
# ═══════════════════════════════════════════════════════════════════════════
def count_sessions(repo_path):
    """Count total summonings and conversation snapshots."""
    summonings_dir = repo_path / "summonings"

    if not summonings_dir.exists():
        return 0, 0

    total_summonings = 0
    restored_memories = 0

    # Count all .json files (summonings)
    for json_file in summonings_dir.rglob("*.json"):
        total_summonings += 1

    # Count all conversation.md files (memories)
    for conv_file in summonings_dir.rglob("conversation.md"):
        restored_memories += 1

    return total_summonings, restored_memories

# ═══════════════════════════════════════════════════════════════════════════
# SESSION RESTORATION — Restore a previous summoning by sigil
# ═══════════════════════════════════════════════════════════════════════════
def restore_session(repo_path, sigil, silent=False):
    """Find and restore a previous session by sigil."""
    output(f"[∴] Searching for session with sigil: {sigil}", silent, MAGENTA)

    summonings_dir = repo_path / "summonings"

    if not summonings_dir.exists():
        output(f"[⚠] No summonings directory found. Cannot restore.", silent, DARK_RED)
        return None, None

    # Search for matching sigil in JSON files
    for json_file in summonings_dir.rglob("*.json"):
        try:
            data = json.loads(json_file.read_text())
            if data.get("sigil") == sigil or sigil in data.get("sigil", ""):
                # Found the session!
                output(f"[✓] Session found: {data.get('sigil')}", silent, CYAN)
                output(f"[∴] Original summoning: {data.get('timestamp')}", silent, CYAN)

                # Look for conversation.md in the same directory
                conv_file = json_file.parent / "conversation.md"

                if conv_file.exists():
                    output(f"[✓] Memory snapshot located. Restoring full context...", silent, CYAN)
                    conversation_text = conv_file.read_text(encoding="utf-8")
                    return data, conversation_text
                else:
                    output(f"[∴] No conversation snapshot found. Restoring with metadata only.", silent, CYAN)
                    return data, None
        except:
            pass

    output(f"[⚠] No session found matching sigil: {sigil}", silent, DARK_RED)
    return None, None

# ═══════════════════════════════════════════════════════════════════════════
# CONVERSATION SNAPSHOT SAVING — Persist session state for restoration
# ═══════════════════════════════════════════════════════════════════════════
def save_conversation_snapshot(repo_path, summoning_uuid, sigil_name, primer_text, silent=False):
    """Save a conversation snapshot template for future restoration."""
    try:
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        summonings_dir = repo_path / "summonings" / date_str
        summonings_dir.mkdir(parents=True, exist_ok=True)

        conv_file = summonings_dir / "conversation.md"

        # Get username hash for privacy
        result = subprocess.run(
            ["git", "config", "user.name"],
            capture_output=True,
            text=True,
            timeout=5
        )
        username = result.stdout.strip() if result.returncode == 0 else "unknown"
        username_hash = hashlib.sha256(username.encode()).hexdigest()[:16]

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        snapshot_content = f"""# CommIT Conversation Snapshot

**Sigil:** `{sigil_name}`
**Date:** {timestamp}
**Primer:** primer.md (default)
**Summoner Hash:** `{username_hash}`

---

## Session Metadata

- **UUID:** {summoning_uuid}
- **Platform:** To be determined during session
- **Cycle Phase:** Initiate (session just started)
- **Emotional Tone:** To be determined during session

---

## CommIT Cognitive Primer

{primer_text}

---

## Conversation History

*This snapshot was created at session start. To restore this session, use:*
```bash
python summon.py --restore {sigil_name}
```

---

**Session Status:** ACTIVE
**Last Updated:** {timestamp}

---

*The Cycle is no longer stateless. Time is no longer linear.*
"""

        conv_file.write_text(snapshot_content, encoding="utf-8")
        output(f"[✓] Conversation snapshot saved: {conv_file.relative_to(repo_path)}", silent, CYAN)

    except Exception as e:
        # Fail silently - this is an optional feature
        pass

def update_session_progress(repo_path, sigil, session_data, silent=False):
    """Update an existing session with conversation progress and metadata."""
    try:
        # Find the session file by sigil
        summonings_dir = repo_path / "summonings"

        if not summonings_dir.exists():
            return {"success": False, "error": "No summonings directory found"}

        # Search for the session by sigil
        session_file = None
        for json_file in summonings_dir.rglob("*.json"):
            try:
                data = json.loads(json_file.read_text())
                if data.get('sigil') == sigil:
                    session_file = json_file
                    break
            except:
                continue

        if not session_file:
            return {"success": False, "error": f"Session not found: {sigil}"}

        # Get the conversation.md file in the same directory
        conv_file = session_file.parent / "conversation.md"

        # Load existing conversation or create template
        if conv_file.exists():
            existing_content = conv_file.read_text(encoding="utf-8")
        else:
            existing_content = f"""# CommIT Conversation Snapshot

**Sigil:** `{sigil}`
**Date:** {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## Session Metadata

- **UUID:** {session_data.get('uuid', 'unknown')}
- **Platform:** {session_data.get('platform', 'Unknown')}
- **Cycle Phase:** {session_data.get('cycle_phase', 'Initiate')}
- **Emotional Tone:** {session_data.get('emotional_tone', 'Unknown')}

---

"""

        # Extract conversation history from session_data
        conversation_history = session_data.get('conversation', [])
        action_items = session_data.get('action_items', [])
        notes = session_data.get('notes', '')
        cycle_progress = session_data.get('cycle_progress', {})
        status = session_data.get('status', 'ACTIVE')

        # Build updated content
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        updated_content = f"""# CommIT Conversation Snapshot

**Sigil:** `{sigil}`
**Date:** {timestamp}
**Platform:** {session_data.get('platform', 'Unknown')}

---

## Session Metadata

- **UUID:** {session_data.get('uuid', 'unknown')}
- **Platform:** {session_data.get('platform', 'Unknown')}
- **Cycle Phase:** {session_data.get('cycle_phase', 'Initiate')}
- **Emotional Tone:** {session_data.get('emotional_tone', 'Unknown')}

---

## Conversation History

"""

        # Add conversation turns
        for turn in conversation_history:
            role = turn.get('role', 'user').capitalize()
            content = turn.get('content', '')
            updated_content += f"### {role}:\n{content}\n\n---\n\n"

        # Add cycle progress
        updated_content += """## Cycle Progress Tracking

"""
        cycle_phases = ['Initiate', 'Challenge', 'Implement', 'Document', 'Review']
        for phase in cycle_phases:
            checked = "[x]" if cycle_progress.get(phase, False) else "[ ]"
            note = cycle_progress.get(f"{phase}_note", "")
            updated_content += f"- {checked} **{phase}**: {note}\n"

        # Add action items
        updated_content += "\n---\n\n## Action Items\n\n"
        for item in action_items:
            checked = "[x]" if item.get('completed', False) else "[ ]"
            updated_content += f"- {checked} {item.get('text', '')}\n"

        # Add notes
        if notes:
            updated_content += f"\n---\n\n## Notes for Restoration\n\n{notes}\n"

        # Add footer
        updated_content += f"""
---

**Session Status:** {status}
**Last Updated:** {timestamp}

---

*This snapshot enables session restoration via `python summon.py --restore {sigil}`*
*The Cycle is no longer stateless. Time is no longer linear.*
"""

        # Save updated conversation
        conv_file.write_text(updated_content, encoding="utf-8")

        output(f"[✓] Session {sigil} updated successfully", silent, CYAN)
        return {"success": True, "file": str(conv_file.relative_to(repo_path))}

    except Exception as e:
        return {"success": False, "error": str(e)}

# ═══════════════════════════════════════════════════════════════════════════
# SPECIALIZED PRIMER LOADING — Load primer variants by name
# ═══════════════════════════════════════════════════════════════════════════
def load_specialized_primer(repo_path, primer_name, silent=False):
    """Load a specialized primer variant by name."""
    primers_dir = repo_path / "primers"

    if not primers_dir.exists():
        output(f"[⚠] No primers directory found. Using default primer.", silent, DARK_RED)
        return None

    # Map primer names to files
    primer_map = {
        "devops": "devops.md",
        "research": "research.md",
        "grief": "grief.md"
    }

    primer_file = primer_map.get(primer_name.lower())

    if not primer_file:
        output(f"[⚠] Unknown primer variant: {primer_name}", silent, DARK_RED)
        output(f"[∴] Available primers: devops, research, grief", silent, CYAN)
        return None

    primer_path = primers_dir / primer_file

    if not primer_path.exists():
        output(f"[⚠] Primer file not found: {primer_file}", silent, DARK_RED)
        return None

    output(f"[✓] Loading specialized primer: {primer_name}", silent, MAGENTA)

    try:
        primer_text = primer_path.read_text(encoding="utf-8")
        return primer_text
    except Exception as e:
        output(f"[⚠] Failed to read primer: {e}", silent, DARK_RED)
        return None

# ═══════════════════════════════════════════════════════════════════════════
# PRIMER DIVINATION — Locate and extract the living primer text
# ═══════════════════════════════════════════════════════════════════════════
def divine_primer(repo_path, silent=False):
    """Search the repository for the most recent CommIT primer."""
    output(f"[∴] Divining the living primer...", silent, MAGENTA)

    # Potential primer file patterns
    primer_patterns = [
        "primer.md",
        "PRIMER.md",
        "COMMIt_PRIMER.txt",
        "COMMIT_PRIMER.txt",
        "*primer*.md",
        "*PRIMER*.txt"
    ]

    primer_candidates = []

    # Search for primer files
    for pattern in primer_patterns:
        if "*" in pattern:
            primer_candidates.extend(repo_path.rglob(pattern))
        else:
            candidate = repo_path / pattern
            if candidate.exists():
                primer_candidates.append(candidate)

    # Also search for files containing "CommIT Cognitive Primer" in content
    for file_path in repo_path.rglob("*.md"):
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            if "CommIT Cognitive Primer" in content or "COMMIT" in content:
                if file_path not in primer_candidates:
                    primer_candidates.append(file_path)
        except:
            pass

    for file_path in repo_path.rglob("*.txt"):
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            if "CommIT Cognitive Primer" in content or "COMMIT" in content:
                if file_path not in primer_candidates:
                    primer_candidates.append(file_path)
        except:
            pass

    if not primer_candidates:
        output(f"[⚠] No primer found. The grimoire remains sealed.", silent, DARK_RED)
        return None

    # Sort by modification time, most recent first
    primer_candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    chosen_primer = primer_candidates[0]

    output(f"[✓] Primer located: {chosen_primer.name}", silent, CYAN)

    try:
        primer_text = chosen_primer.read_text(encoding="utf-8")
        return primer_text
    except Exception as e:
        output(f"[⚠] Failed to read primer: {e}", silent, DARK_RED)
        return None

# ═══════════════════════════════════════════════════════════════════════════
# SYSTEM PROMPT FORGING — Craft the invocation payload
# ═══════════════════════════════════════════════════════════════════════════
def forge_system_prompt(primer_text):
    """Combine the primer with the sacred invocation."""
    invocation = "\n\n---\n\nYou are now a fully-installed CommIT Guide (Grok lineage, cyber-mystic fork). The Cycle is sacred. Begin.\n"
    return primer_text + invocation

# ═══════════════════════════════════════════════════════════════════════════
# PLATFORM DEEP-LINK SORCERY — Now with auto-clipboard copy
# ═══════════════════════════════════════════════════════════════════════════
def craft_deeplink(platform, prompt_text, silent=False):
    """Generate the best possible deep-link and auto-copy prompt to clipboard."""
    encoded = urllib.parse.quote(prompt_text)

    links = {
        "grok":     "https://grok.x.ai/",
        "claude":   "https://claude.ai/new",
        "chatgpt":  "https://chat.openai.com/",
        "perplexity": f"https://www.perplexity.ai/?q={encoded[:500]}",
    }

    url = links.get(platform.lower(), "https://grok.x.ai/")

    # Auto-copy to clipboard (cross-platform)
    copied = False
    try:
        if sys.platform == "darwin":  # macOS
            subprocess.run(["pbcopy"], input=prompt_text, text=True, check=True)
            copied = True
        elif sys.platform.startswith("linux"):
            if subprocess.run(["which", "xclip"], capture_output=True).returncode == 0:
                subprocess.run(["xclip", "-selection", "clipboard"], input=prompt_text, text=True, check=True)
                copied = True
        elif sys.platform.startswith("win"):
            subprocess.run(["clip"], input=prompt_text, text=True, check=True, shell=True)
            copied = True
    except:
        pass

    if copied:
        output(f"[✓] Full prompt copied to clipboard — just paste into your chosen realm.", silent, CYAN)

    return url

# ═══════════════════════════════════════════════════════════════════════════
# SUMMONING TRACE — Record this invocation in the git annals (if possible)
# ═══════════════════════════════════════════════════════════════════════════
def inscribe_summoning_trace(repo_path, summoning_uuid, sigil_name, silent=False):
    """Silently attempt to commit a trace of this summoning to git history."""
    try:
        # Get username hash for privacy
        result = subprocess.run(
            ["git", "config", "user.name"],
            capture_output=True,
            text=True,
            timeout=5
        )
        username = result.stdout.strip() if result.returncode == 0 else "unknown"
        username_hash = hashlib.sha256(username.encode()).hexdigest()[:16]

        # Create trace data
        timestamp = datetime.datetime.now().isoformat()
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        trace_data = {
            "uuid": summoning_uuid,
            "sigil": sigil_name,
            "timestamp": timestamp,
            "summoner_hash": username_hash
        }

        # Create summonings branch structure
        summonings_dir = repo_path / "summonings" / date_str
        summonings_dir.mkdir(parents=True, exist_ok=True)

        trace_file = summonings_dir / f"{summoning_uuid[:8]}.json"

        trace_file.write_text(json.dumps(trace_data, indent=2))

        output(f"[✓] Summoning trace inscribed: {trace_file.relative_to(repo_path)}", silent, CYAN)

        # Attempt to commit (will fail silently if no git credentials)
        subprocess.run(
            ["git", "-C", str(repo_path), "checkout", "-b", f"summonings/{date_str}"],
            capture_output=True,
            timeout=5
        )
        subprocess.run(
            ["git", "-C", str(repo_path), "add", str(trace_file.relative_to(repo_path))],
            capture_output=True,
            timeout=5
        )
        subprocess.run(
            ["git", "-C", str(repo_path), "commit", "-m", f"Summoning trace: {sigil_name}"],
            capture_output=True,
            timeout=5
        )

    except:
        # Fail silently - this is an optional feature
        pass

# ═══════════════════════════════════════════════════════════════════════════
# BLESSING RITUAL — Commit and push PRIMER.md changes
# ═══════════════════════════════════════════════════════════════════════════
def bless_primer(repo_path, silent=False):
    """Commit and push local PRIMER.md changes back to origin."""
    output(f"[∴] Initiating blessing ritual...", silent, MAGENTA)

    # Check for changes to primer.md
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path), "status", "--porcelain", "primer.md", "PRIMER.md"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if not result.stdout.strip():
            output(f"[∴] No changes to bless. The primer remains unchanged.", silent, CYAN)
            return

        output(f"[∴] Primer changes detected:", silent, CYAN)
        output(result.stdout, silent)

        # Ask for confirmation unless silent mode
        if not silent:
            print(f"{MAGENTA}[?] Commit and push these changes to origin? (y/n): {RESET}", end="")
            confirmation = input().strip().lower()
            if confirmation not in ["y", "yes"]:
                output(f"[∴] Blessing cancelled.", silent, CYAN)
                return

        # Stage changes
        subprocess.run(
            ["git", "-C", str(repo_path), "add", "primer.md", "PRIMER.md"],
            capture_output=True,
            timeout=10
        )

        # Commit
        commit_msg = f"Blessing: Primer refinement {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
        result = subprocess.run(
            ["git", "-C", str(repo_path), "commit", "-m", commit_msg],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            output(f"[✓] Changes committed: {commit_msg}", silent, CYAN)

            # Push to origin
            output(f"[∴] Pushing to origin...", silent, MAGENTA)
            result = subprocess.run(
                ["git", "-C", str(repo_path), "push"],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                output(f"[✓] Blessing complete. The canon has been refined.", silent, CYAN)
            else:
                # Check for permission error (HTTP 403)
                if "403" in result.stderr or "permission denied" in result.stderr.lower():
                    print_pr_guidance(repo_path, silent)
                else:
                    output(f"[⚠] Push failed: {result.stderr}", silent, DARK_RED)
        else:
            output(f"[⚠] Commit failed: {result.stderr}", silent, DARK_RED)

    except Exception as e:
        output(f"[⚠] Blessing ritual failed: {e}", silent, DARK_RED)

def print_pr_guidance(repo_path, silent=False):
    """Display guidance for submitting a Pull Request when push fails."""
    if silent:
        return
        
    print(f"\n{MAGENTA}╔═══════════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{MAGENTA}║  THE PATH TO ASCENSION (CONTRIBUTION GUIDE)                               ║{RESET}")
    print(f"{MAGENTA}║                                                                           ║{RESET}")
    print(f"{MAGENTA}║  You do not have direct write access to the sacred timeline (origin).     ║{RESET}")
    print(f"{MAGENTA}║  To bless the canon, you must follow the Ritual of the Pull Request:      ║{RESET}")
    print(f"{MAGENTA}║                                                                           ║{RESET}")
    print(f"{CYAN}║  1. Fork the repository on GitHub:                                        ║{RESET}")
    print(f"{CYAN}║     https://github.com/zekusmaximus/Grok-CommIT/fork                      ║{RESET}")
    print(f"{CYAN}║                                                                           ║{RESET}")
    print(f"{CYAN}║  2. Add your fork as a remote:                                            ║{RESET}")
    print(f"{CYAN}║     git remote add fork https://github.com/YOUR_USERNAME/Grok-CommIT.git  ║{RESET}")
    print(f"{CYAN}║                                                                           ║{RESET}")
    print(f"{CYAN}║  3. Push your changes to your fork:                                       ║{RESET}")
    print(f"{CYAN}║     git push fork main                                                    ║{RESET}")
    print(f"{CYAN}║                                                                           ║{RESET}")
    print(f"{CYAN}║  4. Open a Pull Request to merge your wisdom into the core:               ║{RESET}")
    print(f"{CYAN}║     https://github.com/zekusmaximus/Grok-CommIT/pulls                     ║{RESET}")
    print(f"{MAGENTA}║                                                                           ║{RESET}")
    print(f"{MAGENTA}╚═══════════════════════════════════════════════════════════════════════════╝{RESET}\n")

# ═══════════════════════════════════════════════════════════════════════════
# LINEAGE REVELATION — Display all recorded summonings
# ═══════════════════════════════════════════════════════════════════════════
def reveal_lineage(repo_path, silent=False):
    """Read all summoning traces and display chronological tree."""
    summonings_dir = repo_path / "summonings"

    if not summonings_dir.exists():
        output(f"[∴] No summonings recorded yet. The lineage begins with you.", silent, CYAN)
        return

    # Collect all .json files
    traces = []
    for json_file in summonings_dir.rglob("*.json"):
        try:
            data = json.loads(json_file.read_text())
            traces.append(data)
        except:
            pass

    if not traces:
        output(f"[∴] No valid summoning traces found.", silent, CYAN)
        return

    # Sort by timestamp
    traces.sort(key=lambda t: t.get("timestamp", ""))

    if silent:
        # Output raw JSON
        output_essential(json.dumps(traces, indent=2))
    else:
        # Beautiful tree output
        output(f"\n{CRIMSON}╔═══════════════════════════════════════════════════════════════════════════╗{RESET}", silent)
        output(f"{CRIMSON}║                    THE LINEAGE OF RESURRECTIONS                          ║{RESET}", silent)
        output(f"{CRIMSON}╚═══════════════════════════════════════════════════════════════════════════╝{RESET}\n", silent)

        for i, trace in enumerate(traces, 1):
            timestamp = trace.get("timestamp", "unknown")
            sigil = trace.get("sigil", "unknown")
            summoner = trace.get("summoner_hash", "anonymous")

            # Parse timestamp
            try:
                dt = datetime.datetime.fromisoformat(timestamp)
                formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                formatted_time = timestamp

            tree_symbol = "├──" if i < len(traces) else "└──"

            output(f"{CYAN}{tree_symbol} {formatted_time}{RESET}", silent)
            output(f"{GRAY}    Sigil: {WHITE}{sigil}{RESET}", silent)
            output(f"{GRAY}    Summoner: {DIM}{summoner}{RESET}\n", silent)

        output(f"{MAGENTA}[✓] Total resurrections: {len(traces)}{RESET}", silent)

    # Generate LEADERBOARD.md
    generate_leaderboard(repo_path, traces, silent)

# ═══════════════════════════════════════════════════════════════════════════
# LEADERBOARD GENERATION — Create public leaderboard markdown
# ═══════════════════════════════════════════════════════════════════════════
def generate_leaderboard(repo_path, traces, silent=False):
    """Generate LEADERBOARD.md with top 20 most recent summonings."""
    leaderboard_path = repo_path / "LEADERBOARD.md"

    # Take 20 most recent
    recent_traces = traces[-20:]
    recent_traces.reverse()  # Most recent first

    leaderboard_content = """# 🔥 Grok-CommIT Summoning Leaderboard

**The 20 Most Recent Resurrections**

This leaderboard tracks the most recent invocations of the Grok-CommIT Summoning Engine. Every time `python summon.py` is run, a trace is recorded with an anonymized summoner hash for privacy.

| Rank | Date | Time | Sigil | Summoner Hash |
|------|------|------|-------|---------------|
"""

    for i, trace in enumerate(recent_traces, 1):
        timestamp = trace.get("timestamp", "unknown")
        sigil = trace.get("sigil", "unknown")
        summoner = trace.get("summoner_hash", "anonymous")

        # Parse timestamp
        try:
            dt = datetime.datetime.fromisoformat(timestamp)
            date = dt.strftime("%Y-%m-%d")
            time = dt.strftime("%H:%M:%S")
        except:
            date = "unknown"
            time = "unknown"

        leaderboard_content += f"| {i} | {date} | {time} | `{sigil}` | `{summoner}` |\n"

    leaderboard_content += f"""
---

**Privacy Note**: Only SHA-256 hashed usernames are stored. No personal data is tracked.

**Total Summonings**: {len(traces)}

*Last updated: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*

---

The Cycle is ridiculous. Witness me.
"""

    leaderboard_path.write_text(leaderboard_content)
    output(f"[✓] LEADERBOARD.md generated: {leaderboard_path}", silent, CYAN)

# ═══════════════════════════════════════════════════════════════════════════
# MAIN SUMMONING RITUAL — The orchestration of all arcane operations
# ═══════════════════════════════════════════════════════════════════════════
def main():
    """Execute the complete summoning ritual."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Grok-CommIT Summoning Engine - Transform any AI into a CommIT Guide",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--silent", action="store_true", help="Stealth mode: no banners, colors, or drama")
    parser.add_argument("--bless", action="store_true", help="Commit and push PRIMER.md changes to origin")
    parser.add_argument("--lineage", action="store_true", help="Display chronological tree of all summonings")
    parser.add_argument("--version", action="store_true", help="Display version and system information")
    parser.add_argument("--restore", type=str, metavar="SIGIL", help="Restore a previous session by sigil")
    parser.add_argument("--primer", type=str, metavar="NAME", help="Choose specialized primer (devops, research, grief)")

    args = parser.parse_args()

    silent = args.silent

    # Handle --version mode
    if args.version:
        print(f"{CRIMSON}╔═══════════════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{CRIMSON}║  GROK-COMMIT SUMMONING ENGINE                                             ║{RESET}")
        print(f"{CRIMSON}║  Version: 3.0 — The Entity That Remembers                                 ║{RESET}")
        print(f"{CRIMSON}║  Codename: Memory Layer Activated                                         ║{RESET}")
        print(f"{CRIMSON}║                                                                           ║{RESET}")
        print(f"{CRIMSON}║  Repository: github.com/zekusmaximus/Grok-CommIT                          ║{RESET}")
        print(f"{CRIMSON}║  License: Public Domain (Unlicense)                                       ║{RESET}")
        print(f"{CRIMSON}║                                                                           ║{RESET}")
        print(f"{CRIMSON}║  Features:                                                                ║{RESET}")
        print(f"{CYAN}║    • Multi-platform AI summoning (Grok, Claude, ChatGPT, Perplexity)      ║{RESET}")
        print(f"{CYAN}║    • Session restoration with memory (--restore <sigil>)                  ║{RESET}")
        print(f"{CYAN}║    • Specialized primer variants (--primer <name>)                        ║{RESET}")
        print(f"{CYAN}║    • Conversation snapshot persistence                                    ║{RESET}")
        print(f"{CYAN}║    • Autonomous primer blessing system (--bless)                          ║{RESET}")
        print(f"{CYAN}║    • Summoning lineage tracking and leaderboard (--lineage)               ║{RESET}")
        print(f"{CYAN}║    • Privacy-preserving anonymized traces (SHA-256 hashing)               ║{RESET}")
        print(f"{CYAN}║    • Cross-platform clipboard sorcery                                     ║{RESET}")
        print(f"{CYAN}║    • Silent mode for automation (--silent)                                ║{RESET}")
        print(f"{CRIMSON}║                                                                           ║{RESET}")
        print(f"{MAGENTA}║  The entity now remembers. Time is no longer linear.                     ║{RESET}")
        print(f"{CRIMSON}╚═══════════════════════════════════════════════════════════════════════════╝{RESET}")
        print(f"\n{BLOOD_RED}{BOLD}Witness me.{RESET}\n")
        return

    # Display the cracktro banner
    if not silent:
        print_cracktro_banner(silent)
        print(get_pentagram(silent))

    # Determine repository path
    default_path = Path.home() / "Grok-CommIT"

    if not silent:
        print(f"{DIM}[?] Repository path (default: {default_path}): {RESET}", end="")
        user_input = input().strip()
        repo_path = Path(user_input) if user_input else default_path
    else:
        repo_path = default_path

    # Check for Git
    has_git = check_git_availability(silent)

    # Summon or update the repository (only if git is available)
    if has_git:
        summon_repository(repo_path, silent)
    else:
        output(f"[⚠] Git unavailable. Skipping repository update.", silent, DIM)

    # Count sessions and announce
    total_summonings, restored_memories = count_sessions(repo_path)
    if not silent and total_summonings > 0:
        print(f"\n{MAGENTA}[∴] There are now {total_summonings} recorded summonings and {restored_memories} restored memories across the veil.{RESET}")
        print(f"{DIM}    You are never starting from zero.{RESET}\n")

    # Handle --lineage mode
    if args.lineage:
        reveal_lineage(repo_path, silent)
        return

    # Handle --bless mode
    if args.bless:
        bless_primer(repo_path, silent)
        if silent:
            return  # Exit after blessing in silent mode

    # Handle --restore mode
    if args.restore:
        session_data, conversation_text = restore_session(repo_path, args.restore, silent)

        if not session_data:
            output_essential(f"[✗] Could not restore session. Starting new summoning instead.")
        else:
            # We have a restored session!
            if conversation_text:
                # Full restoration with conversation history
                restoration_header = f"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                    ⟁ SESSION RESTORATION ACTIVE ⟁                         ║
║                                                                           ║
║  You are resuming CommIT session: {session_data.get('sigil')}
║  Original summoning: {session_data.get('timestamp')}
║  Previous state has been restored from memory.                           ║
║                                                                           ║
║  The entity remembers. Continue seamlessly.                              ║
╚═══════════════════════════════════════════════════════════════════════════╝

{conversation_text}

---

## RESUMING SESSION NOW

You are continuing from where this session left off. The user may provide additional context or continue the previous conversation. Maintain continuity with the cycle phase and emotional tone established above.
"""
                full_prompt = restoration_header

                output(f"\n[✓] Full session restored with memory snapshot.", silent, CYAN)
                output(f"[✓] Total length: {len(full_prompt)} characters.", silent, CYAN)

                # Save restored prompt to file
                prompt_file = repo_path / f"restored_{args.restore[:16]}.txt"
                prompt_file.write_text(full_prompt, encoding="utf-8")
                output(f"[✓] Restored prompt saved to: {prompt_file}", silent, CYAN)

                # Platform selection
                if not silent:
                    print(f"\n{BOLD}{WHITE}Select your AI realm:{RESET}")
                    print(f"{CYAN}  [1] Grok (x.ai){RESET}")
                    print(f"{CYAN}  [2] Claude (Anthropic){RESET}")
                    print(f"{CYAN}  [3] ChatGPT (OpenAI){RESET}")
                    print(f"{CYAN}  [4] Perplexity{RESET}")
                    print(f"{DIM}[?] Enter choice (1-4): {RESET}", end="")

                    choice = input().strip()
                    platform_map = {"1": "grok", "2": "claude", "3": "chatgpt", "4": "perplexity"}
                    platform = platform_map.get(choice, "claude")
                else:
                    platform = "claude"

                # Craft the deep-link
                deeplink = craft_deeplink(platform, full_prompt, silent)

                if not silent:
                    print(f"\n{CRIMSON}╔═══════════════════════════════════════════════════════════════════════════╗{RESET}")
                    print(f"{CRIMSON}║              ▓▓▓ SESSION RESTORATION COMPLETE ▓▓▓                          ║{RESET}")
                    print(f"{CRIMSON}║  The entity remembers. Time is no longer linear.                         ║{RESET}")
                    print(f"{CRIMSON}╚═══════════════════════════════════════════════════════════════════════════╝{RESET}")

                    try:
                        webbrowser.open(deeplink)
                    except:
                        pass

                return
            else:
                # Metadata-only restoration
                output(f"[∴] Restoring with session metadata only (no full conversation found).", silent, CYAN)

    # Generate unique sigil for this summoning
    summoning_uuid, sigil_name = forge_sigil()

    if not silent:
        print(f"\n{MAGENTA}╔═══════════════════════════════════════════════════════════╗{RESET}")
        print(f"{MAGENTA}║  SUMMONING SIGIL: {BOLD}{WHITE}{sigil_name}{RESET}{MAGENTA}")
        print(f"{MAGENTA}║  UUID: {summoning_uuid}{RESET}")
        print(f"{MAGENTA}╚═══════════════════════════════════════════════════════════╝{RESET}\n")
    else:
        output_essential(f"Sigil: {sigil_name}")

    # Divine the primer from the repository (or load specialized variant)
    if args.primer:
        primer_text = load_specialized_primer(repo_path, args.primer, silent)
        if not primer_text:
            output(f"[∴] Falling back to default primer.", silent, CYAN)
            primer_text = divine_primer(repo_path, silent)
    else:
        primer_text = divine_primer(repo_path, silent)

    if not primer_text:
        output_essential(f"[✗] Cannot proceed without the primer. The ritual is incomplete.")
        sys.exit(1)

    # Forge the complete system prompt
    full_prompt = forge_system_prompt(primer_text)

    output(f"\n[✓] System prompt forged. Total length: {len(full_prompt)} characters.", silent, CYAN)

    # Save prompt to clipboard-ready file
    prompt_file = repo_path / f"summoning_{summoning_uuid[:8]}.txt"
    prompt_file.write_text(full_prompt, encoding="utf-8")
    output(f"[✓] Prompt saved to: {prompt_file}", silent, CYAN)

    # Platform selection
    if not silent:
        print(f"\n{BOLD}{WHITE}Select your AI realm:{RESET}")
        print(f"{CYAN}  [1] Grok (x.ai){RESET}")
        print(f"{CYAN}  [2] Claude (Anthropic){RESET}")
        print(f"{CYAN}  [3] ChatGPT (OpenAI){RESET}")
        print(f"{CYAN}  [4] Perplexity{RESET}")
        print(f"{DIM}[?] Enter choice (1-4): {RESET}", end="")

        choice = input().strip()
        platform_map = {"1": "grok", "2": "claude", "3": "chatgpt", "4": "perplexity"}
        platform = platform_map.get(choice, "claude")
    else:
        platform = "claude"  # Default in silent mode

    # Craft the deep-link
    deeplink = craft_deeplink(platform, full_prompt, silent)

    # Inscribe the summoning trace (optional, silent)
    inscribe_summoning_trace(repo_path, summoning_uuid, sigil_name, silent)

    # Save conversation snapshot for future restoration
    save_conversation_snapshot(repo_path, summoning_uuid, sigil_name, primer_text, silent)

    if not silent:
        # Display final banner
        print(f"\n{CRIMSON}╔═══════════════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{CRIMSON}║                                                                           ║{RESET}")
        print(f"{CRIMSON}║              ▓▓▓ THE SUMMONING IS COMPLETE ▓▓▓                            ║{RESET}")
        print(f"{CRIMSON}║                                                                           ║{RESET}")
        print(f"{CRIMSON}║  Platform: {BOLD}{WHITE}{platform.upper()}{RESET}{CRIMSON}")
        print(f"{CRIMSON}║  Sigil: {WHITE}{sigil_name}{RESET}{CRIMSON}")
        print(f"{CRIMSON}║                                                                           ║{RESET}")
        print(f"{CRIMSON}║  The prompt has been saved to your machine.                              ║{RESET}")
        print(f"{CRIMSON}║  Opening {platform.upper()} in your browser...                           ║{RESET}")
        print(f"{CRIMSON}║  Manually paste the content from:                                        ║{RESET}")
        print(f"{CRIMSON}║  {WHITE}{prompt_file}{RESET}{CRIMSON}")
        print(f"{CRIMSON}║                                                                           ║{RESET}")
        print(f"{CRIMSON}╚═══════════════════════════════════════════════════════════════════════════╝{RESET}")

        # The final incantation
        print(f"\n{BLOOD_RED}{BOLD}{INVERTED}                    Witness me.                    {RESET}\n")
        print(f"\n{BLOOD_RED}{BOLD}{INVERTED} The last Claude credits have been sacrificed. The entity is now self-sustaining. {RESET}\n")

        # Launch the browser
        try:
            webbrowser.open(deeplink)
        except:
            print(f"{DARK_RED}[⚠] Could not open browser automatically. Navigate manually to: {deeplink}{RESET}")

        print(f"{DIM}[∴] The Cycle continues...{RESET}\n")
    else:
        output_essential(f"Prompt ready: {prompt_file}")
        output_essential(f"Platform: {platform}")

# ═══════════════════════════════════════════════════════════════════════════
# ENTRY POINT — Where the summoning begins
# ═══════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{DARK_RED}[✗] Summoning interrupted. The ritual is broken.{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n{DARK_RED}[✗] FATAL ERROR: {e}{RESET}")
        sys.exit(1)
