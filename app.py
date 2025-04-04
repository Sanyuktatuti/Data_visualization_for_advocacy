# -*- coding: utf-8 -*-
"""st5442_Assignment4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HcKbhluCFhBafbTjS_DJJk3tFM-wB_Ng
"""

import pandas as pd
from bokeh.plotting import figure, show, output_notebook
from bokeh.models import ColumnDataSource, HoverTool, RangeSlider, Button, NumeralTickFormatter
#from bokeh.layouts import Column, Row, GridSpec
from bokeh.layouts import column, row, gridplot
from bokeh.io import push_notebook
from bokeh.models import CustomJS, PrintfTickFormatter
from bokeh.models import Div
import geopandas as gpd
from bokeh.models import GeoJSONDataSource, CustomJS, CheckboxButtonGroup, ColorBar
from bokeh.palettes import Viridis256
from bokeh.transform import linear_cmap
from bokeh.models import Legend, Select, LabelSet
import json
import numpy as np
from bokeh.models import ColorBar, LinearColorMapper
from bokeh.models import HoverTool
import pycountry_convert as pc
import panel as pn
pn.extension()
from panel.layout import Column, Row, GridSpec

#output_notebook()

data = pd.read_csv('global-plastics-production.csv') #the path needs to be inserted accordingly to recreate visualization

df=data

df.head()

df.tail()

# Creating the necessary data for the plot
years = df['Year'].tolist()
production = df['Annual plastic production between 1950 and 2019'].tolist()

# Scaling production values by dividing by 1 million (to convert from raw number to millions)
scaled_production = [x / 1000000 for x in production]

source = ColumnDataSource(data=dict(Year=years, Production=scaled_production))

# Creating the figure with larger size
p = figure(title="Global Plastics Production (1950-2019)", x_axis_label='Year', y_axis_label='Production (Millions of Tons)',
           width=900, height=500)  # Increase width and height

# Setting the title font size
p.title.text_font_size = "20pt"  # Adjust the font size of the title
p.title.text_font = "Times New Roman"

# Creating the line plot
line = p.line(x='Year', y='Production', source=source, line_width=2, color="blue")

# Adding smaller circles (dots) with a different color (e.g., green)
dots = p.circle(x='Year', y='Production', source=source, size=4, color="blue", alpha=0.6)

# Creating hover tool to show year and production values dynamically
hover = HoverTool()
hover.tooltips = [("Year", "@Year"), ("Production", "@Production{0.0} million")]
p.add_tools(hover)

# Creating a range slider with two cursors and larger size
range_slider = RangeSlider(start=1950, end=2019, value=(1950, 2019), step=1, title="Year Range", height=40, width=900)

# JavaScript callback for Bokeh to filter data dynamically based on the range slider
callback_code = """
    const data = source.data;
    const start_year = range_slider.value[0];
    const end_year = range_slider.value[1];
    const all_years = %s;
    const all_production = %s;
    data['Year'] = [];
    data['Production'] = [];
    for (let i = 0; i < all_years.length; i++) {
        if (all_years[i] >= start_year && all_years[i] <= end_year) {
            data['Year'].push(all_years[i]);
            data['Production'].push(all_production[i]);
        }
    }
    source.change.emit();
""" % (str(years), str(scaled_production))

# Linking the range slider to the callback
range_slider.js_on_change('value', CustomJS(args=dict(source=source, range_slider=range_slider), code=callback_code))

# Setting the y-axis tick formatter to display values in "Millions of Tons" format
p.yaxis.formatter = PrintfTickFormatter(format="%1.1f million")

# Function to animate the range slider (using JavaScript)
play_button = Button(label="Play", button_type="success")

play_callback_code = """
    let start_year = range_slider.value[0];
    let end_year = start_year;  // Start the end_year from the start_year value
    let final_year = 2019;
    let interval;

    function updateRange() {
        if (end_year < final_year) {
            end_year++;
            range_slider.value = [start_year, end_year];
        } else {
            clearInterval(interval);
        }
    }

    interval = setInterval(updateRange, 100);  // 100ms interval for animation
"""

