from confluent_kafka import Producer


class KafkaProducer(object):
    """ kafka服务创建 """

    def __init__(self, kafka_config):
        """ 构造函数 """
        self.producer = Producer(kafka_config)


if __name__ != '__main__':
    """ 构建Producer, config从配置文件读取 """
    producer = KafkaProducer({}).producer


if __name__ == '__main__':
    """ 测试 """
    kafka_config = {
        'bootstrap.servers': 'localhost:9092,localhost:9093,localhost:9094',
        'sasl.mechanism': 'PLAIN',
        'security.protocol': 'SASK',
        'sasl.username': 'admin',
        'sasl.password': '<PASSWORD>',
    }

    producer = KafkaProducer(kafka_config).producer

    msg = 'hhh'

    producer.produce('topic', msg)
    producer.flush()