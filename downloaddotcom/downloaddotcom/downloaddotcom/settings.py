# Scrapy settings for downloaddotcom project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'downloaddotcom'

SPIDER_MODULES = ['downloaddotcom.spiders']
NEWSPIDER_MODULE = 'downloaddotcom.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'downloaddotcom (+http://www.yourdomain.com)'

WEBSERVICE_ENABLED = False
TELNETCONSOLE_ENABLED  = False

CONCURRENT_REQUESTS = 50
DOWNLOAD_TIMEOUT = 80


DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 500,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'downloaddotcom.proxymiddle.ProxyMiddleware': 100,
}

