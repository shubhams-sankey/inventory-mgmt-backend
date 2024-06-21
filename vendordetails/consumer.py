# from kafka import KafkaConsumer

# from .views import orderDetailsEventStream

# def kafka_order_consumer():

#     try:

#         print("============ Consumer Starting ===========")

#         consumer = KafkaConsumer(
#             "order-placed",
#             bootstrap_servers="localhost:9095",
#             enable_auto_commit=True,
#             auto_commit_interval_ms=1000
#         )

#         for message in consumer:
#             print("============ Message Received ============= ")
#             print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition, message.offset, message.key, message.value.decode('utf-8')))
#             orderDetailsEventStream(message.value.decode('utf-8'))

#     except Exception as e:
#         print(e)