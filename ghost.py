# Loading modules
import pandas as pd
import bokeh
from bokeh.plotting import output_notebook, figure, show
import folium

# Loading data...
deaths = pd.read_csv('datasets/deaths.csv')

# Dataset shape
print(deaths.shape)

# Printing out the first 5 rows
deaths.head()

# Summarizing the content of deaths
deaths.info()

# Define the new names of your columns
newcols = {
    'Death': 'death_count',
    'X coordinate': 'x_latitude', 
    'Y coordinate': 'y_longitude' 
    }

# Renaming columns
deaths.rename(columns=newcols, inplace=True)

# Dataset description
deaths.describe()

# Subsetting only Latitude and Longitude to create locations col 
locations = deaths[['x_latitude', 'y_longitude']]

# Transforming the DataFrame to list of lists to create death_list hahaha
death_list = locations.values.tolist()

# Check the length of the list
len(death_list)

# Plot the data on map (map location is provided) using folium and for loop for plotting all the points

map = folium.Map(location=[51.5132119,-0.13666], tiles='Stamen Toner', zoom_start=17)
for point in range(0, len(death_list)):
    folium.CircleMarker(death_list[point], radius=8, color='red', fill=True, fill_color='red', opacity = 0.4).add_to(map)
map

# Importing data
pumps = pd.read_csv('datasets/pumps.csv')

# Subsetting Latitude and Longitude cols from the dataset to find pumps
locations_pumps = pumps[['X coordinate', 'Y coordinate']]

# Transforming the DataFrame to list of lists to creat a list of pumps, pumps_lists
pumps_list = locations_pumps.values.tolist()

# For loop & data plotting with folium prev map used + new layer
map1 = map
for point in range(0, len(pumps_list)):
    folium.Marker(pumps_list[point], popup=pumps['Pump Name'][point]).add_to(map1)
map1


# Importing data with parsed dates
dates = pd.read_csv('datasets/dates.csv', parse_dates=['date'])

# When handle was removed (8th of September 1854)
handle_removed = pd.to_datetime('1854/9/8')

# Creating column day_name in dates DataFrame with names of the day 
dates['day_name'] = dates.date.dt.weekday_name

# Creating column handle in dates DataFrame based on a date the handle was removed 
dates['handle'] = dates.date > handle_removed

# Dataset structure
dates.info()

# Comparing Cholera deaths and attacks before and after the handle removal
dates.groupby(['handle']).sum()



# Setting up figure
p = figure(plot_width=900, plot_height=450, x_axis_type='datetime', tools='lasso_select, box_zoom, save, reset, wheel_zoom',
          toolbar_location='above', x_axis_label='Date', y_axis_label='Number of Deaths/Attacks', 
          title='Number of Cholera Deaths/Attacks before and after 8th of September 1854 (removing the pump handle)')

# Plot on figure
p.line(dates['date'], dates['deaths'], color='red', alpha=1, line_width=3, legend='Cholera Deaths')
p.circle(dates['date'], dates['deaths'], color='black', nonselection_fill_alpha=0.2, nonselection_fill_color='grey')
p.line(dates['date'], dates['attacks'], color='black', alpha=1, line_width=2, legend='Cholera Attacks')

show(p)

#Jon Snow was right!