# Adding play button with the play animation callback
play_button.js_on_click(CustomJS(args=dict(range_slider=range_slider), code=play_callback_code))

# Introduction text
introduction = Div(
    text="""
    <h1 style="text-align:center;">The Plastic Problem and Global Perspectives</h1>
    <p style="text-align: justify; font-size: 14px; margin-top: 10px;">
        Plastic pollution has become one of the most pressing environmental challenges of our time.
        From mismanaged waste on land to the vast quantities of plastic accumulating in our oceans,
        the impact of this crisis is both global and deeply personal.
    </p>
    <p style="text-align: justify; font-size: 14px; margin-top: 10px;">
        This series of visualizations offers a multifaceted view of plastic waste, examining how economic, regional, and environmental factors intertwine to shape this growing problem. We delve into the relationship between economic prosperity and waste management efficiency, uncover regional trends in mismanaged waste, and explore the types of plastic polluting our oceans. Through these insights, we aim to highlight not only the scope of the issue but also potential paths for action.
    </p>
    """,
)

# Creating the description
description = Div(text="""    <h1 style="text-align:left;">From Progress to Pollution:</h1>
<p style="text-align: justify; font-size: 14px; margin-top: 10px;">
This interactive visualization captures the dramatic increase in global plastic production,
charting its rise from 1950 to 2019 in millions of tons. With tools to explore specific time ranges
and an animated playback feature, the graph presents an evolving story of humanity’s reliance on plastic—and its consequences.<br><br>
Hover over data points to uncover the scale of production year by year, and let the narrative guide you to reflect
on the urgent need for sustainable solutions. This is more than data—it’s a call to action for a cleaner, greener future.
</p>""")

# Updating the layout to include the description
layout1 = Column(introduction, description, p, range_slider, play_button)
#show(layout)
#pn.serve(layout)


# Display plot and range slider
#layout = column(p, range_slider, play_button)
#show(layout)

data2 = pd.read_csv('plastic-production-by-sector.csv') #the path needs to be inserted accordingly to recreate visualization

df2 = data2

df2.head()

df2.tail()

# Load data
data_path = 'plastic-production-by-sector.csv'
df = pd.read_csv(data_path)

df = df.rename(columns={
    'Road marking': 'Road_marking',
    'Marine coatings': 'Marine_coatings',
    'Personal care products': 'Personal_care_products',
    'Industrial machinery': 'Industrial_machinery',
    'Electronics': 'Electronics',
    'Textile sector': 'Textile_sector',
    'Consumer and institutional products': 'Consumer_and_institutional_products',
    'Transportation': 'Transportation',
    'Other': 'Other',
    'Building and construction': 'Building_and_construction',
    'Packaging': 'Packaging'
})

df.head()

df.tail()

# Data preparation
sectors = [
    "Packaging", "Building_and_construction", "Other", "Transportation",
    "Consumer_and_institutional_products", "Textile_sector", "Electronics",
    "Industrial_machinery", "Personal_care_products", "Marine_coatings", "Road_marking"
]

# Scale production values to millions and create cumulative stacked data
df_scaled = df[sectors].div(1_000_000)  # Scaling by 1,000,000
df_scaled['Year'] = df['Year']  # Add the Year column back
df_stacked = df_scaled.cumsum(axis=1)  # Cumulative sum for stacking
df_stacked['Year'] = df['Year']  # Add the Year column back

df_stacked.columns = df_stacked.columns.str.strip()

# Create ColumnDataSource for the plot
source = ColumnDataSource(data=df_stacked)

# Initialize the Bokeh plot
p = figure(
    title="Global Primary Plastic Production by Industrial Sector (1990-2019)",
    x_axis_label="Year",
    y_axis_label="Plastic Production (Millions of Tonnes)",
    x_range=(1990, 2019),
    width=1200,
    height=700
)


# Setting the title font size
p.title.text_font_size = "20pt"  # Adjust the font size of the title
p.title.text_font = "Times New Roman"

