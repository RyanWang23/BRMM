# BRMM

## Web application structure
This Flask application is designed to manage and display data related to drivers, courses, and run records. It interacts with a MySQL database to retrieve and present information to users via web pages. The application offers several key features:

- List of Drivers:

The "listdrivers" route retrieves a list of drivers from the database, including their names, driver IDs, and additional information.
It provides a clean and organized presentation of driver information, replacing any missing data with a dash ("-") for clarity.
List of Courses:

The "listcourses" route displays a list of available courses, including their names, course IDs, and other details.

- Overall Results:

The "overall" route is designed to generate an overall view of driver performance.
It queries the database to obtain information about drivers, courses, and run records.
It calculates the total time and scores for each driver across various courses.
Results are sorted by total time, with drivers who did not complete all courses marked as "NQ" (Not Qualified).

- Driver Details:

The "driver_detail" route provides detailed information about a specific driver.
It retrieves run records associated with the driver and computes total scores, considering penalties for cones and wrong directions.
Graph Visualization:

The "showgraph" route is intended for displaying visual data, but the implementation is currently incomplete.

- driver_search route:
   This route renders the "driver_search.html" template, which displays a form for searching drivers.

- driver_results route:
- This route is triggered when the user submits the search form. It retrieves the search query from the request args, executes a database query to fetch matching drivers, and renders the "driver_results.html" template with the retrieved drivers and search query as parameters.
 
- edit_run route:
- This route handles the editing of a run. When accessed via GET method, it retrieves driver and course information from the database and renders the "edit_run.html" template with the retrieved data. When accessed via POST method, it updates the run information in the database based on the submitted form data and renders the "edit_list.html" template with the updated run information.

- run_detail route:
  This route displays the details of a specific run. It retrieves the run_id from the URL parameter, queries the database for the corresponding run information, and renders the "run_detail.html" template with the retrieved run information.

- edit_run_detail route:
  This route handles the editing of a specific run's details. When accessed via POST method, it updates the run information in the database based on the submitted form data and renders the "run_detail.html" template with the updated run information.

- add_driver route:
  This route handles the addition of a new driver. When accessed via GET method, it retrieves car and course information from the database and renders the "add_driver.html" template with the retrieved data. When accessed via POST method, it inserts the driver and run information into the database based on the submitted form data and renders the "add_driver.html" template with a success message.

Technologies and Libraries Used:

- Flask: The Python web framework used to create the application.

- MySQL Connector: A library for connecting to the MySQL database.

- HTML Templates: The application uses HTML templates for rendering web pages.

- Bootstrap (partially implemented): Used for styling and front-end components.

- Python: The primary programming language for application logic.

- MySQL Database: Stores and manages driver, course, and run records.

This Flask application provides a user-friendly interface for managing and displaying data related to drivers and courses. It leverages the Flask framework and interacts with a MySQL database to offer features such as listing drivers, calculating overall results, and displaying driver details. With the potential addition of graph visualization, the application has the capacity to become a comprehensive tool for tracking and visualizing driver performance.

## Database questions

### 1
```{sql}
CREATE TABLE IF NOT EXISTS car
(
   car_num INT PRIMARY KEY NOT NULL,
   model VARCHAR(20) NOT NULL,
   drive_class VARCHAR(3) NOT NULL
);
```

### 2
```{sql}
FOREIGN KEY (car) REFERENCES car(car_num) ON UPDATE CASCADE ON DELETE CASCADE
```

### 3
```{sql}
INSERT INTO car VALUES
(11,'Mini','FWD'),
(17,'GR Yaris','4WD'),
(18,'MX-5','RWD'),
(20,'Camaro','RWD'),
(22,'MX-5','RWD'),
(31,'Charade','FWD'),
(36,'Swift','FWD'),
(44,'BRZ','RWD');
```

### 4
```{sql}
drive_class VARCHAR(3) NOT NULL DEFAULT 'RWD'
```

### 5
Data Privacy: Some data and functionality are meant to be accessed and modified only by authorized users. For example, driver profiles and their personal information should be accessible only to the drivers themselves and the club admin, not to other drivers.

Data Integrity: Allowing unrestricted access could lead to unauthorized changes to the database. For example, if all users could modify run results, it could result in incorrect or manipulated data.

### Password to the admin.

The default username is admin, the password is also admin.
