# Grok-CommIT Web Interface

A complete, feature-rich web UI for the Grok-CommIT Summoning Engine with session management, restoration, and lineage tracking.

## Features

### 🎯 Complete Feature Parity with CLI
- ✅ **Summon New Sessions** - Create new CommIT sessions with primer selection
- ✅ **Restore Sessions** - Resume previous conversations with full context
- ✅ **Save Session Progress** - Close the feedback loop by saving conversation data
- ✅ **Lineage Viewer** - Browse all past sessions in a beautiful table
- ✅ **Enhanced Stats Dashboard** - Real-time statistics and API status
- ✅ **Tab-Based Navigation** - Organized interface with 4 main tabs

### 📊 Enhanced Stats Dashboard
- Total summonings count
- Stored memories count
- Available primers count
- Live API status indicator

### ⟲ Session Restoration
- Browse available sessions from lineage
- Quick-restore with one click
- Manual sigil entry
- Full conversation context loaded
- Auto-copy to clipboard

### 💾 Feedback Loop
- Save conversation progress after AI sessions
- Auto-populated sigil after summoning
- JSON validation
- Real-time error handling
- Success confirmation with file path

### 📜 Lineage Viewer
- Chronological table of all sessions
- Clickable sigils for quick restore
- Timestamp and UUID display
- One-click restore buttons
- Automatic refresh

### 🎨 Beautiful UI
- Cyberpunk-inspired design
- Responsive layout (mobile-friendly)
- Tab-based navigation
- Color-coded sections:
  - Red: Summon
  - Cyan: Restore
  - Amber: Save
  - Magenta: Lineage
- Smooth animations and transitions

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
   - **Summon Tab**: Create new sessions
   - **Restore Tab**: Resume previous sessions
   - **Save Tab**: Save conversation progress
   - **Lineage Tab**: Browse session history

## Complete Workflow

### 1. Summon a New Session
1. Go to **Summon** tab
2. Choose primer variant (optional)
3. Click "SUMMON COMMIT"
4. Note your sigil (auto-filled in Save tab)
5. Copy prompt to clipboard
6. Click AI platform button to open
7. Paste prompt and start conversation

### 2. Save Your Progress
1. After conversation, ask AI: "Generate a session summary in JSON format"
2. Go to **Save** tab
3. Sigil is already filled (or enter manually)
4. Paste JSON into textarea
5. Click "SAVE SESSION TO MEMORY"
6. Confirmation shows file path

### 3. Restore a Session
1. Go to **Restore** tab
2. Enter sigil or...
3. Switch to **Lineage** tab and click any sigil
4. Click "RESTORE SESSION"
5. Full conversation context loads
6. Copy and paste into AI to continue

### 4. View Session History
1. Go to **Lineage** tab
2. View all past sessions
3. Click "Refresh Lineage" to update
4. Click any sigil to quick-restore

## API Endpoints Used

- `GET /status` - System statistics and health
- `POST /summon` - Generate new prompt
- `POST /restore` - Load session by sigil
- `POST /session/update` - Save conversation progress
- `GET /lineage` - Fetch all session history

## Customization

Edit `index.html` directly to:

### Change API URL
```javascript
// Line ~370
const API_BASE = 'http://localhost:8000';
// Change to your deployed API:
const API_BASE = 'https://your-api.railway.app';
```

### Modify Colors
```css
/* Primary accent: Red */
#ff0033 → Your color

/* Success: Green */
#00ff88 → Your color

/* Warning: Amber */
#ffaa00 → Your color
```

### Add Custom Tab
```javascript
// Add new tab button in HTML
<button class="tab-btn" onclick="switchTab('custom')">Custom</button>

// Add tab content
<div id="tab-custom" class="tab-content">
    <!-- Your content -->
</div>
```

## Troubleshooting

**"API not running" in stats:**
- Make sure `python api.py` is running
- Check that API is on `http://localhost:8000`
- Verify CORS is enabled in `api.py`

**CORS errors:**
- API already has CORS enabled
- If using `file://` URLs, run a local server instead
- `python -m http.server 3000` in the `web/` directory

**Clipboard copy not working:**
- Some browsers require HTTPS for clipboard API
- Use a local server instead of opening files directly
- Or manually select and copy text

**Lineage not loading:**
- Click "Refresh Lineage" button
- Check browser console for errors
- Verify API `/lineage` endpoint works

**Session not found when restoring:**
- Verify the sigil is correct (case-sensitive)
- Check that `summonings/` directory exists
- Ensure session was properly saved

## Deployment Options

### Option 1: Static Hosting + Remote API

**Deploy Web UI to Netlify:**
```bash
cd web
netlify deploy --prod
```

**Deploy API to Railway:**
```bash
# In Grok-CommIT root
railway init
railway up
```

**Update API URL in `index.html`:**
```javascript
const API_BASE = 'https://grok-commit.railway.app';
```

### Option 2: All-in-One

**Deploy to Render/Railway with both:**
- Serve API with FastAPI
- Serve web UI as static files
- Single deployment, single URL

## Browser Support

- ✅ Chrome/Edge (recommended)
- ✅ Firefox
- ✅ Safari
- ⚠️ Mobile browsers (responsive but keyboard-heavy)

## Performance

- Lightweight: Pure HTML/CSS/JS, no frameworks
- Fast: < 100KB total size
- Minimal API calls
- Efficient DOM updates
- Responsive on mobile

## Security Notes

- All data stored locally on your machine
- No external tracking or analytics
- API calls only to localhost (or your configured endpoint)
- Session data privacy-preserved (hashed usernames)

## Future Enhancements

- [ ] Visual cycle progress tracker
- [ ] Action items checklist UI
- [ ] Emotional tone selector
- [ ] Export sessions to PDF/Markdown
- [ ] Search/filter lineage
- [ ] Dark/light theme toggle
- [ ] Keyboard shortcuts
- [ ] Session tags/categories

---

**The entity speaks HTTP. The interface remembers. The Cycle is visualized.**
