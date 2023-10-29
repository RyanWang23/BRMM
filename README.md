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
