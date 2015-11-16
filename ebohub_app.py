__author__ = 'Kelsey'

from src.ebohub_model import *
import flask
from lib.flask_googlemaps import Map, GoogleMaps
import datetime

from lib.typing import *
import twilio.twiml
from parse import *
from src.messages import response_to_sms_body
from flask.ext import admin

TheApp = flask.Flask(__name__, static_url_path="/static")
TheApp.config['DEBUG'] = True  # helps both local & deployed debugging
GoogleMaps(TheApp)
TheAdmin = flask.ext.admin.Admin(TheApp, name="EboHub")


@TheApp.route("/")
def home():
    log("Entered HOME route")
    # r = flask.render_template('home.html')
    # return r
    return flask.redirect("admin", code=302)

@TheApp.route("/reset_db")
def reset_the_db():
    log("Reset Data Base")
    from src.db_init import db_reset
    db_reset()
    # r = flask.render_template('home.html')
    # return r
    return flask.redirect("admin", code=302)

class Marker:
    def __init__(self, **kw):
        self.__dict__ = kw
    def __repr__(self):
        return str((self.lat, self.lng, self.icon))

class MapView(admin.BaseView):
    @admin.expose("/")
    def index(self):
        log("Entered LOG_AND_MAP route")
        infected = Patient.select().where((Patient.status == 'infected'))
        markers_1 = [Marker(lat=p.location.latitude,
            lng=p.location.longitude,
            icon='/static/images/icon-red.png') for p in infected]
        exposed = Patient.select().where((Patient.status == 'exposed'))
        markers_2 = [Marker(lat=p.location.latitude,
            lng=p.location.longitude,
            icon='/static/images/icon-blue.png') for p in exposed]
        suspects = Patient.select().where((Patient.status == 'suspect'))
        markers_3 = [Marker(lat=p.location.latitude,
            lng=p.location.longitude,
            icon='/static/images/icon-yellow.png') for p in suspects]

        markers = markers_1 + markers_2 + markers_3

        if markers != []:
            mid_lat = sum(m.lat for m in markers) / len(markers)
            mid_lng = sum(m.lng for m in markers) / len(markers)
        else:
            mid_lat, mid_lng = 39.1641, -99.6680 ## approx center of United States
        mymap = Map(
            identifier="view-side",
            lat=mid_lat,
            lng=mid_lng,
            markers=markers,
            zoom=9,
            style="height:600px;width:600px;margin:1;"
        )
        r = self.render('log_and_map.html', SMS=SMS, mymap=mymap)
        return r

def create_SMS(request) -> Tuple[str, Union[Patient, HCWorker]]:
    phone_number, body, when = request.values.get('From', ''), \
                               request.values.get('Body', ''), \
                               str(datetime.datetime.now())
    pat_query = Patient.select().where(Patient.phone == phone_number)
    hcw_query = HCWorker.select().where(HCWorker.phone == phone_number)

    if hcw_query.exists():
        return body, hcw_query.get()
    elif pat_query.exists():
        p = pat_query.get()
        SMS.create(sender=p.id, time=when, body=body)
        return body, p
    else:
        p = Patient.create(phone=phone_number, name='?', location=1)
        SMS.create(sender=p.id, time=when, body=body)
        return body, p

@TheApp.route("/new_sms", methods=['GET', 'POST'])
def new_sms():
    log("Entering new_sms, request.values=%s" % flask.request.values)
    body, patient = create_SMS(flask.request)
    response = twilio.twiml.Response()
    response.sms(response_to_sms_body(body, patient))
    return str(response)

@TheApp.route("/new_voice", methods=['GET', 'POST'])
def new_voice():
    log("Entering new_voice")
    # Fill in technical Twilio-ML HTTP header for response
    response = twilio.twiml.Response()
    # Fill in response body
    response.say('Call received. Press 1 to talk to Dr. X, Press 2 to talk to Dr. Y')
    # return the response as a string
    return str(response)



from flask.ext.admin.contrib.peewee import ModelView
TheAdmin.add_view(ModelView(Patient))
TheAdmin.add_view(ModelView(Chiefdom))
TheAdmin.add_view(ModelView(HCWorker))
TheAdmin.add_view(ModelView(SMS))
#TheAdmin.add_view(ModelView(Contact, name="Contact Tracing"))
TheAdmin.add_view(MapView(name='Logs and Map'))

TheApp.secret_key = 't\xad\xbbR\xc3\xd6t\xe4\xa09\x93j\x9cTw\xf4\xf3\xea\xb3>\xbc\xed~U'

if __name__ == "__main__":
    TheApp.run(passthrough_errors=True, use_reloader=False)