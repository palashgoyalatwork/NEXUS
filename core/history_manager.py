import json
from datetime import datetime
from pathlib import Path


class HistoryManager:
    """
    Stores completed NEXUS investigations locally.
    """

    def __init__(self):
        self.data_dir = (
            Path(__file__).resolve()
            .parent.parent
            / "data"
        )

        self.data_dir.mkdir(
            exist_ok=True
        )

        self.history_file = (
            self.data_dir
            / "incident_history.json"
        )

        if not self.history_file.exists():

            self.history_file.write_text(
                "[]",
                encoding="utf-8",
            )

    def add_incident(
        self,
        analysis,
    ):
        history = self._load()

        incident = analysis.get(
            "incident",
            {},
        )

        severity = analysis.get(
            "severity",
            {},
        )

        confidence = analysis.get(
            "confidence",
            {},
        )

        entry = {
            "id": datetime.now().strftime(
                "%Y%m%d%H%M%S%f"
            ),
            "timestamp": datetime.now().isoformat(
                timespec="seconds"
            ),
            "incident_type": incident.get(
                "incident_type",
                "Unclassified",
            ),
            "description": incident.get(
                "description",
                "",
            ),
            "severity_score": severity.get(
                "severity_score",
                0,
            ),
            "severity_level": severity.get(
                "severity_level",
                "Low",
            ),
            "confidence_score": confidence.get(
                "confidence_score",
                0,
            ),
            "analysis": analysis,
        }

        history.insert(
            0,
            entry,
        )

        self._save(history)

        return entry

    def get_history(
        self,
        limit=None,
    ):
        history = self._load()

        if limit:
            return history[:limit]

        return history

    def get_incident(
        self,
        incident_id,
    ):
        history = self._load()

        for entry in history:

            if entry.get("id") == incident_id:
                return entry

        return None

    def delete_incident(
        self,
        incident_id,
    ):
        history = self._load()

        updated_history = [
            entry
            for entry in history
            if entry.get("id") != incident_id
        ]

        if len(updated_history) == len(history):
            return False

        self._save(updated_history)

        return True

    def clear_history(self):
        self._save([])

    def _load(self):

        try:

            with open(
                self.history_file,
                "r",
                encoding="utf-8",
            ) as file:

                data = json.load(file)

                if isinstance(data, list):
                    return data

        except (
            json.JSONDecodeError,
            FileNotFoundError,
        ):
            pass

        return []

    def _save(
        self,
        history,
    ):

        with open(
            self.history_file,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                history,
                file,
                indent=2,
                ensure_ascii=False,
            )