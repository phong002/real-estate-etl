from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import psycopg2
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 7, 10),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'real_estate_etl_dag',
    default_args=default_args,
    schedule_interval=timedelta(days=1),  # Executes every 24 hours
    catchup=False
)

def scrape_listings(ti):
    all_listing_info = []
    page_number = 1
    while True:
        url = f'https://www.rent.com.au/properties/brisbane-qld-4000/p{page_number}'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # retrieve all listings in given page
        all_listings = soup.find_all('div', class_='overview')

        # if final page exceeded
        if bool(all_listings) is False:
            print("Last page exceeded.")
            break

        # extract key information from each listing preview
        for listing in all_listings:

            # address, price, property type
            property_address = listing.find('h2', class_='address').text.strip()
            property_price = listing.find('span', class_='price').text.strip().split("\n")[0]

            # property type - default to NA for listings without a type 
            property_type_element = listing.find('span', class_='property-type')
            property_type = property_type_element.text.strip() if property_type_element is not None else "NA"

            # beds, baths, parking spaces
            features = listing.find_all('li', class_='feature')
            bed_count, bath_count, parking_count = (feature.find('span', class_='value').text.strip().split(" ")[0] for feature in features[:3])

            all_listing_info.append({
                'address': property_address,
                'price_per_week': property_price,
                'beds':  bed_count,
                'baths': bath_count,
                'parking_spaces': parking_count,
                'property_type': property_type
            })

        page_number += 1

    ti.xcom_push(key='all_listing_info', value=all_listing_info)
    
def clean_data(ti):
    # convert list to df 
    all_listing_info = ti.xcom_pull(key='all_listing_info', task_ids='extract_task')
    df = pd.DataFrame(all_listing_info)

    # modify price column to only keep numeric values
    df = df[df['price_per_week'].str.contains('\$') & df['price_per_week'].str.contains('\d')]
    df.loc[:, 'price_per_week'] = df.loc[:, 'price_per_week'].str.replace(',', '').str.extract(r'\$\s?([\d,]+)').astype(int)

    # add postal code column
    df = df.assign(postal_code = df.loc[:, 'address'].str[-4:].to_list()) 

    # convert back to list before pushing
    all_listing_info = df.to_dict('records')
    ti.xcom_push(key='all_listing_info', value=all_listing_info)

def load_to_rds(ti):
    # Connection parameters
    host = "real-estate-db.czvpezojzuuw.ap-southeast-2.rds.amazonaws.com"
    port = 5432
    dbname = ""
    user = "postgres"
    password = os.getenv('REAL_ESTATE_DB_PASSWORD')

    # establish connection to postgres db
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        print("Connection to the database successful!")

    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
    
    # create cursor object to interact with the db
    cursor = conn.cursor()

    # create listings table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS listings (
        id SERIAL PRIMARY KEY,
        address TEXT,
        price_per_week INT,
        beds INT,
        baths INT,
        parking_spaces INT,
        property_type TEXT,
        postal_code TEXT
    );
    """

    cursor.execute(create_table_query)
    print("Table created successfully!")

    # prepare data as a list of tuples for postgres DB insertion 
    all_listing_info = ti.xcom_pull(key='all_listing_info', task_ids='transform_task')
    data = [(row['address'], row['price_per_week'], row['beds'], row['baths'], row['parking_spaces'], 
             row['property_type'], row['postal_code']) for row in all_listing_info]

    # insert data into the table
    insert_query = """
    INSERT INTO listings (address, price_per_week, beds, baths, parking_spaces, property_type, postal_code)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    cursor.executemany(insert_query, data)
    conn.commit()
    print("Data inserted successfully!")


extract_task = PythonOperator(
    task_id='extract_task',
    python_callable=scrape_listings,
    dag=dag
)

transform_task = PythonOperator(
    task_id='transform_task',
    python_callable=clean_data,
    dag=dag
)

load_task = PythonOperator(
    task_id='load_task',
    python_callable=load_to_rds,
    dag=dag
)


extract_task >> transform_task >> load_task 
