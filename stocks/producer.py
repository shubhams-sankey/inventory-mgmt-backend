from kafka import KafkaProducer

# Create Producer
producer = KafkaProducer(
    bootstrap_servers="localhost:9095"
)

def produce_message(msg):

    try:
        parsed_msg = " {} ".format(str(msg))

        # print("Message Prodcer ===> ", parsed_msg)

        producer.send(topic='order-placed', value=bytes(parsed_msg, 'utf-8'))

    except Exception as e:
        print("Producer error:")
        print(e)