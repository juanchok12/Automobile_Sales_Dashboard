
###Importing Libraries###
import dash
from dash import dcc #dash core components
from dash import html #dash html components
from dash.dependencies import Input, Output #dash dependencies for callbacks
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

#Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')


#Initialize the Dash App
app=dash.Dash(__name__)

#Set the title of the dashboard
app.title='Automobile Sales Statistical Dashboard'

#---------------------------------------------------------------
#Create the dropdown menu options
dropdown_options=[{'label':'Yearly Statistics','value':'Yearly Statistics'},
                  {'label':'Recession Period Statistics','value':'Recession Period Statistics'}
                  ]

#List of years
years_list=[i for i in range(1980,2024,1)] #List comprehension takes each of the numbers in the range and adds themt to a list
#---------------------------------------------------------------
#Create the app layout
app.layout=html.Div([
    #Task 2.1 add title to the dashboard
    html.H1("Automobile Sales Statisitcs Dashboard", 
            style={'textAlign':'center','color':'#503D36','font-size':24}), #May include style for title
    html.Div([
        #Task 2.2 add dropdown menu
        html.Label("Select Statistics"),
        dcc.Dropdown(id='dropdown-statistics',
                     options=[{'label':'Yearly Statistics','value':'Yearly Statistics'}, ##Corrected the label from 'Yearly Statistics' to 'label'
                             {'label':'Recession Period Statisitcs','value':'Recession Period Statistics'}], ##Corrected the label from 'Recession Period Statisitcs' to 'label'
                     value=None,
                     placeholder='Select a report type',
                     style={'width':'80%', 'padding':'3px','font-size':'20px','text-align-last':'center'}
                     )
]),
    html.Div(dcc.Dropdown( 
        id='select-year',
        options=[{'label': str(year), 'value': year} for year in years_list],
        value=2005,
        placeholder='Select a year',
        style={'width':'80%', 'padding':'3px','font-size':'20px','text-align-last':'center'}
    )),

#Task 2.3: Add a division for output display of plots-Output Container
#'''The output contianer serves as the display area where 
#the results or outputs of user internations with your 
#app's components (e.g. dropdowns, sliders, etc.) are shown.
#This is where the callbacks functions return the outputs to 
#displayed.
#  * The className and style attribute soecify CSS styling for the output container
#  * This is where the plots will be displayed
#This is where the plots will be displayed'''
    html.Div(id='output-container',className='chart-grid',style={'display':'flex'})
])
#---------------------------------------------------------------
#Task 2.4: Creating callbacks
'''
The callback function is used the define the interactivity of
the app. It is used to update the output container based on the
user's selection of statistics and year from the dropdown menus.
It connects the inputs and outputs of the app by triggering 
autmatic changes. Callbacks make Dash apps dynamic and 
responsive to user interactions. 
'''
#Define the callback function to update the input container based on the selected statistics
'''
Output() specifies which component and property should
be updated as a result of the callback function.
 * component_id: The ID of the component to be updated
 * component_property: The property of the component to be updated
Input() specifies which component and property should trigger 
the callback function.
 * component_id: the ID of the component that provides the
  input value.
 * component_property: the property of the component that
    provides the input value.

In this case, we pick 'dropdown-statistics' as the input 
because dependent on the selection between 'Yearly Statistics'
or 'Recession Period Statistics', the output container will
enable the selection of 'select-year' dropdown menu.

IF------> 'Yearly Statistics' is selected, 
the 'select-year' enabled
ELSE----> 'Recession Period Statistics' is selected,
the 'select-year' disabled
'''
#Callback for enabling and disabling the 'select-year' dropdown menu
@app.callback(
    Output(component_id='select-year',component_property='disabled'), #component_property set to 'disabled' creates a booelan value that enables or disables the dropdown menu
    Input(component_id='dropdown-statistics',component_property='value'))

#Define the callback function to update the input container based on the selected statistics

#update_input_container() is dertermines whether the component_property of
#the Output() should be enabled or disabled based on the value of the function.

def update_input_container(selected_statistics):
    if selected_statistics=='Yearly Statistics':
        return False
    else:
        return True

#Callback for plotting
'''
In this callback decorator we add two Input() components because we have to
selections that will give us two different sets of plot outputs:

    * dropdown-statistics: allows to select between 'Yearly Statistics' and 'Recession Period Statistics'
    * select-year: allows to select the year for which the statistics will 
    be displayed. This would enabled the user to use the year dropdown menu 
    to select the year for which the statistics will be displayed.
'''
@app.callback(
        Output(component_id='output-container',component_property='children'), #component_property set to 'children' creates a container for the addition of serveral elements to the output container, including text, plots, tables, etc.
        [Input(component_id='dropdown-statistics',component_property='value'),
         Input(component_id='select-year',component_property='value')])


