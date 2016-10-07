__author__ = 'Kelsey'

from peewee import Model, CharField, ForeignKeyField, \
    TextField, FloatField, PostgresqlDatabase

from lib.log import log

# Default DATABASE_URL will be LOCAL_DB_DEFAULT below for local development
# Set environment variable DATABASE_URL if you want something different
# Other suitable cloud DBs:
# HEROKU_TEST_DB = "postgres://vyxede....."
# ELEPHANTSQL_TEST_DB = "postgres://bffueem....."
## THE PRODUCTION DB::

LOCAL_DB_DEFAULT = "postgres://localhost:5432/localDB"

import os
DATABASE_URL = os.environ.get('DATABASE_URL', LOCAL_DB_DEFAULT)

import pw_database_url
db_dict = pw_database_url.parse(DATABASE_URL)
print("Database dict: %s" % db_dict)

TheDB = PostgresqlDatabase(db_dict['name'],
                        user=db_dict['user'],
                        password=db_dict['password'],
                        host=db_dict['host'],
                        port=db_dict['port'])
TheDB.connect()


class BaseModel(Model):
    class Meta:
        database = TheDB
    @classmethod
    def exists(cls, expr):
        return cls.select().where(expr).exists()

class Chiefdom(BaseModel):
    name = CharField(unique=True)
    latitude = FloatField()
    longitude = FloatField()
    # Multi-valued: patients, health_workers

    def __unicode__(self):
        return self.name

class Patient(BaseModel):

    status_enum = ["suspect", "infected", "clear", "deceased", "exposed", "uncooperative"]

    phone = CharField(unique=True)
    name = CharField(default='?')
    status = CharField(default='suspect')  # suspect, infected, clear, deceased, contact
    location = ForeignKeyField(Chiefdom, related_name="patients")
    exposed_to = ForeignKeyField('self', related_name="did_expose", null=True)

    # Multi-valued:

    def __repr__(self):
        return "Patient(%s, %s, %s)" % (self.name, self.phone, self.location.name)
    def candidate_workers(self):
        return self.location.health_workers
    def __unicode__(self):
        return "%s: %s: %s" % (self.name, self.phone, self.location)

class HCWorker(BaseModel):
    phone = CharField(unique=True)
    name = CharField()
    location = ForeignKeyField(Chiefdom, related_name="health_workers")

    def __repr__(self):
        return "HCWorker(%s, %s, %s)" % (self.name, self.phone, self.location.name)
    def candidate_patients(self):
        return self.location.patients
    def __unicode__(self):
        return self.name

# class Contact(BaseModel):
#     sender = ForeignKeyField(Patient, related_name='contacts')
#     sent_on = CharField() # TODO: normalize?
#     description = TextField()


class SMS(BaseModel):
    sender = ForeignKeyField(Patient, related_name='sms_log')
    body = TextField()
    time = CharField()
    def __repr__(self):
        return "SMS case from: %s body:%s time: %s" % (self.sender.name, self.body, self.time)
    def __unicode__(self):
        return "SMS from %s on %s" % (self.sender.name, self.time)
