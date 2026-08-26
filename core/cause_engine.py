class CauseEngine:
    """
    Generates evidence-based probable causes.

    These are investigation hypotheses, not confirmed
    root causes.
    """

    def analyze(
        self,
        incident,
        evidence_result,
    ):
        text = (
            incident.get("description", "")
            + " "
            + incident.get("logs", "")
        ).lower()

        causes = []

        cause_rules = [
            {
                "title": "Database connectivity failure",
                "patterns": [
                    "database connection",
                    "connection refused",
                    "database unavailable",
                    "db connection",
                ],
                "confidence": "High",
                "investigation": (
                    "Check database availability, connection "
                    "configuration, credentials, network access, "
                    "and connection limits."
                ),
            },
            {
                "title": "Deployment-related regression",
                "patterns": [
                    "after deployment",
                    "after deploy",
                    "deployment",
                    "release",
                ],
                "confidence": "Medium",
                "investigation": (
                    "Review recent deployment changes, "
                    "configuration differences, environment "
                    "variables, and rollback history."
                ),
            },
            {
                "title": "Authentication dependency failure",
                "patterns": [
                    "cannot log in",
                    "login failed",
                    "authentication failed",
                    "unauthorized",
                    "access denied",
                ],
                "confidence": "Medium",
                "investigation": (
                    "Check authentication services, credentials, "
                    "token validation, session storage, and "
                    "upstream dependencies."
                ),
            },
            {
                "title": "Network or service connectivity issue",
                "patterns": [
                    "timeout",
                    "connection refused",
                    "unreachable",
                    "dns",
                    "network",
                ],
                "confidence": "Medium",
                "investigation": (
                    "Check network connectivity, DNS resolution, "
                    "service availability, firewall rules, and "
                    "dependency endpoints."
                ),
            },
            {
                "title": "Application-level regression",
                "patterns": [
                    "started failing",
                    "application failed",
                    "crash",
                    "exception",
                    "broken",
                ],
                "confidence": "Medium",
                "investigation": (
                    "Review application logs, recent code changes, "
                    "runtime configuration, and dependency versions."
                ),
            },
        ]

        for rule in cause_rules:

            matches = [
                pattern
                for pattern in rule["patterns"]
                if pattern in text
            ]

            if matches:

                confidence = rule["confidence"]

                if len(matches) >= 2:
                    confidence = "High"

                causes.append(
                    {
                        "cause": rule["title"],
                        "confidence": confidence,
                        "evidence": matches,
                        "investigation": rule[
                            "investigation"
                        ],
                    }
                )

        if not causes:

            causes.append(
                {
                    "cause": (
                        "Insufficient evidence for a "
                        "specific probable cause"
                    ),
                    "confidence": "Low",
                    "evidence": [],
                    "investigation": (
                        "Collect application logs, recent "
                        "changes, timestamps, affected systems, "
                        "and dependency status."
                    ),
                }
            )

        return {
            "probable_causes": causes[:5],
            "cause_count": min(len(causes), 5),
            "disclaimer": (
                "Probable causes are evidence-based "
                "investigation hypotheses and should not "
                "be treated as confirmed root causes."
            ),
        }