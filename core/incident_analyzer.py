import re


class IncidentAnalyzer:
    """
    Converts raw technical incident descriptions into
    structured incident intelligence.
    """

    def analyze(
        self,
        description,
        system="",
        environment="",
        logs="",
    ):
        text = " ".join(
            [
                description or "",
                system or "",
                environment or "",
                logs or "",
            ]
        ).lower()

        incident_type = self._classify_incident(text)

        affected_systems = self._detect_systems(
            text,
            system,
        )

        keywords = self._extract_keywords(text)

        return {
            "description": description,
            "system": system,
            "environment": environment,
            "logs": logs,
            "incident_type": incident_type,
            "affected_systems": affected_systems,
            "keywords": keywords,
            "has_logs": bool(logs.strip()),
            "environment_detected": (
                environment.strip()
                if environment.strip()
                else "Not specified"
            ),
        }

    def _classify_incident(self, text):

        categories = {
            "Authentication Failure": [
                "login",
                "authentication",
                "auth",
                "password",
                "credential",
                "unauthorized",
                "forbidden",
                "access denied",
            ],
            "Database Failure": [
                "database",
                "db",
                "sql",
                "postgres",
                "mysql",
                "mongodb",
                "connection refused",
            ],
            "Deployment Failure": [
                "deployment",
                "deploy",
                "release",
                "rollback",
                "build failed",
            ],
            "Network Failure": [
                "network",
                "timeout",
                "connection",
                "dns",
                "latency",
                "unreachable",
            ],
            "Application Failure": [
                "crash",
                "exception",
                "error",
                "failed",
                "failure",
                "broken",
                "down",
            ],
            "Performance Degradation": [
                "slow",
                "latency",
                "lag",
                "performance",
                "high cpu",
                "memory",
                "overload",
            ],
            "Security Incident": [
                "breach",
                "attack",
                "malware",
                "unauthorized access",
                "suspicious",
                "exploit",
            ],
        }

        scores = {}

        for category, signals in categories.items():

            score = sum(
                1
                for signal in signals
                if signal in text
            )

            if score:
                scores[category] = score

        if not scores:
            return "Unclassified Technical Incident"

        return max(
            scores,
            key=scores.get,
        )

    def _detect_systems(
        self,
        text,
        provided_system,
    ):
        systems = []

        system_patterns = {
            "Authentication": [
                "login",
                "authentication",
                "auth",
                "credential",
            ],
            "Backend API": [
                "api",
                "backend",
                "server",
                "endpoint",
            ],
            "Database": [
                "database",
                "db",
                "sql",
                "postgres",
                "mysql",
                "mongodb",
            ],
            "Deployment Pipeline": [
                "deployment",
                "deploy",
                "release",
                "build",
            ],
            "Network Infrastructure": [
                "network",
                "dns",
                "timeout",
                "connection refused",
            ],
            "Frontend": [
                "frontend",
                "browser",
                "ui",
                "interface",
            ],
        }

        if provided_system.strip():

            systems.append(
                provided_system.strip()
            )

        for system, patterns in system_patterns.items():

            if any(
                pattern in text
                for pattern in patterns
            ):

                if system not in systems:
                    systems.append(system)

        return systems or [
            "System not clearly identified"
        ]

    def _extract_keywords(self, text):

        ignored_words = {
            "the",
            "and",
            "with",
            "from",
            "that",
            "this",
            "after",
            "before",
            "when",
            "were",
            "have",
            "has",
            "been",
            "into",
            "users",
        }

        words = re.findall(
            r"[a-zA-Z]{4,}",
            text,
        )

        keywords = []

        for word in words:

            if (
                word not in ignored_words
                and word not in keywords
            ):

                keywords.append(word)

        return keywords[:12]