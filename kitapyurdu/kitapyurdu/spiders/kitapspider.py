import scrapy

class KitapSpider(scrapy.Spider):
    name = 'kitapyurdu'
    start_urls = ['https://www.kitapyurdu.com/index.php?route=product/category&filter_category_all=true&path=1&filter_in_stock=1&sort=purchased_365&order=DESC&limit=100']

    def parse(self, response):
        for products in response.css('div.product-cr'):
            
            try:
                listing_price = float(products.css('div.price-old > span.value::text').extract()[0].replace(',','.').strip())
                price = float(products.css('div.price-new > span.value::text').extract()[0].replace(',','.').strip())
                info = products.css('div.product-info::text').extract()[0].split('|')
                isbn = info[0].strip()
                lang = info[1].strip()
                page = info[2].strip()
                cover = info[3].strip()
            except:
                page = "error"

            if page.isdigit():
                yield {
                    'name': products.css('div.name > a::attr(title)').extract(),
                    'author': products.css('div.author > span > a > span::text').extract(),
                    'page' : page,
                    'cover' : cover,
                    'publisher' : products.css('div.publisher > span > a > span::text').extract(),
                    'lang' : lang,
                    'price': price,
                    'listing_price': listing_price,
                    'discount' : round(1-(price/listing_price),2),
                    'isbn' : isbn,
                    'link' : products.css('div.name > a::attr(href)').extract(),
                }


        next_page = response.css('a.next').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
            


