from core.incident_analyzer import IncidentAnalyzer
from core.evidence_engine import EvidenceEngine
from core.severity_engine import SeverityEngine
from core.cause_engine import CauseEngine
from core.timeline_engine import TimelineEngine
from core.gap_engine import GapEngine
from core.action_engine import ActionEngine
from core.confidence_engine import ConfidenceEngine
from core.report_engine import ReportEngine


class NexusEngine:
    """
    Main NEXUS intelligence pipeline.

    Coordinates all analysis engines and returns
    one complete incident intelligence report.
    """

    def __init__(self):

        self.incident_analyzer = IncidentAnalyzer()
        self.evidence_engine = EvidenceEngine()
        self.severity_engine = SeverityEngine()
        self.cause_engine = CauseEngine()
        self.timeline_engine = TimelineEngine()
        self.gap_engine = GapEngine()
        self.action_engine = ActionEngine()
        self.confidence_engine = ConfidenceEngine()
        self.report_engine = ReportEngine()

    def investigate(
        self,
        description,
        system="",
        environment="",
        logs="",
    ):
        # Step 1: Structure the incident

        incident = self.incident_analyzer.analyze(
            description=description,
            system=system,
            environment=environment,
            logs=logs,
        )

        # Step 2: Extract evidence

        evidence = self.evidence_engine.analyze(
            incident
        )

        # Step 3: Build probable timeline

        timeline = self.timeline_engine.analyze(
            incident
        )

        # Step 4: Identify investigation gaps

        gaps = self.gap_engine.analyze(
            incident,
            evidence,
            timeline,
        )

        # Step 5: Calculate severity

        severity = self.severity_engine.analyze(
            incident,
            evidence,
        )

        # Step 6: Generate investigation hypotheses

        causes = self.cause_engine.analyze(
            incident,
            evidence,
        )

        # Step 7: Measure investigation confidence

        confidence = self.confidence_engine.analyze(
            incident,
            evidence,
            timeline,
            gaps,
            causes,
        )

        # Step 8: Generate prioritized actions

        actions = self.action_engine.analyze(
            incident,
            severity,
            causes,
            gaps,
        )

        # Step 9: Build final intelligence report

        report = self.report_engine.generate(
            incident=incident,
            evidence=evidence,
            severity=severity,
            causes=causes,
            timeline=timeline,
            gaps=gaps,
            actions=actions,
            confidence=confidence,
        )

        return report

    def to_text(self, report):

        return self.report_engine.to_text(
            report
        )