"""
NLP Service - Text analysis and processing
"""
from typing import Dict, List
import logging
from anthropic import AsyncAnthropic
from app.core.config import settings

logger = logging.getLogger(__name__)


class NLPService:
    """Service for natural language processing tasks"""

    def __init__(self):
        self.anthropic_client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    async def analyze_website_content(self, content_data: Dict) -> Dict:
        """
        Analyze website content to extract business insights

        Args:
            content_data: Dictionary containing crawled website data

        Returns:
            Dictionary with analysis results
        """
        # Prepare content for analysis
        text_content = self._prepare_content(content_data)

        prompt = f"""Analyze this business website content and extract:

1. Industry and sub-industries
2. Company value propositions
3. Customer pain points addressed
4. Technology stack indicators
5. Target market signals

Website Content:
{text_content}

Provide a structured JSON response."""

        try:
            message = await self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}],
            )

            # Parse and return the response
            # TODO: Proper JSON parsing and validation
            return {"raw_analysis": message.content[0].text}

        except Exception as e:
            logger.error(f"Error in NLP analysis: {str(e)}")
            raise

    def _prepare_content(self, content_data: Dict) -> str:
        """Prepare content for analysis"""
        parts = []

        if content_data.get("title"):
            parts.append(f"Title: {content_data['title']}")

        if content_data.get("meta_description"):
            parts.append(f"Description: {content_data['meta_description']}")

        if content_data.get("headings"):
            parts.append("Headings: " + " | ".join(content_data["headings"][:10]))

        if content_data.get("paragraphs"):
            parts.append("Content: " + " ".join(content_data["paragraphs"][:20]))

        return "\n\n".join(parts)[:4000]  # Limit length


# Singleton instance
nlp_service = NLPService()
