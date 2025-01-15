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




The basic structure of a Docker YAML:

root: [dict]
- [ ] include: list[dict[str, list]]
  - path: list[str]
    - main
    - override
    - override
    - ...
- [ ] services
  - service_name: [dict[str, str|list]
    - [x] container_name: [str]
    - [x] hostname: [str]
    - [x] restart: [str]
    - [x] domainname: [str]
    - [x] depends_on: [list[dict[str, list]]]
    - [x] networks: [list[str]]
    - [x] environment: [list[str]]
    - [x] command: [str]
    - [x] ports: [list[str]]
    - [x] volumes: [list[str]]
    - [x] image: [str] or
    - [ ] build: [dict[str, str|list[str]]]
      - context: [str]
      - dockerfile: [str]
      - target: [str]
      - args: [list[str]]
- [ ] volumes
- [ ] networks
...


"""
import os
import argparse
import logging
import pathlib
import sys
from typing import Any

import yaml as pyyaml
import diagrams
from diagrams import custom
from diagrams.generic.network import Subnet, Switch
from diagrams.generic.storage import Storage
from diagrams.onprem.container import Docker
import dotenv
import uuid
from collections import OrderedDict

# from docker_graph import __version__

__author__ = "Michael Mussato"
__copyright__ = "Michael Mussato"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from docker_graph.skeleton import fib`,
# when using this Python module as a library.


class NetworkPort(custom.Custom):
    def __init__(self, label, *args, **kwargs):
        super().__init__(
            label=label,
            icon_path="/home/michael/git/repos/docker-graph/src/docker_graph/resources/network-port.png",
            *args,
            **kwargs,
        )


class DummyPort(custom.Custom):
    def __init__(self, label, *args, **kwargs):
        super().__init__(
            label=label,
            icon_path="",
            *args,
            **kwargs,
        )


class DockerComposeGraph:

    def __init__(self):

        self.docker_yaml: [pathlib.Path | None] = None

        self.services: [list[dict] | None] = None
        self.depends_on: [dict[str, list | dict] | None] = None
        self.network_mappings: [dict[str, list[str]] | None] = None
        self.port_mappings: [dict[str, list[str]] | None] = None
        self.volume_mappings: [dict[str, list[str]] | None] = None

        # Main Graph
        self.graph = self.get_primary_graph()

        # Clusters
        ## Root Clusters
        ### Services
        self.root_services_cluster = self.add_cluster_root_services()
        ### Networks
        self.root_networks_cluster = self.add_cluster_root_networks()
        ### Volumes
        self.root_volumes_cluster = self.add_cluster_root_volumes()
        ### Ports
        self.root_ports_cluster = self.add_cluster_root_ports()

    def write_png(self, path):

        self.graph.write(
            path=path,
            format="png",
        )

    def write_dot(self, path):
        self.graph.write(
            path=path,
            format="dot",
        )

    def as_dot(self):
        return self.graph

    def _to_abs_path(
            self,
            root_path,
            rel_path
    ) -> pathlib.Path:

        abs_path = os.path.join(root_path, rel_path)

        _logger.debug(f"{rel_path} -> {abs_path}")

        return pathlib.Path(abs_path)

    def parse_docker_compose(
            self,
            yaml: pathlib.Path,
            root_path: [pathlib.Path, None] = None,
            ret=None,
    ) -> list[dict]:

        if self.docker_yaml is None:
            self.docker_yaml = yaml
            # self.graph.set_label(self.docker_yaml.as_posix())

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
        _logger.info(f"Processing {_abs_yaml.as_posix()}")

        with open(_abs_yaml, "r") as fr:
            docker_compose_chainmap = pyyaml.full_load(fr)

        # the first iteration
        # of recursive function
        if ret is None:
            ret = []

        ret.append(docker_compose_chainmap)

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

        return ret

    def load_dotenv(self, env: pathlib.Path):
        dotenv.load_dotenv(env)

    def iterate_trees(self, trees):

        self.services = self._get_services(trees)
        self.depends_on = self._get_depends_on(trees)
        self.port_mappings = self._get_ports(trees)
        self.volume_mappings = self._get_volumes(trees)
        self.network_mappings = self._get_networks(trees)

        self.compute_graph()

    def compute_graph(self):

        root_network_nodes = self.add_nodes_network()
        root_volume_nodes = self.add_volume_nodes()
        root_port_nodes = self.add_nodes_port()

        _service_clusters = []
        for service in self.services:
            service_cluster, dummy_port = self.add_cluster_service(
                service,
            )

            _depends_on = service.get("service_config", {}).get("depends_on", {})
            if isinstance(_depends_on, list):
                _depends_on = self._conform_depends_on(_depends_on)

            # print(service)
            # print(_depends_on)

            _service_clusters.append(
                {
                    service_cluster: {
                        "dummy_port": dummy_port,
                        **_depends_on},
                }
            )

            service_networks = self.add_service_networks(
                service_cluster,
                service,
            )

            self.link_networks(
                root_network_nodes,
                service_networks,
            )

            service_volumes = self.add_service_volumes(
                service_cluster,
                service,
            )

            self.link_volumes(
                root_volume_nodes,
                service_volumes,
            )

            service_ports = self.add_service_ports(
                service_cluster,
                service,
            )

            self.link_ports(
                root_port_nodes,
                service_ports,
            )

        self.link_depends_on(_service_clusters)

        self.graph.dot.render(
            format="png",
            view=False,
            quiet=True,
        )

    def _get_services(
            self,
            trees: list[dict]
    ):

        services = []

        for tree in trees:
            _logger.debug(tree)

            for service_name, service_config in tree.get("services", {}).items():

                services.append(
                    {
                        "service_name": service_name,
                        "service_config": service_config,
                     }
                )

        _logger.debug(f"All {services = }")
        print(f"All {services = }")

        return services

    def _get_ports(
            self,
            trees,
    ) -> dict[str, list[str]]:

        port_mappings = {
            "root": [],
            "services": [],
        }

        for tree in trees:
            service_ports = self._get_service_ports(
                tree=tree,
            )

            port_mappings["services"].extend(service_ports)

        _logger.debug(f"All {port_mappings = }")
        print(f"All {port_mappings = }")

        return port_mappings

    @staticmethod
    def _get_service_ports(
            tree: dict,
    ) -> list[dict[str, list[str]]]:

        port_mappings = []

        services: dict = tree.get("services", {})

        for service_name, service_config in services.items():
            ports = service_config.get("ports", [])

            port_mappings.append(
                {
                    # service_name: ports
                    service_name: [os.path.expandvars(p) for p in ports]
                }
            )

        return port_mappings

    def _get_volumes(
            self,
            trees,
    ) -> dict[str, list[str]]:

        volume_mappings = {
            "root": [],
            "services": [],
        }

        for tree in trees:
            service_volumes = self._get_service_volumes(
                tree=tree,
            )
            volume_mappings["services"].extend(service_volumes)

        _logger.debug(f"All {volume_mappings = }")
        print(f"All {volume_mappings = }")

        return volume_mappings

    @staticmethod
    def _get_service_volumes(
            tree: dict,
    ) -> list[dict[str, list[str]]]:

        volume_mappings = []

        services: dict = tree.get("services", {})

        for service_name, service_config in services.items():
            volumes = service_config.get("volumes", [])

            volume_mappings.append(
                {
                    # service_name: volumes
                    service_name: [os.path.expandvars(v) for v in volumes]
                }
            )

        return volume_mappings

    def _get_networks(
            self,
            trees,
    ) -> dict[str, list[str]]:

        network_mappings = {
            "root": [],
            "services": [],
        }

        for tree in trees:
            service_networks = self._get_service_networks(
                tree=tree,
            )
            network_mappings["services"].extend(service_networks)

        _logger.debug(f"All {network_mappings = }")
        print(f"All {network_mappings = }")

        return network_mappings

    @staticmethod
    def _get_service_networks(
            tree: dict,
    ) -> list[dict[str, list[str]]]:

        network_mappings = []

        services: dict = tree.get("services", {})

        for service_name, service_config in services.items():
            networks = service_config.get("networks", [])

            network_mappings.append(
                {
                    service_name: networks
                }
            )

        return network_mappings

    def _get_depends_on(
            self,
            trees,
    ) -> dict[str, list | dict]:

        depends_on_mappings = {
            "root": [],
            "services": [],
        }

        for tree in trees:
            service_depends_on = self._get_service_depends_on(
                tree=tree,
            )

            depends_on_mappings["services"].extend(service_depends_on)

            # Todo
            # root_volumes = self._get_root_volumes(
            #     tree=tree,
            # )
            # volume_mappings["root"].extend(root_volumes)

        # _logger.debug(f"All {service_depends_mappings = }")
        # print(f"All {service_depends_mappings = }")
        return depends_on_mappings

    def _get_service_depends_on(
            self,
            tree: dict,
    ) -> list[dict[Any, dict]]:

        depends_on_mappings = []

        services: dict = tree.get("services", {})

        for service_name, service_config in services.items():
            depends_on = service_config.get("depends_on", [])

            if len(depends_on) == 0:
                # No need to keep what didn't exist
                # in the first place:
                #  {'dagster_dev': []},
                continue

            _depends_on_conform = self._conform_depends_on(depends_on)

            depends_on_mappings.append(
                {
                    service_name: self._conform_depends_on(depends_on)
                }
            )

        return depends_on_mappings

    def _conform_depends_on(
            self,
            depends_on: [list | dict],
    ) -> dict:

        # a depends_on dependency can come in the
        # form of a dict[list]:
        # {'deadline-repository-installer-10-2': ['mongodb-10-2']}
        # or as a dict[dict[str, str]]:
        # {'deadline-client-installer-10-2': {'deadline-repository-installer-10-2': {'condition': 'service_completed_successfully'}}}
        #
        # potentially even more schemas
        #
        # Hence: conform

        _depends_on = depends_on

        if isinstance(depends_on, list):
            _depends_on = {}
            for i in depends_on:
                _depends_on[i] = {
                    "condition": None,
                }

        return _depends_on

    # def _get_root_ports(self, tree):
    #     # Todo
    #     raise NotImplementedError

    # def _get_root_networks(self, tree):
    #     # Todo
    #     raise NotImplementedError

    # def _get_root_volumes(self, tree):
    #     # Todo
    #     raise NotImplementedError

    @staticmethod
    def get_primary_graph():
        with diagrams.Diagram(
            show=False,
            name="main_graph",
            # direction="LR",
            graph_attr={
                "label": "my_graph",
                # "rankdir": "LR",
                "graph_type": "digraph",
                "splines": "False",
                "pad": "1.5",
                "nodesep": "0.3",
                "ranksep": "10",
                "bgcolor": "#2f2f2f",
            },
        ) as main_graph:
            return main_graph

    def add_cluster_root_services(self):
        with self.graph:
            with diagrams.Cluster(
                label="root_services",
                direction="TB",
                graph_attr={
                    "color": "magenta",
                    # "rankdir": "TB",
                },
            ) as cluster_root_services:
                return cluster_root_services

    def add_cluster_root_networks(self):
        with self.graph:
            with diagrams.Cluster(
                label="root_networks",
                graph_attr={
                    "color": "red",
                },
            ) as networks_cluster:
                return networks_cluster

    def add_cluster_service(self, service):
        with self.graph:
            with self.root_services_cluster:
                with diagrams.Cluster(
                    label=f"service_{service.get('service_name')}",
                    # graph_name=f"cluster_service_{service.get('service_name')}",
                    direction="TB",
                    # graph_attr={
                    #     "color": "white",
                    #     "shape": "square",
                    #     "style": "rounded",
                    # },
                ) as service_cluster:
                    dummy_port = DummyPort(
                        label=f"dummyport_service_{service.get('service_name')}"
                    )
                    return service_cluster, dummy_port

    def add_service_networks(
            self,
            services_cluster,
            service,
    ):
        with self.graph:
            with self.root_services_cluster:
                with services_cluster:
                    with diagrams.Cluster(
                        label="networks",
                    ):
                        _network_nodes = []
                        for network in service.get("service_config", {}).get("networks", []):
                            _network_nodes.append(
                                Subnet(
                                    nodeid=f"{service.get('service_name')}_{network}",
                                    label=network,
                                )
                            )
                        return _network_nodes

    def add_service_volumes(
            self,
            services_cluster,
            service,
    ):
        with self.graph:
            with self.root_services_cluster:
                with services_cluster:
                    with diagrams.Cluster(
                        label="volumes",
                    ):
                        _volume_nodes = []
                        for volume in service.get("service_config", {}).get("volumes", []):
                            _volume_nodes.append(
                                Storage(
                                    # nodeid=f"{service.get('service_name')}_{volume}",
                                    nodeid="%s_%s" % (service.get('service_name'), os.path.expandvars(volume).replace(":", "%")),
                                    label=os.path.expandvars(volume),
                                )
                            )
                        return _volume_nodes

    def add_service_ports(
            self,
            services_cluster,
            service,
    ):
        with self.graph:
            with self.root_services_cluster:
                with services_cluster:
                    with diagrams.Cluster(
                        label="ports",
                    ):
                        _port_nodes = []
                        for port in service.get("service_config", {}).get("ports", []):
                            _port_nodes.append(
                                NetworkPort(
                                    # nodeid=f"{service.get('service_name')}_{port}",
                                    nodeid="%s_%s" % (service.get('service_name'), os.path.expandvars(port).replace(":", "%")),
                                    label=os.path.expandvars(port),
                                )
                            )
                        return _port_nodes


    #     # # #######################
    #     # # # Get all images
    #     # # _images = []
    #     # # for service_name, service_values in services.items():
    #     # #     image = service_values.get("image", None)
    #     # #     if image is not None:
    #     # #         _images.append({
    #     # #             f"image_host": image,
    #     # #             f"image_{service_name}": image
    #     # #         })
    #     # #
    #     # # # _images = list(set(_images))
    #     # #
    #     # # for image in _images:
    #     # #     node = pydot.Node(
    #     # #         name=image["image_host"],
    #     # #         label=image["image_host"],
    #     # #     )
    #     # #
    #     # #     self.cluster_root_images.add_node(node)
    #     # # # all images
    #     # # #######################

    def add_cluster_root_ports(self):
        with self.graph:
            with diagrams.Cluster(
                label="root_ports",
                graph_attr={
                    "color": "green",
                },
            ) as ports_cluster:
                return ports_cluster

    def add_cluster_root_volumes(self):
        with self.graph:
            with diagrams.Cluster(
                label="root_volumes",
                graph_attr={
                    "color": "red",
                },
            ) as volumes_cluster:
                return volumes_cluster

    def _get_root_network_nodes(self):
        root_network_nodes = []
        for network_mapping in self.network_mappings.get("services", []):
            for v in network_mapping.values():
                root_network_nodes.extend(v)
        return list(dict.fromkeys(root_network_nodes))

    def add_nodes_network(self):

        root_network_nodes = self._get_root_network_nodes()

        with self.graph:
            with self.root_networks_cluster:
                _root_network_nodes = [
                    Subnet(
                        nodeid=root_network_node.replace(":", "%"),
                        label=root_network_node,
                    ) for root_network_node in root_network_nodes
                ]

                return _root_network_nodes

    def _get_root_volume_nodes(self):
        root_volume_nodes = []
        for volume_mapping in self.volume_mappings.get("services", []):
            for v in volume_mapping.values():
                root_volume_nodes.extend(v)
        return list(dict.fromkeys(root_volume_nodes))

    def add_volume_nodes(self):

        root_volume_nodes = self._get_root_volume_nodes()

        with self.graph:
            with self.root_volumes_cluster:
                _root_volume_nodes = [
                    Storage(
                        nodeid=root_volume_node.replace(":", "%"),
                        label=root_volume_node,
                    ) for root_volume_node in root_volume_nodes
                ]

                return _root_volume_nodes

    def _get_root_port_nodes(self):
        root_port_nodes = []
        for port_mapping in self.port_mappings.get("services", []):
            for v in port_mapping.values():
                root_port_nodes.extend(v)
        return list(dict.fromkeys(root_port_nodes))

    def add_nodes_port(self):

        root_port_nodes = self._get_root_port_nodes()

        with self.graph:
            with self.root_ports_cluster:
                _root_port_nodes = [
                    NetworkPort(
                        nodeid=root_port_node.replace(":", "%"),
                        label=root_port_node,
                    ) for root_port_node in root_port_nodes
                ]

                return _root_port_nodes

    def link_networks(
            self,
            root_network_nodes,
            service_networks,
    ):
        for root_network_node in root_network_nodes:
            src = root_network_node
            for service_network in service_networks:
                if src.label == service_network.label:
                    dst = service_network
                    src << diagrams.Edge(
                        tailport="e",
                        headport="w",
                        color="orange",
                        arrowhead="dot",
                        arrowtail="dot",
                    ) >> dst

    def link_volumes(
            self,
            root_volume_nodes,
            service_volumes,
    ):
        for root_volume_node in root_volume_nodes:
            src = root_volume_node
            for service_volume in service_volumes:
                if src.label == service_volume.label:
                    dst = service_volume
                    src << diagrams.Edge(
                        tailport="e",
                        headport="w",
                        color="green",
                        arrowhead="dot",
                        arrowtail="dot",
                    ) >> dst

    def link_ports(
            self,
            root_port_nodes,
            service_ports,
    ):
        for root_port_node in root_port_nodes:
            src = root_port_node
            for service_port in service_ports:
                if src.label == service_port.label:
                    dst = service_port
                    src << diagrams.Edge(
                        tailport="e",
                        headport="w",
                        color="red",
                        arrowhead="dot",
                        arrowtail="dot",
                    ) >> dst

    def link_depends_on(
            self,
            service_clusters,
    ):
        print(service_clusters)

        clusters = []
        for i in service_clusters:
            clusters.extend(i.keys())

        clusters = list(set(clusters))

        # clusters = [i for i in service_clusters]
        print(clusters)

        for service_cluster in service_clusters:
            for src, dst_dict in service_cluster.items():

                if len(dst_dict) < 2:
                    # print(dst_dict)
                    continue

                # print(k)  # <diagrams.Cluster object at 0x71360c3c6390>
                print(f"{src.label = }")  # service_server

                src = dst_dict.get("dummy_port", None)
                # print(k.node())
                # print(v)  # {'postgres': {'condition': 'service_healthy'}, 'redis': {'condition': 'service_started'}}

                for _service in dst_dict.keys():
                    service = f"service_{_service}"
                    print(f"{service = }")
                    for cluster in clusters:
                        if cluster.label == service:
                            dst = cluster
                            with self.graph:
                                with self.root_services_cluster:
                                    with dst:
                                        _dst = DummyPort(
                                            nodeid=str(uuid.uuid4()),
                                            label="",
                                        )
                            src << diagrams.Edge(
                                tailport="e",
                                headport="w",
                                color="purple",
                                arrowhead="dot",
                                arrowtail="normal",
                                # ltail=src.label,
                                # lhead=dst.label,
                            ) << _dst

                # for k_, v_ in v.items():
                #     for service_cluster_ in service_clusters:
                #         for k__, v__ in service_cluster_.items():
                #             if k__.label == f"service_{k_}":
                #                 # print(k__.label)
                #                 dst = k__
                #                 print(f"{dst.label = }")
                #                 # src << diagrams.Edge(
                #                 #     tailport="e",
                #                 #     headport="w",
                #                 #     color="purple",
                #                 #     arrowhead="dot",
                #                 #     arrowtail="dot",
                #                 # ) >> dst

            # src = service_cluster
            # for service_port in service_ports:
            #     if src.label == service_port.label:
            #         dst = service_port
            #         src << diagrams.Edge(
            #             tailport="e",
            #             headport="w",
            #             color="red",
            #             arrowhead="dot",
            #             arrowtail="dot",
            #         ) >> dst


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
    # parser.add_argument(
    #     "--version",
    #     action="version",
    #     version=f"docker-graph {__version__}",
    # )
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
    # # ^  This is a guard statement that will prevent the following code from
    # #    being executed in the case someone imports this file instead of
    # #    executing it as a script.
    # #    https://docs.python.org/3/library/__main__.html
    #
    # # After installing your project with pip, users can also run your Python
    # # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    # #
    # #     python -m docker_graph.skeleton 42
    # #
    # setup_logging(logging.DEBUG)
    # run()
    dcg = DockerComposeGraph()
    trees = dcg.parse_docker_compose(
        pathlib.Path("/home/michael/git/repos/docker-graph/tests/fixtures/deadline-docker/10.2/docker-compose.yaml")
    )

    # resolve environment variables (optional)
    dcg.load_dotenv(pathlib.Path("/home/michael/git/repos/docker-graph/tests/fixtures/deadline-docker/10.2/.env"))

    # dcg.expand_vars(tree)

    # with open("tree.json", "w") as fw:
    #     json.dump(tree, fw, indent=2)

    dcg.iterate_trees(trees)
    # # dcg.connect()
    # dcg.write_png(
    #     path=pathlib.Path(__file__).parent / "fixtures" / "out" / "main_graph.png",
    # )
    # dcg.write_dot(
    #     path=pathlib.Path(__file__).parent / "fixtures" / "out" / "main_graph.dot",
    # )

else:
    setup_logging(logging.DEBUG)
