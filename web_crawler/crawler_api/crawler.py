import requests
from bs4 import BeautifulSoup
import urllib3
from concurrent.futures import ThreadPoolExecutor
import copy

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def crawl(urls,crawling_rules):
    obj = {
            "url": "",
            "response_code" : "",
            "crawled_objects" : [],
        }
    sub_obj = {
        "content_tag" : "",
        "tag_attributes" : {},
        "text": ""
    }
    def send_request(url):
        new_obj = copy.deepcopy(obj)
        new_obj["url"] = url
        try:
            response = requests.get(url=url, timeout=20, verify=False,
                                    headers={"User-Agent" : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0"} )
            new_obj["response_code"] = response.status_code
            if (new_obj["response_code"]) not in (400,401,402,403,404,500):
                soup = BeautifulSoup(response.content, "html.parser")
                for rule in crawling_rules:
                    try:
                        new_sub_obj = copy.deepcopy(sub_obj)
                        content_tag = rule["content_tag"]
                        tag_attr = rule["tag_attr"]
                        new_sub_obj["content_tag"] = content_tag
                        new_sub_obj["tag_attributes"] = tag_attr
                        text = soup.find(content_tag,tag_attr).text
                        new_sub_obj["text"] = text
                    except:
                        pass
                    new_obj["crawled_objects"].append(new_sub_obj)
            return new_obj
        except:
            return new_obj
    with ThreadPoolExecutor(max_workers=5) as t_pool:
        thread_responses = list(t_pool.map(send_request,urls))
    return thread_responses
