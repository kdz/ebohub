#Program Description#

Description of the program, including:

  - What does it do?
  - What problem were you trying to solve?
  - How does your solution address the problem?
  - Instructions on how to run the program and tests
  
### EboHub ###

EboHub is an online web-based application to assist health-care workers, patients, and administrators coordinate disease surveillance and management on the frontlines of the battle against Ebola.

### The Problem and Constraints ###

The [Ebola outbreak](http://www.bbc.com/news/world-africa-28755033) that started in 2014 is the deadliest outbreak in the history of the disease. The disease spread like wildfire, and the region had none of the infrastructure required to tackle it rapidly and effectively. Tens of thousands 

Major problems included:

  - Health care workers personally identified remote infections, suspects, and exposures
  - Patients could only be safely handled at suitably equipped Ebola response centers
  - There were few ways to dissiminate information or to reach out to local communities
  - There was no central coordinated surveillance system that connected to the public and workers
  - Healthcare workers were recording patient, disease, and test data on paper
  - Mobile telecomm infrastructure was for feature phones (SMS-based) without web access

### The Solution ###

I developed EboHub as a cloud-based service with a centralized disease database containing surveillance, case and contact-tracing data. It used 2-way SMS interactions with health-care workers and the public (with call-in and browser-based interfaces as well), to provide real-time access to case status, to-do lists for workers, contact-tracing, symptom and care instructions as well as allowing SMS-driven updates to that disease database. 

EboHub uses Twilio as a gateway for SMS-Http and Voice-Http bridge services, Python as the implementation language, Flask as the web-server framework, PostGresql as a database, and Heroku as a scalable deployment platform.

![image](https://cloud.githubusercontent.com/assets/4351330/11172302/c1d32ae4-8bca-11e5-82be-e8d1f62ebe8b.png)

EboHub is unique in its holistic scope focusing on both health workers and locals, and in using SMS as a primary communication channel. EboHub directly addresses key objectives in USAID's original BAA for Fighting Ebola. It strengthens healthcare capacities by providing healthcare workers tools to improve quality and timeliness of patient care thereby preventing the virus from spreading. 


