
### EboHub ###

EboHub is an cloud-based application to assist health-care workers, patients, and administrators coordinate disease surveillance and management on the frontlines of the battle against Ebola through SMS and web interfaces.

### The Problem and Constraints ###

The [Ebola outbreak](http://www.bbc.com/news/world-africa-28755033) that started in 2014 is the deadliest outbreak in the history of the disease. The disease spread like wildfire, and the region had none of the infrastructure required to tackle it rapidly and effectively. Well over 10,000 people have died.

Major problems with the epidemic included:

  - Health care workers have to personally identify remote infections, suspects, and exposures
  - Patients can only be safely handled at suitably equipped Ebola response centers
  - There are few ways to dissiminate information or to reach out to local communities
  - There was no central coordinated surveillance system that connected to the public and workers
  - Healthcare workers were recording patient, disease, and test data on paper
  - Mobile telecomm infrastructure was for feature phones (SMS-based) without web access

### The Solution ###

I developed EboHub as a cloud-based service with a centralized disease database containing surveillance, case and contact-tracing data. It uses 2-way SMS interactions with health-care workers and the public (with call-in and browser-based interfaces as well), to provide real-time access to case status, to-do lists for workers, contact-tracing, symptom and care instructions, outbreak maps, and allows authorized workers to do SMS-driven updates to the disease database. 

EboHub uses Twilio as a gateway for SMS-Http and Voice-Http bridge services, Python as the implementation language, Flask as the web-server framework, PostGresql as a database, and Heroku as a scalable deployment platform. I used ngrok during development to route public HTTP requests (originating from SMS or browser interactions) to my laptop.

![image](https://cloud.githubusercontent.com/assets/4351330/11172302/c1d32ae4-8bca-11e5-82be-e8d1f62ebe8b.png)

### EboHub Strengths ###

EboHub is deployed as a robust functioning prototype with case surveillance, worker, patient, and facility coordination, and community education, which allows:

  - 2-way SMS-based interaction with members of the public: `#help` (responds with menu of options), `#info` (provides disease, symptom, and care information), `loc` and `name` (updates the database with new patient info), and `i’m sick` (updates patient as a suspect in database).
  - 2-way SMS-based interaction with health-care workers: `#loc` (updates health-care worker’s location), `todo` (provides worker with assigned list of suspect, infected, and contact cases for worker’s location), `update` case (updates patient status for a given case), `contact` (updates contact-tracing information for an infected case), `i’m sick` (marks health-care worker as a suspect), and `#help` (provides menu of options). 
  - Outbreak map with suspects, infections, and exposures (people who may have been exposed and should be tracked).
  - Voice and IVR interaction for the public (currently just a placeholder message).
  - Initial SMS-blast capability to send SMS messages to a selected set of workers or the public.
  - Initial login and access controls for the web-based interface (disabled for demo purposes).

EboHub is unique in its holistic scope focusing on both health workers and locals, and in using SMS as a primary communication channel. EboHub directly addresses key objectives in USAID's original BAA for Fighting Ebola. It strengthens healthcare capacities by providing healthcare workers tools to improve quality and timeliness of patient care thereby preventing the virus from spreading.

One crucial piece in the fight on Ebola is access to real-time information for health-care workers, health-care administrators, patients, and the public. Many mobile-phone based solutions come up short because vast areas in the region lack access to smart-phones and mobile internet access. EboHub will have a significant positive operational impact on current Ebola surveillance, prevention,  and treatment efforts. 

By building first and foremost atop a foundation of 2-way SMS communication, with voice and IVR as a backup and a web-browser interface, it provides vital outbreak, individual case, contact-tracing, and public-awareness and education services to those on the frontline in this fight. 

By continuously building up a shared cloud database, and providing systematic access to workers and the public to key parts of this data, both upon request and via “push”, EboHub will remove one important barrier to better managing the outbreak. Entire populations in the affected communities will benefit. Having clear, current, and consistent information available to both communities and health workers will reduce errors, miscommunications, rumors, and mistrust while increasing effective resource mobilization.

### How To Use The Program ###

The easiest way is to use the [system as currently deployed](ebohub.herokuapp.com) on Heroku, since it is already configured with a PostGres database and with a Twilio account and phone number for the SMS-http gateway. 

Note that aaccess controls are currently disabled to make it easy for the public to run demos. The home page has a link to reset the database if necessary.

To use the currently deployed system:

  - Gather 2 or more cell phones. Let's call 2 of these phones `Patient` and `Nurse`.
  - Point your web browser at [EboHub.herokuapp.com](http://ebohub.herokuapp.com).
  - Note the primary contact number for all Ebohub SMS and Voice interactions. Let's call this `EboNumber`.
  - Browse the list of current patients, chiefdoms (regions), and health care workers.
  - `Patient` sends `#help` to `EboNumber` to see SMS options as a patient.
  - `Patient` sends `#info` and receives information to self-check symptoms etc.
  - `Patient` places a voice call to `EboNumber` and discusses his issues. Voice-reponse is just a placeholder for now.
  - `Patient` registers as a Patient by sending `i'm sick` to `EboNumber`.
  - `Patient` registers his name by sending `name <some-name>`.
  - `Nurse` registers as a health-care worker in `Yorkville` by:
    - Create an entry on the `H C Worker` page
    - Register the phone number in this exact form: `+1` followed by area-code and number, with no extra characters.
  - `Nurse` asks for her assigned tasks by sending `todo`. She receives assigned patient information in her current location.
  - `Patient` registers moves into `Yorkville` by sending `loc Yorkville`. `Nurse` is notified since she is in `Yorkville`.
  - `Nurse` visits `Patient` and sends `update` with patient-id and status.
  - `Nurse` gets infected and sends in `i'm sick`.
  - An administrator sorts the tables by different columns to get overviews.
  - The administrator visits the `Logs and Map` page to look at the current outbreak map.
  
### How to Install, Run, and Test the Program ###

A full local install to run the program or its executable tests involves these main steps (although it is easier to directly use the version I have deployed on Heroku instead).

1. Unzip the zip file of the entire program, or `git clone` from [github](https://github.com/kdz/ebohub)
2. Install Python 3.4 (recommended source: [anaconda](https://www.continuum.io/downloads)
3. Set up a Python virtual env using pyvenv in the app folder, and activate it.
4. Run `pip install -r requirements.txt` to install all the needed libraries.
5. Install a PostGresql database and start the db-server. Run `python db_init.py` from the src folder.
6. Setup a Twilio account, configure the Twilio phone number to route SMS and Voice requests to your running app. Consider using something like [ngrok](https://ngrok.com/) to connect the public URL to your running app.
8. Start the web server with: `python ebohub_app.py`.
7. Run `pytest tests/test_any.py` from within the app folder to run all the tests.
9. Start using the app through your browser and cell phones.
