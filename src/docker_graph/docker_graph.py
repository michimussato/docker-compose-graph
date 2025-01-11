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
import yaml as pyyaml
import pydot
import dotenv
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


class DockerComposeGraph:

    def __init__(
            self,
    ):

        self.docker_yaml: [pathlib.Path | None] = None

        self.services: [list[dict] | None] = None
        self.depends_on: [dict[str, list | dict] | None] = None
        self.network_mappings: [dict[str, list[str]] | None] = None
        self.port_mappings: [dict[str, list[str]] | None] = None
        self.volume_mappings: [dict[str, list[str]] | None] = None

        # Main Graph

        self.graph = pydot.Dot(
            graph_name="main_graph",
            label="my_graph",
            rankdir="LR",
            graph_type="digraph",
            bgcolor="#2f2f2f",
            # splines="polyline",
            splines=False,
            pad="1.5", nodesep="0.3", ranksep="10"
        )

        # Clusters

        ## Root Clusters

        self.cluster_root_include = pydot.Cluster(
            graph_name="cluster_root_include",
            label="cluster_root_include",
            color="magenta",
            rankdir="TB",
        )

        self.cluster_root_services = pydot.Cluster(
            graph_name="cluster_root_services",
            label="cluster_root_services",
            color="magenta",
            rankdir="TB",
        )

        ### Collection Clusters
        # Clusters summarize root and
        # services into one for easy
        # overview

        #### images

        # self.cluster_root_images = pydot.Cluster(
        #     graph_name="cluster_root_images",
        #     label="cluster_root_images",
        #     color="yellow",
        # )

        #### ports

        self.cluster_root_ports = pydot.Cluster(
            graph_name="cluster_root_ports",
            label="cluster_root_ports",
            color="red",
        )

        #### volumes

        self.cluster_root_volumes = pydot.Cluster(
            graph_name="cluster_root_volumes",
            label="cluster_root_volumes",
            color="red",
            rankdir="TB",
            graph_type="digraph",
            # shape="box",
            # style="rounded",
        )

        #### networks

        self.cluster_root_networks = pydot.Cluster(
            graph_name="cluster_root_networks",
            label="cluster_root_networks",
            color="red",
            rankdir="TB",
            graph_type="digraph",
            # shape="box",
            # style="rounded",
        )

        ## Service Clusters

        ### ports

        ### volumes

        # self.cluster_service_volumes = pydot.Cluster(
        #     graph_name="cluster_service_volumes",
        #     label="cluster_service_volumes",
        #     color="blue",
        # )

        ### networks

        self.cluster_service_networks = pydot.Cluster(
            graph_name="cluster_service_networks",
            label="cluster_service_networks",
            color="blue",
        )

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
            self.graph.set_label(self.docker_yaml.as_posix())

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

        self.services = self._get_serivces(trees)
        self.depends_on = self._get_depends_on(trees)
        self.port_mappings = self._get_ports(trees)
        self.volume_mappings = self._get_volumes(trees)
        self.network_mappings = self._get_networks(trees)

        primary_graph = self.get_primary_graph()

        # for secondary_tree in trees:
        #     print

    def _get_serivces(
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
            "services": {},
        }

        for tree in trees:
            service_ports: dict = self._get_service_ports(
                tree=tree,
            )

            port_mappings["services"].update(service_ports)

            # Todo
            # root_ports = self._get_root_ports(
            #     tree=tree,
            # )
            # port_mappings["root"].extend(root_ports)

        _logger.debug(f"All {port_mappings = }")
        print(f"All {port_mappings = }")

        return port_mappings

    @staticmethod
    def _get_service_ports(
            tree: dict,
    ) -> dict[str, list[str]]:

        port_mappings = {}

        services: dict = tree.get("services", {})

        for service_name, service_config in services.items():
            ports = service_config.get("ports", [])

            port_mappings[service_name] = ports

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

            # Todo
            # root_volumes = self._get_root_volumes(
            #     tree=tree,
            # )
            # volume_mappings["root"].extend(root_volumes)

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
                    service_name: volumes
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

            # Todo
            # root_volumes = self._get_root_volumes(
            #     tree=tree,
            # )
            # volume_mappings["root"].extend(root_volumes)

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
            "services": {},
        }

        for tree in trees:
            service_depends_on: dict = self._get_service_depends_on(
                tree=tree,
            )

            depends_on_mappings["services"].update(service_depends_on)

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
    ) -> dict[str, list[str]]:

        depends_on_mappings = {}

        services: dict = tree.get("services", {})

        for service_name, service_config in services.items():
            depends_on = service_config.get("depends_on", [])

            if len(depends_on) == 0:
                # No need to keep what didn't exist
                # in the first place:
                #  {'dagster_dev': []},
                continue

            _depends_on_conform = self._conform_depends_on(depends_on)

            depends_on_mappings.update(
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

    def _get_root_ports(self, tree):
        # Todo
        raise NotImplementedError

    def _get_root_networks(self, tree):
        # Todo
        raise NotImplementedError

    def _get_root_volumes(self, tree):
        # Todo
        raise NotImplementedError

    @staticmethod
    def get_name(item):
        # pydot seems to sometimes
        # return strings that are
        # wrapped inside quotation
        # marks. No-Go!
        assert isinstance(item, pydot.Common)
        return item.get_name().replace('"', '')

    @staticmethod
    def _get_service_label(
            service: dict,
    ) -> str:
        """
        Generate a Service Node label
        based on service[dict[str, str | dict]].
        This is a bit hacky but it's mostly
        cosmetics except for the TAGs/PLUGs.
        We retain the original service_config
        data this way.
        """

        service_name = service.get("service_name")
        service_config = service.get("service_config")

        ports: list = service_config.get("ports", [])
        if isinstance(ports, list):
            ports_container: list = [os.path.expandvars(p) for p in ports]
        elif isinstance(ports, pyyaml.YAMLObject):
            # OverrideArray() in
            # ~/repos/deadline-docker/src/Deadline/deadline_docker/assets.py
            # Todo: find a better solution
            ports_container: list = [os.path.expandvars(p) for p in ports.array]
        _p = []

        for p in ports_container:
            port_host, port_container = p.split(":", maxsplit=1)
            id_service_port = f"<PLUG_{service_name}__{port_host}__{port_container}> {port_container}"
            _p.append(id_service_port)

        depends_on: list = service_config.get("depends_on", [])

        _d = []
        for d in depends_on:
            id_service_depends_on = f"<PLUG_DEPENDS_ON_NODE-SERVICE_{d}> {d}"
            _d.append(id_service_depends_on)

        volumes: list = [os.path.expandvars(v.split(":")[1]) for v in service_config.get("volumes", [])]

        _v = []
        for v in volumes:
            id_service_volume = f"<PLUG_{service_name}__{v}> {v}"
            _v.append(id_service_volume)

        networks: list = [os.path.expandvars(n) for n in service_config.get("networks", [])]

        _n = []
        for n in networks:
            id_service_network = f"<PLUG_{n}> {n}"
            _n.append(id_service_network)

        restart: str = service_config.get("restart", "")

        _command = service_config.get("command", "-")
        if isinstance(_command, list):
            command = " ".join(_command)
        elif isinstance(_command, str):
            command = _command

        fields = OrderedDict({
            "service_name": service_name,
            "container_name": "{container_name|{" + os.path.expandvars(
                service_config.get("container_name", "-")) + "}}",
            "hostname": "{hostname|{" + os.path.expandvars(service_config.get("hostname", "-")) + "}}",
            "domainname": "{domainname|{" + os.path.expandvars(service_config.get("domainname", "-")) + "}}",
            "volumes": "{{" + "|".join([v for v in sorted(_v)]) + "}|volumes}",
            "restart": "{restart|{" + restart + "}}",
            "depends_on": "{{" + "|".join([d for d in sorted(_d)]) + "}|depends_on}",
            "image": "{image|{" + os.path.expandvars(service_config.get("image", "-")) + "}}",
            "ports": "{{" + "|".join([p for p in sorted(_p)]) + "}|exposed ports}",
            "networks": "{{" + "|".join([n for n in sorted(_n)]) + "}|networks}",
            "command": "{command|{" + os.path.expandvars(command) + "}}",
            "environment": "{environment|{" + "|".join([
                os.path.expandvars(e) for e in sorted(service_config.get(
                    "environment", [],
                ))
            ]) + "}}",
            # "build": os.path.expandvars(service_config.get("build", "-")),
        })

        ret = "|".join([v for k, v in fields.items()])

        return ret

    def get_primary_graph(self):

        self.graph.add_subgraph(self.cluster_root_services)
        self.graph.add_subgraph(self.cluster_root_ports)
        self.graph.add_subgraph(self.cluster_root_volumes)
        self.graph.add_subgraph(self.cluster_root_networks)
        # self.graph.add_subgraph(self.cluster_root_services)
        # self.graph.add_subgraph(self.cluster_service_depends_on)
        # self.graph.add_subgraph(self.cluster_root_images)
        # self.graph.add_subgraph(self.cluster_service_volumes)
        # self.graph.add_subgraph(self.cluster_service_networks)

        #######################
        # Get all Services and add them as clusters
        for service in self.services:
            cluster_service = pydot.Cluster(
                graph_name=f"cluster_service_{service.get('service_name')}",
                label=f"cluster_service_{service.get('service_name')}",
                color="white",
                rankdir="TB",
                shape="square",
                style="rounded",
            )

            node_service = pydot.Node(
                name=f"NODE-SERVICE_{service.get('service_name')}",
                label=self._get_service_label(service),
                shape="record",
                style="filled",
            )

            cluster_service.add_node(node_service)

            _depends_on_conform = self._conform_depends_on(service["service_config"].get("depends_on", []))

            # Todo:
            for depends_on in _depends_on_conform:

                src = self.get_name(node_service)

                edge = pydot.Edge(
                    dst=f"{src}:<PLUG_DEPENDS_ON_NODE-SERVICE_{depends_on}>",
                    src=f"NODE-SERVICE_{depends_on}",
                    # arrowhead="dot",
                    # tailhead="dot",
                    color="yellow",
                )

                # edge.set_headport("nw")
                # edge.set_tailport("ne")

                self.graph.add_edge(edge)

            self.cluster_root_services.add_subgraph(cluster_service)

        # all services
        #######################

        #######################
        # Get all Ports

        # Service Ports
        # Todo
        #  - [ ] Sorted

        _color = "black"
        _fillcolor = "white"

        for service_name, mappings in sorted(self.port_mappings["services"].items()):

            if isinstance(mappings, pyyaml.YAMLObject):
                # OverrideArray() in
                # ~/repos/deadline-docker/src/Deadline/deadline_docker/assets.py
                # Todo: find a better solution
                mappings = mappings.array

            for _mapping in sorted(mappings):
                port_host, port_container = os.path.expandvars(_mapping).split(":", maxsplit=1)
                node_host = pydot.Node(
                    name=f"{service_name}__{port_host}__{port_container}",
                    label=port_host,
                    shape="circle",
                    color=_color,
                    fillcolor=_fillcolor,
                    style="filled",
                )

                self.cluster_root_ports.add_node(node_host)

                for sg in self.cluster_root_services.get_subgraphs():
                    if self.get_name(sg) == f"cluster_cluster_service_{service_name}":
                        n = sg.get_node(name=f"NODE-SERVICE_{service_name}")[0]
                        break

                dst = self.get_name(n)
                edge = pydot.Edge(
                    src=f"{service_name}__{port_host}__{port_container}",
                    dst=f"{dst}:<PLUG_{service_name}__{port_host}__{port_container}>",
                    color=_fillcolor,
                    # fillcolor=_fillcolor,
                    arrowhead="dot",
                    tailhead="dot",
                )

                # edge.set_headport("w")
                edge.set_tailport("e")

                self.graph.add_edge(edge)

        # # Root Ports
        # # Todo
        # for port_mappings in self.port_mappings["root"]:
        #     # port_mapping:
        #     #
        #
        #     _logger.debug(f"Not Implemented yet.")
        #
        #     # for service_name, mappings in port_mapping.items():
        #     #
        #     #     for _mapping in mappings:
        #     #         port_host, port_container = os.path.expandvars(_mapping).split(":", maxsplit=1)
        #     #         # print(service_mapping)
        #     #         node_host = pydot.Node(
        #     #             name=f"{service_name}__{port_host}__{port_container}",
        #     #             label=port_host,
        #     #             shape="circle",
        #     #         )
        #     #
        #     #         self.cluster_root_ports.add_node(node_host)

        # all ports
        #######################

        # #######################
        # # Get all images
        # _images = []
        # for service_name, service_values in services.items():
        #     image = service_values.get("image", None)
        #     if image is not None:
        #         _images.append({
        #             f"image_host": image,
        #             f"image_{service_name}": image
        #         })
        #
        # # _images = list(set(_images))
        #
        # for image in _images:
        #     node = pydot.Node(
        #         name=image["image_host"],
        #         label=image["image_host"],
        #     )
        #
        #     self.cluster_root_images.add_node(node)
        # # all images
        # #######################

        #######################
        # Get all Volumes

        # Service Volumes
        # Todo
        #  - [ ] Sorted

        _color = "black"
        _fillcolor = "green"

        for volume_mapping in self.volume_mappings["services"]:
            # volume_mapping:
            # [{'mongodb-10-2': ['${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/DeadlineDatabase10/mongo/data_LOCAL:/opt/Thinkbox/DeadlineDatabase10/mongo/data', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT}:ro', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT_LNS}:ro']}, {'mongo-express-10-2': ['${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/DeadlineDatabase10/mongo/data_LOCAL:/opt/Thinkbox/DeadlineDatabase10/mongo/data', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT}:ro', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT_LNS}:ro']}, {'filebrowser': ['./databases/filebrowser/filebrowser.db:/filebrowser.db', './configs/filebrowser/filebrowser.json:/.filebrowser.json', '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/DeadlineDatabase10/mongo/data_LOCAL:/opt/Thinkbox/DeadlineDatabase10/mongo/data:ro', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT}:ro', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT_LNS}:ro']}, {'dagster_dev': ['./configs/dagster_shared/workspace.yaml:/dagster/workspace.yaml:ro', './configs/dagster_shared/dagster.yaml:/dagster/materializations/workspace.yaml:ro', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT}', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT_LNS}']}, {'deadline-repository-installer-10-2': ['${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/DeadlineRepository10:/opt/Thinkbox/DeadlineRepository10', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT}:ro', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT_LNS}:ro']}, {'deadline-client-installer-10-2': ['${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/Deadline10:/opt/Thinkbox/Deadline10', '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/DeadlineRepository10:/opt/Thinkbox/DeadlineRepository10', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT}:ro', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT_LNS}:ro']}, {'deadline-rcs-runner-10-2': ['./configs/Deadline10/deadline.ini:/var/lib/Thinkbox/Deadline10/deadline.ini:ro', '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/Deadline10:/opt/Thinkbox/Deadline10', '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/DeadlineRepository10:/opt/Thinkbox/DeadlineRepository10', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT}:ro', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT_LNS}:ro']}, {'deadline-pulse-runner-10-2': ['./configs/Deadline10/deadline.ini:/var/lib/Thinkbox/Deadline10/deadline.ini:ro', '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/Deadline10:/opt/Thinkbox/Deadline10', '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/DeadlineRepository10:/opt/Thinkbox/DeadlineRepository10', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT}:ro', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT_LNS}:ro']}, {'deadline-worker-runner-10-2': ['./configs/Deadline10/deadline.ini:/var/lib/Thinkbox/Deadline10/deadline.ini:ro', '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/Deadline10:/opt/Thinkbox/Deadline10', '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/DeadlineRepository10:/opt/Thinkbox/DeadlineRepository10', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT}:ro', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT_LNS}:ro']}, {'deadline-webservice-runner-10-2': ['./configs/Deadline10/deadline.ini:/var/lib/Thinkbox/Deadline10/deadline.ini:ro', '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/Deadline10:/opt/Thinkbox/Deadline10', '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/DeadlineRepository10:/opt/Thinkbox/DeadlineRepository10', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT}:ro', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT_LNS}:ro']}]

            for service_name, mappings in sorted(volume_mapping.items()):

                for _mapping in sorted(mappings):
                    split = os.path.expandvars(_mapping).split(":")

                    volume_host = split[0]
                    volume_container = split[1]
                    volume_mode = "rw"

                    if len(split) > 2:
                        volume_mode = split[2]

                    node_host = pydot.Node(
                        name=f"{volume_host}__{volume_container}",
                        label=f"{volume_host}",
                        shape="box",
                        style="filled,rounded",
                        color=_color,
                        fillcolor=_fillcolor,
                    )

                    self.cluster_root_volumes.add_node(node_host)

                    for sg in self.cluster_root_services.get_subgraphs():
                        if self.get_name(sg) == f"cluster_cluster_service_{service_name}":
                            n = sg.get_node(name=f"NODE-SERVICE_{service_name}")[0]
                            break

                    dst = self.get_name(n)
                    edge = pydot.Edge(
                        src=node_host,
                        dst=f"{dst}:<PLUG_{service_name}__{volume_container}>",
                        color=_fillcolor,
                        # fillcolor=_fillcolor,
                        arrowhead="dot",
                        # tailhead="dot",
                    )

                    # edge.set_headport("w")
                    edge.set_tailport("e")

                    self.graph.add_edge(edge)

        # Root Volumes
        # Todo
        #  - [ ] Sorted
        # Todo
        for volume_mapping in self.volume_mappings["root"]:
            # volume_mapping:
            #

            _logger.debug(f"Not Implemented yet.")

            # for service_name, mappings in volume_mapping.items():
            #
            #     for _mapping in mappings:
            #         split = os.path.expandvars(_mapping).split(":")
            #
            #         volume_host = split[0]
            #         volume_container = split[1]
            #         volume_mode = "rw"
            #
            #         if len(split) > 2:
            #             volume_mode = split[2]
            #
            #         node_host = pydot.Node(
            #             name=f"{service_name}__{volume_host}__{volume_container}",
            #             label=f"{volume_host} ({volume_mode})",
            #             shape="box",
            #             style="rounded",
            #         )
            #
            #         self.cluster_root_volumes.add_node(node_host)

        # all volumes
        #######################

        #######################
        # Get all Networks

        # Service Networks
        # Todo
        #  - [ ] Sorted

        _color = "black"
        _fillcolor = "orange"

        for network_mapping in self.network_mappings["services"]:
            # network_mapping:
            # [{'mongodb-10-2': ['${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/DeadlineDatabase10/mongo/data_LOCAL:/opt/Thinkbox/DeadlineDatabase10/mongo/data', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT}:ro', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT_LNS}:ro']}, {'mongo-express-10-2': ['${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/DeadlineDatabase10/mongo/data_LOCAL:/opt/Thinkbox/DeadlineDatabase10/mongo/data', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT}:ro', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT_LNS}:ro']}, {'filebrowser': ['./databases/filebrowser/filebrowser.db:/filebrowser.db', './configs/filebrowser/filebrowser.json:/.filebrowser.json', '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/DeadlineDatabase10/mongo/data_LOCAL:/opt/Thinkbox/DeadlineDatabase10/mongo/data:ro', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT}:ro', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT_LNS}:ro']}, {'dagster_dev': ['./configs/dagster_shared/workspace.yaml:/dagster/workspace.yaml:ro', './configs/dagster_shared/dagster.yaml:/dagster/materializations/workspace.yaml:ro', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT}', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT_LNS}']}, {'deadline-repository-installer-10-2': ['${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/DeadlineRepository10:/opt/Thinkbox/DeadlineRepository10', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT}:ro', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT_LNS}:ro']}, {'deadline-client-installer-10-2': ['${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/Deadline10:/opt/Thinkbox/Deadline10', '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/DeadlineRepository10:/opt/Thinkbox/DeadlineRepository10', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT}:ro', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT_LNS}:ro']}, {'deadline-rcs-runner-10-2': ['./configs/Deadline10/deadline.ini:/var/lib/Thinkbox/Deadline10/deadline.ini:ro', '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/Deadline10:/opt/Thinkbox/Deadline10', '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/DeadlineRepository10:/opt/Thinkbox/DeadlineRepository10', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT}:ro', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT_LNS}:ro']}, {'deadline-pulse-runner-10-2': ['./configs/Deadline10/deadline.ini:/var/lib/Thinkbox/Deadline10/deadline.ini:ro', '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/Deadline10:/opt/Thinkbox/Deadline10', '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/DeadlineRepository10:/opt/Thinkbox/DeadlineRepository10', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT}:ro', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT_LNS}:ro']}, {'deadline-worker-runner-10-2': ['./configs/Deadline10/deadline.ini:/var/lib/Thinkbox/Deadline10/deadline.ini:ro', '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/Deadline10:/opt/Thinkbox/Deadline10', '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/DeadlineRepository10:/opt/Thinkbox/DeadlineRepository10', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT}:ro', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT_LNS}:ro']}, {'deadline-webservice-runner-10-2': ['./configs/Deadline10/deadline.ini:/var/lib/Thinkbox/Deadline10/deadline.ini:ro', '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/Deadline10:/opt/Thinkbox/Deadline10', '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/DeadlineRepository10:/opt/Thinkbox/DeadlineRepository10', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT}:ro', '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT_LNS}:ro']}]

            for service_name, mappings in sorted(network_mapping.items()):

                for _mapping in sorted(mappings):
                    # print(_mapping)
                    # split = os.path.expandvars(_mapping).split(":")
                    #
                    # network_host = split[0]
                    # network_container = split[1]
                    # network_mode = "rw"

                    # if len(split) > 2:
                    #     volume_mode = split[2]

                    node_host = pydot.Node(
                        name=f"{_mapping}",
                        label=f"{_mapping}",
                        shape="box",
                        style="filled,rounded",
                        color=_color,
                        fillcolor=_fillcolor,
                    )

                    self.cluster_root_networks.add_node(node_host)

                    for sg in self.cluster_root_services.get_subgraphs():
                        if self.get_name(sg) == f"cluster_cluster_service_{service_name}":
                            n = sg.get_node(name=f"NODE-SERVICE_{service_name}")[0]
                            break

                    dst = self.get_name(n)
                    edge = pydot.Edge(
                        src=f"{_mapping}",
                        dst=f"{dst}:<PLUG_{_mapping}>",
                        color=_fillcolor,
                        # fillcolor=_fillcolor,
                        arrowhead="dot",
                        tailhead="dot",
                    )

                    # edge.set_headport("w")
                    edge.set_tailport("e")

                    self.graph.add_edge(edge)

        # Root Networks
        # Todo
        for network_mapping in self.network_mappings["root"]:
            # network_mapping:
            #

            _logger.debug(f"Not Implemented yet.")

            # for service_name, mappings in network_mapping.items():
            #
            #     for _mapping in mappings:
            #         split = os.path.expandvars(_mapping).split(":")
            #
            #         network_host = split[0]
            #         network_container = split[1]
            #         # network_mode = "rw"
            #
            #         # if len(split) > 2:
            #         #     network_mode = split[2]
            #
            #         node_host = pydot.Node(
            #             name=f"{service_name}__{network_host}__{network_container}",
            #             label=f"{network_host}",
            #             shape="box",
            #             style="rounded",
            #         )
            #
            #         self.cluster_root_networks.add_node(node_host)

        # all networks
        #######################




        #     cluster_volumes.add_node(node)
        # service volumes
        #############################

        # #######################
        # # Get all service networks
        # _networks = []
        # for service_name, service_values in services.items():
        #     _networks.extend(service_values.get("networks", []))
        #
        # _networks = list(set(_networks))
        #
        # for network in _networks:
        #     node = pydot.Node(
        #         name=network,
        #         label=network,
        #     )
        #
        #     self.cluster_service_networks.add_node(node)
        # # service networks
        # ##############################

        # # Individual Services
        # for service_name, service_values in services.items():
        #     cluster_service = pydot.Cluster(
        #         graph_name=service_name,
        #         label=service_name,
        #         # simplify=True,
        #         rankdir="TB",
        #         color="cyan",
        #     )
        #
        #     if service_values.get("hostname", None) is not None:
        #         node_hostname = pydot.Node(
        #             f"{service_name}_{service_values.get('hostname', None)}",
        #         )
        #         cluster_service.add_node(node_hostname)
        #
        #     service_volumes = service_values.get("volumes", None)
        #     if service_volumes is not None:
        #         service_volumes_cluster = pydot.Cluster(
        #             label="Volumes",
        #             rankdir="LR",
        #         )
        #         for service_volume in service_volumes:
        #             volumes_service_host, volumes_service_container = os.path.expandvars(service_volume).split(":", maxsplit=1)
        #             node_service_volume = pydot.Node(
        #                 name=f"{service_name}_{volumes_service_container}",
        #                 label=volumes_service_container,
        #                 shape="box",
        #                 style="rounded"
        #             )
        #             service_volumes_cluster.add_node(node_service_volume)
        #
        #             node_service_volume_host = pydot.Node(
        #                 name=f"{volumes_service_host}",
        #                 label=volumes_service_host,
        #                 shape="box",
        #                 style="rounded",
        #                 color="white",
        #             )
        #             self.cluster_service_volumes.add_node(node_service_volume_host)
        #
        #             edge = pydot.Edge(
        #                 src=node_service_volume_host,
        #                 dst=node_service_volume,
        #             )
        #
        #             self.graph.add_edge(edge)
        #
        #         cluster_service.add_subgraph(service_volumes_cluster)
        #
        #     image = service_values.get("image", None)
        #     if image is not None:
        #         node = pydot.Node(
        #             name=f"{service_name}_{image}",
        #             label=image,
        #         )
        #         cluster_service.add_node(node)
        #
        #         edge = pydot.Edge(
        #             src=image,
        #             dst=f"{service_name}_{image}",
        #         )
        #         self.graph.add_edge(edge)
        #
        #     # Service ports
        #     # for port_mapping in _ports:
        #     #
        #     #     p = port_mapping.get(f"{service_name}_port_container", None)
        #     #
        #     #     if p is not None:
        #     #         node_host = pydot.Node(
        #     #             name=port_mapping.get(f"{service_name}_port_container"),
        #     #             label=port_mapping.get(f"{service_name}_port_container"),
        #     #             shape="circle",
        #     #         )
        #     #
        #     #         edge = pydot.Edge(
        #     #             src=port_mapping.get(f"port_host"),
        #     #             dst=node_host,
        #     #         )
        #     #
        #     #         self.graph.add_edge(edge)
        #     #
        #     #         cluster_service.add_node(node_host)
        #
        #     ##############
        #
        #     self.cluster_root_services.add_subgraph(cluster_service)

        return self.graph


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
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m docker_graph.skeleton 42
    #
    setup_logging(logging.DEBUG)
    run()

else:
    setup_logging(logging.DEBUG)
