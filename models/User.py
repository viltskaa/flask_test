from dataclasses import dataclass, asdict


@dataclass
class User:
    id: int | None
    email: str
    name: str
    age: int
    city: str
    password: str

    def __dict__(self):
        return asdict(self)
