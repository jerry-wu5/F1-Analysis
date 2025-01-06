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


# from flask import Flask, render_template, request, jsonify
# import pandas as pd
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
# from io import BytesIO
# import base64

# # Flask app
# app = Flask(__name__)

# # Load data
# races = pd.read_csv("formula-1/races.csv")
# lap_times = pd.read_csv("formula-1/lap_times.csv")
# drivers = pd.read_csv("formula-1/drivers.csv")

# # Merge datasets
# lap_driver = lap_times.merge(drivers[['driverId', 'forename', 'surname']], on='driverId', how='left')
# lap_driver_race = lap_driver.merge(races[['raceId', 'year', 'name']], on='raceId', how='left')

# # Get valid years and races
# years = sorted(lap_driver_race['year'].unique())
# race_options = lap_driver_race[['raceId', 'year', 'name']].drop_duplicates()

# @app.route("/")
# def index():
#     return render_template("index.html", years=years)

# @app.route("/get-races", methods=["GET"])
# def get_races():
#     """Return a list of races for a selected year."""
#     year = request.args.get("year")
#     if not year:
#         return jsonify([])
#     filtered_races = race_options[race_options["year"] == int(year)]
#     races = [{"raceId": row["raceId"], "name": row["name"]} for _, row in filtered_races.iterrows()]
#     return jsonify(races)

# @app.route("/animate", methods=["GET"])
# def animate():
#     """Render animation for the selected race."""
#     race_id = request.args.get("raceId")
#     if not race_id:
#         return "No race selected.", 400

#     race_data = lap_driver_race[lap_driver_race["raceId"] == int(race_id)]
#     if race_data.empty:
#         return "No data available for this race.", 404

#     # Generate animation
#     fig, ax = plt.subplots(figsize=(15, 6))
#     ax.set_title("Driver Positions Over Laps")
#     ax.set_xlabel("Lap")
#     ax.set_ylabel("Position")
#     ax.set_xlim(1, race_data["lap"].max())
#     ax.set_ylim(0.5, race_data["position"].max() + 0.5)
#     ax.invert_yaxis()

#     # Prepare color map and lines
#     drivers_list = race_data[["driverId", "forename", "surname"]].drop_duplicates()
#     lines = {}
#     for driver_id in drivers_list["driverId"]:
#         lines[driver_id], = ax.plot([], [], label=driver_id)

#     def update(frame):
#         current_data = race_data[race_data["lap"] <= frame]
#         for driver_id, line in lines.items():
#             driver_data = current_data[current_data["driverId"] == driver_id]
#             line.set_data(driver_data["lap"], driver_data["position"])

#     ani = FuncAnimation(fig, update, frames=race_data["lap"].unique(), repeat=False)

#     # Convert animation to JavaScript HTML representation
#     animation_html = ani.to_jshtml()

#     # Return the animation HTML in the template
#     return render_template("animation.html", animation_html=animation_html)

# if __name__ == "__main__":
#     app.run_server(debug=True, port=8001)

import pandas as pd
import plotly.express as px
from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Initialize FastAPI app
app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load CSV data
races = pd.read_csv("formula-1/races.csv")
lap_times = pd.read_csv("formula-1/lap_times.csv")
drivers = pd.read_csv("formula-1/drivers.csv")

# Merge datasets
lap_driver = lap_times.merge(drivers[['driverId', 'forename', 'surname']], on='driverId', how='left')
lap_driver_race = lap_driver.merge(races[['raceId', 'year', 'name']], on='raceId', how='left')

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the home page with a dropdown for years."""
    years = sorted(lap_driver_race['year'].unique())
    return templates.TemplateResponse("index.html", {"request": request, "years": years})

@app.get("/get-races")
async def get_races(year: int = Query(...)):
    """API endpoint to get races for a given year."""
    filtered_races = lap_driver_race[lap_driver_race["year"] == year][["raceId", "name"]].drop_duplicates()
    if filtered_races.empty:
        raise HTTPException(status_code=404, detail="No races found for the selected year.")
    return filtered_races.to_dict(orient="records")

@app.get("/animate", response_class=HTMLResponse)
async def animate(request: Request, raceId: int = Query(...)):
    """Render animation for the selected race."""
    race_data = lap_driver_race[lap_driver_race["raceId"] == raceId]
    if race_data.empty:
        raise HTTPException(status_code=404, detail="No data available for the selected race.")

    # Extract the year and race name for the title
    race_name = race_data["name"].iloc[0]
    race_year = race_data["year"].iloc[0]
    graph_title = f"{race_year} {race_name} Summary"

    # Get available races for the current year
    races = lap_driver_race[lap_driver_race["year"] == race_year][["raceId", "name"]].drop_duplicates().to_dict(orient="records")
    years = sorted(lap_driver_race["year"].unique())

    # Prepare data for Plotly
    race_data = race_data.copy()
    race_data["Driver"] = race_data["forename"].str[0] + ". " + race_data["surname"]
    race_data["Full_Name"] = race_data["forename"] + " " + race_data["surname"]
    race_data = race_data.sort_values(["lap", "position"])
    race_data = race_data.drop_duplicates(subset=["lap", "Driver"])

    max_lap = race_data["lap"].max()
    expanded_data = pd.DataFrame()
    for lap in range(1, max_lap + 1):
        current_frame = race_data[race_data["lap"] <= lap].copy()
        current_frame["animation_frame"] = lap
        expanded_data = pd.concat([expanded_data, current_frame], ignore_index=True)

    # Create the Plotly line plot
    fig = px.line(
        expanded_data,
        x="lap",
        y="position",
        color="Driver",
        animation_frame="animation_frame",
        line_group="Driver",
        hover_name="Driver",
        hover_data={"Full_Name": True,"lap": True, "position": True, "animation_frame": False, "Driver": False},
        title=graph_title,
        labels={"lap": "Lap", "position": "Position"},
    )

    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
        height=800,
        width=1100,
        legend_title="Drivers",
        sliders=[{
            "active": 0,
            "steps": [{"args": [[lap], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate", "transition": {"duration": 0}}], "label": str(lap), "method": "animate"} for lap in sorted(expanded_data["animation_frame"].unique())],
            "currentvalue": {"prefix": "Lap: ", "font": {"size": 16}}
        }],
        updatemenus=[
            {
                "type": "buttons",
                "direction": "left",
                "x": 0.1,
                "y": -0.2,
                "buttons": [
                    {"label": "Play", "method": "animate", "args": [None, {"frame": {"duration": 500, "redraw": True}, "mode": "immediate", "transition": {"duration": 0}}]},
                    {"label": "Pause", "method": "animate", "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}]},
                    {"label": "Reset", "method": "animate", "args": [[1], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate", "transition": {"duration": 0}}]}
                ]
            }
        ],
        xaxis=dict(range=[1, max_lap], title="Lap"),
        yaxis=dict(
            autorange="reversed",
            title="Position",
            tickmode="array",
            tickvals=list(range(1, expanded_data["position"].max() + 1)),
            ticktext=[str(i) for i in range(1, expanded_data["position"].max() + 1)]
        ),
        legend=dict(itemclick="toggleothers", itemdoubleclick="toggle", title="Drivers")
    )

    plot_html = fig.to_html(full_html=False)

    return templates.TemplateResponse("animation.html", {
        "request": request,
        "plot_html": plot_html,
        "years": years,
        "races": races,
        "current_year": race_year,
        "current_raceId": raceId
    })
