__author__ = "GPL"

import tkinter as tk
from tree import *
import re

def main():
    # lst用来存放字符以及权重
    lst = []
    # huffman是huffmanTree的实例
    huffman = None

    def weight():
        '''
        :return 从键盘输入字符以及权重
        '''

        nonlocal lst
        if input("您是输入字符串还是从文件中读取(input/file)\n") == 'input':
            # 如果lst为空则直接从键盘输入并建树
            if not lst:
                a = input("请输入字符和响应的权重(用~隔开,quit退出)\n")
                while a != "quit":
                    string,interger = a.split(sep='~')
                    interger = int(interger)
                    lst.append((string,interger))
                    a = input("请输入字符和响应的权重(用~隔开,quit退出)\n")
            # 如果lst不为空,引导用户是否覆盖原树
            else :
                answer = input("权重列表已经存在,是否将其覆盖?(y/n)\n")
                # 如果覆盖则将lst设置为空
                if answer == 'y':
                    lst = []
                a = input("请输入字符和响应的权重(用~隔开,quit退出)\n")
                while a != "quit":
                    string, interger = a.split(sep='~')
                    interger = int(interger)
                    lst.append((string, interger))
                    a = input("请输入字符和响应的权重(用~隔开,quit退出)\n")
        else:
            # 输入文件名
            filename = input("请输入文件名\n")
            # 打开文件
            with open(filename, 'r') as file:
                # 读出字符串
                tmp = file.read()
                # 分隔开文件
                pattern = re.compile(r'.\d+', re.S)
                # 得到一个列表
                result = re.findall(pattern, tmp)
                # 新模式串
                pattern = re.compile(r'(\D)(\d+)')
                # 如果lst为空，直接创建lst
                if not lst:
                    # 将元组加入到lst中
                    for i in result:
                        lst.append(re.search(pattern, i).groups())
                    for i in range(len(lst)):
                        lst[i] = (lst[i][0],int(lst[i][1]))
                else:
                    answer = input("权重列表已经存在,是否将其覆盖?(y/n)\n")
                    # 如果覆盖则将lst设置为空
                    if answer == 'y':
                        lst = []
                    # 将元组加入到lst中
                    for i in result:
                        lst.append(re.search(pattern, i).groups())

                    for i in range(len(lst)):
                        lst[i] = (lst[i][0], int(lst[i][1]))
        print("创建权重列表成功!\n")

    def spider():
        '''
        :return 爬取简爱,将得到的结果返回并建立Huffman树
        '''
        nonlocal lst
        # 这里以简爱整本书为准
        spider = Spider("https://www.24en.com/novel/classics/jane-eyre/")
        # 从简爱返回的权重
        lst = spider.calculate_weight()
        print("创建权重列表成功!\n")

    def encoding():
        '''
        :return 将输入的字符串根据创建的树编码
        '''
        nonlocal huffman,lst
        if lst:
            if input("您是输入字符串还是从文件中读取(input/file)\n") == 'input':
                # 提示输入字符串
                string = input("请输入您想编码的字符串\n")
                # 创建树
                huffman = HuffmanTree(lst)
                # 返回结果存入到result中
                result = huffman.encoding(string)
                # 提示用户是否存入文件
                if input("您想将该编码保存为文件吗?(y/n)\n") == 'y':
                    # 提示输入文件名
                    filename = input("请输入文件名称\n")
                    # 输入编码
                    with open(filename,'w') as file:
                        file.write(''.join(result))
            else:
                # 输入文件名
                filename = input("请输入文件名\n")
                # 打开文件
                with open(filename, 'r') as file:
                    string = file.read()
                print(string)
                # 创建huffman树
                huffman = HuffmanTree(lst)
                # 编码结果存入到result中
                result = huffman.encoding(''.join(string))
                # 提示用户是否存入文件
                if input("您想将该编码保存为文件吗?(y/n)\n") == 'y':
                    # 提示输入文件名
                    filename = input("请输入文件名称\n")
                    # 输入编码
                    with open(filename, 'w') as file:
                        file.write(''.join(result))
            print("编码成功!\n")
        else:
            print("请先生成Huffman树\n")

    def decoding():
        '''
        :return 解码
        '''
        nonlocal huffman,lst
        if lst:
            if input("您是输入字符串还是从文件中读取(input/file)\n") == 'input':
                # 提示输入编码
                string = input("请输入编码\n")
                if not huffman:
                    huffman = HuffmanTree(lst)
                # 将所得字符串结果返回
                result = huffman.decoding(string)
                # 打印结果
                print(result)
                # 是否保存为文件
                if input("您想将该字符串保存为文件吗?(y/n)\n") == 'y':
                    # 输入文件名
                    filename = input("请输入文件名\n")
                    # 保存文件
                    with open(filename,'w') as file:
                        file.write(result)
            else:
                # 提示输入文件名
                filename = input("请输入文件名\n")
                # 打开文件
                with open(filename,'r') as file:
                    string = ''
                    lines = file.readlines()
                    for line in lines:
                        string+= ''.join(line)

                    # 如果还没建树就建树
                    if not huffman:
                        huffman = HuffmanTree(lst)
                    result = huffman.decoding(string)
                    # 打印结果
                    print(result)
                    # 是否保存为文件
                    if input("您想将该字符串保存为文件吗?(y/n)\n") == 'y':
                        # 输入文件名
                        filename = input("请输入文件名\n")
                        # 保存文件
                        with open(filename, 'w') as file:
                            file.write(result)
            print("解码成功!\n")
        else:
            print("请先生成Huffman树\n")

    def menu():
        # 主窗口
        master = tk.Tk()
        # 标题
        master.title("Huffman")
        # 窗口大小
        master.geometry("600x400")

        # 三个标签
        tk.Label(master, text="实验名称：哈夫曼编码",font =("楷体",14),foreground = "orange").grid(row=0,padx = 200)
        tk.Label(master, text="班级：信卓1901班",font =("楷体",14),foreground = "orange").grid(row=1)
        tk.Label(master, text="作者：高培立",font =("楷体",14),foreground = "orange").grid(row=2)



        # 承载四个按钮的frame
        frame = tk.Frame(master,height = 10,width = 10)
        frame.grid(row = 15,pady = 10)

        # 四个按钮
        button1 = tk.Button(frame,text = "创建权重列表",font =("黑体",14),foreground = 'blue',command = weight)
        button2 = tk.Button(frame,text = "网络爬虫",font =("黑体",14),foreground = 'blue',command = spider)
        button3 = tk.Button(frame,text = "解码",font =("黑体",14),foreground = 'blue',command = decoding)
        button4 = tk.Button(frame,text = "编码",font =("黑体",14),foreground = 'blue',command = encoding)

        # 放置四个按钮
        button1.grid(row = 0,column = 0)
        button2.grid(row = 1,column = 0 )
        button3.grid(row = 2,column = 0 )
        button4.grid(row = 3,column = 0)

        # 退出菜单
        menu = tk.Menu(master)
        menu.add_command(label = "Exit",command = master.quit,underline = 0,accelerator = "Ctrl+Q" )
        master.config(menu = menu)

        # 视图主循环
        master.mainloop()

    return menu()

if __name__ == '__main__':
     main()
