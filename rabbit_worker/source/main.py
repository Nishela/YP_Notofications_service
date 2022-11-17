from rabbitmq import Consumer


def custom_func(channel, method, properties, body):
    print(body)


if __name__ == '__main__':
    consumer = Consumer()
    consumer.set_on_message_callback(custom_func)
    try:
        consumer.start()
    except KeyboardInterrupt:
        consumer.stop()
