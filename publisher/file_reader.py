import os
import json
import pandas as pd
import pika


RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'admin')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'Tubelight@1234')

# print(os.listdir("files"))

credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='file_data', durable=True)


for file in os.listdir("files"):
    print(file)
    try:
        file_extention = file.split(".")[-1]
        file_path = f"files/{file}"
        if file_extention == "xlsx":
            df = pd.read_excel(file_path)
        elif file_extention in ["txt", "csv"]:
            df = pd.read_csv(file_path)
        else:
            print("invalid file")
            continue
        if set(df.columns) != {"name"}:
            print("invalid file headers")
            continue
        print("**********")
        print(df)
        for data in df.to_dict("records"):
            print(data)
            body = json.dumps(data)
            channel.basic_publish(exchange='', routing_key='file_data', body=body.encode())

    except Exception as e:
        print(f"Exception Raised {e}")

