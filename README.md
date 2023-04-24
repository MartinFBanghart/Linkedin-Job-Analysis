# Linkedin-Job-Analysis

This project was created to determine insights for job postings made on Linkedin.com. Specifically, this project aimed to build an ETL pipeline to build out a database of job tech job postings in an effort to understand the most desired and requested programming languages, database platforms, and cloud/distributed computing platforms sought by employers.

This was accomplished by using NLP methods on the job descriptions found for 3 job roles (Data Analyst, Software Engineer, Software Programmer). 

Data is first scraped via linkedin_scraper.py and then cleaned and transformed by text_processor.py.

Subsequently, the prepared datasets are then mounted within the DBFS (DataBricks File System) of a DataBricks Workspace to be queried and analyzed using Apache Spark.


## How to Recreate

To recreate the analysis. You will have to download linkedin_jobscraper.py, text_processor.py, and Extract_Transform.ipynb files into the same folder directory on your local machine. Then, all dependencies must be installed within your python environment. Any empty folder titled 'data' should also be initializied within the same folder directory - this is where all cleaned datasets will be stored after the text_processor functions are applied.

The Extract_Transform.ipynb notebook can now be run. It is setup for 3 queries already - Data Analyst, Software Engineer, Software Programmer. These can be changed to other tech roles if you believe those positions may require similar software proficiencies. 

Intially, the raw datasets will be saved within the same directory as the Extract_transform.ipynb file and python files as '<query>.csv'. Once the text_processor has been applied as mentioned, these new files will be saved in the /data folder within the overall directory with names in the form of 'clean_<query>.csv'
  
Now, after intializing a DataBricks Workspace, you must open the cmd prompt of your machine to mount the data to DataBricks via the DataBricks CLI (this was done on windows but similar configurations can be searched for other os)
 
These commands will then need to be run in the cmd prompt
- databricks configure --token
  
- databricks fs cp "<YOUR-FILE-PATH>\data" dbfs:/mnt/data --recursive
  
change <YOUR-FILE-PATH> to match the path leading to wherever you have the files saved in the 'data' folder
 
Then, in the DataBricks Notebook, you can read the file using this command (instert file name for <file.csv>)

df = spark.read.csv("dbfs:/mnt/local/<file.csv>", header=True, inferSchema=True)
