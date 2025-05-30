from redis import Redis
import json

redis_client = Redis(host='localhost', port=6379, db=0, decode_responses=True)

pubsub = redis_client.pubsub()
pubsub.subscribe('order:status-changed')

for message in pubsub.listen():
    if message['type'] == 'message':
        channel = message['channel']
        data = json.loads(message['data'])
        print(f" Заказ {data['orderId']} пользователя {data['userId']} сменил статус на {data['newStatus']}")