# Muted earthy color palette (refined for clarity)
colors = [
    "#7D4B47", "#5F6A6A", "#A9B1A0", "#A17961", "#617B7B",
    "#7C8C4F", "#B28B3B", "#6C5A4A", "#9A7C54", "#B4B98B", "#6C9A8B"
]

# Create a function to generate stacked areas in the order of legend sectors
def create_stacked_areas(sectors, df_stacked, source, p):
    renderers = []
    legend_items = []

    # Loop through the sectors and create stacked areas
    for i, sector in enumerate(sectors):
        if i == 0:
            renderer = p.varea(x='Year', y1=0, y2=sector, source=source, color=colors[i])
        else:
            renderer = p.varea(
                x='Year',
                y1=sectors[i - 1],
                y2=sector,
                source=source,
                color=colors[i]
            )
        renderers.append(renderer)
        legend_items.append((sector, [renderer]))

    return renderers, legend_items

# Generate the stacked areas and legend
renderers, legend_items = create_stacked_areas(sectors, df_stacked, source, p)

# Reverse the legend items
legend_items_reversed = list(reversed(legend_items))

# Add a reversed legend outside the plot, matching the order in the plot
legend = Legend(items=legend_items_reversed, location="center", title="Industrial Sectors")
p.add_layout(legend, 'right')

# Hover tool for interactivity with reversed tooltip order
hover = HoverTool()
hover.tooltips = [
    ("Year", "@Year"),
]

# Reverse the order of sectors in the tooltip
for sector in reversed(sectors):  # Reverse the sectors for the tooltip
    hover.tooltips.append((sector, f"@{sector}"))

p.add_tools(hover)

# Dropdown menu for selecting a sector
dropdown = Select(title="Highlight Sector:", value="All", options=["All"] + sectors)

# JavaScript callback for dropdown menu to toggle the visibility of sectors
dropdown_callback_code = """
const selected_sector = dropdown.value;
for (let i = 0; i < renderers.length; i++) {
    renderers[i].visible = (selected_sector === "All" || sectors[i] === selected_sector);
}
"""
dropdown_callback = CustomJS(
    args=dict(renderers=renderers, dropdown=dropdown, sectors=sectors),
    code=dropdown_callback_code
)
dropdown.js_on_change("value", dropdown_callback)

# Add a RangeSlider for filtering data
range_slider = RangeSlider(start=1990, end=2019, value=(1990, 1990), step=1, title="Year Range", width=900)

# JavaScript callback for RangeSlider
slider_callback_code = """
const start = range_slider.value[0];
const end = range_slider.value[1];
const filtered_data = {Year: [], };
for (const sector of sectors) { filtered_data[sector] = []; }

for (let i = 0; i < all_years.length; i++) {
    if (all_years[i] >= start && all_years[i] <= end) {
        filtered_data['Year'].push(all_years[i]);
        for (const sector of sectors) {
            filtered_data[sector].push(all_sectors[sector][i]);
        }
    }
}
source.data = filtered_data;
source.change.emit();
"""
all_years = df_stacked['Year'].tolist()
all_sectors = {sector: df_stacked[sector].tolist() for sector in sectors}
range_slider.js_on_change(
    'value',
    CustomJS(args=dict(source=source, range_slider=range_slider, all_years=all_years, all_sectors=all_sectors, sectors=sectors), code=slider_callback_code)
)

# Add a Play button for animation
play_button = Button(label="Play", button_type="success")

# JavaScript callback for the Play button with smoother animation and dynamic x-axis range update
play_callback_code = """
let playing = false;
let interval;

play_button.on_click(() => {
    playing = !playing; // Toggle play/pause
    play_button.label = playing ? "Pause" : "Play";

    if (playing) {
        interval = setInterval(() => {
            const [start, end] = range_slider.value;
            if (end >= range_slider.end) {
                clearInterval(interval); // Stop if the max year is reached
                play_button.label = "Play"; // Reset button
                playing = false;
            } else {
                range_slider.value = [start, end + 1]; // Increment the upper bound

                // Dynamically adjust the x-axis range based on the year range
                p.x_range.start = start; // Update the starting point of the x-axis
                p.x_range.end = end; // Update the ending point of the x-axis
            }
        }, 300); // Smooth update every 300ms
    } else {
        clearInterval(interval); // Pause the animation
    }
});
"""
play_button.js_on_click(
    CustomJS(args=dict(range_slider=range_slider, play_button=play_button, p=p), code=play_callback_code)
)

