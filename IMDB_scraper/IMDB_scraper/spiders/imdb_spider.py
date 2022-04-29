# to run
# scrapy crawl imdb_spider -o movies.cvs

import scrapy

class ImdbSpider(scrapy.Spider):
    name = "imdb_spider"

    start_urls = ["https://www.imdb.com/title/tt8324154/?ref_=fn_al_tt_2"]

    def parse(self, response):

        # find a url of "cast and crew page"
        cast_crew_page = response.css("div.ipc-title__wrapper a").attrib["href"]

        # connect start_urls and cast_crew_page 
        # to succeed to go to crew and cast page
        cast_crew_page = response.urljoin(cast_crew_page)

        # call "parse_full_credits" with "cast_crew_page" url
        yield scrapy.Request(cast_crew_page, callback=self.parse_full_credits)

    
    def parse_full_credits(self, response):
        
        # table.cast_list tr tag has actors names so separate them by for loop
        for cast in response.css("table.cast_list tr"):

            # call "a" tag here
            cast_page = cast.css("a")

            # if there is no page on the tag, skip and go next
            if (cast_page):
                cast_page = response.urljoin(cast_page.attrib["href"])

                # call "parse_actor_page" with "cast_page" which is 
                yield scrapy.Request(cast_page, callback=self.parse_actor_page)

    
    def parse_actor_page(self, response):

        # to get actor's name
        actor_name = response.css("div.name-overview-widget tr h1.header span.itemprop::text").get()

        if (not actor_name):
            # actor_page of actor who does not have picture on profile has 
            # a little bit different html code so write a code to get no-pic actor's name
            actor_name = response.css("div.no-pic-wrapper h1.header span.itemprop::text").get()

        # separate movie and TV name list with for loop then get text movie and TV names
        for movie_TV in response.css("div.filmo-category-section div"):
            movie_or_TV_name = movie_TV.css("b a::text").get()
            # check if there is "movie_or_TV_name"
            if (movie_or_TV_name):
                # make dict with yield
                yield {
                    "actor" : actor_name, 
                    "movie_or_TV_name" : movie_or_TV_name
                    }