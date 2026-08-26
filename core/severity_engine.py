class SeverityEngine:
    """
    Calculates incident severity using visible
    impact and technical evidence signals.
    """

    def analyze(
        self,
        incident,
        evidence_result,
    ):
        score = 0
        signals = []

        description = incident.get(
            "description",
            "",
        ).lower()

        logs = incident.get(
            "logs",
            "",
        ).lower()

        environment = incident.get(
            "environment_detected",
            "",
        ).lower()

        incident_type = incident.get(
            "incident_type",
            "",
        )

        text = description + " " + logs

        # User impact

        user_impact_signals = [
            "users cannot",
            "cannot log in",
            "service unavailable",
            "service down",
            "outage",
            "all users",
        ]

        matches = [
            signal
            for signal in user_impact_signals
            if signal in text
        ]

        if matches:
            points = min(
                30,
                len(matches) * 15,
            )

            score += points

            signals.append(
                {
                    "signal": "User impact detected",
                    "points": points,
                    "severity": "high",
                    "matches": matches,
                }
            )

        # Production environment

        if (
            "production" in environment
            or "prod" in environment
        ):
            score += 20

            signals.append(
                {
                    "signal": (
                        "Production environment affected"
                    ),
                    "points": 20,
                    "severity": "high",
                    "matches": [
                        incident.get(
                            "environment_detected",
                            "Production",
                        )
                    ],
                }
            )

        # Critical incident categories

        critical_categories = {
            "Security Incident": 30,
            "Database Failure": 25,
            "Authentication Failure": 22,
            "Deployment Failure": 18,
            "Network Failure": 18,
            "Application Failure": 18,
            "Performance Degradation": 12,
        }

        category_points = critical_categories.get(
            incident_type,
            8,
        )

        score += category_points

        signals.append(
            {
                "signal": (
                    f"Incident classified as "
                    f"{incident_type}"
                ),
                "points": category_points,
                "severity": (
                    "critical"
                    if category_points >= 25
                    else "high"
                    if category_points >= 18
                    else "medium"
                ),
                "matches": [incident_type],
            }
        )

        # Evidence strength

        evidence_count = evidence_result.get(
            "evidence_count",
            0,
        )

        if evidence_count >= 5:
            points = 15
        elif evidence_count >= 3:
            points = 10
        elif evidence_count >= 1:
            points = 5
        else:
            points = 0

        if points:
            score += points

            signals.append(
                {
                    "signal": (
                        "Multiple supporting "
                        "investigation signals detected"
                    ),
                    "points": points,
                    "severity": "medium",
                    "matches": [
                        f"{evidence_count} evidence signals"
                    ],
                }
            )

        # Logs available

        if incident.get("has_logs"):
            score += 5

            signals.append(
                {
                    "signal": (
                        "Technical logs available"
                    ),
                    "points": 5,
                    "severity": "low",
                    "matches": [],
                }
            )

        score = min(score, 100)

        level = self._get_level(score)

        return {
            "severity_score": score,
            "severity_level": level,
            "signals": signals,
            "signal_count": len(signals),
        }

    def _get_level(self, score):

        if score >= 80:
            return "Critical"

        if score >= 60:
            return "High"

        if score >= 35:
            return "Medium"

        return "Low"