#Define the callback function to update the input container based on the selected statistics

#* This function indicates that if we pick 'Recession Period Statistics'
#our dataframe will be filtered to only include the recession years. 


def update_output_container(selected_statistics,input_year):
    '''This function indicates that if we pick 'Recession Period Statistics'
    our dataframe will be filtered to only include the recession years.'''
    if selected_statistics=='Recession Period Statistics':
        #Filter the data for recession periods
        recession_data=data[data['Recession']==1]
        #2.5: Create and display graphs for Recession Report Statistics
        #Plot 1: Automobile sales flucturate over recession period (year wise)
        #Use groupby to create relevant data for plotting
        yearly_rec=recession_data.groupby(['Year'])['Automobile_Sales'].mean().reset_index()
        r_chart1=dcc.Graph(
            figure=px.line(yearly_rec,
                        x='Year',
                        y='Automobile_Sales',
                        title='Average Automobile Sales fluctuation over Recession Period')
        )
        #Plot 2: Calculate the average number of vehicles sold by vehicle type
        #Use grouby to create relevenat data based on vehicle type and sales
        ave_sales=recession_data.groupby(['Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        r_chart2=dcc.Graph(figure=px.bar(ave_sales,
                                        x='Vehicle_Type',
                                        y='Automobile_Sales',
                                        title='Average Number of Vehicles Sold by Vehicle Type')
                        )       

        #Plot 3: Pie chart for total expenditure share by vehicle during recessions
        #Use grouby to create relevant data for plotting pie chart for total expenditure share by vehicle-type during recessions
        total_exp=recession_data.groupby(['Vehicle_Type'])['Advertising_Expenditure'].sum().reset_index()
        r_chart3=dcc.Graph(figure=px.pie(total_exp,
                                        values='Advertising_Expenditure',
                                        names='Vehicle_Type',
                                        title='Total Expenditure Share by Vehicle Type during Recession')
                        )


        #Plot 4 bar chart for the effect of unemployment rate on automobile sales during recession
        #Use groupby to create relevant data for plotting
        unemp_sales=recession_data.groupby(['unemployment_rate'])['Automobile_Sales'].mean().reset_index()
        r_chart4=dcc.Graph(figure=px.bar(unemp_sales,
                                        x='unemployment_rate',
                                        y='Automobile_Sales',
                                        title='Effect of unemployment rate and sales'
                                        ))

        #Return the four graphs for displaying recession data
        return [
            html.Div(className='chart-item',children=[html.Div(children=r_chart1),html.Div(children=r_chart3)]),
            html.Div(className='chart-item',children=[html.Div(children=r_chart2),html.Div(children=r_chart4)])     
            ]

    
    #When both condtions are met:
    #    * The data is filtered for the selected year
    #   * The data is filtered for 'Yearly Statistics'
    #the function proceed to filter the data for the selected year and 
    #generated the corresponding plots.
    
    elif (input_year and selected_statistics=='Yearly Statistics'):
        #Filter the data for the selected year
        yearly_data=data[data['Year']==input_year]
        #TASK 2.5: Creating Graphs Yearly data                     
        #plot 1: Yearly Automobile sales using line chart for the whole period.
        yas= data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        yas
        Y_chart1 = dcc.Graph(figure=px.line(
            yas, 
            x='Year',
            y='Automobile_Sales',
            title="Average Automobile Sales over the years"
        ))
            
        #Plot 2: Total Monthly Automobile sales using line chart.
        Y_chart2 = dcc.Graph(figure=px.line(
            yearly_data,
            x='Month',
            y='Automobile_Sales',
            title='Total monthly automobile sales over the years'
        ))

        #Plot 3: Bar chart for average number of vehicles sold during the given year
        avr_vdata=yearly_data.groupby(['Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph( figure=px.bar(
                              avr_vdata,
                              x='Vehicle_Type',
                              y='Automobile_Sales',
                              title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)))

        #Plot 4: Total Advertisement Expenditure for each vehicle using pie chart
        exp_data=yearly_data.groupby(['Vehicle_Type'])['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(
                             exp_data,
                             values='Advertising_Expenditure',
                             names='Vehicle_Type',
                             title='Total Advertisement Expenditure for each vehicle using pie chart')
        )

#TASK 2.6: Returning the graphs for displaying Yearly data
        return [    
                html.Div(className='chart-row', children=[html.Div(children=Y_chart1),html.Div(children=Y_chart2)]),
                html.Div(className='chart-row', children=[html.Div(children=Y_chart3),html.Div(children=Y_chart4)])
                ]
    else:
        return None
#----------------------------------------------------------------

# Run the Dash app
if __name__=='__main__':
    app.run_server(debug=False)







