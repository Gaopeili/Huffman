import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import tkinter as tk
from selenium import webdriver

__author__ = "GPL"

class Node():
    '''
    :param weight 节点的权重
    '''
    def __init__(self,weight,string = None):
        self.string = string
        self.weight = weight
        self.lchild = None
        self.rchild = None

class Spider():
    '''
    从网上爬取某一文章存入到文件中，并且计算文件中每个字符出现的频率作为字符的权重
    '''
    def __init__(self,url):
        self.url = url
        self.text = None

    '''
    将爬取的文章保存到文件中
    '''
    def save2file(self):
        # 调用getHTML来更新self.text
        self.getHTML()
        # 做一锅汤
        soup = BeautifulSoup(self.text,'html.parser')
        elements = soup.find_all('div',attrs={'class':"chapter-lan-en toleft"})
        with open("huffman.txt",'a+',encoding='utf-8') as file:
            for element in elements:
                for temp in element.find_all('p'):
                    file.write(temp.text)
    
    def getHTML(self):
        for i in range(1975,2003):
            url = self.url + str(i)+".html"
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
                }
                # 响应
                response = requests.get(url,headers = headers)
                # 发起错误
                response.raise_for_status()
                print(response.status_code)
                # 更新编码
                response.encoding = response.apparent_encoding
                # 更新self.text
                if not self.text:
                    self.text = response.text
                else:
                    self.text+=response.text
            except :
                print("Error")


    def calculate_weight(self):
        '''
        :return: 从简爱中得到字符的权重并返回
        '''
        # 初始化列表ASCII码从0-128
        lst = [(chr(i),0) for i in range(0,129)]
        # 打开爬取的文件
        with open("huffman.txt",'r') as file:
            # 读取所有行
            lines = file.readlines()

        # 每一行
        for line in lines[:100]:
            # 构建权重元组列表
            for index in range(0, 129):
                # 新值等于原值再加当前行该元素的个数
                lst[index] = (chr(index), lst[index][1] + line.count(chr(index)))
        # 返回权重表
        return lst

class HuffmanTree():

    def __init__(self,lst):
        self.root = None
        self.tree = None
        self.lst = lst
        self.array = []
        self.code = []

    def createTree(self):
        '''
        :param lst:元素为tuple的列表，其中每个tuple元素的第一位为string,第二位为weight
        :return:
        '''
        
        # 将lst转化为叶子节点并且存入到self.tree中
        self.tree = [Node(i[1],i[0]) for i in self.lst]
        # 只剩下根节点之前一直遍历
        while len(self.tree) > 1:
            # 每次都需要按照weight从大到小排序
            self.tree.sort(reverse=True, key=lambda node:node.weight)
            # 把最后一个弹出去
            _left = self.tree.pop()
            # 倒数第二个弹出去
            _right = self.tree.pop()
            # 创建新的连接节点
            parent = Node(_left.weight + _right.weight)
            # 左孩子是较小的那个
            parent.lchild = _left
            # 右孩子是较大的那个
            parent.rchild = _right
            # 加入新节点
            self.tree.append(parent)
        # 更新根节点
        self.root = self.tree[0]

    def get_encode(self,node):
        temp = node
        # 如果是叶子节点
        if temp.string :
            # 打印编码
            print(temp.string+'的编码为',self.array)
            # 将array中的数据以及对应的字符传入到code中并且记录下来
            self.code.append((temp.string,self.array[:]))
            # 记录完后将array最后一个元素弹出并返回
            self.array.pop()
            return

        # 如果不是叶子节点，由于二叉树中没有度为1的节点所以除叶子节点之外都有左右孩子
        # 首先将0加入到array中
        self.array.append(0)
        # 然后递归调用左子树
        self.get_encode(temp.lchild)
        # 调用外左子树之后，array又回复到原来的状态，所以将1加入到右子树
        self.array.append(1)
        # 递归调用右子树
        self.get_encode(temp.rchild)
        # 左右子树调用完之后，这个节点的任务已经完成，需要把当前节点的值弹出
        if len(self.array):
            self.array.pop()

    def encoding(self,string):
        '''
        :param string:将要编码的字符串
        '''
        # lst是即将返回的列表
        lst = []
        # 创建Huffman树
        self.createTree()
        # 获取编码并且存入到code中
        self.get_encode(self.root)
        # 遍历字符串并且为每个字符编码
        for i in string:
            j = 0
            while self.code[j][0] != i:
                j+=1
                if j==len(self.code):
                    break
            # 以列表形式打印出结果
            if j<len(self.code):
                for number in self.code[j][1]:
                    print(number,end='',sep=' ')
                    lst.append(str(number))
        print('\n')
        return lst

    def decoding(self,string):
        '''
        :param string: 将要解码的用数字字符形成的字符串
        '''

        # 如果二叉树的根为空，那么创建二叉树
        if not self.root:
            self.createTree()
        root = self.root
        # 返回的字符串
        lst = ''
        # 求解字符串
        for i in string:
            i = int(i)
            # i为0则往左遍历
            if i==0:
                if root.lchild.string:
                    lst+=root.lchild.string
                    print(root.lchild.string)
                    root = self.root
                else :
                    root = root.lchild
            # i为1则往右遍历
            elif i ==1:
                if root.rchild.string:
                    lst+=root.rchild.string
                    print(root.rchild.string)
                    root = self.root
                else:
                    root = root.rchild
        # 返回求得的字符串
        return lst



















