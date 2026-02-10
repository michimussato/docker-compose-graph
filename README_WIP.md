<!-- TOC -->
* [docker-compose-graph](#docker-compose-graph)
  * [Install](#install)
  * [CLI](#cli)
  * [Todo](#todo)
    * [`network_mode: service:gerbil`](#network_mode-servicegerbil)
<!-- TOC -->

---

# docker-compose-graph

## Install

```shell
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
```

```shell
pip install git+https://github.com/michimussato/docker-compose-graph.git
```

or

```shell
git clone +https://github.com/michimussato/docker-compose-graph.git
pip install --editable docker-compose-graph
```

## CLI

```
$ docker-compose-graph --help
usage: docker-compose-graph [-h] [--version] [-v] [-vv] [--no-expand-vars] [--no-resolve-relative-volumes] --yaml DOCKER_COMPOSE_YAML
                            [--dot-env DOT_ENV] --outfile OUTFILE --format {dot,svg,png}

Create a graph representation of a Docker Compose file

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -v, --verbose         set loglevel to INFO
  -vv, --very-verbose   set loglevel to DEBUG
  --no-expand-vars, -nx
                        Don't expand environment variables
  --no-resolve-relative-volumes, -nr
                        Don't resolve relative volume paths to absolute paths
  --yaml DOCKER_COMPOSE_YAML, -y DOCKER_COMPOSE_YAML
                        Full path to docker-compose.yaml
  --dot-env DOT_ENV, -d DOT_ENV
                        Full path to .env file
  --outfile OUTFILE, -o OUTFILE
                        Full output path
  --format {dot,svg,png}, -f {dot,svg,png}
                        Output format
```

## Todo

### `network_mode: service:gerbil`

```yaml
  traefik:
    image: traefik:v3.4.0
    container_name: traefik
    env_file:
      - ../.env/pangolin.env
    restart: unless-stopped
    network_mode: service:gerbil # Ports appear on the gerbil service
    depends_on:
      pangolin:
        condition: service_healthy
    command:
      - --configFile=/etc/traefik/traefik_config.yml
```