from typing import Generator
from pathlib import Path

def read_lines(path: str | Path, do_strip: bool = True) -> Generator[str, None, None]:
    with open(path, 'r', encoding='utf8') as file:
        for line in file:
            if do_strip:
                line = line.strip()
            yield line