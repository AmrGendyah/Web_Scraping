## Introduction

This script is used to scrap and crawl [steam](http://store.steampowered.com/search/?filter=topsellers) top seller by using python ,scrapy, scrapyrt, and Flask.

## To run the script

1. Install [Python.](https://www.python.org/downloads/).
2. Open terminal , cd to file directory , and run command ``pip install -r requirements.txt``
3. in terminal run ``scrapy crawl best_selling``
   -To save crawled data as **csv** file run ``scrapy crawl best_selling-o "file_name".csv``
   -To save crawled data as **json** file run  ``scrapy crawl best_selling-o "file_name".json``
4. To run web app
   1. in terminal run ``cd web``
   2. run python ./app.py

