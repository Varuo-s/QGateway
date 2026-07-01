from __future__ import annotations

import shutil
from typing import TypedDict

from backend.app.config.settings import get_settings


class LauncherCandidate(TypedDict):
    name: str
    found: bool
    path: str | None


def detect_launchers() -> list[LauncherCandidate]:
    settings = get_settings()
    candidates: list[LauncherCandidate] = []
    for executable in settings.launcher.executables:
        found_path = shutil.which(executable)
        candidates.append({"name": executable, "found": found_path is not None, "path": found_path})
    return candidates
