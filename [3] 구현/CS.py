from ast import Compare
from os import sep
from typing import Container

BaseRule    = ["string", "int", "char"]
CSRule      = ["string", "int", "char"]

WordEndList = [" ", "=", ";", "(", ")", "{", "}", "[", "]", ">", "<", "\n", "\r"]

CompareOperator = [">", "<", ">=", "<=", "==", "!="]
StartRange = ["(", "{", "["]
EndRange = [")", "}", "]"]
CSAccessModifier = ["public", "private", "protected", "default"]
CSDataType = ["int", "string", "long", "char"]

ContainAll = CSAccessModifier + CSDataType

## 주어진 코드 추출
def Extraction( code ):
    code += "     "
    
    result = Container()
    
    result.Announces.clear()
    result.IfMethods.clear()
    
    word = None
    
    isword = False
    ismethod = False
    isannounce = False
    
    wordindex = 0
    
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
                
                ## if 문의 경우
                if word == "if":
                    pointA = i
                    
                    while True:
                        pointA += FindRange(code[pointA : ], "{")
                        
                        if FindNextCharLength(code[pointA + 1 : ], 4 == "else"):
                            continue
                        
                        break
                    
                    result.IfMethods.append(ConvertIfMethod(code[wordindex : pointA + 1]))
                    
                    finishindex = pointA + 1
                    
                    
    print(str(len(result.Announces)))
    print(str(len(result.IfMethods)))
    return result

## 선언문 변환
def ConvertAnnounce(code, name):
    result = Announce()
    startword = False
    startvalue = False
    startindex = 0
    valueindex = 0
    
    result.Name = name
    
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
                            
    return result

## 조건문 변환
def ConvertCondition(code):
    result = Condition()
    
    finishindex = 0

    result.Target = FindNextWord(code)
    index = FindNextWordLastIndex(code)
    
    if FindNextChar(code[index : ]) in CompareOperator:
        result.Operator = FindNextChar(code[index : ])
        finishindex = index + FindNextCharIndex(code[index : ], result.Operator) + 1
        
    elif FindNextCharLength(code[index : ], 2) in CompareOperator:
        result.Operator = FindNextCharLength(code[index : ], 2)
        finishindex = index + FindNextCharIndex(code[index : ], FindNextChar(code[index : ])) + 2
        
    result.Value = code[finishindex : ]
    
    return result

def ConvertIfMethod(code):
    result = If_Method()
    result.Condition.clear()
    result.Value.clear()
    
    index = 0
    
    for i in range(len(code)):
        if FindNextWord(code[index : ]) == "if":
            startrange = index + FindNextCharIndex(code[index : ], "(") + 1
            conditionrange = index + FindRange(code[index : ], "(")
            result.Condition.append(ConvertCondition(code[startrange : conditionrange]))
                    
            startrange = conditionrange + FindNextCharIndex(code[conditionrange : ], "{") + 1
            valuerange = conditionrange + FindRange(code[conditionrange : ], "{")
            result.Value.append(Extraction(code[startrange : valuerange]))
            
            index += valuerange + 1
            
        elif FindNextWord(code[index : ]) == "else":
            if FindNextCharLength(code[index + 4 : ], 2) == "if":
                startrange = index + FindNextCharIndex(code[index : ], "(") + 1
                conditionrange = index + FindRange(code[index : ], "(")
                result.Condition.append(ConvertCondition(code[startrange : conditionrange]))
                    
                startrange = conditionrange + FindNextCharIndex(code[conditionrange : ], "{") + 1
                valuerange = conditionrange + FindRange(code[conditionrange : ], "{")
                result.Value.append(Extraction(code[startrange : valuerange]))
                
                index += valuerange + 1
            else:
                startrange = index + FindNextCharIndex(code[index : ], "{") + 1
                valuerange = index + FindRange(code[index : ], "{")
                result.Else = Extraction(code[startrange : valuerange])
                
                break
                
        else:
            break
    
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

## (코드 추출 추가 메소드) 바로 다음의 단어 찾기
def FindNextWordLastIndex( code ):
    word = None
    startindex = 0
    startword = False
    
    for i in range(0, len(code)):
        if startword == False and code[i] not in WordEndList:
            startindex = i
            startword = True
        
        if startword and code[i] in WordEndList:
            return i
        
    return i

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
    IfMethods = []
    
    def __new__(cls):
        obj = super().__new__(cls)
        return obj

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