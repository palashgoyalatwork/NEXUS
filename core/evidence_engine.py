class EvidenceEngine:
    """
    Extracts structured evidence from an incident and
    separates explicit observations from contextual signals.
    """

    def analyze(self, incident):
        description = incident.get(
            "description",
            "",
        )

        logs = incident.get(
            "logs",
            "",
        )

        text = (
            description
            + " "
            + logs
        ).lower()

        evidence = []

        patterns = {
            "Authentication failure observed": [
                "cannot log in",
                "login failed",
                "authentication failed",
                "unauthorized",
                "access denied",
            ],
            "Database connectivity issue": [
                "database connection",
                "connection refused",
                "db connection",
                "database unavailable",
            ],
            "Recent deployment mentioned": [
                "after deployment",
                "after deploy",
                "deployment",
                "release",
            ],
            "Application failure observed": [
                "application failed",
                "started failing",
                "crash",
                "exception",
                "service down",
            ],
            "Performance degradation observed": [
                "slow",
                "latency",
                "timeout",
                "lag",
                "high cpu",
                "memory",
            ],
            "Security-related activity observed": [
                "unauthorized access",
                "suspicious activity",
                "attack",
                "breach",
                "exploit",
            ],
        }

        for label, signals in patterns.items():

            matches = [
                signal
                for signal in signals
                if signal in text
            ]

            if matches:

                evidence.append(
                    {
                        "evidence": label,
                        "matches": matches,
                        "source": (
                            "logs"
                            if any(
                                match in logs.lower()
                                for match in matches
                            )
                            else "incident description"
                        ),
                        "confidence": self._confidence(
                            matches,
                            logs,
                        ),
                    }
                )

        if incident.get("has_logs"):

            evidence.append(
                {
                    "evidence": (
                        "Technical logs were provided "
                        "for investigation."
                    ),
                    "matches": [],
                    "source": "logs",
                    "confidence": "High",
                }
            )

        return {
            "evidence": evidence,
            "evidence_count": len(evidence),
        }

    def _confidence(
        self,
        matches,
        logs,
    ):
        if any(
            match in logs.lower()
            for match in matches
        ):
            return "High"

        if len(matches) >= 2:
            return "High"

        return "Medium"