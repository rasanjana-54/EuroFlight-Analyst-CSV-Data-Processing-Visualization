"""
****************************************************************************
Additional info
 1. I declare that my work contains no examples of misconduct, such as
 plagiarism, or collusion.
 2. Any code taken from other sources is referenced within my code solution.
 3. Student ID: [20240728/w2152943]
 4. Date: [sep 01]
****************************************************************************
"""

from graphics import *
import csv
import os

data_list = []  # data_list holds the data from csv file

# Dictionary of airport codes (Table 2)
AIRPORTS = {
    "LHR": "London Heathrow",              
    "MAD": "Madrid Adolfo Suárez-Barajas",
    "CDG": "Charles De Gaulle International",
    "IST": "Istanbul Airport International",
    "AMS": "Amsterdam Schiphol",
    "LIS": "Lisbon Portela",
    "FRA": "Frankfurt Main",
    "FCO": "Rome Fiumicino",
    "MUC": "Munich International",
    "BCN": "Barcelona International"
}

# Dictionary of airline codes (Table 3)
AIRLINES = {
    "BA": "British Airways",
    "AF": "Air France",
    "AY": "Finnair",
    "KL": "KLM",
    "SK": "Scandinavian Airlines",
    "TP": "TAP Air Portugal",
    "TK": "Turkish Airlines",
    "W6": "Wizz Air",
    "U2": "easyJet",
    "FR": "Ryanair",
    "A3": "Aegean Airlines",
    "SN": "Brussels Airlines",
    "EK": "Emirates",
    "QR": "Qatar Airways",
    "IB": "Iberia",
    "LH": "Lufthansa"
}

# ----------------------------------------------------------------------------------
# Provided function - DO NOT EDIT
def load_csv(CSV_chosen):
    """
    Loads CSV file by name into the list 'data_list'
    """
    with open(CSV_chosen, 'r', encoding="utf-8") as file:
        csvreader = csv.reader(file)
        header = next(csvreader)  # skip header
        for row in csvreader:
            data_list.append(row)
    return header

# ----------------------------------------------------------------------------------
# Task A: Input validation + load
def get_valid_airport():
    """Prompt for a valid 3-letter airport code (case-insensitive)."""
    while True:
        code = input("Please enter the three-letter code for the departure city required: ").strip().upper()
        if len(code) != 3:
            print("Wrong code length - please enter a three-letter city code")
            continue
        if code not in AIRPORTS:
            print("Unavailable city code - please enter a valid city code")
            continue
        return code

def get_valid_year():
    """Prompt for a valid 4-digit year (2000-2025)."""
    while True:
        year = input("Please enter the year required in the format YYYY: ").strip()
        if not year.isdigit() or len(year) != 4:
            print("Wrong data type - please enter a four-digit year value")
            continue
        year = int(year)
        if year < 2000 or year > 2025:
            print("Out of range - please enter a value from 2000 to 2025")
            continue
        return year

def choose_file():
    """Combine airport code and year into filename, load data, return details."""
    code = get_valid_airport()
    year = get_valid_year()
    filename = f"{code}{year}.csv"
    
    # clear any old data
    data_list.clear()
    
    # Check if the file exists before trying to load it
    if not os.path.exists(filename):
        print(f"Error: The file {filename} does not exist.")
        # Recursively call choose_file to prompt again
        return choose_file()
        
    load_csv(filename)
    airport_name = AIRPORTS[code]

    print("********************************************************************")
    print(f"File {filename} selected - Planes departing {airport_name} {year}.")
    print("********************************************************************")

    return filename, airport_name, year, code

