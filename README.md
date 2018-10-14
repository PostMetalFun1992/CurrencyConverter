# Currency conversation API

Based on: DRF, SQLite, Celery & Docker

## Up & run:
1. ```git clone https://github.com/PostMetalFun1992/CurrencyConverter.git```
2. Set your envivoment variables: make ```compose/ENVS.env``` file based on ```compose/ENVS.env.example```
3. Inside repo dir: ```docker-compose build```
4. And then: ```docker-compose up -d```
5. View API logs: ```docker-compose logs -f api```

## Useful scripts:
* ```./run_celery``` - starts periodic tasks
* ```./run_convert``` - executes curl test script
* ```./run_shell``` - runs django shell with ipython mode
* ```./run_tests``` - starts test session
