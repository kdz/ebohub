__author__ = 'Kelsey'

from src.ebohub_model import *
from src.ebola_info import INFO
import parse
from lib.typing import *
from src.twilio_setup import TW_client, TW_phone

### all message-actions take patient + msg-args, execute & return msg-string
###    supporting _actions return additional msg-strings to append

def location(p: Union[Patient, HCWorker], loc: str) -> str:
    log("loc(%s, %s)" % (p, loc))
    if Chiefdom.exists(Chiefdom.name == loc):
        cd = Chiefdom.get(Chiefdom.name == loc)
        p.location = cd
        p.save()
        msg1 = "Location updated to %s. " % cd.name

        if isinstance(p, Patient):
            if p.status == 'infected':
                return msg1 + _notify_closest_worker(p)
            else:
                return msg1
        else:
            return msg1
    else:
        locs = [l.name for l in Chiefdom.select()]
        locString = ", ".join(locs)
        return "Sorry, invalid location. Valid locations are: %s" % (locString)

def _notify_closest_worker(patient: Patient) -> str:
    workers = patient.candidate_workers()
    if workers.count() > 0:
        w = workers.get()
        msg = 'Please contact patient %s at %s in %s' % (patient.name, patient.phone, patient.location.name)
        TW_client.messages.create(to=w.phone, from_=TW_phone, body=msg)
        return "Health worker %s at %s notified to contact you shortly" % (w.name, w.phone)
    else:
        return "No health worker currently available. Please try again later."

def worker_infected(w: HCWorker) -> str:
    p = Patient.create(name=w.name, phone=w.phone, location=w.location, status="infected")
    w.delete_instance()
    return "You are registered as a patient. " + _notify_closest_worker(p)

def patient_infected(p: Patient) -> str:
    p.status = 'infected'
    p.save()
    return "Your status has been updated. Please quarantine yourself." + _notify_closest_worker(p)

def update_case(w: HCWorker, case_id: int, status: str):
    log("update(%s, %s, %s)" % (w, case_id, status))
    statuses = ", ".join(Patient.status_enum)
    if Patient.exists(Patient.id == case_id) and status in Patient.status_enum:
        patient = Patient.get(Patient.id == case_id)
        patient.status = status
        patient.save()
        return "Status %s for %s accepted" % (status, patient.name)
    else:
        return "Status not recognized. Options are: %s" ++ statuses

def new_case(w: HCWorker, patient_phone: str):
    log("new phone %s received" % (patient_phone))
#w: HCWorker, patient_name: str, patient_loc:str, patient_phone: str, patient_status: str
    # if Patient.exists(Patient.phone == patient_phone):
    #     return "patient already exists"
    # else:
    #     return "new patient phone recieved"
        # if Chiefdom.exists(Chiefdom.name == patient_loc):
        #     cd=chiefdom.get(Chiefdom.name == patient_loc)
        #     p = Patient.create(name=patient_name, phone=patient_phone, status=patient_status)
        #     p.location=cd
        #     return ("created patient %s in %s phone %s" % (patient_name, patient_loc, patient_phone))
        # else:
        #     return "chiefdom entered does not exist"

#
# def contacts(patient: Patient, c: str) -> str:
#     Patient.create(sender=patient, sent_on="some date", description=c)
#     return "patient %s contacts %s" % (patient, c)

def todo_for_worker(w: HCWorker) -> str:
    suspect = Patient.select().where((Patient.status == 'suspect') &
                                     (Patient.location == w.location))
    infected = Patient.select().where((Patient.status == 'infected') &
                                      (Patient.location == w.location))
    exposed = Patient.select().where((Patient.status == 'exposed') &
                                  (Patient.location == w.location))
    msg1 = "INFECTED: %s" % ', '.join(["%s %s %s phone: %s  " % (p.id, p.location, p.name, p.phone) for p in infected])
    msg2 = "SUSPECT: %s" % ', '.join(["%s %s %s phone: %s  " % (p.id, p.location, p.name, p.phone) for p in suspect])
    msg3 = "EXPOSED: %s" % ', '.join(["%s %s %s phone: %s  " % (p.id, p.location,p.name, p.phone) for p in exposed])
    return msg1 + "\n " + msg2 + "\n" + msg3

def exposed(w: HCWorker, origin_id: int, contact_phone: str):
    if Patient.exists(Patient.id == origin_id) \
            and not Patient.exists(Patient.phone == contact_phone):
        origin = Patient.get(Patient.id == origin_id)
        contact = Patient.create(phone=contact_phone,
                                 location=origin.location,
                                 status='exposed',
                                 exposed_to=origin)
        return "origin found, contact %s added" %(contact)
    else:
        return "origin not found, or contact already linked to an origin"

def hc_help(*a, **k):
    return ',\n'.join([patt for patt, func in Messages[HCWorker]])
def patient_help(*a, **k):
    return ',\n'.join([patt for patt, func in Messages[Patient]])

Messages = {
    HCWorker: [("loc {loc}", location),  # ==> res.named == {'loc' : 'austin'}
               ("todo", todo_for_worker),
               ("update {case_id:d} {status}", update_case),
               ("test {patient_phone} ", new_case),
     #          ("new {patient_name} loc {patient_loc} phone {patient_phone} status {patient_status}", new_case),
               ("i'm sick", worker_infected),
               ("patient {origin_id:d} contacted {contact_phone}", exposed),
               ("#help", hc_help)],
    Patient:  [("#info", INFO),
               ("loc {loc}", location),
#               ("contacted {c}", contacts),  # ==> res.named == {'c' : 'samuel'}
               ("i'm sick", patient_infected),
               ("#help", patient_help)]
}

def response_to_sms_body(msg: str, p: Union[Patient, HCWorker]) -> str:
    log("response_to_sms_body (%s, %s)" %(msg, p))
    for pattern, func in Messages[type(p)]:
        res = parse.parse(pattern, msg)
        if res is not None:
            if isinstance(func, str):
                return func
            else:
                return func(p, **res.named) # {'a': 'b'} ==> (a=b)
    return "Message not recognized. Text '#help' for options."
