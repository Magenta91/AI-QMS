from groq import Groq
from app.core.config import settings
from app.core.logging import get_logger
from typing import List, Dict, Any, Optional

logger = get_logger("GROQ")

class GroqClient:
    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key)
        self.model = settings.groq_model

    def chat(self, messages: list[dict], **kwargs):
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            **kwargs,
        )

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Async chat completion wrapper"""
        try:
            logger.info(f"Calling Groq API with model {self.model}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            content = response.choices[0].message.content
            
            return {
                "content": content,
                "model": response.model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
        except Exception as e:
            logger.error(f"Groq API error: {str(e)}")
            raise
