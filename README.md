# Real Estate ETL Project with AWS EC2, AWS RDS PostgreSQL, Apache Airflow

![ETL-Flowchart](https://github.com/phong002/real-estate-etl/assets/47654096/6dbd3ab4-cd32-4a4b-9f2e-ddac311190a0)

## Description 
- The purpose of this project was to develop an automated, scalable extract, transform and load (ETL) pipeline to facilitate the end-to-end flow of data from its source into a database, allowing up-to-date data to be queried for data analysis and visualisation.

- Tools used: AWS EC2, AWS RDS PostgreSQL, Apache Airflow, Python, Tableau

- [Snapshot of Tableau dashboard](https://public.tableau.com/views/real-estate_16899622401130/Dashboard1?:language=en-GB&publish=yes&:display_count=n&:origin=viz_share_link)


## Methodology

1) **Project Setup**: The first step involved setting up an AWS EC2 instance to host the entire ETL project. The EC2 instance provides a scalable and flexible computing environment for running the webscraping and data processing tasks.

2) **Web Scraping**: Using Python and its webscraping libraries (BeautifulSoup), rental listing data was extracted from rent.com.au. The web scraping process involved fetching web pages, parsing HTML content, and extracting relevant data, such as property locations, number of rooms, and prices.
  
3) **Data Transformation**: After web scraping, the raw data was transformed in Python to convert it into a structured and usable format. Data transformation tasks included handling missing values, standardising data types and performing any necessary data manipulations to ensure consistency and accuracy.
  
4) **Database Setup**: An AWS RDS PostgreSQL database was created to store the webscraped real estate data. As an AWS-managed service, the RDS PostgreSQL database provides a reliable and scalable solution for storing structured data and enables efficient querying and analysis.

5) **Data Loading**: The transformed data was loaded into the PostgreSQL database. This process involved connecting to the database from Python and inserting the cleaned and structured data into the appropriate table.

6) **Data Visualisation**: A connection with the RDS PostgreSQL database was setup in Tableau to create visualisations. 

7) **Automation with Apache Airflow**: The entire ETL pipeline was automated using Apache Airflow. Airflow allows for the definition of tasks and dependencies, enabling the scheduling and execution of the web scraping, data transformation, and data loading tasks at specified intervals. The scheduling ensured that the ETL pipeline ran automatically, fetching new data from rent.com.au and updating the PostgreSQL database with the latest information.


## At a glance
### Connecting to EC2 instance via SSH and activating virtual environment
```zsh
etl_project % ssh -i "real-estate-key-pair.pem" ubuntu@ec2-3-26-47-6.ap-southeast-2.compute.amazonaws.com
```
![255392484-fb1e3389-c280-4054-a798-8561fb36e49f](https://github.com/phong002/real-estate-etl/assets/47654096/09f5092f-502d-4277-b136-f604d685f03b)

### Starting Airflow webserver/scheduler
![255392961-a1fd5321-9002-4dec-8c60-6f120ef10ce9](https://github.com/phong002/real-estate-etl/assets/47654096/3ffced5f-f0bf-4a61-9c1b-91dcd240d520)

### Airflow DAG consisting of 3 tasks
![254183208-86fbf2bd-6c14-4849-a39e-e9adbb260e5d](https://github.com/phong002/real-estate-etl/assets/47654096/860e6fef-b1d9-4938-8216-fad98ca4abf7)

### All tasks when successfully executed
![254185671-87e585f0-a431-4ada-8b31-cc1e6d85b3d6](https://github.com/phong002/real-estate-etl/assets/47654096/d491e360-c82b-46ab-8674-d2775d5eceeb)

### Connecting to postgres in Tableau
![255391861-f9bb0088-6a8f-4ac2-9f7e-a32bf41a057e](https://github.com/phong002/real-estate-etl/assets/47654096/c3370f1f-fd96-4a51-adc5-20792280b265)

### Listings table
![255391640-98ae3c92-bbe0-4bb0-8cf0-b7813c01c27c](https://github.com/phong002/real-estate-etl/assets/47654096/559567a6-a5d0-4918-8d24-7c1ff1d0dc66)

### Dashboard
![image](https://github.com/phong002/real-estate-etl/assets/47654096/5843de6b-3aca-4d7f-8a8f-077e52ff4202)



 
## Things I learned to do
### AWS 
- Configure IAM permissions for IAM users
- Create EC2 and RDS instances
- Configure security group settings (e.g. to only allow connections from the EC2 instance into Postgres) 
- SSH into an EC2 instance
- Transfer files into an EC2 instance using Secure Copy (SCP)
### Python
- Webscrape data using BeautifulSoup
- Transform data stored within Python data structures
- Connect to and perform database operations (insertion, updating, querying) with an RDS PostgreSQL database using psycopg2 
### Apache Airflow
- Install Airflow and its dependencies into the AWS EC2 instance 
- Define tasks using Airflow operators (e.g. PythonOperator) and setting up task dependencies
- Pass data between tasks using XCom (cross-communication) 
- Define a Directed Acyclic Graph (DAG) which contains the collection of tasks to be run
- Configure DAG scheduling options (e.g. to execute every 24 hours)
- Configure systemd unit files to enable airflow webserver/scheduler to run continuously in the EC2 instance (ie. start at boot, restart in case of failures)
### Misc
- Operate within Linux environment 

## Limitations 
- Since the tasks are relatively infrequent, services such as AWS Glue may be more cost-effective since they are pay-per-use, as opposed to EC2 which has fixed costs regardless of usage. 
  
- The process of extracting data by means of webscraping is not viable in the long term. Apart from ethical considerations, websites can change their HTML structure over time, which would cause the webscraper to fail since it relies on specific element identifiers. The use of supported APIs would be more reliable and secure as a long-term solution. 

- Tableau's live dashboard can only be viewed by authenticated users, while Tableau Public dashboards cannot establish live database connections. Therefore, only a snapshot of the dashboard is provided. 



















