class GapEngine:
    """
    Identifies missing investigation information
    needed to improve incident confidence.
    """

    def analyze(
        self,
        incident,
        evidence_result,
        timeline_result,
    ):
        gaps = []

        description = incident.get(
            "description",
            "",
        ).lower()

        logs = incident.get(
            "logs",
            "",
        ).strip()

        environment = incident.get(
            "environment",
            "",
        ).strip()

        affected_systems = incident.get(
            "affected_systems",
            [],
        )

        evidence_count = evidence_result.get(
            "evidence_count",
            0,
        )

        event_count = timeline_result.get(
            "event_count",
            0,
        )

        if not logs:

            gaps.append(
                {
                    "gap": "Technical logs are missing",
                    "priority": "High",
                    "why": (
                        "Logs can provide direct evidence "
                        "about errors, failures, and affected "
                        "dependencies."
                    ),
                    "question": (
                        "What relevant application, server, "
                        "or infrastructure logs are available?"
                    ),
                }
            )

        if not environment:

            gaps.append(
                {
                    "gap": "Environment is not specified",
                    "priority": "Medium",
                    "why": (
                        "The impact and investigation path "
                        "can differ between development, "
                        "staging, and production."
                    ),
                    "question": (
                        "Which environment is affected?"
                    ),
                }
            )

        if (
            not affected_systems
            or affected_systems == [
                "System not clearly identified"
            ]
        ):

            gaps.append(
                {
                    "gap": "Affected system is unclear",
                    "priority": "High",
                    "why": (
                        "Investigation scope cannot be "
                        "reliably determined."
                    ),
                    "question": (
                        "Which service, component, or "
                        "dependency is affected?"
                    ),
                }
            )

        time_indicators = [
            "when",
            "after",
            "before",
            "minutes",
            "hours",
            "today",
            "yesterday",
            "timestamp",
        ]

        if not any(
            indicator in description
            for indicator in time_indicators
        ):

            gaps.append(
                {
                    "gap": "Incident timing is unclear",
                    "priority": "Medium",
                    "why": (
                        "Without timing information it is "
                        "harder to correlate failures with "
                        "deployments or infrastructure events."
                    ),
                    "question": (
                        "When did the incident begin, and "
                        "what changed around that time?"
                    ),
                }
            )

        if evidence_count < 3:

            gaps.append(
                {
                    "gap": "Limited supporting evidence",
                    "priority": "Medium",
                    "why": (
                        "Few independent signals reduce "
                        "confidence in the investigation."
                    ),
                    "question": (
                        "Can additional logs, metrics, error "
                        "messages, or observations be provided?"
                    ),
                }
            )

        if event_count < 2:

            gaps.append(
                {
                    "gap": "Incident sequence is incomplete",
                    "priority": "Low",
                    "why": (
                        "A clearer sequence can help identify "
                        "the earliest failure point."
                    ),
                    "question": (
                        "What happened immediately before and "
                        "after the failure began?"
                    ),
                }
            )

        return {
            "investigation_gaps": gaps,
            "gap_count": len(gaps),
        }