import pytest
from click.testing import CliRunner

from src.homeworks.homework_4.task_1.main_script import get_commit_info, get_repo_info

repo_expected_output = """Repository info:
Name:SPbU_Python_1Sem
Description:This is 1 semester of Python in SPbU
Topics:[]
URL:https://github.com/Engelsgeduld/SPbU_Python_1Sem
Owner URL: https://github.com/Engelsgeduld
"""

commit_expected_output = """Commit info:
Message:Init: Test: Final. Task 1 Takes. Knyazev (#31)

* Init: Test: Final. Task 1 Takes. Knyazev

* Fix: Black
Author name:Knyazev Dmitrii
Author email:144917566+Engelsgeduld@users.noreply.github.com
Committer name:GitHub
Committer email:noreply@github.com
Date:2023-12-28T13:54:50Z



Commit info:
Message:Homework 6 task 1 shopping (#23)

* Init: Homework 6 Task 1 Shopping Knyazev

* Fix: Test file paths

* Fix: balance and logs file name input, get max/min rework, upper/lower bound without split

* Fix: min/max refactor, add balance test
Author name:Knyazev Dmitrii
Author email:144917566+Engelsgeduld@users.noreply.github.com
Committer name:GitHub
Committer email:noreply@github.com
Date:2023-12-27T13:01:45Z



Commit info:
Message:Init: Practice 13 Task 1 Finite State Machine Knyazev (#27)

* Init: Practice 13 Task 1 Finite State Machine Knyazev

* Changes: main function splited to validation and creation, fix typing, recursion -> loop, state move rework, code refactoring, language validation rework

* Changes: main.yaml change python version to 3.12.0

* Fix: code refactor, iterator return None if state is empty
Author name:Knyazev Dmitrii
Author email:144917566+Engelsgeduld@users.noreply.github.com
Committer name:GitHub
Committer email:noreply@github.com
Date:2023-12-27T08:50:38Z



Commit info:
Message:Init: Test 2. Task 2 Safe Call. Knyazev (#30)
Author name:Knyazev Dmitrii
Author email:144917566+Engelsgeduld@users.noreply.github.com
Committer name:GitHub
Committer email:noreply@github.com
Date:2023-12-25T09:59:27Z



Commit info:
Message:Init: Test 2 Task 1 Fibonacci Knyazev (#25)
Author name:Knyazev Dmitrii
Author email:144917566+Engelsgeduld@users.noreply.github.com
Committer name:GitHub
Committer email:noreply@github.com
Date:2023-11-29T14:32:47Z



Commit info:
Message:Init: Test 1 Task 1 Merge Knyazev (#22)
Author name:Knyazev Dmitrii
Author email:144917566+Engelsgeduld@users.noreply.github.com
Committer name:GitHub
Committer email:noreply@github.com
Date:2023-11-29T14:28:47Z



Commit info:
Message:Init: Homework 5 Task 2 DNA Compress Knyazev (#20)

* Init: Homework 5 Task 2 DNA Compress Knyazev

* Changes: От сишного к питонячему(Наверное)
Author name:Knyazev Dmitrii
Author email:144917566+Engelsgeduld@users.noreply.github.com
Committer name:GitHub
Committer email:noreply@github.com
Date:2023-11-29T14:24:37Z



Commit info:
Message:Init: Homework 5 Task 1 UTF-16 Knyazev (#19)

* Init: Homework 5 Task 1 UTF-16 Knyazev

* Changes: remove debug from test, get_chars removed, add format_utf_16 func, code refactoring
Author name:Knyazev Dmitrii
Author email:144917566+Engelsgeduld@users.noreply.github.com
Committer name:GitHub
Committer email:noreply@github.com
Date:2023-11-29T14:21:52Z



Commit info:
Message:Homework 4 Task 1 Knyazev (#15)

* Homework 4 Task 1 Knyazev

* Change: in progress

* Changes: xor -> inverse function, code refator, add difference, fnmatch -> try constr, first_bit -> sign_bit, valid_user_input -> validate_user_input

* Changes: float validation -> int validation

* Changes: remove cases with implicit type conversion
Author name:Knyazev Dmitrii
Author email:144917566+Engelsgeduld@users.noreply.github.com
Committer name:GitHub
Committer email:noreply@github.com
Date:2023-11-29T14:17:43Z



Commit info:
Message:Homework 4 Task 3 Knyazev (#14)

* Homework 4 Task 3 Knyazev

* Change: create_queue now return Queue(), top and tail remove None when queue is empty, Exception -> IndexError

* Changes: class -> dataclass
Author name:Knyazev Dmitrii
Author email:144917566+Engelsgeduld@users.noreply.github.com
Committer name:GitHub
Committer email:noreply@github.com
Date:2023-11-29T14:16:17Z



Commit info:
Message:Practice 8 Task 1 BST Knyazev (#18)

* Init: Practice 8 Task 1 BST Knyazev

* Changes: mapp -> map, Node field key and data not Optional, remove class Pair -> Tuple, remove cringe, remove Data_type, V -> Value

* Change: class Tree add Generic values, class Node add Value to r/l children, code refactoring, None key check moved to _valid_input_key
Author name:Knyazev Dmitrii
Author email:144917566+Engelsgeduld@users.noreply.github.com
Committer name:GitHub
Committer email:noreply@github.com
Date:2023-11-07T17:04:17Z



Commit info:
Message:Merge pull request #10 from Engelsgeduld/Practice-5-Stack-Knyazev

Stack Realisation
Author name:Egor Spirin
Author email:Spirin.egor@gmail.com
Committer name:GitHub
Committer email:noreply@github.com
Date:2023-11-04T10:38:23Z



Commit info:
Message:Merge pull request #13 from Engelsgeduld/Practice-7-Unit-Tests

Practice 7 Task 1 Knyazev
Author name:Egor Spirin
Author email:Spirin.egor@gmail.com
Committer name:GitHub
Committer email:noreply@github.com
Date:2023-10-26T15:58:24Z



Commit info:
Message:Changes: user input validation -> user input parser, choose_func -> solve_func, check argument 'a' now in solve_function, a in find_linear_solution renamed into k
Author name:Engelsgeduld
Author email:knyazev.dmitrii05@gmail.com
Committer name:Engelsgeduld
Committer email:knyazev.dmitrii05@gmail.com
Date:2023-10-26T15:05:24Z



Commit info:
Message:Merge pull request #11 from Engelsgeduld/Homework-3-Task-1-Knyazev

Homework 3 Task 1 Knyazev
Author name:Egor Spirin
Author email:Spirin.egor@gmail.com
Committer name:GitHub
Committer email:noreply@github.com
Date:2023-10-26T12:39:19Z



Commit info:
Message:Changes were made
Author name:Engelsgeduld
Author email:knyazev.dmitrii05@gmail.com
Committer name:Engelsgeduld
Committer email:knyazev.dmitrii05@gmail.com
Date:2023-10-23T18:38:23Z



Commit info:
Message:Practice 7 Task 1 Knyazev
Author name:Engelsgeduld
Author email:knyazev.dmitrii05@gmail.com
Committer name:Engelsgeduld
Committer email:knyazev.dmitrii05@gmail.com
Date:2023-10-20T16:31:58Z



Commit info:
Message:I`m Magical Trickster!
Author name:Engelsgeduld
Author email:knyazev.dmitrii05@gmail.com
Committer name:Engelsgeduld
Committer email:knyazev.dmitrii05@gmail.com
Date:2023-10-17T20:36:54Z



Commit info:
Message:Merge pull request #8 from Engelsgeduld/Homework-2-Task-2-Knyazev

Homework 2 Task 2 Knyazev
Author name:Egor Spirin
Author email:Spirin.egor@gmail.com
Committer name:GitHub
Committer email:noreply@github.com
Date:2023-10-08T20:58:57Z



Commit info:
Message:Merge pull request #7 from Engelsgeduld/Homework_2-Task_1-Knyazev

Homework 2 Task 1 Knyazev
Author name:Egor Spirin
Author email:Spirin.egor@gmail.com
Committer name:GitHub
Committer email:noreply@github.com
Date:2023-10-08T20:56:50Z



Commit info:
Message:Homework 3 Task 1 Knyazev
Author name:Engelsgeduld
Author email:knyazev.dmitrii05@gmail.com
Committer name:Engelsgeduld
Committer email:knyazev.dmitrii05@gmail.com
Date:2023-10-07T21:24:22Z



Commit info:
Message:Changes were made
Author name:Engelsgeduld
Author email:knyazev.dmitrii05@gmail.com
Committer name:Engelsgeduld
Committer email:knyazev.dmitrii05@gmail.com
Date:2023-10-06T12:18:59Z



Commit info:
Message:Stack Realisation
Author name:Engelsgeduld
Author email:knyazev.dmitrii05@gmail.com
Committer name:Engelsgeduld
Committer email:knyazev.dmitrii05@gmail.com
Date:2023-10-06T11:47:33Z



Commit info:
Message:Changes were made
Author name:Engelsgeduld
Author email:knyazev.dmitrii05@gmail.com
Committer name:Engelsgeduld
Committer email:knyazev.dmitrii05@gmail.com
Date:2023-10-03T19:51:26Z



Commit info:
Message:changes were made
Author name:Engelsgeduld
Author email:knyazev.dmitrii05@gmail.com
Committer name:Engelsgeduld
Committer email:knyazev.dmitrii05@gmail.com
Date:2023-10-03T16:51:14Z



Commit info:
Message:After merge and black
Author name:Engelsgeduld
Author email:knyazev.dmitrii05@gmail.com
Committer name:Engelsgeduld
Committer email:knyazev.dmitrii05@gmail.com
Date:2023-09-29T16:29:17Z



Commit info:
Message:Merge branch 'main' into Homework-2-Task-2-Knyazev
Author name:Engelsgeduld
Author email:knyazev.dmitrii05@gmail.com
Committer name:Engelsgeduld
Committer email:knyazev.dmitrii05@gmail.com
Date:2023-09-29T16:27:36Z



Commit info:
Message:Merge branch 'main' into Homework_2-Task_1-Knyazev
Author name:Engelsgeduld
Author email:knyazev.dmitrii05@gmail.com
Committer name:Engelsgeduld
Committer email:knyazev.dmitrii05@gmail.com
Date:2023-09-29T16:25:29Z



Commit info:
Message:Merge pull request #9 from Engelsgeduld/Practice-3-Task-1-Knyazev

Practice 3 Task 1 Knyazev
Author name:Egor Spirin
Author email:Spirin.egor@gmail.com
Committer name:GitHub
Committer email:noreply@github.com
Date:2023-09-29T16:17:24Z



Commit info:
Message:Moving Homework 1 Files to new folder
Author name:Engelsgeduld
Author email:knyazev.dmitrii05@gmail.com
Committer name:Engelsgeduld
Committer email:knyazev.dmitrii05@gmail.com
Date:2023-09-29T15:46:46Z\n


"""


class TestMainScriptTests:
    def test_get_repo_info(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(get_repo_info, ["Engelsgeduld", "SPbU_Python_1Sem", "repo_res"])
            assert result.exit_code == 0
            assert result.output == repo_expected_output

    def test_get_commit_info(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(get_commit_info, ["Engelsgeduld", "SPbU_Python_1Sem", "repo_res"])
            assert result.exit_code == 0
            assert result.output == commit_expected_output
