# stock-screener

### Local Environment Setup
- Download mongo db from docker using following command
```commandline
    docker pull mongo
```
- Start mongo on local machine using
```commandline
    docker run -d -p 27017:27017 mongo:latest
```
- Install all required dependencies
```commandline
    pip3 install -r requirements.txt
```
### Development enviornment
- Run test cases
```commandline
    tox -epy38
```

- Run static code analysis
```commandline
    tox -epep8
```

- Run coverage
```commandline
    tox -ecover
```

### Run screener for development on local
```
    python3/python screener.py screen --t=stock/index/sector --config-file=<yaml config file>
```

### Package project in docker image
- Go to project folder
- Build docker image
```commandline
    docker build -t screener:latest -f Dockerfile .
```
**NOTE**: Now docker image is ready
