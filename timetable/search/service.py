import subprocess
from enum import StrEnum
from typing import Final

ALLOWED_INDEXES: Final = frozenset(["teachers", "subjects"])


class CommandType(StrEnum):
    index = "index"
    document = "document"


class OpensearchCommandExecutor:
    def __call__(self, command_type: CommandType, index: str) -> str:
        cmd = ["python", "manage.py", "opensearch"]
        if command_type == CommandType.index:
            additional_cmd = ["index", "rebuild", "--force", index]
        else:
            additional_cmd = ["document", "index", "--force", "-i", index]

        cmd.extend(additional_cmd)
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)  # noqa: S603
        message = f"Команда выполнена успешно:\n{result.stdout}"
        if result.stderr:
            message += f"\nОшибки:\n{result.stderr}"

        return message
