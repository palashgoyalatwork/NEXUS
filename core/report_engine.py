from datetime import datetime


class ReportEngine:
    """
    Builds a complete NEXUS incident intelligence report
    from all analysis engines.
    """

    def generate(
        self,
        incident,
        evidence,
        severity,
        causes,
        timeline,
        gaps,
        actions,
        confidence,
    ):
        report_id = datetime.now().strftime(
            "NEXUS-%Y%m%d-%H%M%S"
        )

        summary = self._build_summary(
            incident,
            severity,
            causes,
            confidence,
        )

        return {
            "report_id": report_id,
            "generated_at": datetime.now().isoformat(
                timespec="seconds"
            ),
            "title": "NEXUS INCIDENT INTELLIGENCE REPORT",
            "summary": summary,
            "incident": incident,
            "severity": severity,
            "evidence": evidence,
            "causes": causes,
            "timeline": timeline,
            "gaps": gaps,
            "actions": actions,
            "confidence": confidence,
        }

    def _build_summary(
        self,
        incident,
        severity,
        causes,
        confidence,
    ):
        incident_type = incident.get(
            "incident_type",
            "Unclassified Technical Incident",
        )

        severity_level = severity.get(
            "severity_level",
            "Unknown",
        )

        severity_score = severity.get(
            "severity_score",
            0,
        )

        confidence_level = confidence.get(
            "confidence_level",
            "Low",
        )

        confidence_score = confidence.get(
            "confidence_score",
            0,
        )

        probable_causes = causes.get(
            "probable_causes",
            [],
        )

        top_cause = (
            probable_causes[0].get("cause")
            if probable_causes
            else "No specific probable cause identified"
        )

        return (
            f"This incident is classified as "
            f"{incident_type} with a "
            f"{severity_level} severity rating "
            f"({severity_score}/100). "
            f"The leading investigation hypothesis is "
            f"{top_cause}. "
            f"Current investigation confidence is "
            f"{confidence_level} "
            f"({confidence_score}/100)."
        )

    def to_text(self, report):
        """
        Converts a report object into a clean
        plain-text incident report.
        """

        lines = []

        lines.append(
            "NEXUS INCIDENT INTELLIGENCE REPORT"
        )

        lines.append(
            "=" * 42
        )

        lines.append(
            f"Report ID: "
            f"{report.get('report_id')}"
        )

        lines.append(
            f"Generated: "
            f"{report.get('generated_at')}"
        )

        lines.append("")

        lines.append("EXECUTIVE SUMMARY")
        lines.append("-" * 42)
        lines.append(
            report.get(
                "summary",
                "No summary available.",
            )
        )

        incident = report.get(
            "incident",
            {},
        )

        lines.append("")
        lines.append("INCIDENT PROFILE")
        lines.append("-" * 42)
        lines.append(
            f"Type: "
            f"{incident.get('incident_type')}"
        )
        lines.append(
            f"Environment: "
            f"{incident.get('environment_detected')}"
        )
        lines.append(
            "Affected Systems: "
            + ", ".join(
                incident.get(
                    "affected_systems",
                    [],
                )
            )
        )

        severity = report.get(
            "severity",
            {},
        )

        lines.append("")
        lines.append("SEVERITY ASSESSMENT")
        lines.append("-" * 42)
        lines.append(
            f"Severity: "
            f"{severity.get('severity_level')} "
            f"({severity.get('severity_score')}/100)"
        )

        lines.append("")
        lines.append("PROBABLE CAUSES")
        lines.append("-" * 42)

        for cause in report.get(
            "causes",
            {},
        ).get(
            "probable_causes",
            [],
        ):

            lines.append(
                f"[{cause.get('confidence')}] "
                f"{cause.get('cause')}"
            )

        lines.append("")
        lines.append("INCIDENT TIMELINE")
        lines.append("-" * 42)

        for index, event in enumerate(
            report.get(
                "timeline",
                {},
            ).get(
                "timeline",
                [],
            ),
            start=1,
        ):

            lines.append(
                f"{index}. {event.get('event')}"
            )

        lines.append("")
        lines.append("RECOMMENDED ACTIONS")
        lines.append("-" * 42)

        for action in report.get(
            "actions",
            {},
        ).get(
            "recommended_actions",
            [],
        ):

            lines.append(
                f"P{action.get('priority')} - "
                f"{action.get('action')}"
            )

        confidence = report.get(
            "confidence",
            {},
        )

        lines.append("")
        lines.append("INVESTIGATION CONFIDENCE")
        lines.append("-" * 42)
        lines.append(
            f"{confidence.get('confidence_level')} "
            f"({confidence.get('confidence_score')}/100)"
        )

        lines.append("")
        lines.append(
            "NOTE: Probable causes are investigation "
            "hypotheses and are not confirmed root causes."
        )

        return "\n".join(lines)