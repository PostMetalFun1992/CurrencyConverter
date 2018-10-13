# Currency conversation API

Django REST Framework, SQLite & Celery

## Up & run:
1. Install docker & docker compose
2. Clone repo into some dir: ```https://github.com/PostMetalFun1992/CurrencyConverter.git```
3. Inside repo dir: ```docker-compose build```
4. And then: ```docker-compose up -d```
5. Access API logs: ```docker-compose logs -f api```

## Useful scripts:
* ```./run_shell``` - runs django shell with ipython mode
* ```./run_tests``` - starts pytest session
* ```./run_convert``` - curl script for API requests
* ```./run_celery``` - start celery tasks 
