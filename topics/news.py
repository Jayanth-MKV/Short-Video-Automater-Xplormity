import json
import logging

import requests

from util.const import LOG_PATH, NEWS_FETCH_LIMIT,BRANDS
from util.files import save_json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename=LOG_PATH)


class NEWS:
    def __init__(self, news_url):
        self.news_fetch_limit = NEWS_FETCH_LIMIT
        self.url = news_url
        self.results=[]
        self.nextPage=""

    def loadNextPage(self,url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            response_data = response.json()
            # logging.info(f"news_response: {response_data}")
            response_business = response_data["results"]
            self.results=response_business
            self.nextPage=response_data.get("nextPage")
            logging.info("API request successful. Retrieved {} business news articles.".format(len(response_business)))
            # return response_business
        except requests.exceptions.RequestException as e:
            logging.error("API request failed: {}".format(str(e)))

    def getnews(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            response_data = response.json()
            # logging.info(f"news_response: {response_data}")
            response_business = response_data["results"]
            self.results=response_business
            self.nextPage=response_data.get("nextPage")
            logging.info("API request successful. Retrieved {} business news articles.".format(len(response_business)))
            # return response_business
        except requests.exceptions.RequestException as e:
            logging.error("API request failed: {}".format(str(e)))

    def logNews(self,outputfile):
        # logging.info(f"news_response: {news_response}")
        logging.info(f"fetched article length news_response: {len(self.results)}")
        res=[]
        titles_set=set()
        while len(res)<20:
            for article in self.results:
                title = article.get("title")
                if title in titles_set:
                    continue
                titles_set.add(title)
                if any(brand.lower() in title.lower() for brand in BRANDS):
                    continue
                description = article.get("description",None)
                if not description:
                    continue
                link = article.get("url")
                category = article.get("category")
                keywords = article.get("keywords")
                # logging.info(
                #     f"{{title:{title}, description :{description}, link :{link}, category :{category},keywords :{keywords}}}")
                data ={
                    "index":len(res),
                    "title":title,
                    "description":description,
                    "link":link,
                    "category":category,
                    "keywords":keywords
                }
                res.append(data)

            url = f"{self.url}&page={self.nextPage}"
            self.loadNextPage(url)


        save_json(outputfile,res)


    