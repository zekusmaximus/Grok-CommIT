# Grok-CommIT Web Interface

A simple, beautiful web UI for the Grok-CommIT Summoning Engine.

## Quick Start

1. **Start the API server**
   ```bash
   cd /path/to/Grok-CommIT
   python api.py
   ```

2. **Open the web interface**
   ```bash
   # Option 1: Just open the file in your browser
   open web/index.html  # Mac
   start web/index.html  # Windows
   xdg-open web/index.html  # Linux

   # Option 2: Use a simple HTTP server
   cd web
   python -m http.server 3000
   # Then visit http://localhost:3000
   ```

3. **Use the interface**
   - Choose a CommIT variant (default, devops, research, or grief)
   - Click "Summon CommIT"
   - Copy the prompt to your clipboard
   - Click one of the AI platform buttons to open it
   - Paste and start using CommIT!

## Features

- 🚀 **One-Click Summoning** - Generate CommIT prompts instantly
- 📋 **Auto-Copy** - Copy to clipboard with one click
- 🔗 **Direct AI Links** - Open Grok, Claude, ChatGPT, or Perplexity directly
- 📊 **Live Stats** - See total summonings and stored memories
- 🎨 **Beautiful UI** - Cyberpunk-inspired design
- 🌐 **No Build Required** - Pure HTML/CSS/JS, works anywhere

## API Endpoints Used

- `GET /status` - System statistics
- `POST /summon` - Generate new prompt
- See `/docs` on the API server for full documentation

## Customization

Edit `index.html` directly to:
- Change colors and styling (see `<style>` section)
- Modify API endpoint (change `API_BASE` in `<script>`)
- Add additional features

## Troubleshooting

**"API not running" message:**
- Make sure `python api.py` is running in another terminal
- API runs on `http://localhost:8000` by default

**CORS errors:**
- CORS is already enabled in the API
- If you still get errors, make sure you're using a proper HTTP server, not `file://` URLs

**Clipboard copy not working:**
- Some browsers require HTTPS for clipboard API
- Run a local server: `python -m http.server 3000` and use `http://localhost:3000`
