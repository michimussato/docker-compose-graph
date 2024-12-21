"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = docker_graph.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This file can be renamed depending on your needs or safely removed if not needed.

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import os
import argparse
import logging
import pathlib
import sys
import yaml as pyyaml
from graphviz import Digraph
from collections import ChainMap

from docker_graph import __version__

__author__ = "Michael Mussato"
__copyright__ = "Michael Mussato"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from docker_graph.skeleton import fib`,
# when using this Python module as a library.


def fib(n):
    """Fibonacci example function

    Args:
      n (int): integer

    Returns:
      int: n-th Fibonacci number
    """
    assert n > 0
    a, b = 1, 1
    for _i in range(n - 1):
        a, b = b, a + b
    return a


class DockerComposeGraph(Digraph):

    # def __init__(self, compose_file):
    #     super().__init__()
    #     self.compose_files: list[pathlib.Path] = []

    def parse_docker_compose(self, yaml: pathlib.Path, docker_compose_chainmap: dict = {}):

        print(os.path.relpath(yaml, os.getcwd()))  # ../deadline-docker/10.2/docker-compose.yaml
        print(os.path.relpath(os.getcwd(), yaml))  # ../../../docker-graph

        print(pathlib.Path().cwd().relative_to(yaml))

        # working_dir = pathlib.Path().absolute()

        # print(os.path.relpath(yaml.parent, start=pathlib.Path.cwd()))

        with open(yaml, "r") as fr:
            docker_compose_chainmap.update(pyyaml.safe_load(fr))

        # print(docker_compose_chainmap)

        for include in docker_compose_chainmap.get("include", []):
            for included_docker_compose in include.values():
                for _path in included_docker_compose:
                    # print(yaml)
                    # print(_path)
                    # print(yaml.relative_to(_path))
                    # yaml = pathlib.Path(_path).resolve()
                    # # os.path.relpath(_path, start=yaml)
                    # docker_compose_include = pathlib.Path(_path).absolute()
                    # # docker_compose_include = pathlib.Path(_path).resolve()
                    # # print(_path)
                    # # print(pathlib.Path(_path).resolve().absolute())
                    self.parse_docker_compose(yaml=pathlib.Path(os.path.relpath(pathlib.Path(_path).parent, start=pathlib.Path.cwd())))
                # self.parse_docker_compose(included_docker_compose., docker_compose_chainmap)

        # self.compose_files.insert(0, docker_compose_chainmap)

        return docker_compose_chainmap

    # def _parse_docker_compose_includes(self, yaml: pathlib.Path):
    #
    #     with open(yaml, "r") as fr:
    #         docker_compose_chainmap = pyyaml.safe_load(fr)
    #
    #     self.compose_files.append(docker_compose_chainmap)
    #
    # def parse_includes(self):
    #     for compose_file in self.compose_files[0]["includes"]:




"""
from docker_graph.docker_graph import DockerComposeGraph
from pathlib import Path
dcg = DockerComposeGraph()
dcg.parse_docker_compose(Path("/home/michael/git/repos/deadline-docker/10.2/docker-compose.yaml"))


"""



# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Just a Fibonacci demonstration")
    parser.add_argument(
        "--version",
        action="version",
        version=f"docker-graph {__version__}",
    )
    parser.add_argument(dest="n", help="n-th Fibonacci number", type=int, metavar="INT")
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Starting crazy calculations...")
    print(f"The {args.n}-th Fibonacci number is {fib(args.n)}")
    _logger.info("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m docker_graph.skeleton 42
    #
    run()
