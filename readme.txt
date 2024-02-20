стягиваем имеджи
docker pull mongo
docker pull redis
docker pull rabbitmq:3-management

создаем контейнеры
docker run -d -p 27017:27017 --name my_mongodb mongo
docker run -p 6379:6379 --name some-redis -d redis
docker run -d --name rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3-management

запускаем контейнеры
docker start my_mongodb
docker start some-redis
docker start rabbit

логинка в rabbitmq
rabbitmq login: guest
rabbitmq password: guest

1я часть дз
с помощью "load_data.py" загружаем данные в монгу
с помощью "search_quotes.py" проверяем наши запросы

2я часть дз
с помощью "producer.py" отправляем дынные в rabbitmq
с помощью "consumer_email.py" и "consumer_sms.py" проверяем