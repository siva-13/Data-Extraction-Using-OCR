from flask import Flask, render_template, request
import textextract
import os
app = Flask(__name__)
UPLOAD_FOLDER = r'C:\Users\hp\PycharmProjects\Flask-work\uploaded_image'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/')  
def upload():  
    return render_template("file_upload_form.html")  
 
@app.route('/success', methods = ['POST'])  

def success():  
    if request.method == 'POST':  
        f = request.files['file']
        FNAME = os.path.join(UPLOAD_FOLDER,(f.filename))
        f.save(FNAME)
        a,b,c,d,e=textextract.main(FNAME)
        return render_template("success.html",name1=a,name2=b,name3=c,name4=d,name5=e)

if __name__=="__main__":
    app.run(debug=True)

