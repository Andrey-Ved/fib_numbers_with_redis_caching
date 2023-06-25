#  Fibonacci numbers with Redis caching

Simple example of Redis use (python, [Redis](https://redis.io/docs/))

##  Setup & Installation 

Create a virtual environment and install the dependencies:
```bash
$ python -m venv venv
$ source env/bin/activate

$ pip install -r requirements.txt
```

Start Redis with docker-compose:

```bash
docker-compose up -d
```

Verify that the services are up and running:
```
$ docker ps
```

## Usage

Start app.py
```bash
$ python app.py
```

## Note

Stop lifted containers:
```bash
$ docker-compose stop
```

Start stopped containers:
```bash
$ docker-compose start
```

Stop and delete containers and network:
```bash
$ docker-compose down
```

Remove Redis image:
```bash
$ docker rmi redis
```