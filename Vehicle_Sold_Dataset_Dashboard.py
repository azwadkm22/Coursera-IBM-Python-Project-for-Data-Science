import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Sales Dashboard"

# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
# List of years
year_list = [i for i in range(1980, 2024, 1)]

# Create the layout of the app
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Select Statistics',
            placeholder='Select a report type'
        )
    ], style={'width': '80%', 'padding': '3px', 'font-size': 20, 'text-align': 'center'}),
    html.Div(dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value='1980'
        ),
        style={'width': '80%', 'padding': '3px', 'font-size': 20, 'text-align': 'center'}
        ),
    html.Div(id='output-container', className='chart-grid', style={'display': 'flex'}),
])

# Callbacks
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)

@app.callback(
    Output(component_id='output-container', component_property='children'),
    [
        Input(component_id='select-year', component_property='value'),
        Input(component_id='dropdown-statistics', component_property='value')
    ]
)

def update_input_container(selected_statistics):
    return selected_statistics != 'Yearly Statistics'

def update_output_container(selected_year, selected_statistics):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]
        
        # Plot 1: Automobile sales fluctuate over Recession Period (year wise)
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, x='Year', y='Automobile_Sales',
                           title="Average Automobile Sales fluctuation over Recession Period")
        )

        # Plot 2: Calculate the average number of vehicles sold by vehicle type
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()                        
        R_chart2 = dcc.Graph(
            figure=px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales',
                          title="Average Number of vehicles sold by Vehicle Type"))

        # Plot 3: Pie chart for total expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec, values='Automobile_Sales', names='Vehicle_Type',
                            title="Total Expenditure Share by Vehicle Type during recessions"))

        # Plot 4: Bar chart for the effect of unemployment rate on vehicle type and sales
        grouped_data = recession_data.groupby('Vehicle_Type').agg({'unemployment_rate': 'mean', 'Automobile_Sales': 'mean'}).reset_index()
        R_chart4 = dcc.Graph(
            figure= px.bar(grouped_data, x='Vehicle_Type', y='Automobile_Sales', 
                   color='unemployment_rate', title='Effect of Unemployment Rate on Vehicle Type and Sales',
                   labels={'Vehicle_Type': 'Vehicle Type', 'Automobile_Sales': 'Average Sales', 'unemployment_rate': 'Average Unemployment Rate'}))

        return [
            html.Div(className='chart-item', 
                     children=[
                         html.Div(children=R_chart1, style={'display': 'flex'}),
                         html.Div(children=R_chart2, style={'display': 'flex'})
                     ],
                     style={'display': 'block'}
            ),
            html.Div(className='chart-item', 
                     children=[
                         html.Div(children=R_chart3, style={'display': 'flex'}),
                         html.Div(children=R_chart4, style={'display': 'flex'}),
                     ],
                     style={'display': 'block'}
            )
        ]

    elif selected_statistics == 'Yearly Statistics':
        yearly_data = data[data['Year'] == int(selected_year)]

        # Plot 1: Yearly Automobile sales using line chart for the whole period
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yas, x='Year', y='Automobile_Sales',
                    title='Yearly Average Automobile sales from 1980 to 2023'.format(selected_year)))

        # Plot 2: Total Monthly Automobile sales using line chart
        # Implement this as needed
        mas = data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(figure=px.line(mas, x='Month', y='Automobile_Sales',
                    title='Total Monthly Automobile sales in the year {}'.format(selected_year)))

        # Plot 3: Bar chart for average number of vehicles sold during the given year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales',
                    title='Average Vehicles Sold by Vehicle Type in the year {}'.format(selected_year)))

        # Plot 4: Total Advertisement Expenditure for each vehicle using pie chart
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(exp_data, values='Advertising_Expenditure', names='Vehicle_Type',
                    title='Total Advertisement Expenditure for each vehicle type in the year {}'.format(selected_year)))

        return [
            html.Div(className='chart-item', 
                     children=[
                         html.Div(children=Y_chart1),
                         html.Div(children=Y_chart2)
                     ],
                     style={'display': 'block'}
            ),
            html.Div(className='chart-item', 
                     children=[
                         html.Div(children=Y_chart3),
                         html.Div(children=Y_chart4)
                     ],
                     style={'display': 'block'}
            )
        ]
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
