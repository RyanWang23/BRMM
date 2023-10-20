from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect

app = Flask(__name__)

dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True, auth_plugin='mysql_native_password')
    dbconn = connection.cursor()
    return dbconn

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/listdrivers")
def listdrivers():
    connection = getCursor()
    connection.execute("SELECT * FROM driver;")
    driverList = connection.fetchall()
    result = []
    for i in range(len(driverList)):
        driver = list(driverList[i])
        if driver[4] is None:
            driver[4] = "-"
        if driver[5] is None:
            driver[5] = "-"
        del driver[len(driver)-1]
        temp = [driver[0], driver[1] + " "+ driver[2],  driver[3], driver[4], driver[5]]
        result.append(temp)
    return render_template("driverlist.html", driver_list = result)    

@app.route("/listcourses")
def listcourses():
    connection = getCursor()
    connection.execute("SELECT * FROM course;")
    courseList = connection.fetchall()
    return render_template("courselist.html", course_list = courseList)


@app.route("/overall")
def overall():
    connection = getCursor()
    connection.execute("select * from run join driver on driver.driver_id=run.dr_id join course on course.course_id=run.crs_id;")
    cursor_description = [desc[0] for desc in connection.description]
    rows = connection.fetchall()
    result_lst = [dict(zip(cursor_description, row)) for row in rows]
    drivers = []
    driver_names = []
    courses = []
    for result in result_lst:
        if result["dr_id"] not in drivers:
            drivers.append(result["dr_id"])
            driver_names.append(result["first_name"] +  " " + result["surname"])
        if result["name"] not in courses:
            courses.append(result["name"])
    course_time = []
    for driver in drivers:
        scores = []
        for course in courses:
            records = []
            for result in result_lst:
                if result["dr_id"] == driver and result["name"] == course:
                    records.append(result)
            if records[0]["seconds"] is None and records[1]["seconds"] is None:
                scores.append(None)
            elif records[0]["seconds"] is None and records[1]["seconds"] is not None:
                time = records[1]["seconds"]
                cone = records[1]["cones"]
                wd = records[1]["wd"]
                if cone is None:
                    cone = 0
                scores.append(time+cone*5+wd*10)
            elif records[0]["seconds"] is not None and records[1]["seconds"] is None:
                time = records[0]["seconds"]
                cone = records[0]["cones"]
                wd = records[0]["wd"]
                if cone is None:
                    cone = 0
                scores.append(time+cone*5+wd*10)
            else:
                time = records[0]["seconds"]
                cone = records[0]["cones"]
                wd = records[0]["wd"]
                if cone is None:
                    cone = 0
                time1 = time+cone*5+wd*10
                time = records[1]["seconds"]
                cone = records[1]["cones"]
                wd = records[1]["wd"]
                if cone is None:
                    cone = 0
                time2 = time+cone*5+wd*10
                scores.append(min([time1, time2]))
        if None in scores:
            course_time.append("NQ")
        else:
            course_time.append(sum(scores))
    data_lst = []
    for i in range(len(drivers)):
        d = {
            "driver_id": drivers[i],
            "driver_name": driver_names[i],
            "course_time": course_time[i],
        }
        data_lst.append(d)
    data_lst = sorted(data_lst, key=lambda x: (x['course_time'] == 'NQ', float('inf')), reverse=True)
    print(data_lst)
    return render_template("overall.html", data_lst = data_lst)

@app.route("/driver/<int:driver_id>")
def driver_detail(driver_id):
    connection = getCursor()
    connection.execute("SELECT * FROM run where dr_id=%s;", (driver_id,))
    runList = connection.fetchall()
    result = []
    for arr in runList:
        arr = list(arr)
        crones = arr[4]
        wd = arr[5]
        if crones is None:
            crones = 0
            arr[4] = 0
        if arr[3] is None:
            arr.append("DNF")
        else:
            total = arr[3] + crones*5+wd*10
            arr.append(total)
        result.append(arr)
    return render_template("detail.html", run_list = result)    

@app.route("/graph")
def showgraph():
    connection = getCursor()
    # Insert code to get top 5 drivers overall, ordered by their final results.
    # Use that to construct 2 lists: bestDriverList containing the names, resultsList containing the final result values
    # Names should include their ID and a trailing space, eg '133 Oliver Ngatai '
    resultsList= []
    bestDriverList= []
    return render_template("top5graph.html", name_list = bestDriverList, value_list = resultsList)

if __name__ == "__main__":
    app.run(debug=True)