from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

import scrapy

# item models
from locanto.items import LocantoItemSearch, LocantoItemDetail

class LocantoSpider(CrawlSpider):

    name = "locanto"
    allowed_domains = ["locanto.com"]
    start_urls = [
        "http://sanfrancisco.locanto.com/Musical-Instruments/415/1/"
    ]

    rules = (
        # Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="button next"]',)), follow = True),
        # //a/strong[contains(text(), 'Next >')]/../@href"
        Rule(LinkExtractor(allow=(), restrict_xpaths=("//a/strong[contains(text(), 'Next >')]/../.",)), callback="parse_search_results", follow = True),
    )


    def parse_search_results(self, response):

        # Select parent elements containing each search result
        search_results = response.xpath("//div[@class='resultMain']")

        # Iterate through each "item" in the search results
        for row in search_results:

            # Extend this extracted dictionary with new items
            extracted = {
                "title":    row.xpath(".//span[@class='textHeader']/text()").extract(),
                "location": row.xpath(".//span[@class='textLoc']/text()").extract(),
                "description": row.xpath(".//span/text()").extract()
                #"price": row.xpath(".//strong/text()").extract()
            }

            # Intiailize a new row item with our predifed model
            # (Dont forget to update this in items.py for capturing new elements!)
            search_item =   LocantoItemSearch()

            # Check that our extracted entities are not empty
            for entity, extracted in extracted.items():
                
                if len(extracted) > 0:
                    # if not, extract the first item (expecting single list entities)
                    print "extracted: ", entity, "value: ", extracted[0]
                    search_item[entity] = extracted[0]

            yield search_item