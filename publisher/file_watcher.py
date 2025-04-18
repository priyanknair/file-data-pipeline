import os
import pika
import time
import json
import pandas as pd
from datetime import datetime
# Was not working with docker as it was not detecting changes in volume
# from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import FileSystemEventHandler


RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'guest')

print("Starting publisher")


def push_to_queue(file_path):
    file_extension = file_path.split(".")[-1]
    if file_extension == "xlsx":
        df = pd.read_excel(file_path)
    elif file_extension in ["txt", "csv"]:
        df = pd.read_csv(file_path)
    else:
        print(f"[{datetime.now()}] invalid file {file_path}")
        return
    if set(df.columns) != {"name"}:
        print(f"[{datetime.now()}]invalid file headers")
        return
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='file_data', durable=True)
    print("**********")
    print(df)
    for data in df.to_dict("records"):
        print(data)
        body = json.dumps(data)
        channel.basic_publish(exchange='', routing_key='file_data', body=body.encode())

    connection.close()


class FileChangeHandler(FileSystemEventHandler):
    # def on_modified(self, event):
    #     print(event)
    #     if not event.is_directory:
    #         push_to_queue(event.src_path)

    def on_created(self, event):
        print(event)
        if not event.is_directory:
            push_to_queue(event.src_path)


if __name__ == "__main__":
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path='files', recursive=False)
    observer.start()
    print(" [*] Watching files in 'files' folder")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
