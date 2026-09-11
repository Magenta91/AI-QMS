# AIVOA Complaint Management System — Starter

This starter implements the planned modular-monolith architecture for the AIVOA AI Product Engineer assignment.

## Stack
React + Redux Toolkit + Vite | Python + FastAPI | LangGraph | Groq/Gemma 2 9B IT | PostgreSQL

## Architecture
React/Redux -> FastAPI -> Services -> LangGraph/AI -> Repositories -> PostgreSQL

Services are logical modules inside one FastAPI deployment, not separate network microservices. This keeps the project simple while making each service independently testable and future-microservice-ready.

## Build order
1. Backend health
2. PostgreSQL
3. Service/repository skeleton
4. React UI
5. React <-> FastAPI
6. Mock extraction
7. Groq
8. LangGraph
9. PDF
10. Conversational correction
11. Risk assessment
12. Bonus features
13. Tests, README and demo

See AGENT_PROMPT.md for the complete Kiro/IDE-agent implementation brief.
