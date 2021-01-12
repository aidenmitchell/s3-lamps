import keyboard
import boto3


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
    except:
        return False
    return True


s3 = boto3.client('s3')

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