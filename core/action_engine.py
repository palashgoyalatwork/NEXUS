class ActionEngine:
    """
    Generates prioritized investigation and response
    actions from incident intelligence.
    """

    def analyze(
        self,
        incident,
        severity_result,
        cause_result,
        gap_result,
    ):
        actions = []

        severity_level = severity_result.get(
            "severity_level",
            "Low",
        )

        severity_score = severity_result.get(
            "severity_score",
            0,
        )

        # Immediate severity response

        if severity_level == "Critical":

            actions.append(
                {
                    "priority": 1,
                    "action": (
                        "Begin immediate incident "
                        "investigation and containment."
                    ),
                    "reason": (
                        "The incident has been classified "
                        "as Critical based on current "
                        "impact and evidence."
                    ),
                    "type": "Immediate Response",
                }
            )

        elif severity_level == "High":

            actions.append(
                {
                    "priority": 1,
                    "action": (
                        "Assign high-priority investigation "
                        "and monitor user impact closely."
                    ),
                    "reason": (
                        "The incident shows significant "
                        "technical or user impact."
                    ),
                    "type": "Immediate Response",
                }
            )

        # Probable-cause investigations

        for cause_data in cause_result.get(
            "probable_causes",
            [],
        ):

            confidence = cause_data.get(
                "confidence",
                "Low",
            )

            if confidence in [
                "High",
                "Medium",
            ]:

                actions.append(
                    {
                        "priority": (
                            2
                            if confidence == "High"
                            else 3
                        ),
                        "action": cause_data.get(
                            "investigation",
                            "Investigate the identified "
                            "probable cause.",
                        ),
                        "reason": (
                            f"Probable cause identified: "
                            f"{cause_data.get('cause')}"
                        ),
                        "type": "Investigation",
                    }
                )

        # Information gaps

        for gap in gap_result.get(
            "investigation_gaps",
            [],
        ):

            priority_map = {
                "High": 2,
                "Medium": 4,
                "Low": 5,
            }

            actions.append(
                {
                    "priority": priority_map.get(
                        gap.get("priority"),
                        5,
                    ),
                    "action": gap.get(
                        "question",
                        "Collect missing investigation "
                        "information.",
                    ),
                    "reason": gap.get(
                        "why",
                        "Additional context is required "
                        "for the investigation.",
                    ),
                    "type": "Information Collection",
                }
            )

        # Logs should be preserved for serious incidents

        if (
            severity_score >= 60
            and incident.get("has_logs")
        ):

            actions.append(
                {
                    "priority": 2,
                    "action": (
                        "Preserve relevant logs and "
                        "incident evidence for analysis."
                    ),
                    "reason": (
                        "Technical evidence is available "
                        "and should remain accessible "
                        "during investigation."
                    ),
                    "type": "Evidence Preservation",
                }
            )

        actions.sort(
            key=lambda item: item["priority"]
        )

        # Remove duplicate actions

        unique_actions = []
        seen = set()

        for action in actions:

            action_text = action.get(
                "action",
                "",
            )

            if action_text not in seen:

                seen.add(action_text)

                unique_actions.append(action)

        return {
            "recommended_actions": unique_actions[:7],
            "action_count": min(
                len(unique_actions),
                7,
            ),
        }