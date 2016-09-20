import requests
from bs4 import BeautifulSoup
import csv
import os


def get_month_list():
    index_page_url = 'http://www.rebgv.org/home-price-index'
    source_code = requests.get(index_page_url)
    source_code_text = source_code.text
    dom = BeautifulSoup(source_code_text, "html.parser")
    # month list as empty array
    month_list = []
    for selection in dom.find_all("select"):
        if selection["name"] == "date":
            for option in selection.find_all('option'):
                month_list.append(str(option["value"]))

    return month_list


def get_monthly_data(month):
    monthly_data_url = 'http://www.rebgv.org/home-price-index?region=all&type=all&date=' + month
    source_code = requests.get(monthly_data_url)
    source_code_text = source_code.text
    dom = BeautifulSoup(source_code_text, "html.parser")
    listing_table = dom.find('table')
    tbody = listing_table.find('tbody')
    row_list = tbody.find_all('tr')
    i = 0
    row_list_len = len(row_list)

    monthly_data = []
    while i < row_list_len-1:
        if row_list[i].has_attr('class'):
            # the one before great vancouver is type
            type = get_type(row_list[i-1])

            # check next 24 rows
            j = 0
            while j < 23:
                if i+j < row_list_len:
                    # check is isSeparator
                    if is_separator(row_list[i+j]) == False:
                        if is_type(row_list[i+j]) == False:
                            area_data = get_area_data(row_list[i + j], type, month)
                            monthly_data.append(area_data)

                j = j+1

            # check new line has separator

        i = i + 1

    return monthly_data


def get_type(row):
    h2 = row.find('h2')
    return h2.string.strip(' ')


def is_separator(row):
    separator = row.find('td', 'separator')

    if separator == None:
        return False
    else:
        return True


def is_type(row):
    h2 = row.find('h2')

    if h2 == None:
        return False
    else:
        return True


def get_area_data(row, type, month):
    td_list = row.find_all('td')
    area = td_list[0].string
    benchmark = int(td_list[1].string.replace('$', '').replace(',', ''))
    price_index = float(td_list[2].string)
    area_data = {"area": area, "benchmark": benchmark, "price_index": price_index, "type": type, "month": month}
    return area_data


def WriteDictToCSV(csv_file,csv_columns,dict_data):
    try:
        with open(csv_file, 'wb') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError as (errno, strerror):
            print("I/O error({0}): {1}".format(errno, strerror))
    return


def start_spider():
    month_list = get_month_list()
    # test with july

    csv_header = ["type", "month", "benchmark", "price_index", "area"]
    csv_data = []

    # testing
    # monthly_data = get_monthly_data("2016-07-01")
    # print monthly_data

    for month in month_list:
        monthly_data = get_monthly_data(month)
        csv_data = csv_data + monthly_data
        print "finish month: " + month

    # save to csv
    currentPath = os.getcwd()
    csv_file = currentPath + "/csv/hpi_data.csv"
    WriteDictToCSV(csv_file, csv_header, csv_data)

# start the app
start_spider()

# run analysis
def sort_by_area():
    area_data = {}

    with open('./csv/hpi_data.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # find area
            area = row["area"]

            if area in area_data:
                area_data[area].append(row)
            else:
                # create new object
                area_data[area] = []
                area_data[area].append(row)

    return area_data


# find increase rate from the start to now
def sort_by_area_type(area_data):
    for area in area_data:
        val = area_data[area]
        for item in val:
            print item


def start_analysis():
    area_data = sort_by_area()
    area_type_data = sort_by_area_type(area_data)



# start_analysis()