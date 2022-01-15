import threading

import pika

exchage_name = 'news'
queue_name = 'urls'

params = pika.URLParameters('amqp://guang:123456@192.168.66.12:5672/test')
connection = pika.BlockingConnection(params)
channel = connection.channel()

# 指定交换机使用路由模式
channel.exchange_declare(exchange=exchage_name, exchange_type='direct')

# 设置queue，一定要绑定，不使用缺省交换机了
channel.queue_declare(queue=queue_name, exclusive=False)
channel.queue_bind(queue=queue_name, exchange=exchage_name)


def cancel(ch, tag):
    print(ch, tag)
    ch.basic_cancel(tag)


def callback(ch, method, properties, body):
    print('Get Msg = {}'.format(body))


# with connection:
#     """单个消费"""
#     method, props, body = channel.basic_get(
#         queue=queue_name,
#         auto_ack=True
#     )
#     if body:
#         print('get Msg{}'.format(body))

with connection:
    """批量消费"""
    tag = channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True
    )
    # 超时自动取消
    threading.Timer(10, cancel, [channel, tag]).start()

    channel.start_consuming()
