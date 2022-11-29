from ast import Compare
from os import sep
from typing import Container
from inspect import indentsize

BaseRule    = []
CSRule      = []

WordEndList = [" ", "=", ";", "(", ")", "{", "}", "[", "]", ">", "<", "\n", "\r"]

ConditionOperator = [">", "<", ">=", "<=", "==", "!="]
AnnounceOperator = ["=", "+=", "-=", "++", "--"]
StartRange = ["(", "{", "["]
EndRange = [")", "}", "]"]
CSAccessModifier = ["public", "private", "protected", "default"]
CSDataType = ["int", "string", "long", "char", "bool", "double", "shot", "float"]
CSStatic = ["static"]

ContainAll = CSAccessModifier + CSDataType + CSStatic

## 코드 변환 base -> CS
def ConvertCodeToCS( container, depth ):
    result = container
    
    for i in range(0, len(container.Announces)):
        if result.Announces[i].AccessModifier in BaseRule:
            result.Announces[i].AccessModifier = CSRule[BaseRule.index(result.Announces[i].AccessModifier)]
        elif result.Announces[i].StaticModifier in BaseRule:
            result.Announces[i].StaticModifier = CSRule[BaseRule.index(result.Announces[i].StaticModifier)]
        elif result.Announces[i].DataType in BaseRule:
            result.Announces[i].DataType = CSRule[BaseRule.index(result.Announces[i].DataType)]
      
    return CombineCode(result, depth)

## 코드 변환 CS -> base
def ConvertCodeToBase( container ):
    result = container
    
    for i in range(0, len(container.Announces)):
        if result.Announces[i].AccessModifier in CSRule:
            result.Announces[i].AccessModifier = BaseRule[CSRule.index(result.Announces[i].AccessModifier)]
        elif result.Announces[i].StaticModifier in CSRule:
            result.Announces[i].StaticModifier = BaseRule[CSRule.index(result.Announces[i].StaticModifier)]
        elif result.Announces[i].DataType in CSRule:
            result.Announces[i].DataType = BaseRule[CSRule.index(result.Announces[i].DataType)]
    
    return result
    

## 코드 결합
def CombineCode( code, depth ):
    result = ""
    
    for i in range(0, len(code.Announces)):
        temp = ""
        temp += IndentSpace(depth)
        
        if code.Announces[i].AccessModifier != "default":
            temp += code.Announces[i].AccessModifier + " "
        if code.Announces[i].StaticModifier != "default":
            temp += code.Announces[i].StaticModifier + " "
        if code.Announces[i].DataType != "default" and code.Announces[i].ArrayValue == None:
            temp += code.Announces[i].DataType + " "
        elif code.Announces[i].DataType != "default" and code.Announces[i].ArrayValue != None:
            temp += code.Announces[i].DataType + "[" + code.Announces[i].ArrayValue + "] "
        temp += code.Announces[i].Name
        if code.Announces[i].Value != None:
            temp += " = "
            temp += code.Announces[i].Value
        temp += ";"
        temp += "\n"
        result += temp
    
    for i in range(0, len(code.IfMethods)):
        temp = ""
        
        for j in range(0, len(code.IfMethods[i].Condition)):
            temp += IndentSpace(depth)
            
            if j != 0:
                temp += "else "
            
            temp += "if (" + code.IfMethods[i].Condition[j].Target + " " + code.IfMethods[i].Condition[j].Operator + code.IfMethods[i].Condition[j].Value + ")\n"
            
            temp += IndentSpace(depth)+ "{\n"
            depth += 1
            temp += ConvertCodeToCS(code.IfMethods[i].Value[j], depth)
            depth -= 1
            temp += IndentSpace(depth) + "}\n"
            
        if code.IfMethods[i].Else != None:
            temp += IndentSpace(depth) + "else\n"
            
            temp += IndentSpace(depth) + "{\n"
            depth += 1
            temp += ConvertCodeToCS(code.IfMethods[i].Else, depth) + "\n"
            depth -= 1
            temp += IndentSpace(depth) + "}\n"
    
        result += temp
        
    for i in range(0, len(code.ForMethods)):
        temp = ""
        temp += IndentSpace(depth)
        
        tempCon = Container()
        
        tempCon.AddAnnounces(code.ForMethods[i].Announce)
        
        temp += "for(" + ConvertCodeToCS(tempCon, 0).replace('\n', '') + " " 
        temp += code.ForMethods[i].Condition.Target + " " + code.ForMethods[i].Condition.Operator + " " + code.ForMethods[i].Condition.Value + '; '
        
        tempCon.Announces.clear()
        tempCon.AddAnnounces(code.ForMethods[i].Operator)
        
        temp += ConvertCodeToCS(tempCon, 0).replace('\n', '') + ")\n"
        
        tempCon.Announces.clear()
        
        temp += IndentSpace(depth)+ "{\n"
        depth += 1
        temp += ConvertCodeToCS(code.ForMethods[i].Value, depth)
        depth -= 1
        temp += IndentSpace(depth) + "}\n"
        
        result += temp
    
    del code
    return result

