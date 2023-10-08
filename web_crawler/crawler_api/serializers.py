from rest_framework import serializers
from .models import Crawl_Job

class Crawl_Job_serializer(serializers.ModelSerializer):
    class Meta:
        model = Crawl_Job
        fields = ("name", "job_ID","created","status")
