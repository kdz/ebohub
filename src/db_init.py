__author__ = 'Kelsey'

import datetime

from src.ebohub_model import *


# TO RESET your CURRENT DB:
#  python <thisFile.py>
# You can also import and selective use sample_data or initialize_sample_data

Models = [Chiefdom, Patient, SMS, HCWorker]

def drop_tables():
    TheDB.connect()
    for m in Models:
        m.drop_table(fail_silently=True, cascade=True)

def create_tables():
    TheDB.connect()
    for m in Models:
        m.create_table(fail_silently=False)

sample_data = {
    'chiefdoms': [
        ("Morningside Heights", 40.8090, -73.9624),
        ("Harlem", 40.8116, -73.9465),
        ("East Harlem", 40.7957, -73.9389),
        ("Upper West Side", 40.7870, -73.9754),
        ("Lincoln Square", 40.7738, -73.9845),
        ("Carnegie Hill", 40.7847, -73.9561),
        ("Yorkville", 40.7762, -73.9492),
        ("Upper East Side", 40.7736, -73.9566),
        ("Lenox Hill", 40.7690, -73.9620),
        ("Hell's Kitchen", 40.7638, -73.9918),
        ("Theater District", 40.7590, -73.9845),
        ("Midtown East", 40.7540, -73.9668),
        ("Murray Hill", 40.7479, -73.9757)],
    'patients': [('+15551112222', "bob", "Harlem", "infected"),
                 ('+15551112223', "don", "Lenox Hill", "suspect"),
                 ('+15551112224', "sam", "Lincoln Square", "suspect"),
                 ('+15551112225', "earl", "Yorkville", "exposed"),
                 ('+15551112226', "gary", "Yorkville", "suspect"),
                 ('+15551112227', "hank", "Yorkville", "infected")],
    'hc_workers': [("+15129815570", "maria", "Harlem"),
                   ("+15128505584", "tina", "Murray Hill"),
                   ("+15128504380", "kelsey", "Yorkville"),
                   ("+15126898496", "dobie", "Harlem")],
    'smss': [("bob", "hello I'm Bob"),
             ("sam", "hi I'm Sam"),
             ("bob", "#help")],
#    'contacts': [("bob", "21 Sept 2014", "was cozy with sally yesterday"),
#                ("sam", "12 Oct 2014", "rode W27 bus around 9:00am this morning from Downtown to Midtown")]
}


def initialize_sample_data(chiefdoms=[], patients=[], smss=[], hc_workers=[], contacts=[]):
    for city, lat, long in chiefdoms:
        Chiefdom.create(name=city, latitude=lat, longitude=long)
    for phone, name, city, status in patients:
        c_id = Chiefdom.get(name=city).id
        Patient.create(phone=phone, name=name, location=c_id, status=status)
    for name, body in smss:
        patient_id = Patient.get(name=name).id
        SMS.create(sender=patient_id, time=str(datetime.datetime.now()), body=body)
    for phone, name, city in hc_workers:
        c_id = Chiefdom.get(name=city).id
        HCWorker.create(phone=phone, name=name, location=c_id)
    # for name, date, description in contacts:
    #     patient_id = Patient.get(name=name).id
    #    Contact.create(sender=patient_id, sent_on=date, description=description)

def db_reset():
    print("Resetting database: %s url: %s" % (TheDB, DATABASE_URL))
    drop_tables()
    create_tables()
    initialize_sample_data(**sample_data)

if __name__ == "__main__":
    db_reset()