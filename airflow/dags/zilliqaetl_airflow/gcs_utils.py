import logging
import os
import shutil
import gzip as gz

MEGABYTE = 1024 * 1024


def upload_to_gcs(gcs_hook, bucket, object, filename, gzip=False, mime_type='application/octet-stream'):
    service = gcs_hook.get_conn()

    if gzip:
        filename_gz = filename + '.gz'

        with open(filename, 'rb') as f_in:
            with gz.open(filename_gz, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
                filename = filename_gz

    bucket = service.get_bucket(bucket)
    blob = bucket.blob(object, chunk_size=10 * MEGABYTE)
    blob.upload_from_filename(filename)


def download_from_gcs(bucket, object, filename):
    """Download a file from GCS. Can download big files unlike gcs_hook.download which saves files in memory first"""
    from google.cloud import storage

    storage_client = storage.Client()

    bucket = storage_client.get_bucket(bucket)
    blob_meta = bucket.get_blob(object)

    if blob_meta.size > 10 * MEGABYTE:
        blob = bucket.blob(object, chunk_size=10 * MEGABYTE)
    else:
        blob = bucket.blob(object)

    blob.download_to_filename(filename)
