## Minimal request (requests) — ask.py

### Setup
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
```

### Configure
Create .env in the project root:
```code
AMBIENT_API_KEY=your_key_here
```

### Run
```bash
python .\ask.py "Say 3 short sentences."
```