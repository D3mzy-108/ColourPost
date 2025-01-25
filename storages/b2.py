from django.core.files.storage import Storage
from core import settings
from b2sdk.v2 import InMemoryAccountInfo, B2Api
import os


class BackblazeB2Storage(Storage):
    def __init__(self):
        self.account_info = InMemoryAccountInfo()
        self.b2_api = B2Api(self.account_info)
        print(settings.AWS_ACCESS_KEY_ID)
        print(settings.AWS_SECRET_ACCESS_KEY)
        self.b2_api.authorize_account(
            "production", settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        self.bucket = self.b2_api.get_bucket_by_name(self.bucket_name)

    def _save(self, name, content):
        name = self._clean_name(name)
        content.open()
        try:
            file_data = content.read()
            self.bucket.upload_bytes(file_data, name)
        except Exception as e:
            raise IOError(f"Error uploading file {name}: {e}")
        finally:
            content.close()
        return name

    def _open(self, name, mode='rb'):
        name = self._clean_name(name)
        try:
            file_info = self.bucket.download_file_by_name(name)
            return file_info.download_as_bytes()
        except Exception as e:
            raise IOError(f"Error retrieving file {name}: {e}")

    def url(self, name):
        name = self._clean_name(name)
        return f"https://f003.backblazeb2.com/file/{settings.AWS_STORAGE_BUCKET_NAME}/{name}"

    def exists(self, name):
        name = self._clean_name(name)
        try:
            for file_version in self.bucket.list_file_versions(file_name=name):
                if file_version.file_name == name:
                    return True
            return False
        except Exception:
            return False

    def _clean_name(self, name):
        return os.path.normpath(name).replace('\\', '/')
