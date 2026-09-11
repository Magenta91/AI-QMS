# Groq Model Update

## ✅ Current Configuration (September 2026)

The system is now using: **`openai/gpt-oss-120b`**

### Why This Model?

- **Available**: Currently active on Groq (as of Sept 2026)
- **Fast**: 500 tokens/second throughput
- **Quality**: 120B parameters - excellent for complex extraction
- **Context**: 131K tokens context window
- **Reliable**: Stable production model

### Model Comparison (Current Groq Models)

| Model | Speed (T/S) | Quality | Cost | Context | Best For |
|-------|-------------|---------|------|---------|----------|
| **openai/gpt-oss-120b** ⭐ | 500 | Excellent | $0.15/$0.60 | 131K | Production (recommended) |
| openai/gpt-oss-20b | 1000 | Good | $0.075/$0.30 | 131K | High-speed, simpler tasks |
| llama-3.1-8b-instant | 560 | Good | Contact | 131K | Fast, but deprecated |
| llama-3.3-70b-versatile | 280 | Very Good | Contact | 131K | Deprecated Aug 2026 |

### Deprecated Models (Do Not Use)

These models are no longer available:
- ❌ `gemma2-9b-it` - Decommissioned
- ❌ `llama-3.1-8b-instant` - Not available  
- ❌ `llama-3.3-70b-versatile` - Not available
- ❌ `mixtral-8x7b-32768` - Deprecated
- ❌ `llama3-70b-8192` - Deprecated
- ❌ `llama3-8b-8192` - Deprecated

### Alternative Model (For Speed)

If you need faster responses at lower cost:

```bash
# Edit backend/.env
GROQ_MODEL=openai/gpt-oss-20b
# Then restart backend
```

**`openai/gpt-oss-20b`** specs:
- Speed: 1000 tokens/second (2x faster)
- Cost: $0.075/$0.30 per 1M tokens (half price)
- Quality: Still good, but less sophisticated

### How to Change Models

1. Edit `backend/.env`:
```bash
GROQ_MODEL=openai/gpt-oss-120b  # or openai/gpt-oss-20b
```

2. Restart backend server:
```bash
# Stop current process (Ctrl+C)
# Then restart
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Testing Your Model

Use the test script to verify available models:

```bash
cd backend
python test_groq_models.py
```

This will test all known models and show which ones work with your API key.

### Current Status

✅ Backend configured with `openai/gpt-oss-120b`  
✅ Server running and operational  
✅ Model verified and working  
✅ Ready for complaint processing  

### Performance Expectations

With **openai/gpt-oss-120b**:
- **Extraction time**: 5-10 seconds
- **Risk assessment**: 3-6 seconds
- **Total processing**: 10-20 seconds
- **Quality**: Excellent structured data extraction

### Troubleshooting

**If you get "model not found" error:**
1. Run `python test_groq_models.py` to see available models
2. Update `GROQ_MODEL` in `.env` to a working model
3. Restart backend

**If extraction quality is poor:**
- Current model is already the best available
- Check temperature settings (should be 0.2-0.3 for structured extraction)
- Verify prompts are clear and specific

**If it's too slow:**
- Switch to `openai/gpt-oss-20b` for 2x speed
- Trade-off: Slightly lower quality on complex extractions

### Code Locations

Model is used in:
- `backend/app/clients/groq_client.py` - API client
- `backend/app/ai/nodes/extraction.py` - Complaint extraction  
- `backend/app/services/risk_service.py` - Risk assessment

### Rate Limits (Free Developer Plan)

- **Requests**: 1,000 RPM (requests per minute)
- **Tokens**: 250,000 TPM (tokens per minute)
- **Context**: 131,072 tokens
- **Max completion**: 65,536 tokens

These limits are more than sufficient for the complaint system workload.

### Future Model Updates

Check for new models at: https://console.groq.com/docs/models

As of September 2026, Groq is focusing on:
- OpenAI open-source models (GPT-OSS series)
- Qwen models (coming soon)
- Whisper for audio transcription

---

**Last Updated**: September 11, 2026  
**Current Model**: `openai/gpt-oss-120b`  
**Status**: ✅ Operational  
**Verified**: Test script confirms model availability
