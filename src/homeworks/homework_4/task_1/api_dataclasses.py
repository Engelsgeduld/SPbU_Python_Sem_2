from dataclasses import dataclass

from src.homeworks.homework_4.task_1.json_orm import ORM


@dataclass
class Owner(ORM):
    login: str
    id: int
    html_url: str
    organizations_url: str


@dataclass
class Repository(ORM):
    id: int
    name: str
    html_url: str
    description: str
    topics: list[str]
    owner: Owner


@dataclass
class Author(ORM):
    name: str
    email: str
    date: str


@dataclass
class Committer(ORM):
    name: str
    email: str
    date: str


@dataclass
class Commit(ORM):
    author: Author
    committer: Committer
    message: str


@dataclass
class CommitBody(ORM):
    commit: Commit
    author: Owner


@dataclass
class CommitRequest(ORM):
    commits: list[CommitBody]
