"""
Module implementing all of the AWS S3 API functions.
"""
import os
import boto3


# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/migrations3.html

def upload_fileobj(aws_access_key_id: str, aws_secret_access_key: str,
                   bucket: str, file_name: str, fileobj: bytes) -> str:
    """This function uploads a file object to a versioned S3 bucket.
    If the assignment uuid has not been created, S3 will create
    a file that is versioned.

    :param aws_access_key_id: An AWS Access key ID
    :param aws_secret_access_key: An AWS Secret access key
    :param bucket: The account bucket
    :param assignment_uuid: The assignment UUID
    :param fileobj: A byte string for a file upload.

    Returns a dictionary of response values

    {'ResponseMetadata':
        {'RequestId': 'EYJ2AARW72SZQMA5',
                       'HostId': 'AQs/sYLoDoOrfCHng6sI7uO2xrHrZ3YNkRRFeR8Vdl5Us5qsn4ukcSh/Lb217HSVuQVJnbScuJw=',
                       'HTTPStatusCode': 200,
                       'HTTPHeaders': {'x-amz-id-2': 'AQs/sYLoDoOrfCHng6sI7uO2xrHrZ3YNkRRFeR8Vdl5Us5qsn4ukcSh/Lb217HSVuQVJnbScuJw=',
                       'x-amz-request-id': 'EYJ2AARW72SZQMA5',
                       'date': 'Mon, 12 Sep 2022 01:18:32 GMT',
                       'x-amz-version-id': 'UeIoFvKqd84.jsbIIGrpMh.5vrIIKeaI',
                       'etag': '"3579c8da7f1e0ad94656e76c886e5125"',
                       'x-amz-storage-class': 'GLACIER_IR',
                       'server': 'AmazonS3',
                       'content-length': '0'}, 'RetryAttempts': 1
        },
     'ETag': '"3579c8da7f1e0ad94656e76c886e5125"',
     'VersionId': 'UeIoFvKqd84.jsbIIGrpMh.5vrIIKeaI'}
    """

    client = boto3.client('s3',
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          )

    response = client.put_object(
        Bucket=bucket,
        Body=fileobj,
        StorageClass='GLACIER_IR', # Glacier instant retrieval
        Key=file_name,
    )

    # For versioned objects (assignments), there
    # is a version ID, everything else does not.
    return response.get('VersionId', '')


def download_fileobj(aws_access_key_id: str,
                     aws_secret_access_key: str,
                     bucket_name: str,
                     file_name: str,
                     download_dir: str,
                     ) -> str:
    """Download a specific file version from s3.

    :param aws_access_key_id: An AWS Access key ID
    :param aws_secret_access_key: An AWS Secret access key
    :param bucket: The account bucket
    :param assignment_name: The name of the assignment. This
                            has the form of 'assign-{assignment_id}'
    :param download_dir: The download directory where the file will be placed

    :returns: A full path to the file.
    """

    client = boto3.client('s3',
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          )

    path = os.path.join(download_dir, file_name)
    with open(path, 'wb') as f:

        client.download_fileobj(bucket_name,
                                file_name,
                                f,
        )

    return path
