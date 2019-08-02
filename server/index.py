from flask import Flask
from get_polylines import *

#cors added to allow for access on chrome
app = Flask(__name__)
Session = dict() #mapping of requestTokens to requestTokenSecrets and AccessTokenPair
@app.route("/getAggregatePolylines")
def serve_aggregate_polylines():
    return get_aggregate_polylines();
