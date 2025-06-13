from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import yagmail
import os

search_keywords = ["solar", "wind", "technician", "energy", "power",
                   "renewable energy", "clean", "cooking", "biogas",
                   "biofuel", "maintenance", "geothermal", "environment"]

job_location = "Kenya"

def scrape_fuzu():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    url = ("https://www.fuzu.com/jobs?q=" +
           "+".join(search_keywords) +
           "&location=" + job_location)
    driver.get(url)
    jobs = []
    for a in driver.find_elements(By.CSS_SELECTOR, "a[href*='/job/']"):
        jobs.append(f"{a.text}\n{a.get_attribute('href')}")
    driver.quit()
    return list(dict.fromkeys(jobs))

def send_email(jobs):
    if jobs:
        yag = yagmail.SMTP(os.getenv("EMAIL_ADDRESS"),
                           os.getenv("EMAIL_PASSWORD"))
        yag.send(os.getenv("EMAIL_ADDRESS"),
                 "Fuzu Daily Jobs",
                 "\n\n".join(jobs))

if __name__ == "__main__":
    jobs = scrape_fuzu()
    send_email(jobs)
