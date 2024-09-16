import os
from dotenv import load_dotenv

import swan
import json

def bucket_info(bucket_client: swan.BucketAPI, bucket_names: list[str]) -> None:
    """Create however many buckets in the bucket_names list, get their information, then delete them.

    Args:
        bucket_client: The BucketApi client to use MultiChain Storage.
        bucket_names: A list of bucket names.

    Return:
        None.
    """
    # try to delete the bucket, this is so that the program can run again properly if an error occurs
    # this will print an error if the bucket does not yet exist.
    for bucket in bucket_names:
        bucket_client.delete_bucket(bucket)

    # create buckets and store the function returns as a tuple of the bucket name and creation status
    bucket_create_statuses = [(bucket_name, bucket_client.create_bucket(bucket_name)) for bucket_name in bucket_names]

    # Determine which bucket could not be created
    for bucket_create_status in bucket_create_statuses:
        if not bucket_create_status[1]:
            print(f"Error creating bucket: {bucket_create_status[0]}")

    # get the buckets that were created
    created_buckets = [bucket_create_status[0] for bucket_create_status in bucket_create_statuses if bucket_create_status[1]]

    # return if no buckets were created
    if not created_buckets:
        return

    # get the info of the first created bucket
    print(bucket_client.get_bucket(created_buckets[0]).to_json())

    # get the info of all the buckets
    for bucket in bucket_client.list_buckets():
        print(bucket.to_json())

    # delete the buckets
    bucket_delete_statuses = [(bucket_name, bucket_client.delete_bucket(bucket_name)) for bucket_name in created_buckets]

    # Determine which bucket could not be deleted
    for bucket_delete_status in bucket_delete_statuses:
        if not bucket_delete_status[1]:
            print(f"Error deleting bucket: {bucket_create_status[0]}")



if __name__ == '__main__':
    # load environment variables
    load_dotenv("../.env")

    # create the bucket client
    API_KEY = os.getenv("API_KEY")
    CHAIN_NAME = os.getenv("CHAIN_NAME")
    # set is_calibration=True if using the calibration MCS
    #mcs_api = APIClient(api_key=API_KEY, chain_name=CHAIN_NAME, is_calibration=True)
    #bucket_client = BucketAPI(api_key=API_KEY, is_calibration=True)

    bucket_client = swan.resource(api_key=API_KEY, service_name='mcs', is_calibration=True)


    bucket_names = ["my-test-bucket-1", "my-test-bucket-2"]
    bucket_info(bucket_client, bucket_names)

