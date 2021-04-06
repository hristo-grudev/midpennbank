import scrapy

from scrapy.loader import ItemLoader

from ..items import MidpennbankItem
from itemloaders.processors import TakeFirst


class MidpennbankSpider(scrapy.Spider):
	name = 'midpennbank'
	start_urls = ['https://midpennbank.com/about-us/blog/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="link--read-more"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@rel="next"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//div[@class="main-content"]/h2/text()').get()
		description = response.xpath('//div[@class="main-content"]//text()[normalize-space() and not(ancestor::h1 | ancestor::h2 | ancestor::div[@class="meta"])]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="meta"]/text()').get()

		item = ItemLoader(item=MidpennbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
