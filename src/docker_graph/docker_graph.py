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


# def fib(n):
#     """Fibonacci example function
#
#     Args:
#       n (int): integer
#
#     Returns:
#       int: n-th Fibonacci number
#     """
#     assert n > 0
#     a, b = 1, 1
#     for _i in range(n - 1):
#         a, b = b, a + b
#     return a


class DockerComposeGraph:

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

    def iterate_trees(self, trees):
        primary_tree = trees.pop(0)

        primary_graph = self.get_primary_graph(primary_tree)

        # for secondary_tree in trees:
        #     print

    def get_primary_graph(self, tree):
        # graph = pydot.

        # include = tree.get("include", [])
        services = tree.get("services", [])
        # networks = tree.get("networks", [])
        # volumes = tree.get("volumes", [])

        # if graph is None:
        graph = pydot.Dot(
            "my_graph",
            rankdir="TB",
            graph_type="digraph",
            bgcolor="#2f2f2f",
        )

        cluster_services = pydot.Cluster(
            graph_name="cluster_services",
            label="cluster_services",
            color="magenta",
        )
        graph.add_subgraph(cluster_services)

        cluster_ports = pydot.Cluster(
            graph_name="cluster_ports",
            label="cluster_ports",
            color="red",
        )
        graph.add_subgraph(cluster_ports)

        cluster_images = pydot.Cluster(
            graph_name="cluster_images",
            label="cluster_images",
            color="yellow",
        )
        graph.add_subgraph(cluster_images)

        # cluster_volumes = pydot.Cluster(
        #     graph_name="cluster_volumes",
        #     label="cluster_volumes",
        #     color="blue",
        # )
        # graph.add_subgraph(cluster_volumes)

        cluster_networks = pydot.Cluster(
            graph_name="cluster_networks",
            label="cluster_networks",
            color="blue",
        )
        graph.add_subgraph(cluster_networks)

        #######################
        # Get all ports
        _ports = []
        for service_name, service_values in services.items():
            ports = service_values.get("ports", [])
            for port_tuple in ports:
                port_host, port_container = os.path.expandvars(port_tuple).split(":")

                _ports.append(
                    {
                        "port_host": f"{service_name}:{port_host}",
                        # f"{service_name}_port_container": f"{service_name}_{port_container}"
                        f"{service_name}_port_container": f"{port_container}"
                    }
                )

        for port_mapping in _ports:
            node_host = pydot.Node(
                name=port_mapping["port_host"],
                label=port_mapping["port_host"],
                shape="circle",
            )

            cluster_ports.add_node(node_host)
        # all ports
        #######################

        #######################
        # Get all images
        _images = []
        for service_name, service_values in services.items():
            image = service_values.get("image", None)
            if image is not None:
                _images.append({
                    f"image_host": image,
                    f"image_{service_name}": image
                })

        # _images = list(set(_images))

        for image in _images:
            node = pydot.Node(
                name=image["image_host"],
                label=image["image_host"],
            )

            cluster_images.add_node(node)
        # all images
        #######################

        #######################
        # Get all service volumes
        _volumes_service = []
        for service_name, service_values in services.items():
            volumes_service = service_values.get("volumes", [])
            for volumes_service_tuple in volumes_service:
                # print(volumes_service_tuple)
                volumes_service_host, volumes_service_container = os.path.expandvars(volumes_service_tuple).split(":", maxsplit=1)

                _volumes_service.append(
                    {
                        f"volumes_service_host": f"{service_name}:{volumes_service_host}",
                        f"{service_name}_volumes_service_container": f"{volumes_service_container}"
                    }
                )

        for volume_service_mapping in _volumes_service:
            node = pydot.Node(
                name=volume_service_mapping["volumes_service_host"],
                label=volume_service_mapping["volumes_service_host"],
                shape="triangle",
                color="white"
            )

            cluster_volumes.add_node(node)
        # service volumes
        ##############################

        #######################
        # Get all service networks
        _networks = []
        for service_name, service_values in services.items():
            _networks.extend(service_values.get("networks", []))

        _networks = list(set(_networks))

        for network in _networks:
            node = pydot.Node(
                name=network,
                label=network,
            )

            cluster_networks.add_node(node)
        # service networks
        ##############################

        # Individual Services
        for service_name, service_values in services.items():
            cluster_service = pydot.Cluster(
                graph_name=service_name,
                label=service_name,
                # simplify=True,
                rankdir="TB",
                color="cyan",
            )

            if service_values.get('hostname', None) is not None:
                node_hostname = pydot.Node(
                    f"{service_name}_{service_values.get('hostname', None)}",
                )
                cluster_service.add_node(node_hostname)

            image = service_values.get("image", None)
            if image is not None:
                node = pydot.Node(
                    name=f"{service_name}_{image}",
                    label=image,
                )
                cluster_service.add_node(node)

                edge = pydot.Edge(
                    src=image,
                    dst=f"{service_name}_{image}",
                )
                graph.add_edge(edge)

            # Service ports
            for port_mapping in _ports:

                p = port_mapping.get(f"{service_name}_port_container", None)

                if p is not None:
                    node_host = pydot.Node(
                        name=port_mapping.get(f"{service_name}_port_container"),
                        label=port_mapping.get(f"{service_name}_port_container"),
                        shape="circle",
                    )

                    edge = pydot.Edge(
                        src=port_mapping.get(f"port_host"),
                        dst=node_host,
                    )

                    graph.add_edge(edge)

                    cluster_service.add_node(node_host)

            ##############

            cluster_services.add_subgraph(cluster_service)

        graph.write_png("graph2.png")
        return graph


    def process_graph(
            self,
            tree,
            # graph: [pydot.Dot, None] = None
    ):

        # print(tree)

        # if graph is None:
        graph = pydot.Dot(
            "my_graph",
            rankdir="TB",
            graph_type="digraph",
            bgcolor="#2f2f2f",
        )

        for compose in tree:
            print(compose)

            includes_compose = compose.get("include", [])
            # print(f"{includes_compose = }")
            services_compose = compose.get("services", [])
            print(f"{services_compose = }")
            networks_compose = compose.get("networks", [])
            # print(f"{networks_compose = }")
            volumes_compose = compose.get("volumes", [])
            # print(f"{volumes_compose = }")

            for services, values in services_compose.items():

                print(f"{values = }")

                service_name = services
                image_name = values.get("image", None)
                service_depends_on = values.get("depends_on", [])
                print(f"{service_depends_on = }")
                # service_restart = compose[service].get("restart", None)
                # container_name = compose[service].get("container_name", None)
                # host_name = service.get("host_name", None)
                # domain_name = service.get("domain_name", None)
                # service_networks = service.get("networks", None)
                # service_environment = service.get("environment", None)
                service_ports = values.get("ports", [])
                # service_volumes = service.get("volumes", None)

                # _nodes = graph.get_nodes()

                # graph_service = pydot.Subgraph("service_graph", graph_type="digraph", bgcolor="green")

                # if service_name not in [_node.get_name() for _node in _nodes]:
                #     graph.add_node(pydot.Node(service_name))



                # graph_service = pydot.Dot(service_name, graph_type="digraph", bgcolor="yellow")
                # graph_service = pydot.Subgraph(service_name, graph_type="digraph", bgcolor="yellow")
                graph_cluster = pydot.Cluster(
                    service_name,
                    label=service_name,
                    graph_type="digraph",
                    rankdir="TB",
                    bgcolor="brown",
                    shape="box",
                    simplify=True,
                    strict=True,
                    style="rounded",
                )

                node_image = pydot.Node(image_name, bgcolor="3a3a3a")
                graph_cluster.add_node(node_image)

                # depends_on
                # edges only
                for depends_on in service_depends_on:
                    node = [n for n in graph.get_nodes() if n.get_name() == depends_on]
                    if bool(node):
                        pass
                    else:
                        node = pydot.Node(
                                depends_on,
                                label=depends_on,
                                shape="database",
                                bgcolor="blue",
                            )

                        graph_cluster.add_node(
                            node,
                        )

                    edge = pydot.Edge(
                        src=service_name,
                        dst=node,
                        style="dashed",
                    )
                    graph.add_edge(edge)

                # ports
                for port in service_ports:
                    port_host, port_container = os.path.expandvars(port).split(":")

                    node_container = [n for n in graph_cluster.get_nodes() if n.get_name() == f"{service_name}_{port_container}"]
                    if bool(node_container):
                        pass
                    else:
                        node_container = pydot.Node(
                            f"{service_name}_{port_container}",
                            label=port_container,
                            shape="circle",
                            bgcolor="red",
                        )

                        graph_cluster.add_node(node_container)

                    edge_container = pydot.Edge(
                        src=node_container,
                        dst=service_name,
                    )

                    graph.add_edge(edge_container)

                    # _port = os.path.expandvars(port).replace(":", " -> ")

                    node_host = [n for n in graph.get_nodes() if n.get_name() == port_host]
                    if bool(node_host):
                        pass
                    else:
                        node_host = pydot.Node(
                            port_host,
                            shape="circle",
                            bgcolor="red",
                        )

                        graph.add_node(node_host)

                    edge_host = pydot.Edge(
                        src=node_host,
                        dst=node_container,
                    )

                    graph.add_edge(edge_host)


                graph_cluster.add_node(pydot.Node(service_name))
                # graph.add_node(pydot.Node("service_name"))
                #
                graph.add_subgraph(graph_cluster)



                # if not bool(graph_service):
                #     # if image_name not in [_node.get_name() for _node in _nodes]:
                #     graph_service = pydot.Subgraph(image_name, graph_type="digraph", bgcolor="green")
                #     for network in networks_compose:
                #         print(network)
                #         graph_service.add_node(pydot.Node(network))
                #     graph.add_subgraph(graph_service)
                # else:
                #     graph.add_subgraph(graph_service[0])

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
    # print(f"The {args.n}-th Fibonacci number is {fib(args.n)}")
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
