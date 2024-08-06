from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    thumbnail_url = models.URLField()
    file_path = models.CharField(max_length=255)

    def __str__(self):
        return self.title