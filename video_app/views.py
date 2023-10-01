"""This module defines class UploadFile"""
import os
import re
import magic
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView
from chunked_upload.exceptions import ChunkedUploadError
from chunked_upload.constants import http_status


class UploadFile(ChunkedUploadView):
    """This class defines a method for posting video files to the app."""

    parser_classes = [FormParser, MultiPartParser]
    max_bytes = 300 * 1000 * 1000
    chunk_max_bytes = 30 * 1000 * 1000
    content_range_header = 'HTTP_CONTENT_RANGE'
    content_range_pattern = re.compile(
        r'^bytes (?P<start>\d+)-(?P<end>\d+)/(?P<total>\d+)$'
    )

    def check_permissions(self, request):
        """
        Grants permission to start/continue an upload based on the request.
        """
        # pylint: disable=unnecessary-pass
        pass


    def validate(self, request):
        """
        Placeholder method to define extra validation.
        Must raise ChunkedUploadError if validation fails.
        """
        file = request.FILES.get('file')
        if not file:
            raise ChunkedUploadError(status=http_status.HTTP_400_BAD_REQUEST,
                                     detail='No chunk file was submitted')

        content_range = request.META.get(self.content_range_header, '')
        match = self.content_range_pattern.match(content_range)
        if match:
            start = int(match.group('start'))
            end = int(match.group('end'))

            if end + 1 - start > self.chunk_max_bytes:
                raise ChunkedUploadError(status=http_status.HTTP_400_BAD_REQUEST,
                                        detail=f'Chunk size {end + 1 - start} exceeded chunk '\
                                                f'limit {self.chunk_max_bytes} bytes.')

        upload_id = request.FILES.get('upload_id')
        acceptable_mimetypes = ['video/mp4', 'video/webm', 'video/ogg', 'video/x-msvideo',
                                'video/x-matroska', 'video/x-flv', 'video/3gpp']

        if not upload_id:
            file_mime_type = magic.from_buffer(file.read(1024), mime=True)
            if file_mime_type not in acceptable_mimetypes:
                raise ChunkedUploadError(status=http_status.HTTP_400_BAD_REQUEST,
                                        detail='Unsupported file type')


class CompletedUpload(ChunkedUploadCompleteView):
    """This class defines a method for posting video files to the app."""

    parser_classes = [FormParser, MultiPartParser]
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
