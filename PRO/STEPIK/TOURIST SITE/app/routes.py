from flask import render_template
from app import app
from app.data import title, subtitle, departures, tours, description

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title=title, subtitle=subtitle, description = description, departures=departures, tours=tours)

@app.route('/departure/<departure>')
def destination(departure):
    l_tours = list()
    for k,v in tours.items():
        v["id"] = k
        l_tours.append(v)
    return render_template('departure.html', departure = departure, departures = departures, tours=tours, l_tours=l_tours)

@app.route('/tour/<id>')
def tour(id):
    return render_template('tour.html', tour = tours[int(id)], destination=departures[tours[int(id)]['departure']], departures=departures)

if __name__ == '__main__':
	app.run()