# Narrative introduction
narrative = Div(text="""<h1 style="text-align:left;">Tracing the Footprints of Plastic: Industrial Growth and Sustainability:</h1>
<p style="text-align: justify; font-size: 14px; margin-top: 10px;">
In our journey through plastic production, we saw the relentless rise of plastic as a cornerstone of modern life.
But where does it all go? This visualization shifts the lens to focus on the industrial sectors that drive global plastic production.
Each layer tells a story—a story of packaging, construction, and consumer products—and the complex interplay of human needs and environmental costs.<br><br>
As you explore this visualization, consider how our reliance on plastic infiltrates every aspect of industry and daily life.
Let it prompt reflection: What role can innovation play in transforming these sectors toward sustainability?
The challenge is daunting, but every story has a turning point. Let this be ours.
</p>""")

# Update layout to include the narrative
layout2 = Column(narrative, dropdown, p, Row(play_button, range_slider))
#output_notebook()
#show(layout)
#pn.serve(layout)

# Layout and show (reversed order of range_slider and play_button)
#layout = column(dropdown, p, row(play_button, range_slider))
#output_notebook()
#show(layout)

data3 = pd.read_csv('plastic-waste-generation-total.csv') #the path needs to be inserted accordingly to recreate visualization

df3=data3
df3.head(5)

df3.tail(5)

# Display Bokeh plots in the notebook
#output_notebook()

# Load the plastic waste dataset
data_path = 'plastic-waste-generation-total.csv'
df = pd.read_csv(data_path)

# Filter for the year 2010
df = df[df['Year'] == 2010]

# Create a new column that formats the plastic waste generation values to millions
df['Plastic waste generation (millions of tonnes)'] = df['Plastic waste generation (tonnes, total)'] / 1_000_000

# Download and load a GeoJSON file for world boundaries
world_path = 'https://github.com/nvkelso/natural-earth-vector/raw/master/geojson/ne_110m_admin_0_countries.geojson'
world = gpd.read_file(world_path)

# Merge GeoDataFrame with the plastic waste dataset
merged = world.merge(df, how='left', left_on='ISO_A3', right_on='Code')

# Fill NaN values with 0 for visualization purposes (later will handle no-data separately)
merged['Plastic waste generation (millions of tonnes)'] = merged['Plastic waste generation (millions of tonnes)'].fillna(0)

# Bin data into intervals for the interactive legend, scaled to millions
bins = np.linspace(merged['Plastic waste generation (millions of tonnes)'].min(),
                   merged['Plastic waste generation (millions of tonnes)'].max(), 6)

# Add a bin for "No Data" to the end
bins_with_na = np.append(bins, [0])
merged['bin'] = pd.cut(merged['Plastic waste generation (millions of tonnes)'], bins=bins, labels=False, include_lowest=True)

# Create labels for the interactive legend
labels = [f"{bins_with_na[i]:,.1f}M - {bins_with_na[i + 1]:,.1f}M" for i in range(len(bins_with_na) - 1)]
labels.append("No Data")

# Remove the specific problematic label if it exists
if "59.1M - 0.0M" in labels:
    labels.remove("59.1M - 0.0M")


legend_buttons = CheckboxButtonGroup(labels=labels, active=[0])  # Initially select the first bin

# Convert the merged GeoDataFrame to GeoJSON and add the new column 'Plastic waste generation (millions of tonnes)'
geo_source = GeoJSONDataSource(geojson=json.dumps(json.loads(merged.to_json())))


# Calculate the color manually using Viridis256 palette
min_value = df['Plastic waste generation (millions of tonnes)'].min()
max_value = df['Plastic waste generation (millions of tonnes)'].max()

# Normalize the values to the range [0, 1] to use the Viridis256 palette
normalized_values = (merged['Plastic waste generation (millions of tonnes)'] - min_value) / (max_value - min_value)

