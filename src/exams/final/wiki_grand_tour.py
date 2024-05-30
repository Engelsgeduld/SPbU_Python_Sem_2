import queue
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import Manager, active_children
from multiprocessing.managers import DictProxy
from typing import Optional

import click
from bs4 import BeautifulSoup, SoupStrainer
from requests import get


class WikiGrandTour:
    def __init__(self, depth: int, process_count: int, unique: bool, points: list[str]) -> None:
        if unique and len(set(points)) != len(points):
            raise ValueError("All links in point should be unique in unique mode")

        self.depth = depth
        self.process_count = process_count
        self.points = points
        self.unique = unique

    def links_parse(self, url: str) -> list[str]:
        response = get(url).content
        links = []
        soup = BeautifulSoup(response, "html.parser", parse_only=SoupStrainer("a"))
        for link in soup.find_all(href=True):
            if link["href"].startswith("/wiki"):
                links.append("https://en.wikipedia.org" + link["href"])
        return links

    def page_parse(
        self, queue: queue.Queue[list[str]], end: str, seen: "DictProxy[str, None]", absolute_path: list[str]
    ) -> Optional[list[str]]:
        path = queue.get()
        links = self.links_parse(path[-1])
        for link in links:
            if self.unique and link in absolute_path:
                continue
            if link == end:
                return path + [link]
            if link in seen:
                continue
            seen[link] = None
            queue.put(path + [link])
        return None

    def bfs(self, start: str, end: str, absolute_path: list[str]) -> list[str]:
        with Manager() as manager:
            queue = manager.Queue()
            queue.put([start])
            manager_seen = manager.dict()
            for current_deep in range(self.depth):
                with ProcessPoolExecutor(max_workers=self.process_count) as executor:
                    workers = [
                        executor.submit(self.page_parse, queue, end, manager_seen, absolute_path)
                        for _ in range(queue.qsize())
                    ]
                    for worker in as_completed(workers):
                        result = worker.result()
                        if result:
                            active = active_children()
                            for proc in active:
                                proc.kill()
                            return result[1:]
                        continue
            raise ValueError(f"Path not fount at deep limit {self.depth}")

    def find_road(self) -> list[str]:
        road: list[str] = [self.points[0]]
        with click.progressbar(range(len(self.points) - 1), label="Progress") as bar:
            for i in bar:
                road += [*self.bfs(self.points[i], self.points[i + 1], road)]
        return road


@click.command("WikiRace")
@click.argument("process_count", type=click.IntRange(min=1))
@click.argument("deep_limit", type=click.IntRange(min=1))
@click.option("--unique", is_flag=True, default=False)
@click.argument("points", nargs=-1, type=click.STRING)
def script(process_count: int, deep_limit: int, unique: bool, points: list[str]) -> None:
    wiki = WikiGrandTour(deep_limit, process_count, unique, points)
    click.echo(wiki.find_road())


if __name__ == "__main__":
    try:
        script()
    except Exception as e:
        click.echo(e)
