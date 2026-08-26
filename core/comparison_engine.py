class ComparisonEngine:
    """
    Compares two completed NEXUS incident analyses
    and identifies meaningful changes and similarities.
    """

    def compare(
        self,
        previous,
        current,
    ):
        previous_severity = previous.get(
            "severity",
            {},
        )

        current_severity = current.get(
            "severity",
            {},
        )

        previous_confidence = previous.get(
            "confidence",
            {},
        )

        current_confidence = current.get(
            "confidence",
            {},
        )

        severity_change = (
            current_severity.get(
                "severity_score",
                0,
            )
            - previous_severity.get(
                "severity_score",
                0,
            )
        )

        confidence_change = (
            current_confidence.get(
                "confidence_score",
                0,
            )
            - previous_confidence.get(
                "confidence_score",
                0,
            )
        )

        previous_systems = set(
            previous.get(
                "incident",
                {},
            ).get(
                "affected_systems",
                [],
            )
        )

        current_systems = set(
            current.get(
                "incident",
                {},
            ).get(
                "affected_systems",
                [],
            )
        )

        common_systems = sorted(
            previous_systems
            & current_systems
        )

        previous_causes = {
            cause.get("cause")
            for cause in previous.get(
                "causes",
                {},
            ).get(
                "probable_causes",
                [],
            )
        }

        current_causes = {
            cause.get("cause")
            for cause in current.get(
                "causes",
                {},
            ).get(
                "probable_causes",
                [],
            )
        }

        new_causes = sorted(
            current_causes
            - previous_causes
        )

        removed_causes = sorted(
            previous_causes
            - current_causes
        )

        previous_evidence = {
            item.get("evidence")
            for item in previous.get(
                "evidence",
                {},
            ).get(
                "evidence",
                [],
            )
        }

        current_evidence = {
            item.get("evidence")
            for item in current.get(
                "evidence",
                {},
            ).get(
                "evidence",
                [],
            )
        }

        shared_evidence = sorted(
            previous_evidence
            & current_evidence
        )

        similarity_score = self._similarity(
            previous_systems,
            current_systems,
            previous_causes,
            current_causes,
            previous_evidence,
            current_evidence,
        )

        return {
            "previous_severity_score": previous_severity.get(
                "severity_score",
                0,
            ),
            "current_severity_score": current_severity.get(
                "severity_score",
                0,
            ),
            "severity_change": severity_change,
            "severity_trend": self._trend(
                severity_change
            ),
            "previous_confidence_score": previous_confidence.get(
                "confidence_score",
                0,
            ),
            "current_confidence_score": current_confidence.get(
                "confidence_score",
                0,
            ),
            "confidence_change": confidence_change,
            "common_systems": common_systems,
            "shared_evidence": shared_evidence,
            "new_causes": new_causes,
            "removed_causes": removed_causes,
            "similarity_score": similarity_score,
            "summary": self._summary(
                severity_change,
                common_systems,
                new_causes,
                similarity_score,
            ),
        }

    def _trend(self, change):

        if change > 0:
            return "Severity Increased"

        if change < 0:
            return "Severity Decreased"

        return "Severity Unchanged"

    def _similarity(
        self,
        previous_systems,
        current_systems,
        previous_causes,
        current_causes,
        previous_evidence,
        current_evidence,
    ):
        groups = [
            (
                previous_systems,
                current_systems,
            ),
            (
                previous_causes,
                current_causes,
            ),
            (
                previous_evidence,
                current_evidence,
            ),
        ]

        scores = []

        for previous_set, current_set in groups:

            union = previous_set | current_set

            if not union:
                continue

            intersection = (
                previous_set
                & current_set
            )

            scores.append(
                len(intersection)
                / len(union)
            )

        if not scores:
            return 0

        return round(
            sum(scores)
            / len(scores)
            * 100
        )

    def _summary(
        self,
        severity_change,
        common_systems,
        new_causes,
        similarity_score,
    ):
        parts = []

        if severity_change > 0:
            parts.append(
                f"Severity increased by "
                f"{severity_change} points"
            )
        elif severity_change < 0:
            parts.append(
                f"Severity decreased by "
                f"{abs(severity_change)} points"
            )
        else:
            parts.append(
                "Severity remained unchanged"
            )

        if common_systems:
            parts.append(
                f"{len(common_systems)} shared "
                f"affected system(s)"
            )

        if new_causes:
            parts.append(
                f"{len(new_causes)} new probable "
                f"cause(s)"
            )

        parts.append(
            f"{similarity_score}% overall similarity"
        )

        return ". ".join(parts) + "."