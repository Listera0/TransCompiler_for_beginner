from operator import index
from tokenize import String
from flask import Flask,request, render_template
import C, CS, CPP, Python, Java

app = Flask(__name__)

## 시작 화면
@app.route('/', methods = ['POST', 'GET'])
def Start():
    if request.method == 'POST':
        submit = str(request.form["submit_type"])
        if submit == "번역":
            code = str(request.form["input_field"])
            input_language = str(request.form["input_language"])
            output_language = str(request.form["output_language"])
            result = str(Converting(code, input_language, output_language))
            return render_template("Main.html",origin = code , value = result)
        elif submit == "⇋":
            temp1 = str(request.form["input_field"])
            temp2 = str(request.form["output_field"])
            return render_template("Main.html", origin = temp2, value = temp1)
        else:
            return render_template("Main.html", value = '')
    else:
        return render_template("Main.html", value = '')

## 변환
def Converting( code, in_lan, out_lan ):
    temp1 = None
    temp2 = ''
    
    if in_lan == "1":
        temp1 = C.Extraction(code)
    elif in_lan == "2":
        temp1 = CS.Extraction(code)
    elif in_lan == "3":
        temp1 = CPP.Extraction(code)
    elif in_lan == "4":
        temp1 = Python.Extraction(code)
    elif in_lan == "5":
        temp1 = Java.Extraction(code)
    
    if out_lan == "1":
        temp2 = C.ConvertCodeToC(temp1, 0)
    elif out_lan == "2":
        temp2 = CS.ConvertCodeToCS(temp1, 0)
    elif out_lan == "3":
        temp2 = CPP.ConvertCodeToCPP(temp1, 0)
    elif out_lan == "4":
        temp2 = Python.ConvertCodeToPython(temp1, 0)
    elif out_lan == "5":
        temp2 = Java.ConvertCodeToJava(temp1, 0)
    
    return temp2

if __name__ == '__main__':
    app.run()