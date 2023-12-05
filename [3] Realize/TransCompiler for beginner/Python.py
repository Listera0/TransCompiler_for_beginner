from ast import Compare
from os import sep
from typing import Container
from inspect import indentsize

BaseRule    = ["public", "protected", "private"]
PythonRule    = ["default", "_", "__"]

WordEndList = [" ", "=", ";", "(", ")", "{", "}", "[", "]", ">", "<", "\n", "\r"]

ConditionOperator = [">", "<", ">=", "<=", "==", "!="]
AnnounceOperator = ["=", "+=", "-="]
StartRange = ["(", "{", "[", ":"]
EndRange = [")", "}", "]", ":"]
PythonAccessModifier = ["_", "__"]
PythonDataType = ["int", "string", "long", "char", "bool", "double", "short", "float"]
PythonStatic = ["static"]

MethodStartList = ["if", "for", "while"]

ContainAll = PythonAccessModifier + PythonDataType + PythonStatic

## 코드 변환 Base -> Python
def ConvertCodeToPython( container, depth ):
    result = container
    
    for i in range(0, len(container.Announces)):
        if result.Announces[i].AccessModifier in BaseRule:
            result.Announces[i].AccessModifier = PythonRule[BaseRule.index(result.Announces[i].AccessModifier)]
        elif result.Announces[i].StaticModifier in BaseRule:
            result.Announces[i].StaticModifier = PythonRule[BaseRule.index(result.Announces[i].StaticModifier)]
        elif result.Announces[i].DataType in BaseRule:
            result.Announces[i].DataType = PythonRule[BaseRule.index(result.Announces[i].DataType)]
            
    return CombineCode(result, depth)

