# import dash
# from dash import dcc, html, Input, Output, State
# import pandas as pd
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
# from IPython.display import HTML
# from matplotlib import colormaps
# from matplotlib.ticker import MultipleLocator
# import base64
# from io import BytesIO
# from matplotlib.animation import HTMLWriter

# races = pd.read_csv("formula-1/races.csv")
# lap_times = pd.read_csv("formula-1/lap_times.csv")
# drivers = pd.read_csv("formula-1/drivers.csv")

# # Merge lap_times with drivers to get driver names
# lap_driver = lap_times.merge(drivers[['driverId', 'forename', 'surname']], on='driverId', how='left')

# # Merge with races to get race names and year
# lap_driver_race = lap_driver.merge(races[['raceId', 'year', 'name']], on='raceId', how='left')

# # Example race selection for visualization (first race in the dataset)
# selected_race_id = lap_driver_race['raceId'].iloc[0]
# race_data = lap_driver_race[lap_driver_race['raceId'] == selected_race_id]

# # Sort by lap for visualization
# race_data = race_data.sort_values(by=['lap', 'position'])

# race_data.head()

# # Step 1: Data Preparation
# valid_race_ids = lap_driver_race['raceId'].unique()  # Races with lap data
# filtered_races = races[races['raceId'].isin(valid_race_ids)]

# # Dropdown options
# years = sorted(filtered_races['year'].unique())
# race_options = filtered_races[['raceId', 'year', 'name']].drop_duplicates()
# race_options['label'] = race_options['year'].astype(str) + " - " + race_options['name']
# race_dict = dict(zip(race_options['label'], race_options['raceId']))

# # Step 2: Dash App Initialization
# app = dash.Dash(__name__)
# app.title = "F1 Driver Positions Animation"

# # Step 3: App Layout
# app.layout = html.Div([
#     html.H1("F1 Driver Positions Over Laps", style={'textAlign': 'center'}),

#     # Dropdowns for Year and Race
#     html.Div([
#         html.Label("Select Year:"),
#         dcc.Dropdown(
#             id="year-dropdown",
#             options=[{'label': year, 'value': year} for year in years],
#             placeholder="Select a Year"
#         ),
#         html.Label("Select Race:"),
#         dcc.Dropdown(
#             id="race-dropdown",
#             placeholder="Select a Race"
#         )
#     ], style={'width': '50%', 'margin': 'auto'}),

#     html.Div(id="animation-container", style={'textAlign': 'center'})
# ])

# # Step 4: Callbacks
# # Update race dropdown based on selected year
# @app.callback(
#     Output('race-dropdown', 'options'),
#     Input('year-dropdown', 'value')
# )
# def update_race_dropdown(selected_year):
#     if selected_year is None:
#         return []
#     filtered_race_options = race_options[race_options['year'] == selected_year]
#     return [{'label': row['name'], 'value': row['label']} for _, row in filtered_race_options.iterrows()]

# import tempfile
# from matplotlib.animation import HTMLWriter

# @app.callback(
#     Output('animation-container', 'children'),
#     Input('race-dropdown', 'value')
# )
# def display_animation(selected_race_label):
#     print(f"Selected Race Label: {selected_race_label}")
#     if not selected_race_label or selected_race_label not in race_dict:
#         return "Invalid race selected. Please choose a valid race."

#     selected_race_id = race_dict[selected_race_label]
#     race_data = lap_driver_race[lap_driver_race['raceId'] == selected_race_id]

#     if race_data.empty:
#         return "No lap data available for the selected race."

#     # Create the Matplotlib figure
#     drivers_list = race_data[['driverId', 'forename', 'surname']].drop_duplicates()
#     fig, ax = plt.subplots(figsize=(15, 6))
#     ax.set_title(f"Driver Positions Over Laps - {selected_race_label}")
#     ax.set_xlabel("Lap")
#     ax.set_ylabel("Position")
#     ax.set_xlim(1, race_data['lap'].max())
#     ax.set_ylim(0.5, drivers_list.shape[0] + 0.5)
#     ax.invert_yaxis()
#     ax.yaxis.set_major_locator(MultipleLocator(1))

#     # Prepare color map and lines
#     cmap = colormaps['tab20'].resampled(len(drivers_list))
#     lines = {}
#     labels = []  # To store legend labels

#     for idx, driver_id in enumerate(drivers_list['driverId']):
#         driver_name = drivers_list.loc[drivers_list['driverId'] == driver_id, ['forename', 'surname']].iloc[0]
#         color = cmap(idx)
#         label = f"{driver_name['forename'][0]}. {driver_name['surname']}"
#         lines[driver_id], = ax.plot([], [], label=label, color=color)
#         labels.append(label)  # Append legend labels

#     # Add the legend outside the plot area
#     ax.legend(
#         loc='center left', bbox_to_anchor=(1.05, 0.5),
#         title="Drivers", fontsize='small', title_fontsize='medium'
#     )

#     plt.tight_layout()

#     def update(frame):
#         current_data = race_data[race_data['lap'] <= frame]
#         for driver_id, line in lines.items():
#             driver_data = current_data[current_data['driverId'] == driver_id]
#             line.set_data(driver_data['lap'], driver_data['position'])

#     ani = FuncAnimation(fig, update, frames=race_data['lap'].unique(), repeat=False, blit=False)

#     # Convert animation to HTML using to_jshtml()
#     animation_html = ani.to_jshtml()

#     # Return animation as an iframe
#     return html.Iframe(srcDoc=animation_html, width='100%', height='600px')

# # Step 5: Run the App
# if __name__ == '__main__':
#     app.run_server(debug=True, port=8080)
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import pandas as pd

app = FastAPI()

# Load CSV data
races = pd.read_csv("formula-1/races.csv")
lap_times = pd.read_csv("formula-1/lap_times.csv")
drivers = pd.read_csv("formula-1/drivers.csv")

lap_driver = lap_times.merge(drivers[['driverId', 'forename', 'surname']], on='driverId', how='left')
lap_driver_race = lap_driver.merge(races[['raceId', 'year', 'name']], on='raceId', how='left')

@app.get("/api/years")
async def get_years():
    years = sorted(lap_driver_race['year'].unique())
    return years

@app.get("/api/races")
async def get_races(year: int = Query(...)):
    filtered_races = lap_driver_race[lap_driver_race['year'] == year][['raceId', 'name']].drop_duplicates()
    return filtered_races.to_dict(orient="records")

@app.get("/api/race-data")
async def get_race_data(raceId: int = Query(...)):
    race_data = lap_driver_race[lap_driver_race['raceId'] == raceId]
    if race_data.empty:
        return JSONResponse({"error": "No data available for the selected race."}, status_code=404)
    response_data = {
        "laps": race_data['lap'].tolist(),
        "positions": race_data['position'].tolist(),
        "drivers": race_data[['driverId', 'forename', 'surname']].drop_duplicates().to_dict(orient="records")
    }
    return response_data
