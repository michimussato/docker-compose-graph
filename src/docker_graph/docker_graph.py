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
import copy
import os
import shlex
import argparse
import logging
import pathlib
import sys
import yaml as pyyaml
import pydot
import dotenv
from collections import OrderedDict
from jinja2 import Environment, FileSystemLoader

from docker_graph.yaml_tags.overrides import OverrideArray
from docker_graph.utils import *

from docker_graph import __version__

__author__ = "Michael Mussato"
__copyright__ = "Michael Mussato"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


USE_HTML_LABELS = True


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from docker_graph.skeleton import fib`,
# when using this Python module as a library.


class DockerComposeGraph:

    global_dot_settings = {
        "fontname": "Helvetica",
        "style": "rounded",
    }

    def __init__(
            self,
            expandvars: bool = True,  # False is buggy
            resolve_relative_volumes: bool = False,
    ):

        self.expanded_vars = expandvars
        self.resolve_relative_volumes = resolve_relative_volumes

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
            splines="line",
            # splines=False,
            pad="1.5", nodesep="0.3", ranksep="10",
            **self.global_dot_settings,
        )

        # Clusters

        self.alpha = "10"

        ## Root Clusters

        # Todo:
        #  - [ ] useful?
        # self.fillcolor_cluster_root_include = "#0000FF"
        #
        # self.cluster_root_include = pydot.Cluster(
        #     graph_name="cluster_root_include",
        #     label="root_include",
        #     rankdir="TB",
        #     **{
        #         **self.global_dot_settings,
        #         "style": "filled,rounded",
        #         "color": self.fillcolor_cluster_root_include,
        #         "fillcolor": f"{self.fillcolor_cluster_root_include}{alpha}",
        #     },
        # )

        self.fillcolor_cluster_root_services = "#FF00FF"

        self.cluster_root_services = pydot.Cluster(
            graph_name="cluster_root_services",
            label="Services",
            fontsize="40",
            rankdir="TB",
            **{
                **self.global_dot_settings,
                "style": "filled,rounded",
                "color": self.fillcolor_cluster_root_services,
                "fontcolor": self.fillcolor_cluster_root_services,
                "fillcolor": f"{self.fillcolor_cluster_root_services}{self.alpha}",
            },
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

        #### host

        self.fillcolor_cluster_host = "#FFFF00"

        self.cluster_host = pydot.Cluster(
            graph_name="cluster_host",
            label="Host",
            fontsize="40",
            rankdir="TB",
            **{
                **self.global_dot_settings,
                "style": "filled,rounded",
                "color": self.fillcolor_cluster_host,
                "fontcolor": self.fillcolor_cluster_host,
                "fillcolor": f"{self.fillcolor_cluster_host}{self.alpha}",
            },
        )

        #### ports

        self.fillcolor_cluster_root_ports = "#FFFFFF"

        self.cluster_root_ports = pydot.Cluster(
            graph_name="cluster_root_ports",
            label="Exposed Ports",
            fontsize="40",
            rankdir="TB",
            **{
                **self.global_dot_settings,
                "style": "filled,rounded",
                "color": self.fillcolor_cluster_root_ports,
                "fontcolor": self.fillcolor_cluster_root_ports,
                "fillcolor": f"{self.fillcolor_cluster_root_ports}{self.alpha}",
            },
        )

        #### volumes

        self.fillcolor_cluster_root_volumes = "#00FFFF"

        self.cluster_root_volumes = pydot.Cluster(
            graph_name="cluster_root_volumes",
            label="Mounted Volumes",
            fontsize="40",
            rankdir="TB",
            **{
                **self.global_dot_settings,
                "style": "filled,rounded",
                "color": self.fillcolor_cluster_root_volumes,
                "fontcolor": self.fillcolor_cluster_root_volumes,
                "fillcolor": f"{self.fillcolor_cluster_root_volumes}{self.alpha}",
            },
        )

        #### networks

        self.fillcolor_cluster_root_networks = "#FFA500"

        self.cluster_root_networks = pydot.Cluster(
            graph_name="cluster_root_networks",
            label="Networks",
            fontsize="40",
            rankdir="TB",
            **{
                **self.global_dot_settings,
                "style": "filled,rounded",
                "color": self.fillcolor_cluster_root_networks,
                "fontcolor": self.fillcolor_cluster_root_networks,
                "fillcolor": f"{self.fillcolor_cluster_root_networks}{self.alpha}",
            },
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
        """Recursive"""

        if self.docker_yaml is None:
            # The main yaml we process will be
            # the label of the main graph
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
            docker_compose_chainmap: dict = pyyaml.full_load(fr)

        # the first iteration
        # of recursive function
        if ret is None:
            ret = []

        ret.append(docker_compose_chainmap)

        includes: list = docker_compose_chainmap.get("include", [])

        _logger.debug(includes)

        for include in includes:
            if isinstance(include, dict):

                include_set = include

                for included_docker_compose in include_set.get("path", []):
                    _logger.debug(included_docker_compose)
                    pathlib_path = pathlib.Path(included_docker_compose)
                    _logger.debug(pathlib_path)

                    print(f"{ret = }")

                    self.parse_docker_compose(
                        yaml=pathlib_path,
                        root_path=root_path,
                        ret=ret,
                    )

        return ret

    def load_dotenv(self, env: pathlib.Path):
        dotenv.load_dotenv(env)

    @staticmethod
    def _get_service_names(
            services: list[dict],
    ) -> list[str]:

        keys: list = list()
        for service in services:
            key = service.get("service_name", None)
            if key is None or key in keys:
                continue
            keys.append(key)

        return keys

    def merge_services(
            self,
            services,
    ):
        ret: list[dict] = []

        service_name_keys: list = self._get_service_names(services)

        # find dicts that have the same service_name
        # and merge them into one
        for service_name_key in service_name_keys:
            service_dict_merged: dict = dict()
            for service in services:
                if service_name_key != service["service_name"]:
                    # print(f"{key = }")
                    continue
                service_dict_merged = deep_merge(
                    dict1=service_dict_merged,
                    dict2=service,
                )

            ret.append(copy.deepcopy(service_dict_merged))

        return ret

    def iterate_trees(self, trees):

        services = self._get_services(trees)

        self.services = self.merge_services(services)
        self.depends_on = self._get_depends_on(trees)
        self.port_mappings = self._get_ports(trees)
        self.volume_mappings = self._get_volumes(trees)
        self.network_mappings = self._get_networks(trees)

        primary_graph = self.get_primary_graph()

        # for secondary_tree in trees:
        #     print

    def _get_services(
            self,
            trees: list[dict]
    ):

        services = []

        for tree in trees:
            _logger.debug(tree)

            for service_name, service_config in tree.get("services", {}).items():

                # some environment definitions in docker compose
                # (i.e. for ayon) will be loaded as lists instead
                # of k=v pairs. This "tries" to convert it
                # Todo: maybe improve logic here
                environment = service_config.get("environment", None)
                if environment is not None:
                    if isinstance(environment, list):
                        _environment = dict()
                        for env in sorted(environment):
                            k, v = env.replace(" ", "").split("=", maxsplit=1)
                            _environment[k] = v
                        service_config["environment"] = _environment

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
            service_ports = self._get_service_ports(
                tree=tree,
            )

            port_mappings["services"].update(service_ports)

        _logger.debug(f"All {port_mappings = }")
        print(f"All {port_mappings = }")

        return port_mappings

    def _get_service_ports(
            self,
            tree: dict,
    ) -> dict[str, list[str]]:

        port_mappings = {}

        services: dict = tree.get("services", {})

        for service_name, service_config in services.items():
            ports = service_config.get("ports", [])

            if isinstance(ports, OverrideArray):
                ports: list = ports.array

            if self.expanded_vars:
                port_mappings[service_name] = [os.path.expandvars(p) for p in ports]
            else:
                port_mappings[service_name] = ports

        return port_mappings

    def _get_volumes(
            self,
            trees,
    ) -> dict[str, list[str]]:

        volume_mappings = {
            "root": [],
            "services": {},
        }

        for tree in trees:
            service_volumes = self._get_service_volumes(
                tree=tree,
            )
            volume_mappings["services"].update(service_volumes)

        _logger.debug(f"All {volume_mappings = }")
        print(f"All {volume_mappings = }")

        return volume_mappings

    def _get_service_volumes(
            self,
            tree: dict,
    ) -> dict[str, list[str]]:

        volume_mappings = {}

        services: dict = tree.get("services", {})

        for service_name, service_config in services.items():
            volumes = service_config.get("volumes", [])

            if self.expanded_vars:
                volume_mappings[service_name] = [os.path.expandvars(v) for v in volumes]
            else:
                volume_mappings[service_name] = volumes

        return volume_mappings

    def _get_networks(
            self,
            trees,
    ) -> dict[str, list[str]]:

        network_mappings = {
            "root": [],
            "services": {},
        }

        for tree in trees:
            service_networks = self._get_service_networks(
                tree=tree,
            )
            network_mappings["services"].update(service_networks)

        _logger.debug(f"All {network_mappings = }")
        print(f"All {network_mappings = }")

        return network_mappings

    @staticmethod
    def _get_service_networks(
            tree: dict,
    ) -> dict[str, list[str]]:

        network_mappings = {}

        services: dict = tree.get("services", {})

        for service_name, service_config in services.items():
            networks = service_config.get("networks", [])

            network_mappings[service_name] = networks

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
            service_depends_on = self._get_service_depends_on(
                tree=tree,
            )

            depends_on_mappings["services"].update(service_depends_on)

        _logger.debug(f"All {depends_on_mappings = }")
        print(f"All {depends_on_mappings = }")

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

            depends_on_mappings[service_name] = _depends_on_conform

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

    @staticmethod
    def get_name(item):
        # Todo: check effect
        # pydot seems to sometimes
        # return strings that are
        # wrapped inside quotation
        # marks. No-Go!
        assert isinstance(item, pydot.Common)
        return item.get_name().replace('"', '')

    def _get_service_label(
            self,
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

        ports_container: list = list()
        _ports: list = service_config.get("ports", [])
        if isinstance(_ports, list):
            ports_container: list = [os.path.expandvars(p) for p in _ports]
        elif isinstance(_ports, OverrideArray):
            # OverrideArray() in
            # ~/repos/deadline-docker/src/Deadline/deadline_docker/assets.py
            # Todo: find a better solution
            ports_container: list = sorted([os.path.expandvars(p) for p in _ports.array])

        ports = [
            *ports_container
        ]

        _p = []
        for p in ports_container:
            port_host, port_container = p.split(":", maxsplit=1)
            id_service_port = f"<PLUG_{service_name}__{port_host}__{port_container}> {port_container}"
            _p.append(id_service_port)

        depends_on: dict = OrderedDict(self._conform_depends_on(service_config.get("depends_on", [])))
        assert isinstance(depends_on, dict)

        _d = []
        for d in depends_on:
            id_service_depends_on = f"<PLUG_DEPENDS_ON_NODE-SERVICE_{d}> {d}"
            _d.append(id_service_depends_on)

        volumes: list = []
        for v in service_config.get("volumes", []):
            v_dict: dict = {}
            v_split: list = v.split(":")
            if self.expanded_vars:
                v_dict["volume"] = os.path.expandvars(v_split[1])
            else:
                v_dict["volume"] = str(v_split[1])
            if len(v_split) > 2:
                v_dict["mode"] = v_split[2]
            else:
                v_dict["mode"] = "rw"
            volumes.append(copy.deepcopy(v_dict))

        _v = []
        for v in volumes:
            id_service_volume = f"<PLUG_{service_name}__{v['volume']}> {v['volume']}"
            _v.append(id_service_volume)

        networks: list = [os.path.expandvars(n) for n in service_config.get("networks", [])]
        networks.sort()

        _n = []
        for n in networks:
            id_service_network = f"<PLUG_{n}> {n}"
            _n.append(id_service_network)

        _command = service_config.get("command", "-")

        healthcheck_cmd = None
        _healthcheck = service_config.get("healthcheck", {})
        if bool(_healthcheck):
            _healthcheck_cmd = _healthcheck.get("test", [])
            if bool(_healthcheck_cmd):
                healthcheck_cmd = " ".join(shlex.quote(s) for s in _healthcheck_cmd)

        print(service_config)

        if isinstance(_command, list):
            command = " ".join(_command)
        elif isinstance(_command, str):
            command = _command
        else:
            raise TypeError(f"Unhandled command type: {_command} ({type(_command)})")

        if USE_HTML_LABELS:

            env = Environment(loader=FileSystemLoader("/home/michael/git/repos/docker-graph/src/docker_graph/resources"))
            template = env.get_template("service_node_label.j2")

            ret = template.render(
                service_name=service_name,
                container_name=os.path.expandvars(service_config.get("container_name", "-")),
                hostname=os.path.expandvars(service_config.get("hostname", "-")),
                domainname=os.path.expandvars(service_config.get("domainname", "-")),
                restart=service_config.get("restart", "-"),
                image=os.path.expandvars(service_config.get("image", "(build)")),
                command=command,
                # Todo:
                healthcheck=healthcheck_cmd,
                environment=service_config.get("environment", {}),
                volumes=volumes,
                depends_on=depends_on,
                ports=ports,
                networks=networks,
            )

            return f"<{ret}>"

        else:

            fields = OrderedDict({
                "service_name": "{service_name|{" + service_name + "}}",
                "container_name": "{container_name|{" + os.path.expandvars(service_config.get("container_name", "-")) + "}}",
                "hostname": "{hostname|{" + os.path.expandvars(service_config.get("hostname", "-")) + "}}",
                "domainname": "{domainname|{" + os.path.expandvars(service_config.get("domainname", "-")) + "}}",
                "volumes": "{{" + "|".join([v for v in sorted(_v)]) + "}|volumes}",
                "restart": "{restart|{" + service_config.get("restart", "-") + "}}",
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
        self.cluster_host.add_subgraph(self.cluster_root_ports)
        self.cluster_host.add_subgraph(self.cluster_root_volumes)
        self.cluster_host.add_subgraph(self.cluster_root_networks)
        self.graph.add_subgraph(self.cluster_host)
        # self.graph.add_subgraph(self.cluster_root_images)

        #######################
        # Get all Services and add them as clusters
        for service in self.services:
            cluster_service = pydot.Cluster(
                graph_name=f"cluster_service_{service.get('service_name')}",
                label=service.get('service_name'),
                rankdir="TB",
                shape="square",
                **{
                    **self.global_dot_settings,
                    "style": "filled,rounded",
                    "color": "white",
                    "fontcolor": "white",
                    "fillcolor": f"{self.fillcolor_cluster_root_volumes}{self.alpha}",
                },
            )

            node_service = pydot.Node(
                name=f"NODE-SERVICE_{service.get('service_name')}",
                label=self._get_service_label(service),
                labeljust="l",
                shape="plain" if USE_HTML_LABELS else "Mrecord",  # for HTML style labels
                **{
                    **self.global_dot_settings,
                    "style": "filled",
                    "color": "#0A0A0A",
                    "fillcolor": "#A0A0A0",
                }
            )

            cluster_service.add_node(node_service)

            self.cluster_root_services.add_subgraph(cluster_service)

            for depends_on in service.get("service_config", {}).get("depends_on", {}):

                src = self.get_name(node_service)

                edge = pydot.Edge(
                    dst=f'"{src}":"PLUG_DEPENDS_ON_NODE-SERVICE_{depends_on}":w',
                    src=f'"NODE-SERVICE_{depends_on}":"PLUG_NODE-SERVICE_{depends_on}":e',
                    arrowhead="dot",
                    arrowtail="dot",
                    dir="both",
                    color="yellow",
                    **{
                        **self.global_dot_settings,
                        "style": "bold",
                    }
                )

                self.cluster_root_services.add_edge(edge)

        # all services
        #######################

        #######################
        # Get all Ports

        _color = "black"
        # _fillcolor = "white"

        for service_name, mappings in sorted(self.port_mappings["services"].items()):

            if isinstance(mappings, OverrideArray):
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
                    fillcolor=self.fillcolor_cluster_root_ports,
                    **{
                        **self.global_dot_settings,
                        "style": "filled",
                    }
                )

                self.cluster_root_ports.add_node(node_host)

                for sg in self.cluster_root_services.get_subgraphs():
                    if self.get_name(sg) == f"cluster_cluster_service_{service_name}":
                        n = sg.get_node(name=f"NODE-SERVICE_{service_name}")[0]
                        break

                dst = self.get_name(n)
                edge = pydot.Edge(
                    src=f'"{service_name}__{port_host}__{port_container}":e',
                    dst=f'"{dst}":"PLUG_{service_name}__{port_host}__{port_container}":w',
                    color=self.fillcolor_cluster_root_ports,
                    dir="both",
                    arrowhead="dot",
                    arrowtail="dot",
                    **self.global_dot_settings,
                )

                self.graph.add_edge(edge)

        # all ports
        #######################

        # #######################
        # #Todo:
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

        _color = "black"
        # _fillcolor = "green"

        for service_name, mappings in sorted(self.volume_mappings.get("services", {}).items()):
            # volume_mappings:
            # {'mongodb-10-2': ['/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineDatabase10/mongo/data_LOCAL:/opt/Thinkbox/DeadlineDatabase10/mongo/data', '/data/share/nfs:/data/share/nfs:ro', '/data/share/nfs:/nfs:ro'], 'mongo-express-10-2': ['/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineDatabase10/mongo/data_LOCAL:/opt/Thinkbox/DeadlineDatabase10/mongo/data', '/data/share/nfs:/data/share/nfs:ro', '/data/share/nfs:/nfs:ro'], 'filebrowser': ['./databases/filebrowser/filebrowser.db:/filebrowser.db', './configs/filebrowser/filebrowser.json:/.filebrowser.json', '/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineDatabase10/mongo/data_LOCAL:/opt/Thinkbox/DeadlineDatabase10/mongo/data:ro', '/data/share/nfs:/data/share/nfs:ro', '/data/share/nfs:/nfs:ro'], 'dagster_dev': ['./configs/dagster_shared/workspace.yaml:/dagster/workspace.yaml:ro', './configs/dagster_shared/dagster.yaml:/dagster/materializations/workspace.yaml:ro', '/data/share/nfs:/data/share/nfs', '/data/share/nfs:/nfs'], 'likec4_dev': [], 'deadline-repository-installer-10-2': ['/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineRepository10:/opt/Thinkbox/DeadlineRepository10', '/data/share/nfs:/data/share/nfs:ro', '/data/share/nfs:/nfs:ro'], 'deadline-client-installer-10-2': ['/data/share/nfs/test_data/10.2/opt/Thinkbox/Deadline10:/opt/Thinkbox/Deadline10', '/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineRepository10:/opt/Thinkbox/DeadlineRepository10', '/data/share/nfs:/data/share/nfs:ro', '/data/share/nfs:/nfs:ro'], 'deadline-rcs-runner-10-2': ['./configs/Deadline10/deadline.ini:/var/lib/Thinkbox/Deadline10/deadline.ini:ro', '/data/share/nfs/test_data/10.2/opt/Thinkbox/Deadline10:/opt/Thinkbox/Deadline10', '/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineRepository10:/opt/Thinkbox/DeadlineRepository10', '/data/share/nfs:/data/share/nfs:ro', '/data/share/nfs:/nfs:ro'], 'deadline-pulse-runner-10-2': ['./configs/Deadline10/deadline.ini:/var/lib/Thinkbox/Deadline10/deadline.ini:ro', '/data/share/nfs/test_data/10.2/opt/Thinkbox/Deadline10:/opt/Thinkbox/Deadline10', '/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineRepository10:/opt/Thinkbox/DeadlineRepository10', '/data/share/nfs:/data/share/nfs:ro', '/data/share/nfs:/nfs:ro'], 'deadline-worker-runner-10-2': ['./configs/Deadline10/deadline.ini:/var/lib/Thinkbox/Deadline10/deadline.ini:ro', '/data/share/nfs/test_data/10.2/opt/Thinkbox/Deadline10:/opt/Thinkbox/Deadline10', '/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineRepository10:/opt/Thinkbox/DeadlineRepository10', '/data/share/nfs:/data/share/nfs:ro', '/data/share/nfs:/nfs:ro'], 'deadline-webservice-runner-10-2': ['./configs/Deadline10/deadline.ini:/var/lib/Thinkbox/Deadline10/deadline.ini:ro', '/data/share/nfs/test_data/10.2/opt/Thinkbox/Deadline10:/opt/Thinkbox/Deadline10', '/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineRepository10:/opt/Thinkbox/DeadlineRepository10', '/data/share/nfs:/data/share/nfs:ro', '/data/share/nfs:/nfs:ro'], 'kitsu-10-2': ['./postgres/postgresql.conf:/etc/postgresql/14/main/postgresql.conf:ro', '/data/share/nfs:/data/share/nfs', '/data/share/nfs:/nfs'], 'postgres': ['/etc/localtime:/etc/localtime:ro', '/data/share/nfs/databases/ayon/postgresql/data:/var/lib/postgresql/data'], 'redis': [], 'server': []}

            for _mapping in sorted(mappings):
                split = os.path.expandvars(_mapping).split(":")

                volume_host = split[0]
                volume_container = split[1]
                volume_mode = "rw"
                edge_style = "solid"

                if len(split) > 2:
                    volume_mode = split[2]
                    edge_style = "dashed"

                if self.resolve_relative_volumes:
                    _volume_host = pathlib.Path(volume_host)
                    if not _volume_host.is_absolute() \
                            and not _volume_host.is_symlink():
                        volume_host = _volume_host.resolve().as_posix()

                node_host = pydot.Node(
                    name=f"{volume_host}",
                    label=f"{volume_host}",
                    shape="box",
                    color=_color,
                    fillcolor=self.fillcolor_cluster_root_volumes,
                    **{
                        **self.global_dot_settings,
                        "style": "filled,rounded",
                    }
                )

                self.cluster_root_volumes.add_node(node_host)

                for sg in self.cluster_root_services.get_subgraphs():
                    if self.get_name(sg) == f"cluster_cluster_service_{service_name}":
                        n = sg.get_node(name=f"NODE-SERVICE_{service_name}")[0]
                        break

                dst = self.get_name(n)
                edge = pydot.Edge(
                    src=node_host,
                    dst=f'"{dst}":"PLUG_{service_name}__{volume_container}":w',
                    color=self.fillcolor_cluster_root_volumes,
                    dir="both",
                    arrowhead="dot",
                    arrowtail="dot",
                    tailport="e",
                    **{
                        **self.global_dot_settings,
                        "style": edge_style,
                    }
                )

                self.graph.add_edge(edge)

        # all volumes
        #######################

        #######################
        # Get all Networks

        _color = "black"
        # _fillcolor = "orange"

        for service_name, mappings in sorted(self.network_mappings.get("services", {}).items()):
            # network_mappings:
            # {'mongodb-10-2': ['mongodb', 'repository'], 'mongo-express-10-2': ['mongodb'], 'filebrowser': ['repository'], 'dagster_dev': ['repository', 'mongodb'], 'likec4_dev': [], 'deadline-repository-installer-10-2': ['mongodb', 'repository'], 'deadline-client-installer-10-2': ['mongodb', 'repository'], 'deadline-rcs-runner-10-2': ['mongodb', 'repository'], 'deadline-pulse-runner-10-2': ['mongodb', 'repository'], 'deadline-worker-runner-10-2': ['mongodb', 'repository'], 'deadline-webservice-runner-10-2': ['mongodb', 'repository'], 'kitsu-10-2': [], 'postgres': ['repository', 'mongodb'], 'redis': ['repository', 'mongodb'], 'server': ['repository', 'mongodb']}

            for _mapping in sorted(mappings):

                node_host = pydot.Node(
                    name=f"{_mapping}",
                    label=f"{_mapping}",
                    shape="box",
                    color=_color,
                    fillcolor=self.fillcolor_cluster_root_networks,
                    **{
                        **self.global_dot_settings,
                        "style": "filled,rounded",
                    }
                )

                self.cluster_root_networks.add_node(node_host)

                for sg in self.cluster_root_services.get_subgraphs():
                    if self.get_name(sg) == f"cluster_cluster_service_{service_name}":
                        n = sg.get_node(name=f"NODE-SERVICE_{service_name}")[0]
                        break

                dst = self.get_name(n)
                edge = pydot.Edge(
                    src=f'"{_mapping}":e',
                    dst=f'"{dst}":"PLUG_{_mapping}":w',
                    color=self.fillcolor_cluster_root_networks,
                    dir="both",
                    arrowhead="dot",
                    arrowtail="dot",
                    **self.global_dot_settings,
                )

                self.graph.add_edge(edge)

        # networks
        ##############################

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
    setup_logging(logging.DEBUG)
    run()

else:
    setup_logging(logging.DEBUG)
