#_*_ coding: utf-8 _*_ 

# 문자열 
# 이게 주석입니다. 파이썬의 기본 인코딩은 ascii이다. 위와 같이 인코딩 정보를 명시해주어야 한다.
print("hello world")

# 파이썬은 문자려에 작은 따옴표, 큰 따옴표 둘다 사용한다. 
print 'hello world'
print "hello world"  
print "what 's your name" # 큰 따옴표 안에 작은 따옴포를 넣읈 수 있다.  반대도 가능하다. 
print '"kim"'

# 따옴표 세게 
# 멀티라인 문자열은 세 개의 따옴표로  ''' 또는 """ 
s = ''' 이게 바로 멀티 라인 스트링
입니다. 
여기도 포함됩니다. 
'''

print s

#formating 
age = 20
name = 'jonggun'


print '{0} was {1} years old'.format(name, age)  
print '{} was {} years old'.format(name, age) # 인덱스 넘버 생략 가능
print name + ' was ' + str(age) + ' years old'



# operator
x = 3; y = 6 

print x <= y
print y <= x

print x == y
print x != y

print not (x == y)

print not (x == y) and x < y

print (x == y) or x < y

a = 2
a += 4
a *= 3

print a



# statement 
# 파이썬에는 swith 문이 없다. if else를 사용하거나 dict을 사용한다. 


# while else 
# while을 break를 빠져 노아지 않으면 else 가 실행된다. 
cnt = 10 
while cnt > 0:
    print cnt
    cnt -= 1
else:
    print 'while loop is done' 

cnt = 10 
while cnt > 0:
    print cnt
    cnt -= 1
    if cnt == 5:
        break; # else가 실행되지 않음 
else:
    print 'while  is done' 

# for else
for i in range(1, 5):
    print i 
else:
    print 'print for is done'

# variable scope 


g = 10

def foo():
    g = 2
foo()
print 'g', g

def foo2(): 
    global g
    g = 2
foo2()
print 'g', g

# 디폴트 파라미터
def goo(a=10):
    print(a)

goo(3)
goo()

# 키워드 인수
# 장점 - 장적 인수 순서를 신겨쓰지 않고 호출. 특정한 변수엑만 값을 넘김 

def foo3(a, b=5, c=10):
    print ('a:', a, 'b:', b, 'c:', c)

foo3(20)
foo3(20, c=100)
foo3(b=2, a=3)

# VarArg - Variable arguments
# * 는 튜플로 받는다. 
# ** 는 dict 으로 받는다. 
def total(initial=5, *numbers, **keywords):
    ''' 함수에 관한 docstring을 여기에다가 
    추가한다. 즉 함수 첫번째 줄에 추가한다. 
    함수이름에 커서가 놓이면 여기 설명이 표시된다.
    '''
    count = initial
    for num in numbers:
        count += num

    for key in keywords:
        count += keywords[key]
    return count

print total(10, 1,2,3, kin=50, jong=10)

''' docstring은 함수객체가 가지고 있는 기본 속성이다. 
help() 가 하는 일이 doc 속성을 보여주는 것이다. '''
print total.__doc__


''' import 테스트 '''

import sys

print('command line args are:')
for i in sys.argv:
    print i

print '\n PYTHON path:', sys.path, '\n'

''' import custom module '''

import test_module

test_module.say_hi()
print 'ver: ', test_module.__version__

from test_module import say_hi, __version__
say_hi()
print __version__

print dir(test_module)


''' package 
그냥 단순한 폴더지만 파이썬에게 이 폴던는 파이썬 모듈을 담고 있는다는 것으 알려주는 역할을 하는 
init.py 라는 특별한 파일을 한 개 포함하고 있다.'''


''' Data structure '''
chapter = '''list '''
print chapter

shoplist = ['iphone', 'ipad', 'new mac book']

print 'the number of items', len(shoplist)

for item in shoplist:
    print item,
print ''

shoplist.append('playstation4')

print 'new shopping list', shoplist

shoplist.sort();
print 'sorted shopping list', shoplist

del shoplist[3]
print 'updated shoppling list', shoplist

chapter = '==' * 4 +" tuple"
print chapter

zoo = ('snake', 'horse', 'lion')
print 'number of animals', len(zoo)

new_zoo = ('monkey', 'tiger', 'dog', zoo)

print "new zoo 's animals", len(new_zoo)
print 'last animal', new_zoo[3][2]

''' 튜플 요소가 한 개일 때 뒤에 쉼포를 추가해줘야한다.
 그렇지 않으면 연산 괄호로 생각한다.'''
a = (2, )

chapter = 'Dict'
print chapter

