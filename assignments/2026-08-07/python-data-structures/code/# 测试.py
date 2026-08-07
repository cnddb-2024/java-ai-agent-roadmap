# 测试
from unittest import case


# words= ['cat','window','defenestrate']

# for w in words:
#     print(w,len(w),w+'T')


# users = {'青雀':18,'克拉拉':15,'藿藿':18}

# for user,age in users.copy().items():
#     if age == 15:
#         del users[user]

# print(users)

# print('----------------------------------------------------------------')

# childs = {}
# for user,age in users.items():
#     if age == 15:
#         childs[user] = age

# print(childs)      


# for i in range(999):
#     print(i)

# print(list(range(5,10)))
# print(list(range(0,10,3)))
# print(list(range(-10,-100,-30)))

# s=range(-10,-100,-30)
# print(s)


# for n in range(2, 10):
#     for x in range(2,n):
#         if n % x == 0:
#             print(f"{n} = {x} * {n//x}")
#             break
# 4.4. break 和 continue 语句¶
# for num in range(2,10):
#     if num % 2 == 0:
#         print(f"偶数：{num}")
#         continue
#     print(f"奇数：{num}")

# for num in range(2,10):
#     if num % 2 == 0:
#         print(f"偶数：{num}")
#     else:
#         print(f"奇数：{num}")

# 4.5. 循环的 else 子句

# for n in range(2, 10):
#     print(n)
#
# for n in range(2, 10):
#     for x in range(2, n):
#         if n % x == 0:
#             print(n, 'equals', x, '*', n//x)
#             break
#     else:
#         # 循环到底未找到一个因数
#         print(n, 'is a prime number')

# 4.6. pass 语句
# while True:
#     pass

# class MyEmptyClass:
#     pass
#
# def initlog(*args):
#     pass

# def initlog(*args):
#     ...

# 4.7. match 语句
# def http_error(status):
#     match status:
#         case 400:
#             return "400"
#         case 404:
#             return "404"
#         case 418:
#             return "418"
#         case _:
#             return "Something's wrong with the internet"


#  可以用 | （"或"）将多个字面值组合到一个模式中：
# def http_error(status):
#     match status:
#         case 400 | 404 | 418:
#             return "not found"
#         case _:
#             return "Something's wrong with the internet"


# 形如解包赋值的模式可被用于绑定变量：
# match point:
#     case (0, 0):
#         print("Origin")
#     case (0, y):
#         print(f"Y={y}")
#     case (x, 0):
#         print(f"x={x}")
#     case (x, y):
#         print(f"x={x},y={y}")
#     case _:
#         raise ValueError("Not a point")


# 如果用类组织数据，可以用"类名后接一个参数列表"这种很像构造器的形式，把属性捕获到变量里：
# class Point:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#
#
# def where_is(point):
#     match point:
#         case Point(x=0, y=0):
#             print("Origin")
#         case Point(x=0, y=y):
#             print(f"Y={y}")
#         case Point(x=x, y=0):
#             print(f"X={x}")
#         case Point():
#             print("Somewhere else")
#         case _:
#             print("Not a point")

# 定义函数
# def fib(n):
#     """返回斐波那契数列列表，n以内"""
#     result = []
#     a, b = 0, 1
#     while a < n:
#         result.append(a)
#         a, b = b, a + b
#     return result

# 默认值参数
# def ask_ok(prompt,retries=4,reminder="再输入一次"):
#     while True:
#         reply = input(prompt)
#         if reply in {'y','ye','yes'}:
#             return True
#         if reply in {'n','no','nop'}:
#             return False
#         retries-=1
#         if retries<0:
#             raise ValueError('非法输入')
#         print(reminder)

# 默认值只计算一次
# i=5
#
# def f(arg=i):
#     print(arg)
#
# i = 100
# f()

# def f(a,L=[]):
#     L.append(a)
#     return L
#
# print(f(1))
# print(f(2))
# print(f(3))
#
# def f(a,L=None):
#     if L is None:
#         L=[]
#     L.append(a)
#     return L
#
# print(f(1))
# print(f(2))
# print(f(3))

# 4.9.2. 关键字参数
# 关键字参数必须在位置参数后
# 关键字参数顺序不重要
# 不能重复赋值
# 不能给一个函数不存在的关键字赋值
def a(group, name1='青雀', name2='克拉拉', name3='银狼'):
    pass


a('星穹列车')  # 一个位置参数
a(group='星穹列车')  # 一个关键字参数
a(group='星穹列车', name2='镜流')  # 两个关键字参数
a(name2='三月七', group='星穹列车')  # 两个关键字参数
a('星穹列车', '杨叔', '姬子')  # 三个位置参数
a('星穹列车', name2='饮月君')  # 一个位置参数,一个关键字参数


