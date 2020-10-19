import logging
import os
import shutil
import gzip as gz

MEGABYTE = 1024 * 1024


def upload_to_gcs(gcs_hook, bucket, object, filename, gzip=False, mime_type='application/octet-stream'):
    """Upload a file to GCS. Helps avoid OverflowError:
    https://stackoverflow.com/questions/47610283/cant-upload-2gb-to-google-cloud-storage,
    https://developers.google.com/api-client-library/python/guide/media_upload#resumable-media-chunked-upload
    """
    from apiclient.http import MediaFileUpload
    from googleapiclient import errors

    service = gcs_hook.get_conn()

    if gzip:
        filename_gz = filename + '.gz'

        with open(filename, 'rb') as f_in:
            with gz.open(filename_gz, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
                filename = filename_gz

    if os.path.getsize(filename) > 10 * MEGABYTE:
        media = MediaFileUpload(filename, mime_type, resumable=True)

        try:
            request = service.objects().insert(bucket=bucket, name=object, media_body=media)
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    logging.info("Uploaded %d%%." % int(status.progress() * 100))

            return True
        except errors.HttpError as ex:
            if ex.resp['status'] == '404':
                return False
            raise
    else:
        media = MediaFileUpload(filename, mime_type)

        try:
            service.objects().insert(bucket=bucket, name=object, media_body=media).execute()
            return True
        except errors.HttpError as ex:
            if ex.resp['status'] == '404':
                return False
            raise


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
