# -*- coding:utf-8 -*-
# __author__ = 'robin'
import urllib2
import re


# 1、语句不用分号
# 2、函数定义不用大括号，直接冒号
# 3、命名习惯同java
# 4、每个函数的第一个参数为self，对于其他的成变，不用传入了！！！key
# 5、行参中有self，实参中没有
class QSBK:
    #类的成变放在初始化方法中
    def __init__(self):

        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}

        self.itemIndex=0
        self.pageIndex=1
        self.itemQueue=[]
        self.isContine=False

    def getPage(self):
        url = 'http://www.qiushibaike.com/8hr/page/' + str(self.pageIndex)
        try:
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            pageCode=response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError,e:
            print u"连接糗事百科失败，错误原因",e.reason
            return None

    def getPageItem(self):
        content=self.getPage();
        if not content:
            print u"页面加载失败"
            return None
        pattern = re.compile('<div.*?author.*?<a.*?href.*?<h2>(.*?)</h2>.*?'
                             + '<a.*?href.*?<div.*?content">.*?<span>(.*?)</span>.*?'
                             + '<div.*?stats.*?span.*?stats-vote.*?<i.*?number">(.*?)</i>.*?'
                             + '<span.*?stats-comments.*?a.*?href.*?<i.*?number">(.*?)</i>.*?'
                             + 'div.*?single-clear.*?</div>(.*?)</div>'
                             , re.S)
        items = re.findall(pattern, content)
        stories=[]
        for item in items:
            story = []
            story.append(item[0].strip())
            story.append(item[1].strip())
            story.append(item[2].strip())
            story.append(item[3].strip())
            haveComment = re.search("cmt-name", item[4])
            if haveComment:
                pat = re.compile('<a.*?href.*?div.*?cmtMain.*?span.*?cmt-name">(.*?)</span>.*?'
                                 + '<div.*?main-text">(.*?)<div', re.S);
                ites = re.findall(pat, item[4])
                for ite in ites:
                    story.append(ite[0].strip())
                    story.append(ite[1].strip())
            stories.append(story)

        return stories

    def loadPage(self):
        if self.isContine==True:
            if len(self.itemQueue)<2:
                list=self.getPageItem()
                if list:
                    self.itemQueue.append(list)
                    self.pageIndex+=1

    def getOneItem(self):
        for item in self.itemQueue:

            self.loadPage()

            for ite in item:
                input = raw_input()
                if input == 'q':
                    self.isContine = False
                    return

                print u"第%d页,第%d条" %(self.pageIndex-2,self.itemIndex+1)
                print u"发布者：%s" %(ite[0])
                print u"发布内容：%s" % (ite[1])
                print u"赞：%s" %(ite[2])
                print u"评论：%s" %(ite[3])

                if len(ite)>4:
                    print u"评论者:%s" %(ite[4])
                    print u"评论内容:%s" % (ite[5])
                print u"-----------------------------"
                self.itemIndex += 1
    def action(self):
        print u"正在读取段子，按回车查看下一个，q退出"
        self.isContine=True
        self.loadPage()
        while self.isContine:
            self.getOneItem()

qsbk=QSBK()
qsbk.action()