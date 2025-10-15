from flask import Flask, render_template, request, redirect
import requests
import json
import folium
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'data.json'

def get_location():
    try:
        res = requests.get("http://ip-api.com/json/").json()
        return {
            'lat': res.get("lat", 0),
            'lon': res.get("lon", 0),
            'city': res.get("city", "Inconnu")
        }
    except:
        return {'lat': 0, 'lon': 0, 'city': "Erreur"}

def save_entry(entry):
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
    except:
        data = []

    data.append(entry)

    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def generate_map():
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
    except:
        data = []

    # Créer la carte centrée sur un point global
    map = folium.Map(location=[20, 0], zoom_start=2)

    for entry in data:
        folium.Marker(
            location=[entry['lat'], entry['lon']],
            popup=f"{entry['humeur']} ({entry['ville']})<br>{entry['commentaire']}",
            icon=folium.Icon(color='blue')
        ).add_to(map)

    map.save("static/map.html")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        humeur = request.form.get("humeur")
        commentaire = request.form.get("commentaire")

        loc = get_location()

        entry = {
            "date": datetime.now().isoformat(),
            "humeur": humeur,
            "commentaire": commentaire,
            "lat": loc['lat'],
            "lon": loc['lon'],
            "ville": loc['city']
        }

        save_entry(entry)
        generate_map()

        return redirect("/")

    generate_map()
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
