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
import pydot
from collections import ChainMap
import dotenv

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

    # result = {}

    # def __init__(self, compose_file):
    #     super().__init__()
    #     self.compose_files: list[pathlib.Path] = []

    def _to_abs_path(
            self,
            root_path,
            rel_path
    ) -> pathlib.Path:

        abs_path = os.path.join(root_path, rel_path)

        _logger.debug(f"{rel_path} -> {abs_path}")

        return pathlib.Path(abs_path)

    def parse_docker_compose(self, yaml: pathlib.Path, root_path: [pathlib.Path, None] = None, ret=None):

        if not yaml.is_absolute():
            _logger.debug(yaml)
            _abs_yaml = self._to_abs_path(
                root_path=root_path,
                rel_path=yaml,
            )
        else:
            _abs_yaml = yaml
            root_path = _abs_yaml.parent

        _abs_yaml = _abs_yaml.resolve()

        print(f"Processing {_abs_yaml.as_posix()}")

        with open(_abs_yaml, "r") as fr:
            docker_compose_chainmap = pyyaml.safe_load(fr)

        if ret is None:
            ret = []

        ret.append(docker_compose_chainmap)

        # self.result.update(docker_compose_chainmap)

        _logger.debug(docker_compose_chainmap.get("include", []))

        for include in docker_compose_chainmap.get("include", []):
            for included_docker_compose in include.get("path", []):
                _logger.debug(included_docker_compose)
                pathlib_path = pathlib.Path(included_docker_compose)
                _logger.debug(pathlib_path)

                self.parse_docker_compose(
                    yaml=pathlib_path,
                    root_path=root_path,
                    ret=ret,
                )

                # yield included_docker_compose

        return ret

        # return self.result

    def load_dotenv(self, env: pathlib.Path):
        dotenv.load_dotenv(env)

    def process_graph(
            self,
            tree,
            graph: [pydot.Dot, None] = None
    ):

        if graph is None:
            graph = pydot.Dot("my_graph", graph_type="digraph", bgcolor="yellow")

            if isinstance(tree, dict):
                if "services" in tree:
                    services = tree["services"]
                    for service in services:
                        node = pydot.Node(service, label=service)
                        graph.add_node(node)
                for key, value in tree.items():
                    if isinstance(value, dict):
                        self.process_graph(value)
                    elif isinstance(value, list):
                        for item in value:
                            self.process_graph(item)
                    else:
                        print(f"{value} -> {os.path.expandvars(str(value))}")
                        tree[key] = value
            elif isinstance(tree, list):
                for obj in tree:
                    self.process_graph(obj)

            elif isinstance(tree, str):
                print(f"{tree} -> {os.path.expandvars(str(tree))}")

        graph.write_png("graph.png")

        return graph


    # def expand_vars(self, nested_obj):
    #     if isinstance(nested_obj, dict):
    #         for key, value in nested_obj.items():
    #             if isinstance(value, dict):
    #                 self.expand_vars(value)
    #             elif isinstance(value, list):
    #                 for item in value:
    #                     self.expand_vars(item)
    #             else:
    #                 print(f"{value} -> {os.path.expandvars(str(value))}")
    #                 nested_obj[key] = value
    #     elif isinstance(nested_obj, list):
    #         for obj in nested_obj:
    #             self.expand_vars(obj)
    #
    #     elif isinstance(nested_obj, str):
    #         print(f"{nested_obj} -> {os.path.expandvars(str(nested_obj))}")

            # nested_dict = {'outer_key': {'inner_key1': 'value1', 'inner_key2': 'value2'}}
            # iterate_nested_dict(nested_dict)



"""
from docker_graph.docker_graph import DockerComposeGraph
import json
from pathlib import Path
dcg = DockerComposeGraph()
tree = dcg.parse_docker_compose(Path("/home/michael/git/repos/deadline-docker/10.2/docker-compose.yaml"))
# j = json.dumps(tree, indent=2)
# print(j)

dcg.load_dotenv(Path("/home/michael/git/repos/deadline-docker/10.2/.env"))

# dcg.expand_vars(tree)
dcg.process_graph(tree)

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
