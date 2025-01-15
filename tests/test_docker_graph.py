import pytest
import json
import pathlib

from docker_graph.docker_graph import main, DockerComposeGraph

__author__ = "Michael Mussato"
__copyright__ = "Michael Mussato"
__license__ = "MIT"


# def test_get_root_ports():
#     # Todo
#     raise NotImplementedError


def test_get_service_ports():
    dcg = DockerComposeGraph()
    trees = dcg.parse_docker_compose(
        pathlib.Path("/home/michael/git/repos/docker-graph/tests/fixtures/deadline-docker/10.2/docker-compose.yaml")
    )

    # resolve environment variables (optional)
    # dcg.load_dotenv(pathlib.Path("/home/michael/git/repos/docker-graph/tests/fixtures/deadline-docker/10.2/.env"))

    port_mappings = dcg._get_service_ports(
        tree=trees[0],
    )

    expected = {
        'dagster_dev': ['${DAGSTER_DEV_PORT_HOST}:${DAGSTER_DEV_PORT_CONTAINER}'],
        'deadline-client-installer-10-2': [],
        'deadline-pulse-runner-10-2': [],
        'deadline-rcs-runner-10-2': ['${RCS_HTTP_PORT_HOST}:${RCS_HTTP_PORT_CONTAINER}'],
        'deadline-repository-installer-10-2': [],
        'deadline-webservice-runner-10-2': ['${WEBSERVICE_HTTP_PORT_HOST}:${WEBSERVICE_HTTP_PORT_CONTAINER}'],
        'deadline-worker-runner-10-2': [],
        'filebrowser': ['${FILEBROWSER_PORT_HOST}:${FILEBROWSER_PORT_CONTAINER}'],
        'likec4_dev': ['${LIKEC4_DEV_PORT_HOST}:${LIKEC4_DEV_PORT_CONTAINER}'],
        'mongo-express-10-2': ['${MONGO_EXPRESS_PORT_HOST}:${MONGO_EXPRESS_PORT_CONTAINER}'],
        'mongodb-10-2': ['${MONGO_DB_PORT_HOST}:${MONGO_DB_PORT_CONTAINER}']
    }

    assert port_mappings == expected


def test_get_service_volumes():
    dcg = DockerComposeGraph()
    trees = dcg.parse_docker_compose(
        pathlib.Path("/home/michael/git/repos/docker-graph/tests/fixtures/deadline-docker/10.2/docker-compose.yaml")
    )

    # resolve environment variables (optional)
    # dcg.load_dotenv(pathlib.Path("/home/michael/git/repos/docker-graph/tests/fixtures/deadline-docker/10.2/.env"))

    volume_mappings = dcg._get_service_volumes(
        tree=trees[0],
    )

    expected = {
        'dagster_dev': ['./configs/dagster_shared/workspace.yaml:/dagster/workspace.yaml:ro',
                        './configs/dagster_shared/dagster.yaml:/dagster/materializations/workspace.yaml:ro',
                        '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT}',
                        '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT_LNS}'],
        'deadline-client-installer-10-2': [
            '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/Deadline10:/opt/Thinkbox/Deadline10',
            '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/DeadlineRepository10:/opt/Thinkbox/DeadlineRepository10',
            '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT}:ro',
            '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT_LNS}:ro'],
        'deadline-pulse-runner-10-2': ['./configs/Deadline10/deadline.ini:/var/lib/Thinkbox/Deadline10/deadline.ini:ro',
                                       '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/Deadline10:/opt/Thinkbox'
                                       '/Deadline10',
                                       '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/DeadlineRepository10:/opt'
                                       '/Thinkbox/DeadlineRepository10',
                                       '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT}:ro',
                                       '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT_LNS}:ro'],
        'deadline-rcs-runner-10-2': ['./configs/Deadline10/deadline.ini:/var/lib/Thinkbox/Deadline10/deadline.ini:ro',
                                     '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/Deadline10:/opt/Thinkbox'
                                     '/Deadline10',
                                     '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/DeadlineRepository10:/opt'
                                     '/Thinkbox/DeadlineRepository10',
                                     '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT}:ro',
                                     '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT_LNS}:ro'],
        'deadline-repository-installer-10-2': [
            '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/DeadlineRepository10:/opt/Thinkbox/DeadlineRepository10',
            '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT}:ro',
            '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT_LNS}:ro'],
        'deadline-webservice-runner-10-2': [
            './configs/Deadline10/deadline.ini:/var/lib/Thinkbox/Deadline10/deadline.ini:ro',
            '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/Deadline10:/opt/Thinkbox/Deadline10',
            '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/DeadlineRepository10:/opt/Thinkbox/DeadlineRepository10',
            '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT}:ro',
            '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT_LNS}:ro'],
        'deadline-worker-runner-10-2': [
            './configs/Deadline10/deadline.ini:/var/lib/Thinkbox/Deadline10/deadline.ini:ro',
            '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/Deadline10:/opt/Thinkbox/Deadline10',
            '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/DeadlineRepository10:/opt/Thinkbox/DeadlineRepository10',
            '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT}:ro',
            '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT_LNS}:ro'],
        'filebrowser': ['./databases/filebrowser/filebrowser.db:/filebrowser.db',
                        './configs/filebrowser/filebrowser.json:/.filebrowser.json',
                        '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/DeadlineDatabase10/mongo/data_LOCAL:/opt'
                        '/Thinkbox/DeadlineDatabase10/mongo/data:ro',
                        '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT}:ro',
                        '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT_LNS}:ro'],
        'likec4_dev': [],
        'mongo-express-10-2': [
            '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/DeadlineDatabase10/mongo/data_LOCAL:/opt/Thinkbox'
            '/DeadlineDatabase10/mongo/data',
            '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT}:ro',
            '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT_LNS}:ro'],
        'mongodb-10-2': [
            '${NFS_ENTRY_POINT}/test_data/10.2/opt/Thinkbox/DeadlineDatabase10/mongo/data_LOCAL:/opt/Thinkbox'
            '/DeadlineDatabase10/mongo/data',
            '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT}:ro',
            '${NFS_ENTRY_POINT}:${NFS_ENTRY_POINT_LNS}:ro']
    }

    assert volume_mappings == expected


def test_get_service_networks():
    dcg = DockerComposeGraph()
    trees = dcg.parse_docker_compose(
        pathlib.Path("/home/michael/git/repos/docker-graph/tests/fixtures/deadline-docker/10.2/docker-compose.yaml")
    )

    # resolve environment variables (optional)
    # dcg.load_dotenv(pathlib.Path("/home/michael/git/repos/docker-graph/tests/fixtures/deadline-docker/10.2/.env"))

    network_mappings = dcg._get_service_networks(
        tree=trees[0],
    )

    expected = {
        'dagster_dev': ['repository', 'mongodb'],
        'deadline-client-installer-10-2': ['mongodb', 'repository'],
        'deadline-pulse-runner-10-2': ['mongodb', 'repository'],
        'deadline-rcs-runner-10-2': ['mongodb', 'repository'],
        'deadline-repository-installer-10-2': ['mongodb', 'repository'],
        'deadline-webservice-runner-10-2': ['mongodb', 'repository'],
        'deadline-worker-runner-10-2': ['mongodb', 'repository'],
        'filebrowser': ['repository'],
        'likec4_dev': [],
        'mongo-express-10-2': ['mongodb'],
        'mongodb-10-2': ['mongodb', 'repository']
    }

    assert network_mappings == expected


def test_get_service_depends_on():
    dcg = DockerComposeGraph()
    trees = dcg.parse_docker_compose(
        pathlib.Path("/home/michael/git/repos/docker-graph/tests/fixtures/deadline-docker/10.2/docker-compose.yaml")
    )

    # resolve environment variables (optional)
    # dcg.load_dotenv(pathlib.Path("/home/michael/git/repos/docker-graph/tests/fixtures/deadline-docker/10.2/.env"))

    depends_on = dcg._get_service_depends_on(
        tree=trees[0],
    )

    expected = {
        'mongo-express-10-2': {'mongodb-10-2': {'condition': None}},
        'filebrowser': {'mongodb-10-2': {'condition': None}},
        'deadline-repository-installer-10-2': {'mongodb-10-2': {'condition': None}},
        'deadline-client-installer-10-2': {
            'deadline-repository-installer-10-2': {'condition': 'service_completed_successfully'}
        },
        'deadline-rcs-runner-10-2': {
            'deadline-client-installer-10-2': {'condition': 'service_completed_successfully'}
        },
        'deadline-pulse-runner-10-2': {
            'deadline-client-installer-10-2': {'condition': 'service_completed_successfully'},
            'deadline-rcs-runner-10-2': {'condition': 'service_started'}
        }, 'deadline-worker-runner-10-2': {
            'deadline-client-installer-10-2': {'condition': 'service_completed_successfully'},
            'deadline-rcs-runner-10-2': {'condition': 'service_started'}
        }, 'deadline-webservice-runner-10-2': {
            'deadline-client-installer-10-2': {'condition': 'service_completed_successfully'},
            'deadline-rcs-runner-10-2': {'condition': 'service_started'}
        }
    }

    assert depends_on == expected


def test_iterate_trees():
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
    # dcg.connect()
    dcg.write_png(
        path=pathlib.Path(__file__).parent / "fixtures" / "out" / "main_graph.png",
    )
    dcg.write_dot(
        path=pathlib.Path(__file__).parent / "fixtures" / "out" / "main_graph.dot",
    )
