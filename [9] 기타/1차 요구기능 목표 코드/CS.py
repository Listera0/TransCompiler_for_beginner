from ast import Compare
from os import sep
from typing import Container

BaseRule    = ["string", "int", "char"]
CSRule      = ["string", "int", "char"]

WordEndList = [" ", "=", ";", "(", ")", "{", "}", "[", "]", "\n", "\r"]

CompareOperator = [">", "<", ">=", "<=", "==", "!="]
StartRange = ["(", "{", "["]
EndRange = [")", "}", "]"]
CSAccessModifier = ["public", "private", "protected", "default"]
CSDataType = ["int", "string", "long", "char"]

ContainAll = CSAccessModifier + CSDataType

## 주어진 코드 추출
def Extraction( code ):
    result = Container()
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
    
    tempifmethod = None
    
    finishindex = 0
    
    for i in range(0, len(code)):
        ## 단어 찾기
        if i >= finishindex:
            if isword == False and ismethod == False and isannounce == False and code[i] not in WordEndList:
                wordindex = i
                isword = True
            
            if isword and code[i] in WordEndList:
                word = code[wordindex : i]
                isword = False
                
                if word not in CSAccessModifier and word not in CSDataType and word != "static":
                    ## 선언문의 경우
                    if FindNextChar(code[i : ]) == '=' or FindNextChar(code[i : ]) == ';':
                        result.Announces.append(ConvertAnnounce(code[finishindex : i + (FindNextCharIndex(code[i : ], ';'))] + ';', word))
                        
                        finishindex = (i + 1 + FindNextCharIndex(code[i : ], ';'))
                        
                    ## 조건식의 경우
                    if FindNextChar(code[i : ]) in CompareOperator or FindNextCharLength(code[i : ], 2) in CompareOperator:
                        return ConvertCondition(code, word)
                    
                
                ## if 문의 경우
                if word == "if" and isifmethod == False:
                    tempifmethod = If_Method()
                    
                    conditionrange = i + 1 + FindRange(code[i : ], FindNextChar(code[i : ]))
                    tempifmethod.Condition.append(Extraction(code[i : conditionrange]))
                    
                    valuerange = conditionrange + 1 + FindRange(code[conditionrange : ], FindNextChar(code[conditionrange : ]))
                    tempifmethod.Value.append(Extraction(code[conditionrange : valuerange]))

                    finishindex = valuerange
                    isifmethod = True
                    
                    if FindNextCharLength(code[valuerange : ], 4) != "else":
                        isifmethod = False
                        result.IfMethods.append(tempifmethod)
                        tempifmethod = None
                    
                ## else의 경우
                if word == "else":
                    ## else if 문
                    if FindNextCharLength(code[i : ], 2) == "if":
                        StartRange = i + 1 + FindNextCharIndex(code[i : ], 'f')
                        
                        conditionrange = StartRange + 1 + FindRange(code[StartRange : ], FindNextChar(code[StartRange : ]))
                        tempifmethod.Condition.append(Extraction(code[StartRange : conditionrange]))
                    
                        valuerange = conditionrange + 1 + FindRange(code[conditionrange : ], FindNextChar(code[conditionrange : ]))
                        tempifmethod.Value.append(Extraction(code[conditionrange : valuerange]))
                        
                        finishindex = valuerange
                        
                        if FindNextCharLength(code[valuerange : ], 4) != "else":
                            isifmethod = False
                            result.IfMethods.append(tempifmethod)
                            tempifmethod = None
                            
                    ## else 문
                    else:
                        valuerange = i + 1 + FindRange(code[i : ], FindNextChar(code[i : ]))
                        tempifmethod.Else = Extraction(code[i : valuerange])
                        
                        finishindex = False
                        
                        isifmethod = False
                        result.IfMethods.append(tempifmethod)
                        tempifmethod = None
            
    return result

'''
결과값
container 형태인데 그 안에
IfMethod 의 condition 안에 Condition 여러개
                           Value 여러개
                           Else 하나
'''

## 선언문 변환
def ConvertAnnounce(code, name):
    result = Announce()
    
    startword = False
    startvalue = False
    startindex = 0
    valueindex = 0
    
    for i in range(0, len(code)):
        if startword == False and startvalue == False and code[i] not in WordEndList:
            startindex = i
            startword = True
            
        if startword and code[i] in WordEndList:
            word = code[startindex : i]
            startword = False
            
            if word in CSAccessModifier:
                result.AccessModifier = word
            elif word == "static":
                result.StaticModifier = word
            elif word in CSDataType:
                result.DataType = word
                if FindNextChar(code[i : ]) == '[':
                    startvalue = True
                    valueindex = (i + 1)
            
            if startvalue and code[i] == ']':
                startvalue = False
                result.ArrayValue = code[valueindex : i]
            if code[i] == '=':
                result.Value = code[FindNextCharIndex(code[i + 1 : ], FindNextChar(code[i + 1 : ])) + i + 1 : FindNextCharIndex(code, ';')]
                
    return result

## 조건문 변환
def ConvertCondition(code, name):
    result = Condition()
    
    finishindex = 0
    
    result.Target = name
    
    if FindNextChar(code) in CompareOperator:
        result.Operator = FindNextChar(code)
        finishindex = FindNextCharIndex(code, result.Operator) + 1
    elif FindNextCharLength(code, 2) in CompareOperator:
        result.Operator = FindNextCharLength(code, 2)
        finishindex = FindNextCharIndex(code, FindNextChar(code)) + 2
        
    result.Value = code[finishindex : ]
    
    return result

## (코드 추출 추가 메소드) 바로 다음의 글자 찾기 
def FindNextChar( code ):
    for i in range( 0, len(code) ):
        if code[i] != ' ' and code[i] != '\n' and code[i] != '\n':
            return code[i]
    return 0

## (코드 추출 추가 메소드) 다음의 글자 count개 찾기
def FindNextCharLength( code, count ):
    for i in range( 0, len(code) ):
        if code[i] != ' ' and code[i] != '\n' and code[i] != '\n':
            return code[i : i + count]
        
    return 0

## (코드 추출 추가 메소드) target 글자의 위치 찾기
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

## (코드 추출 추가 메소드) 범위 구하기
def FindRange( code, startrange ):
    count = 0
    start = False
    
    rangeindex = StartRange.index(startrange)
    
    for i in range(0, len(code)):
        if code[i] == StartRange[rangeindex]:
            count += 1
            start = True
        if code[i] == EndRange[rangeindex]:
            count -= 1
        
        if count == 0 and start == True:
            return i
        
    return 0
    

## 코드 변환 (1 = C / 2 = C# / 3 = C++ / 4 = Python / 5 = Java)
def ConvertCode( code ):
    result = code
    return result

## 코드 결합
def CombineCode( code ):
    result = ""
    return result

## 목록
class Container():
    Announces = []
    Conditions = []
    Functions = []
    IfMethods = []

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

class If_Method():
    Condition = []
    Value = []
    Else = None

class Method_For():
    First = None
    Condition = None
    Change = None
    Value = []