tb = { 'kin': 20, 'hee': 21, 'won': 'lee'}

print 'kin age:', tb['kin']

for k in tb:
    print tb[k], 

''' item() key,val 튜플을 리턴해준다. '''
for k,v in tb.items():
    print 'key', k, 'value',v

del tb['won'] 
print 'table', tb

tb['won2'] = 9

if 'kin' in tb:
    print tb['kin']

print 'number of items in table', len(tb)

''' 열거형 (시퀀스 컬렉션 ) - string, list, tuple '''
''' 특징 1) 멤버쉽 테스트(in, not in) 2) 인덱싱 연산 3) 슬라이스 연산'''


''' python reference '''

# variable is like pointer
reflist = shoplist

del reflist[0]

# deep copy
deeplist = shoplist[:]

del deeplist[0]

print deeplist
print shoplist


chapter = ''' Class '''
print chapter

class Person:
    ''' hello Person '''

    # class variable 
    greedy = True
    population = 0

    def __init__(self, name, age):
        ''' put name of person 기본적으로 모든 클래스의 field는 public 이다. 그러나 밑줄 두개 예르를 들면 
        __data 처럼 하면 private으로 된다.  '''
        self.name = name
        self.age = age
        self.__private_name = name
        # way to access calss variable
        Person.population += 1
    
    def who_i_am(self): 
        return 'name: {}, age: {}'.format(self.name, self.age)

    def virutalMethod(self):
        print 'ojbect method in python is virtual'

    def say_hello(self):
        ''' get name of the person and print it '''
        print 'hi my name is ' + self.name

    def die(self):
        print 'one persion just died'
        Person.population -= 1

        if Person.population == 0:
            print ('human being is done')
    # @decorator
    @classmethod
    def how_manay_people(cls):
        return Person.population

class Student(Person):
    def __init__(self, name, age, marks):
        ''' python은 상속한 부모의 생성자를 호출해주지 않으므로 명시적으로 호출한다. '''
        Person.__init__(self, name, age)
        self.marks = marks
    
    def who_i_am(self):
        ''' 부모 메소드를 호출할때 내가 직접호출 하며 self를 넘겨줘야하는 구만. '''
        return Person.who_i_am(self) + ', marks' + self.marks

    def virutalMethod(self):
        print 'student method in python is virtual'


class Teacher(Person):
    def __init__(self, name, age, salary):
        Person.__init__(self, name, age)
        self.salary = salary
    
    def who_i_am(self):
        return Person.who_i_am(self) + ', salary:' + str(self.salary)

    def virutalMethod(self):
        print 'teacher method in python is virtual'

print 'All human being is greday? ' + str(Person.greedy)

student = Student('masako', 10, 'what?')
teacher = Teacher('kin', 20, 1000)


''' 다형성 테스트 ''' 
members = [student, teacher]
for member in members:
    print member.who_i_am()
    print member.virutalMethod()


print (' how many people now?', Person.how_manay_people())

teacher.die()

print (' how many people now?', Person.how_manay_people())



chapter = "Python IO"
print chapter



print 'pandrom'


def reverse_data(in_data):
    return in_data[::-1]

def is_pandrom(in_data):
    return in_data == reverse_data(in_data)

''' object serialization '''
import pickle

f = open('object.data', 'w')
shoplist = ['ipad', 'iphone']

pickle.dump(shoplist, f)
f.close
del shoplist


f = open('object.data', 'r')

shoplist = pickle.load(f)

print shoplist


chapter = '''exception'''
print chapter


class ShortInputException(Exception):
    def __init__(self, length, atleast):
        Exception.__init__(self)
        self.length = length
        self.atleast = atleast
    

try:
    text = raw_input('input: ')

    if len(text) < 3:
        raise ShortInputException(len(text), 3)
except EOFError:
    print 'EOFError'
except ShortInputException as ex:
    print 'your text len: {} at least {} requred'.format(ex.length, ex.atleast)
else:
    print 'called when no exception occured '
finally:
    print 'called when exceotion occured and not occured'


chapter = '''standard module'''

import sys

print sys.version_info


import os, logging, platform 


if platform.platform().startswith('Windows'):
    logging_file_path = os.path.join(os.getenv('HOMEDRIVE'), os.getenv('HOMEPATH'), 'test.log')
else:
    logging_file_path = os.path.join(os.getenv('HOME'), 'test.log')

print logging_file_path

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s : %(levelname)s : %(message)s',
    filename=logging_file_path,
    filemode='w',
)

logging.debug('start to login debug mode')
logging.info('this is info message')
logging.warning('this is warning msg')