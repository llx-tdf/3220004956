#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/9/17 14:17
# @Author  : LLX

import jieba
import jieba.analyse
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from decimal import Decimal
import time


# 读取文件内容到字符串
def string_txt(file):
    fp = open(file, 'r', encoding='utf-8')
    strings = fp.read()
    return strings


# 过滤标点等符号，留下文字
def filter_string(string):
    # 字符串直接就用replace来过滤就好
    new_string = string.replace("\n", "").replace("，", "").replace("。", "").replace("、", "").replace("”", "").replace(
        "“", "").replace(" ", "").replace("：", "").replace("*", "").replace("《", "").replace("》", "")
    return new_string


# 用jieba模块找出关键词并计算词频
def jb_list(string):
    # 找出30个关键词
    ls = jieba.analyse.extract_tags(string, withWeight=False, topK=20)
    words = jieba.lcut(string)

    counts = np.zeros(len(ls))
    for w in words:
        for l in ls:
            if w == l:
                counts[ls.index(l)] += 1

    return counts


# sklearn中的sklearn.metrics.pairwise.cosine_similarity函数可直接计算余弦相似度
def duplicate(num1, num2):
    num1 = np.array(num1)
    num2 = np.array(num2)
    res = cosine_similarity(num1.reshape(1, -1), num2.reshape(1, -1))[0][0]
    # 精确到小数点后两位(四舍五入)
    res = Decimal(res).quantize(Decimal("0.00"))
    return res


def main_d():
    origin_file = input("论文原文的文件的绝对路径：")
    origin_add_file = input("抄袭版论文的文件的绝对路径：")

    # start = time.time()
    string_txt1 = string_txt(fr"{origin_file}")
    string_txt2 = string_txt(fr"{origin_add_file}")

    filter_string1 = filter_string(string_txt1)
    filter_string2 = filter_string(string_txt2)

    jb_list1 = jb_list(filter_string1)
    jb_list2 = jb_list(filter_string2)

    with open("answer.txt", "a+", encoding="utf-8")as f:
        f.write(str(duplicate(jb_list1, jb_list2)))
        f.write("\n")
    print(r"输出的答案文件的绝对路径：D:\aaaaaa\junior_year\SE\github\3220004956\个人项目作业论文查重\answer.txt")
    # end = time.time()
    # print(end-start)


if __name__ == '__main__':
    main_d()

"""
D:\aaaaaa\junior_year\SE\github\3220004956\个人项目作业论文查重\测试文本\orig.txt
D:\aaaaaa\junior_year\SE\github\3220004956\个人项目作业论文查重\测试文本\orig_0.8_add.txt    
D:\aaaaaa\junior_year\SE\github\3220004956\个人项目作业论文查重\测试文本\orig_0.8_del.txt   
D:\aaaaaa\junior_year\SE\github\3220004956\个人项目作业论文查重\测试文本\orig_0.8_dis_1.txt 
D:\aaaaaa\junior_year\SE\github\3220004956\个人项目作业论文查重\测试文本\orig_0.8_dis_10.txt  
D:\aaaaaa\junior_year\SE\github\3220004956\个人项目作业论文查重\测试文本\orig_0.8_dis_15.txt
"""