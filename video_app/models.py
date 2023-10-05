"""This module defines class Subtitle."""
from django.db import models
from chunked_upload.models import ChunkedUpload


class Subtitle(models.Model):
    """This model defines the columns of the subtitles table."""
    Subtitle = models.TextField()
    video = models.ForeignKey(ChunkedUpload, on_delete=models.CASCADE,
                              related_name='video_subtitles')

    class Meta:
        """db_table: Defines the name of the table in the database."""
        db_table = 'subtitles'

    def __str__(self):
        """Returns a string representation of the instance of the class."""
        # pylint: disable=no-member
        return f'{self.id}'