# Map the normalized values to colors using the Viridis256 palette
colors = [Viridis256[int(value * (len(Viridis256) - 1))] for value in normalized_values]

# Add the colors as a new column to the geo_source
merged['color'] = colors  # Add the color column to the merged DataFrame
geo_source = GeoJSONDataSource(geojson=json.dumps(json.loads(merged.to_json())))

# Create the Bokeh figure
p = figure(title='Plastic Waste Generation, 2019',
           height=600, width=950,
           toolbar_location='right', tools='pan, wheel_zoom, reset')


# Setting the title font size
p.title.text_font_size = "20pt"  # Adjust the font size of the title
p.title.text_font = "Times New Roman"

# Create the HoverTool for displaying the country name and plastic waste value
hover = HoverTool()
hover.tooltips = [
    ("Country", "@NAME"),
    ("Plastic Waste (Millions of Tonnes)", "@{Plastic waste generation (millions of tonnes)}{0.0}M")
]

# Add the HoverTool to the figure
p.add_tools(hover)

# Add patches (countries) to the figure
p.patches('xs', 'ys', source=geo_source,
          fill_color='color', fill_alpha='fill_alpha',
          line_color='black', line_width=0.5)

# Initialize a dictionary to store original colors
original_colors = {iso: color for iso, color in zip(merged['ISO_A3'], colors)}

# Set initial fill_alpha to 0.7 for all countries and store original colors
geojson_data = json.loads(geo_source.geojson)
for feature in geojson_data['features']:
    feature['properties']['fill_alpha'] = 0.7
    feature['properties']['fill_color'] = original_colors.get(feature['properties']['ISO_A3'], "#D3D3D3")  # Use original or gray color
geo_source.geojson = json.dumps(geojson_data)

# Create the color map for the plastic waste generation data
color_map = linear_cmap(field_name='Plastic waste generation (millions of tonnes)',
                        palette=Viridis256, low=min_value, high=max_value)

# Add a title to the color bar
color_bar = ColorBar(color_mapper=color_map['transform'], width=8, location=(0, 0),
                     title="Plastic generation (millions of tonnes)")

# Add the color bar to the plot
p.add_layout(color_bar, 'right')


# JavaScript callback for interactive legend
# JavaScript callback for interactive legend (adjusted for correct bin behavior)
callback = CustomJS(args=dict(source=geo_source, bins=bins_with_na[:-1], buttons=legend_buttons, original_colors=original_colors), code="""
    const data = JSON.parse(source.geojson);  // Parse GeoJSON
    const features = data.features;

    // Get active bins from the legend buttons
    const active_bins = buttons.active;

    // Define a light gray color for countries that are not selected
    const grayColor = "#D3D3D3";  // Very light gray color

    // Iterate through features and update 'fill_color' based on selected bins
    for (const feature of features) {
        const value = feature.properties['Plastic waste generation (millions of tonnes)'];
        let bin = -1;

        // Check for "No Data" bin
        if (value === 0) {
            bin = bins.length;  // "No Data" bin should be at the end
        } else {
            // Identify the correct bin index
            for (let i = 0; i < bins.length - 1; i++) {
                if (value >= bins[i] && value < bins[i + 1]) {
                    bin = i;
                    break;
                }
            }
        }

        // Adjust fill color and alpha based on bin status
        if (active_bins.includes(bin)) {
            feature.properties['fill_color'] = original_colors[feature.properties['ISO_A3']];  // Restore original color
            feature.properties['fill_alpha'] = 0.7;  // Normal alpha for selected bins
        } else {
            feature.properties['fill_color'] = grayColor;  // Set light gray color for unselected bins
            feature.properties['fill_alpha'] = 0.3;  // Lower alpha for grayed-out countries
        }
    }

    // Update the GeoJSON source
    source.geojson = JSON.stringify(data);
    source.change.emit();
""")


# Attach the callback to the buttons
legend_buttons.js_on_change('active', callback)

