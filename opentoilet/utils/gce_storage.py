import datetime
import mimetypes
import re
import uuid
from tempfile import SpooledTemporaryFile
from urllib import parse as urlparse

from django.conf import settings
from django.core.exceptions import SuspiciousFileOperation
from django.core.files.base import File
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from django.utils.encoding import force_str, smart_str
from google.cloud import _helpers as gcloud_helpers
from google.cloud import storage
from google.cloud.exceptions import NotFound

storage_client = storage.Client(settings.GS_PROJECT_ID)


def safe_join(base, path):
    base = force_str(base).replace("\\", "/").lstrip("/").rstrip("/") + "/"
    path = force_str(path).replace("\\", "/").lstrip("/")

    # Ugh... there must be a better way that I can't think of right now
    if base == "/":
        base = ""

    resolved_url = urlparse.urljoin(base, path)

    resolved_url = re.sub("//+", "/", resolved_url)

    if not resolved_url.startswith(base):
        raise SuspiciousFileOperation(
            "The joined path ({}) is located outside of the base path "
            "component ({})".format(resolved_url, base)
        )

    return resolved_url


def prepare_name(name):
    return smart_str(name, encoding="utf-8")


def remove_prefix(target, prefix):
    if target.startswith(prefix):
        return target[len(prefix) :]
    return target


class GCloudFile(File):
    """
    Django file object that wraps a SpooledTemporaryFile and remembers changes on
    write to reupload the file to GCS on close()
    """

    def __init__(self, blob, maxsize=1000):
        """
        :type blob: google.cloud.storage.blob.Blob
        """
        self._dirty = False
        self._tmpfile = SpooledTemporaryFile(
            max_size=maxsize, prefix="django_gcloud_storage_"
        )

        self._blob = blob

        super(GCloudFile, self).__init__(self._tmpfile)

    def _update_blob(self):
        # Specify explicit size to avoid problems with not yet spooled temporary files
        # Djangos File.size property already knows how to handle cases like this
        self._blob.upload_from_file(self._tmpfile, size=self.size, rewind=True)

    def write(self, content):
        self._dirty = True
        super(GCloudFile, self).write(content)

    def close(self):
        if self._dirty:
            self._update_blob()
            self._dirty = False

        super(GCloudFile, self).close()


@deconstructible
class DjangoGCloudStorage(Storage):
    _client = None

    def __init__(self, project=None, bucket=None, directory=""):
        self._bucket = None

        if bucket is not None:
            self.bucket_name = bucket
        else:
            self.bucket_name = settings.GS_BUCKET_NAME

        if project is not None:
            self.project_name = project
        else:
            self.project_name = settings.GS_PROJECT_ID

        self.bucket_subdir = directory  # TODO should be a parameter
        self.default_content_type = "application/octet-stream"

    @staticmethod
    def generic_upload_location(instance, original_filename):
        filename = original_filename.split("/")[-1]
        return f"{settings.GS_DIR}/files/{str(uuid.uuid4())}-{filename}"

    @property
    def client(self):
        """
        :rtype: storage.Client
        """
        if not self._client:
            self._client = storage_client
        return self._client

    @property
    def bucket(self):
        """
        :rtype: Bucket
        """
        if not self._bucket:
            self._bucket = self.client.get_bucket(self.bucket_name)
        return self._bucket

    def _save(self, name, content):
        name = safe_join(self.bucket_subdir, name)
        name = prepare_name(name)

        # Required for InMemoryUploadedFile objects, as they have no fileno
        total_bytes = None if not hasattr(content, "size") else content.size

        # Set correct mimetype or fallback to default
        _type, _ = mimetypes.guess_type(name)
        content_type = getattr(content, "content_type", None)
        content_type = content_type or _type or self.default_content_type

        blob = self.bucket.blob(name)
        blob.upload_from_file(content, size=total_bytes, content_type=content_type)

        return name

    def _open(self, name, mode):
        # TODO implement mode?

        name = safe_join(self.bucket_subdir, name)
        name = prepare_name(name)

        blob = self.bucket.get_blob(name)
        if blob is None:
            # Create new
            blob = self.bucket.blob(name)
            tmp_file = GCloudFile(blob)
        else:
            tmp_file = GCloudFile(blob)
            blob.download_to_file(tmp_file)

        tmp_file.seek(0)
        return tmp_file

    def created_time(self, name):
        name = safe_join(self.bucket_subdir, name)
        name = prepare_name(name)

        blob = self.bucket.get_blob(name)

        # google.cloud doesn't provide a public method for this
        value = blob._properties.get("timeCreated", None)
        if value is not None:
            naive = datetime.datetime.strptime(value, gcloud_helpers._RFC3339_MICROS)
            return naive.replace(tzinfo=gcloud_helpers.UTC)

    def delete(self, name):
        name = safe_join(self.bucket_subdir, name)
        name = prepare_name(name)

        try:
            self.bucket.delete_blob(name)
        except NotFound:
            pass

    def exists(self, name):
        name = safe_join(self.bucket_subdir, name)
        name = prepare_name(name)

        return self.bucket.get_blob(name) is not None

    def size(self, name):
        name = safe_join(self.bucket_subdir, name)
        name = prepare_name(name)

        blob = self.bucket.get_blob(name)

        return blob.size if blob is not None else None

    def modified_time(self, name):
        name = safe_join(self.bucket_subdir, name)
        name = prepare_name(name)

        blob = self.bucket.get_blob(name)

        return blob.updated if blob is not None else None

    def get_modified_time(self, name):
        # In Django>=1.10, modified_time is deprecated, and modified_time will be removed in Django 2.0.
        return self.modified_time(name)

    def listdir(self, path):
        path = safe_join(self.bucket_subdir, path)
        path = prepare_name(path)

        iterator = self.bucket.list_blobs(prefix=path, delimiter="/")

        items = [remove_prefix(blob.name, path) for blob in list(iterator)]
        # prefixes is only set after first iterating the results!
        dirs = [
            remove_prefix(prefix, path).rstrip("/")
            for prefix in list(iterator.prefixes)
        ]

        items.sort()
        dirs.sort()

        return dirs, items

    def url(self, name):
        name = prepare_name(name)
        return f"{settings.GS_CDN_URL}/{name}"
