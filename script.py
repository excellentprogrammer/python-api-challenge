import requests

def load_fixtures():
    try:
        response = requests.get('http://localhost:8000/departures/load-fixtures')    # request to load the dpatures.json to db.
        print(response.text)
    except requests.ConnectionError as e:
        print("Server is not running. Please try later.")

def date_filter(departure):                                                  # start_date filter definition
    return departure["start_date"] > "2018-06-01"

def category_filter(departure):                                              # category filter definition
    return departure["category"] == "Adventurous"

def filter_departures(departures):                                           # apply date_filter and category_filter together
    departures = list(filter(date_filter, departures))
    departures = list(filter(category_filter, departures))
    return departures

def write_to_csv(departures, filename):
    if len(departures)==0:                                                    #check if there is departures to write.
        print("There is nothing to write.")
        return

    with open(filename,"w") as output:                                        #writing to csv
        columns = []
        column_titles = []

        for column in departures[0]:                                          #retriving columns
            if column!="id":
                columns.append(column)
                column_titles.append(column.title())

        output.write(', '.join(column_titles))
        output.write('\n')
                                                                                # writing rows to the csv
        for departure in departures:
            row = []
            for column in columns:
                row.append(departure[column])

            output.write(', '.join(row))
            output.write('\n')

def collect_data(request_url):
    departures = []
    try:
        response = requests.get(request_url).json()                            # get all the departures by iteration of requests to next url
        while response["next"]:
            departures += response["results"]
            response = requests.get(response["next"]).json()
    except requests.ConnectionError as e:
        print("Server is not running. Please try later.")
    return departures

request_url = 'http://localhost:8000/departures/'
csv_filename = "filtered_departures.csv"
load_fixtures()
departures = collect_data(request_url)
departures = filter_departures(departures)
write_to_csv(departures, csv_filename)
