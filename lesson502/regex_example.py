#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 20:54
# @Author  : tanxw
# @Desc    : regex 抓取数据示例

import re
import lesson502.common_download

def scrape(html):
    # area = re.findall('<tr id="places_area__row">.*?<td\s*class=["\']w2p_fw["\']>(.*?)</td>', html.decode("utf8"))[0]
    area = re.findall('<tr id="places_area__row"><td class="w2p_fl"><label class="readonly" for="places_area" id="places_area__label">Area: </label></td><td class="w2p_fw">(.*?)</td>', html.decode("utf8"))
    return area


if __name__ == '__main__':
    html = lesson502.common_download.download('http://example.webscraping.com/places/default/view/Aland-Islands-2')
    print(scrape(html))