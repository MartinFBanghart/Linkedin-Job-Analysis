# Linkedin-Job-Analysis

This project was created to determine insights for job postings made on Linkedin.com. Specifically, this project aimed to build an ETL pipeline to build out a database of job tech job postings in an effort to understand the most desired and requested programming languages, database platforms, and cloud/distributed computing platforms sought by employers.

This was accomplished by using NLP methods on the job descriptions found for 3 job roles (Data Analyst, Software Engineer, Software Programmer). 

Data is first scraped via linkedin_scraper.py and then cleaned and transformed by text_processor.py.

Subsequently, the prepared datasets are then mounted within the DBFS (DataBricks File System) of a DataBricks Workspace to be queried and analyzed using Apache Spark (via PySpark API).


## How to Recreate

### Properly Saving Files and Setting up Folder Directory
To recreate the analysis. You will have to download linkedin_jobscraper.py, text_processor.py, and Extract_Transform.ipynb files into the same folder directory on your local machine. Then, all dependencies must be installed within your python environment. Any empty folder titled 'data' should also be initializied within the same folder directory - this is where all cleaned datasets will be stored after the text_processor functions are applied.

### Scraping and Cleaning the Data
The Extract_Transform.ipynb notebook can now be run. It is setup for 3 queries already - Data Analyst, Software Engineer, Software Programmer. These can be changed to other tech roles if you believe those positions may require similar software proficiencies. 

Intially, the raw datasets will be saved within the same directory as the Extract_transform.ipynb file and python files as '<query>.csv'. Once the text_processor has been applied as mentioned, these new files will be saved in the /data folder within the overall directory with names in the form of 'clean_<query>.csv'

### Analyzing in DataBricks
Now, after intializing a DataBricks Workspace, you must open the cmd prompt of your machine to mount the data to DataBricks via the DataBricks CLI (this was done on windows but similar configurations can be searched for other os)
 
These commands will then need to be run in the cmd prompt
- databricks configure --token
  
- databricks fs cp "(YOUR-FILE-PATH)\data" dbfs:/mnt/data --recursive
  
change (YOUR-FILE-PATH) to match the path leading to wherever you have the files saved in the 'data' folder
 
Then, in the DataBricks Notebook, you can read the file using this command (insert file name for <file.csv>)

df = spark.read.csv("dbfs:/mnt/local/<file.csv>", header=True, inferSchema=True)
  
The, simply configure the user defined functions to create Pie Chart and Bigram Box Chart visualizations if your queries varied from the 3 previously defined roles for this project.
 
### Potential Automation

This Pipeline currently requires manual configuration to save each batch. However, the idea would be setup simple batch streaming with automation.

This could be achieved on a weekly basis by using a third party task scheduler (such as *Task Till Dawn*) to automate the Extract_Transform.ipynb file
 
The datasets could then be uploaded to an AWS S3 bucket that is mounted within the DataBricks Workspace to be utilized. The files could be seamlessly integrated. (this step may also be simplified further by utilizing a DBFS mount refresh command but some difficulty was encountered when trying to implement this)
 
All that would be left to do is write code for reading the files from the S3 bucket within the DataBricks notebook and using the schedule option for the notebook.
