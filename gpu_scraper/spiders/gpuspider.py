import scrapy

# based on https://github.com/jhnwr/whiskyspider

base_url = 'https://www.hardwareluxx.de'

threads = {
    'RTX 3050': base_url+'/community/threads/rtx-3050-gpu-verf%C3%BCgbarkeitshinweise.1312445/',
    'RTX 3060': base_url+'/community/threads/rtx-3060-gpu-verf%C3%BCgbarkeitshinweise.1292392/',
    'RTX 3060 Ti': base_url+'/community/threads/rtx-3060ti-gpu-verf%C3%BCgbarkeitshinweise.1284025',
    'RTX 3070': base_url+'/community/threads/rtx-3070-gpu-verf%C3%BCgbarkeitshinweise.1284024/',
    'RTX 3070 Ti': base_url+'/community/threads/rtx-3070ti-gpu-verf%C3%BCgbarkeitshinweise.1298653/',
    'RTX 3080': base_url+'/community/threads/rtx-3080-gpu-verf%C3%BCgbarkeitshinweise.1281755/',
    'RTX 3080 Ti': base_url+'/community/threads/rtx-3080ti-gpu-verf%C3%BCgbarkeitshinweise.1298309/',
    'RTX 3090': base_url+'/community/threads/rtx-3090-gpu-verf%C3%BCgbarkeitshinweise.1283956/'
}


class GPUSpider(scrapy.Spider):
    name = 'gpu'
    start_urls = threads.values()

    def parse(self, response):
        for post in response.css('article.message.message--post'):
            full_text = post.css('div.bbWrapper::text').get()
            if full_text is not None and 'Neue Verfügbarkeit entdeckt!' in full_text:
                name = post.css('div.bbWrapper').re_first(r'Name: (.*)<br>').strip()
                price = post.css('div.bbWrapper').re_first(r'Preis: (.*)<br>').replace('€', '').strip()
                shop = post.css('div.bbWrapper').re_first(r'Shop: (.*)<br>').strip()
                post_url = base_url + post.css('header_1 ul.message-attribution-main a').attrib['href']
                datetime = post.css('header_1 ul.message-attribution-main a time').attrib['datetime']
                post_number = post.css('header_1 ul.message-attribution-opposite li:last-child a::text').get().replace('#', '').strip()

                model = ''
                for thread_model, thread_url in threads.items():
                    if post_url.startswith(thread_url):
                        model = thread_model
                        break

                yield {
                    'model': model,
                    'name': name,
                    'price': price,
                    'shop': shop,
                    'datetime': datetime,
                    'number': post_number,
                    'url': post_url,
                }

        next_page = response.css('a.pageNav-jump.pageNav-jump--next')
        if len(next_page) > 0:
            yield response.follow(next_page.attrib['href'], callback=self.parse)
