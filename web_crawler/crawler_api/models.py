from django.db import models
import uuid

class Crawl_Job(models.Model):
    job_ID = models.CharField(max_length=32, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, default="ongoing")