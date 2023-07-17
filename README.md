# Real Estate ETL Project with AWS EC2, RDS PostgreSQL, Apache Airflow

![image](https://github.com/phong002/webscrape-project/assets/47654096/5b971b67-7c4e-4f70-8c33-4d22de261d44)

## Description 
- The purpose of this project was to develop an automated, scalable extract, transform and load (ETL) pipeline to facilitate the end-to-end flow of data from its source into a database, allowing up-to-date data to be queried for data analysis and visualisation.

- Tools used: AWS EC2, AWS RDS PostgreSQL, Apache Airflow, Python, Tableau


## Methodology

- **Project Setup**: The first step involved setting up an AWS EC2 instance to host the entire ETL project. The EC2 instance provides a scalable and flexible computing environment for running the webscraping and data processing tasks.

- **Web Scraping**: Using Python and its webscraping libraries (BeautifulSoup), rental listing data was extracted from rent.com.au. The web scraping process involved fetching web pages, parsing HTML content, and extracting relevant data, such as property locations, number of rooms, and prices.
  
- **Data Transformation**: After web scraping, the raw data was transformed in Python to convert it into a structured and usable format. Data transformation tasks included handling missing values, standardising data types and performing any necessary data manipulations to ensure consistency and accuracy.
  
- **Database Setup**: An AWS RDS PostgreSQL database was created to serve as the repository for the webscraped real estate data. As an AWS-managed service, the RDS PostgreSQL database provides a reliable and scalable solution for storing structured data and enables efficient querying and analysis.

- **Data Loading**: The transformed data was loaded into the PostgreSQL database. This process involved connecting to the database from Python and inserting the cleaned and structured data into the appropriate table.

- **Automation with Apache Airflow**: The entire ETL pipeline was automated using Apache Airflow. Airflow allows for the definition of tasks and dependencies, enabling the scheduling and execution of the web scraping, data transformation, and data loading tasks at specified intervals. The scheduling ensured that the ETL pipeline ran automatically, fetching new data from rent.com.au and updating the PostgreSQL database with the latest information.  

 
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
- Define a Directed Acyclic Graph (DAG) which contains the collection of tasks to be run
- Configure DAG scheduling options (e.g. to execute every 24 hours) 
