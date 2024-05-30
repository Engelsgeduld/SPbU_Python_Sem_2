import json

import click
import requests

from src.homeworks.homework_4.task_1.api_dataclasses import CommitRequest, Repository
from src.homeworks.homework_4.task_1.json_parser import JsonReader


def _repo_request(username: str, repo_name: str, file_name: str) -> None:
    response = requests.get(f"https://api.github.com/repos/{username}/{repo_name}")
    with open(f"{file_name}.json", "w+") as file:
        file.write(json.dumps(response.json(), indent=2))


def _commit_request(username: str, repo_name: str, file_name: str) -> None:
    response = requests.get(f"https://api.github.com/repos/{username}/{repo_name}/commits")
    with open(f"{file_name}.json", "w+") as file:
        file.write(json.dumps(response.json(), indent=2))


def _repo_info_output(file_name: str, strict: bool) -> None:
    reader = JsonReader(file_name)
    repo = Repository.set_dataclass(reader, strict)
    click.echo(
        f"Repository info:\nName:{repo.name}\nDescription:{repo.description}\nTopics:{repo.topics}\nURL:{repo.html_url}\nOwner URL: {repo.owner.html_url}"
    )


def _commit_info_output(file_name: str, strict: bool) -> None:
    reader = JsonReader(file_name)
    commit = CommitRequest.set_dataclass(reader, strict)
    for commit_body in commit.commits:
        message = f"Commit info:\nMessage:{commit_body.commit.message}\nAuthor name:{commit_body.commit.author.name}\nAuthor email:{commit_body.commit.author.email}\nCommitter name:{commit_body.commit.committer.name}\nCommitter email:{commit_body.commit.committer.email}\nDate:{commit_body.commit.author.date}"
        click.echo(message)
        click.echo("\n\n")


@click.group()
def all_commands() -> None:
    pass


@all_commands.command()
@click.argument("username", type=click.STRING)
@click.argument("repo_name", type=click.STRING)
@click.argument("file_name", type=click.STRING)
@click.option("--strict", is_flag=True, default=False)
def get_repo_info(username: str, repo_name: str, file_name: str, strict: bool) -> None:
    _repo_request(username, repo_name, file_name)
    _repo_info_output(file_name, strict)


@all_commands.command()
@click.argument("username", type=click.STRING)
@click.argument("repo_name", type=click.STRING)
@click.argument("file_name", type=click.STRING)
@click.option("--strict", is_flag=True, default=False)
def get_commit_info(username: str, repo_name: str, file_name: str, strict: bool) -> None:
    _commit_request(username, repo_name, file_name)
    _commit_info_output(file_name, strict)


if __name__ == "__main__":
    try:
        all_commands()
    except Exception as e:
        click.echo(e)
