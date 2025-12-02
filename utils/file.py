from typing import Generator
from pathlib import Path

def read_lines(path: str | Path) -> Generator[str, None, None]:
    with open(path, 'r', encoding='utf8') as file:
        for line in file:
            yield line.strip()