import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Path to sqlite
hawaii_database_path = "Resources/hawaii.sqlite"

# # create engine to hawaii.sqlite
engine = create_engine(f"sqlite:///{hawaii_database_path}")
# conn = engine.connect()

# View all of the classes that automap found
Base = automap_base()
Base.prepare(engine,reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Set up Flask
app = Flask(__name__)
@app.route("/")
def climate():
    return (
        f"The available routes ARE:</br>"
        f"/api/v1.0/precipitation</br>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/<start></br>"
        f"/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/precipitation")
def prcp():
    # Design a query to retrieve the last 12 months of precipitation data and plot the results. 
    # Starting from the most recent data point in the database. 

    # Calculate the date one year from the last date in data set.
    last_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    # Perform a query to retrieve the date and precipitation scores
    precp_score = session.query(Measurement.date, Measurement.prcp).\
                    filter(Measurement.date >= last_year).all()
    #for date, prcp in precp_score:
    precp_dict = {date: prcp for date, prcp in precp_score}
    session.close()
    return jsonify(precp_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Design a query to calculate the total number stations in the dataset
    total_stations = session.query(Station.station).all()
    station_list = list(np.ravel(total_stations))
    session.close()
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def temperature():
# Calculate the date one year from the last date in data set.
    # Using the most active station id
    # Query the last 12 months of temperature observation data for this station and plot the results as a histogram
    # Calculate the date one year from the last date in data set.
    last_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= last_year).all()
    temp_list = list(np.ravel(results))
    session.close()
    return jsonify(temp_list)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def most_active(start=None,end=None):
    # Using the most active station id from the previous query, calculate the lowest, \
    # highest, and average temperature.
    if not end:
        total_temp = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).all()
        range_list = list(np.ravel(total_temp))
        return jsonify(range_list)
    total_temp1 = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).all()
    range_list1 = list(np.ravel(total_temp1))
    return jsonify(range_list1)

if __name__ == '__main__':
    app.run()