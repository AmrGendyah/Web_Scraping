## Introduction

This script is used to scrap ,crawl ,and download images from [zillow](www.zillow.com) through API by using python and scrapy. 

## To run the script

1. Install [Python.](https://www.python.org/downloads/).
2. Open terminal , cd to file directory , and run command ``pip install -r requirements.txt``
3. in terminal run ``scrapy crawl zillow_houses``
   -To save crawled data as **csv** file run ``scrapy crawl zillow_houses-o "file_name".csv``
   -To save crawled data as **json** file run  ``scrapy crawl zillow_houses-o "file_name".json``
4. To run Gui app
   1. run ``python ./gui_app.py`` 

