from enum import Enum


class Type(Enum):
    BOOL = 'bool'
    CHAR = 'char'
    INT = 'int'
    SHORT = 'short'
    FLOAT = 'float'
    DOUBLE = 'double'
    LONG = 'long'
    LONGLONG = 'long long'


class SpecialSymbol(Enum):
    #special symbols
    EXCLAMATION = '!'
    AT = '@'
    SHARP = '#'
    DOLLAR = '$'
    PERCENT = '%'
    TILDE = '~'
    CARET = '^'
    QUESTION = '?'
    AMPERSAND = '&'
    ASTERISK = '*'
    OPEN_BRACKET = '['
    CLOSE_BRACKET = ']'
    OPEN_BRACES = '{'
    CLOSE_BRACES = '}'
    OPEN_PARENTHESES = '('
    CLOSE_PARENTHESES = ')'
    #Comparison Operator
    GT = '>'
    GTE = '>='
    LT = '<'
    LTE = '<='
    EQ = '=='
    NE = '!='
    
    LSHIFT = '<<'
    RSHIFT = '>>' 
    
    SEMI_COLON = ';'
    COLON = ':'
    
    NEWLINE = '\n'
    BLANK = ' '
    EOF = '\0'
    
    #Logical Operator
    PLUS = '+'
    MINUS = '-'
    
    #Assignment Operator
    ADDASSIGN = '+=' #Addition Assignment Operator
    SUBASSIGN = '-=' #Subtraction Assiiignment Operator
    MULASSIGN = '*='
    DIVASSIGN = '/='
    MODASSIGN = '%='
    LSHIFTASSIGN = '<<='
    RSHIFTASSIGN = '>>='
    
    def isComparisonOperator(c):
        return (c == SpecialSymbol.GT.value or c == SpecialSymbol.GTE.value or
                c == SpecialSymbol.LT.value or c == SpecialSymbol.LTE.value or
                c == SpecialSymbol.EQ.value or c == SpecialSymbol.NE.value)

    def isLogicalOperatror(c):
        return (c == SpecialSymbol.PLUS.value or c == SpecialSymbol.MINUS.value)

    def isAssingmentOperator(c):
        return (c == SpecialSymbol.ADDASSIGN.value or c == SpecialSymbol.SUBASSIGN.value or
                c == SpecialSymbol.MULASSIGN.value or c == SpecialSymbol.DIVASSIGN.value or
                c == SpecialSymbol.MODASSIGN.value or c == SpecialSymbol.LSHIFTASSIGN.value or
                c == SpecialSymbol.RSHIFTASSIGN.value)

    #keywords
    IF = 'if'
    ELSE_IF = 'else if'
    ELSE = 'ELSE'
    FOR = 'for'
    WHILE = 'while'
    BREAK = 'break'
    
    

class Function():
    def __init__(self, count=0):
        self.m_count(count) # counts this function's depth
        self.m_announce=[]
    
    def addAnnounce(self, announce):
        self.m_announce.append(announce)
        
        
class Announce():
    def __init__(self):
        self.m_variable=[]
        self.m_operator=[]
    
    def addVariable(self, variable):
        self.m_variable.append(variable)
    def addOperator(self, opeator):
        self.m_operator.append(opeator)

class variable():
    def __init__(self, type='', name=''):
        self.m_type = ''
        self.m_name = ''
    


class Token():
    def __init__(self, name='', row = 0, col = 0):
        self.type = ''
        self.name = name
        self.row = row
        self.col = col
        
        
    def add(self, name):
        self.name += name
    
    def __str__(self):
        arr = str(self.name + " " + str(self.row) + " " + str(self.col))
        return arr
        
    
#input: code, output: Tokens
class Tokenizer():
    def __init__(self):
        self.tokens=[]

    def tokenize(self, code:str):
        tokenNum = 0
        col = 0
        row = 0
        tmp = ''
        for i in range(0, len(code)):
            if(code[i] == SpecialSymbol.NEWLINE.value):
                if(tmp != ''):
                    self.tokens.append(Token(tmp, row, col))
                    row += 1
                    col = 0 # todo 함수일때는 col = 0 아님.
                    tokenNum += 1
                    tmp = ''
            elif code[i] == SpecialSymbol.BLANK.value:
                if(tmp != ''):
                    self.tokens.append(Token(tmp, row, col))
                    col += 1
                    tokenNum += 1
                    tmp = ''    
            elif code[i] == SpecialSymbol.SEMI_COLON.value:
                self.tokens.append(Token(tmp, row, col))
                row += 1
                col = 0 # todo 함수일때는 col = 0 아님.
                tokenNum += 1
                tmp = ''
            else:
                tmp += code[i]
                if(i == len(code)-1):
                    self.tokens.append(Token(tmp, row, col))


#input: Tokens, output: AST(Abstract Syntax Tree)
class Lexer():
    def __init__(self):
        self.tokens = []
        
    def lex(self, tokens):
        return 0
        
    def lex(self, Tokenizer):
        return 0

class Parser():
    def __init__(self):
        self.tokens = []

if __name__ == "__main__":
    s = "int a = 3;\n int b = 4;"
    tokenizer = Tokenizer()
    tokenizer.tokenize(s)
    for i in tokenizer.tokens:
        print(i)