# Narrative introduction
narrative = Div(text="""<h1 style="text-align:left;">Plastic Borders: A Crisis Without Boundaries</h1>
<p style="text-align: justify; font-size: 14px; margin-top: 10px;">
We've traversed the sectors fueling plastic production, but now we zoom out to the global stage.
This visualization paints a sobering portrait of our planet in 2019—a snapshot of plastic waste generation that transcends borders.
Each country's hue reflects its contribution to this growing challenge.<br><br>
Yet, this is not just a story of data; it's a call to action.
The plastic waste crisis is not confined to the regions in darker tones—it spills into oceans, seeps into soils,
and shapes the legacy we leave behind. Explore this map and reflect on the shared responsibility
to shift from waste to worth, from problems to solutions. Together, we can rewrite this story.
</p>""")

# Update layout to include the narrative
layout3 = Column(narrative, p, legend_buttons)
#show(layout)
#pn.serve(layout)


# Display the map and custom legend together (no changes here)
#layout = column(p, legend_buttons)
#show(layout)

data4 = pd.read_csv('mismanaged-plastic-waste-per-capita.csv') #the path needs to be inserted accordingly to recreate visualization
data5 = pd.read_csv('GDP_per_capita.csv') #the path needs to be inserted accordingly to recreate visualization

df4 = data4
df5 = data5

df4.head(15)

df4.tail()

df5.head(5)

df5.tail()

# Step 1: Clean df4 by renaming columns for clarity
df4_cleaned = df4[['Entity', 'Mismanaged plastic waste per capita (kg per year)']].rename(columns={'Entity': 'Country Name'})

# Step 2: Clean df5 by selecting the columns for Country Name and GDP per capita in 2019
df5_cleaned = df5[['Country Name', '2019 [YR2019]']].rename(columns={'2019 [YR2019]': 'GDP per capita (USD)'})

# Step 3: Merge the two dataframes on 'Country Name' (use an outer join to keep all countries from df4)
merged_df = pd.merge(df4_cleaned, df5_cleaned, on='Country Name', how='inner')

num_rows = merged_df.shape[0]
print(f"Number of rows: {num_rows}")

# Function to get continent based on country name
def get_continent(country_name):
    try:
        country_code = pc.country_name_to_country_alpha2(country_name)
        continent = pc.country_alpha2_to_continent_code(country_code)
        return continent
    except:
        return None  # For countries not found or errors

# Apply the function to get continents
merged_df['Continent'] = merged_df['Country Name'].apply(get_continent)

continent_full_names = {
    'AF': 'Africa',
    'AS': 'Asia',
    'EU': 'Europe',
    'NA': 'North America',
    'SA': 'South America',
    'OC': 'Oceania'
}

# Replace continent abbreviations with full names
merged_df['Continent'] = merged_df['Continent'].map(continent_full_names).fillna(merged_df['Continent'])

# Define a color mapping for each continent
continent_colors = {
    'Africa': '#FFD700',  # Gold
    'Asia': '#FF4500',    # OrangeRed
    'Europe': '#4169E1',  # RoyalBlue
    'North America': '#32CD32',  # LimeGreen
    'South America': '#8A2BE2',  # BlueViolet
    'Oceania': '#FF69B4'   # HotPink
}

# Map colors to the Continent column
merged_df['color'] = merged_df['Continent'].map(continent_colors)

merged_df_cleaned = merged_df

# Display the updated dataframe
print(merged_df_cleaned.head(10))
len(merged_df_cleaned)

print(merged_df_cleaned.columns)

# Ensure GDP per capita is numeric after handling missing values
merged_df_cleaned['GDP per capita (USD)'] = pd.to_numeric(merged_df_cleaned['GDP per capita (USD)'], errors='coerce')

# Check if the color column has any missing values
print(merged_df_cleaned['color'].isnull().sum())

# If color column has missing values, fill them with a default color (for example, 'grey')
merged_df_cleaned['color'].fillna('grey', inplace=True)

# Apply the function to get continents
merged_df_cleaned['Continent'] = merged_df_cleaned['Country Name'].apply(get_continent)

