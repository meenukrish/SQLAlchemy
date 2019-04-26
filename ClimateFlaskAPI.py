# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import join
from sqlalchemy import create_engine, func
import datetime as dt
from dateutil.parser import parse
# 1. import Flask
from flask import Flask , jsonify
import numpy as np

######################################################################################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite" , connect_args={'check_same_thread': False})
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# We can view all of the classes that automap found
Base.classes.keys()
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

##############################################################################################################

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
   
       return ( f"Welcome to my 'Climate API' page created using Python and Flask:</br></br>"
                f"Available Routes:<br/>"
                f"============ <br/>"
                f"/api/v1.0/precipitation <br/>"
                f"/api/v1.0/stations <br/>" 
                f"/api/v1.0/tobs <br/>"
                f"/api/v1.0/2012-02-28 <br/>"
                f"/api/v1.0/2012-02-28/2012-03-05 <br/>"
       )

# 4. Define what to do when a user hits the /about route
@app.route("/api/v1.0/precipitation")
def precipitation():
    strStartDate = session.query(Measurement.date).order_by(Measurement.date.desc()).first()  # find the latest date in dataset
    formattedDate = dt.datetime.strptime(strStartDate[0], '%Y-%m-%d')                         # String to DateTime format
    # Calculate the date 1 year ago from the last data point in the database
    Oneyearago = formattedDate - dt.timedelta(days=366)                                      # 366 for leap year
    # Perform a query to retrieve the data and precipitation scores

    results = session.query(Measurement.date,Measurement.prcp).\
                        filter(Measurement.date >= Oneyearago).\
                        order_by(Measurement.date.desc()).all()  
    
    Percpdict = {}
    for tup in results:
        Percpdict[tup[0]] = tup[1]
        
    return jsonify(Percpdict) 

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    
    StationsList = list(np.ravel(results))
    return jsonify(StationsList)
                                  

@app.route("/api/v1.0/tobs")
def tobs():

    strStartDate = session.query(Measurement.date).order_by(Measurement.date.desc()).first()  # find the latest date in dataset
    formattedDate = dt.datetime.strptime(strStartDate[0], '%Y-%m-%d')                         # String to DateTime format
    Oneyearago = formattedDate - dt.timedelta(days=366)                                       # 366 for leap year

   
    results = session.query(Measurement.tobs).filter(Measurement.date >= Oneyearago).all()

    tobsresults = list(np.ravel(results))

    return jsonify(tobsresults)


@app.route("/api/v1.0/<start>")
def caltemps_afterstart(start):

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), 
                            func.max(Measurement.tobs)).\
                            filter(Measurement.date >= start).all()

    tempresults = list(np.ravel(results))

    return jsonify(tempresults)

@app.route("/api/v1.0/<start>/<end>")
def caltemps_startEnd(start, end):

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), 
                            func.max(Measurement.tobs)).\
                            filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    tempresults = list(np.ravel(results))

    return jsonify(tempresults)


if __name__ == "__main__":
    app.run(debug=True)
