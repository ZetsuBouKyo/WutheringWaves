from typing import Callable, Optional

from PySide2.QtWidgets import QTextEdit


def get_docs(func: Callable[[], Optional[str]]) -> QTextEdit:
    html = func()
    if html is None:
        html = ""
    q_text = QTextEdit()
    q_text.setAcceptRichText(True)
    q_text.setHtml(html)
    return q_text
