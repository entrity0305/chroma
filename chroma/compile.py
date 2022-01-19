from dataclasses import dataclass


@dataclass
class Var:
    name: str

    def __repr__(self):
        return f'VAR {self.name}\n'
