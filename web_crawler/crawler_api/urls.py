from django.urls import path
from .views import CrawlRequest, MongoCrawlJobs

urlpatterns = [
    path("crawler", CrawlRequest.as_view()),
    path("mongo_crawljobs", MongoCrawlJobs.as_view()),
]
