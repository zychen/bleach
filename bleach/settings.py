# -*- coding: utf-8 -*-

# Scrapy settings for bleach project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'bleach'

SPIDER_MODULES = ['bleach.spiders']
NEWSPIDER_MODULE = 'bleach.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'bleach (+http://www.yourdomain.com)'

# 设置代理
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'bleach.middlewares.ProxyMiddleware': 100,
}

# 下载图片
ITEM_PIPELINES = {
    # 'scrapy.contrib.pipeline.images.ImagesPipeline': 1
    'bleach.pipelines.BleachPipeline'
}
# 下载图片存储位置
IMAGES_STORE = 'e:\\PythonCode\\bleach\\bleach\\images\\op'

# 访问页面延时
DOWNLOAD_DELAY = 3
# 将访问页面延时时间设置成随机，随机值=random(0.5, 1.5) * DOWNLOAD_DELAY
RANDOMIZE_DOWNLOAD_DELAY = True

