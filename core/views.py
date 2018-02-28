# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unicodecsv as csv
from django.shortcuts import render
from bs4 import BeautifulSoup
import urllib2


# Create your views here.

def get_data():
    soup = BeautifulSoup(
        urllib2.urlopen('http://www.agriculture.gov.au/pests-diseases-weeds/plant#travelling--or-mailing-to-australia'),
        "html.parser")
    data = soup.find_all("div", {"class": "body-wrapper"})[0].find("div", {"id": "page-wrapper"}).find("div", {
        "id": "main"}).find("div", {"id": "collapsefaq"}).find_all("ul", {"class": "flex-container"})[0]
    host_url = "http://www.agriculture.gov.au"

    dict_data = {}
    for count, link in enumerate(data):
        current_url = link.find("a")["href"]
        title = ""
        data_list = []
        if "pests-diseases-weeds" in current_url and "forestry-timber" not in current_url:
            current_url_soup = BeautifulSoup(urllib2.urlopen(host_url + current_url), "html.parser")
            current_url_data = \
                current_url_soup.find_all("div", {"class": "body-wrapper"})[0].find("div", {"id": "page-wrapper"}).find(
                    "div", {"id": "main"}).find("span", {"id": "DeltaPlaceHolderMain"}).find_all("div",
                                                                                                 {"page-content"})[0]
            title = current_url_data.find("h1").text
            pest_header = \
                current_url_data.find("div",
                                      {"id": "ctl00_PlaceHolderMain_ctl01__ControlWrapper_RichHtmlField"}).find_all(
                    "div", {"class": "pest-header-wrapper"})[0]
            image = pest_header.find_all("div", {"class": "pest-header-image"})[0].find("h3").find("img")["src"]
            pest_type = pest_header.find_all("div", {"class": "pest-header-image"})[0].find_all("div", {
                "class": "fact-sheet-label"})[0].find("p").text
            pest_content = pest_header.find_all("div", {"class": "pest-header-content"})[0].find_all("p")[1].text
            origin_content = ", ".join(pest_content.split("\n"))
            origin_data = origin_content[origin_content.find("Origin"):origin_content.find("Distribution")].replace(
                "Origin:", "")
            other_data = current_url_data.find("div", {
                "id": "ctl00_PlaceHolderMain_ctl01__ControlWrapper_RichHtmlField"}).find("div", {
                "id": "collapsefaq"}).find_all("div", {"class": "hide"})
            check_legal_content = other_data[1].find_all("p")
            secure_any_content = other_data[2].find_all("p")
            data_list = [host_url + image, pest_type, origin_data, ",".join([i.text for i in check_legal_content]),
                         ",".join([j.text for j in secure_any_content])]
        if "planthealthaustralia" in current_url:
            current_url_soup = BeautifulSoup(urllib2.urlopen(current_url), "html.parser")
            current_url_data = current_url_soup.find_all("div", {"class": "wrapper"})[0].find("div", {"class": "container"}).find_all("div", {"class": "main"})[0]
            title = current_url_data.find("h1").text
            image = ""
            try:
                image = current_url_data.find_all("div", {"class": "content"})[0].find("table").find("tbody").find("tr").find_all("td")[0].find("div").find("img")["src"]
            except AttributeError:
                pass
            data_list = [image, "", "", "", ""]
        dict_data.update({title.replace("\r\n", "").replace(" ", " "): data_list})
        print "Complete count no.: " + str(count)

    with open("data.csv", "w+") as csv_file:
        data_writer = csv.writer(csv_file)
        data_writer.writerow(
            ["Disease Name", "Image URL", "Pest Type", "Origin", "Legal Content", "Secure any content"])
        for key, value in dict_data.iteritems():
            try:
                data_writer.writerow([key, value[0], value[1], value[2], value[3], value[4]])
            except IndexError:
                pass


def index(request):
    data = {"dict_data": {}}
    with open("data.csv") as csv_file:
        data_reader = csv.reader(csv_file)
        for row in data_reader:
            my_list = [row[1], row[2], row[3], row[4], row[5]]
            data["dict_data"].update({row[0]: my_list})
    return render(request, "show_data.html", data)
