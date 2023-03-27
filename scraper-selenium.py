import requests
import json
import time
from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

scraped_offers=2 # Initializing the number of scraped offers

class JobOffer:
    def __init__(self, title, street, country_code, address_text, marker_icon, 
                 workplace_type, company_name, company_url, company_size, 
                 experience_level, offer_id, employment_types, skills, remote, multilocation):
        # Initialize JobOffer attributes
        self.title = title
        self.street = street
        self.country_code = country_code
        self.address_text = address_text
        self.marker_icon = marker_icon
        self.workplace_type = workplace_type
        self.company_name = company_name
        self.company_url = company_url
        self.company_size = company_size
        self.experience_level = experience_level
        self.offer_id = offer_id
        self.employment_types = employment_types
        self.skills = skills
        self.remote = remote
        self.multilocation = multilocation
        self.description = None # Initialize description as None


class JobScraper:
    def __init__(self, scraped_offers: int):
        # Initialize JobScraper attributes
        self.scraped_offers = scraped_offers
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=self.options)

    def scrape_data(self) -> List[JobOffer]:
        # Retrieve job offers data from API endpoint and scrape job offer webpage for each offer
        url = "https://justjoin.it/api/offers"
        response = requests.get(url)
        raw_data = response.json()[:self.scraped_offers]

        job_offers = []
        for item in raw_data:
            job_offer = JobOffer(
                title=item["title"],
                street=item["street"],
                country_code=item["country_code"],
                address_text=item["address_text"],
                marker_icon=item["marker_icon"],
                workplace_type=item["workplace_type"],
                company_name=item["company_name"],
                company_url=item["company_url"],
                company_size=item["company_size"],
                experience_level=item["experience_level"],
                offer_id=item["id"],
                employment_types=item["employment_types"],
                skills=item["skills"],
                remote=item["remote"],
                multilocation=item["multilocation"]
            )
            self.driver.get("https://justjoin.it/offers/" + job_offer.offer_id)
            time.sleep(5)
            desc = self.driver.find_elements(by=By.CLASS_NAME, value='css-p1hlmi')
            if desc:
                job_offer.description = desc[0].text # Extract the description text and assign it to the job_offer object
            job_offers.append(job_offer)

        self.driver.quit() # Quit the driver to close the browser

        return job_offers


if __name__ == '__main__':
    scraper = JobScraper(scraped_offers) # Instantiate the JobScraper object
    job_offers = scraper.scrape_data() # Call the scrape_data() method to retrieve job offer data

    with open("data.json", "w") as f:
        json.dump([job_offer.__dict__ for job_offer in job_offers], f) # Write the job offer data to a JSON file
