import requests
from bs4 import BeautifulSoup
from db_connection import get_db_connection

def scrape_jobs():
    url = "https://www.naukri.com/"  # Change this URL to the job portal you're scraping from
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []
    for job_listing in soup.find_all("article"):  # Change the tag to match the job portal's structure
        title = job_listing.find("h2").text.strip() if job_listing.find("h2") else ""
        company = job_listing.find("a", class_="company").text.strip() if job_listing.find("a", class_="company") else ""
        skills = job_listing.find("ul", class_="skills").text.strip() if job_listing.find("ul", class_="skills") else ""
        location = job_listing.find("span", class_="location").text.strip() if job_listing.find("span", class_="location") else ""

        job_data = {
            "title": title,
            "company": company,
            "skills": skills,
            "location": location
        }

        jobs.append(job_data)

    # Connect to MongoDB and save scraped jobs
    db = get_db_connection()
    jobs_collection = db["jobs"]
    jobs_collection.insert_many(jobs)
    print("Job data scraped and saved to MongoDB!")

# Run the scraper
if __name__ == "__main__":
    scrape_jobs()
