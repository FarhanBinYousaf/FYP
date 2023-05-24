import requests
from bs4 import BeautifulSoup
from lxml import etree
import csv
# Main URL of CareerOkay.com
url_template = 'https://www.careerokay.com/jobs/index/page:{}'
current_page = 1
max_pages = 4

with open('JobsData.csv', mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['Title','Link','Company','Location','Date','Experience','Salary','Time','Apply Here','Category','Career Level','Qualification','vacancies'])
    writer.writeheader()
# 
    while current_page <= max_pages:
        url = url_template.format(current_page)
        print('Scraping URL of :', url)
        response = requests.get(url)
        soup = BeautifulSoup(response.content,'html.parser')
        divs = soup.find_all('div',class_='job-style1')
        # Link of website that will be combined to every job URL
        mylink = 'https://www.careerokay.com/'
        # Main divs for hiting HTML structure to crawl data
        for div in divs:
            # Main div of Job Content
            mydiv = div.find('div',class_='job-content')
            title = mydiv.find('h3').text.replace('\n',"")      # Job Title
            aTag = mydiv.find('h3').find('a')                   # Finding ancher(a) tag of every jobs to get URL
            link = aTag['href']                                 # Hyperlink of every job
            jobLink = mylink +  link                            # complete link of every job after combining with URL of every job 

            CompanyAndLocation = mydiv.find('p')                # Getting div of Company and Location
            company = CompanyAndLocation.find('a').text         # Company Name 
            location = CompanyAndLocation.find('span',class_='post-stats-line').text.replace('\n',"")       # Location Name (City Name)
            # Getting paragraph of Salar,Time,Date and Experience
            bar = mydiv.find('p',class_='post-stats-line')
            barr = bar.find_all('span',limit=4)         # Putting limit for getting span
            date = barr[0].text                     # Getting Date 
            experience = barr[1].text               # Getting Experience 
            salary = barr[2].text                   # Getting Salary
            time = barr[3].text                     # Getting Time
            # Getting Apply Button
            applybutton = div.find('div',class_='col-sm-2')
            btn = applybutton.find('a')             # Getting Apply Button's ancher tag
            applyLink = mylink +  btn['href']       # Apply Button Hyperlink

            # Using Requests for every jobs detail
            f = requests.get(jobLink)
            data = BeautifulSoup(f.content,'html.parser')
            nextdiv = data.find('div',class_='job-details-wrap')   # Getting div of Every Job Detail which is on next page
            col = nextdiv.find('div',class_='col-sm-9').find('div',class_='row')   # Getting Row under columns to get detail
            firstCol = col.find_all('div',class_='col-md-6')
            FirstColDetail = firstCol[0].find('dl',class_='dl-horizontal')
            dd = FirstColDetail.find_all('dd',limit=9)  # Putting limit to find elements by indexing 
            category = dd[0].text       # Category
            careerLevel = dd[1].text    # Career Level
            Qualification = dd[3].text  # Qualification
            vacancies = dd[7].text      # Vacancies

            # parsing data to CSV File 
            record = {'Title': title, 'Link': jobLink, 'Company':company, 'Location': location, 'Date': date, 'Experience': experience, 'Salary': salary, 'Time': time, 'Apply Here': applyLink,'Category':category,'Career Level': careerLevel, 'Qualification':Qualification,'vacancies':vacancies }
            writer.writerow(record)

        current_page += 1       # Increasing pages by one 
