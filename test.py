import csv
from services.nlq import get_query_nlq

idx = 0
ou_id = "e7252c77ff4c"

### Set of variables to store the statistics

# Total 
total = 0
# Valid metric
validation_success = 0
# Table metric & aggregation
metric_success = 0
# Table dimensions
dimensions_success = 0
# Result of query
success = 0

def print_results():
    print('Total: ', total)
    print('Validation failures: ', total - validation_success)
    print('Metric failures: ', total - metric_success)
    print('Dimensions failures: ', total - dimensions_success)
    print('Result failures: ', total - success)

def test_row(row):
    global idx
    global total
    global validation_success
    global metric_success
    global dimensions_success
    global success

    idx += 1
    total += 1

    product, table, dimensions, metric,valid_question, query = get_query_nlq(row['Question'],ou_id)
    if not (valid_question == row["Valid"]):
        print(f'Failed {idx}: ValidationMismatch : [Validation|{valid_question}|{row["Valid"]}]')
        return False
    if not (table == row["Table"] and metric == row["Metric"]):
        print(f'Failed {idx}: MetricMismatch : [Table|{table}|{row["Table"]}], [Metric|{metric}|{row["Metric"]}]')
        return False
    if not (dimensions == row["Dimensions"]):
        print(f'Failed {idx}: DimensionsMismatch : (Dimensions|{dimensions}|{row["Dimensions"]})')
        return False
    metric_success += 1
    return True

def parse_tsv_output(rd):
    # CSV reader provides output as array of array. This function converts that
    # to array of objects with keys as header row. This prevents the script from
    # breaking if there are any changes in the google sheet.
    #
    # Returns the parsed array of objects
    
    parsed = []
    header_row = []
    first = True

    for row in rd:
        if first:
            header_row = row
            first = False
            continue
        
        parsed_row = {}
        for i in range(len(row)):
            value = row[i]
            key = header_row[i]
            parsed_row[key] = value
        
        if (parsed_row["Valid"] == "TRUE"):
            parsed_row["Valid"] = True
        elif (parsed_row["Valid"] == "FALSE"):
            parsed_row["Valid"] = False
        else:
            parsed_row["Valid"] = None

        parsed.append(parsed_row)
    
    return parsed

def run():
    with open("./test_inputs/sample1.tsv") as fd:
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        parsed = parse_tsv_output(rd)
        for row in parsed:
            test_row(row)

    print_results()

run()