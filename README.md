Webscrapper for justjoin.it
Program "scraper_a.py" extracts information from the website justjoin.it and save it to JSON file. Output this program is "document_db.json" which is located in \research\sourced_data

The program has a variable "scrapped_offers" that initializes the number of scrapped offers, because each single offer opens its own link in turn, which takes a certain amount of time.

*** ATTENTION ***
To run the program, you must have a chrome browser and webdriver which you can download from site:
https://chromedriver.chromium.org/downloads
After downloaded you have to add "chromedriver.exe" to project directory.
