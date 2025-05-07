import re


def prepare_prepare_line(line: str) -> str:
    line = line.strip()
    line = re.sub(r"\s+", " ", line)
    return line.replace("(", "").replace(")", "").replace(",", "")