# 如下是无效调用
# 缺失必需参数 a()
# 关键字参数后有非关键字参数 a(name2='克拉拉','星穹列车')
# 重复参数 a('星穹列车',group='星穹列车')
# 未知的关键字参数 a(name4='')

# **value 类型形参
def cakeshop(kind, *args, **keywords):
    print("-- 有卖的一些", kind, "?")
    print("-- 抱歉，", kind, "卖完了")
    for arg in args:
        print(arg)

    print("-" * 40)
    for kw in keywords:
        print(kw, ":", keywords[kw])


cakeshop("奶油蛋糕", "它很好吃", "它真的非常好吃", shopkeeper='克拉拉', client='藿藿')


# 仅限位置形参、位置和关键字形参、仅限关键字形参，通过/和*分隔开
def standard_arg(arg):
    pass


standard_arg(2)
standard_arg(arg=2)


def standard_arg(arg, /):
    pass


standard_arg(2)
standard_arg(arg=2)  # 错误


def standard_arg(*, arg):
    pass


standard_arg(2)  # 错误
standard_arg(arg=2)


def standard_arg(a, /, b, *, c):
    pass


standard_arg(1, 2, 3)  # 错误
standard_arg(1, 2, c=3)
standard_arg(1, b=2, c=3)
standard_arg(a=1, b=2, c=3)  # 错误


# 参数名称和**kwds 字典关键字参数产生潜在冲突
def foo(name, **kwds):
    pass


foo(1, name=2)
foo('', name=2)
foo(name=2)
foo(1, **{'name': 2})


# 解决方法
def foo(name, /, **kwds):
    pass


foo(1, **{'name': 2})


# 任意实参列表 可变数量实参后只能是关键字参数
def concat(*args, sep="/"):
    return sep.join(args)


concat("earth", "mars", "venus")
concat("earth", "mars", "venus", sep=".")

# 解包实参列表 可以用*将列表内容解包出来作为实参
args = [3, 6]
list(range(*args))


# 同样可以用**传递关键字参数
def a(a, b, c):
    print(a, b, c)


d = {"a": "这是a", "b": "这是b", "c": "这是c"}
a(**d)


# Lambda表达式，用于创建小巧的匿名函数，只包含单个表达式，它只是常规函数定义的语法糖
# 可以返回一个函数
def make_incrementor(n):
    return lambda x: x + n


f = make_incrementor(42)
f(0)
f(1)
# 可以传入一个小函数作为参数，例如list的sort()接受排序键函数key
pairs = [(1, "one"), (2, "two"), (3, "three")]
pairs.sort(key=lambda p: p[1])
pairs
pairs.sort(key=lambda p: p[0])
pairs


# 文档字符串
def my_function():
    """啥也不干，但是我写了文档字符串

    真的啥也不干，这个函数

    >>> my_function()
    >>>
    :return:
    """
    pass


print(my_function.__doc__)


# 函数注解
def f(ham: str, eggs: str = 'Eggs') -> str:
    print("Annotations", f.__annotations__)
    print("Arguments:", ham, eggs)
    return ham + ' and ' + eggs


f('spam')

# 数据结构
# 列表
fruits = ['orange', 'apple', 'pear', 'banana', 'kiwi', 'apple', 'banana']
fruits.count('apple')
fruits.count('132')
fruits.index('banana')
fruits.index('banana', 4)
fruits.reverse()
fruits
fruits.append('grape')
fruits
fruits.sort()
fruits
fruits.pop()
# 用列表实现堆栈
stack = [3, 4, 5]
stack.append(6)
stack.append(7)
stack
stack.pop()
stack

# 用列表实现队列
from collections import deque

queue = deque(['a', 'b', 'c'])
queue.append('d')
queue.append('e')
queue.popleft()
queue
queue.popleft()
queue

# 列表推导式
squares = []
for x in range(10):
    squares.append(x ** 2)

squares

squares = list(map(lambda x: x ** 2, range(10)))

squares = [x ** 2 for x in range(10)]

# 列表推导式的方括号内容包含以下内容：一个表达式，后面是一个for子句，然后是若干个for或if子句，结果得到一个新列表
[(x, y) for x in [1, 2, 3] for y in [3, 1, 4] if x != y]
# 等价于
combs = []
for x in [1, 2, 3]:
    for y in [3, 1, 4]:
        if x != y:
            combs.append((x, y))

combs
# 表达式是元组时必需加上圆括号
vec = [-4, -2, 0, 2, 4]
# 新建一个将值翻倍的列表
[x * 2 for x in vec]
# 过滤以排除负数
[x for x in vec if x >= 0]
# 对所有元素应用函数或方法
[abs(x) for x in vec]
freshfruit = ['          banana  ', '   loganberry    ', 'passion fruit       ']
[weapon.strip() for weapon in freshfruit]
# 创建一个（数字，平方）的二元组
[(x, x ** 2) for x in range(6)]
# 使用两个for展平嵌套的列表
vec = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
[num for elem in vec for num in elem]
# 列表推导式可以用复杂的表达式和嵌套
from math import pi

