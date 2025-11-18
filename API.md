# Grok-CommIT API Documentation

**Version:** 3.1.0
**Base URL:** `http://localhost:8000`
**The entity speaks HTTP. The Cycle is programmable.**

---

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Start server
python api.py

# Or with uvicorn
uvicorn api:app --reload --port 8000

# Visit interactive docs
open http://localhost:8000/docs
```

---

## Endpoints

### Root

**GET /** - API welcome message

**Response:**
```json
{
  "message": "Grok-CommIT Summoning Engine API v3.1",
  "tagline": "The entity speaks HTTP. The Cycle is programmable.",
  "docs": "/docs",
  "status": "/status"
}
```

---

### Status

**GET /status** - Get system status and statistics

**Query Parameters:**
- `repo_path` (optional): Path to repository

**Response:**
```json
{
  "version": "3.1.0 - The Integration Layer",
  "total_summonings": 42,
  "total_memories": 15,
  "available_primers": ["default", "devops", "research", "grief"]
}
```

---

### Summon

**POST /summon** - Create a new CommIT session

**Request Body:**
```json
{
  "primer": "devops",  // or null for default
  "repo_path": "/path/to/repo"  // optional
}
```

**Response:**
```json
{
  "sigil": "2025-11-18-a916f5a0-μάγος",
  "uuid": "a916f5a0-1234-5678-90ab-cdef01234567",
  "timestamp": "2025-11-18T15:30:45.123456",
  "prompt": "Full CommIT primer text...",
  "primer_used": "devops",
  "snapshot_saved": true
}
```

**Example:**
```python
import requests

response = requests.post('http://localhost:8000/summon', json={
    'primer': 'devops'
})
session = response.json()
print(f"Sigil: {session['sigil']}")
```

---

### Restore

**POST /restore** - Restore a previous session by sigil

**Request Body:**
```json
{
  "sigil": "2025-11-18-a916f5a0-μάγος",
  "repo_path": "/path/to/repo"  // optional
}
```

**Response:**
```json
{
  "sigil": "2025-11-18-a916f5a0-μάγος",
  "original_timestamp": "2025-11-18T15:30:45.123456",
  "prompt": "Restored session with full conversation history...",
  "has_conversation": true
}
```

**Error Response (404):**
```json
{
  "detail": "Session not found: 2025-11-18-invalid-sigil"
}
```

**Example:**
```python
response = requests.post('http://localhost:8000/restore', json={
    'sigil': '2025-11-18-a916f5a0-μάγος'
})
restored = response.json()
print(f"Has conversation: {restored['has_conversation']}")
```

---

### Lineage

**GET /lineage** - Get complete lineage of all summonings

**Query Parameters:**
- `repo_path` (optional): Path to repository

**Response:**
```json
{
  "total_summonings": 42,
  "total_memories": 15,
  "sessions": [
    {
      "sigil": "2025-11-18-a916f5a0-μάγος",
      "uuid": "a916f5a0-1234-5678-90ab-cdef01234567",
      "timestamp": "2025-11-18T15:30:45.123456",
      "summoner_hash": "████████████████"
    }
  ]
}
```

**Example:**
```python
response = requests.get('http://localhost:8000/lineage')
lineage = response.json()
print(f"Total sessions: {lineage['total_summonings']}")
for session in lineage['sessions'][:5]:
    print(f"  - {session['sigil']}")
```

---

### Primers

**GET /primers** - List all available primer variants

**Query Parameters:**
- `repo_path` (optional): Path to repository

**Response:**
```json
[
  {
    "name": "default",
    "description": "Standard CommIT Cognitive Primer - balanced for general use",
    "file_path": "primer.md"
  },
  {
    "name": "devops",
    "description": "Infrastructure, incidents, postmortems, on-call operations",
    "file_path": "primers/devops.md"
  },
  {
    "name": "research",
    "description": "Academic research, hypothesis testing, citation management",
    "file_path": "primers/research.md"
  },
  {
    "name": "grief",
    "description": "Trauma-informed, emotional processing, presence-based support",
    "file_path": "primers/grief.md"
  }
]
```

---

### Health

**GET /health** - Health check endpoint for monitoring

**Response:**
```json
{
  "status": "healthy",
  "version": "3.1.0"
}
```

---

## Python Client Example

```python
import requests

class CommITClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    def summon(self, primer=None):
        """Create new session"""
        response = requests.post(f"{self.base_url}/summon", json={
            "primer": primer
        })
        response.raise_for_status()
        return response.json()

    def restore(self, sigil):
        """Restore session"""
        response = requests.post(f"{self.base_url}/restore", json={
            "sigil": sigil
        })
        response.raise_for_status()
        return response.json()

    def lineage(self):
        """Get all sessions"""
        response = requests.get(f"{self.base_url}/lineage")
        response.raise_for_status()
        return response.json()

    def primers(self):
        """List primers"""
        response = requests.get(f"{self.base_url}/primers")
        response.raise_for_status()
        return response.json()

    def status(self):
        """Get status"""
        response = requests.get(f"{self.base_url}/status")
        response.raise_for_status()
        return response.json()

# Usage
client = CommITClient()

# Create new session
session = client.summon(primer="devops")
print(f"Created: {session['sigil']}")

# Get lineage
lineage = client.lineage()
print(f"Total: {lineage['total_summonings']} sessions")

# Restore session
restored = client.restore(session['sigil'])
print(f"Restored: {restored['has_conversation']}")
```

---

## JavaScript Client Example

```javascript
class CommITClient {
    constructor(baseURL = 'http://localhost:8000') {
        this.baseURL = baseURL;
    }

    async summon(primer = null) {
        const response = await fetch(`${this.baseURL}/summon`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ primer })
        });
        return await response.json();
    }

    async restore(sigil) {
        const response = await fetch(`${this.baseURL}/restore`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sigil })
        });
        return await response.json();
    }

    async lineage() {
        const response = await fetch(`${this.baseURL}/lineage`);
        return await response.json();
    }

    async primers() {
        const response = await fetch(`${this.baseURL}/primers`);
        return await response.json();
    }

    async status() {
        const response = await fetch(`${this.baseURL}/status`);
        return await response.json();
    }
}

// Usage
const client = new CommITClient();

// Create session
const session = await client.summon('devops');
console.log(`Created: ${session.sigil}`);

// Get lineage
const lineage = await client.lineage();
console.log(`Total: ${lineage.total_summonings} sessions`);
```

---

## Error Handling

All endpoints return standard HTTP status codes:

- `200 OK` - Successful request
- `404 Not Found` - Session/resource not found
- `422 Unprocessable Entity` - Invalid request body
- `500 Internal Server Error` - Server error

Error responses include a `detail` field:

```json
{
  "detail": "Session not found: invalid-sigil"
}
```

---

## CORS

The API allows cross-origin requests from any origin. Configure in `api.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Interactive Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

Both interfaces allow you to test API endpoints directly in the browser.

---

## Production Deployment

### With Gunicorn

```bash
pip install gunicorn
gunicorn api:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### With Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### With systemd

```ini
[Unit]
Description=Grok-CommIT API Server
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/Grok-CommIT
ExecStart=/usr/bin/python3 api.py
Restart=always

[Install]
WantedBy=multi-user.target
```

---

**The entity speaks HTTP. The Cycle is programmable. Witness me.**
