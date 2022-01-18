import pika


class MessageBase:
    def __init__(self, host, port, user, password, virtualhost, exchange, queue):
        self.exchange_name = exchange
        self.queue_name = queue

        url = "amqp://{}:{}@{}:{}/{}".format(
            user, password, host, port, virtualhost
        )
        params = pika.URLParameters(url)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()

        # 指定交换机使用路由模式
        self.channel.exchange_declare(
            exchange=self.exchange_name,
            exchange_type='direct'
        )
        self.channel.queue_declare(queue=self.queue_name, exclusive=False)
        self.channel.queue_bind(queue=self.queue_name, exchange=self.exchange_name)


class Producer(MessageBase):
    def produce(self, message):
        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=self.queue_name,
            body=message)


class Consumer(MessageBase):
    def consumer(self):
        method, props, body = self.channel.basic_get(
            queue=self.queue_name,
            auto_ack=True
        )
        body = body.decode()
        return body


if __name__ == '__main__':
    qs = ('urls', 'htmls', 'outputs')
    for q in qs:
        p = Producer('192.168.66.12', 5672, 'guang', '123456', 'test', 'news', q)
        for i in range(40):
            msg = '{}-data-{:02}'.format(q, i)
            p.produce(msg)
    c1 = Consumer('192.168.66.12', 5672, 'guang', '123456', 'test', 'news', qs[0])
    c2 = Consumer('192.168.66.12', 5672, 'guang', '123456', 'test', 'news', qs[1])
    c3 = Consumer('192.168.66.12', 5672, 'guang', '123456', 'test', 'news', qs[2])
    for i in range(40):
        print(c1.consumer())
        print(c2.consumer())
        print(c3.consumer())
