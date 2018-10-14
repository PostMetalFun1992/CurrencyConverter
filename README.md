# Currency conversation API

Based on: DRF, SQLite, Celery & Docker

## Up & run:
1. ```git clone https://github.com/PostMetalFun1992/CurrencyConverter.git```
2. Inside repo dir: ```docker-compose build```
3. And then: ```docker-compose up -d```
4. View API logs: ```docker-compose logs -f api```

## Useful scripts:
* ```./run_celery``` - starts periodic tasks
* ```./run_convert``` - executes curl test script
* ```./run_shell``` - runs django shell with ipython mode
* ```./run_tests``` - starts test session
