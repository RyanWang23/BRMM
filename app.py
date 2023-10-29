from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session

import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect

app = Flask(__name__)
app.secret_key = 'xxxxdsfdsfdfdf'

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
    return  redirect(url_for('listdrivers'))

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
    connection.execute("select * from run join driver on driver.driver_id=run.dr_id join course on course.course_id=run.crs_id join car on car.car_num=driver.car;")
    cursor_description = [desc[0] for desc in connection.description]
    rows = connection.fetchall()
    result_lst = [dict(zip(cursor_description, row)) for row in rows]
    drivers = []
    driver_names = []
    models = []
    courses = []

    for result in result_lst:
        age = result["age"]
        if result["dr_id"] not in drivers:
            drivers.append(result["dr_id"])
            if age is None:
                driver_names.append(result["first_name"] +  " " + result["surname"])
            else:
                driver_names.append(result["first_name"] +  " " + result["surname"] + " (J)")
            models.append(result["model"])
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
            course_time.append(round(sum(scores)))
    data_lst = []
    for i in range(len(drivers)):
        d = {
            "driver_id": drivers[i],
            "driver_name": driver_names[i],
            "course_time": course_time[i],
            "model": models[i],
        }
        data_lst.append(d)
    data_lst = sorted(data_lst, key=lambda x: (x['course_time'] == 'NQ', x['course_time'] if x['course_time'] != 'NQ' else float('inf')))
    data_lst[0]["course_time"] = str(data_lst[0]["course_time"]) + " (win)"
    for i in range(1,5):
        data_lst[i]["course_time"] = str(data_lst[i]["course_time"]) + " (prize)"
    return render_template("overall.html", data_lst = data_lst)


@app.route("/detail", methods=['GET', 'POST'])
def detail():
    if request.method == 'POST':
        driver_id = request.form.get('driver_id')
        return redirect(url_for('driver_detail', driver_id=driver_id))
    else:
        # Fetch all drivers from the database to populate the dropdown list
        connection = getCursor()
        connection.execute("select * from driver;")
        cursor_description = [desc[0] for desc in connection.description]
        rows = connection.fetchall()
        drivers = [dict(zip(cursor_description, row)) for row in rows]
        print(drivers)
        return render_template('detail_query.html', drivers=drivers)



@app.route("/driver/<int:driver_id>")
def driver_detail(driver_id):
    connection = getCursor()
    connection.execute("select * from driver join run on run.dr_id=driver.driver_id join course on course.course_id=run.crs_id join car on car.car_num=driver.car where dr_id=%s;", (driver_id,))
    
    cursor_description = [desc[0] for desc in connection.description]
    rows = connection.fetchall()
    result_lst = [dict(zip(cursor_description, row)) for row in rows]
    for row in result_lst:
        if row["cones"] is None:
            row["cones"] = 0
        if row["seconds"] is None:
            row["seconds"] = ''
            row["cones"] = ''
            row["wd"] = ''
            row["run_total"] = ''
        else:
            row["run_total"] = row["seconds"] + row["cones"]*5+ row["wd"]*10
    return render_template("detail.html", run_list = result_lst)    


@app.route("/graph")
def showgraph():
    connection = getCursor()
    connection.execute("select * from run join driver on driver.driver_id=run.dr_id join course on course.course_id=run.crs_id join car on car.car_num=driver.car;")
    cursor_description = [desc[0] for desc in connection.description]
    rows = connection.fetchall()
    result_lst = [dict(zip(cursor_description, row)) for row in rows]
    drivers = []
    driver_names = []
    models = []
    courses = []

    for result in result_lst:
        age = result["age"]
        if result["dr_id"] not in drivers:
            drivers.append(result["dr_id"])
            if age is None:
                driver_names.append(result["first_name"] +  " " + result["surname"])
            else:
                driver_names.append(result["first_name"] +  " " + result["surname"] + " (J)")
            models.append(result["model"])
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
            course_time.append(round(sum(scores)))
    data_lst = []
    for i in range(len(drivers)):
        d = {
            "driver_id": drivers[i],
            "driver_name": driver_names[i],
            "course_time": course_time[i],
            "model": models[i],
        }
        data_lst.append(d)
    data_lst = sorted(data_lst, key=lambda x: (x['course_time'] == 'NQ', x['course_time'] if x['course_time'] != 'NQ' else float('inf')))
    data_lst[0]["course_time"] = str(data_lst[0]["course_time"]) + " (win)"
    resultsList = []
    bestDriverList =[]
    for i in range(1,6):
        resultsList.append(data_lst[i]["course_time"])
        bestDriverList.append(data_lst[i]["driver_name"])
    print(resultsList)
    return render_template("top5graph.html", name_list = bestDriverList, value_list = resultsList)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if username == "admin" and password == "admin":
            session["username"] = username
            return redirect(url_for("junior_drivers"))
        else:
            error_message = "Invalid username or password"
            return render_template("login.html", error=error_message)
    
    return render_template("login.html")


@app.route("/junior-drivers")
def junior_drivers():
    connection = getCursor()
    connection.execute('''SELECT A.driver_id as driver_id, concat(A.first_name, ' ' ,  A.surname) driver_name,
A.age as age, concat(B.first_name, ' ' ,  B.surname) care_name 
 FROM driver as A left join driver as B on B.driver_id=A.caregiver where A.age is not null
 order by A.age desc, A.surname;''')
    cursor_description = [desc[0] for desc in connection.description]
    rows = connection.fetchall()
    driver_list = [dict(zip(cursor_description, row)) for row in rows]
    return render_template("junior_drivers.html", driver_list=driver_list)

@app.route("/driver-search")
def driver_search():
    return render_template("driver_search.html")


@app.route("/driver-results")
def driver_results():
    search_query = request.args.get("search", "")
    connection = getCursor()
    connection.execute("select * from driver where first_name like '%{}%' or surname like '%{}%';".format(search_query, search_query))
    cursor_description = [desc[0] for desc in connection.description]
    rows = connection.fetchall()
    drivers = [dict(zip(cursor_description, row)) for row in rows]
    print(drivers)
    return render_template("driver_results.html", drivers=drivers, search_query=search_query)

@app.route("/edit-run")
def edit_run():
    return render_template("edit_run.html")

@app.route("/add-driver")
def add_driver():
    return render_template("add_driver.html")

    

if __name__ == "__main__":
    app.run(debug=True)