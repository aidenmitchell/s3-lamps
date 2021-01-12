# import boto3
#
# s3 = boto3.resource('s3')
# my_bucket = s3.Bucket('lamps-python')
#
# for my_bucket_object in my_bucket.objects.all():
#     print(my_bucket_object)

import logging
import time
import boto3
import keyboard
from botocore.exceptions import ClientError
from threading import Thread, Lock

mutex = Lock()

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def sync_lamp():
    while True:
        with mutex:
            s3.download_file('lamps-python', 'color.txt', 'color.txt')
            with open("color.txt", "r") as color:
                current_color = color.read()
            if current_color == "green":
                print("GREEN")
            elif current_color == "blue":
                print("BLUE")
            time.sleep(5)


def listen_change():
    if keyboard.is_pressed('g'):
        with mutex:
            f = open("color.txt", "w")
            f.write("green")
            f.close()
            upload_file("color.txt", "lamps-python")
    elif keyboard.is_pressed('b'):
        with mutex:
            f = open("color.txt", "w")
            f.write("blue")
            f.close()
            upload_file("color.txt", "lamps-python")


s3 = boto3.client('s3')

if __name__ == '__main__':
    t1 = Thread(target = sync_lamp)
    t2 = Thread(target = listen_change)
    t1.start()
    t2.start()
    t1.join() # Don't exit while threads are running
    t2.join()
