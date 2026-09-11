# Architecture

Use a modular monolith with clear service boundaries.

React/Redux
 -> FastAPI routes
 -> Services
 -> LangGraph / AI where applicable
 -> Repositories
 -> PostgreSQL

Services:
- ComplaintService
- DocumentService
- AIService
- RiskService
- DuplicateService (bonus)

Keep BaseService/BaseRepository intentionally small.

This avoids unnecessary distributed-system complexity while allowing isolated debugging and future extraction of a service into a real microservice.
