import csv
import sys
from services.nlq import get_query_nlq
from libs.openai_libs import openai_text_completion

idx = 0
ou_id = "e7252c77ff4c"

### Set of variables to store the statistics

# Total 
total = 0
# Valid metric
validation_success = 0
# Table
table_success = 0
# Metric
metric_success = 0
# Table dimensions
dimensions_success = 0
# Result of query
query_success = 0
# All success
success = 0

prompt_sql_compare = """
You are a clickhouse 22.7 expert

This is SQL statement 1
"{sql1}"

This is SQL statement 2
"{sql2}"

Till me if two SQL statements will give me the exact same result. Answer should
strictly be either "True" if the results are exactly the same. Otherwise only
return a reason describing why these are different.
"""

def print_results():
    print('Total: ', total)
    print('Validation failures: ', total - validation_success)
    print('Table failures: ', total - table_success)
    print('Metric failures: ', total - metric_success)
    print('Dimensions failures: ', total - dimensions_success)
    print('Query failures: ', total - query_success)
    print('Result failures: ', total - success)

def match_sql(sql1, sql2):
    # Returns True if sql1 & sql2 statements are exact match, False otherwise.
    
    user_text = prompt_sql_compare.format(sql1=sql1, sql2=sql2)
    result = openai_text_completion("", user_text)
    return result == "True", result


def test_row(row):
    # Tests each row privided by input against the function return values and
    # updates the metric variables for success & Log the failures

    global idx
    global total
    global validation_success
    global table_success
    global metric_success
    global dimensions_success
    global query_success
    global success

    idx += 1
    total += 1
    test_passed = True

    mismatch_list = []

    # Get actual values by executing function
    product, table, dimensions, metric,valid_question, query = get_query_nlq(row['Question'],ou_id)

    # Check validation
    if not (valid_question == row["Valid"]):
        mismatch_list.append({
            "field": "Validation",
            "expected": row["Valid"],
            "got": valid_question
        })
        test_passed = False
    else:
        validation_success += 1

    # Check table
    if not table == row["Table"]:
        mismatch_list.append({
            "field": "Table",
            "expected": row["Table"],
            "got": table
        })
        test_passed = False
    else:
        table_success += 1

    # Check metric
    if not metric == row["Metric"]:
        mismatch_list.append({
            "field": "Metric",
            "expected": row["Metric"],
            "got": metric
        })
        test_passed = False
    else:
        metric_success += 1

    # Check dimensions
    if not (dimensions == row["Dimensions"]):
        mismatch_list.append({
            "field": "Dimensions",
            "expected": row["Dimensions"],
            "got": dimensions
        })
        test_passed = False
    else:
        dimensions_success += 1

    # Check sql query criteria
    query_match, reason = match_sql(query, row["ExpectedQuery"])
    if not query_match:
        mismatch_list.append({
            "field": "Query",
            "expected": row["ExpectedQuery"],
            "got": query,
            "reason": reason
        })
        test_passed = False
    else:
        query_success += 1

    if test_passed:
        success += 1
    else:
        print(f"Failed {idx}:-\nQuestion: {row['Question']}")
        for item in mismatch_list:
            print(f"""
  FIELD:    {item["field"]}
  EXPECTED: {item["expected"]}
  GOT:      {item["got"]}""")
            if item.get("reason"):
                print(f"  REASON: {item["reason"]}")
        print("-------------")
    return test_passed

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

        parsed_row["Dimensions"] = parsed_row["Dimensions"].split(',')

        parsed.append(parsed_row)
    
    return parsed

def run():
    if len(sys.argv) != 2:
        print("Invalid number of arguments")
        return

    with open(f"./test_inputs/{sys.argv[1]}") as fd:
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        parsed = parse_tsv_output(rd)
        for row in parsed:
            if row["Active"] == "TRUE":
                test_row(row)

    print_results()

run()