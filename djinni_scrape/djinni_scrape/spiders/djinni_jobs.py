import csv
import json
import re
import time
import scrapy

class DjinniJobsSpider(scrapy.Spider):
    name = "djinni_jobs"
    allowed_domains = ["djinni.co"]

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'djinni.csv',
        'FEED_EXPORTERS': {
            'csv': 'scrapy.exporters.CsvItemExporter'
        },
        'FEED_EXPORT_KEYS': ['Job title', 'Experience', 'Technologies', 'Views', 'Salary'],
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def __init__(self, keyword='Python', **kwargs):
        super().__init__(**kwargs)
        self.keyword = keyword

    def start_requests(self):
        url = f"https://djinni.co/jobs/?primary_keyword={self.keyword}"
        yield scrapy.Request(url=url, callback=self.parse_job_list)

    def parse_job_list(self, response):
        job_links = response.css('div.list-jobs__title a.profile::attr(href)').getall()
        for job_link in job_links:
            yield response.follow(job_link, callback=self.parse_job_details)
            time.sleep(1)

        next_page_links = response.css('ul.pagination_with_numbers li.page-item:not(.active) a.page-link::attr(href)').getall()
        for next_page_link in next_page_links:
            yield response.follow(next_page_link, callback=self.parse_job_list)

    def parse_job_details(self, response):
        job_title = response.css('div.detail--title-wrapper h1::text').get().strip()

        additional_info = response.xpath(
            '//div[contains(@class, "card job-additional-info")]/ul[@class="job-additional-info--body"][1]/li/div[contains(@class, "job-additional-info--item-text")]/text()'
        ).getall()
        additional_info = [info.strip() for info in additional_info if info.strip()]

        experience = None
        for info in additional_info:
            match = re.search(r'(\d+) роки', info)
            if match:
                experience = int(match.group(1))
                break

        technologies = response.xpath(
            '//div[contains(@class, "card job-additional-info")]/ul[@class="job-additional-info--body"][1]/li[contains(@class, "job-additional-info--item")]/div[contains(@class, "job-additional-info--item-text")]/span/text()'
        ).getall()
        technologies = [tech.strip() for tech in technologies if tech.strip()]

        views = response.xpath(
            '//div[@class="mb-4 text-small" and p[@class="text-muted"]]//span[contains(@class, "bi-eye")]/following-sibling::text()'
        ).get()
        views = int(re.search(r'(\d+)', views).group(1)) if views else None

        salary = response.xpath('//h1/span[@class="public-salary-item"]/text()').get()
        if salary:
            salary_range = re.findall(r'\d+', salary)
            if salary_range:
                salary_values = [int(value) for value in salary_range]
                min_salary = min(salary_values)
                max_salary = max(salary_values)
            else:
                min_salary = max_salary = None
        else:
            min_salary = max_salary = None

        yield {
            'Job title': job_title,
            'Experience': experience,
            'Technologies': ', '.join(technologies) if technologies else [],
            'Views': views,
            'Salary': {'Min': min_salary, 'Max': max_salary}
        }

    def closed(self, reason):
        if reason != 'finished':
            raise scrapy.exceptions.CloseSpider('Spider closed unexpectedly')

        # Read the CSV file and update the index column
        with open('djinni.csv', 'r', newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # Convert the 'Salary' values to JSON strings
        for row in rows:
            salary = row['Salary']
            if salary and salary != 'None':
                salary_dict = ast.literal_eval(salary)
                row['Salary'] = json.dumps(salary_dict)

        # Create headers manually
        headers = ['Job title', 'Experience', 'Technologies', 'Views', 'Salary']

        # Write the headers and rows back to the CSV file
        with open('djinni.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
