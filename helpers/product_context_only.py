message_VS = """Business Terminologies: 
 - Client: IDfy's clients using our products / solutions.
 - Customer: End customer of our clients.
 - OU / Organizational Unit: Same as client. Each one has a unique id within IDfy known as OUID.
 - POI: Proof of Identity (like pan card, etc.)
 - POA: Proof of Address (like aadhaar card, voter card, etc.)

Internal Terminologies:
 - Package: A configuration defined by the client & stored within IDfy to define end to end KYC journey. There can be multiple packages for a single OU.

"IDfy" offers "Video KYC" as a B2B solution to help clients like banks / NBFCs onboard their customers and perform KYC
process remotely and instantly. The customers need to fill up their details, give some ID proofs and get on a call with
an operator where the customer is verified.

To start the onboarding process, the client creates a "Profile" using REST API for each customer being onboarded. The
profile goes through various states during the onboarding process. The final state for a profile is "completed" when the
KYC is successful or "failed" when it was not. The backend service responsible for managing a profile is called
"Profile Manager".

The client receives a "Capture Link" for his customer during profile creation. The customer goes to the link to
complete his onboarding jouney. This part is handled by the service known as "Capture". Customer uses the link to input
his personal data (like name, father's name, address, etc.) and uploads his documents (POI, POA) to start his KYC
process. The fields & documents required are configurable via package. Customer then gets connected to an operator who
performs various document captures, ask questions to validate the identity & ask's the customer to perform various tasks
to prevent fraud over the video call. At the end of the video call the agent either approves the customer, rejects him
in case the customer was fraudulent or marks the "Call"/"Task" as unable to verify (UTV). In case of rejection, the
profile is rejected as well. In case of UTV, the customer needs to again got on a video call after some time using the
same link. UTV can be marked due to either business reasons (Like "ID card not available") or technical reasons (like
"customer on a bad network").

The video call leg is managed by the service known as "Video Service" which provides a video call centre like
functionality. For each video call, a "Task" gets created by "Profile Manger" which is then marked as either verified,
rejected or unable to verify. In case of UTV, "Profile Manager" creates another task for the same profile to let
customer perform another video call. 

"Operator Dashboard" is the frontend application used by the operator to connect to customers via video call & perform
various tasks during the video call like document capture, selfie capture, photo cropping, OCR on captured documents,
etc. The operator marks his readiness to accept a video call by "Toggling On" & "Toggles off" Whenever he is
unavailable.

"Media Server Controller" is an internal IDfy service that acts like a media server. Assisted Video backend uses it's
APIs and frontend library known as "MS Adaptor". MS Controller internally uses multiple media servers and provides
functionality like "Reconnect" to make the video call more reliable. It also provides a recording functionality. Each
Video composition service is responsible for stiching multiple videos (caused by reconnects) into one & returns the
recording to Assisted Video service.

After the video call is approved by the operator, all the artifics created by customer / operator are then reviewed
by a reviewer using "Reviewer Dashboard". This include the textual data, documents & video call. The reviewer can
mark the profile as "approved" which completes his KYC process, "rejected" to reject a fraudulant customer, "recapture"
to ask the customer to provide certain documents again in case of any issues. Recapture creates a new "Capture" & the
new link which needs to be sent to the customer

Each of these services emit various events during the profile's journey which are stored in a Data Warehouse
(Clickhouse). This data can be used to answer various kind of questions for analysis & product support.


1. PM / Profile Manager / PG / Profile Gateway / PH / Profile Hub: It 
2. AV / Assisted Video / Video Service / Video KYC: 
3. MSC / MS Controller / Media Server Controller: 
- MS Adaptor / Media Server Adaptor:
4. Tasky
5. Capture / Capture Journey:
6. OD / Operator Dashboard:
7. RD / Reviewer Dashboard:
"""
message_EVE = """Eve is our product which exposes APIs that helps in verifying user's uploaded documents using OCR. Lot of clients, identified uniquely by their OUID, use our APIs to verify uploaded documents on their platform by their users. We log the activities performed on our APIs by our clients in Clickhouse tables and then use that data to derive insights and analytics.   
"""
message_GCP = """
GCP stands for Google Cloud Platform. It's a suite of cloud computing services provided by Google, offering a range of services for computing, storage, data analytics, machine learning, and more, all hosted on Google's infrastructure. GCP allows businesses and developers to build, deploy, and scale applications and services efficiently in the cloud, leveraging Google's global network infrastructure and advanced technologies.
"""

message_RAI = """
Risk AI is a Software-As-A-Service product for which we are providing valuable insights. RiskAI's main purpose is to facilitate the loan approval or rejection process. It achieves this by considering various factors such as financial assessments, fraud detection mechanisms, director details verification, Anti-Money Laundering (AML) checks, and Early Warning System (EWS) triggers.

Every client of RiskAI is uniquely identified by their OUIDs. The insights/analytics that we derive should be filtered on basis of each client.
"""

message_DF = """
Data Fabric, also known as DF, is the Business Intelligence service provided to all the suites of products offered by the company. DF also provided its own Business Intelligence to itself wherein it records all the KPIs and other performance/business metrics of "Insights Service" which is the dashboard visualization portal for all the other products. 

While instrumenting itself, DF writes data into Clickhouse just like an other team. 
"""

message_DC = """
Double Check, also known as DC, is a software as a service product. We need to generate valuable insights about the performance and other KPIs of this product. DC’s main purpose is to conduct background verification checks also known as BGV on Individuals, companies and organisations. To achieve this, DC operates via multiple verticals. These verticals are Court Record, Employment check, Address Verification and Education verification.

Clients can upload the profiles on DC that are to be Background Verified via multiple channel. Some of these channels are API, Double Check client portal also knows as HR Portal, Bulk Upload via Email, Google Forms etc. 

Operators and verification professionals receives each of these tickets or tasks and conduct verification using multiple channels. IDfy operators use Ops Portal to keep track of these activities. These activities and their TAT are recorded in Clickhouse database via eventbus. 
For Address verification, they have separate module named addressify. They perform address verification via two ways, DAV that is digital address verification is used using PG API and Physical verification happens via different vendors, where vendors deploy runners in respective PIN code area to verify the address.

If the operator finds descripancy or finds some missing documents, he/she can raise an Insuff Flag against that ticket. 

Every client of DC is uniquely identified by their OUIDs. The insights/analytics that we derive should be filtered on basis of each client.
"""

message_CC = """
Crimecheck is a Software-As-A-Service product for which we are providing valuable insights. Crimecheck's main purpose is to provide information about any legal action, Court case, FIR etc against an individual or organization. To provide this information Crimecheck crawls multiple court records and police records and organizes the data in structured format. Final insights they show to their client on Crime Portal. TMS is ticket management service gets internally called for their services and Ticket ERP is used by the ops people as front end application. Crimecheck uses multiple Machine Learning APIs and Apps that are developed internally. Events from these Machine Learning Apps are stored in our Clickhouse tables. We need to derive insights from these tables.

Every client of Crimecheck is uniquely identified by their OUIDs. The insights/analytics that we derive should be filtered on basis of each client.
"""