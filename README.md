# Linkedin-Job-Analysis

This project was created to determine insights for job postings made on Linkedin.com. Specifically, this project aimed to build an ETL pipeline to build out a database of job tech job postings in an effort to understand the most desired and requested programming languages, database platforms, and cloud/distributed computing platforms sought by employers.

This was accomplished by using NLP on the job descriptions found for 3 job roles (Data Analyst, Software Engineer, Software Programmer). 

Data is first scraped via linkedin_scraper.py and then cleaned and transformed by text_processor.py.

Subsequently, the prepared datasets are then mounted within the DBFS (DataBricks File System) of a DataBricks Workspace to be queried and analyzed using Apache Spark.
