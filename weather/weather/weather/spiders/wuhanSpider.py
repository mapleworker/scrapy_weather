import scrapy
from weather.items import WeatherItem
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
class Spider(CrawlSpider):
    name = 'weatherSpider'
    start_urls = [
        "http://www.weather.com.cn/weather1d/101020100.shtml?from=shanghai"
    ]
    rules = (

        Rule(LinkExtractor(allow=('http://www.weather.com.cn/weather1d/101\d{6}.shtml#around2')), follow=False,
             callback='parse_item'),
    )
    def parse_item(self, response):
        item = WeatherItem()
        item['city'] = response.xpath("//div[@class='crumbs fl']/a/text()").extract_first()
        city_addition = response.xpath("//div[@class='crumbs fl']/span[2]/text()").extract_first()
        if city_addition == '>':
            item['city_addition'] = response.xpath("//div[@class='crumbs fl']/a[2]/text()").extract_first()
        else:
            item['city_addition'] = response.xpath("//div[@class='crumbs fl']/span[2]/text()").extract_first()
        item['city_addition2'] = response.xpath("//ul[@class='clearfix city']/li[2]/a/span[1]/text()").extract_first()
        weatherData = response.xpath("//div[@class='today clearfix']/input[1]/@value").extract_first()
        item['data'] = weatherData[0:5]
        item['weather'] = response.xpath("//p[@class='wea']/text()").extract_first()
        item['temperatureMax'] = response.xpath(
            "//ul[@class='clearfix']/li[2]/p[@class='tem']/span[1]/text()").extract_first()
        item['temperatureMin'] = response.xpath(
            "//ul[@class='clearfix']/li[1]/p[@class='tem']/span[1]/text()").extract_first()
        yield item
