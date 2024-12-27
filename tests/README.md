

---

# Setup

```
cd tests/fixtures
gh repo clone michimussato/deadline-docker

mkdir -p deadline-docker/repos

git -C deadline-docker/repos clone https://github.com/ynput/ayon-docker
git -C deadline-docker/repos clone https://gitlab.com/mathbou/docker-cgwire.git
```