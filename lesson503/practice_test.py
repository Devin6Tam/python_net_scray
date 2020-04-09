#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 23:33
# @Author  : tanxw
# @Desc    : 下载缓存练习示例

import re
import urllib.parse
import zlib

url = 'http://example.webscraping.com/places/default/view/Aland-Islands-2'
content = re.sub(r'[^/0-9a-zA-z\-.,;_]', '_', url)
print(content)



"""
还有一种边界情况需要考虑，那就是URL 路径可能会以斜杠(/)结尾，
此时斜杠后面的空字符串就会成为一个非法的文件名。但是，如果移除这个
斜杠，使用其父字符串作为文件名，又会造成无法保存其他URL的问题。考
虑下面这两个URL：
http://example.webscraping.com/index/
http://example.webscraping.com/index/1

如果我们希望这两个URL都能保存下来，就需要以index作为目录名，
以1作为子路径。对于像第一个URL路径这样以斜杠结尾的情况，这里使用
的解决方案是添加index.html作为其文件名。同样地，当URL路径为空
时也进行相同的操作。为了解析URL，我们需要使用urlparse.urlsplit()
函数，将URL分割成几个部分。
"""
components = urllib.parse.urlsplit(url)
print(components)
print(components.path)

# 该函数提供了解析和处理URL的便捷接口。下面是使用该模块对上述边
# 界情况添加index.html的示例代码。
path = components.path
if not path:
    path = "/index.html"
elif path.endswith('/'):
    path += 'index.html'
    filename = components.netloc + path + components.query
    print(filename)
print(path)

# 文件名及其父目录的长度需要限制在255个字符以内(实现代码如下),以满足表3.1中给出的长度限制。
# filename = '/'.join(segment[:255] for segment in filename.split('/'))

# zlib.compress(pickle.dumps(result))

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
url = 'http://example.webscraping.com/places/default/view/Andorra-6'
html = '...'
db = client['python_practice']
col = db['sites']
print(db)
print(col)


# insertResult = col.insert_one({'url': url, 'html': html})
# print(insertResult.inserted_id)
# searchResult = col.find_one({'url': url})
# print(searchResult)
# insertResult = col.insert_one({'url': url, 'html': html})
# print(insertResult.inserted_id)
# 上面的例子存在一个问题，那就是如果我们对相同的URL插入另一条不同
# 的文档时，MongoDB会欣然接受并执行这次插入操作，其执行过程如下所示。
count = col.count_documents({'url': url})  #col.find({'url': url}).count() 改方法已废弃
print(count)

# 此时，同一URL下出现了多条记录，但我们只关心最新存储的那条数据。
# 为了避免重复，我们将ID设置为URL，并执行upsert操作该操作表示
# 当记录存在时更新记录，否则插入新记录，其代码如下所示。

# col.update_one({'url': url}, {'$set': {'html': html}})
# searchResult = col.find_one({'url': url})
# print(searchResult)
# 现在，当我们尝试向同一URL插入记录时，将会更新其内容，而不是创
# 建冗余的数据，如下面的代码所示。
new_html = '<html></html>'
updateResult = col.update_one({'url': url}, {'$set': {'html': new_html}}, upsert=True)
print(updateResult.modified_count)
searchResult = col.find_one({'url': url})
print(searchResult)
col.count_documents({'url': url})

col.drop()
# 可以看出，在添加了这条记录之后，虽然HTML 的内容更新了，但该URL的记录数仍然是1 。

