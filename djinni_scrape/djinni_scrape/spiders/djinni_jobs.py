import scrapy


class DjinniJobsSpider(scrapy.Spider):
    name = "djinni_jobs"
    allowed_domains = ["djinni.co"]
    start_urls = ["https://djinni.co/jobs/keyword-python/"]

    def parse(self, response):
        pass
