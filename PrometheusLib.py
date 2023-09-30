import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

def dataclean(csv_file): # data cleaning function
    df = pd.read_csv(csv_file, skiprows=2, sep=";") # store csv data in a dataframe, by skipping both first rows
    df.set_index("Numéro") # New index is the column "Numéro"
    df['Commune'] = df['Commune'].str.upper() #Capital letters over the column
    df['Lieu-dit'] = df['Lieu-dit'].str.upper() #Capital letters over the column
    df = df.dropna(subset=['Lieu-dit']) # Drop NaN values
    df[["Date", 'Time']] = df["Alerte"].str.split(' ', expand=True) # split Date and Time from 'Alerte' column
    df["Date"] = df['Date'].astype('datetime64[ns]') # change the type of Date from object to datetime
    df["Time"] = pd.to_datetime(df["Time"], format='%H:%M:%S').dt.time # change the type of Time from object to datetime
    df["Surface parcourue (ha)"] = df["Surface parcourue (m2)"] * 0.0001 # convert m2 into ha, and store in a new column
    return df


# Count the number of fires by year and by department allowing the user 
# to choose the department (or all departments) and the year.
def nb_fires(data, department='00', year=2000): # department = 00 : for all departments and by default
    if department == '00':
        return data[(data["Date"].dt.year==year)]["Département"].count()
    else :
        return data[(data["Département"]==department) & (data["Date"].dt.year==year)]["Département"].count()


    
# Sum the burnt area by year and by department allowing the user to 
# choose the department (or all departments) and the year.
def burnt_area(data, department='00', year=2000):
    if department == '00': # 00 == all department. And default value
        return round(data[(data["Date"].dt.year==year)]["Surface parcourue (ha)"].sum() , 2)
    else : # if the user chosed a department
        return round(data[(data["Département"]==department) & (data["Date"].dt.year==year)]["Surface parcourue (ha)"].sum(), 2)
    
# compute the mean, median, Q1, and Q3 of the burnt area by year
# and by department allowing the user to choose the departement (or all departments)
# and the year.
def des(data, department='00', year=2000):
    if department == '00': # 00 == all department. And default value
        values = data[(data["Date"].dt.year==year)]["Surface parcourue (ha)"]
    else :
        values = data[(data["Département"]==department) & (data["Date"].dt.year==year)]["Surface parcourue (ha)"] 
    mean = values.mean()
    Q1 = values.quantile(0.25)
    Q3 = values.quantile(0.75)
    return department, year, round(mean, 2), Q1, Q3


# Create an interactive line chart with Plotly Express
def plot_department_timeseries(dataframe, department):
    unique_years = dataframe['Date'].dt.year.unique()
    fires_per_year = [nb_fires(dataframe, department=department, year=year) for year in unique_years]
    fig = px.line(x=unique_years, y=fires_per_year, markers=True, labels={'x': 'Year', 'y': 'Number of Wildfires'},
                  title=f'Wildfires Evolution in Department {department}', line_shape='linear')
    fig.write_html('plot_fire_per_years.html')
    
# Create an interactive pie chart with Plotly Express
def plot_pie_chart(datas, year):
    grouped_dt = datas[(datas['Année'] == year)].groupby((datas['Département'])).sum('Surface parcourue (ha)')
    total = grouped_dt['Surface parcourue (ha)'].sum()
    grouped_dt['pourcentage'] = (grouped_dt['Surface parcourue (ha)']/total)*100
    counts = grouped_dt['pourcentage']
    fig = px.pie(names=counts.index, values=counts, title='Camembert')
    fig.update_traces(textinfo='percent+label', pull=[0.1, 0.1, 0.1, 0.1], hoverinfo='label+percent')
    fig.write_html('interactive_pie_chart.html')

    
    
    
    
    
    
