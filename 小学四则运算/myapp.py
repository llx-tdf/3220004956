#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/9/24 16:15
# @Author  : LLX

import random
from fractions import Fraction
import decimal
import re


# 小数 ——> 真分数
def proper_fraction(num):
    frac = Fraction(str(num))
    numerator, denominator = frac.numerator, frac.denominator
    a = numerator // denominator
    b = numerator % denominator
    if a == 0 and b == 0:
        res = 0
    elif b == 0 and a != 0:
        res = str(a)
    elif a == 0 and b != 0:
        res = str(b) + "/" + str(denominator)
    else:
        res = str(a) + "‘ " + str(b) + "/" + str(denominator)
    return res


# 生成 n 条自然数四则表达式
def generateNaturals(n, r):
    ops = ["+", "-", "*", "/"]
    i = 1
    questions = []  # 题目
    answers = []  # 题目答案
    responses = []  # 答题
    while i < n + 1:  # n条表达式
        m = random.randint(1, 3)  # 一条表达式的运算符数
        if m == 1:  # 一个运算符
            op = ops[random.randint(0, 3)]
            num1 = random.randint(0, r)
            if op == "/":
                num2 = random.randint(1, r)
            elif op == "-":
                num2 = random.randint(0, num1)
            else:
                num2 = random.randint(0, r)
            e1 = str(num1) + " " + op + " " + str(num2)
        elif m == 2:  # 两个运算符
            op1 = ops[random.randint(0, 3)]
            op2 = ops[random.randint(0, 3)]
            num1 = random.randint(0, r)
            if op1 == "/" and op2 != "/":
                num2 = random.randint(1, r)
                num3 = random.randint(0, r)
            elif op1 != "/" and op2 == "/":
                num2 = random.randint(0, r)
                num3 = random.randint(1, r)
            elif op1 == "/" and op2 == "/":
                num2 = random.randint(1, r)
                num3 = random.randint(1, r)
            else:
                num2 = random.randint(0, r)
                num3 = random.randint(0, r)
            e1 = str(num1) + " " + op1 + " " + str(num2) + " " + op2 + " " + str(num3)
        else:  # 三个运算符
            op1 = ops[random.randint(0, 3)]
            op2 = ops[random.randint(0, 3)]
            op3 = ops[random.randint(0, 3)]
            num1 = random.randint(0, r)
            num2 = random.randint(0, r)
            num3 = random.randint(0, r)
            num4 = random.randint(0, r)
            if op1 == "/":
                num2 = random.randint(1, r)
            if op2 == "/":
                num3 = random.randint(1, r)
            if op3 == "/":
                num4 = random.randint(1, r)
            e1 = str(num1) + " " + op1 + " " + str(num2) + " " + op2 + " " + str(num3) + " " + op3 + " " + str(num4)
        val = eval(e1)
        if val < 0:
            i -= 1
        elif "." in str(val):
            val = round(decimal.Decimal(str(val)), 2)  # 保留两位小数
            e2 = e1.replace("/", "÷")
            val = proper_fraction(val)
            ques = f"【第{i}题】 {e2} ="
            print(ques)
            questions.append(ques)
            answers.append(str(val))
            # 回答问题
            res = input()
            responses.append(res)
        else:
            e2 = e1.replace("/", "÷")
            ques = f"【第{i}题】 {e2} ="
            print(ques)
            questions.append(ques)
            answers.append(str(val))
            # 回答问题
            res = input()
            responses.append(res)

        # 将问题写入 Exercises.txt
        inFile(questions, "Exercises.txt")
        # 将答案写入 Answers.txt
        inFile(answers, "Answers.txt")
        # 对比答案
        check(answers, responses)
        i += 1


# 对比答案
def check(answers, responses):
    correct = ()
    wrong = ()
    cNum = 0
    wNum = 0
    for i in range(0, len(answers)):
        answer = answers[i]
        response = responses[i]
        # 带分数
        if len(re.findall(r"\d+", answer)) == 3 and len(re.findall(r"\d+", response)) == 3:
            an_frac, a, b = re.findall(r"\d+", answer)[0], re.findall(r"\d+", answer)[1], re.findall(r"\d+", answer)[2]
            a_num = float(int(a) / int(b))
            re_frac, c, d = re.findall(r"\d+", response)[0], re.findall(r"\d+", response)[1], \
                            re.findall(r"\d+", response)[2]
            r_num = float(int(c) / int(d))
            if (int(an_frac) == int(re_frac)) and (r_num - a_num) < 0.01:   # 带分数整数部分相同，分数部分相减小于0.01
                correct = correct + ((i + 1),)
                cNum += 1
            else:
                wrong = wrong + ((i + 1),)
                wNum += 1
        # 分数
        elif len(re.findall(r"\d+", answer)) == 2 and len(re.findall(r"\d+", response)) == 2:
            a, b = re.findall(r"\d+", answer)[0], re.findall(r"\d+", answer)[1]
            a_num = float(int(a) / int(b))
            c, d = re.findall(r"\d+", response)[0], re.findall(r"\d+", response)[1]
            r_num = float(int(c) / int(d))
            if (r_num - a_num) < 0.01:
                correct = correct + ((i + 1),)
                cNum += 1
            else:
                wrong = wrong + ((i + 1),)
                wNum += 1
        else:
            if response == answer:
                correct = correct + ((i + 1),)
                cNum += 1
            else:
                wrong = wrong + ((i + 1),)
                wNum += 1
    with open("Grade.txt", "w", encoding="utf-8")as fp:
        fp.write(f"Correct:{cNum} {correct}\n")
        fp.write(f"Wrong:{wNum} {wrong}")


def inFile(content, filename):
    with open(filename, "w", encoding="utf-8")as fp:
        fp.write("\n".join(content))


def main():
    # 异常处理
    try:
        n = int(input("生成题目的个数："))
        r = int(input("题目中数值（自然数、真分数和真分数分母）的范围："))
        generateNaturals(n, r)
    except ValueError:
        main()


if __name__ == '__main__':
    main()