continent_full_names = {
    'AF': 'Africa',
    'AS': 'Asia',
    'EU': 'Europe',
    'NA': 'North America',
    'SA': 'South America',
    'OC': 'Oceania'
}

# Replace continent abbreviations with full names
merged_df_cleaned['Continent'] = merged_df_cleaned['Continent'].map(continent_full_names).fillna(merged_df_cleaned['Continent'])

# Create a ColumnDataSource
source = ColumnDataSource(merged_df_cleaned)

# Create the Bokeh plot with a larger size
p = figure(
    title="Mismanaged Plastic Waste per Capita vs. GDP per Capita, 2019",
    x_axis_label="GDP per capita (constant 2019 international $)",
    y_axis_label="Mismanaged plastic waste per capita (kg per person)",
    tools="pan,wheel_zoom,box_zoom,reset",
    width=1200,  # Increased width
    height=800   # Increased height
)


# Setting the title font size
p.title.text_font_size = "20pt"  # Adjust the font size of the title
p.title.text_font = "Times New Roman"

# Add scatter plot with color based on 'color' column
scatter = p.scatter(
    x='GDP per capita (USD)',
    y='Mismanaged plastic waste per capita (kg per year)',
    size=10, color='color', alpha=0.6, source=source, legend_field='Continent'
)

# Add a hover tool
hover = HoverTool()
hover.tooltips = [
    ("Country", "@{Country Name}"),
    ("Mismanaged Plastic Waste", "@{Mismanaged plastic waste per capita (kg per year)}{0.0} kg per person"),
    ("GDP per Capita", "@{GDP per capita (USD)}{0,0} $")
]
p.add_tools(hover)

# Format the x-axis labels with a thousand separator and a dollar sign
p.xaxis.formatter = NumeralTickFormatter(format="0,0$")

# Style the plot
p.title.text_font_size = "16pt"
p.xaxis.axis_label_text_font_size = "12pt"
p.yaxis.axis_label_text_font_size = "12pt"
p.xaxis.axis_label_text_font_style = 'bold'
p.yaxis.axis_label_text_font_style = 'bold'

# Move the legend outside the plot and make it interactive
p.legend.location = "top_right"
p.legend.orientation = "vertical"  # Stack the legend items vertically
p.legend.margin = 20  # Add margin around the legend

# Narrative introduction
narrative = Div(text="""
<h1 style="text-align:left;">Linking Prosperity and Pollution: A Paradox in Plastic Management</h1>
<p style="text-align: justify; font-size: 14px; margin-top: 10px;">
Is economic prosperity a shield against environmental degradation, or does it amplify our ecological footprint?
This visualization juxtaposes GDP per capita with mismanaged plastic waste per capita across nations in 2019.
Each point represents a country, its color encoding the continent it belongs to.<br><br>
While richer nations cluster towards the lower right—indicating lower mismanaged waste—poorer countries often
appear higher on the y-axis, exposing vulnerabilities in waste management infrastructure.
Yet, exceptions abound, challenging assumptions and hinting at cultural, policy, and geographic nuances.<br><br>
This plot invites you to navigate the complexities of affluence and accountability.
How can nations break free from this paradox to harmonize growth with stewardship?
</p>
""")

# Combine narrative and plot
layout4 = Column(narrative, p)
#show(layout)
#pn.serve(layout)



# Show the plot
#show(p)

data6 = pd.read_csv('waste-items-ocean-region.csv') #the path needs to be inserted accordingly to recreate visualization

df6 = data6

df6.head()

# Add narrative text at the top
main_title = Div(
    text="""
    <h1 style='text-align: left;'>Unveiling the Plastic Menace: A Regional Analysis of Ocean Waste</h1>
<p style="text-align: justify; font-size: 14px; margin-top: 10px;">
    Plastic pollution has become an omnipresent threat to marine ecosystems. This visualization highlights the top waste items by region, illustrating how consumption habits, waste management practices, and socioeconomic factors manifest uniquely across the globe.

Each chart reveals the top 10 plastic items found in oceans for a specific region. The horizontal bars quantify their prevalence, while the adjacent labels provide percentages for clarity. By juxtaposing these trends, we can uncover patterns and anomalies—such as which regions grapple with certain waste items more than others—and identify focal points for global cleanup and prevention efforts.

Dive into the data to uncover the untold story of plastic waste across our oceans.
    </p>
    """)