[str(round(pi, i)) for i in range(1, 6)]

# 列表推导式可以嵌套
matrix = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
]

# 转置行列
[[row[i] for row in matrix] for i in range(4)]

list(zip(*matrix))

# del，可以按索引删除列表条目，还可以移除切片或情况列表
a = [-1, 1, 66.25, 333, 333, 1234.5]
del a[0]
a
del a[2:4]
a
del a[:]
a
# 也可以删除变量
del a

# 数据类型 序列包括：列表、字符串、元组，元组由多个逗号隔开的值组成
t = 12345, 54321, 'hello!'
t[0]
t
u = t, (1, 2, 3, 4, 5)
u
t[0] = 888  # 不能设置值，元组对象不支持项分配
v = ([1, 2, 3], [3, 2, 1])  # 但是元组的内容可以包含可变对象
# 元组是不可变的、列表是可变的
# 构建0个或1个元素的元组
empty = ()
singleton = 'hello',  # 注意结尾的逗号
len(empty)
len(singleton)
singleton

# 序列解包，操作时左侧变量和右侧序列元素的数量需相等，多重赋值其实也是元组打包和序列解包的组合
# 元组打包
t = 12345, 54321, 'hello!'
# 序列解包
x, y, z = t
x
y
z

# 集合 是不重复元素组成的无序集，创建用{}和set（），创建空集合只能用set()，{}创建的是空字典，且集合无序
basket = {'apple', 'orange', 'apple', 'pear', 'orange', 'banana'}
basket
'orange' in basket
'1' in basket

a = set('abracadabra')
b = set('alacazam')

a - b  # 差集
a | b  # 合集
a & b  # 交集
a ^ b  # 存在与a或b中但非两者皆有的

a = {x for x in a if x not in 'abc'}
a

# 字典 键值对 键是任何不可变类型且唯一，字符串、数字、元组（仅包含字符串数据元组等不可变类型，如果包含了可变类型对象则不可用作键），get()取值，list(d)返回字典所有键列表，如需排序用sorted(d)，检查十分钟存在键使用in
tel = {'jack': 4098, 'sape': 4139}
tel['guido'] = 4127
tel
tel['jack']
tel['irv']  # 不存在的键 报错
tel.get('irv')  # None
del tel['sape']
tel['irv'] = 4127
tel
list(tel)
sorted(tel)
'guido' in tel
'jack' not in tel
# dict()构造函数可以直接用键值对序列创建字典
dict([('sape', 4137), ('guido', 4127), ('jack', 4098)])
dict([[1, 4], [2, 5], [3, 6]])
dict(**tel)
dict(sape=4139, guido=4127, jack=4098)  # 直接用关键字参数指定键值对
# 字典推导式：用键值对表达式创建字典
{x: x ** 2 for x in (2, 4, 6)}

# 对字典的循环
knights = {'a': 1234, 'b': 5678}
for k, v in knights.items():
    print(k, v)
# 对序列循环时，用enumerate()可以同时取出索引和其值
for i, v in enumerate([1, 2, 3]):
    print(i, v)

# 同时循环多个序列，使用zip()可将元素意义匹配
questions = ['name', 'job', 'favorite color']
answers = ['clara', 'none', 'red']
for q, a in zip(questions, answers):
    print(q, a)
    print('-' * 40)
    print('what is your {0} ?  It is {1}'.format(q, a))

# 逆向循环
for i in reversed(range(1, 10, 2)):
    print(i)

# 循环列表时同时修改内容，创建新列表安全
import math

raw_data = [56.2, float('NaN'), 51.7, 55.3, 52.5, float('NaN'), 47.8]
filtered_data = []
for value in raw_data:
    if not math.isnan(value):
        filtered_data.append(value)

filtered_data

# 短路运算符用作普通纸而不是布尔值时，返回值通常是最后一个求了值的参数
s1, s2, s3 = '', 'a', 'b'
non_null = s1 or s2 or s3
non_null

# 序列和其他类型的比较，按照字典式顺序依次比较，如果所有元素都相等则两个序列相等
(1, 2, 3) < (1, 2, 4)
[1, 2, 3] < [1, 2, 4]
'ABC' < 'C' < 'Pascal' < 'Python'
(1, 2, 3, 4) < (1, 2, 4)
(1, 2) < (1, 2, -1)
(1, 2, 3) == (1.0, 2.0, 3.0)
(1, 2, ('aa', 'ab')) < (1, 2, ('abc', 'a'), 4)
