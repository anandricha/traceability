from flask import request,redirect,url_for,flash
from tracebility.utils import datagenerator
import os
from datetime import datetime
from tracebility.database import DB
from werkzeug.utils import secure_filename

APP_ROOT = os.path.abspath(os.path.dirname(__file__))

ALLOWED_EXTENSIONS = {'xlsx',}



class ExcelReadAndUpload:
    target = os.path.join(APP_ROOT, '/data')

    def allowed_file(self,filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def excel_upload(self):
        if request.method == 'POST':
            print(request.files)
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)

        # create directory to save file if directory does not exists.

        print(ExcelReadAndUpload.target)
        if not os.path.isdir(ExcelReadAndUpload.target):
            os.mkdir(ExcelReadAndUpload.target)

        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename

        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            destination = "/".join([ExcelReadAndUpload.target, filename])
            print("this is filename : ", filename)
            file.save(destination)
            excel_data = datagenerator.get_row_data(destination, 'Sheet1')
            for row in excel_data:
                print("value in row", row)
                post = {"Sprint": row[0],
                        "JIRA_ID": row[1],
                        "Manual_Testcase": row[2],
                        "Testcase_ID": row[3],
                        "Automated": row[4],
                        "Test_method": row[5],
                        "Bugs": row[6].split(","),
                        "Status": row[7],
                        "date": datetime.utcnow()}
                DB.insert("data", post)
                flash("DB insertion completed")
            return redirect(request.url)
        else:
            flash("Extention not supported")
            return redirect(request.url)
