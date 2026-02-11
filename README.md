# Capstone-Project
# CityBike — Bike-Sharing Analytics Platform

## Motivation & Context
Bike-sharing systems have become a cornerstone of modern urban transport in cities worldwide — from Berlin’s Nextbike to New York’s Citi Bike and London’s Santander Cycles. These systems generate vast amounts of operational data every day: trip records, station usage, fleet maintenance logs, and user activity.

Managing such a system is a real-world software engineering challenge. Operators need to:

- Track hundreds of bikes across dozens of stations
- Understand when and where demand peaks occur
- Schedule preventive maintenance to minimize downtime
- Analyze user behavior to optimize station placement and pricing
- Generate reports for city authorities and stakeholders

In this capstone project, you will build a complete backend platform for a fictional city bike-sharing service. You will model the domain with object-oriented design, load and clean operational datasets, implement algorithms, compute statistics, generate visualizations, and deliver a well-structured, version-controlled codebase.

---

## Project Overview
This is the final integrative project of the course, demonstrating mastery of Units 1–13.  
It integrates:

- Modular code structure, functions, multi-file organization
- Object-oriented design: classes, inheritance, abstract base classes, design patterns
- Algorithms: sorting, searching, complexity analysis
- NumPy for numerical computing
- Pandas for data analysis, cleaning, and aggregation
- Data visualization with Matplotlib
- Version control with Git and GitHub

Unlike earlier mini-projects, this capstone requires all of the above in a single, cohesive application. Code must be documented, modular, and professionally structured.

---

## Functional Requirements

### 1. Object-Oriented Data Models
- **Entity (abstract base class)**: shared id, created_at; enforces `__str__` and `__repr__`.
- **Bike(Entity)**: `bike_id`, `bike_type`, `status` (available/in_use/maintenance)  
  - ClassicBike(Bike): `gear_count`  
  - ElectricBike(Bike): `battery_level`, `max_range_km`
- **Station(Entity)**: `station_id`, `name`, `capacity`, `latitude`, `longitude`
- **User(Entity)**: `user_id`, `name`, `email`, `user_type`  
  - CasualUser(User): `day_pass_count`  
  - MemberUser(User): `membership_start`, `membership_end`, `tier`
- **Trip**: `trip_id`, `user`, `bike`, `start_station`, `end_station`, `start_time`, `end_time`, `distance_km`
- **MaintenanceRecord**: `record_id`, `bike`, `date`, `maintenance_type`, `cost`, `description`
- **BikeShareSystem**: orchestrates loading, cleaning, analysis, and reporting

**OOP Requirements:**

- Proper constructors with input validation
- `__str__` and `__repr__` implemented
- At least one abstract base class
- Inheritance hierarchies with depth ≥2
- Use of `@property` for controlled attribute access
- Implement **Factory Pattern** (create objects from CSV row dictionaries)
- Implement **Strategy Pattern** (interchangeable pricing strategies)

---

### 2. Data Loading & Cleaning
- Load CSV files into Pandas DataFrames
- Inspect structure, types, missing values
- Handle missing values (drop, fill, interpolate — document strategy)
- Convert types: parse dates, ensure numeric columns, standardize categorical values
- Remove duplicates and invalid entries (e.g., trips where `end_time < start_time`)
- Export cleaned datasets to CSV

---

### 3. Algorithmic Analysis
**Sorting:**

- Implement custom sorting (merge sort, quicksort)
- Sort trips by duration or distance
- Compare with built-in `sorted()` or `sort_values()` using `timeit`

**Searching:**

- Implement custom search (binary search, etc.)
- Apply to find trips, stations, or users by ID/attribute
- Compare with built-in methods (`in`, `.loc[]`, `.query()`)
- Document Big-O and performance differences

---

### 4. Numerical Computing (NumPy)
- Compute distances between stations (Euclidean formula)
- Compute vectorized statistics on trip durations and distances (mean, median, std, percentiles)
- Batch numerical computation (fares, outlier detection) using NumPy arrays

---

### 5. Analytics & Business Insights
Answer at least 10 of the following using Pandas/NumPy:

1. Total trips, total distance, average duration
2. Top 10 start and end stations
3. Peak usage hours
4. Day of week with highest trip volume
5. Average trip distance by user type
6. Bike utilization rate
7. Monthly trip trend
8. Top 15 active users
9. Maintenance cost per bike type
10. Most common station-to-station routes
11. Trip completion rate
12. Avg trips per user by type
13. Bikes with highest maintenance frequency
14. Identify outlier trips

---

### 6. Visualization (Matplotlib)
Create at least 4 charts:

- **Bar chart:** trips per station or revenue by user type
- **Line chart:** monthly trip volume trend
- **Histogram:** trip duration or distance distribution
- **Box plot:** duration by user type or bike type

**Requirements:**

- Titles, axis labels, legend (if applicable)
- Clean, readable styling
- Export PNGs to `output/figures/`

---

### 7. Reporting & Export
- Export cleaned datasets to CSV
- Generate summary report (`summary_report.txt`) with metrics and answers
- Export top stations, top users, maintenance summaries

---

## Project Structure

citybike/
├─ main.py # Orchestrates pipeline
├─ models.py # OOP classes
├─ analyzer.py # Analysis methods
├─ algorithms.py # Sorting/searching
├─ numerical.py # NumPy computations
├─ visualization.py # Matplotlib chart functions
├─ pricing.py # Strategy Pattern pricing
├─ factories.py # Factory Pattern object creation
├─ utils.py # Helpers, validation, formatting
├─ data/
│ ├─ trips.csv
│ ├─ stations.csv
│ ├─ maintenance.csv
│ ├─ trips_clean.csv
│ └─ stations_clean.csv
├─ output/
│ ├─ summary_report.txt
│ ├─ top_stations.csv
│ ├─ top_users.csv
│ └─ figures/ # PNG charts
├─ README.md
├─ requirements.txt
└─ .gitignore

---

## Setup & Usage

1. Clone the repository:

```bash
git clone <repo-url>
cd citybike
Install dependencies:

pip install -r requirements.txt
Run the platform:

python main.py
Check output/ for cleaned data, reports, and charts.

Data Generator
A synthetic data generator is included to create trips.csv, stations.csv, and maintenance.csv.
It introduces duplicates, missing values, and inconsistencies to simulate real-world scenarios.

Milestones
Project Setup: GitHub repo, project structure, README, requirements, raw data

Domain Models: OOP classes, Factory & Strategy patterns

Data Loading & Cleaning

Algorithms: sorting/searching and benchmarks

Numerical Computing: NumPy operations

Analytics: business questions and summary report

Visualizations: charts exported as PNG

Polish & Delivery: docstrings, type hints, final commit

Git & Version Control
Use Git for version control

Feature branches for major components

At least 15 meaningful commits

Clear commit messages (feat, fix, test, docs)

Main branch always contains working code

Submission
Submit:

GitHub repository URL

All source code modules

README.md with project description, setup, and usage

requirements.txt

Raw CSV data files

Cleaned CSV files

Summary report and top entity exports

Visualization PNGs

Execution:

pip install -r requirements.txt
python main.py