## 코드 변환 Python -> base
def ConvertCodeToBase( container ):
    result = container
    
    for i in range(0, len(container.Announces)):
        if result.Announces[i].AccessModifier in PythonRule:
            result.Announces[i].AccessModifier = BaseRule[PythonRule.index(result.Announces[i].AccessModifier)]
        elif result.Announces[i].StaticModifier in PythonRule:
            result.Announces[i].StaticModifier = BaseRule[PythonRule.index(result.Announces[i].StaticModifier)]
        elif result.Announces[i].DataType in PythonRule:
            result.Announces[i].DataType = BaseRule[PythonRule.index(result.Announces[i].DataType)]
    
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
            
            ## if AlreadyUsed(code.UsingName, code.Announces[announceC].Name) == False:
            if code.Announces[announceC].AccessModifier != "default":
                temp += code.Announces[announceC].AccessModifier    
            
            temp += code.Announces[announceC].Name
            if code.Announces[announceC].Value != None:
                temp += " = "
                temp += code.Announces[announceC].Value
            temp += "\n"
            result += temp
            announceC += 1
            
        elif code.IndexList[i] == "IfMethod":
            temp = ""
        
            for j in range(0, len(code.IfMethods[ifC].Condition)):
                temp += IndentSpace(depth)
                
                if j != 0:
                    temp += "el"
                
                temp += "if " + code.IfMethods[ifC].Condition[j].Target + " " + code.IfMethods[ifC].Condition[j].Operator + " " + code.IfMethods[ifC].Condition[j].Value + ":\n"
                depth += 1
                code.IfMethods[ifC].Value[j].UsingName += code.UsingName
                temp += ConvertCodeToPython(code.IfMethods[ifC].Value[j], depth)
                depth -= 1
                temp += IndentSpace(depth) + "\n"
                
            if code.IfMethods[ifC].Else != None:
                temp += IndentSpace(depth) + "else:\n"
                depth += 1
                code.IfMethods[ifC].Else.UsingName += code.UsingName
                temp += ConvertCodeToPython(code.IfMethods[ifC].Else, depth) + "\n"
                depth -= 1
                temp += IndentSpace(depth) + "\n"
                
            result += temp
            ifC += 1
            
        elif code.IndexList[i] == "ForMethod":
            temp = ""
            temp += IndentSpace(depth)
            
            temp += "for " + code.ForMethods[forC].Announce.Name + " in range(" + code.ForMethods[forC].Announce.Value + "," + code.ForMethods[forC].Condition.Value + "):\n"
            
            depth += 1
            code.ForMethods[forC].Value.UsingName += code.UsingName
            temp += ConvertCodeToPython(code.ForMethods[forC].Value, depth)
            depth -= 1
            temp += IndentSpace(depth) + "\n"
            
            result += temp
            forC += 1
            
        elif code.IndexList[i] == "WhileMethod":
            temp = ""
            temp += f"while {code.WhileMethods[whileC].Condition.Target} {code.WhileMethods[whileC].Condition.Operator} {code.WhileMethods[whileC].Condition.Value}:\n"
            depth += 1
            code.WhileMethods[whileC].Value.UsingName += code.UsingName
            temp += ConvertCodeToPython(code.WhileMethods[whileC].Value, depth)
            depth -= 1
            temp += f"{IndentSpace(depth)}\n"
            
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
    result = Container()
    
    word = None
    
    isword = False
    ismethod = False
    isannounce = False
    
    Flag = 0
    
    wordindex = 0
    
    finishindex = 0
    
    code = code.replace('\r', '')
    if code[-1] == '\n':
        code = code.rstrip('\n')
    splitcode = code.split('\n')
    
    for i in range(0, len(splitcode)):
        indent = FindNextCharIndex(splitcode[i], FindNextChar(splitcode[i]))
        
        if i >= finishindex:
            if FindNextWord(splitcode[i]) == "if":
                for j in range(i + 1, len(splitcode)):
                    if FindNextCharIndex(splitcode[j], FindNextChar(splitcode[j])) < indent:
                        tempcode = ""
                        for n in range(i, j):
                            tempcode += splitcode[n] + "\n"
                        tempcode = tempcode.rstrip('\n')
                        result.AddIfMethods(ConvertIfMethod(tempcode))
                        finishindex = j
                        Flag = 1
                        break
                            
                    if FindNextCharIndex(splitcode[j], FindNextChar(splitcode[j])) == indent:
                        if FindNextWord(splitcode[j]) != "elif" and FindNextWord(splitcode[j]) != "else":
                            tempcode = ""
                            for n in range(i, j):
                                tempcode += splitcode[n] + "\n"
                            tempcode = tempcode.rstrip('\n')
                            result.AddIfMethods(ConvertIfMethod(tempcode))
                            finishindex = j
                            Flag = 1
                            break
                
                if Flag == 0:          
                    tempcode = ""
                    for n in range(i, len(splitcode)):
                        tempcode += splitcode[n] + "\n"
                    tempcode = tempcode.rstrip('\n')
                    result.AddIfMethods(ConvertIfMethod(tempcode))
                    finishindex = len(splitcode)
                    break
                else:
                    Flag = 0               
            
            elif FindNextWord(splitcode[i]) == "for":
                for j in range(i + 1, len(splitcode)):
                    if FindNextCharIndex(splitcode[j], FindNextChar(splitcode[j])) <= indent:
                        tempcode = ""
                        for n in range(i, j):
                            tempcode += splitcode[n] + "\n"
                        tempcode = tempcode.rstrip('\n')
                        result.AddForMethods(ConvertForMethod(tempcode))
                        finishindex = j
                        Flag = 1
                        break
                
                if Flag == 0:
                    tempcode = ""
                    for n in range(i, len(splitcode)):
                        tempcode += splitcode[n] + "\n"
                    tempcode = tempcode.rstrip('\n')
                    result.AddForMethods(ConvertForMethod(tempcode))
                    finishindex = len(splitcode)
                    break
                else:
                    Flag == 0
                    
            elif FindNextWord(splitcode[i]) == "while":
                for j in range(i + 1, len(splitcode)):
                    if FindNextCharIndex(splitcode[j], FindNextChar(splitcode[j])) <= indent:
                        tempcode = ""
                        for n in range(i, j):
                            tempcode += splitcode[n] + "\n"
                        tempcode = tempcode.rstrip('\n')
                        result.AddWhileMethods(ConvertWhileMethod(tempcode))
                        finishindex = j
                        Flag = 1
                        break
                
                if Flag == 0:
                    tempcode = ""
                    for n in range(i, len(splitcode)):
                        tempcode += splitcode[n] + "\n"
                    tempcode = tempcode.rstrip('\n')
                    result.AddWhileMethods(ConvertWhileMethod(tempcode))
                    finishindex = len(splitcode)
                    break
                else:
                    Flag == 0
            
            else:
                if FindNextWord(splitcode[i]) != None:
                    result.AddAnnounces(ConvertAnnounce(splitcode[i]))
                    pass
               
    return ConvertCodeToBase(result)


## 선언문 변환
def ConvertAnnounce(code):
    result = Announce()
    
    code = code.replace('\n', '')
     
    result.Name = FindNextWord(code)
    
    if FindNextWord(code)[ : 2] == "__":
        result.AccessModifier = "__"
        result.Name = FindNextWord(code)[2 : ]
    elif FindNextWord(code)[ : 1] == "_":
        result.AccessModifier = "_"
        result.Name = FindNextWord(code)[1 : ]
    else:
        result.AccessModifier = "default"
    
    result.Value = code[FindNextCharIndex(code, "=") + 1 : ].strip()
    
    if result.Value[ : 1] == "\"":
        result.DataType = "string"
    elif result.Value[ : 1] == "\'":
        result.DataType = "char"
    elif result.Value == "False" or result.Value == "True":
        result.DataType = "bool"
    else:
        result.DataType = "int"
        for i in range(len(result.Value)):
            if result.Value[i] == ".":
                result.DataType = "float"
                    
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


