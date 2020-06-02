import logging
import boto3



def make_object_public(bucket, object_key):
    s3 = boto3.resource('s3')
    object_acl = s3.ObjectAcl(bucket, object_key)
    return object_acl.put(ACL='public-read')


def upload_file(file_name, bucket, object_name=None, public_access=True):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    """

    s3_client = boto3.client('s3')

    if object_name is None: object_name = file_name

    if public_access is True:
        return s3_client.upload_file(file_name, bucket, object_name, ExtraArgs={'ACL':'public-read'})
    else:
        return s3_client.upload_file(file_name, bucket, object_name)
