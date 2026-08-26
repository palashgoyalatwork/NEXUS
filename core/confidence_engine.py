class ConfidenceEngine:
    """
    Estimates how well-supported the current
    incident investigation is.
    """

    def analyze(
        self,
        incident,
        evidence_result,
        timeline_result,
        gap_result,
        cause_result,
    ):
        score = 0
        factors = []

        evidence_count = evidence_result.get(
            "evidence_count",
            0,
        )

        event_count = timeline_result.get(
            "event_count",
            0,
        )

        gap_count = gap_result.get(
            "gap_count",
            0,
        )

        causes = cause_result.get(
            "probable_causes",
            [],
        )

        # Evidence quality

        if evidence_count >= 5:
            score += 30
            factors.append(
                "Strong volume of supporting evidence"
            )
        elif evidence_count >= 3:
            score += 20
            factors.append(
                "Moderate supporting evidence available"
            )
        elif evidence_count >= 1:
            score += 10
            factors.append(
                "Limited supporting evidence available"
            )

        # Technical logs

        if incident.get("has_logs"):
            score += 20
            factors.append(
                "Technical logs were provided"
            )

        # Timeline quality

        if event_count >= 4:
            score += 20
            factors.append(
                "Clear multi-stage incident sequence"
            )
        elif event_count >= 2:
            score += 12
            factors.append(
                "Partial incident sequence identified"
            )

        # Investigation gaps

        if gap_count == 0:
            score += 15
            factors.append(
                "No major information gaps detected"
            )
        elif gap_count <= 2:
            score += 8
            factors.append(
                "Limited investigation gaps remain"
            )
        else:
            factors.append(
                "Multiple investigation gaps remain"
            )

        # Cause confidence

        high_confidence_causes = sum(
            1
            for cause in causes
            if cause.get("confidence") == "High"
        )

        if high_confidence_causes >= 2:
            score += 15
            factors.append(
                "Multiple high-confidence investigation hypotheses"
            )
        elif high_confidence_causes == 1:
            score += 10
            factors.append(
                "At least one high-confidence investigation hypothesis"
            )
        elif causes:
            score += 5
            factors.append(
                "Probable causes identified with limited confidence"
            )

        score = min(score, 100)

        confidence_level = self._get_level(score)

        return {
            "confidence_score": score,
            "confidence_level": confidence_level,
            "confidence_factors": factors,
        }

    def _get_level(self, score):

        if score >= 80:
            return "High"

        if score >= 50:
            return "Medium"

        return "Low"