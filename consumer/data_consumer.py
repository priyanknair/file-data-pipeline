import os
import sys
import json
import pika
from datetime import datetime
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import urllib.parse


RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'guest')
HOST = os.getenv('DB_HOST', '127.0.0.1')
USER = os.getenv('DB_USER', 'postgres')
PASSWORD = os.getenv('DB_PASSWORD', 'root')

print("Starting Consumer")


def main():
    enc_password = urllib.parse.quote_plus(PASSWORD)
    # engine = create_engine(f"mysql+pymysql://{USER}:{enc_password}@{HOST}:3306/test")
    engine = create_engine(f"postgresql+psycopg2://{USER}:{enc_password}@{HOST}:5432/test")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    FileData = Base.classes.file_data
    session = Session(engine)
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='file_data', durable=True)

    def callback(ch, method, properties, body):
        if isinstance(body, str):
            body = json.loads(body)
        else:
            body = json.loads(body.decode())
        print(f"Received {body}")
        if body.get("name"):
            data = FileData(name=body["name"], created_date=datetime.now())
            session.add(data)
        session.commit()

    channel.basic_consume(queue='file_data', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for callbacks. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)