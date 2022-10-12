import re
from collections import defaultdict
from dataclasses import dataclass

from PyQt6 import QtCore, QtGui

from .logger import AppLogger

logger = AppLogger("logger")

COLOUR = QtCore.Qt.GlobalColor


class BMLHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent: QtGui.QTextDocument = None):
        super().__init__(parent)
        self._mapping: dict[re.Pattern, QtGui.QTextCharFormat] = {}

    def add_mapping(self, pattern: re.Pattern, pattern_format: QtGui.QTextCharFormat):  # noqa
        self._mapping[pattern] = pattern_format

    def highlightBlock(self, text: str) -> None:
        for pattern, fmt in self._mapping.items():
            for match in pattern.finditer(text):
                start, end = match.span()
                self.setFormat(start, end-start, fmt)


@dataclass(slots=True)
class PatternFormat:
    pattern: re.Pattern = None
    text_format: QtGui.QTextCharFormat = None


def fmt(colour: QtCore.Qt.GlobalColor) -> QtGui.QTextCharFormat:
    f = QtGui.QTextCharFormat()
    f.setForeground(colour)

    return f


def pattern(p: str) -> re.Pattern:
    return re.compile(p, re.MULTILINE)


def new_highlighter() -> BMLHighlighter:
    patterns = defaultdict(PatternFormat)  # noqa

    patterns["variable"].pattern = pattern(r"[A-Za-z]+")
    patterns["matrix"].pattern = pattern(r"(?<!\S)matrix(?!\w+)")
    patterns["set"].pattern = pattern(r"(?<!\S)set(?!\w+)")
    patterns["func"].pattern = pattern(r"\w+(?=\(\w+\))")
    patterns["and"].pattern = pattern(r"(?<!\S)and(?!\w+)")
    patterns["for"].pattern = pattern(r"(?<!\S)for(?=\s*)")
    patterns["exists"].pattern = pattern(r"(?<!\S)exists(?!\w+)")
    patterns["paren"].pattern = pattern(r"[()\[\]{}]")
    patterns["`sym"].pattern = pattern(r"(?<!\S)`\w+")
    patterns["matrix_name"].pattern = pattern(r"(?<=^matrix )\w+")
    patterns["set_name"].pattern = pattern(r"(?<=^set )\w+")
    patterns["arrow"].pattern = pattern(r"(?<!\S)=>(?!\S)")
    patterns["mod"].pattern = pattern(r"(?<!\S)mod(?!\w+)")
    patterns["comment"].pattern = pattern(r"#.*$")
    patterns["number"].pattern = pattern(r"\d+\.?\d*[a-z]?")
    patterns["abs"].pattern = pattern(r"\|")

    patterns["variable"].text_format = fmt(COLOUR.cyan)
    patterns["matrix"].text_format = fmt(COLOUR.darkCyan)
    patterns["set"].text_format = fmt(COLOUR.darkCyan)
    patterns["func"].text_format = fmt(COLOUR.darkCyan)
    patterns["and"].text_format = fmt(COLOUR.cyan)
    patterns["for"].text_format = fmt(COLOUR.red)
    patterns["exists"].text_format = fmt(COLOUR.red)
    patterns["paren"].text_format = fmt(COLOUR.yellow)
    patterns["`sym"].text_format = fmt(COLOUR.green)
    patterns["matrix_name"].text_format = fmt(COLOUR.green)
    patterns["set_name"].text_format = fmt(COLOUR.green)
    patterns["arrow"].text_format = fmt(COLOUR.gray)
    patterns["mod"].text_format = fmt(COLOUR.red)
    patterns["comment"].text_format = fmt(COLOUR.lightGray)
    patterns["number"].text_format = fmt(COLOUR.cyan)
    patterns["abs"].text_format = fmt(COLOUR.gray)

    syntax_highlighter = BMLHighlighter()

    for _, f in patterns.items():
        if f.pattern is None or f.text_format is None:
            continue

        syntax_highlighter.add_mapping(f.pattern, f.text_format)

    return syntax_highlighter
