### Launch docker
```shell
> docker-compose -f docker/docker-compose.yml up
```

### Install dependency
```shell
> poetry shell
> poetry install
```

### Run server
```shell
> python main.py --env local|dev|prod --debug
```
