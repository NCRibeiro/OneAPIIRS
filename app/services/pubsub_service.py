import json
import os
from typing import Any
from core.settings import settings

from google.cloud import pubsub_v1

project_id = os.getenv("GCP_PROJECT_ID", "oneapiirs")
topic_name = os.getenv("PUBSUB_TOPIC", "oneapiirs-events")

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)


def pubsub_message(data: dict[str, Any]) -> Any:
    data_bytes = json.dumps(data).encode("utf-8")
    future = publisher.publish(topic_path, data=data_bytes)
    return future.result()
