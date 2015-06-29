# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem
from cStringIO import StringIO
from PIL import Image
from scrapy.contrib.pipeline.images import ImageException


class BleachPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        # 图片扩展名
        image_ext = request.url.split('.')[-1]
        image_path = request.meta['image_path']
        image_full_name = image_path + '.' + image_ext
        return image_full_name

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            image_path = item['name'] + '/' + item['image_name']
            yield Request(image_url, meta={'image_path': image_path})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item

    def get_images(self, response, request, info):
        """重写ImagesPipeline.get_images
        ImagesPipeline会将所有图片都转换为jpg格式，
        改写后即保存原始下载的图片
        重写get_images的内容几乎和ImagesPipeline.get_images一样，
        只是在self.convert_image返回buf（已经转换格式的图片数据）后，
        将buf内容换成原始图片信息；response.body
        """
        path = self.file_path(request, response=response, info=info)
        orig_image = Image.open(StringIO(response.body))

        width, height = orig_image.size
        if width < self.MIN_WIDTH or height < self.MIN_HEIGHT:
            raise ImageException("Image too small (%dx%d < %dx%d)" %
                                 (width, height, self.MIN_WIDTH, self.MIN_HEIGHT))

        image, buf = self.convert_image(orig_image)

        # 将buf内容换成原始图片信息
        # buf = StringIO(response.body)
        yield path, image, buf

        for thumb_id, size in self.THUMBS.iteritems():
            thumb_path = self.thumb_path(request, thumb_id, response=response, info=info)
            thumb_image, thumb_buf = self.convert_image(image, size)
            yield thumb_path, thumb_image, thumb_buf




