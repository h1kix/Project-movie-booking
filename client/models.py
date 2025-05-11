from dataclasses import dataclass, field
from typing import List

@dataclass
class Movie:
    id: int
    title: str
    description: str = ""

@dataclass
class Booking:
    movie_id: int
    seats: List[str] = field(default_factory=list)
