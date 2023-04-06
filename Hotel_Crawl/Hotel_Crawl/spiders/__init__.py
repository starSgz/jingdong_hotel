# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import base64

import gvcode
import io
s, v = gvcode.generate() #序列解包
# print(s.verify())
# s.show() #显示生成的验证码图片
# 将图片转换为BytesIO对象
img_bytes_io = io.BytesIO()
s.save(img_bytes_io, format='PNG')
img_bytes_io.seek(0)

# 将BytesIO对象转换为base64编码的字符串
image_base64 = base64.b64encode(img_bytes_io.getvalue())
image_base64_str = image_base64.decode('utf-8')
print(image_base64_str)