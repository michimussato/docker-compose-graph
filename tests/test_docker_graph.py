import pydot
import pathlib

from docker_graph.docker_graph import main, DockerComposeGraph

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
    dcg = DockerComposeGraph(
        expandvars=False
    )
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

    dcg.iterate_trees(trees)

    fixed_graph = dcg.get_fixed_graph()

    fixed_graph.write_png(
        path=pathlib.Path(__file__).parent / "fixtures" / "out" / "main_graph.png",
    )
    fixed_graph.write_dot(
        path=pathlib.Path(__file__).parent / "fixtures" / "out" / "main_graph.dot",
    )


# def test_main(capsys):
#     """CLI Tests"""
#     # capsys is a pytest fixture that allows asserts against stdout/stderr
#     # https://docs.pytest.org/en/stable/capture.html
#     main(["7"])
#     captured = capsys.readouterr()
#     assert "The 7-th Fibonacci number is 13" in captured.out