# ----------------------------------------------------------------------------------
# Task B: Analyse outcomes
def analyse_data():
    """
    Process the dataset and calculate all required outcomes.
    Returns a dictionary of results.
    """
    total_flights = len(data_list)

    runway1 = sum(1 for row in data_list if len(row) > 8 and row[8] == "1")
    over_500 = sum(1 for row in data_list if len(row) > 5 and row[5].isdigit() and int(row[5]) > 500)
    british_airways = sum(1 for row in data_list if len(row) > 1 and row[1].startswith("BA"))
    rain_flights = sum(1 for row in data_list if len(row) > 9 and "rain" in row[9].lower())

    # departures per hour (12-hour period)
    avg_per_hour = round(total_flights / 12, 2) if total_flights else 0

    # Air France %
    air_france = sum(1 for row in data_list if len(row) > 1 and row[1].startswith("AF"))
    air_france_percent = round((air_france / total_flights) * 100, 2) if total_flights else 0

    # delayed flights %
    delayed = sum(1 for row in data_list if len(row) > 3 and row[2] != row[3])
    delayed_percent = round((delayed / total_flights) * 100, 2) if total_flights else 0

    # hours of rain
    rain_hours = {row[2].split(":")[0] for row in data_list if len(row) > 9 and "rain" in row[9].lower() and len(row[2].split(":")) > 0}
    total_rain_hours = len(rain_hours)

    # most common destination
    destinations = {}
    for row in data_list:
        if len(row) > 4:
            dest_code = row[4]
            destinations[dest_code] = destinations.get(dest_code, 0) + 1
    most_common = []
    if destinations:
        max_count = max(destinations.values())
        most_common = [AIRPORTS.get(code, code) for code, count in destinations.items() if count == max_count]

    return {
        "total_flights": total_flights,
        "runway1": runway1,
        "over_500": over_500,
        "british_airways": british_airways,
        "rain_flights": rain_flights,
        "avg_per_hour": avg_per_hour,
        "air_france_percent": air_france_percent,
        "delayed_percent": delayed_percent,
        "rain_hours": total_rain_hours,
        "most_common": most_common
    }

def print_results(results, airport_name, year, filename):
    """Nicely formatted print to shell."""
    print("\n*********************************************************************************")
    print(f"File {filename} selected - Planes departing {airport_name} {year}")
    print("*********************************************************************************")
    print(f"The total number of flights from this airport was {results['total_flights']}")
    print(f"The total number of flights departing Runway one was {results['runway1']}")
    print(f"The total number of departures of flights over 500 miles was {results['over_500']}")
    print(f"There were {results['british_airways']} British Airways flights from this airport")
    print(f"There were {results['rain_flights']} flights from this airport departing in rain")
    print(f"There was an average of {results['avg_per_hour']} flights per hour from this airport")
    print(f"Air France planes made up {results['air_france_percent']}% of all departures")
    print(f"{results['delayed_percent']}% of all departures were delayed")
    print(f"There were {results['rain_hours']} hours in which rain fell")
    print(f"The most common destinations are {results['most_common']}")

# ----------------------------------------------------------------------------------
# Task C: Save results
def save_results(results, airport_name, year, filename):
    """Save results to results.txt (create if doesn't exist, append if it does)."""
    try:
        with open("results.txt", "a", encoding="utf-8") as f:
            f.write("\n*********************************************************************************\n")
            f.write(f"File {filename} selected - Planes departing {airport_name} {year}\n")
            f.write("*********************************************************************************\n")
            f.write(f"The total number of flights from this airport was {results['total_flights']}\n")
            f.write(f"The total number of flights departing Runway one was {results['runway1']}\n")
            f.write(f"The total number of departures of flights over 500 miles was {results['over_500']}\n")
            f.write(f"There were {results['british_airways']} British Airways flights from this airport\n")
            f.write(f"There were {results['rain_flights']} flights from this airport departing in rain\n")
            f.write(f"There was an average of {results['avg_per_hour']} flights per hour from this airport\n")
            f.write(f"Air France planes made up {results['air_france_percent']}% of all departures\n")
            f.write(f"{results['delayed_percent']}% of all departures were delayed\n")
            f.write(f"There were {results['rain_hours']} hours in which rain fell\n")
            f.write(f"The most common destinations are {results['most_common']}\n")
    except FileNotFoundError:
        # If file doesn't exist, create it first and then write
        with open("results.txt", "w", encoding="utf-8") as f:
            f.write("\n*********************************************************************************\n")
            f.write(f"File {filename} selected - Planes departing {airport_name} {year}\n")
            f.write("*********************************************************************************\n")
            f.write(f"The total number of flights from this airport was {results['total_flights']}\n")
            f.write(f"The total number of flights departing Runway one was {results['runway1']}\n")
            f.write(f"The total number of departures of flights over 500 miles was {results['over_500']}\n")
            f.write(f"There were {results['british_airways']} British Airways flights from this airport\n")
            f.write(f"There were {results['rain_flights']} flights from this airport departing in rain\n")
            f.write(f"There was an average of {results['avg_per_hour']} flights per hour from this airport\n")
            f.write(f"Air France planes made up {results['air_france_percent']}% of all departures\n")
            f.write(f"{results['delayed_percent']}% of all departures were delayed\n")
            f.write(f"There were {results['rain_hours']} hours in which rain fell\n")
            f.write(f"The most common destinations are {results['most_common']}\n")

