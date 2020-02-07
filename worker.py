#!/usr/bin/env python
from typing import Any

from confluent_kafka import Consumer, KafkaException
import django
import os
import json
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()


def main() -> None:
    from notifications.worker import execute_message

    consumer = Consumer(
        {
            "bootstrap.servers": "kafka:29092",
            "group.id": "notifications",
            "auto.offset.reset": "earliest",
        }
    )

    consumer.subscribe(["notifications"])
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            else:
                try:
                    data = json.loads(msg.value())
                    execute_message(data)

                except Exception as e:
                    print(msg.value())
                    print("Failed to handle message " + str(e))

    except KeyboardInterrupt:
        sys.stderr.write("%% Aborted by user\n")

    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


if __name__ == "__main__":
    main()
