import pytest
from src import db_init
from src.messages import *


def test_db_rebuild():
    try:
        db_init.db_reset()
    except Exception:
        pytest.fail("DB rebuild failure")

# ##### Test Patient Messages

def test_patient_info():
  db_init.db_reset()
  p = Patient.select().where(Patient.id == 1).get()
  assert response_to_sms_body("#info", p) == INFO

def test_patient_name():
  db_init.db_reset()
  p = Patient.select().where(Patient.id == 1).get()
  r = response_to_sms_body("name klingon", p)
  assert Patient.select().where(Patient.id == 1).get().name == "klingon"

def test_patient_loc():
  db_init.db_reset()
  p = Patient.select().where(Patient.id == 1).get()
  r = response_to_sms_body("loc Yorkville", p)
  assert Patient.select().where(Patient.id == 1).get().loc == 1

def test_patient_sick():
  db_init.db_reset()
  p = Patient.select().where(Patient.id == 1).get()
  r = response_to_sms_body("i'm sick", p)
  assert Patient.select().where(Patient.id == 1).get().status == "infected"

def test_patient_help():
  db_init.db_reset()
  p = Patient.select().where(Patient.id == 1).get()
  assert response_to_sms_body("#help", p) == patient_help()

# ##### Test HCWorker Messages

def test_hc_help():
  db_init.db_reset()
  h = HCWorker.select().where(HCWorker.id == 1).get()
  assert response_to_sms_body("#help", h) == hc_help()

def test_hc_todo():
  db_init.db_reset()
  h = HCWorker.select().where(HCWorker.id == 2).get()
  assert response_to_sms_body("todo", h) == \
  """INFECTED:
  SUSPECT: 3 <Chiefdom: 'Yorkville'> sam phone: 15551112224
  EXPOSED: 4 <Chiefdom: 'Yorkville'> earl phone: 15551112225"""

# TODO: add tests for remaining HCWorker messages

