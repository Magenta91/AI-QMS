# Demo checklist

## Product demo
1. Paste complaint.
2. Process it.
3. Show extracted fields.
4. Show completeness/validation.
5. Show AI risk.
6. Correct a field via chat.
7. Upload complaint PDF.
8. Show extraction.
9. Save to PostgreSQL.

## Code walkthrough
React -> Redux -> FastAPI endpoint -> Service -> LangGraph node -> AIService/GroqClient -> Repository -> PostgreSQL.

Be ready to explain why the project uses a modular monolith instead of network microservices.
