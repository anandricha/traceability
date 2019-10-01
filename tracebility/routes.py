from flask import render_template, request
from tracebility import app
from tracebility.helpers.excel_upload import ExcelReadAndUpload
from tracebility.helpers.sprint_details import traceability_data
from tracebility.database import DB

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/bulk-upload")
def bulkupload():
    return render_template("/upload/bulk-upload.html")


@app.route("/upload", methods=['POST'])
def upload():
    reader = ExcelReadAndUpload()
    reader.excel_upload()
    return render_template("/upload/upload_result.html")


@app.route("/reports")
def reports():
    count_string = "value"
    titles = ('Sprint', 'Manual_Testcase_Count', 'Automation_test_Case_Count')
    # get umbrella values from DB
    sprint = DB.distinct("data", "Sprint")
    sprint_data_all = list()
    for item in sprint:
        sprint_data = list()
        query = [{"$match": {"Sprint": item}},
                 {"$match": {"Manual_Testcase": {"$ne": False}}}, {"$count": count_string}]
        manual_data = DB.iterator_with_count(DB.agrregate("data", query), count_string)
        query1 = [{"$match": {"Sprint": item}},
                  {"$match": {"Automated": {"$ne": False}}}, {"$count": count_string}]
        automation_data = DB.iterator_with_count(DB.agrregate("data", query1), count_string)
        sprint_data.append(item)
        sprint_data.append(manual_data["value"])
        sprint_data.append(automation_data["value"])
        sprint_data_all.append(sprint_data)
    #  get data grouped by manual and automation
    data_sprint = dict()
    for item in sprint:
        query = [{"$match": {"Sprint": item}},
                 {"$group": {"_id": {"Manual_Count": "$Manual_Testcase", "Automation_Count": "$Automated"},
                  "count": {"$sum": 1}}}]
        group_data = DB.iterator_with_group(DB.agrregate("data", query), "_id")
        # print("group_data_sprint", item, group_data)
        data_sprint[item] = group_data
        # print("this is group data", data_sprint)
    return render_template('/reports/reports.html',
                           the_title='Sprint data Report',
                           the_row_titles=titles,
                           db_data=sprint_data_all,
                           group_data_sprint = data_sprint)


@app.route("/Sprint/<sprint>")
def sprint_wise_details(sprint):
    tr_data = traceability_data()
    sprint_data = tr_data.sprint_details(sprint)
    print("--------------",sprint_data)
    return render_template('reports/sprint_data.html',
                           the_title=sprint,
                           the_row_titles=sprint_data[0],
                           db_data=sprint_data[1])