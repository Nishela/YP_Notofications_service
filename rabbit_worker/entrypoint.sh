#!/bin/sh

echo "Waiting for RabbitMQ..."
while ! nc -z -v "$RABBITMQ_HOST" "$RABBITMQ_PORT";
do
  >&2 echo "RabbitMQ is unavailable - sleeping"
  sleep 0.4;
done
echo "RabbitMQ was started"


exec "$@"
