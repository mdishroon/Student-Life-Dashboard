# Student Lifestyle Analytics Dashboard

An interactive Python-based web application that analyzes the relationship between student lifestyle factors and academic performance. This project utilizes a full-stack data approach, featuring an ETL pipeline and a local SQLite database.

## Features
* **Interactive Visualizations**: Dynamic bar charts, histograms, and scatter plots.
* **Correlation Analysis**: A heatmap to identify hidden relationships between lifestyle variables.
* **Responsive UI**: Built with Dash Bootstrap Components using the MINTY theme.
* **SQL Backend**: Efficient data management using SQLite for localized data warehousing.

## Tech Stack
* **Language**: Python 3.x
* **Frontend**: Dash, Plotly, Dash Bootstrap Components
* **Backend**: SQLite3, Pandas
* **Deployment Ready**: Configured for local or cloud environments.

## Data Source
The dataset used in this project is the Student Lifestyle and Academic Performance Dataset, which is available on [Kaggle](https://www.kaggle.com/datasets/rafi003/student-lifestyle-and-academic-performance-dataset)

## Installation and Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mdishroon/Student-Life-Dashboard.git
   cd Student-Life-Dashboard
   ```

2. **Install dependencies**:
   The trendline analysis requires the statsmodels library.
   ```bash
   pip install pandas sqlite3 plotly dash dash-bootstrap-components statsmodels
   ```

3. **Run the application**:
   ```bash
   python studentLife.py
   ```
   Open your browser and navigate to [http://127.0.0.1:8052](http://127.0.0.1:8052)

## Project Architecture
The application follows a standard ETL (Extract, Transform, Load) workflow:
1. **Extract**: Reads raw student data from a CSV file.
2. **Transform**: Processes averages and correlations using Pandas.
3. **Load**: Stores and queries data via a local SQLite database named operation.db.
4. **Visualize**: Renders data through a Plotly Dash interface.

## Data Dictionary
The dashboard analyzes several key metrics:
* **CGPA**: Cumulative Grade Point Average.
* **Stress Level**: Self-reported stress on a scale of 1 to 10.
* **Lifestyle Factors**: Study hours, sleep hours, and screen time.
* **Categorical Data**: Branch of study, diet type, and residence status.

## Usage
The dashboard allows users to filter data by Branch, Diet Type, or Residence to uncover how different student demographics manage stress and academic output. Use the dropdown menu at the top to update all graphs simultaneously.
