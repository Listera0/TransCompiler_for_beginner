from inspect import indentsize

BaseRule    = ["string", "int", "char"]
JavaRule    = ["String", "Int", "Char"]

## 코드 변환 (1 = C / 2 = C# / 3 = C++ / 4 = Python / 5 = Java)
def ConvertCode( container, depth ):
    result = container
    
    for i in range(0, len(container.Announces)):
        if result.Announces[i].AccessModifier in BaseRule:
            result.Announces[i].AccessModifier = JavaRule[BaseRule.index(result.Announces[i].AccessModifier)]
        elif result.Announces[i].StaticModifier in BaseRule:
            result.Announces[i].StaticModifier = JavaRule[BaseRule.index(result.Announces[i].StaticModifier)]
        elif result.Announces[i].DataType in BaseRule:
            result.Announces[i].DataType = JavaRule[BaseRule.index(result.Announces[i].DataType)]
      
    return CombineCode(result, depth)

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
            temp += ConvertCode(code.IfMethods[i].Value[j], depth)
            depth -= 1
            temp += IndentSpace(depth) + "}\n"
            
        if code.IfMethods[i].Else != None:
            temp += IndentSpace(depth) + "else\n"
            
            temp += IndentSpace(depth) + "{\n"
            depth += 1
            temp += ConvertCode(code.IfMethods[i].Else, depth) + "\n"
            depth -= 1
            temp += IndentSpace(depth) + "}\n"
    
        result += temp
        
    for i in range(0, len(code.ForMethods)):
        temp = ""
        temp += IndentSpace(depth)
        
        tempCon = tempContainer()
        
        tempCon.Announces.append(code.ForMethods[i].Announce)
        
        temp += "for(" + ConvertCode(tempCon, 0).replace('\n', '') + " " 
        temp += code.ForMethods[i].Condition.Target + " " + code.ForMethods[i].Condition.Operator + " " + code.ForMethods[i].Condition.Value + '; '
        
        tempCon.Announces.clear()
        tempCon.Announces.append(code.ForMethods[i].Operator)
        
        temp += ConvertCode(tempCon, 0).replace('\n', '') + ")\n"
        
        tempCon.Announces.clear()
        
        temp += IndentSpace(depth)+ "{\n"
        depth += 1
        temp += ConvertCode(code.ForMethods[i].Value, depth)
        depth -= 1
        temp += IndentSpace(depth) + "}\n"
        
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