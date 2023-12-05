from ast import Compare
from os import sep
from typing import Container
from inspect import indentsize

BaseRule    = []
CPPRule      = []

WordEndList = [" ", "=", ";", "(", ")", "{", "}", "[", "]", ">", "<", "\n", "\r"]

ConditionOperator = [">", "<", ">=", "<=", "==", "!="]
AnnounceOperator = ["=", "+=", "-=", "++", "--"]
StartRange = ["(", "{", "["]
EndRange = [")", "}", "]"]
CPPAccessModifier = ["public", "private", "protected"]
CPPDataType = ["int", "long", "char", "bool", "double", "short", "float"]
CPPStatic = ["static"]

ContainAll = CPPAccessModifier + CPPDataType + CPPStatic

## 코드 변환 base -> CPP
def ConvertCodeToCPP( container, depth ):
    result = container
    
    for i in range(0, len(container.Announces)):
        if result.Announces[i].AccessModifier in BaseRule:
            result.Announces[i].AccessModifier = CPPRule[BaseRule.index(result.Announces[i].AccessModifier)]
        elif result.Announces[i].StaticModifier in BaseRule:
            result.Announces[i].StaticModifier = CPPRule[BaseRule.index(result.Announces[i].StaticModifier)]
        elif result.Announces[i].DataType in BaseRule:
            result.Announces[i].DataType = CPPRule[BaseRule.index(result.Announces[i].DataType)]
      
    return CombineCode(result, depth)

## 코드 변환 CPP -> base
def ConvertCodeToBase( container ):
    result = container
    
    for i in range(0, len(container.Announces)):
        if result.Announces[i].AccessModifier in CPPRule:
            result.Announces[i].AccessModifier = BaseRule[CPPRule.index(result.Announces[i].AccessModifier)]
        elif result.Announces[i].StaticModifier in CPPRule:
            result.Announces[i].StaticModifier = BaseRule[CPPRule.index(result.Announces[i].StaticModifier)]
        elif result.Announces[i].DataType in CPPRule:
            result.Announces[i].DataType = BaseRule[CPPRule.index(result.Announces[i].DataType)]
    
    return result
    

## 코드 결합
def CombineCode( code, depth ):
    result = ""
    announceC = 0
    ifC = 0
    forC = 0
    whileC = 0
    
    for i in range(0, len(code.IndexList)):
        if code.IndexList[i] == "Announce":
            temp = ""
            temp += IndentSpace(depth)
            
            if AlreadyUsed(code.UsingName, code.Announces[announceC].Name) == False:
                if code.Announces[announceC].AccessModifier != "default":
                    temp += code.Announces[announceC].AccessModifier + " "
                if code.Announces[announceC].StaticModifier != "default":
                    temp += code.Announces[announceC].StaticModifier + " "
                if code.Announces[announceC].DataType != "default" and code.Announces[announceC].ArrayValue == None:
                    temp += code.Announces[announceC].DataType + " "
                elif code.Announces[announceC].DataType != "default" and code.Announces[announceC].ArrayValue != None:
                    temp += code.Announces[announceC].DataType + "[" + code.Announces[announceC].ArrayValue + "] "
                    
                code.AddUsingName(code.Announces[announceC].Name)
                
            temp += code.Announces[announceC].Name
            if code.Announces[announceC].Value != None:
                temp += " = "
                temp += code.Announces[announceC].Value
            temp += ";"
            temp += "\n"
            result += temp
            announceC += 1
            
        elif code.IndexList[i] == "IfMethod":
            temp = ""
        
            for j in range(0, len(code.IfMethods[ifC].Condition)):
                temp += IndentSpace(depth)
                
                if j != 0:
                    temp += "else "
                
                temp += "if (" + code.IfMethods[ifC].Condition[j].Target + " " + code.IfMethods[ifC].Condition[j].Operator + " " + code.IfMethods[ifC].Condition[j].Value + ")\n"
                
                temp += IndentSpace(depth)+ "{\n"
                depth += 1
                code.IfMethods[ifC].Value[j].UsingName += code.UsingName
                temp += ConvertCodeToCPP(code.IfMethods[ifC].Value[j], depth)
                depth -= 1
                temp += IndentSpace(depth) + "}\n"
                
            if code.IfMethods[ifC].Else != None:
                temp += IndentSpace(depth) + "else\n"
                
                temp += IndentSpace(depth) + "{\n"
                depth += 1
                code.IfMethods[ifC].Else.UsingName += code.UsingName
                temp += ConvertCodeToCPP(code.IfMethods[ifC].Else, depth) + "\n"
                depth -= 1
                temp += IndentSpace(depth) + "}\n"
        
            result += temp
            ifC += 1
            
        elif code.IndexList[i] == "ForMethod":
            temp = ""
            temp += IndentSpace(depth)
            
            tempCon = Container()
            
            tempCon.AddAnnounces(code.ForMethods[forC].Announce)
            temp += "for(" + ConvertCodeToCPP(tempCon, 0).replace('\n', '') + " " 
            tempCon.UsingName += code.UsingName
            temp += code.ForMethods[forC].Condition.Target + " " + code.ForMethods[forC].Condition.Operator + " " + code.ForMethods[forC].Condition.Value + '; '
            
            tempCon = Container()
            tempCon.AddAnnounces(code.ForMethods[forC].Operator)
            tempCon.UsingName += code.UsingName
            temp += ConvertCodeToCPP(tempCon, 0).replace('\n', '').rstrip(';') + ")\n"
            
            del tempCon
            
            temp += IndentSpace(depth)+ "{\n"
            depth += 1
            code.ForMethods[forC].Value.UsingName += code.UsingName
            temp += ConvertCodeToCPP(code.ForMethods[forC].Value, depth)
            depth -= 1
            temp += IndentSpace(depth) + "}\n"
            
            result += temp
            forC += 1
            
        elif code.IndexList[i] == "WhileMethod":
            temp = ""
            temp += IndentSpace(depth)
            
            temp += "while(" + code.WhileMethods[whileC].Condition.Target + " " + code.WhileMethods[whileC].Condition.Operator + " " + code.WhileMethods[whileC].Condition.Value + ")\n"
            temp += IndentSpace(depth) + "{\n"
            depth += 1
            code.WhileMethods[whileC].Value.UsingName += code.UsingName
            temp += ConvertCodeToCPP(code.WhileMethods[whileC].Value, depth)
            depth -= 1
            temp += IndentSpace(depth) + "}\n"
            
            result += temp
            whileC += 1
            
    return result