def ConvertForMethod(code):
    result = For_Method()
    
    splitcode = code.split('\n')
    
    index = FindNextWordLastIndex(splitcode[0])                                 ## for 거름
    name = FindNextChar(splitcode[0][index : ])                                 ## name
    
    index += FindNextWordLastIndex(splitcode[0][index : ])                      ## name 거름
    index += FindNextWordLastIndex(splitcode[0][index : ])                      ## in 거름
    
    index += FindNextCharIndex(splitcode[0][index : ], '(') + 1                     ## range 거름
    x = splitcode[0][index : index + FindNextCharIndex(splitcode[0][index : ], ',')]    ## x
    
    index += FindNextCharIndex(splitcode[0][index : ], ',') + 1                     ## , 거름
    y = splitcode[0][index : index + FindNextCharIndex(splitcode[0][index : ], ')')]    ## y
    
    result.Announce = ConvertAnnounce(name + " = " + str(x))
    result.Condition = ConvertCondition(name + " < " + str(y))
    result.Operator = ConvertAnnounce(f"{name} = {name} + 1")
    
    tempcode = ""
    for n in range(1, len(splitcode)):
        tempcode += splitcode[n] + "\n"
    tempcode = tempcode.rstrip('\n')
    result.Value = Extraction(tempcode)
    
    return result

def ConvertWhileMethod(code):
    result = While_Method()
    
    splitcode = code.split('\n')
    
    start = FindNextWordLastIndex(splitcode[0])
    end = FindNextCharIndex(splitcode[0], ':')
    
    result.Condition = ConvertCondition(splitcode[0][start : end])
    
    tempcode = ""
    for n in range(1, len(splitcode)):
        tempcode += splitcode[n] + "\n"
    tempcode = tempcode.rstrip('\n')
    result.Value = Extraction(tempcode)
    
    return result

def ConvertIfMethod(code):
    result = If_Method()
    
    splitcode = code.split('\n')
    indent = FindNextCharIndex(splitcode[0], FindNextChar(splitcode[0]))
    finishindex = 0
    
    for i in range(0, len(splitcode)):
        if i >= finishindex:
            if FindNextWord(splitcode[i]) == "if":
                result.AddCondition(ConvertCondition(splitcode[i][FindNextWordLastIndex(splitcode[i]) + 1 : FindNextCharIndex(splitcode[i], ':')]))
                for j in range(i + 1, len(splitcode)):
                    if FindNextCharIndex(splitcode[j], FindNextChar(splitcode[j])) < indent + 4:
                        tempcode = ""
                        for n in range(i + 1, j):
                            tempcode += splitcode[n] + "\n"
                        tempcode = tempcode.rstrip('\n')
                        result.AddValue(Extraction(tempcode))
                        finishindex = j
                        break
                tempcode = ""
                for n in range(i + 1, len(splitcode)):
                    tempcode += splitcode[n] + "\n"
                tempcode = tempcode.rstrip('\n')
                result.AddValue(Extraction(tempcode))
                finishindex = len(splitcode)
                        
            elif FindNextWord(splitcode[i]) == "elif":
                result.AddCondition(ConvertCondition(splitcode[i][FindNextWordLastIndex(splitcode[i]) : FindNextCharIndex(splitcode[i], ':')]))
                for j in range(i + 1, len(splitcode)):
                    if FindNextCharIndex(splitcode[j], FindNextChar(splitcode[j])) < indent + 4:
                        tempcode = ""
                        for n in range(i + 1, j):
                            tempcode += splitcode[n] + "\n"
                        tempcode = tempcode.rstrip('\n')
                        result.AddValue(Extraction(tempcode))
                        finishindex = j
                        break
                tempcode = ""
                for n in range(i + 1, len(splitcode)):
                    tempcode += splitcode[n] + "\n"
                tempcode = tempcode.rstrip('\n')
                result.AddValue(Extraction(tempcode))
                finishindex = len(splitcode)    
                
                        
            elif FindNextWord(splitcode[i]) == "else":
                for j in range(i + 1, len(splitcode)):
                    if FindNextCharIndex(splitcode[j], FindNextChar(splitcode[j])) < indent + 4:
                        tempcode = ""
                        for n in range(i + 1, j):
                            tempcode += splitcode[n] + "\n"
                        result.Else = Extraction(tempcode)
                        finishindex = j
                        break
                tempcode = ""
                for n in range(i + 1, len(splitcode)):
                    tempcode += splitcode[n] + "\n"
                tempcode = tempcode.rstrip('\n')
                result.Else = Extraction(tempcode)
                finishindex = len(splitcode)
                
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
    return "0"

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

## if문
class If_Method():
    Else = None
    
    def __init__(self):
        self.Condition = []
        self.Value = []
    
    def AddCondition(self, condition):
        self.Condition.append(condition)
        
    def AddValue(self, value):
        self.Value.append(value)

## for 문
class For_Method():
    Announce = None
    Condition = None
    Operator = None
    Value = None
    
class While_Method():
    Condition = None
    Value = None