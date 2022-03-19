import datetime

import scrapy


class GrantsSpider(scrapy.Spider):
    name = "GrantsSpider"
    start_urls = [
        'https://www.narodniprogramzp.cz/nabidka-dotaci/',
    ]
    available_domains = ['narodniprogramzp.cz']

    def parse(self, response):
        for grant_href in response.css('div.row header.news__header a::attr(href)').getall():
            yield response.follow(grant_href, callback=self.parse_grant)

    def parse_grant(self, response):
        start_end_date = str(response.css('div span.info-content::text').get()).strip().split('-')
        receivers = str(response.css('div.challenge__description ul:nth-child(4) li::text').getall().encode('utf-8'))
        supported_activities = str(response.css('div.challenge__description ul:nth-child(2) li::text').getall())
        support_form = str(response.css('div span:nth-child(4)::text').get())
        doc_names = response.css('div.challenge__description ul:first-child li a::text').getall()
        doc_hrefs = response.css('div.challenge__description ul:last-child li a:nth-child(2)::attr(href)').getall()
        for description in response.css("body"):
            yield {
                'headline': description.css('h1.entry-title span.title::text').get(),
                'description': description.css('div.font-italic::text').get(),
                'retrieved_at': datetime.datetime.now(),
                'domain': self.available_domains[0],
                'link': response.url,
                'program': None,
                'start_date': start_end_date[0],
                'deadline_date': start_end_date[1],
                'receivers': receivers,
                'supported_activities': supported_activities,
                'support_form': support_form,
                'documents': list(map(lambda x, y: {'url': x, 'name': y},
                                      doc_hrefs, doc_names))
            }
