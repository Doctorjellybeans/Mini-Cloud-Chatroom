A real-time web chatroom designed as a hands-on learning project focused on cloud computing, computer networks, and distributed systems architecture.

---

## Table of Contents
- Project Objective
- Current Scope
- Tech Stack
- Architecture
- Repository Structure
- Running Locally
- Roadmap
- Useful Resources

## Project Objective 

The main goal of this project is to learn and apply core and advanced concepts related to:

 - Cloud computing
 - Computer Networks
 - Distributed Systems Architecture
 - Real-time comunication using WenSockets
 - Proffesional development and DevOps best practices

The focus is on understanding system design decisions and implementation trade-offs rather than delivering a production-ready product.

---

## Current Scope

**Initial local MVP**
  - Web-based chatroom accessible via browser
  - Join a global room by entering a username (no persistent authentication)
  - Backend implemented in Python using FastAPI
  - Message persistence using PostgreSQL (local setup)

---

## Tech Stack

### Backend
  - Python <= v3.12
  - FastAPI <= v0.124.4
  - Uvicorn  <= v0.38.0
  - WebSockets <= v15.0.1 

### Database
  - PostgreSQL <= v16.11

### Tooling
  - Git <= v2.43.0
  - Docker <= v28.3.3
  - Terraform <= v1.14.2

## Architecture
**High-level system overview**
[![System-Context.png](https://i.postimg.cc/FRNyGfXs/System-Context.png)](https://postimg.cc/94gwQQfv)
WebClient -> WebSocket -> FastAPI (backend) -> PostgreSQL

## Repository Structure
TODO: add diagram or add ACSII

## Running Locally

### Requierements
  - Python
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
- [ ] Foundation
- [ ] Real-Time Messaging
- [ ] Message Persistence
- [ ] User Identity
- [ ] Frontend MVP
- [ ] Containerization
- [ ] Cloud Deployment
- [ ] Production Readiness (Lite)

## Useful resources

Diagrams:
- System Context Diagram guide: https://www.geeksforgeeks.org/system-design/context-diagrams/

