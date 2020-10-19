#! /usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import re
import csv

CONFERENCE_HOMEPAGE = "https://www.apnic.net/events/conferences/"

def attendees_url(id):
    return ["https://conference.apnic.net/{}/register/attendees/attendees_table.html".format(id), "https://conference.apnic.net/{}/scripts/attendees.htm".format(id),
    "https://conference.apnic.net/{}/attendees.html".format(id), "https://conference.apnic.net/{}/{}/attendees.html".format(id,id), "https://conference.apnic.net/{}/{}/register/attendees.html".format(id,id)]   

def get_conference_list():
    r = requests.get(CONFERENCE_HOMEPAGE)

    bs = BeautifulSoup(r.text, "lxml")
    conferences = bs.findAll("div", {"class": "apnic-conference"})

    conf_results = {}
    for conf in conferences:
        name    = conf.contents[0].text.strip()
        details = conf.contents[1].text.strip()
        conf_id = re.search(r'\d+', name).group()

        conf_results[conf_id] = {
            "name":    name,
            "details": details,
            "id":      conf_id
        }
    return conf_results

def get_conference_attendees(html):
    bs = BeautifulSoup(html, "lxml")
    table = bs.find('table')

    if table == None:
        print("Cannot read table\n")
        return []

    headers = [header.text for header in table.find_all('th')]
    results = [{headers[i]: cell.text for i, cell in enumerate(row.find_all('td'))}
                for row in table.find_all('tr')]

    return results

def write_to_csv(results, id):

    # opens file for writing
    data_file = open('../data_csv_scraper/APNIC_{}_attendees.csv'.format(id), 'w') 

    # create the csv writer object 
    csv_writer = csv.writer(data_file)

    # remove first element because it is empty
    results.pop(0) 

    for attendee in results: 

        conference = {'Conference': id}

        attendee.update(conference)
        # Writing data of CSV file 
        csv_writer.writerow(attendee.values()) 

    data_file.close()
    

conferences = get_conference_list()
conference_ids = conferences.keys()

attendees_by_conference = {}

print("Found {} conferences...".format(len(conference_ids)))

for conf_id in conference_ids:
    print("Fetching attendees for conference '{}'".format(conferences[conf_id]["name"]))

    if (int(conf_id) < 27):
        print("Attendee list not available anymore for conference '{}'\n".format(conferences[conf_id]["name"]))
        continue

    possible_urls = attendees_url(conf_id)

    for url in possible_urls:

        r = requests.get(url)

        if (r.status_code == 200):
            break

    if (r.status_code != 200):
        print("No attendees page found\n")
        continue

    results = get_conference_attendees(r.text)
    attendees_by_conference[conf_id] = results

    if(len(results) > 0):
        write_to_csv(results, conf_id)

    #print all of the attendees for this row
    # for row in results:
    #     print(row)

    print("Conference has {} attendees\n".format(len(results)))

print("Fetched attendees for {} conferences.".format(len(attendees_by_conference.keys())))