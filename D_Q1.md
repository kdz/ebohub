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

One crucial piece in the fight on Ebola is access to real-time information for health-care workers, health-care administrators, patients, and the public. Many mobile-phone based solutions come up short because vast areas in the region lack access to smart-phones and mobile internet access. EboHub will have a significant positive operational impact on current Ebola surveillance, prevention,  and treatment efforts. 

By building first and foremost atop a foundation of 2-way SMS communication, with voice and IVR as a backup and a web-browser interface, it provides vital outbreak, individual case, contact-tracing, and public-awareness and education services to those on the frontline in this fight. 

By continuously building up a shared cloud database, and providing systematic access to workers and the public to key parts of this data, both upon request and via “push”, EboHub will remove one important barrier to better managing the outbreak. Entire populations in the affected communities will benefit. Having clear, current, and consistent information available to both communities and health workers will reduce errors, miscommunications, rumors, and mistrust while increasing effective resource mobilization.

