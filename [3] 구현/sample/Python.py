BaseRule    = ["public", "protected", "private"]
PythonRule    = ["default", "_", "__"]

PythonAccessModifier = ["", "_", "__"]

## 코드 변환 (1 = C / 2 = C# / 3 = C++ / 4 = Python / 5 = Java)
def ConvertCode( container, depth ):
    result = container
    
    for i in range(0, len(container.Announces)):
        if result.Announces[i].AccessModifier in BaseRule:
            result.Announces[i].AccessModifier = PythonRule[BaseRule.index(result.Announces[i].AccessModifier)]
        elif result.Announces[i].StaticModifier in BaseRule:
            result.Announces[i].StaticModifier = PythonRule[BaseRule.index(result.Announces[i].StaticModifier)]
        elif result.Announces[i].DataType in BaseRule:
            result.Announces[i].DataType = PythonRule[BaseRule.index(result.Announces[i].DataType)]
            
    return CombineCode(result, depth)

## 코드 결합
def CombineCode( code, depth):
    result = ""
    
    for i in range(0, len(code.Announces)):
        temp = ""
        temp += IndentSpace(depth)
        
        if code.Announces[i].AccessModifier != "default":
            temp += code.Announces[i].AccessModifier
        temp += code.Announces[i].Name
        if code.Announces[i].Value != None:
            temp += " = "
            temp += code.Announces[i].Value
        temp += "\n"
        result += temp
        
    for i in range(0, len(code.IfMethods)):
        temp = ""
        
        for j in range(0, len(code.IfMethods[i].Condition)):
            temp += IndentSpace(depth)
            
            if j != 0:
                temp += "el"
            
            temp += "if " + code.IfMethods[i].Condition[j].Target + " " + code.IfMethods[i].Condition[j].Operator + " " + code.IfMethods[i].Condition[j].Value + ":\n"
            
            depth += 1
            temp += CombineCode(code.IfMethods[i].Value[j], depth)
            depth -= 1
            temp += IndentSpace(depth) + "\n"
            
        if code.IfMethods[i].Else != None:
            temp += IndentSpace(depth) + "else:\n"
            depth += 1
            temp += CombineCode(code.IfMethods[i].Else, depth) + "\n"
            depth -= 1
            temp += IndentSpace(depth) + "\n"
            
        result += temp
        
    for i in range(0, len(code.ForMethods)):
        temp = ""
        temp += IndentSpace(depth)
        
        temp += "for " + code.ForMethods[i].Announce.Name + " in range(" + code.ForMethods[i].Announce.Value + "," + code.ForMethods[i].Condition.Value + "):\n"
        
        depth += 1
        temp += ConvertCode(code.ForMethods[i].Value, depth)
        depth -= 1
        temp += IndentSpace(depth) + "\n"
        
        result += temp
    
        
    del code
    return result

def IndentSpace(depth):
    return " " * (depth * 4)

## 목록
class Container():
    Announces = []
    IfMethods = []
    ForMethods = []
    
    def __new__(cls):
        obj = super().__new__(cls)
        return obj
    
class tempContainer():
    Announces = []
    IfMethods = []
    ForMethods = []

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

class For_Method():
    Announce = None
    Condition = None
    Operator = None
    Value = None