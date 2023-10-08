from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
import json
from .models import Crawl_Job
from django.shortcuts import get_object_or_404
from .serializers import Crawl_Job_serializer
from .utils import get_db_handle
import django_rq
from .tasks import crawl_job_handeling

class CrawlRequest(GenericAPIView):
    serializer_class = (Crawl_Job_serializer,)
    
    def post(self, request, *args, **kwargs):
        queue = django_rq.get_queue('default', default_timeout=800)
        re_id_parameter = request.query_params.get('re_id') or ''
        if re_id_parameter:
            old_crawl_job = get_db_handle().crawling_data.find_one({"crawling_job_ID": re_id_parameter})
            new_crawl_job = Crawl_Job.objects.create(status="pending", name=f"{old_crawl_job['crawling_job_name']}_rerun")
            queue.enqueue(crawl_job_handeling, args=(old_crawl_job["crawl_job_input"],new_crawl_job))
            return Response({"crawling_job_ID" : new_crawl_job.job_ID})
        else:
            rq_body = json.loads(request.body)
            crawl_job = Crawl_Job.objects.create(status="pending", name=rq_body["name"])
            queue.enqueue(crawl_job_handeling, args=(rq_body,crawl_job))
            return Response({"crawling_job_ID" : crawl_job.job_ID})

    def get(self, request, *args, **kwargs):
        serialized_jobs = Crawl_Job_serializer(Crawl_Job.objects.order_by("-created"), many=True)
        return Response(serialized_jobs.data)
        
    def delete(self,request, *args, **kwargs):
        try:
            job_id = json.loads(request.body)["id"]
            get_db_handle().crawling_data.delete_one({"crawling_job_ID": job_id})
            get_object_or_404(Crawl_Job, job_ID=job_id).delete()
            return Response(f"Job {job_id} was deleted successfully")
        except:
            return Response("An error occured, check the sent ID!")

class MongoCrawlJobs(GenericAPIView):

    def get(self, request, *args, **kwargs):
        id_parameter = request.query_params.get('id') or ''
        if id_parameter:
            crawl_job = get_db_handle().crawling_data.find_one({"crawling_job_ID": id_parameter})
            return Response({"crawling_job_name": crawl_job["crawling_job_name"],
                             "crawl_job_ID" : crawl_job["crawling_job_ID"],
                             "job_creation_date" : crawl_job["crawling_job_create"],
                             "crawl_job_input" : crawl_job["crawl_job_input"],
                             "crawled_objects" : crawl_job["job_crawled_data"]})
        else:
            crawl_jobs = get_db_handle().crawling_data.find({},{"_id": 0, "job_crawled_data": 0, "crawl_job_input": 0})
            return Response(list(crawl_jobs))
