import json
from google.cloud import storage
from google.cloud.storage import Blob


bucket_name = 'miro-to-notion'
file_name = 'card_metadata.json'
client = storage.Client()
bucket = client.get_bucket(bucket_name)


def read():
    global bucket
    blob = bucket.get_blob(file_name)
    if blob is None:
        return {}
    return json.loads(blob.download_as_string(client=None))


def save(data):
    global bucket
    blob = Blob(file_name, bucket)
    blob.upload_from_string(json.dumps(data))
    return 200
