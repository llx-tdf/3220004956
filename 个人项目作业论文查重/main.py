#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/9/17 14:17
# @Author  : LLX

import jieba
import jieba.analyse
from memory_profiler import profile
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from decimal import Decimal
import time
import os
import re
from zhon.hanzi import punctuation


# 读取文件内容到字符串
def string_txt(file):
    strings = ""
    fp = open(f"{file}", 'r', encoding='utf-8')
    line = fp.readline()
    while line:
        strings += line
        line = fp.readline()
    fp.close()
    return strings


# 过滤英文字符标点符号，留下文字
def filter_string(string):
    new_string = re.sub(r"([%s])+" % punctuation, "", string).replace("\n", "").replace(" ", "")

    return new_string


# 用jieba模块找出关键词并计算词频
def jb_list(string):
    # 找出topK个关键词
    ls = jieba.analyse.extract_tags(string, withWeight=False, topK=30)
    words = jieba.lcut(string)

    counts = np.zeros(len(ls))
    for w in words:
        for i in ls:
            if w == i:
                counts[ls.index(i)] += 1
    return counts


# sklearn中的sklearn.metrics.pairwise.cosine_similarity函数直接计算余弦相似度
def duplicate(num1, num2):
    num1 = np.array(num1)
    num2 = np.array(num2)
    res = cosine_similarity(num1.reshape(1, -1), num2.reshape(1, -1))[0][0]

    # 精确到小数点后两位(四舍五入)
    res = Decimal(res).quantize(Decimal("0.00"))
    return res


# 输出答案文件
def outfile(answer_file, num):
    with open(f"{answer_file}", "w", encoding="utf-8")as f:
        f.write(str(num))
        f.write("\n")
    print(fr"{answer_file}")


# 输入异常处理
def command():
    try:
        origin_file, origin_add_file, answer_file = input().split()
        return origin_file, origin_add_file, answer_file
    except Exception as e:
        print(e)
        print("输入有误，请重新输入！\n")
        return command()


# @profile
def main_d():
    origin_file, origin_add_file, answer_file = command()

    if not os.path.exists(origin_file):
        print("【论文原文的文件的绝对路径】输入有误，现返回重新输入！\n")
        main_d()
    elif not os.path.exists(origin_add_file):
        print("【抄袭版论文的文件的绝对路径】输入有误，现返回重新输入！\n")
        main_d()
    else:
        string_txt1 = string_txt(origin_file)
        string_txt2 = string_txt(origin_add_file)

        jb_list1 = jb_list(filter_string(string_txt1))
        jb_list2 = jb_list(filter_string(string_txt2))

        duplicate_num = duplicate(jb_list1, jb_list2)
        outfile(answer_file, duplicate_num)


# 测试函数
def main_test():
    origin_file = input("请输入论文原文的文件的绝对路径：")
    origin_add_file = input("请输入抄袭版论文的文件的绝对路径：")
    jb_list1 = jb_list(filter_string(string_txt(origin_file)))
    jb_list2 = jb_list(filter_string(string_txt(origin_add_file)))
    duplicate_num = duplicate(jb_list1, jb_list2)
    return duplicate_num


def test2():
    jb_list1 = jb_list(
        filter_string(string_txt("D:\\aaaaaa\\junior_year\\SE\\github\\3220004956\\个人项目作业论文查重\\测试文本\\orig.txt")))
    jb_list2 = jb_list(filter_string(
        string_txt("D:\\aaaaaa\\junior_year\\SE\\github\\3220004956\\个人项目作业论文查重\\测试文本\\orig_0.8_add.txt ")))
    jb_list3 = jb_list(filter_string(
        string_txt("测试文本/orig_0.8_del.txt")))
    jb_list4 = jb_list(filter_string(
        string_txt("D:\\aaaaaa\\junior_year\\SE\\github\\3220004956\\个人项目作业论文查重\\测试文本\\orig_0.8_dis_1.txt")))
    jb_list5 = jb_list(filter_string(
        string_txt("D:\\aaaaaa\\junior_year\\SE\\github\\3220004956\\个人项目作业论文查重\\测试文本\\orig_0.8_dis_10.txt")))
    jb_list6 = jb_list(filter_string(
        string_txt("D:\\aaaaaa\\junior_year\\SE\\github\\3220004956\\个人项目作业论文查重\\测试文本\\orig_0.8_dis_15.txt")))
    print(duplicate(jb_list1, jb_list2))
    print(duplicate(jb_list1, jb_list3))
    print(duplicate(jb_list1, jb_list4))
    print(duplicate(jb_list1, jb_list5))
    print(duplicate(jb_list1, jb_list6))


if __name__ == '__main__':
    main_d()
    # test2()


"""
D:\\aaaaaa\\junior_year\\SE\\github\\3220004956\\个人项目作业论文查重\\测试文本\\orig.txt
D:\\aaaaaa\\junior_year\\SE\\github\\3220004956\\个人项目作业论文查重\\测试文本\\orig_0.8_add.txt    
D:\\aaaaaa\\junior_year\\SE\\github\\3220004956\\个人项目作业论文查重\\测试文本\\orig_0.8_del.txt   
D:\\aaaaaa\\junior_year\\SE\\github\\3220004956\\个人项目作业论文查重\\测试文本\\orig_0.8_dis_1.txt 
D:\\aaaaaa\\junior_year\\SE\\github\\3220004956\\个人项目作业论文查重\\测试文本\\orig_0.8_dis_10.txt 
D:\\aaaaaa\\junior_year\\SE\\github\\3220004956\\个人项目作业论文查重\\测试文本\\orig_0.8_dis_15.txt

D:\\aaaaaa\\junior_year\\SE\\github\\3220004956\\个人项目作业论文查重\测试数据\\add_answer.txt

D:\\aaaaaa\\junior_year\SE\github\\3220004956\\个人项目作业论文查重\\测试文本\\orig.txt D:\\aaaaaa\junior_year\\SE\\github\\3220004956\个人项目作业论文查重\\测试文本\\orig_0.8_add.txt D:\\aaaaaa\\junior_year\\SE\\github\\3220004956\\个人项目作业论文查重\\测试数据\\add_answer1.txt

"""