def IndentSpace(depth):
    return " " * (depth * 4)

def AlreadyUsed(using, name):
    for i in range(0, len(using)):
        if using[i] == name:
            return True
    return False

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
                
                if word not in CPPAccessModifier and word not in CPPDataType and word != "static":
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
                
                if word == "while":
                    conditionstart = i + FindNextCharIndex(code[i : ], "(") + 1
                    conditionend = i + FindRange(code[i : ], "(")
                    
                    actionstart = conditionend + FindNextCharIndex(code[conditionend : ], "{") + 1
                    actionend = conditionend + FindRange(code[conditionend : ], "{")
                    
                    result.AddWhileMethods(ConvertWhileMethod(code[conditionstart : conditionend],code[actionstart : actionend]))
                    
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
            
            if word in CPPAccessModifier:
                result.AccessModifier = word
            elif word == "static":
                result.StaticModifier = word
            elif word in CPPDataType:
                result.DataType = word
                if FindNextChar(code[i : ]) == '[':
                    startvalue = True
                    valueindex = (i + 1)
            
            if startvalue and code[i] == ']':
                startvalue = False
                result.ArrayValue = code[valueindex : i]
            
        if code[i] == '=':
            result.Value = code[FindNextCharIndex(code[i + 1 : ], FindNextChar(code[i + 1 : ])) + i + 1 : FindNextCharIndex(code, ';')].strip()
            return result
            
        elif code[i : i + 2] in AnnounceOperator:
            result.Value = code[FindNextCharIndex(code[i + 2 : ], FindNextChar(code[i + 2 : ])) + i + 1 : FindNextCharIndex(code, ';')].strip()
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
        
    result.Value = code[finishindex : ].strip()
    
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

def ConvertWhileMethod(con, value):
    result = While_Method()
    
    result.Condition = ConvertCondition(con)
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
            result.AddCondition(ConvertCondition(code[startrange : conditionrange]))
                    
            startrange = conditionrange + FindNextCharIndex(code[conditionrange : ], "{") + 1
            valuerange = conditionrange + FindRange(code[conditionrange : ], "{")
            result.AddValue(Extraction(code[startrange : valuerange]))
            
            index += valuerange + 1
            
        elif FindNextWord(code[index : ]) == "else":
            if FindNextCharLength(code[index + 4 : ], 2) == "if":
                startrange = index + FindNextCharIndex(code[index : ], "(") + 1
                conditionrange = index + FindRange(code[index : ], "(")
                result.AddCondition(ConvertCondition(code[startrange : conditionrange]))
                    
                startrange = conditionrange + FindNextCharIndex(code[conditionrange : ], "{") + 1
                valuerange = conditionrange + FindRange(code[conditionrange : ], "{")
                result.AddValue(Extraction(code[startrange : valuerange]))
                
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
        self.WhileMethods = []
        self.IndexList = []
        self.UsingName = []
        
    def AddAnnounces(self, announce):
        self.Announces.append(announce)
        self.IndexList.append("Announce")
        
    def AddIfMethods(self, ifmethod):
        self.IfMethods.append(ifmethod)
        self.IndexList.append("IfMethod")
        
    def AddForMethods(self, formethod):
        self.ForMethods.append(formethod)
        self.IndexList.append("ForMethod")
        
    def AddWhileMethods(self, whilemethod):
        self.WhileMethods.append(whilemethod)
        self.IndexList.append("WhileMethod")
        
    def AddUsingName(self, usingname):
        self.UsingName.append(usingname)

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

class While_Method():
    Condition = None
    Value = None