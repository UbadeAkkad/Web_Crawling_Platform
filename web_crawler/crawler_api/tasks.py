from .crawler import crawl
from .utils import get_db_handle


def crawl_job_handeling(request_data, crawl_job):
    crawl_job.status = "ongoing"
    crawl_job.save()
    crawl_output = crawl(request_data["urls"],request_data["crawling_rules"])
    crawl_job.status = "done"
    crawl_job.save()

    get_db_handle().crawling_data.insert_one({"crawling_job_name": str(crawl_job.name),
                                              "crawling_job_ID": str(crawl_job.job_ID),
                                              "crawling_job_create": str(crawl_job.created),
                                              "crawl_job_input": request_data,
                                              "job_crawled_data": crawl_output})