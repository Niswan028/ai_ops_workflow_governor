import csv
from typing import List, Dict


def parse_logs(filename: str) -> List[Dict[str, str]]:
    with open(filename, newline="") as f:
        return list(csv.DictReader(f))
