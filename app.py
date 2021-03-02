from flask import Flask,request,render_template,send_from_directory,abort
import PyPDF2
from werkzeug.utils import secure_filename
import time
import os

app=Flask(__name__)

app.config["CLIENT_TEXTFILES"]=os.getcwd()

@app.route("/",methods=['GET','POST'])
def home():
    if request.method=="POST":
        file = request.files['filename']
        passwrd=request.form["pass"]
        filename=secure_filename(file.filename)
        file.save(filename)
        time.sleep(5)
        pdf_file = open(filename, "rb")
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        pdf_writer = PyPDF2.PdfFileWriter()

        for i in range(pdf_reader.numPages):
            pdf_writer.addPage(pdf_reader.getPage(i))

        pdf_writer.encrypt(passwrd)

        # give the path where you want to save encrypted pdf file
        result = open("encrypt.pdf", "wb")
        pdf_writer.write(result)

        result.close()
        try:
            return send_from_directory(app.config["CLIENT_TEXTFILES"], filename="encrypt.pdf", as_attachment=True)
        except FileNotFoundError:
            abort(404)
    return render_template("home.html")


if __name__=="__main__":
    app.run(debug=True)

