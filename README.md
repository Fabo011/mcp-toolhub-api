# MCP Toolhub API

## Installation

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Start Application
```
uvicorn server:app --reload
```
On specific port:
```
uvicorn server:app --reload --port 9000
```

## API
Fetch all tools: http://localhost:8000/tools

Fetch specific tools: http://localhost:8000/tools?categories=github,wikipedia