#from urllib.parse import urlparse
from urllib.request import urlopen, Request, quote
from html.parser import HTMLParser
import sys

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global dataType
        if tag == 'a':
            href = dict(attrs).get('href')
            if href == None:
                return
            elif href.startswith('/'):
                link = urlDomain + href
            elif href.startswith(urlDomain):
                link = href
            else:
                return
            if link not in allLinks:
                allLinks.add(link)
                linksStack.append(link)
        if tag == 'title':
            dataType = 'title'
        if tag == 'div':
            clas = dict(attrs).get('class')
            if clas == None:
                return
            if clas.find('productName') != -1:
                dataType = 'productName'
    def handle_data(self, data):
        global dataType, pageTitle, productName
        if dataType == '':
            return
        if dataType == 'title':
            pageTitle = data
        elif dataType == 'productName':
            productName = data
        dataType = ''


myParser = MyHTMLParser()
urlDomain = 'http://www.epocacosmeticos.com.br'
lenUrlDomain = len(urlDomain)
allLinks = {urlDomain}
linksStack = [urlDomain]

dataType = ''
pageTitle = ''
productName = ''

csvFile = open('products.csv', 'w')

while linksStack:
    url = linksStack.pop()
    try:
        req = Request(url=urlDomain+quote(url[lenUrlDomain:]))
        response = urlopen(req)
        html = response.read().decode('utf-8', 'ignore')
        myParser.feed(html)
        if pageTitle != '' and productName != '':
            csvFile.write(productName + '\t' + pageTitle + '\t' + url + '\n')
        dataType = ''
        pageTitle = ''
        productName = ''
    except Exception as e:
        print("Erro ao acessar a url:", url)
