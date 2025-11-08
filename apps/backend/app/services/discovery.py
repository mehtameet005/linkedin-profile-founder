"""
Discovery Service - Search for LinkedIn profiles using search engines
"""
from typing import Dict, List
import logging
import httpx
from app.core.config import settings

logger = logging.getLogger(__name__)


class DiscoveryService:
    """Service for discovering LinkedIn profiles via search APIs"""

    def __init__(self):
        self.google_api_key = settings.GOOGLE_API_KEY
        self.google_cse_id = settings.GOOGLE_CSE_ID

    async def search_profiles(
        self, persona: Dict, location: str = None, limit: int = 10
    ) -> List[Dict]:
        """
        Search for LinkedIn profiles matching a persona

        Args:
            persona: Persona data with titles, keywords, etc.
            location: Optional location filter
            limit: Maximum number of results

        Returns:
            List of candidate profile data
        """
        queries = self._build_search_queries(persona, location)
        all_results = []

        async with httpx.AsyncClient() as client:
            for query in queries[:3]:  # Limit to 3 queries per persona
                try:
                    results = await self._execute_google_search(client, query, limit)
                    all_results.extend(results)
                except Exception as e:
                    logger.error(f"Search error for query '{query}': {str(e)}")
                    continue

        # Deduplicate by LinkedIn URL
        seen_urls = set()
        unique_results = []
        for result in all_results:
            url = result.get("linkedin_url")
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)

        return unique_results[:limit]

    def _build_search_queries(self, persona: Dict, location: str = None) -> List[str]:
        """Build optimized search queries for a persona"""
        queries = []
        titles = persona.get("titles", [])[:2]
        keywords = persona.get("keywords", [])[:3]

        for title in titles:
            # Basic title + location query
            query_parts = [f'site:linkedin.com/in/ "{title}"']

            if location:
                query_parts.append(f'"{location}"')

            # Add primary keywords
            if keywords:
                query_parts.append(f'"{keywords[0]}"')

            queries.append(" ".join(query_parts))

        return queries

    async def _execute_google_search(
        self, client: httpx.AsyncClient, query: str, limit: int
    ) -> List[Dict]:
        """Execute a Google Custom Search API request"""
        if not self.google_api_key or not self.google_cse_id:
            logger.warning("Google API credentials not configured")
            return []

        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": self.google_api_key,
            "cx": self.google_cse_id,
            "q": query,
            "num": min(limit, 10),  # Google allows max 10 per request
        }

        try:
            response = await client.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()

            results = []
            for item in data.get("items", []):
                results.append(
                    {
                        "linkedin_url": item["link"],
                        "title": item.get("title", ""),
                        "snippet": item.get("snippet", ""),
                        "query": query,
                    }
                )

            return results

        except httpx.HTTPError as e:
            logger.error(f"HTTP error in Google search: {str(e)}")
            return []

    def parse_profile_snippet(self, snippet_data: Dict) -> Dict:
        """Parse snippet data to extract profile information"""
        snippet = snippet_data.get("snippet", "")
        title_text = snippet_data.get("title", "")

        # Simple parsing (can be enhanced with NLP)
        parts = title_text.split(" - ")

        return {
            "linkedin_url": snippet_data["linkedin_url"],
            "inferred_name": parts[0] if parts else None,
            "inferred_title": parts[1] if len(parts) > 1 else None,
            "inferred_company": parts[2] if len(parts) > 2 else None,
            "result_snippet": snippet,
            "inferred_location": self._extract_location(snippet),
        }

    def _extract_location(self, text: str) -> str | None:
        """Simple location extraction from snippet"""
        # TODO: Implement more sophisticated location extraction
        # For now, just return None
        return None


# Singleton instance
discovery_service = DiscoveryService()
