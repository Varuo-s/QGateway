from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Literal, TypedDict

from pydantic import BaseModel

from backend.app.config.settings import get_settings
from backend.app.logging.logger import get_logger

RuntimeState = Literal["stopped", "running", "error"]
logger = get_logger("runtime")


class RuntimeStatus(TypedDict):
    state: RuntimeState
    provider: str
    executable: str
    executable_exists: bool
    model_path: str
    model_exists: bool
    host: str
    port: int
    pid: int | None
    command: list[str]
    error: str | None


class RuntimeStartRequest(BaseModel):
    model_path: str | None = None
    host: str | None = None
    port: int | None = None


class RuntimeManager:
    def __init__(self) -> None:
        self._process: subprocess.Popen[str] | None = None
        self._error: str | None = None

    def _runtime_settings(self):
        return get_settings().runtime

    def _resolve(self, value: str) -> Path:
        return get_settings().resolve_path(value).resolve()

    def build_command(self, request: RuntimeStartRequest | None = None) -> list[str]:
        runtime = self._runtime_settings()
        executable = self._resolve(runtime.executable)
        model_value = request.model_path if request and request.model_path else runtime.model_path
        model_path = self._resolve(model_value)
        host = request.host if request and request.host else runtime.host
        port = request.port if request and request.port else runtime.port
        return [str(executable), "-m", str(model_path), "--host", host, "--port", str(port)]

    def status(self) -> RuntimeStatus:
        runtime = self._runtime_settings()
        executable = self._resolve(runtime.executable)
        model_path = self._resolve(runtime.model_path)
        state: RuntimeState = "stopped"
        pid: int | None = None

        if self._process is not None:
            return_code = self._process.poll()
            if return_code is None:
                state = "running"
                pid = self._process.pid
            else:
                state = "error" if return_code != 0 else "stopped"
                self._error = self._error or f"process exited with code {return_code}"
                self._process = None

        return {
            "state": state,
            "provider": runtime.provider,
            "executable": str(executable),
            "executable_exists": executable.exists(),
            "model_path": str(model_path),
            "model_exists": model_path.exists(),
            "host": runtime.host,
            "port": runtime.port,
            "pid": pid,
            "command": self.build_command(),
            "error": self._error,
        }

    def start(self, request: RuntimeStartRequest | None = None) -> RuntimeStatus:
        current = self.status()
        if current["state"] == "running":
            return current

        command = self.build_command(request)
        executable = Path(command[0])
        model_path = Path(command[2])
        if not executable.exists():
            self._error = f"runtime executable not found: {executable}"
            logger.error(self._error)
            return self.status()
        if not model_path.exists():
            self._error = f"model file not found: {model_path}"
            logger.error(self._error)
            return self.status()

        log_path = get_settings().resolve_path("logs/runtime.log")
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_file = log_path.open("a", encoding="utf-8")
        logger.info("starting runtime: %s", " ".join(command))
        try:
            self._process = subprocess.Popen(
                command,
                cwd=str(get_settings().project_root),
                stdout=log_file,
                stderr=subprocess.STDOUT,
                text=True,
            )
            self._error = None
        except OSError as exc:
            self._error = str(exc)
            logger.error("failed to start runtime: %s", exc)
        return self.status()

    def stop(self) -> RuntimeStatus:
        if self._process is None or self._process.poll() is not None:
            self._process = None
            return self.status()

        logger.info("stopping runtime pid=%s", self._process.pid)
        self._process.terminate()
        try:
            self._process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            logger.error("runtime did not stop gracefully; killing pid=%s", self._process.pid)
            self._process.kill()
            self._process.wait(timeout=5)
        finally:
            self._process = None
        return self.status()


runtime_manager = RuntimeManager()