def IndentSpace(depth):
    return " " * (depth * 4)


## 주어진 코드 추출
def Extraction( code ):
    code += "     "
    
    result = Container()
    
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
                        result.AddAnnounces(ConvertAnnounce(code[finishindex : i + (FindNextCharIndex(code[i : ], ';'))] + ';'))
                        
                        finishindex = (i + 1 + FindNextCharIndex(code[i : ], ';'))
                
                ## if 문의 경우
                if word == "if":
                    pointA = i
                    
                    while True:
                        pointA += FindRange(code[pointA : ], "{")
                        
                        if FindNextCharLength(code[pointA + 1 : ], 4) == "else":
                            continue
                        
                        break
                    
                    result.AddIfMethods(ConvertIfMethod(code[wordindex : pointA + 1]))
                    
                    finishindex = pointA + 1
                
                # for 문의 경우
                if word == "for":
                    conditionstart = i + FindNextCharIndex(code[i : ], "(") + 1
                    conditionend = i + FindRange(code[i : ], "(")
                    
                    actionstart = conditionend + FindNextCharIndex(code[conditionend : ], "{") + 1
                    actionend = conditionend + FindRange(code[conditionend : ], "{")
                    
                    result.AddForMethods(ConvertForMethod(code[conditionstart : conditionend], code[actionstart : actionend]))
                    
                    finishindex = actionend + 1
                    
    return ConvertCodeToBase(result)


## 선언문 변환
def ConvertAnnounce(code):
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
            
            if word not in ContainAll:
                result.Name = word
            
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
            
        elif code[i : i + 2] in AnnounceOperator:
            result.Value = code[FindNextCharIndex(code[i + 2 : ], FindNextChar(code[i + 2 : ])) + i + 1 : FindNextCharIndex(code, ';')]
            return result
                            
    return result

## 조건문 변환
def ConvertCondition(code):
    result = Condition()
    
    finishindex = 0

    result.Target = FindNextWord(code)
    index = FindNextWordLastIndex(code)
    
    if FindNextChar(code[index : ]) in ConditionOperator:
        result.Operator = FindNextChar(code[index : ])
        finishindex = index + FindNextCharIndex(code[index : ], result.Operator) + 1
        
    elif FindNextCharLength(code[index : ], 2) in ConditionOperator:
        result.Operator = FindNextCharLength(code[index : ], 2)
        finishindex = index + FindNextCharIndex(code[index : ], FindNextChar(code[index : ])) + 2
        
    result.Value = code[finishindex : ]
    
    return result

def ConvertForMethod(con, value):
    result = For_Method()
    
    start = 0
    end = FindNextCharIndex(con[start : ], ';')
    result.Announce = ConvertAnnounce(con[start : end + 1])
    
    start = end + 1
    end = start + FindNextCharIndex(con[start : ], ';')
    result.Condition = ConvertCondition(con[start : end])
    
    start = end + 1
    result.Operator = ConvertAnnounce((con[start : ] + ';')) 
    
    result.Value = Extraction(value)
    
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
        
    return 0

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

## 목록
class Container():
    
    def __init__(self):
        self.Announces = []
        self.IfMethods = []
        self.ForMethods = []
        
    def AddAnnounces(self, announce):
        self.Announces.append(announce)
        
    def AddIfMethods(self, ifmethod):
        self.IfMethods.append(ifmethod)
        
    def AddForMethods(self, ifmethod):
        self.ForMethods.append(ifmethod)
        
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
    Else = None
    
    def __init__(self):
        self.Condition = []
        self.Value = []
    
    def AddCondition(self, condition):
        self.Condition.append(condition)
        
    def AddValue(self, value):
        self.Value.append(value)

class For_Method():
    Announce = None
    Condition = None
    Operator = None
    Value = None