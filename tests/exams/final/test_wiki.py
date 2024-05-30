import pytest
from click.testing import CliRunner

from src.exams.final.wiki_grand_tour import *


class TestExceptions:
    def test_deep_limit_exception(self):
        wiki = WikiGrandTour(
            1, 8, False, ["https://en.wikipedia.org/wiki/Russia", "https://en.wikipedia.org/wiki/3333333"]
        )
        with pytest.raises(ValueError):
            wiki.find_road()

    def test_unique_exception(self):
        with pytest.raises(ValueError):
            wiki = WikiGrandTour(
                1, 8, True, ["https://en.wikipedia.org/wiki/Russia", "https://en.wikipedia.org/wiki/Russia"]
            )


class TestNormalScenario:
    def test_normal_scenario(self):
        expected = [
            "https://en.wikipedia.org/wiki/United_States",
            "https://en.wikipedia.org/wiki/Missouri",
            "https://en.wikipedia.org/wiki/Eminem",
            "https://en.wikipedia.org/wiki/Hip_hop_music",
            "https://en.wikipedia.org/wiki/Adolf_Hitler",
        ]
        wiki = WikiGrandTour(
            10,
            8,
            False,
            [
                "https://en.wikipedia.org/wiki/United_States",
                "https://en.wikipedia.org/wiki/Eminem",
                "https://en.wikipedia.org/wiki/Adolf_Hitler",
            ],
        )
        assert wiki.find_road() == expected

    def test_click_output(self):
        runner = CliRunner()
        result = runner.invoke(
            script, ["8", "10", "https://en.wikipedia.org/wiki/China", "https://en.wikipedia.org/wiki/Adolf_Hitler"]
        )
        assert (
            result.output
            == "Progress\n['https://en.wikipedia.org/wiki/China', 'https://en.wikipedia.org/wiki/Marxist%E2%80%93Leninist', 'https://en.wikipedia.org/wiki/Adolf_Hitler']\n"
        )
