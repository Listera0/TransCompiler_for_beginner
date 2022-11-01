BaseRule    = ["string", "int", "char"]
JavaRule    = ["String", "Int", "Char"]

## 코드 변환 (1 = C / 2 = C# / 3 = C++ / 4 = Python / 5 = Java)
def ConvertCode( container ):
    result = container
    
    for i in range(0, len(container.Announces)):
        if result.Announces[i].AccessModifier in BaseRule:
            result.Announces[i].AccessModifier = JavaRule[BaseRule.index(result.Announces[i].AccessModifier)]
        elif result.Announces[i].StaticModifier in BaseRule:
            result.Announces[i].StaticModifier = JavaRule[BaseRule.index(result.Announces[i].StaticModifier)]
        elif result.Announces[i].DataType in BaseRule:
            result.Announces[i].DataType = JavaRule[BaseRule.index(result.Announces[i].DataType)]
            
    return CombineCode(result)

## 코드 결합
def CombineCode( code ):
    result = ""
    
    for i in range(0, len(code.Announces)):
        temp = ""
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
        
    code.Announces.clear()
    
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