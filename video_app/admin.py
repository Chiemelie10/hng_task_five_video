"""This module configures the admin web page."""
import magic
from django.contrib import admin
from django.core.exceptions import ValidationError


# class ChunkedUploadAdmin(admin.ModelAdmin):
#     """This class configures the admin web page."""
#     search_fields = ('upload_id',)

#     def save_model(self, request, obj, form, change):
#         """
#         This method checks that only allowed extensions can be saved in the database
#         """
#         if obj.chunked_upload_chunkedupload.file:
#             accept = ['video/mp4', 'video/webm', 'video/ogg', 'video/x-msvideo', 'video/mpeg']
#             file_mime_type = magic.from_buffer(obj.chunked_upload_chunkedupload.file.read(1204), mime=True)
#             if file_mime_type not in accept:
#                 raise ValidationError('Unaccepted file type.')

#         return super().save_model(request, obj, form, change)


# admin.site.register(ChunkedUploadAdmin)
