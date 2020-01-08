import  requests
from  lxml import  etree
from  pyquery import  PyQuery

#采集列表页面的url 并且返回url列表
def parse(response):
    r=response.text
    selector=etree.HTML(r)
    urls=selector.xpath('//li[@class="tli1"]/a/@href')
    result=[url   for url in urls]  #返回url或者单个类型的数据用列表
    print(result)

# 采集小区详情页的名称，放假，地址，建筑年代 返回dict字典数据类型
def xiaoqu_parse(response):
    r=response.text
    selector=etree.HTML(r)
    result=dict() #返回数据就用字典包裹
    result['name']=selector.xpath('//span[@class="title"]/text()')[0]
    result['reference_price']=selector.xpath('//span[@class="price"]/text()')[0]
    result['address']=selector.xpath('/html/body/div[2]/div[4]/div[2]/div[2]/table/tr[1]/td[4]/text()')[0].split()[0]
    result['times']=selector.xpath('/html/body/div[2]/div[4]/div[2]/div[2]/table/tr[5]/td[2]/text()')[0].split()[0]
    print(result)

def get_ershou_fang_list_parse(response):
    r=response.text
    selector=etree.HTML(r)
    result=list()
    trs=selector.xpath('//*[@id="infolist"]/div[2]/table/tr')
    for tr in trs:
        price_tag=tr.xpath('./td[@class="tc"]/b/text()')[0]
        result.append(price_tag)
    print(result)

def chuzu_list_detail_url(response):
    r=response.text
    selector=etree.HTML(r)
    urls=selector.xpath('//*[@id="infolist"]/div[2]/table/tr/td[2]/a[1]/@href')
    result=[url for url in urls]
    print(result)




if __name__ == '__main__':
    r=requests.get('http://cd.58.com/xiaoqu/')
    parse(r)
    r1 = requests.get('http://cd.58.com/xiaoqu/shenxianshudayuan/')
    # xiaoqu_parse(r1)

    r2=requests.get('http://cd.58.com/xiaoqu/shenxianshudayuan/ershoufang/')
    # get_ershou_fang_list_parse(r2)

    r3=requests.get('http://cd.58.com/xiaoqu/shenxianshudayuan/chuzu/')
    # chuzu_list_detail_url(r3)