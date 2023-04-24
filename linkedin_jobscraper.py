
import pandas as pd
import logging
from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData, EventMetrics
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, TypeFilters, ExperienceLevelFilters, OnSiteOrRemoteFilters

# Change root logger level (default is WARN)
logging.basicConfig(level=logging.INFO)

scraper = LinkedinScraper(
    chrome_executable_path=r"C:\Users\marty\OneDrive - The George Washington University\Documents\CSCI 4443\Project\chromedriver_win32\chromedriver.exe",  # Custom Chrome executable path (e.g. /foo/bar/bin/chromedriver) 
    chrome_options=None,  # Custom Chrome options here
    headless=True,  # Overrides headless mode only if chrome_options is None
    max_workers=1,  # How many threads will be spawned to run queries concurrently (one Chrome driver for each thread)
    slow_mo=2,  # Slow down the scraper to avoid 'Too many requests 429' errors (in seconds)
    page_load_timeout=40  # Page load timeout (in seconds)    
)

queries = [
    Query(
        query='Data Analyst',
        options=QueryOptions(
            locations=[],
            apply_link=False,  # Try to extract apply link (easy applies are skipped). If set to True, scraping is slower because an additional page mus be navigated. Default to False.
            skip_promoted_jobs=True,  # Skip promoted jobs. Default to False.
            limit=100,
            filters=QueryFilters(
                # company_jobs_url='https://www.linkedin.com/jobs/search/?f_C=1441%2C17876832%2C791962%2C2374003%2C18950635%2C16140%2C10440912&geoId=92000000',  # Filter by companies.                
                relevance=RelevanceFilters.RECENT,
                time=TimeFilters.MONTH,
                type=[TypeFilters.FULL_TIME, TypeFilters.INTERNSHIP],
                #on_site_or_remote=[OnSiteOrRemoteFilters.REMOTE],
                experience=[ExperienceLevelFilters.MID_SENIOR]
            )
        )
    ),
]

states = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware",
          "D.C","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky",
          "Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri",
          "Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina",
          "North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota",
          "Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"
]

def scrape_jobs(job_title):
    
    job_title = job_title.lower().strip()
    filename = job_title.replace(" ", "_")

    for i in range(len(states)):
        queries = [
            Query(
                query=job_title,
                options=QueryOptions(
                    locations=[states[i]],
                    apply_link=False,  # Try to extract apply link (easy applies are skipped). If set to True, scraping is slower because an additional page mus be navigated. Default to False.
                    skip_promoted_jobs=True,  # Skip promoted jobs. Default to False.
                    limit=50,
                    filters=QueryFilters(
                        relevance=RelevanceFilters.RECENT,
                        time=TimeFilters.MONTH,
                        type=[TypeFilters.FULL_TIME, TypeFilters.INTERNSHIP, TypeFilters.PART_TIME],
                        experience=[ExperienceLevelFilters.INTERNSHIP, ExperienceLevelFilters.MID_SENIOR]
                    )
                )
            ),
        ]

        job_postings = []
        scraper.run(queries)
        df = pd.DataFrame(job_postings, columns=['Job_ID','Location','Title', 'Company','Date', 'Link', 'Description'])
        df.to_csv("{}.csv".format(filename), index=False, mode="a", header=False)