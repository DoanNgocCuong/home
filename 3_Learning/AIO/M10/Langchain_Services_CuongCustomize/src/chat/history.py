import re
from pathlib import Path
from typing import Callable, Union

from langchain_core.chat_history import BaseChatMessageHistory
from langchain.memory import FileChatMessageHistory

from fastapi import HTTPException



def _is_valid_identifier(value: str) -> bool:
    valid_characters = re.compile(r"^[a-zA-Z0-9-_]+$")
    return bool(valid_characters.match(value))


def create_session_factory(base_dir: Union[str, Path],
                           max_history_length: int 
                           ) -> Callable[[str], BaseChatMessageHistory]:
    base_dir_ = Path(base_dir) if isinstance(base_dir, str) else base_dir
    if not base_dir_.exists():
        base_dir_.mkdir(parents=True)

    def get_chat_history(session_id: str) -> FileChatMessageHistory:
        if not _is_valid_identifier(session_id):
            raise HTTPException(
                status_code=400,
                detail=f"Session ID `{session_id}` is not in a valid format. "
                "Session ID must only contain alphanumeric characters, "
                "hyphens, and underscores.",
            )
        file_path = base_dir_ / f"{session_id}.json"

        chat_hist = FileChatMessageHistory(str(file_path))
        messages = chat_hist.messages

        if len(messages) > max_history_length:
            chat_hist.clear()
            for message in messages[-max_history_length:]:
                chat_hist.add_message(message)

        print("chat_hist len: ", len(chat_hist.messages))
        return chat_hist

    return get_chat_history

