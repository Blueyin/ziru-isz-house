import requests
from bs4 import BeautifulSoup


def get_html(url):
    # 模拟请求
    headers = {
	'User-Agent': 'Mozilla/5.0(Windows NT 6.1; WOW64)',
    }
    try:
        response = requests.get(url, headers=headers)
        html = response.text
        # 返回页面内容
        return html
    except:
        print('request error')
        pass

def get_ziru_hourse(html):
    # 解析为对象
    soup = BeautifulSoup(html, 'lxml')
    # 房源名字，地址，特点
    house_names = []
    house_urls = []
    spes = []
    links = soup.find('ul', id='houseList').find_all('a')
    spans = soup.find('ul', id='houseList').find_all('span')
    special = ''
    for span in spans:
        # 特点叠加获取
        special += (span.get_text()) + ' '
        # 匹配最后一个字段结束特点获取，并重置变量
        if '每月' in span.get_text():
            spes.append(special)
            special = ''

    for link in links:
        # 连接地址获取
        house_url = link.get('href')
        # 未带http的加上http
        if 'http' not in house_url:
            house_url = 'http:' + house_url
        if house_url not in house_urls and 'youjia_fbh' not in house_url:
            house_urls.append(house_url)
        house_name = link.get_text()
        # 名字匹配加入
        if '龙湖春江' in house_name:
            house_names.append(house_name)

    return zip(house_names, house_urls, spes)

def get_isz_hourse(html):
    # 解析为对象
    soup = BeautifulSoup(html, 'lxml')
    # 名字特点为一起，url单独获取
    house_names = []
    house_urls = []
    links = soup.find('div', class_='left').find_all('a')
    house_name = ''
    for link in links:
        # 获取房源名字和特征
        span = link.get_text()
        if '龙湖春江' in span:
            house_names.append(house_name)
            house_name = ''
        # 获取url
        house_url = link.get('href')
        house_name += span + ' '
        # 判断url是否正常
        if house_url is not None and house_url not in house_urls and '%E9%BE%99%E6%B9%96%E6%98%A5%E6%B1%9F' not in house_url:
            house_urls.append(house_url)
    # 删除第一个字段为空
    del house_names[0]
    return zip(house_names,house_urls)

if __name__=='__main__':
    url = 'http://hz.ziroom.com/z/nl/z3-d330108.html?qwd=%E9%BE%99%E6%B9%96%E6%98%A5%E6%B1%9F'
    html = get_html(url)
    houses = get_ziru_hourse(html)
    print('自如房子：')
    for house in houses:
         print(house[0], house[1], house[2])

    isz_url = 'http://www.ishangzu.com/zufang/?q=%E9%BE%99%E6%B9%96%E6%98%A5%E6%B1%9F'
    html = get_html(isz_url)
    houses = get_isz_hourse(html)
    print('爱上租房子：')
    for house in houses:
        print(house[0], house[1])

