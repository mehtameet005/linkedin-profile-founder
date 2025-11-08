"""
Scoring Service - Score and rank candidates with explainability
"""
from typing import Dict, List
import logging
import numpy as np

logger = logging.getLogger(__name__)


class ScoringService:
    """Service for scoring candidates and providing explainability"""

    def __init__(self):
        # Default weights (can be tuned via feedback)
        self.weights = {
            "semantic": 0.55,
            "role": 0.20,
            "industry": 0.15,
            "geo": 0.10,
        }

    def score_candidate(
        self, candidate: Dict, persona: Dict, icp: Dict
    ) -> Dict[str, any]:
        """
        Score a candidate against persona and ICP

        Args:
            candidate: Candidate profile data
            persona: Target persona
            icp: Ideal customer profile

        Returns:
            Dictionary with scores and explainability data
        """
        # Calculate individual score components
        semantic_score = self._calculate_semantic_similarity(
            candidate.get("result_snippet", ""), persona
        )
        role_score = self._calculate_role_match(
            candidate.get("inferred_title", ""), persona.get("titles", [])
        )
        industry_score = self._calculate_industry_match(candidate, icp)
        geo_score = self._calculate_geo_relevance(
            candidate.get("inferred_location"), icp
        )

        # Calculate final weighted score
        final_score = (
            self.weights["semantic"] * semantic_score
            + self.weights["role"] * role_score
            + self.weights["industry"] * industry_score
            + self.weights["geo"] * geo_score
        )

        # Generate explainability data
        keywords_matched = self._extract_matched_keywords(
            candidate.get("result_snippet", ""), persona
        )

        return {
            "scores": {
                "semantic": round(semantic_score, 3),
                "role": round(role_score, 3),
                "industry": round(industry_score, 3),
                "geo": round(geo_score, 3),
                "final": round(final_score, 3),
            },
            "explainability": {
                "keywords_matched": keywords_matched,
                "feature_contributions": {
                    "semantic": round(self.weights["semantic"] * semantic_score, 3),
                    "role": round(self.weights["role"] * role_score, 3),
                    "industry": round(self.weights["industry"] * industry_score, 3),
                    "geo": round(self.weights["geo"] * geo_score, 3),
                },
            },
        }

    def _calculate_semantic_similarity(self, text: str, persona: Dict) -> float:
        """
        Calculate semantic similarity between candidate snippet and persona

        TODO: Implement with actual embeddings
        For now, using simple keyword overlap
        """
        text_lower = text.lower()
        keywords = persona.get("keywords", [])

        if not keywords:
            return 0.5

        matches = sum(1 for kw in keywords if kw.lower() in text_lower)
        return min(matches / len(keywords), 1.0)

    def _calculate_role_match(self, candidate_title: str, persona_titles: List[str]) -> float:
        """Calculate role/title match score"""
        if not candidate_title or not persona_titles:
            return 0.3

        candidate_title_lower = candidate_title.lower()

        # Check for exact or partial matches
        for persona_title in persona_titles:
            persona_title_lower = persona_title.lower()

            if persona_title_lower in candidate_title_lower:
                return 1.0

            # Check for partial word matches
            persona_words = set(persona_title_lower.split())
            candidate_words = set(candidate_title_lower.split())
            overlap = len(persona_words & candidate_words)

            if overlap > 0:
                return min(overlap / len(persona_words), 0.8)

        return 0.2

    def _calculate_industry_match(self, candidate: Dict, icp: Dict) -> float:
        """Calculate industry relevance score"""
        # TODO: Implement based on company information
        # For now, return a default score
        return 0.5

    def _calculate_geo_relevance(self, candidate_location: str, icp: Dict) -> float:
        """Calculate geographic relevance score"""
        if not candidate_location:
            return 0.5

        # TODO: Implement location matching logic
        return 0.7

    def _extract_matched_keywords(self, text: str, persona: Dict) -> List[str]:
        """Extract keywords that matched in the candidate text"""
        text_lower = text.lower()
        keywords = persona.get("keywords", [])

        matched = [kw for kw in keywords if kw.lower() in text_lower]

        # Also check for persona goals and pains
        for goal in persona.get("goals", []):
            if goal.lower() in text_lower:
                matched.append(goal)

        return list(set(matched))[:10]  # Limit to top 10

    def update_weights(self, new_weights: Dict[str, float]):
        """Update scoring weights based on feedback"""
        # Validate that weights sum to ~1.0
        total = sum(new_weights.values())
        if abs(total - 1.0) > 0.01:
            raise ValueError("Weights must sum to 1.0")

        self.weights.update(new_weights)
        logger.info(f"Updated scoring weights: {self.weights}")


# Singleton instance
scoring_service = ScoringService()
