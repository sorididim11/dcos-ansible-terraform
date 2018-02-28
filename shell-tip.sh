#!/usr/bin/env bash
# Bash는 공백에 민감하다.

# 주석은 이렇게 
# echo 는 printf 와 동일. shell 에서는 printf 사용 
echo "test echo/printf"
echo "hello world"
printf "hello world by printf\n"
printf "formatting: %d %s" 10 test

# function

# function keyword 생략 가능
function string_test1() {
    echo "string test1"
}

string_test2()
{
    echo "string test2"
    echo "인자 값: $@"
}

# 호출
string_test1
string_test2

string_test2 12 "kim" jong
echo ""

# 변수 
# 변수 사용은 생각하지 말고 ${변수} 이렇게 쓰자.
#  사용시 '=' 기회 앞뒤로 공백이 없어야 대입연산자가 됨
# 기본적으로 모드 전역 변수임. 함수 안에서만 지역 변수를 쓸수 있으나 local keyword를 붙여줘야함 
# 전역 변수는 현재 쉘에서만 유효. 즉 자식 쉘에서는 유효하지 않음 - export를 붙여 전역 변수를 환경변수로 만들면 자식 쉘에서도 유효.

echo "varible test"
str="hello world by variable"
echo ${str}

function local_var_test() {
    str="stil gloabl"
    echo $str

    local str="this is diffrent local var"
    echo $str
}

local_var_test

# 지역 변수 테스트 함수에서 동일한 변수 명을 사용했지만 값이 변경되지 않음
echo $str
echo ""

# reserved variable
echo "reserved variable"
echo $HOSTNAME
echo $OSTYPE
echo $LOGNAME
echo $USER
echo $UID
echo ""

# Positional Parameters
echo "Positional Parameters"
echo "실행된 스크립트 이름 $0"

function test_Positional_params() {
    echo "전체 인자 $@"
    echo "전체 인자 $*" # $@ 동일하지만 인자에 쌍따옴표가 있으면 결과가 다름
    echo "첫번째: $1, 두번째: $2"
    echo "인자 개수: $#"
}

test_Positional_params 10 20 30


# 특수 매개 변수(Special Parameters)
echo "특수 매개 변수(Special Parameters)"
echo "최근에 실행된 명령어, 함수, 스크립트 자식의 종료 상태: $?"
echo "$-	현재 옵션 플래그"
echo ""

# 매개 변수 확장(Parameter Expansion)
echo "매개 변수 확장(Parameter Expansion)"

# $변수와 동일하지만 {} 사용해야만 동작하는 것들이 있음(예: echo ${string})
va="variable test"
echo ${va}

# 위치 다음부터 문자열 추출(예: echo ${string:4})
echo ${va:3}

# 위치 다음부터 지정한 길이 만큼의 문자열 추출(예: echo ${string:4:3})
echo ${va:4:3}

# 변수 미선언 혹은 NULL일때 기본값 지정, 위치 매개 변수는 사용 불가(예: echo ${string:-HELLO}).
# ${변수:=단어} 와 동일
unset va
echo ${va:-default}

unset va
echo ${va:=default}

# 변수 미선언시만 디폴트 값을 적용할 경우  ${변수-단어} 또는 ${변수=단어}
unset va
echo ${va-default}

unset va
echo ${va=default}
echo ""

# Array 

# 배열의 크기 지정없이 배열 변수로 선언
# 참고: 'declare -a' 명령으로 선언하지 않아도 배열 변수 사용 가능함
declare -a array

arr=("hello" "array" "test")
arr[3]="ok"
echo "hello world 출력: ${arr[0]} ${arr[3]}"
echo "배열 전체 출력: ${arr[@]}"
echo "배열 전체 개수 출력: ${#arr[@]}"

# 배열 특정 요소만 지우기
unset arr[3]
echo "배열 전체 출력: ${arr[@]}"

# 배열 전체 지우기
unset arr
echo "배열 전체 출력: ${arr[@]}"

# 변수 타입 지정(Variables Revisited)
# 읽기 전용
# readonly string_variable="hello world" 문법과 동일 함
declare -r string_variable

# 정수
# number_variable=10 문법과 동일 함
declare -i number_variable=10

# 배열
# array_variable=() 문법과 동일 함
declare -a array_variable

# 환경 변수
# export export_variable="hello world" 문법과 동일 함
declare -x export_variable="hello world"

# 현재 스크립트의 전체 함수 출력
declare -f

# 현재 스크립트에서 지정한 함수만 출력
declare -f 함수이름


# 반복문 
echo "반복문"
for str in "hello" "world" "..."
do
  echo ${str}
done


for i in {1..5}
do
  echo "index: ${i}"
done 


count=0
while [ ${count} -le 5 ]
do
  echo ${count}
  count=$(( ${count} + 1 ))
done


# 조건문
echo "conditional statement"
str1="hello"
str2="world"

if [ ${str1} == ${str2} ]
then
  echo "first"
elif [ $str2 == $str1 ]
then 
  echo "second"
else
  echo "third"
fi
echo ""

# switch
echo "switch case statment"
for str in "HELLO" "WORLD" "hello" "world" "s" "start" "end" "etc"
do
  case ${str} in
    hello|HELLO)
      echo "${str} hello 또는 HELLO"
      ;;
    wo*)
      echo "${str} wo로 시작"
      ;;
    s|h)
      echo "${str} s또는 h로 시작"
      ;;
    *)
      echo "${str} 기타"
      ;;
  esac
done