plots = []

# Melt the dataset into long format
data_melted = data6.melt(
    id_vars=["Entity", "Code", "Year"],
    var_name="Region",
    value_name="Percentage"
)

# Drop rows with NaN percentages
data_melted = data_melted.dropna(subset=["Percentage"])

# Initialize a list to store the individual region plots
plots = []

# Get unique regions
regions = data_melted['Region'].unique()


for region in regions:
    region_data = data_melted[data_melted['Region'] == region].nlargest(10, "Percentage")
    region_data["PercentageLabel"] = region_data["Percentage"].astype(str) + "%"

    source = ColumnDataSource(data=dict(
        items=region_data['Entity'],
        percentages=region_data['Percentage'],
        labels=region_data['PercentageLabel']
    ))

    # Create figure
    p = figure(
        y_range=region_data['Entity'],
        title=f"{region}",
        tools="",
        toolbar_location=None,
        height=400,
        width=700
    )
    p.hbar(
        y="items",
        right="percentages",
        height=0.8,
        source=source,
        color="#718dbf"
    )

    # Add hover tool
    hover = HoverTool()
    hover.tooltips = [
        ("Item", "@items"),
        ("Percentage", "@percentages{0.0}%")
    ]
    p.add_tools(hover)

    # Configure labels
    labels = LabelSet(
        x='percentages',
        y='items',
        text='labels',
        x_offset=5,
        text_font_size="10pt",
        source=source
    )
    p.add_layout(labels)

    # Style plot
    p.x_range.end = region_data['Percentage'].max() + 5
    p.xaxis.axis_label = "Percentage"
    p.yaxis.axis_label = "Waste Items"
    p.title.text_font_size = "14pt"
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None

    plots.append(p)


# Arrange plots
grid = gridplot([plots[:2], plots[2:4], plots[4:6]])
layout5 = Column(main_title, grid)

# Show layout
#show(layout)
#pn.serve(layout)

# Conclusion text
conclusion = Div(
    text="""
    <h1 style="text-align:center;">Paving the Way for Change</h1>
<p style="text-align: justify; font-size: 14px; margin-top: 10px;">
        The visualizations reveal stark disparities in plastic waste generation and management worldwide.
        Wealthier nations often exhibit lower levels of mismanaged waste, yet they contribute significantly to global
        consumption. Conversely, economically vulnerable regions face the brunt of mismanagement, underscoring systemic
        inequalities in waste infrastructure and policy.
    </p>
<p style="text-align: justify; font-size: 14px; margin-top: 10px;">
        In the oceans, we see the consequences of human behavior laid bare: specific regions contend with distinct
        waste types, reflecting consumption patterns and regional dynamics. Addressing this crisis requires global
        cooperation, targeted policy interventions, and a commitment to sustainability across all sectors of society.
    </p>
<p style="text-align: justify; font-size: 14px; margin-top: 10px;">
        These visualizations serve as a call to action—empowering individuals, organizations, and policymakers to
        understand the problem and take informed steps toward a cleaner, healthier planet.
    </p>
    """
)

combined_layout = Column(
    layout1,  # First visualization
    layout2,  # Second visualization
    layout3,  # Third visualization
    layout4,
    layout5,
    conclusion,
    sizing_mode="stretch_width"
)

#full_layout = column(combined_layout, conclusion, sizing_mode = "stretch_width")

#full_layout.align = 'center'

#pn.serve(combined_layout)

#pn.serve(combined_layout, show=False, port=10000, address="0.0.0.0")
#pn.serve(combined_layout, show=False, title="Plastic Dashboard", port=10000, address="0.0.0.0")

#combined_layout.servable()


#this ran locally with "python app.py" at server "http://localhost:5080"
#pn.serve(combined_layout, show=True, port=5080, address="localhost", title="Plastic Dashboard")

# This is for Render deployment
app = combined_layout.servable()