# ----------------------------------------------------------------------------------
# Task D: Histogram with graphics.py
def get_valid_airline():
    """Prompt for a valid 2-letter airline code (case-insensitive)."""
    while True:
        code = input("Enter a two-character Airline code to plot a histogram: ").strip().upper()
        if code not in AIRLINES:
            print("Unavailable Airline code please try again.")
            continue
        return code

def plot_histogram(airline_code, airport_name, year, airport_code):
    """Plot histogram of flights per hour for chosen airline."""
    # count flights per hour (12-hour period: 0-11)
    hourly_counts = [0] * 12
    for row in data_list:
        if len(row) > 1 and row[1].startswith(airline_code):
            try:
                hour = int(row[2].split(":")[0])
                if 0 <= hour < 12:  # Only consider hours 0-11 (12-hour period)
                    hourly_counts[hour] += 1
            except (ValueError, IndexError):
                continue

    if max(hourly_counts) == 0:
        print(f"No flights found for {AIRLINES[airline_code]} at this airport/year.")
        return

    win = GraphWin("Histogram", 800, 500)
    win.setBackground("light gray")

    max_count = max(hourly_counts)
    bar_width = 50
    spacing = 10
    x_offset = 50
    y_offset = 400
    scale = 300 / max_count if max_count > 0 else 1

    # Draw title
    title_text = f"Departures by hour for {AIRLINES[airline_code]} from {AIRPORTS[airport_code]} {year}"
    title = Text(Point(400, 30), title_text)
    title.setSize(16)
    title.setStyle("bold")
    title.draw(win)

    # Draw bars and labels
    for i in range(12):
        bar_height = hourly_counts[i] * scale
        x1 = x_offset + i * (bar_width + spacing)
        y1 = y_offset - bar_height
        x2 = x1 + bar_width
        y2 = y_offset
        
        # Draw bar
        bar = Rectangle(Point(x1, y1), Point(x2, y2))
        bar.setFill("light green")
        bar.setOutline("dark green")
        bar.setWidth(2)
        bar.draw(win)
        
        # Add count label on top of bar
        count_text = Text(Point(x1 + bar_width/2, y1 - 15), str(hourly_counts[i]))
        count_text.setSize(12)
        count_text.setTextColor("black")
        count_text.draw(win)
        
        # Add hour label below bar
        hour_label = f"{i:02d}"
        hour_text = Text(Point(x1 + bar_width/2, y_offset + 20), hour_label)
        hour_text.setSize(10)
        hour_text.setTextColor("black")
        hour_text.draw(win)

    # Add axis labels
    x_axis = Text(Point(400, 450), "Hours 00:00 to 12:00")
    x_axis.setSize(12)
    x_axis.draw(win)
    
    # Add instruction to close
    instruction = Text(Point(400, 480), "Click anywhere to close")
    instruction.setSize(10)
    instruction.setTextColor("red")
    instruction.draw(win)

    win.getMouse()  # wait for click to close
    win.close()

# ----------------------------------------------------------------------------------
# Task E: Program loop
def main():
    """Main program function that handles the execution flow."""
    print("European Airports Survey Data Analysis")
    print("======================================")
    
    while True:
        # Task A: File selection
        filename, airport_name, year, airport_code = choose_file()
        
        # Task B: Data analysis and display
        results = analyse_data()
        print_results(results, airport_name, year, filename)
        
        # Task C: Save results
        save_results(results, airport_name, year, filename)
        print("\nResults saved to 'results.txt'")
        
        # Task D: Histogram
        airline_code = get_valid_airline()
        plot_histogram(airline_code, airport_name, year, airport_code)
        
        # Task E: Loop control
        while True:
            response = input("Do you want to select a new data file? Y/N: ").strip().upper()
            if response in ["Y", "N"]:
                break
            print("Please enter Y or N")
        
        if response == "N":
            print("Thank you. End of run")
            break

# Run the program
if __name__ == "__main__":
    main()
