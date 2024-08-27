import csv
from services.nlq import get_query_nlq

idx = -1
ou_id = "e7252c77ff4c"

### Set of variables to store the statistics

# Total 
total = 0
# Table metric & aggregation
metric_success = 0
# Table dimensions
dimensions_success = 0
# Query filters
filters_success = 0
# Result of query
success = 0

def print_results():
    print('Total: ', total)
    print('Metric failures: ', total - metric_success)
    print('Dimensions failures: ', total - dimensions_success)
    print('Filters failures: ', total - filters_success)
    print('Result failures: ', total - success)

def parse_row(row):
    dimensions = row[4].split(',')
    filters = []

    return {
        "question": row[0],
        "table": row[1],
        "metric": row[2],
        "metric_agg": row[3],
        "dimensions": dimensions,
        "filters": filters,
        "expected_query": row[6],
        "expected_result": row[7],
    }

def test_row(row):
    global idx
    global total
    global metric_success
    global dimensions_success
    global filters_success
    global success

    idx += 1
    if idx == 0:
        # Ignore header row
        return
    
    row = parse_row(row)

    total += 1

    product, table, dimensions, metric,valid_question, query = get_query_nlq(row['question'],ou_id)
    filters = ""
    if not (table == row["table"] and metric == row["metric"]):
        print(f'Failed {idx}: MetricMismatch : (Table|{table}|{row["table"]}), (Metric|{metric}|{row["metric"]}))')
        return False
    metric_success += 1
    return True

def run():
    with open("./test_inputs/sample1.tsv") as fd:
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        for row in rd:
            test_row(row)

    print_results()

run()