import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine,reflect=True)
Base.classes.keys()
Station = Base.classes.station
Measurement = Base.classes.measurement

session = Session(engine)


app = Flask(__name__)

@app.route("/")
def home():
    return "/api/precipitation"
    return "/api/stations"
    return "/api/temperature"
    return "/api/<start>"
    return "/api/<start>/<end>"

@app.route("/api/precipitation")
def precipitation():
    x = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date_minus_yr = datetime.strptime(x[0],'%Y-%m-%d') - dt.timedelta(days=365)
    prcp = engine.execute(f"Select date,station,prcp from Measurement where date >= :x and prcp is not null", {'x': last_date_minus_yr}).fetchall()
    return jsonify(prcp)

@app.route("/api/stations")
def stations():
    stations_list = engine.execute('select * from station').fetchall()
    return jsonify(stations_list)

@app.route("/api/temperature")
def temperature():
    y = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date_minus_yr = datetime.strptime(y[0],'%Y-%m-%d') - dt.timedelta(days=365)
    tobs_highest_obs = engine.execute(f"Select date,station,tobs from Measurement where station='USC00519281' and date >= :y and tobs is not null ", {'y': last_date_minus_yr}).fetchall()
    return jsonify(tobs_highest_obs)

@app.route("/api/<start>")
def start(tobs_calc_from_start_date):
    x = session.query(Measurement.date).order_by(Measurement.date.asc()).first()
    startdate = datetime.strptime(x[0],'%Y-%m-%d') - dt.timedelta(days=365)
    enddate =  dt.date(2017, 8, 23)
    tobs_calc = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= startdate).filter(Measurement.date <= enddate).all()
    tobs_stats = list(np.ravel(tobs_calc))
    return jsonify(tobs_stats)




@app.route("/api/<start>/<end>")
def end(tobs_from_start_end_date):
    x = session.query(Measurement.date).order_by(Measurement.date.asc()).first()
    start_date = datetime.strptime(x[0],'%Y-%m-%d') - dt.timedelta(days=365)
    enddate =  session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    end_date =  dt.date(2017,8,23) - dt.timedelta(days=365)
    start_end_tobs = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
    filter(Measurements.date >= start_date).filter(Measurements.date <= end_date).all()
    one_yr_start_end_tobs = list(np.ravel(start_end_tobs))
    return jsonify(one_yr_start_end_tobs)





if __name__ == "__main__":
    app.run(debug=True)
