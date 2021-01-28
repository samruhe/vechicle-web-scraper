# pip install bs4

from requests import get
from bs4 import BeautifulSoup
from random import randint
from time import sleep
import csv
import numpy as np

print("Enter the base of the url for the location you would like to search.")
location_url = input("  'xxxxxx.craigslist.org' \n")
car_location = location_url.split(".")[0]

try:
    # get the first page of the reno cars and trucks listings
    response = get('https://' + location_url + '/search/cta?hasPic=1&availabilityMode=0&auto_drivetrain=3')
except Exception:
    print("There was an error with the provided url, please try agian.")
    exit()

html_soup = BeautifulSoup(response.text, 'html.parser')

# get all of the listings
posts = html_soup.find_all('li', class_ = 'result-row')

# get first post
one_post = posts[0]
count = 1

# get price of post
post_price = one_post.a.text.strip()

#get the time of the post in datetime format to save on cleaning efforts
post_time = one_post.find('time', class_ = 'result-date')
post_datetime = post_time['datetime']

# get title of post
post_title_data = one_post.find('a', class_ ='result-title hdrlnk')
post_link = post_title_data['href']
post_title = post_title_data.text

# go into post to get tags
res = get(post_link)
soup = BeautifulSoup(res.text, 'html.parser')

fields = ['id', 'price','year', 'make_model', 'post_date', 'odometer', 'condition', 'cylinders', 'drive', 'fuel', 'color', 'size', 'title_status', 'transmission', 'type', 'location']
rows = []

attrs = soup.find_all('p', class_ = 'attrgroup')[1]
car_year = soup.find_all('p', class_ = 'attrgroup')[0].text[1:5]
tags = attrs.find_all('span')
this_row = [count, post_price, car_year, post_title, post_datetime, '', '', '', '', '', '', '', '', '', '', car_location]
count += 1
for tag in tags:
    attr_data = tag.text.split(": ")
    attr = attr_data[0]
    if attr == 'odometer':
        this_row[4] = attr_data[1]
    if attr == 'condition':
        this_row[5] = attr_data[1]
    if attr == 'cylinders':
        this_row[6] = attr_data[1].split(" ")[0]
    if attr == 'drive':
        this_row[7] = attr_data[1]
    if attr == 'fuel':
        this_row[8] = attr_data[1]
    if attr == 'paint color':
        this_row[9] = attr_data[1]
    if attr == 'size':
        this_row[10] = attr_data[1]
    if attr == 'title status':
        this_row[11] = attr_data[1]
    if attr == 'transmission':
        this_row[12] = attr_data[1]
    if attr == 'type':
        this_row[13] = attr_data[1]
    
rows.append(this_row)

# name of csv file  
filename = "scraped_listings.csv"
    
# create file and write headers if does not exist
# add current row either way
try:
    # writing to csv file  
    with open(filename, 'x') as csvfile:  
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
            
        # writing the fields
        csvwriter.writerow(fields)

        # writing the data rows
        csvwriter.writerows(rows)
except FileExistsError:
    with open(filename, 'a') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the data rows
        csvwriter.writerows(rows)

results_num = html_soup.find('div', class_= 'search-legend')
results_total = int(results_num.find('span', class_='totalcount').text)

pages = np.arange(0, results_total+1, 120)
for page in pages:
    response = get('https://' + location_url + '/search/cta?'
                        + 's='
                        + str(page)
                        + '&hasPic=1&availabilityMode=0'
                        + '&auto_drivetrain=3')

    sleep(randint(1,5))

    soup = BeautifulSoup(response.text, 'html.parser')

    posts = soup.find_all('li', class_ = 'result-row')

    for post in posts:
        post_price = post.a.text.strip()

        post_time = post.find('time', class_ = 'result-date')
        post_datetime = post_time['datetime']

        post_title_data = post.find('a', class_ ='result-title hdrlnk')
        post_link = post_title_data['href']
        post_title = post_title_data.text
        car_year = post_title[:4]
        if car_year.isnumeric() == False:
            car_year = ''

        res = get(post_link)
        soup = BeautifulSoup(res.text, 'html.parser')

        fields = ['id', 'price','year', 'make_model', 'post_date', 'odometer', 'condition', 'cylinders', 'drive', 'fuel', 'color', 'size', 'title_status', 'transmission', 'type', 'location']
        rows = []

        attrs = soup.find_all('p', class_ = 'attrgroup')[1]
        car_year = soup.find_all('p', class_ = 'attrgroup')[0].text[1:5]
        tags = attrs.find_all('span')
        this_row = [count, post_price, car_year, post_title, post_datetime, '', '', '', '', '', '', '', '', '', '', car_location]
        count += 1
        for tag in tags:
            attr_data = tag.text.split(": ")
            attr = attr_data[0]
            if attr == 'odometer':
                this_row[4] = attr_data[1]
            if attr == 'condition':
                this_row[5] = attr_data[1]
            if attr == 'cylinders':
                this_row[6] = attr_data[1].split(" ")[0]
            if attr == 'drive':
                this_row[7] = attr_data[1]
            if attr == 'fuel':
                this_row[8] = attr_data[1]
            if attr == 'paint color':
                this_row[9] = attr_data[1]
            if attr == 'size':
                this_row[10] = attr_data[1]
            if attr == 'title status':
                this_row[11] = attr_data[1]
            if attr == 'transmission':
                this_row[12] = attr_data[1]
            if attr == 'type':
                this_row[13] = attr_data[1]
            
        rows.append(this_row)

        with open(filename, 'a') as csvfile:
            # creating a csv writer object 
            csvwriter = csv.writer(csvfile)  

            # writing the data rows  
            csvwriter.writerows(rows)
        
        # sleep(randint(1,3))
        