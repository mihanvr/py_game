from dataclasses import dataclass


@dataclass()
class User:
    login: str
    token: str
