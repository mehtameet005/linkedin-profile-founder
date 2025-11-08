"""
ICP Generator Service - Generate Ideal Customer Profiles and Personas
"""
from typing import Dict, List
import logging
import json
from anthropic import AsyncAnthropic
from app.core.config import settings

logger = logging.getLogger(__name__)


class ICPGeneratorService:
    """Service for generating ICPs and buyer personas"""

    def __init__(self):
        self.anthropic_client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    async def generate_icp(self, website_analysis: Dict, website_url: str) -> Dict:
        """
        Generate an Ideal Customer Profile from website analysis

        Args:
            website_analysis: Analysis results from NLP service
            website_url: The original website URL

        Returns:
            ICP data structure
        """
        prompt = f"""Based on this business website analysis, generate a detailed Ideal Customer Profile (ICP).

Website URL: {website_url}
Analysis: {json.dumps(website_analysis, indent=2)}

Generate a JSON response with the following structure:
{{
  "company_name": "extracted or inferred company name",
  "industry": "primary industry",
  "sub_industries": ["sub-industry-1", "sub-industry-2"],
  "firmographics": {{
    "employee_range": "e.g., 100-500",
    "revenue_band": "e.g., $10M-$50M"
  }},
  "value_props": ["value proposition 1", "value proposition 2"],
  "pain_points": ["pain point 1", "pain point 2"],
  "trigger_events": ["trigger event 1", "trigger event 2"],
  "tech_stack": {{
    "category": "technology"
  }}
}}

Respond ONLY with valid JSON, no other text."""

        try:
            message = await self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}],
            )

            # Parse JSON response
            response_text = message.content[0].text
            icp_data = json.loads(response_text)

            return icp_data

        except Exception as e:
            logger.error(f"Error generating ICP: {str(e)}")
            raise

    async def generate_personas(self, icp_data: Dict) -> List[Dict]:
        """
        Generate buyer personas from an ICP

        Args:
            icp_data: The ICP data structure

        Returns:
            List of persona data structures
        """
        prompt = f"""Based on this Ideal Customer Profile, generate 2-4 detailed buyer personas.

ICP Data: {json.dumps(icp_data, indent=2)}

For each persona, provide:
{{
  "persona_name": "e.g., VP of Sales",
  "titles": ["job title 1", "job title 2"],
  "goals": ["goal 1", "goal 2"],
  "pains": ["pain 1", "pain 2"],
  "kpis": ["kpi 1", "kpi 2"],
  "keywords": ["keyword 1", "keyword 2"]
}}

Respond with a JSON array of personas. ONLY valid JSON, no other text."""

        try:
            message = await self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=3000,
                messages=[{"role": "user", "content": prompt}],
            )

            response_text = message.content[0].text
            personas = json.loads(response_text)

            return personas if isinstance(personas, list) else [personas]

        except Exception as e:
            logger.error(f"Error generating personas: {str(e)}")
            raise


# Singleton instance
icp_generator_service = ICPGeneratorService()
