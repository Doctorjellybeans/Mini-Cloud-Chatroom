# Mini-Cloud-Chatroom

A real-time web chatroom designed as a hands-on learning project focused on cloud computing, computer networks, and distributed systems architecture.

---

## Project objective 

The main goal of this project is to learn and apply core and advanced concepts related to:
 - Cloud computing
 - Computer Networks
 - Distributed Systems Architecture
 - Real-time comunication using WenSockets
 - Proffesional development and DevOps best practices

So in coclussion yhis project is intended as a technical learning laboratory rather than a commercial product.

---

## Current scope

Initial local MVP
  - Web-based chatroom accessible via browser
  - Join a global room by entering a username (no persistent authentication)
  - Backend implemented in Python using FastAPI
  - Message persistence using PostgreSQL (local setup)

---

## Tech stack

### Backend
  - Python 3.12
  - FastAPI
  - Uvicorn
  - WebSockets

### Database
  - PostgreSQL

### Tooling
  - Git / GitHub
  - Docker
  - Terraform

## Architecture

TODO: add a diagram and update the current text version  
WebClient -> WebSocket -> FastAPI (backend) -> PostgreSQL

## Repository Structure
TODO: add diagram or add ACSII

## Running Locally

### Requierements
  - Python3.12
  - PostgreSQL

### Setup

1. Clone the repo
```git clone https://github.com/your-username/distributed-chatroom.git ```

2. Create and activate a virtual enviorment
```python -m venv "whatever_name_you_please"```
```source whatever_name_you_please/bin/activate```


3. Install dependencies 
TODO: add requirements.txt
```pip install -r backend/requirements.txt```

4. Configure enviorment variables
TODO: add env var
```export ```

5. Run the backend
```uvicorn backend.app.main:app --reload```

## Roadmap
TODO: propper roadmap
Placeholder:
- [x] Foundation
- [ ] Real-Time Messaging
- [ ] Persistence
- [ ] Frontend MVP
- [ ] Containerization
- [ ] Scalability
- [ ] Cloud Deployment
- [ ] Observability



