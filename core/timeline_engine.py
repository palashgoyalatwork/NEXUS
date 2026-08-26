import re


class TimelineEngine:
    """
    Extracts and orders incident events from
    descriptions and technical context.
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

        events = []

        rules = [
            {
                "title": "Deployment or release event",
                "patterns": [
                    "deployment",
                    "deploy",
                    "release",
                ],
                "stage": 1,
            },
            {
                "title": "Application failure begins",
                "patterns": [
                    "started failing",
                    "application failed",
                    "crash",
                    "exception",
                    "service down",
                ],
                "stage": 2,
            },
            {
                "title": "User impact observed",
                "patterns": [
                    "users cannot",
                    "cannot log in",
                    "login failed",
                    "users affected",
                ],
                "stage": 3,
            },
            {
                "title": "Dependency or database issue detected",
                "patterns": [
                    "database connection",
                    "connection refused",
                    "database unavailable",
                    "timeout",
                ],
                "stage": 4,
            },
        ]

        for rule in rules:

            matches = [
                pattern
                for pattern in rule["patterns"]
                if pattern in text
            ]

            if matches:

                events.append(
                    {
                        "event": rule["title"],
                        "matches": matches,
                        "stage": rule["stage"],
                        "source": (
                            "logs"
                            if any(
                                match in logs.lower()
                                for match in matches
                            )
                            else "incident description"
                        ),
                    }
                )

        events.sort(
            key=lambda event: event["stage"]
        )

        for event in events:
            event.pop("stage", None)

        if not events:

            events.append(
                {
                    "event": (
                        "No clear sequence of incident "
                        "events could be extracted"
                    ),
                    "matches": [],
                    "source": "insufficient context",
                }
            )

        return {
            "timeline": events,
            "event_count": len(events),
            "timeline_summary": self._summary(
                events
            ),
        }

    def _summary(self, events):

        if len(events) == 1:
            return (
                "Limited timeline evidence was "
                "available from the incident context."
            )

        event_names = [
            event["event"]
            for event in events
        ]

        return (
            " → ".join(event_names)
        )