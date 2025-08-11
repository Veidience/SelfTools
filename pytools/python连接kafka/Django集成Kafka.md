# Django集成Kafka

# 1. 引入库

```shell
# 官方推荐
pip install confluent-kafka
```

# 2. 填写配置文件

```py
# settings.py

KAFKA_CONFIG = {
	'bootstrap.servers': 'localhost:9092,localhost:9092',
	'group.id': 'my-group',
	# 偏移量重置策略
	'auto.offset.reset': 'earliest',
	'security.protocol': 'SASL_PLAINTEXT',
	'sasl.mechanism': 'PLAIN',
	'sasl.username': '',
	'sasl.password': ''
}
```



