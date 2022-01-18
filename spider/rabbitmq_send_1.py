import pika
import time

exchange_name = 'news'
queue_name = 'urls'

params = pika.URLParameters('amqp://guang:123456@192.168.66.12:5672/test')
connection = pika.BlockingConnection(params)

channel = connection.channel()
channel.exchange_declare(exchange=exchange_name, exchange_type='direct')

# 设置queue，一定要绑定，不使用缺省交换机了
channel.queue_declare(queue=queue_name, exclusive=False)
# routing_key不指定使用队列名
channel.queue_bind(queue=queue_name, exchange=exchange_name)

with connection:
    for i in range(20):
        message = "{}-data-{:02}".format(queue_name, i)
        channel.basic_publish(
            exchange=exchange_name,
            routing_key=queue_name,
            body=message)
        time.sleep(0.1)
    print('Sent OK')

