from os import sep
from typing import Container

BaseRule    = ["string", "int", "char"]
CSRule      = ["string", "int", "char"]

WordEndList = [" ", "=", ";", "(", ")", "{", "}", "[", "]", "\n", "\r"]

CSAccessModifier = ["public", "private", "protected", "default"]
CSDataType = ["int", "string", "long", "char"]

ContainAll = CSAccessModifier + CSDataType

## 주어진 코드 추출
def Extraction( code ):
    result = []
    object = None
    word = None
    
    isword = False
    ismethod = False
    isannounce = False
    iscondition = False
    isOperator = False
    
    wordindex = None
    methodindex = None
    announceindex = None
    conditionindex = None
    operatorindex = None
    
    finishindex = 0
    opencount = 0
    
    for i in range(0, len(code)):
        ## 단어 찾기
        if i >= finishindex:
            if isword == False and ismethod == False and isannounce == False and code[i] not in WordEndList:
                wordindex = i
                isword = True
            
            if isword and code[i] in WordEndList:
                word = code[wordindex : i]
                isword = False
                
                ## 선언문의 경우
                if word not in CSAccessModifier and word not in CSDataType and word != "static":
                    ## 선언문의 경우
                    if FindNextChar(code[i : ]) == '=' or FindNextChar(code[i : ]) == ';':
                        temp = List()
                        temp.Category = "Announce"
                        temp.Target = word
                        temp.Value = code[finishindex : i + (FindNextCharIndex(code[i : ], ';'))] + ';'
                        result.append(temp)
                        
                    finishindex = (i + 1 + FindNextCharIndex(code[i : ], ';'))
            
    return conv(result)

## 구성요소 설정
def conv( code ):
    result = Container()
    
    word = None
    startindex = 0
    startword = False
    
    startvalue = False
    valueindex = 0
    
    for i in range(0, len(code)):
        if code[i].Category == "Announce":
            temp = Announce()
            temp.Name = code[i].Target
            
            for j in range(0, len(code[i].Value)):
                if startword == False and startvalue == False and code[i].Value[j] not in WordEndList:
                    startindex = j
                    startword = True
        
                if startword and code[i].Value[j] in WordEndList:
                    word = code[i].Value[startindex : j]
                    startword = False
                    
                    if word in CSAccessModifier:
                        temp.AccessModifier = word
                    elif word == "static":
                        temp.StaticModifier = word
                    elif word in CSDataType:
                        temp.DataType = word
                        if FindNextChar(code[i].Value[j : ]) == '[':
                            startvalue = True
                            valueindex = (j + 1)
                
                if startvalue and code[i].Value[j] == ']':
                    startvalue = False
                    temp.ArrayValue = code[i].Value[valueindex : j]
                    
                if code[i].Value[j] == '=':
                    temp.Value = code[i].Value[FindNextCharIndex(code[i].Value[j + 1 : ], FindNextChar(code[i].Value[j + 1 : ])) + j + 1 : FindNextCharIndex(code[i].Value, ';')]
                        
            result.Announces.append(temp)
            
    return result


## (코드 추출 추가 메소드) 바로 다음의 문자 찾기 
def FindNextChar( code ):
    for i in range( 0, len(code) ):
        if code[i] != ' ' and code[i] != '\n' and code[i] != '\n':
            return code[i]
    return 0

## (코드 추출 추가 메소드) 바로 다음의 문자 찾기 
def FindNextCharIndex( code, target ):
    for i in range( 0, len(code) ):
        if code[i] == target:
            return i
    return 0

## (코드 추출 추가 메소드) 바로 다음의 단어 찾기
def FindNextWord( code ):
    word = None
    startindex = 0
    startword = False
    
    for i in range(0, len(code)):
        if startword == False and code[i] not in WordEndList:
            startindex = i
            startword = True
        
        if startword and code[i] in WordEndList:
            word = code[startindex : i]
            return word
        
    return word

## 코드 변환 (1 = C / 2 = C# / 3 = C++ / 4 = Python / 5 = Java)
def ConvertCode( code ):
    result = code
    return result

## 코드 결합
def CombineCode( code ):
    result = ""
    return result

class List():
    Category = None
    Target = None
    Value = None

class Container():
    Announces = []
    Functions = []
    Methods = []

## 선언문
class Announce():
    AccessModifier = "default"
    StaticModifier = "default"
    DataType = "default"
    ArrayValue = None
    Name = "default"
    Value = None

## 조건문
class Condition():
    Target = None
    Operator = None
    Value = None
    
## 증감문
class Operator():
    Target = None
    Operator = None
    Value = None

class Method_If():
    Condition = []
    Value = []
    Else = None

class Method_For():
    First = None
    Condition = None
    Change = None
    Value = []