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
from threading import Thread


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
        s3.download_file('lamps-python', 'color.txt', 'color.txt')
        color = open("color.txt", "r")
        current_color = color.read()
        color.close()
        if current_color == "green":
            print("GREEN")
        elif current_color == "blue":
            print("BLUE")
        time.sleep(5)


def listen_change():
    while True:
        if keyboard.is_pressed('g'):
            f = open("color.txt", "w")
            f.write("green")
            f.close()
            upload_file("color.txt", "lamps-python")
        elif keyboard.is_pressed('b'):
            f = open("color.txt", "w")
            f.write("blue")
            f.close()
            upload_file("color.txt", "lamps-python")


s3 = boto3.client('s3')


if __name__ == '__main__':
    Thread(target=sync_lamp()).start()
    Thread(target=listen_change()).start()
