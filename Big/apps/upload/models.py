from django.db import models
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.conf import settings

class fireVideo(models.Model):
    video = models.FileField(upload_to='fire/', storage=FileSystemStorage(location=settings.MEDIA_ROOT))
    result = models.JSONField(blank=True, null=True)
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.video.name
