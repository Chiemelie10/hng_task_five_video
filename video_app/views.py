"""This module defines class UploadFile"""
import os
from rest_framework.parsers import MultiPartParser
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView


class UploadFile(ChunkedUploadView):
    """This class defines a method for posting video files to the app."""

    parser_classes = [MultiPartParser]

    def check_permissions(self, request):
        """
        Grants permission to start/continue an upload based on the request.
        """
        # pylint: disable=unnecessary-pass
        pass

    def get_max_bytes(self, request):
        """
        Used to limit the max amount of data that can be uploaded. `None` means
        no limit.
        You can override this to have a custom `max_bytes`, e.g. based on
        logged user.
        """

        self.max_bytes = 30 * 1000 * 1000

        return self.max_bytes



class CompletedUpload(ChunkedUploadCompleteView):
    """This class defines a method for posting video files to the app."""

    parser_classes = [MultiPartParser]
    do_md5_check = False

    def check_permissions(self, request):
        """
        Grants permission to start/continue an upload based on the request.
        """
        # pylint: disable=unnecessary-pass
        pass

    def _save(self, chunked_upload):
        """
        Overrode the save method.
        """
        filename = chunked_upload.filename

        current_path = chunked_upload.file
        print(current_path)

        if 'part' in f'{current_path}' and '.' in filename:
            file_extension = filename.split('.')[-1]
            new_path = f'{current_path}'.replace('part', file_extension)

            current_destination_abs_path = os.path.join(settings.MEDIA_ROOT, f'{current_path}')
            absolute_destination_path = os.path.join(settings.MEDIA_ROOT, f'{new_path}')

            os.rename(f'{current_destination_abs_path}', f'{absolute_destination_path}')

            chunked_upload.file = new_path
            chunked_upload.save()

    def get_response_data(self, chunked_upload, request):
        """
        Data for the response. Should return a dictionary-like object.
        Called *only* if POST is successful.
        """
        media_url = settings.MEDIA_URL
        return {
            "upload_id": chunked_upload.upload_id,
            "upload_status": chunked_upload.status,
            "created_on": chunked_upload.created_on,
            "completed_on": chunked_upload.completed_on,
            "filename": chunked_upload.filename,
            "url": f"http://{get_current_site(request).domain}{media_url}{chunked_upload.file}"
        }
