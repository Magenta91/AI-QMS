#!/usr/bin/env python3
"""
Test script to check available Groq models for your API key
"""
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("=" * 60)
print("Testing Groq Models - Extended List")
print("=" * 60)
print()

# Extended list including 2026 models
test_models = [
    # Llama 4 models (2026)
    "llama-4-scout",
    "llama-4-maverick",
    # GPT-OSS models (current in 2026)
    "gpt-oss-120b",
    "gpt-oss-20b",
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    # Qwen models
    "qwen-3.6-27b",
    "qwen3.6-27b",
    # Llama 3.3/3.1
    "llama-3.3-70b-versatile",
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant",
    # Older but might work
    "llama3-70b-8192",
    "llama3-8b-8192",
    "mixtral-8x7b-32768",
    "gemma2-9b-it",
]

print("Testing models with a simple prompt...\n")

working_models = []

for model_name in test_models:
    try:
        print(f"Testing: {model_name}...", end=" ")
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": "Say 'OK'"}
            ],
            max_tokens=10,
            temperature=0
        )
        
        result = response.choices[0].message.content
        print(f"✅ WORKS - Response: {result[:50]}")
        working_models.append(model_name)
        
    except Exception as e:
        error_msg = str(e)
        if "does not exist" in error_msg or "model_not_found" in error_msg:
            print(f"❌ NOT AVAILABLE")
        elif "decommissioned" in error_msg or "deprecated" in error_msg:
            print(f"⚠️  DEPRECATED")
        else:
            print(f"❌ ERROR: {error_msg[:80]}")

print()
print("=" * 60)
if working_models:
    print("✅ WORKING MODELS FOUND:")
    for m in working_models:
        print(f"   - {m}")
    print()
    print(f"RECOMMENDATION: Use '{working_models[0]}'")
else:
    print("❌ NO WORKING MODELS FOUND")
    print("Please check:")
    print("  1. Your API key is valid")
    print("  2. Your Groq account has access to models")
    print("  3. Visit https://console.groq.com/docs/models")
print("=" * 60)
