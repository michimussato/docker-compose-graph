import pytest
import json
import pathlib

from docker_graph.docker_graph import main, DockerComposeGraph

__author__ = "Michael Mussato"
__copyright__ = "Michael Mussato"
__license__ = "MIT"


# import logging
# import sys
#
# logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
# logging.basicConfig(
#     level=logging.DEBUG, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
# )


# def test_fib():
#     """API Tests"""
#     assert fib(1) == 1
#     assert fib(2) == 1
#     assert fib(7) == 13
#     with pytest.raises(AssertionError):
#         fib(-10)

def test_get_root_ports():
    # Todo
    raise NotImplementedError


def test_get_service_ports():
    dcg = DockerComposeGraph()
    trees = dcg.parse_docker_compose(pathlib.Path("/home/michael/git/repos/deadline-docker/10.2/docker-compose.yaml"))

    # resolve environment variables (optional)
    # dcg.load_dotenv(pathlib.Path("/home/michael/git/repos/deadline-docker/10.2/.env"))

    port_mappings = dcg._get_service_ports(
        tree=trees[0],
    )

    expected = [{'mongodb-10-2': ['${MONGO_DB_PORT_HOST}:${MONGO_DB_PORT_CONTAINER}']},
                {'mongo-express-10-2': ['${MONGO_EXPRESS_PORT_HOST}:${MONGO_EXPRESS_PORT_CONTAINER}']},
                {'filebrowser': ['${FILEBROWSER_PORT_HOST}:${FILEBROWSER_PORT_CONTAINER}']},
                {'dagster_dev': ['${DAGSTER_DEV_PORT_HOST}:${DAGSTER_DEV_PORT_CONTAINER}']},
                {'deadline-repository-installer-10-2': []}, {'deadline-client-installer-10-2': []},
                {'deadline-rcs-runner-10-2': ['${RCS_HTTP_PORT_HOST}:${RCS_HTTP_PORT_CONTAINER}']},
                {'deadline-pulse-runner-10-2': []}, {'deadline-worker-runner-10-2': []},
                {'deadline-webservice-runner-10-2': ['${WEBSERVICE_HTTP_PORT_HOST}:${WEBSERVICE_HTTP_PORT_CONTAINER}']}]

    assert port_mappings == expected


def test_iterate_trees():
    dcg = DockerComposeGraph()
    trees = dcg.parse_docker_compose(pathlib.Path("/home/michael/git/repos/deadline-docker/10.2/docker-compose.yaml"))

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
