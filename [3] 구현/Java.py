from inspect import indentsize

BaseRule    = ["string", "int", "char"]
JavaRule    = ["String", "Int", "Char"]

intra = 0

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
      
    return CombineCode(result, 0)

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
            
            temp += "if (" + code.IfMethods[i].Condition[j].Target + " " + code.IfMethods[i].Condition[j].Operator + " " + code.IfMethods[i].Condition[j].Value + ")\n"
            
            temp += IndentSpace(depth)+ "{\n"
            depth += 1
            temp += CombineCode(code.IfMethods[i].Value[j], depth)
            depth -= 1
            temp += IndentSpace(depth) + "}\n"
            
        if code.IfMethods[i].Else != None:
            temp += IndentSpace(depth) + "else\n"
            
            temp += IndentSpace(depth) + "{\n"
            depth += 1
            temp += CombineCode(code.IfMethods[i].Else, depth) + "\n"
            depth -= 1
            temp += IndentSpace(depth) + "}\n"
    
        result += temp
        
    del code
    
    return result

def IndentSpace(depth):
    return " " * (depth * 4)

class Container():
    Announces = []
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

class Method_If():
    Condition = []
    Value = []
    Else = None

class Method_For():
    First = None
    Condition = None
    Change = None
    Value = []