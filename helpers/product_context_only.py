message_VS = """Video KYC Journey Overview:
1. Video KYC (Know Your Customer) is conducted for user verification.
Each client is identified by a unique OUID (Organization Unique Identifier).
Operators/agents conduct the KYC process for end customers.
Activities of operators, end customers, and reviewers are logged for analysis.

2.Key Steps in the Video KYC Journey:
Profile Creation: When a new customer begins the KYC journey, a ProfileID is generated internally. Each client/OUID has a unique ExtReferenceID linked to their ProfileID.
Capture Window: Customers log in and perform activities. A CaptureSessionID is created for each session, associated with the ProfileID.
Queue Assignment: Assisted Video sessions are assigned to specific queues based on language and skill preferences. QueueID or QueueName is recorded in the data.
Assisted Video (AV): Customers move to assisted video sessions with a designated agent. Each session has a unique AVSessionID. Agents create tasks for profile details, associated with ProfileID and AVSessionID.
Profile Verification: Agents verify profiles or mark them as UTV (Unable To Verify) based on profile status. Reviewed profiles proceed to the reviewer.
Review Process: Reviewers verify documents and complete tasks. They can also reject profiles with reasons provided.

3.Data Logging and Analysis:
All activities, including operator, customer, and reviewer actions, are logged in ClickHouse tables.
Key data includes ProfileID, ExtReferenceID, CaptureSessionID, AVSessionID, AgentID, TaskID, QueueID/QueueName, ProfileStatus, and Reason.
TTL (Time To Live) fields are set for data retention in ClickHouse tables.
In summary, the Video KYC process involves multiple steps, including queue assignment during assisted video sessions. Data from these activities is logged for analysis, facilitating insights into operator performance, customer behavior, and verification outcomes.
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
