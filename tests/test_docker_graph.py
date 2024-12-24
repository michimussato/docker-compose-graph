import pytest
import json
import pathlib

from docker_graph.docker_graph import main, DockerComposeGraph

__author__ = "Michael Mussato"
__copyright__ = "Michael Mussato"
__license__ = "MIT"


# def test_fib():
#     """API Tests"""
#     assert fib(1) == 1
#     assert fib(2) == 1
#     assert fib(7) == 13
#     with pytest.raises(AssertionError):
#         fib(-10)


def test_process_graph():
    dcg = DockerComposeGraph()
    tree = dcg.parse_docker_compose(pathlib.Path("/home/michael/git/repos/deadline-docker/10.2/docker-compose.yaml"))
    # j = json.dumps(tree, indent=2)
    # print(j)

    dcg.load_dotenv(pathlib.Path("/home/michael/git/repos/deadline-docker/10.2/.env"))

    # dcg.expand_vars(tree)

    with open("tree.json", "w") as fw:
        json.dump(tree, fw, indent=2)

    dcg.process_graph(tree)


def test_iterate_trees():
    dcg = DockerComposeGraph()
    trees = dcg.parse_docker_compose(pathlib.Path("/home/michael/git/repos/deadline-docker/10.2/docker-compose.yaml"))
    # j = json.dumps(tree, indent=2)
    # print(j)

    # resolve environment variables (optional)
    dcg.load_dotenv(pathlib.Path("/home/michael/git/repos/deadline-docker/10.2/.env"))

    # dcg.expand_vars(tree)

    # with open("tree.json", "w") as fw:
    #     json.dump(tree, fw, indent=2)

    dcg.iterate_trees(trees)


# def test_main(capsys):
#     """CLI Tests"""
#     # capsys is a pytest fixture that allows asserts against stdout/stderr
#     # https://docs.pytest.org/en/stable/capture.html
#     main(["7"])
#     captured = capsys.readouterr()
#     assert "The 7-th Fibonacci number is 13" in captured.out
