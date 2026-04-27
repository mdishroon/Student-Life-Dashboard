# handles data manipulation and db management
import pandas as pd
# provides SQLite db support
import sqlite3
# provides file system operations (ex: checking if a file exists))
import os
# provides plotting capabilities for data visualization
import plotly.express as px
# provides the web framework for creating interactive dashboards
import dash
# provides pre-built Bootstrap components for styling the dashboard
import dash_bootstrap_components as dbc
# provides components for building the dashboard layout and interactivity
from dash import dcc, html, Input, Output

def main(data_file):
    # ensure the file exists
    if not os.path.exists(data_file):
        raise Exception(f"File '{data_file}' not found!")

    # creates the DB connection in the same folder as your script
    db_path = 'operation.db'
    conn = sqlite3.connect(db_path)
    
    try:
        # ETL pipeline, Extract, Transform, Load :)
        print(f"Reading {data_file}...")
        # extract data by reading specific CSV
        df = pd.read_csv(data_file)
        
        # convert CSV to SQL Table
        df.to_sql('STUDENT_PERFORMANCE', conn, if_exists='replace', index=False)
        
        conn.commit()        
    except Exception as e:
        print(f"Error processing data: {e}")
    finally:
        conn.close()

# this function will query the DB and return a DataFrame with the data needed for visualization
def get_student_warehouse_df():
    # db file created in main function, make sure to run main() at least once before calling this function
    db_file = 'operation.db'
    # Pulling all columns so the dropdown can filter by any of them
    query = 'SELECT * FROM STUDENT_PERFORMANCE'
    try:
        conn = sqlite3.connect(db_file)
        return pd.read_sql_query(query, conn)
    finally:
        conn.close()

# visualization function that creates a scatter plot with bubble size representing stress level
def create_visualizations(df_warehouse):
    # use the warehouse data to see Study Efficiency vs Stress
    fig_scatter = px.scatter(
        df_warehouse, 
        x='Study_Hours_per_Day', 
        y='CGPA',
        size='Stress_Level_1_to_10', 
        color='Branch', 
        color_discrete_sequence=px.colors.qualitative.Pastel,
        hover_name='Diet_Type',
        title='Study Hours vs CGPA (Bubble Size = Stress Level)',
        # theme
        template='plotly_dark'
    )
    
    fig_scatter.show()

# create the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

# prepare data and figures for the dashboard
target_file = 'student_lifestyle_performance_dataset.csv'
main(target_file) 
df_raw = get_student_warehouse_df()

# define the navbar component
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("GitHub", href="https://github.com/mdishroon")),
        dbc.NavItem(dbc.NavLink("Documentation", href="https://dash.plotly.com/")),
    ],
    brand="Student Performance Insights",
    brand_href="#",
    color="primary",  # This uses the MINTY green color
    dark=True,        # This makes the text white for better contrast
    className="mb-4",
)

# define webpage layourout using Bootstrap components
app.layout = html.Div([
    navbar, # Add the navbar at the very top
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Student Lifestyle Analytics", className="text-center mt-4"), width=12)
        ]),
        
        # Adding a row for the dropdown interaction
        dbc.Row([
            dbc.Col([
                html.Label("Select Category to Compare:"),
                dcc.Dropdown(
                    id='category-dropdown',
                    options=[
                        {'label': 'Branch', 'value': 'Branch'},
                        {'label': 'Diet Type', 'value': 'Diet_Type'},
                        {'label': 'Residence', 'value': 'Residence'}
                    ],
                    value='Branch', # default selection
                    clearable=False,
                    style={'width': '50%'}
                )
            ], width=12, className="mb-4")
        ]),

        # individual rows for each graph to ensure they take up the full line
        dbc.Row([
            dbc.Col(dcc.Graph(id='main-graph'), width=12)
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(dcc.Graph(id='stress-hist'), width=12)
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(dcc.Graph(id='scatter-plot'), width=12)
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(dcc.Graph(id='heatmap-plot'), width=12)
        ], className="mb-4")
    ], fluid=True)
])

# callback to update the graph based on dropdown selection
@app.callback(
    [Output('main-graph', 'figure'),
     Output('stress-hist', 'figure'),
     Output('scatter-plot', 'figure'),
     Output('heatmap-plot', 'figure')],
    Input('category-dropdown', 'value')
)
def update_graphs(selected_category):
    # 1. Bar Chart logic
    avg_df = df_raw.groupby(selected_category)['CGPA'].mean().reset_index()
    fig_bar = px.bar(
        avg_df, x=selected_category, y='CGPA',
        title=f'Average CGPA by {selected_category}',
        template='seaborn', 
        color=selected_category,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_bar.update_yaxes(range=[avg_df['CGPA'].min() - 0.5, avg_df['CGPA'].max() + 0.5])
    fig_bar.update_layout(title_x=0.5)

    # 2. Histogram logic
    fig_hist = px.histogram(
        df_raw, x='Stress_Level_1_to_10',
        color=selected_category,
        title='Stress Distribution', template='seaborn',
        labels={'Stress_Level_1_to_10': 'Stress Level'},
        color_discrete_sequence=px.colors.qualitative.Pastel,
        barmode='overlay'
    )
    fig_hist.update_layout(title_x=0.5)

    # 3. Scatter Plot logic: Study Hours vs CGPA
    fig_scatter = px.scatter(
        df_raw, x='Study_Hours_per_Day', y='CGPA',
        color=selected_category,
        title='Study Hours vs CGPA Correlation',
        labels={'Study_Hours_per_Day': 'Study Hours/Day'},
        template='seaborn',
        color_discrete_sequence=px.colors.qualitative.Pastel,
        trendline="ols"
    )
    fig_scatter.update_layout(title_x=0.5)

    # 4. Heatmap logic: Numerical Correlations
    numeric_df = df_raw.select_dtypes(include=['number'])
    numeric_df.columns = [col.replace('_', ' ') for col in numeric_df.columns]
    corr_matrix = numeric_df.corr()
    
    fig_heatmap = px.imshow(
        corr_matrix,
        text_auto=True, 
        aspect="auto",
        title='Lifestyle Variable Correlation Matrix',
        color_continuous_scale='GnBu', 
        labels={'x': 'Variable', 'y': 'Variable', 'color': 'Correlation Value'}
    )
    fig_heatmap.update_layout(title_x=0.5)

    return fig_bar, fig_hist, fig_scatter, fig_heatmap

if __name__ == "__main__":
    target_file = 'student_lifestyle_performance_dataset.csv'
    db_path = 'operation.db'

    # Check if the database already exists before running ETL process
    if not os.path.exists(db_path):
        print(f"Database not found. Creating {db_path}...")
        main(target_file) 
    else:
        print(f"Database {db_path} already exists. Skipping file read!")

    # Still need to pull the data into memory for the app to use
    df_raw = get_student_warehouse_df()

    # run the Dash app on localhost
    app.run(debug=True, port=8052)