#
#    # @formatter:off
 #    expected = """("('digraph main_graph {\n"
 # "'\n"
 # ' '
 # '\'label="/home/michael/git/repos/docker-graph/tests/fixtures/deadline-docker/10.2/docker-compose.yaml";\n'
 # "'\n"
 # " 'rankdir=LR;\n"
 # "'\n"
 # ' \'bgcolor="#2f2f2f";\n'
 # "'\n"
 # " 'splines=false;\n"
 # "'\n"
 # " 'pad=1.5;\n"
 # "'\n"
 # " 'nodesep=0.3;\n"
 # "'\n"
 # " 'ranksep=10;\n"
 # "'\n"
 # " 'subgraph cluster_cluster_root_services {\n"
 # "'\n"
 # ' \'label="cluster_root_services";\n'
 # "'\n"
 # " 'color=magenta;\n"
 # "'\n"
 # " 'rankdir=TB;\n"
 # "'\n"
 # ' \'subgraph "cluster_cluster_service_mongodb-10-2" {\n'
 # "'\n"
 # ' \'label="cluster_service_mongodb-10-2";\n'
 # "'\n"
 # " 'color=white;\n"
 # "'\n"
 # " 'rankdir=TB;\n"
 # "'\n"
 # " 'shape=square;\n"
 # "'\n"
 # " 'style=rounded;\n"
 # "'\n"
 # ' \'"NODE-SERVICE_mongodb-10-2" \'\n'
 # ' '
 # '\'[label="mongodb-10-2|{container_name|{mongodb-10-2}}|{hostname|{mongodb-10-2}}|{domainname|{farm.evil}}|{{<PLUG_mongodb-10-2__/data/share/nfs> '
 # "'\n"
 # " '/data/share/nfs|<PLUG_mongodb-10-2__/nfs> '\n"
 # " '/nfs|<PLUG_mongodb-10-2__/opt/Thinkbox/DeadlineDatabase10/mongo/data> '\n"
 # ' '
 # "'/opt/Thinkbox/DeadlineDatabase10/mongo/data}|volumes}|{restart|{}}|{{}|depends_on}|{image|{mongodb/mongodb-community-server:4.4-ubuntu2004}}|{{<PLUG_mongodb-10-2__21017__21017> "
 # "'\n"
 # " '21017}|exposed ports}|{{<PLUG_mongodb> mongodb|<PLUG_repository> '\n"
 # " 'repository}|networks}|{command|{--dbpath '\n"
 # " '/opt/Thinkbox/DeadlineDatabase10/mongo/data --bind_ip_all --noauth '\n"
 # " '--storageEngine wiredTiger --tlsMode disabled\n"
 # "'\n"
 # ' \'}}|{environment|{MONGO_PORT=21017}}", shape=record, style=filled];\n'
 # "'\n"
 # " '}\n"
 # "'\n"
 # " '\n"
 # "'\n"
 # ' \'subgraph "cluster_cluster_service_mongo-express-10-2" {\n'
 # "'\n"
 # ' \'label="cluster_service_mongo-express-10-2";\n'
 # "'\n"
 # " 'color=white;\n"
 # "'\n"
 # " 'rankdir=TB;\n"
 # "'\n"
 # " 'shape=square;\n"
 # "'\n"
 # " 'style=rounded;\n"
 # "'\n"
 # ' \'"NODE-SERVICE_mongo-express-10-2" \'\n'
 # ' '
 # '\'[label="mongo-express-10-2|{container_name|{mongo-express-10-2}}|{hostname|{mongo-express-10-2}}|{domainname|{farm.evil}}|{{<PLUG_mongo-express-10-2__/data/share/nfs> '
 # "'\n"
 # " '/data/share/nfs|<PLUG_mongo-express-10-2__/nfs> '\n"
 # ' '
 # "'/nfs|<PLUG_mongo-express-10-2__/opt/Thinkbox/DeadlineDatabase10/mongo/data> "
 # "'\n"
 # ' '
 # "'/opt/Thinkbox/DeadlineDatabase10/mongo/data}|volumes}|{restart|{always}}|{{<PLUG_DEPENDS_ON_NODE-SERVICE_mongodb-10-2> "
 # "'\n"
 # ' '
 # "'mongodb-10-2}|depends_on}|{image|{mongo-express}}|{{<PLUG_mongo-express-10-2__10000__8081> "
 # "'\n"
 # " '8081}|exposed ports}|{{<PLUG_mongodb> '\n"
 # ' '
 # '\'mongodb}|networks}|{command|{-}}|{environment|{ME_CONFIG_BASICAUTH_PASSWORD=web|ME_CONFIG_BASICAUTH_USERNAME=web|ME_CONFIG_MONGODB_SERVER=mongodb-10-2|ME_CONFIG_MONGODB_URL=mongodb://admin:pass@localhost:21017/db?ssl=false|ME_CONFIG_OPTIONS_EDITORTHEME=darcula}}", '
 # "'\n"
 # " 'shape=record, style=filled];\n"
 # "'\n"
 # " '}\n"
 # "'\n"
 # " '\n"
 # "'\n"
 # " 'subgraph cluster_cluster_service_filebrowser {\n"
 # "'\n"
 # ' \'label="cluster_service_filebrowser";\n'
 # "'\n"
 # " 'color=white;\n"
 # "'\n"
 # " 'rankdir=TB;\n"
 # "'\n"
 # " 'shape=square;\n"
 # "'\n"
 # " 'style=rounded;\n"
 # "'\n"
 # ' \'"NODE-SERVICE_filebrowser" \'\n'
 # ' '
 # '\'[label="filebrowser|{container_name|{mongo-filebrowser-10-2}}|{hostname|{mongo-filebrowser-10-2}}|{domainname|{farm.evil}}|{{<PLUG_filebrowser__/.filebrowser.json> '
 # "'\n"
 # " '/.filebrowser.json|<PLUG_filebrowser__/data/share/nfs> '\n"
 # " '/data/share/nfs|<PLUG_filebrowser__/filebrowser.db> '\n"
 # " '/filebrowser.db|<PLUG_filebrowser__/nfs> '\n"
 # " '/nfs|<PLUG_filebrowser__/opt/Thinkbox/DeadlineDatabase10/mongo/data> '\n"
 # ' '
 # "'/opt/Thinkbox/DeadlineDatabase10/mongo/data}|volumes}|{restart|{always}}|{{<PLUG_DEPENDS_ON_NODE-SERVICE_mongodb-10-2> "
 # "'\n"
 # ' '
 # "'mongodb-10-2}|depends_on}|{image|{filebrowser/filebrowser}}|{{<PLUG_filebrowser__80__80> "
 # "'\n"
 # " '80}|exposed ports}|{{<PLUG_repository> '\n"
 # ' \'repository}|networks}|{command|{-}}|{environment|{}}", shape=record, \'\n'
 # " 'style=filled];\n"
 # "'\n"
 # " '}\n"
 # "'\n"
 # " '\n"
 # "'\n"
 # " 'subgraph cluster_cluster_service_dagster_dev {\n"
 # "'\n"
 # ' \'label="cluster_service_dagster_dev";\n'
 # "'\n"
 # " 'color=white;\n"
 # "'\n"
 # " 'rankdir=TB;\n"
 # "'\n"
 # " 'shape=square;\n"
 # "'\n"
 # " 'style=rounded;\n"
 # "'\n"
 # ' \'"NODE-SERVICE_dagster_dev" \'\n'
 # ' '
 # '\'[label="dagster_dev|{container_name|{dagster-dev-10-2}}|{hostname|{dagster-dev-10-2}}|{domainname|{farm.evil}}|{{<PLUG_dagster_dev__/dagster/materializations/workspace.yaml> '
 # "'\n"
 # ' '
 # "'/dagster/materializations/workspace.yaml|<PLUG_dagster_dev__/dagster/workspace.yaml> "
 # "'\n"
 # " '/dagster/workspace.yaml|<PLUG_dagster_dev__/data/share/nfs> '\n"
 # " '/data/share/nfs|<PLUG_dagster_dev__/nfs> '\n"
 # ' '
 # "'/nfs}|volumes}|{restart|{always}}|{{}|depends_on}|{image|{-}}|{{<PLUG_dagster_dev__3000__3000> "
 # "'\n"
 # " '3000}|exposed ports}|{{<PLUG_mongodb> mongodb|<PLUG_repository> '\n"
 # ' \'repository}|networks}|{command|{-}}|{environment|{}}", shape=record, \'\n'
 # " 'style=filled];\n"
 # "'\n"
 # " '}\n"
 # "'\n"
 # " '\n"
 # "'\n"
 # " 'subgraph cluster_cluster_service_likec4_dev {\n"
 # "'\n"
 # ' \'label="cluster_service_likec4_dev";\n'
 # "'\n"
 # " 'color=white;\n"
 # "'\n"
 # " 'rankdir=TB;\n"
 # "'\n"
 # " 'shape=square;\n"
 # "'\n"
 # " 'style=rounded;\n"
 # "'\n"
 # ' \'"NODE-SERVICE_likec4_dev" \'\n'
 # ' '
 # '\'[label="likec4_dev|{container_name|{likec4-dev-10-2}}|{hostname|{likec4-dev-10-2}}|{domainname|{farm.evil}}|{{}|volumes}|{restart|{always}}|{{}|depends_on}|{image|{-}}|{{<PLUG_likec4_dev__4567__4567> '
 # "'\n"
 # ' \'4567}|exposed ports}|{{}|networks}|{command|{-}}|{environment|{}}", \'\n'
 # " 'shape=record, style=filled];\n"
 # "'\n"
 # " '}\n"
 # "'\n"
 # " '\n"
 # "'\n"
 # ' \'subgraph "cluster_cluster_service_deadline-repository-installer-10-2" {\n'
 # "'\n"
 # ' \'label="cluster_service_deadline-repository-installer-10-2";\n'
 # "'\n"
 # " 'color=white;\n"
 # "'\n"
 # " 'rankdir=TB;\n"
 # "'\n"
 # " 'shape=square;\n"
 # "'\n"
 # " 'style=rounded;\n"
 # "'\n"
 # ' \'"NODE-SERVICE_deadline-repository-installer-10-2" \'\n'
 # ' '
 # '\'[label="deadline-repository-installer-10-2|{container_name|{deadline-repository-installer-10-2}}|{hostname|{deadline-repository-installer-10-2}}|{domainname|{farm.evil}}|{{<PLUG_deadline-repository-installer-10-2__/data/share/nfs> '
 # "'\n"
 # " '/data/share/nfs|<PLUG_deadline-repository-installer-10-2__/nfs> '\n"
 # ' '
 # "'/nfs|<PLUG_deadline-repository-installer-10-2__/opt/Thinkbox/DeadlineRepository10> "
 # "'\n"
 # ' '
 # "'/opt/Thinkbox/DeadlineRepository10}|volumes}|{restart|{no}}|{{<PLUG_DEPENDS_ON_NODE-SERVICE_mongodb-10-2> "
 # "'\n"
 # " 'mongodb-10-2}|depends_on}|{image|{-}}|{{}|exposed ports}|{{<PLUG_mongodb> "
 # "'\n"
 # " 'mongodb|<PLUG_repository> '\n"
 # ' '
 # '\'repository}|networks}|{command|{-}}|{environment|{INSTALLERS_ROOT=/data/share/nfs/installers}}", '
 # "'\n"
 # " 'shape=record, style=filled];\n"
 # "'\n"
 # " '}\n"
 # "'\n"
 # " '\n"
 # "'\n"
 # ' \'subgraph "cluster_cluster_service_deadline-client-installer-10-2" {\n'
 # "'\n"
 # ' \'label="cluster_service_deadline-client-installer-10-2";\n'
 # "'\n"
 # " 'color=white;\n"
 # "'\n"
 # " 'rankdir=TB;\n"
 # "'\n"
 # " 'shape=square;\n"
 # "'\n"
 # " 'style=rounded;\n"
 # "'\n"
 # ' \'"NODE-SERVICE_deadline-client-installer-10-2" \'\n'
 # ' '
 # '\'[label="deadline-client-installer-10-2|{container_name|{client-installer-10-2}}|{hostname|{client-installer-10-2}}|{domainname|{farm.evil}}|{{<PLUG_deadline-client-installer-10-2__/data/share/nfs> '
 # "'\n"
 # " '/data/share/nfs|<PLUG_deadline-client-installer-10-2__/nfs> '\n"
 # " '/nfs|<PLUG_deadline-client-installer-10-2__/opt/Thinkbox/Deadline10> '\n"
 # ' '
 # "'/opt/Thinkbox/Deadline10|<PLUG_deadline-client-installer-10-2__/opt/Thinkbox/DeadlineRepository10> "
 # "'\n"
 # ' '
 # "'/opt/Thinkbox/DeadlineRepository10}|volumes}|{restart|{no}}|{{<PLUG_DEPENDS_ON_NODE-SERVICE_deadline-repository-installer-10-2> "
 # "'\n"
 # " 'deadline-repository-installer-10-2}|depends_on}|{image|{-}}|{{}|exposed '\n"
 # " 'ports}|{{<PLUG_mongodb> mongodb|<PLUG_repository> '\n"
 # ' '
 # '\'repository}|networks}|{command|{-}}|{environment|{INSTALLERS_ROOT=/data/share/nfs/installers}}", '
 # "'\n"
 # " 'shape=record, style=filled];\n"
 # "'\n"
 # " '}\n"
 # "'\n"
 # " '\n"
 # "'\n"
 # ' \'subgraph "cluster_cluster_service_deadline-rcs-runner-10-2" {\n'
 # "'\n"
 # ' \'label="cluster_service_deadline-rcs-runner-10-2";\n'
 # "'\n"
 # " 'color=white;\n"
 # "'\n"
 # " 'rankdir=TB;\n"
 # "'\n"
 # " 'shape=square;\n"
 # "'\n"
 # " 'style=rounded;\n"
 # "'\n"
 # ' \'"NODE-SERVICE_deadline-rcs-runner-10-2" \'\n'
 # ' '
 # '\'[label="deadline-rcs-runner-10-2|{container_name|{rcs-runner-10-2}}|{hostname|{rcs-runner-10-2}}|{domainname|{farm.evil}}|{{<PLUG_deadline-rcs-runner-10-2__/data/share/nfs> '
 # "'\n"
 # " '/data/share/nfs|<PLUG_deadline-rcs-runner-10-2__/nfs> '\n"
 # " '/nfs|<PLUG_deadline-rcs-runner-10-2__/opt/Thinkbox/Deadline10> '\n"
 # ' '
 # "'/opt/Thinkbox/Deadline10|<PLUG_deadline-rcs-runner-10-2__/opt/Thinkbox/DeadlineRepository10> "
 # "'\n"
 # ' '
 # "'/opt/Thinkbox/DeadlineRepository10|<PLUG_deadline-rcs-runner-10-2__/var/lib/Thinkbox/Deadline10/deadline.ini> "
 # "'\n"
 # ' '
 # "'/var/lib/Thinkbox/Deadline10/deadline.ini}|volumes}|{restart|{always}}|{{<PLUG_DEPENDS_ON_NODE-SERVICE_deadline-client-installer-10-2> "
 # "'\n"
 # ' '
 # "'deadline-client-installer-10-2}|depends_on}|{image|{-}}|{{<PLUG_deadline-rcs-runner-10-2__8888__8888> "
 # "'\n"
 # " '8888}|exposed ports}|{{<PLUG_mongodb> mongodb|<PLUG_repository> '\n"
 # ' \'repository}|networks}|{command|{-}}|{environment|{}}", shape=record, \'\n'
 # " 'style=filled];\n"
 # "'\n"
 # " '}\n"
 # "'\n"
 # " '\n"
 # "'\n"
 # ' \'subgraph "cluster_cluster_service_deadline-pulse-runner-10-2" {\n'
 # "'\n"
 # ' \'label="cluster_service_deadline-pulse-runner-10-2";\n'
 # "'\n"
 # " 'color=white;\n"
 # "'\n"
 # " 'rankdir=TB;\n"
 # "'\n"
 # " 'shape=square;\n"
 # "'\n"
 # " 'style=rounded;\n"
 # "'\n"
 # ' \'"NODE-SERVICE_deadline-pulse-runner-10-2" \'\n'
 # ' '
 # '\'[label="deadline-pulse-runner-10-2|{container_name|{pulse-runner-10-2}}|{hostname|{pulse-runner-10-2}}|{domainname|{farm.evil}}|{{<PLUG_deadline-pulse-runner-10-2__/data/share/nfs> '
 # "'\n"
 # " '/data/share/nfs|<PLUG_deadline-pulse-runner-10-2__/nfs> '\n"
 # " '/nfs|<PLUG_deadline-pulse-runner-10-2__/opt/Thinkbox/Deadline10> '\n"
 # ' '
 # "'/opt/Thinkbox/Deadline10|<PLUG_deadline-pulse-runner-10-2__/opt/Thinkbox/DeadlineRepository10> "
 # "'\n"
 # ' '
 # "'/opt/Thinkbox/DeadlineRepository10|<PLUG_deadline-pulse-runner-10-2__/var/lib/Thinkbox/Deadline10/deadline.ini> "
 # "'\n"
 # ' '
 # "'/var/lib/Thinkbox/Deadline10/deadline.ini}|volumes}|{restart|{always}}|{{<PLUG_DEPENDS_ON_NODE-SERVICE_deadline-client-installer-10-2> "
 # "'\n"
 # ' '
 # "'deadline-client-installer-10-2|<PLUG_DEPENDS_ON_NODE-SERVICE_deadline-rcs-runner-10-2> "
 # "'\n"
 # " 'deadline-rcs-runner-10-2}|depends_on}|{image|{-}}|{{}|exposed '\n"
 # " 'ports}|{{<PLUG_mongodb> mongodb|<PLUG_repository> '\n"
 # ' \'repository}|networks}|{command|{-}}|{environment|{}}", shape=record, \'\n'
 # " 'style=filled];\n"
 # "'\n"
 # " '}\n"
 # "'\n"
 # " '\n"
 # "'\n"
 # ' \'subgraph "cluster_cluster_service_deadline-worker-runner-10-2" {\n'
 # "'\n"
 # ' \'label="cluster_service_deadline-worker-runner-10-2";\n'
 # "'\n"
 # " 'color=white;\n"
 # "'\n"
 # " 'rankdir=TB;\n"
 # "'\n"
 # " 'shape=square;\n"
 # "'\n"
 # " 'style=rounded;\n"
 # "'\n"
 # ' \'"NODE-SERVICE_deadline-worker-runner-10-2" \'\n'
 # ' '
 # '\'[label="deadline-worker-runner-10-2|{container_name|{worker-runner-10-2}}|{hostname|{worker-runner-10-2}}|{domainname|{farm.evil}}|{{<PLUG_deadline-worker-runner-10-2__/data/share/nfs> '
 # "'\n"
 # " '/data/share/nfs|<PLUG_deadline-worker-runner-10-2__/nfs> '\n"
 # " '/nfs|<PLUG_deadline-worker-runner-10-2__/opt/Thinkbox/Deadline10> '\n"
 # ' '
 # "'/opt/Thinkbox/Deadline10|<PLUG_deadline-worker-runner-10-2__/opt/Thinkbox/DeadlineRepository10> "
 # "'\n"
 # ' '
 # "'/opt/Thinkbox/DeadlineRepository10|<PLUG_deadline-worker-runner-10-2__/var/lib/Thinkbox/Deadline10/deadline.ini> "
 # "'\n"
 # ' '
 # "'/var/lib/Thinkbox/Deadline10/deadline.ini}|volumes}|{restart|{always}}|{{<PLUG_DEPENDS_ON_NODE-SERVICE_deadline-client-installer-10-2> "
 # "'\n"
 # ' '
 # "'deadline-client-installer-10-2|<PLUG_DEPENDS_ON_NODE-SERVICE_deadline-rcs-runner-10-2> "
 # "'\n"
 # " 'deadline-rcs-runner-10-2}|depends_on}|{image|{-}}|{{}|exposed '\n"
 # " 'ports}|{{<PLUG_mongodb> mongodb|<PLUG_repository> '\n"
 # ' \'repository}|networks}|{command|{-}}|{environment|{}}", shape=record, \'\n'
 # " 'style=filled];\n"
 # "'\n"
 # " '}\n"
 # "'\n"
 # " '\n"
 # "'\n"
 # ' \'subgraph "cluster_cluster_service_deadline-webservice-runner-10-2" {\n'
 # "'\n"
 # ' \'label="cluster_service_deadline-webservice-runner-10-2";\n'
 # "'\n"
 # " 'color=white;\n"
 # "'\n"
 # " 'rankdir=TB;\n"
 # "'\n"
 # " 'shape=square;\n"
 # "'\n"
 # " 'style=rounded;\n"
 # "'\n"
 # ' \'"NODE-SERVICE_deadline-webservice-runner-10-2" \'\n'
 # ' '
 # '\'[label="deadline-webservice-runner-10-2|{container_name|{webservice-runner-10-2}}|{hostname|{webservice-runner-10-2}}|{domainname|{farm.evil}}|{{<PLUG_deadline-webservice-runner-10-2__/data/share/nfs> '
 # "'\n"
 # " '/data/share/nfs|<PLUG_deadline-webservice-runner-10-2__/nfs> '\n"
 # " '/nfs|<PLUG_deadline-webservice-runner-10-2__/opt/Thinkbox/Deadline10> '\n"
 # ' '
 # "'/opt/Thinkbox/Deadline10|<PLUG_deadline-webservice-runner-10-2__/opt/Thinkbox/DeadlineRepository10> "
 # "'\n"
 # ' '
 # "'/opt/Thinkbox/DeadlineRepository10|<PLUG_deadline-webservice-runner-10-2__/var/lib/Thinkbox/Deadline10/deadline.ini> "
 # "'\n"
 # ' '
 # "'/var/lib/Thinkbox/Deadline10/deadline.ini}|volumes}|{restart|{always}}|{{<PLUG_DEPENDS_ON_NODE-SERVICE_deadline-client-installer-10-2> "
 # "'\n"
 # ' '
 # "'deadline-client-installer-10-2|<PLUG_DEPENDS_ON_NODE-SERVICE_deadline-rcs-runner-10-2> "
 # "'\n"
 # ' '
 # "'deadline-rcs-runner-10-2}|depends_on}|{image|{-}}|{{<PLUG_deadline-webservice-runner-10-2__8899__8899> "
 # "'\n"
 # " '8899}|exposed ports}|{{<PLUG_mongodb> mongodb|<PLUG_repository> '\n"
 # ' \'repository}|networks}|{command|{-}}|{environment|{}}", shape=record, \'\n'
 # " 'style=filled];\n"
 # "'\n"
 # " '}\n"
 # "'\n"
 # " '\n"
 # "'\n"
 # ' \'subgraph "cluster_cluster_service_kitsu-10-2" {\n'
 # "'\n"
 # ' \'label="cluster_service_kitsu-10-2";\n'
 # "'\n"
 # " 'color=white;\n"
 # "'\n"
 # " 'rankdir=TB;\n"
 # "'\n"
 # " 'shape=square;\n"
 # "'\n"
 # " 'style=rounded;\n"
 # "'\n"
 # ' \'"NODE-SERVICE_kitsu-10-2" \'\n'
 # ' '
 # '\'[label="kitsu-10-2|{container_name|{kitsu-10-2}}|{hostname|{kitsu-10-2}}|{domainname|{farm.evil}}|{{<PLUG_kitsu-10-2__/data/share/nfs> '
 # "'\n"
 # " '/data/share/nfs|<PLUG_kitsu-10-2__/etc/postgresql/14/main/postgresql.conf> "
 # "'\n"
 # " '/etc/postgresql/14/main/postgresql.conf|<PLUG_kitsu-10-2__/nfs> '\n"
 # ' '
 # "'/nfs}|volumes}|{restart|{always}}|{{}|depends_on}|{image|{-}}|{{<PLUG_kitsu-10-2__5432__5432> "
 # "'\n"
 # " '5432|<PLUG_kitsu-10-2__8181__80> 80}|exposed '\n"
 # ' \'ports}|{{}|networks}|{command|{-}}|{environment|{}}", shape=record, \'\n'
 # " 'style=filled];\n"
 # "'\n"
 # " '}\n"
 # "'\n"
 # " '\n"
 # "'\n"
 # " 'subgraph cluster_cluster_service_postgres {\n"
 # "'\n"
 # ' \'label="cluster_service_postgres";\n'
 # "'\n"
 # " 'color=white;\n"
 # "'\n"
 # " 'rankdir=TB;\n"
 # "'\n"
 # " 'shape=square;\n"
 # "'\n"
 # " 'style=rounded;\n"
 # "'\n"
 # ' \'"NODE-SERVICE_postgres" \'\n'
 # ' '
 # '\'[label="postgres|{container_name|{-}}|{hostname|{-}}|{domainname|{-}}|{{<PLUG_postgres__/etc/localtime> '
 # "'\n"
 # " '/etc/localtime|<PLUG_postgres__/var/lib/postgresql/data> '\n"
 # ' '
 # "'/var/lib/postgresql/data}|volumes}|{restart|{unless-stopped}}|{{}|depends_on}|{image|{postgres:15}}|{{}|exposed "
 # "'\n"
 # ' '
 # '\'ports}|{{}|networks}|{command|{-}}|{environment|{POSTGRES_DB=ayon|POSTGRES_PASSWORD=ayon|POSTGRES_USER=ayon}}", '
 # "'\n"
 # " 'shape=record, style=filled];\n"
 # "'\n"
 # " '}\n"
 # "'\n"
 # " '\n"
 # "'\n"
 # " 'subgraph cluster_cluster_service_redis {\n"
 # "'\n"
 # ' \'label="cluster_service_redis";\n'
 # "'\n"
 # " 'color=white;\n"
 # "'\n"
 # " 'rankdir=TB;\n"
 # "'\n"
 # " 'shape=square;\n"
 # "'\n"
 # " 'style=rounded;\n"
 # "'\n"
 # ' \'"NODE-SERVICE_redis" \'\n'
 # ' '
 # '\'[label="redis|{container_name|{-}}|{hostname|{-}}|{domainname|{-}}|{{}|volumes}|{restart|{unless-stopped}}|{{}|depends_on}|{image|{redis:alpine}}|{{}|exposed '
 # "'\n"
 # ' \'ports}|{{}|networks}|{command|{-}}|{environment|{}}", shape=record, \'\n'
 # " 'style=filled];\n"
 # "'\n"
 # " '}\n"
 # "'\n"
 # " '\n"
 # "'\n"
 # " 'subgraph cluster_cluster_service_server {\n"
 # "'\n"
 # ' \'label="cluster_service_server";\n'
 # "'\n"
 # " 'color=white;\n"
 # "'\n"
 # " 'rankdir=TB;\n"
 # "'\n"
 # " 'shape=square;\n"
 # "'\n"
 # " 'style=rounded;\n"
 # "'\n"
 # ' \'"NODE-SERVICE_server" \'\n'
 # ' '
 # '\'[label="server|{container_name|{-}}|{hostname|{-}}|{domainname|{-}}|{{<PLUG_server__/addons> '
 # "'\n"
 # " '/addons|<PLUG_server__/etc/localtime> "
 # "/etc/localtime|<PLUG_server__/storage> '\n"
 # ' '
 # "'/storage}|volumes}|{restart|{unless-stopped}}|{{<PLUG_DEPENDS_ON_NODE-SERVICE_postgres> "
 # "'\n"
 # " 'postgres|<PLUG_DEPENDS_ON_NODE-SERVICE_redis> '\n"
 # " 'redis}|depends_on}|{image|{ynput/ayon:latest}}|{{<PLUG_server__5000__5000> "
 # "'\n"
 # ' \'5000}|exposed ports}|{{}|networks}|{command|{-}}|{environment|{}}", \'\n'
 # " 'shape=record, style=filled];\n"
 # "'\n"
 # " '}\n"
 # "'\n"
 # " '\n"
 # "'\n"
 # " 'subgraph cluster_cluster_service_postgres {\n"
 # "'\n"
 # ' \'label="cluster_service_postgres";\n'
 # "'\n"
 # " 'color=white;\n"
 # "'\n"
 # " 'rankdir=TB;\n"
 # "'\n"
 # " 'shape=square;\n"
 # "'\n"
 # " 'style=rounded;\n"
 # "'\n"
 # ' \'"NODE-SERVICE_postgres" \'\n'
 # ' '
 # '\'[label="postgres|{container_name|{ayon-postgres-10-2}}|{hostname|{ayon-postgres-10-2}}|{domainname|{farm.evil}}|{{<PLUG_postgres__/etc/localtime> '
 # "'\n"
 # " '/etc/localtime|<PLUG_postgres__/var/lib/postgresql/data> '\n"
 # ' '
 # "'/var/lib/postgresql/data}|volumes}|{restart|{}}|{{}|depends_on}|{image|{-}}|{{}|exposed "
 # "'\n"
 # " 'ports}|{{<PLUG_mongodb> mongodb|<PLUG_repository> '\n"
 # ' \'repository}|networks}|{command|{-}}|{environment|{}}", shape=record, \'\n'
 # " 'style=filled];\n"
 # "'\n"
 # " '}\n"
 # "'\n"
 # " '\n"
 # "'\n"
 # " 'subgraph cluster_cluster_service_redis {\n"
 # "'\n"
 # ' \'label="cluster_service_redis";\n'
 # "'\n"
 # " 'color=white;\n"
 # "'\n"
 # " 'rankdir=TB;\n"
 # "'\n"
 # " 'shape=square;\n"
 # "'\n"
 # " 'style=rounded;\n"
 # "'\n"
 # ' \'"NODE-SERVICE_redis" \'\n'
 # ' '
 # '\'[label="redis|{container_name|{ayon-redis-10-2}}|{hostname|{ayon-redis-10-2}}|{domainname|{farm.evil}}|{{}|volumes}|{restart|{}}|{{}|depends_on}|{image|{-}}|{{}|exposed '
 # "'\n"
 # " 'ports}|{{<PLUG_mongodb> mongodb|<PLUG_repository> '\n"
 # ' \'repository}|networks}|{command|{-}}|{environment|{}}", shape=record, \'\n'
 # " 'style=filled];\n"
 # "'\n"
 # " '}\n"
 # "'\n"
 # " '\n"
 # "'\n"
 # " 'subgraph cluster_cluster_service_server {\n"
 # "'\n"
 # ' \'label="cluster_service_server";\n'
 # "'\n"
 # " 'color=white;\n"
 # "'\n"
 # " 'rankdir=TB;\n"
 # "'\n"
 # " 'shape=square;\n"
 # "'\n"
 # " 'style=rounded;\n"
 # "'\n"
 # ' \'"NODE-SERVICE_server" \'\n'
 # ' '
 # '\'[label="server|{container_name|{ayon-server-10-2}}|{hostname|{ayon-server-10-2}}|{domainname|{farm.evil}}|{{}|volumes}|{restart|{}}|{{}|depends_on}|{image|{-}}|{{<PLUG_server__5005__5000> '
 # "'\n"
 # " '5000}|exposed ports}|{{<PLUG_mongodb> mongodb|<PLUG_repository> '\n"
 # ' \'repository}|networks}|{command|{-}}|{environment|{}}", shape=record, \'\n'
 # " 'style=filled];\n"
 # "'\n"
 # " '}\n"
 # "'\n"
 # " '\n"
 # "'\n"
 # " '}\n"
 # "'\n"
 # " '\n"
 # "'\n"
 # " 'subgraph cluster_cluster_root_ports {\n"
 # "'\n"
 # ' \'label="cluster_root_ports";\n'
 # "'\n"
 # " 'color=red;\n"
 # "'\n"
 # " 'dagster_dev__3000__3000 [label=3000, shape=circle];\n"
 # "'\n"
 # ' \'"deadline-rcs-runner-10-2__8888__8888" [label=8888, shape=circle];\n'
 # "'\n"
 # ' \'"deadline-webservice-runner-10-2__8899__8899" [label=8899, '
 # 'shape=circle];\n'
 # "'\n"
 # " 'filebrowser__80__80 [label=80, shape=circle];\n"
 # "'\n"
 # ' \'"kitsu-10-2__8181__80" [label=8181, shape=circle];\n'
 # "'\n"
 # ' \'"kitsu-10-2__5432__5432" [label=5432, shape=circle];\n'
 # "'\n"
 # " 'likec4_dev__4567__4567 [label=4567, shape=circle];\n"
 # "'\n"
 # ' \'"mongo-express-10-2__10000__8081" [label=10000, shape=circle];\n'
 # "'\n"
 # ' \'"mongodb-10-2__21017__21017" [label=21017, shape=circle];\n'
 # "'\n"
 # " 'server__5005__5000 [label=5005, shape=circle];\n"
 # "'\n"
 # " '}\n"
 # "'\n"
 # " '\n"
 # "'\n"
 # " 'subgraph cluster_cluster_root_volumes {\n"
 # "'\n"
 # ' \'label="cluster_root_volumes";\n'
 # "'\n"
 # " 'color=red;\n"
 # "'\n"
 # " 'rankdir=TB;\n"
 # "'\n"
 # ' '
 # '\'"/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineDatabase10/mongo/data_LOCAL__/opt/Thinkbox/DeadlineDatabase10/mongo/data" '
 # "'\n"
 # ' '
 # '\'[label="/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineDatabase10/mongo/data_LOCAL", '
 # "'\n"
 # " 'shape=box, style=rounded];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/nfs" [label="/data/share/nfs", shape=box, \'\n'
 # " 'style=rounded];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/data/share/nfs" [label="/data/share/nfs", shape=box, '
 # "'\n"
 # " 'style=rounded];\n"
 # "'\n"
 # ' '
 # '\'"/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineDatabase10/mongo/data_LOCAL__/opt/Thinkbox/DeadlineDatabase10/mongo/data" '
 # "'\n"
 # ' '
 # '\'[label="/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineDatabase10/mongo/data_LOCAL", '
 # "'\n"
 # " 'shape=box, style=rounded];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/nfs" [label="/data/share/nfs", shape=box, \'\n'
 # " 'style=rounded];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/data/share/nfs" [label="/data/share/nfs", shape=box, '
 # "'\n"
 # " 'style=rounded];\n"
 # "'\n"
 # ' '
 # '\'"/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineDatabase10/mongo/data_LOCAL__/opt/Thinkbox/DeadlineDatabase10/mongo/data" '
 # "'\n"
 # ' '
 # '\'[label="/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineDatabase10/mongo/data_LOCAL", '
 # "'\n"
 # " 'shape=box, style=rounded];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/nfs" [label="/data/share/nfs", shape=box, \'\n'
 # " 'style=rounded];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/data/share/nfs" [label="/data/share/nfs", shape=box, '
 # "'\n"
 # " 'style=rounded];\n"
 # "'\n"
 # ' \'"./configs/filebrowser/filebrowser.json__/.filebrowser.json" \'\n'
 # ' \'[label="./configs/filebrowser/filebrowser.json", shape=box, '
 # 'style=rounded];\n'
 # "'\n"
 # ' \'"./databases/filebrowser/filebrowser.db__/filebrowser.db" \'\n'
 # ' \'[label="./databases/filebrowser/filebrowser.db", shape=box, '
 # 'style=rounded];\n'
 # "'\n"
 # ' \'"/data/share/nfs__/nfs" [label="/data/share/nfs", shape=box, \'\n'
 # " 'style=rounded];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/data/share/nfs" [label="/data/share/nfs", shape=box, '
 # "'\n"
 # " 'style=rounded];\n"
 # "'\n"
 # ' '
 # '\'"./configs/dagster_shared/dagster.yaml__/dagster/materializations/workspace.yaml" '
 # "'\n"
 # ' \'[label="./configs/dagster_shared/dagster.yaml", shape=box, '
 # 'style=rounded];\n'
 # "'\n"
 # ' \'"./configs/dagster_shared/workspace.yaml__/dagster/workspace.yaml" \'\n'
 # ' \'[label="./configs/dagster_shared/workspace.yaml", shape=box, \'\n'
 # " 'style=rounded];\n"
 # "'\n"
 # ' '
 # '\'"/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineRepository10__/opt/Thinkbox/DeadlineRepository10" '
 # "'\n"
 # ' '
 # '\'[label="/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineRepository10", '
 # "'\n"
 # " 'shape=box, style=rounded];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/nfs" [label="/data/share/nfs", shape=box, \'\n'
 # " 'style=rounded];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/data/share/nfs" [label="/data/share/nfs", shape=box, '
 # "'\n"
 # " 'style=rounded];\n"
 # "'\n"
 # ' '
 # '\'"/data/share/nfs/test_data/10.2/opt/Thinkbox/Deadline10__/opt/Thinkbox/Deadline10" '
 # "'\n"
 # ' \'[label="/data/share/nfs/test_data/10.2/opt/Thinkbox/Deadline10", '
 # "shape=box, '\n"
 # " 'style=rounded];\n"
 # "'\n"
 # ' '
 # '\'"/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineRepository10__/opt/Thinkbox/DeadlineRepository10" '
 # "'\n"
 # ' '
 # '\'[label="/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineRepository10", '
 # "'\n"
 # " 'shape=box, style=rounded];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/nfs" [label="/data/share/nfs", shape=box, \'\n'
 # " 'style=rounded];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/data/share/nfs" [label="/data/share/nfs", shape=box, '
 # "'\n"
 # " 'style=rounded];\n"
 # "'\n"
 # ' '
 # '\'"/data/share/nfs/test_data/10.2/opt/Thinkbox/Deadline10__/opt/Thinkbox/Deadline10" '
 # "'\n"
 # ' \'[label="/data/share/nfs/test_data/10.2/opt/Thinkbox/Deadline10", '
 # "shape=box, '\n"
 # " 'style=rounded];\n"
 # "'\n"
 # ' '
 # '\'"/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineRepository10__/opt/Thinkbox/DeadlineRepository10" '
 # "'\n"
 # ' '
 # '\'[label="/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineRepository10", '
 # "'\n"
 # " 'shape=box, style=rounded];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/nfs" [label="/data/share/nfs", shape=box, \'\n'
 # " 'style=rounded];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/data/share/nfs" [label="/data/share/nfs", shape=box, '
 # "'\n"
 # " 'style=rounded];\n"
 # "'\n"
 # ' '
 # '\'"./configs/Deadline10/deadline.ini__/var/lib/Thinkbox/Deadline10/deadline.ini" '
 # "'\n"
 # ' \'[label="./configs/Deadline10/deadline.ini", shape=box, style=rounded];\n'
 # "'\n"
 # ' '
 # '\'"/data/share/nfs/test_data/10.2/opt/Thinkbox/Deadline10__/opt/Thinkbox/Deadline10" '
 # "'\n"
 # ' \'[label="/data/share/nfs/test_data/10.2/opt/Thinkbox/Deadline10", '
 # "shape=box, '\n"
 # " 'style=rounded];\n"
 # "'\n"
 # ' '
 # '\'"/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineRepository10__/opt/Thinkbox/DeadlineRepository10" '
 # "'\n"
 # ' '
 # '\'[label="/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineRepository10", '
 # "'\n"
 # " 'shape=box, style=rounded];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/nfs" [label="/data/share/nfs", shape=box, \'\n'
 # " 'style=rounded];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/data/share/nfs" [label="/data/share/nfs", shape=box, '
 # "'\n"
 # " 'style=rounded];\n"
 # "'\n"
 # ' '
 # '\'"./configs/Deadline10/deadline.ini__/var/lib/Thinkbox/Deadline10/deadline.ini" '
 # "'\n"
 # ' \'[label="./configs/Deadline10/deadline.ini", shape=box, style=rounded];\n'
 # "'\n"
 # ' '
 # '\'"/data/share/nfs/test_data/10.2/opt/Thinkbox/Deadline10__/opt/Thinkbox/Deadline10" '
 # "'\n"
 # ' \'[label="/data/share/nfs/test_data/10.2/opt/Thinkbox/Deadline10", '
 # "shape=box, '\n"
 # " 'style=rounded];\n"
 # "'\n"
 # ' '
 # '\'"/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineRepository10__/opt/Thinkbox/DeadlineRepository10" '
 # "'\n"
 # ' '
 # '\'[label="/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineRepository10", '
 # "'\n"
 # " 'shape=box, style=rounded];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/nfs" [label="/data/share/nfs", shape=box, \'\n'
 # " 'style=rounded];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/data/share/nfs" [label="/data/share/nfs", shape=box, '
 # "'\n"
 # " 'style=rounded];\n"
 # "'\n"
 # ' '
 # '\'"./configs/Deadline10/deadline.ini__/var/lib/Thinkbox/Deadline10/deadline.ini" '
 # "'\n"
 # ' \'[label="./configs/Deadline10/deadline.ini", shape=box, style=rounded];\n'
 # "'\n"
 # ' '
 # '\'"/data/share/nfs/test_data/10.2/opt/Thinkbox/Deadline10__/opt/Thinkbox/Deadline10" '
 # "'\n"
 # ' \'[label="/data/share/nfs/test_data/10.2/opt/Thinkbox/Deadline10", '
 # "shape=box, '\n"
 # " 'style=rounded];\n"
 # "'\n"
 # ' '
 # '\'"/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineRepository10__/opt/Thinkbox/DeadlineRepository10" '
 # "'\n"
 # ' '
 # '\'[label="/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineRepository10", '
 # "'\n"
 # " 'shape=box, style=rounded];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/nfs" [label="/data/share/nfs", shape=box, \'\n'
 # " 'style=rounded];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/data/share/nfs" [label="/data/share/nfs", shape=box, '
 # "'\n"
 # " 'style=rounded];\n"
 # "'\n"
 # ' '
 # '\'"./configs/Deadline10/deadline.ini__/var/lib/Thinkbox/Deadline10/deadline.ini" '
 # "'\n"
 # ' \'[label="./configs/Deadline10/deadline.ini", shape=box, style=rounded];\n'
 # "'\n"
 # ' \'"/data/share/nfs__/nfs" [label="/data/share/nfs", shape=box, \'\n'
 # " 'style=rounded];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/data/share/nfs" [label="/data/share/nfs", shape=box, '
 # "'\n"
 # " 'style=rounded];\n"
 # "'\n"
 # ' \'"./postgres/postgresql.conf__/etc/postgresql/14/main/postgresql.conf" \'\n'
 # ' \'[label="./postgres/postgresql.conf", shape=box, style=rounded];\n'
 # "'\n"
 # ' \'"/etc/localtime__/etc/localtime" [label="/etc/localtime", shape=box, \'\n'
 # " 'style=rounded];\n"
 # "'\n"
 # ' \'"db__/var/lib/postgresql/data" [label=db, shape=box, style=rounded];\n'
 # "'\n"
 # ' \'"./addons__/addons" [label="./addons", shape=box, style=rounded];\n'
 # "'\n"
 # ' \'"./storage__/storage" [label="./storage", shape=box, style=rounded];\n'
 # "'\n"
 # ' \'"/etc/localtime__/etc/localtime" [label="/etc/localtime", shape=box, \'\n'
 # " 'style=rounded];\n"
 # "'\n"
 # ' '
 # '\'"/data/share/nfs/databases/ayon/postgresql/data__/var/lib/postgresql/data" '
 # "'\n"
 # ' \'[label="/data/share/nfs/databases/ayon/postgresql/data", shape=box, \'\n'
 # " 'style=rounded];\n"
 # "'\n"
 # ' \'"/etc/localtime__/etc/localtime" [label="/etc/localtime", shape=box, \'\n'
 # " 'style=rounded];\n"
 # "'\n"
 # " '}\n"
 # "'\n"
 # " '\n"
 # "'\n"
 # " 'subgraph cluster_cluster_root_networks {\n"
 # "'\n"
 # ' \'label="cluster_root_networks";\n'
 # "'\n"
 # " 'color=red;\n"
 # "'\n"
 # " 'rankdir=TB;\n"
 # "'\n"
 # " 'mongodb [label=mongodb, shape=box, style=rounded];\n"
 # "'\n"
 # " 'repository [label=repository, shape=box, style=rounded];\n"
 # "'\n"
 # " 'mongodb [label=mongodb, shape=box, style=rounded];\n"
 # "'\n"
 # " 'repository [label=repository, shape=box, style=rounded];\n"
 # "'\n"
 # " 'mongodb [label=mongodb, shape=box, style=rounded];\n"
 # "'\n"
 # " 'repository [label=repository, shape=box, style=rounded];\n"
 # "'\n"
 # " 'mongodb [label=mongodb, shape=box, style=rounded];\n"
 # "'\n"
 # " 'repository [label=repository, shape=box, style=rounded];\n"
 # "'\n"
 # " 'mongodb [label=mongodb, shape=box, style=rounded];\n"
 # "'\n"
 # " 'repository [label=repository, shape=box, style=rounded];\n"
 # "'\n"
 # " 'mongodb [label=mongodb, shape=box, style=rounded];\n"
 # "'\n"
 # " 'repository [label=repository, shape=box, style=rounded];\n"
 # "'\n"
 # " 'mongodb [label=mongodb, shape=box, style=rounded];\n"
 # "'\n"
 # " 'repository [label=repository, shape=box, style=rounded];\n"
 # "'\n"
 # " 'mongodb [label=mongodb, shape=box, style=rounded];\n"
 # "'\n"
 # " 'repository [label=repository, shape=box, style=rounded];\n"
 # "'\n"
 # " 'mongodb [label=mongodb, shape=box, style=rounded];\n"
 # "'\n"
 # " 'repository [label=repository, shape=box, style=rounded];\n"
 # "'\n"
 # " 'mongodb [label=mongodb, shape=box, style=rounded];\n"
 # "'\n"
 # " 'repository [label=repository, shape=box, style=rounded];\n"
 # "'\n"
 # " 'mongodb [label=mongodb, shape=box, style=rounded];\n"
 # "'\n"
 # " 'repository [label=repository, shape=box, style=rounded];\n"
 # "'\n"
 # " 'mongodb [label=mongodb, shape=box, style=rounded];\n"
 # "'\n"
 # " 'repository [label=repository, shape=box, style=rounded];\n"
 # "'\n"
 # " '}\n"
 # "'\n"
 # " '\n"
 # "'\n"
 # ' \'"NODE-SERVICE_mongodb-10-2" -> \'\n'
 # ' '
 # '\'"NODE-SERVICE_mongo-express-10-2":<PLUG_DEPENDS_ON_NODE-SERVICE_mongodb-10-2> '
 # "'\n"
 # " '[arrowhead=dot, color=yellow, tailport=ne];\n"
 # "'\n"
 # ' \'"NODE-SERVICE_mongodb-10-2" -> \'\n'
 # ' \'"NODE-SERVICE_filebrowser":<PLUG_DEPENDS_ON_NODE-SERVICE_mongodb-10-2> '
 # "'\n"
 # " '[arrowhead=dot, color=yellow, tailport=ne];\n"
 # "'\n"
 # ' \'"NODE-SERVICE_mongodb-10-2" -> \'\n'
 # ' '
 # '\'"NODE-SERVICE_deadline-repository-installer-10-2":<PLUG_DEPENDS_ON_NODE-SERVICE_mongodb-10-2> '
 # "'\n"
 # " '[arrowhead=dot, color=yellow, tailport=ne];\n"
 # "'\n"
 # ' \'"NODE-SERVICE_deadline-repository-installer-10-2" -> \'\n'
 # ' '
 # '\'"NODE-SERVICE_deadline-client-installer-10-2":<PLUG_DEPENDS_ON_NODE-SERVICE_deadline-repository-installer-10-2> '
 # "'\n"
 # " '[arrowhead=dot, color=yellow, tailport=ne];\n"
 # "'\n"
 # ' \'"NODE-SERVICE_deadline-client-installer-10-2" -> \'\n'
 # ' '
 # '\'"NODE-SERVICE_deadline-rcs-runner-10-2":<PLUG_DEPENDS_ON_NODE-SERVICE_deadline-client-installer-10-2> '
 # "'\n"
 # " '[arrowhead=dot, color=yellow, tailport=ne];\n"
 # "'\n"
 # ' \'"NODE-SERVICE_deadline-client-installer-10-2" -> \'\n'
 # ' '
 # '\'"NODE-SERVICE_deadline-pulse-runner-10-2":<PLUG_DEPENDS_ON_NODE-SERVICE_deadline-client-installer-10-2> '
 # "'\n"
 # " '[arrowhead=dot, color=yellow, tailport=ne];\n"
 # "'\n"
 # ' \'"NODE-SERVICE_deadline-rcs-runner-10-2" -> \'\n'
 # ' '
 # '\'"NODE-SERVICE_deadline-pulse-runner-10-2":<PLUG_DEPENDS_ON_NODE-SERVICE_deadline-rcs-runner-10-2> '
 # "'\n"
 # " '[arrowhead=dot, color=yellow, tailport=ne];\n"
 # "'\n"
 # ' \'"NODE-SERVICE_deadline-client-installer-10-2" -> \'\n'
 # ' '
 # '\'"NODE-SERVICE_deadline-worker-runner-10-2":<PLUG_DEPENDS_ON_NODE-SERVICE_deadline-client-installer-10-2> '
 # "'\n"
 # " '[arrowhead=dot, color=yellow, tailport=ne];\n"
 # "'\n"
 # ' \'"NODE-SERVICE_deadline-rcs-runner-10-2" -> \'\n'
 # ' '
 # '\'"NODE-SERVICE_deadline-worker-runner-10-2":<PLUG_DEPENDS_ON_NODE-SERVICE_deadline-rcs-runner-10-2> '
 # "'\n"
 # " '[arrowhead=dot, color=yellow, tailport=ne];\n"
 # "'\n"
 # ' \'"NODE-SERVICE_deadline-client-installer-10-2" -> \'\n'
 # ' '
 # '\'"NODE-SERVICE_deadline-webservice-runner-10-2":<PLUG_DEPENDS_ON_NODE-SERVICE_deadline-client-installer-10-2> '
 # "'\n"
 # " '[arrowhead=dot, color=yellow, tailport=ne];\n"
 # "'\n"
 # ' \'"NODE-SERVICE_deadline-rcs-runner-10-2" -> \'\n'
 # ' '
 # '\'"NODE-SERVICE_deadline-webservice-runner-10-2":<PLUG_DEPENDS_ON_NODE-SERVICE_deadline-rcs-runner-10-2> '
 # "'\n"
 # " '[arrowhead=dot, color=yellow, tailport=ne];\n"
 # "'\n"
 # ' \'"NODE-SERVICE_postgres" -> \'\n'
 # ' \'"NODE-SERVICE_server":<PLUG_DEPENDS_ON_NODE-SERVICE_postgres> \'\n'
 # " '[arrowhead=dot, color=yellow, tailport=ne];\n"
 # "'\n"
 # ' \'"NODE-SERVICE_redis" -> \'\n'
 # ' \'"NODE-SERVICE_server":<PLUG_DEPENDS_ON_NODE-SERVICE_redis> '
 # "[arrowhead=dot, '\n"
 # " 'color=yellow, tailport=ne];\n"
 # "'\n"
 # " 'dagster_dev__3000__3000 -> '\n"
 # ' \'"NODE-SERVICE_dagster_dev":<PLUG_dagster_dev__3000__3000> [color=white, '
 # "'\n"
 # " 'arrowhead=dot, tailhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"deadline-rcs-runner-10-2__8888__8888" -> \'\n'
 # ' '
 # '\'"NODE-SERVICE_deadline-rcs-runner-10-2":<PLUG_deadline-rcs-runner-10-2__8888__8888> '
 # "'\n"
 # " '[color=white, arrowhead=dot, tailhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"deadline-webservice-runner-10-2__8899__8899" -> \'\n'
 # ' '
 # '\'"NODE-SERVICE_deadline-webservice-runner-10-2":<PLUG_deadline-webservice-runner-10-2__8899__8899> '
 # "'\n"
 # " '[color=white, arrowhead=dot, tailhead=dot, tailport=e];\n"
 # "'\n"
 # " 'filebrowser__80__80 -> "
 # '"NODE-SERVICE_filebrowser":<PLUG_filebrowser__80__80> \'\n'
 # " '[color=white, arrowhead=dot, tailhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"kitsu-10-2__8181__80" -> \'\n'
 # ' \'"NODE-SERVICE_kitsu-10-2":<PLUG_kitsu-10-2__8181__80> [color=white, \'\n'
 # " 'arrowhead=dot, tailhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"kitsu-10-2__5432__5432" -> \'\n'
 # ' \'"NODE-SERVICE_kitsu-10-2":<PLUG_kitsu-10-2__5432__5432> [color=white, \'\n'
 # " 'arrowhead=dot, tailhead=dot, tailport=e];\n"
 # "'\n"
 # " 'likec4_dev__4567__4567 -> '\n"
 # ' \'"NODE-SERVICE_likec4_dev":<PLUG_likec4_dev__4567__4567> [color=white, \'\n'
 # " 'arrowhead=dot, tailhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"mongo-express-10-2__10000__8081" -> \'\n'
 # ' \'"NODE-SERVICE_mongo-express-10-2":<PLUG_mongo-express-10-2__10000__8081> '
 # "'\n"
 # " '[color=white, arrowhead=dot, tailhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"mongodb-10-2__21017__21017" -> \'\n'
 # ' \'"NODE-SERVICE_mongodb-10-2":<PLUG_mongodb-10-2__21017__21017> '
 # "[color=white, '\n"
 # " 'arrowhead=dot, tailhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'server__5005__5000 -> "NODE-SERVICE_server":<PLUG_server__5005__5000> \'\n'
 # " '[color=white, arrowhead=dot, tailhead=dot, tailport=e];\n"
 # "'\n"
 # ' '
 # '\'"/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineDatabase10/mongo/data_LOCAL__/opt/Thinkbox/DeadlineDatabase10/mongo/data" '
 # "'\n"
 # " '-> '\n"
 # ' '
 # '\'"NODE-SERVICE_mongodb-10-2":<PLUG_mongodb-10-2__/opt/Thinkbox/DeadlineDatabase10/mongo/data> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/nfs" -> \'\n'
 # ' \'"NODE-SERVICE_mongodb-10-2":<PLUG_mongodb-10-2__/nfs> [color=green, \'\n'
 # " 'arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/data/share/nfs" -> \'\n'
 # ' \'"NODE-SERVICE_mongodb-10-2":<PLUG_mongodb-10-2__/data/share/nfs> \'\n'
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' '
 # '\'"/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineDatabase10/mongo/data_LOCAL__/opt/Thinkbox/DeadlineDatabase10/mongo/data" '
 # "'\n"
 # " '-> '\n"
 # ' '
 # '\'"NODE-SERVICE_mongo-express-10-2":<PLUG_mongo-express-10-2__/opt/Thinkbox/DeadlineDatabase10/mongo/data> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/nfs" -> \'\n'
 # ' \'"NODE-SERVICE_mongo-express-10-2":<PLUG_mongo-express-10-2__/nfs> \'\n'
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/data/share/nfs" -> \'\n'
 # ' '
 # '\'"NODE-SERVICE_mongo-express-10-2":<PLUG_mongo-express-10-2__/data/share/nfs> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' '
 # '\'"/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineDatabase10/mongo/data_LOCAL__/opt/Thinkbox/DeadlineDatabase10/mongo/data" '
 # "'\n"
 # " '-> '\n"
 # ' '
 # '\'"NODE-SERVICE_filebrowser":<PLUG_filebrowser__/opt/Thinkbox/DeadlineDatabase10/mongo/data> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/nfs" -> \'\n'
 # ' \'"NODE-SERVICE_filebrowser":<PLUG_filebrowser__/nfs> [color=green, \'\n'
 # " 'arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/data/share/nfs" -> \'\n'
 # ' \'"NODE-SERVICE_filebrowser":<PLUG_filebrowser__/data/share/nfs> '
 # "[color=green, '\n"
 # " 'arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"./configs/filebrowser/filebrowser.json__/.filebrowser.json" -> \'\n'
 # ' \'"NODE-SERVICE_filebrowser":<PLUG_filebrowser__/.filebrowser.json> \'\n'
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"./databases/filebrowser/filebrowser.db__/filebrowser.db" -> \'\n'
 # ' \'"NODE-SERVICE_filebrowser":<PLUG_filebrowser__/filebrowser.db> '
 # "[color=green, '\n"
 # " 'arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/nfs" -> \'\n'
 # ' \'"NODE-SERVICE_dagster_dev":<PLUG_dagster_dev__/nfs> [color=green, \'\n'
 # " 'arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/data/share/nfs" -> \'\n'
 # ' \'"NODE-SERVICE_dagster_dev":<PLUG_dagster_dev__/data/share/nfs> '
 # "[color=green, '\n"
 # " 'arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' '
 # '\'"./configs/dagster_shared/dagster.yaml__/dagster/materializations/workspace.yaml" '
 # "'\n"
 # " '-> '\n"
 # ' '
 # '\'"NODE-SERVICE_dagster_dev":<PLUG_dagster_dev__/dagster/materializations/workspace.yaml> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"./configs/dagster_shared/workspace.yaml__/dagster/workspace.yaml" -> \'\n'
 # ' \'"NODE-SERVICE_dagster_dev":<PLUG_dagster_dev__/dagster/workspace.yaml> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' '
 # '\'"/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineRepository10__/opt/Thinkbox/DeadlineRepository10" '
 # "'\n"
 # " '-> '\n"
 # ' '
 # '\'"NODE-SERVICE_deadline-repository-installer-10-2":<PLUG_deadline-repository-installer-10-2__/opt/Thinkbox/DeadlineRepository10> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/nfs" -> \'\n'
 # ' '
 # '\'"NODE-SERVICE_deadline-repository-installer-10-2":<PLUG_deadline-repository-installer-10-2__/nfs> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/data/share/nfs" -> \'\n'
 # ' '
 # '\'"NODE-SERVICE_deadline-repository-installer-10-2":<PLUG_deadline-repository-installer-10-2__/data/share/nfs> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' '
 # '\'"/data/share/nfs/test_data/10.2/opt/Thinkbox/Deadline10__/opt/Thinkbox/Deadline10" '
 # "'\n"
 # " '-> '\n"
 # ' '
 # '\'"NODE-SERVICE_deadline-client-installer-10-2":<PLUG_deadline-client-installer-10-2__/opt/Thinkbox/Deadline10> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' '
 # '\'"/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineRepository10__/opt/Thinkbox/DeadlineRepository10" '
 # "'\n"
 # " '-> '\n"
 # ' '
 # '\'"NODE-SERVICE_deadline-client-installer-10-2":<PLUG_deadline-client-installer-10-2__/opt/Thinkbox/DeadlineRepository10> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/nfs" -> \'\n'
 # ' '
 # '\'"NODE-SERVICE_deadline-client-installer-10-2":<PLUG_deadline-client-installer-10-2__/nfs> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/data/share/nfs" -> \'\n'
 # ' '
 # '\'"NODE-SERVICE_deadline-client-installer-10-2":<PLUG_deadline-client-installer-10-2__/data/share/nfs> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' '
 # '\'"/data/share/nfs/test_data/10.2/opt/Thinkbox/Deadline10__/opt/Thinkbox/Deadline10" '
 # "'\n"
 # " '-> '\n"
 # ' '
 # '\'"NODE-SERVICE_deadline-rcs-runner-10-2":<PLUG_deadline-rcs-runner-10-2__/opt/Thinkbox/Deadline10> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' '
 # '\'"/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineRepository10__/opt/Thinkbox/DeadlineRepository10" '
 # "'\n"
 # " '-> '\n"
 # ' '
 # '\'"NODE-SERVICE_deadline-rcs-runner-10-2":<PLUG_deadline-rcs-runner-10-2__/opt/Thinkbox/DeadlineRepository10> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/nfs" -> \'\n'
 # ' '
 # '\'"NODE-SERVICE_deadline-rcs-runner-10-2":<PLUG_deadline-rcs-runner-10-2__/nfs> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/data/share/nfs" -> \'\n'
 # ' '
 # '\'"NODE-SERVICE_deadline-rcs-runner-10-2":<PLUG_deadline-rcs-runner-10-2__/data/share/nfs> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' '
 # '\'"./configs/Deadline10/deadline.ini__/var/lib/Thinkbox/Deadline10/deadline.ini" '
 # "'\n"
 # " '-> '\n"
 # ' '
 # '\'"NODE-SERVICE_deadline-rcs-runner-10-2":<PLUG_deadline-rcs-runner-10-2__/var/lib/Thinkbox/Deadline10/deadline.ini> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' '
 # '\'"/data/share/nfs/test_data/10.2/opt/Thinkbox/Deadline10__/opt/Thinkbox/Deadline10" '
 # "'\n"
 # " '-> '\n"
 # ' '
 # '\'"NODE-SERVICE_deadline-pulse-runner-10-2":<PLUG_deadline-pulse-runner-10-2__/opt/Thinkbox/Deadline10> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' '
 # '\'"/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineRepository10__/opt/Thinkbox/DeadlineRepository10" '
 # "'\n"
 # " '-> '\n"
 # ' '
 # '\'"NODE-SERVICE_deadline-pulse-runner-10-2":<PLUG_deadline-pulse-runner-10-2__/opt/Thinkbox/DeadlineRepository10> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/nfs" -> \'\n'
 # ' '
 # '\'"NODE-SERVICE_deadline-pulse-runner-10-2":<PLUG_deadline-pulse-runner-10-2__/nfs> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/data/share/nfs" -> \'\n'
 # ' '
 # '\'"NODE-SERVICE_deadline-pulse-runner-10-2":<PLUG_deadline-pulse-runner-10-2__/data/share/nfs> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' '
 # '\'"./configs/Deadline10/deadline.ini__/var/lib/Thinkbox/Deadline10/deadline.ini" '
 # "'\n"
 # " '-> '\n"
 # ' '
 # '\'"NODE-SERVICE_deadline-pulse-runner-10-2":<PLUG_deadline-pulse-runner-10-2__/var/lib/Thinkbox/Deadline10/deadline.ini> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' '
 # '\'"/data/share/nfs/test_data/10.2/opt/Thinkbox/Deadline10__/opt/Thinkbox/Deadline10" '
 # "'\n"
 # " '-> '\n"
 # ' '
 # '\'"NODE-SERVICE_deadline-worker-runner-10-2":<PLUG_deadline-worker-runner-10-2__/opt/Thinkbox/Deadline10> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' '
 # '\'"/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineRepository10__/opt/Thinkbox/DeadlineRepository10" '
 # "'\n"
 # " '-> '\n"
 # ' '
 # '\'"NODE-SERVICE_deadline-worker-runner-10-2":<PLUG_deadline-worker-runner-10-2__/opt/Thinkbox/DeadlineRepository10> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/nfs" -> \'\n'
 # ' '
 # '\'"NODE-SERVICE_deadline-worker-runner-10-2":<PLUG_deadline-worker-runner-10-2__/nfs> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/data/share/nfs" -> \'\n'
 # ' '
 # '\'"NODE-SERVICE_deadline-worker-runner-10-2":<PLUG_deadline-worker-runner-10-2__/data/share/nfs> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' '
 # '\'"./configs/Deadline10/deadline.ini__/var/lib/Thinkbox/Deadline10/deadline.ini" '
 # "'\n"
 # " '-> '\n"
 # ' '
 # '\'"NODE-SERVICE_deadline-worker-runner-10-2":<PLUG_deadline-worker-runner-10-2__/var/lib/Thinkbox/Deadline10/deadline.ini> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' '
 # '\'"/data/share/nfs/test_data/10.2/opt/Thinkbox/Deadline10__/opt/Thinkbox/Deadline10" '
 # "'\n"
 # " '-> '\n"
 # ' '
 # '\'"NODE-SERVICE_deadline-webservice-runner-10-2":<PLUG_deadline-webservice-runner-10-2__/opt/Thinkbox/Deadline10> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' '
 # '\'"/data/share/nfs/test_data/10.2/opt/Thinkbox/DeadlineRepository10__/opt/Thinkbox/DeadlineRepository10" '
 # "'\n"
 # " '-> '\n"
 # ' '
 # '\'"NODE-SERVICE_deadline-webservice-runner-10-2":<PLUG_deadline-webservice-runner-10-2__/opt/Thinkbox/DeadlineRepository10> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/nfs" -> \'\n'
 # ' '
 # '\'"NODE-SERVICE_deadline-webservice-runner-10-2":<PLUG_deadline-webservice-runner-10-2__/nfs> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/data/share/nfs" -> \'\n'
 # ' '
 # '\'"NODE-SERVICE_deadline-webservice-runner-10-2":<PLUG_deadline-webservice-runner-10-2__/data/share/nfs> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' '
 # '\'"./configs/Deadline10/deadline.ini__/var/lib/Thinkbox/Deadline10/deadline.ini" '
 # "'\n"
 # " '-> '\n"
 # ' '
 # '\'"NODE-SERVICE_deadline-webservice-runner-10-2":<PLUG_deadline-webservice-runner-10-2__/var/lib/Thinkbox/Deadline10/deadline.ini> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/nfs" -> '
 # '"NODE-SERVICE_kitsu-10-2":<PLUG_kitsu-10-2__/nfs> \'\n'
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"/data/share/nfs__/data/share/nfs" -> \'\n'
 # ' \'"NODE-SERVICE_kitsu-10-2":<PLUG_kitsu-10-2__/data/share/nfs> '
 # "[color=green, '\n"
 # " 'arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"./postgres/postgresql.conf__/etc/postgresql/14/main/postgresql.conf" -> '
 # "'\n"
 # ' '
 # '\'"NODE-SERVICE_kitsu-10-2":<PLUG_kitsu-10-2__/etc/postgresql/14/main/postgresql.conf> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"/etc/localtime__/etc/localtime" -> \'\n'
 # ' \'"NODE-SERVICE_postgres":<PLUG_postgres__/etc/localtime> [color=green, \'\n'
 # " 'arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"db__/var/lib/postgresql/data" -> \'\n'
 # ' \'"NODE-SERVICE_postgres":<PLUG_postgres__/var/lib/postgresql/data> \'\n'
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"./addons__/addons" -> "NODE-SERVICE_server":<PLUG_server__/addons> \'\n'
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"./storage__/storage" -> "NODE-SERVICE_server":<PLUG_server__/storage> '
 # "'\n"
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"/etc/localtime__/etc/localtime" -> \'\n'
 # ' \'"NODE-SERVICE_server":<PLUG_server__/etc/localtime> [color=green, \'\n'
 # " 'arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' '
 # '\'"/data/share/nfs/databases/ayon/postgresql/data__/var/lib/postgresql/data" '
 # "'\n"
 # ' \'-> "NODE-SERVICE_postgres":<PLUG_postgres__/var/lib/postgresql/data> \'\n'
 # " '[color=green, arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'"/etc/localtime__/etc/localtime" -> \'\n'
 # ' \'"NODE-SERVICE_postgres":<PLUG_postgres__/etc/localtime> [color=green, \'\n'
 # " 'arrowhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'mongodb -> "NODE-SERVICE_mongodb-10-2":<PLUG_mongodb> [color=orange, \'\n'
 # " 'arrowhead=dot, tailhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'repository -> "NODE-SERVICE_mongodb-10-2":<PLUG_repository> '
 # "[color=orange, '\n"
 # " 'arrowhead=dot, tailhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'mongodb -> "NODE-SERVICE_mongo-express-10-2":<PLUG_mongodb> '
 # "[color=orange, '\n"
 # " 'arrowhead=dot, tailhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'repository -> "NODE-SERVICE_filebrowser":<PLUG_repository> [color=orange, '
 # "'\n"
 # " 'arrowhead=dot, tailhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'mongodb -> "NODE-SERVICE_dagster_dev":<PLUG_mongodb> [color=orange, \'\n'
 # " 'arrowhead=dot, tailhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'repository -> "NODE-SERVICE_dagster_dev":<PLUG_repository> [color=orange, '
 # "'\n"
 # " 'arrowhead=dot, tailhead=dot, tailport=e];\n"
 # "'\n"
 # " 'mongodb -> "
 # '"NODE-SERVICE_deadline-repository-installer-10-2":<PLUG_mongodb> \'\n'
 # " '[color=orange, arrowhead=dot, tailhead=dot, tailport=e];\n"
 # "'\n"
 # " 'repository -> '\n"
 # ' \'"NODE-SERVICE_deadline-repository-installer-10-2":<PLUG_repository> \'\n'
 # " '[color=orange, arrowhead=dot, tailhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'mongodb -> "NODE-SERVICE_deadline-client-installer-10-2":<PLUG_mongodb> '
 # "'\n"
 # " '[color=orange, arrowhead=dot, tailhead=dot, tailport=e];\n"
 # "'\n"
 # " 'repository -> '\n"
 # ' \'"NODE-SERVICE_deadline-client-installer-10-2":<PLUG_repository> \'\n'
 # " '[color=orange, arrowhead=dot, tailhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'mongodb -> "NODE-SERVICE_deadline-rcs-runner-10-2":<PLUG_mongodb> \'\n'
 # " '[color=orange, arrowhead=dot, tailhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'repository -> "NODE-SERVICE_deadline-rcs-runner-10-2":<PLUG_repository> '
 # "'\n"
 # " '[color=orange, arrowhead=dot, tailhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'mongodb -> "NODE-SERVICE_deadline-pulse-runner-10-2":<PLUG_mongodb> \'\n'
 # " '[color=orange, arrowhead=dot, tailhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'repository -> "NODE-SERVICE_deadline-pulse-runner-10-2":<PLUG_repository> '
 # "'\n"
 # " '[color=orange, arrowhead=dot, tailhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'mongodb -> "NODE-SERVICE_deadline-worker-runner-10-2":<PLUG_mongodb> \'\n'
 # " '[color=orange, arrowhead=dot, tailhead=dot, tailport=e];\n"
 # "'\n"
 # " 'repository -> "
 # '"NODE-SERVICE_deadline-worker-runner-10-2":<PLUG_repository> \'\n'
 # " '[color=orange, arrowhead=dot, tailhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'mongodb -> "NODE-SERVICE_deadline-webservice-runner-10-2":<PLUG_mongodb> '
 # "'\n"
 # " '[color=orange, arrowhead=dot, tailhead=dot, tailport=e];\n"
 # "'\n"
 # " 'repository -> '\n"
 # ' \'"NODE-SERVICE_deadline-webservice-runner-10-2":<PLUG_repository> \'\n'
 # " '[color=orange, arrowhead=dot, tailhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'mongodb -> "NODE-SERVICE_postgres":<PLUG_mongodb> [color=orange, \'\n'
 # " 'arrowhead=dot, tailhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'repository -> "NODE-SERVICE_postgres":<PLUG_repository> [color=orange, '
 # "'\n"
 # " 'arrowhead=dot, tailhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'mongodb -> "NODE-SERVICE_redis":<PLUG_mongodb> [color=orange, '
 # "arrowhead=dot, '\n"
 # " 'tailhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'repository -> "NODE-SERVICE_redis":<PLUG_repository> [color=orange, \'\n'
 # " 'arrowhead=dot, tailhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'mongodb -> "NODE-SERVICE_server":<PLUG_mongodb> [color=orange, \'\n'
 # " 'arrowhead=dot, tailhead=dot, tailport=e];\n"
 # "'\n"
 # ' \'repository -> "NODE-SERVICE_server":<PLUG_repository> [color=orange, \'\n'
 # " 'arrowhead=dot, tailhead=dot, tailport=e];\n"
 # "'\n"
 # " '}\n"
 # "')\n")
 # """
 #    # @formatter:on
#
#    result = str(dcg.as_dot())
#
#    assert expected == result

# def test_main(capsys):
#     """CLI Tests"""
#     # capsys is a pytest fixture that allows asserts against stdout/stderr
#     # https://docs.pytest.org/en/stable/capture.html
#     main(["7"])
#     captured = capsys.readouterr()
#     assert "The 7-th Fibonacci number is 13" in captured.out
