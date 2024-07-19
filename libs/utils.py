from datetime import datetime, timedelta
import json

def calculate_previous_date_range(current_start_date, current_end_date):
    # Convert string dates to datetime objects
    start_date = datetime.strptime(current_start_date, '%Y-%m-%d')
    end_date = datetime.strptime(current_end_date, '%Y-%m-%d')

    # Calculate the difference in days
    date_difference = (end_date - start_date).days

    # Calculate the previous end date
    previous_end_date = start_date - timedelta(days=1)

    # Calculate the previous start date
    previous_start_date = previous_end_date - timedelta(days=date_difference)

    # Convert datetime objects back to string
    previous_start_date_str = previous_start_date.strftime('%Y-%m-%d')
    previous_end_date_str = previous_end_date.strftime('%Y-%m-%d')

    return previous_start_date_str, previous_end_date_str


def get_data_from_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data
