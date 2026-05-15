import json
from datetime import datetime
from pathlib import Path

from config import RESULTS_PATH


def save_experiment(result: dict) -> None:
    path = Path(RESULTS_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        with path.open("r") as f:
            history = json.load(f)
    else:
        history = []

    result["timestamp"] = datetime.utcnow().isoformat()
    history.append(result)

    with path.open("w") as f:
        json.dump(history, f, indent=2)


def load_experiments() -> list[dict]:
    path = Path(RESULTS_PATH)

    if not path.exists():
        return []

    with path.open("r") as f:
        return json.load(f)