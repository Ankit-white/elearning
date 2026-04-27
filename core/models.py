from django.db import models
from cloudinary.models import CloudinaryField

class File(models.Model):
    title = models.CharField(max_length=100)
    file = CloudinaryField('file', resource_type='auto')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title