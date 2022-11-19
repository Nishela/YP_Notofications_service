mq_connection = None
mq_producer = None


async def get_mq_producer():
    return mq_producer


async def get_mq_connection():
    return mq_connection
