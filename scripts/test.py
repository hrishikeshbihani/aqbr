import csv
import streamlit as st
from services.chat_completion import get_query

ou_id = st.text_input("Enter OU ID", value="e7252c77ff4c")

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

def test_row(row, idx):
    global total
    global metric_success
    global dimensions_success
    global filters_success
    global success
    
    row = parse_row(row)

    total += 1

    # {query, table, metric, metric_agg, dimensions, filters} = get_query(row[0], ou_id)
    query = ""
    table = ""
    metric = ""
    metric_agg = ""
    dimensions = ""
    filters = ""
    if not (table == row["table"] and metric == row["metric"] and metric_agg == row["metric_agg"]):
        print(f'Failed {idx}: MetricMismatch : (Table|{table}|{row["table"]}), (Metric|{metric}|{row["metric"]}), (MetricAgg|{metric_agg}|{row["metric_agg"]})')
        return False
    metric_success += 1
    return True

def run():
    with open("./scripts/test_inputs/sample1.tsv") as fd:
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        for row, i in rd:
            test_row(row, i)

    print_results()

run()