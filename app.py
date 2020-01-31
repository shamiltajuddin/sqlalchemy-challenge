import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def allroutes():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation outcomes"""
    # Query all precipitation outcomes
    results = session.query(Measurement.prcp,Measurement.date).all()

    session.close()

    prcp_data = []
    for prcp,date in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    station_data = list(np.ravel(results))

    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all tobs"""
    # Query all tobs
    tob_results = session.query(Measurement.date,  Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23').all()

    session.close()

    return jsonify(tob_results)


@app.route("/api/v1.0/<start>")
def start():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    # Query minimum temperature, the average temperature, and the max temperature
    min_temp = session.query(func.min(Measurement.tobs)).\
           filter(Measurement.date == start).all()
    max_temp = session.query(func.max(Measurement.tobs)).\
           filter(Measurement.date == start).all()
    avg_temp = session.query(func.avg(Measurement.tobs)).\
           filter(Measurement.date == start).all()
    
    
    result = min_temp, max_temp, avg_temp
    temp_list = list(np.ravel(result))
    temp_info = {'min_temp':temp_list[0], 'max_temp':temp_list[1], 'avg_temp':temp_list[2]}
    
    return jsonify(temp_info)

@app.route("/api/v1.0/<start>/<end>")
def end():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    # Query minimum temperature, the average temperature, and the max temperature
    end_min_temp = session.query(func.min(Measurement.tobs)).\
           filter(Measurement.date == end).all()
    end_max_temp = session.query(func.max(Measurement.tobs)).\
           filter(Measurement.date == end).all()
    end_avg_temp = session.query(func.avg(Measurement.tobs)).\
           filter(Measurement.date == end).all()
    
    
    result = end_min_temp, end_max_temp, end_avg_temp
    end_temp_list = list(np.ravel(result))
    end_temp_info = {'end_min_temp':end_temp_list[0], 'end_max_temp':end_temp_list[1], 'end_avg_temp':end_temp_list[2]}
    
    return jsonify(end_temp_info)


if __name__ == '__main__':
    app.run(debug=True)
