import pathlib

from docker_graph.docker_graph import main, DockerComposeGraph
from docker_graph.utils import *
from docker_graph.yaml_tags.overrides import *

__author__ = "Michael Mussato"
__copyright__ = "Michael Mussato"
__license__ = "MIT"


# def test_get_root_ports():
#     # Todo
#     raise NotImplementedError


def test_get_service_ports():
    dcg = DockerComposeGraph(
        expandvars=False
    )
    trees = dcg.parse_docker_compose(
        pathlib.Path(__file__).parent / "fixtures" / "deadline-docker" / "10.2" / "docker-compose.yaml"
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
    dcg = DockerComposeGraph(
        expandvars=False
    )
    trees = dcg.parse_docker_compose(
        pathlib.Path(__file__).parent / "fixtures" / "deadline-docker" / "10.2" / "docker-compose.yaml"
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
        pathlib.Path(__file__).parent / "fixtures" / "deadline-docker" / "10.2" / "docker-compose.yaml"
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
        pathlib.Path(__file__).parent / "fixtures" / "deadline-docker" / "10.2" / "docker-compose.yaml"
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


def test_deep_merge_1():
    d1 = {
        "key1": "value1",
    }

    d2 = {
        "key2": "value2",
    }

    expected = {
        "key1": "value1",
        "key2": "value2",
    }

    result = deep_merge(dict1=d1, dict2=d2)

    assert result == expected


def test_deep_merge_2():
    d1 = {
        "key1": "value1",
    }

    d2 = {
        "key1": "value2",
    }

    expected = {
        "key1": "value2",
    }

    result = deep_merge(dict1=d1, dict2=d2)

    assert result == expected


def test_deep_merge_3():
    d1 = {
        "key1": [
            "value1",
        ],
    }

    d2 = {
        "key1": [
            "value2",
        ],
    }

    expected = {
        "key1": [
            "value2",
        ],
    }

    result = deep_merge(dict1=d1, dict2=d2)

    assert result == expected


def test_deep_merge_4():
    d1 = {
        'service_name': 'server',
        'service_config': {
            'image': 'ynput/ayon:latest',
            'restart': 'unless-stopped',
            'healthcheck': {
                'test': [
                    'CMD',
                    'curl',
                    '-f',
                    'http://localhost:5000/api/info'
                ], 'interval': '10s',
                'timeout': '2s',
                'retries': 3
            },
            'depends_on': {
                'postgres': {
                    'condition': 'service_healthy'
                },
                'redis': {
                    'condition': 'service_started'
                }
            },
            'expose': [5000],
            'ports': ['5000:5000'],
            'volumes': [
                './addons:/addons',
                './storage:/storage',
                '/etc/localtime:/etc/localtime:ro'
            ]
        }
    }

    d2 = {
        'service_name': 'server',
        'service_config': {
            'container_name': 'ayon-server-10-2',
            'hostname': 'ayon-server-10-2',
            'domainname': '${ROOT_DOMAIN}',
            'networks': [
                'repository', 'mongodb'
            ],
            'ports': OverrideArray(array=['${AYON_PORT_HOST}:${AYON_PORT_CONTAINER}'])
        }
    }

    expected = {
        "key1": [
            "value2",
        ],
    }

    result = deep_merge(dict1=d1, dict2=d2)

    assert result == expected


def test_iterate_trees():
    dcg = DockerComposeGraph(
        expandvars=True,
        resolve_relative_volumes=True,
    )
    trees = dcg.parse_docker_compose(
        pathlib.Path(__file__).parent / "fixtures" / "deadline-docker" / "10.2" / "docker-compose.yaml"
    )

    print(f"{trees = }")

    # resolve environment variables (optional)
    dcg.load_dotenv(
        pathlib.Path(__file__).parent / "fixtures" / "deadline-docker" / "10.2" / ".env"
    )

    dcg.iterate_trees(trees)

    # fixed_graph = dcg.get_fixed_graph()

    dcg.write_png(
        path=pathlib.Path(__file__).parent / "fixtures" / "out" / "main_graph.png",
    )
    dcg.write_dot(
        path=pathlib.Path(__file__).parent / "fixtures" / "out" / "main_graph.dot",
    )

# def test_main(capsys):
#     """CLI Tests"""
#     # capsys is a pytest fixture that allows asserts against stdout/stderr
#     # https://docs.pytest.org/en/stable/capture.html
#     main(["7"])
#     captured = capsys.readouterr()
#     assert "The 7-th Fibonacci number is 13" in captured.out
