import csv
import sys
from services.nlq import get_query_nlq
from libs.openai_libs import openai_text_completion

idx = 0
ou_id = "e7252c77ff4c"

# Variables to store the statistics
total = 0
validation_success = 0
table_success = 0
metric_success = 0
dimensions_success = 0
query_success = 0
success = 0

# List to store test results
test_results = []

prompt_sql_compare = """
You are a clickhouse 22.7 expert

This is SQL statement 1
"{sql1}"

This is SQL statement 2
"{sql2}"

Tell me if two SQL statements will give me the exact same result. Answer should
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
    user_text = prompt_sql_compare.format(sql1=sql1, sql2=sql2)
    result = openai_text_completion("", user_text)
    return result == "True", result


def test_row(row):
    global idx, total, validation_success, table_success, metric_success, dimensions_success, query_success, success

    idx += 1
    total += 1
    test_passed = True

    print(f"Processing row {idx}: {row['Question']}")

    # Get actual values by executing function
    product, table, dimensions, metric, valid_question, query = get_query_nlq(
        row['Question'], ou_id)

    # Initialize expected and actual values for output
    expected_table = row["Table"]
    expected_metric = row["Metric"]
    expected_dimension = row["Dimensions"]
    actual_table = table
    actual_metric = metric
    actual_dimension = ', '.join(dimensions) if dimensions else ""

    # Check table
    if not table == expected_table:
        print(f"Table mismatch: Expected {expected_table}, Got {actual_table}")
        test_passed = False
    else:
        table_success += 1
        print("Table validation passed")

    # Check metric
    if not metric == expected_metric:
        print(
            f"Metric mismatch: Expected {expected_metric}, Got {actual_metric}")
        test_passed = False
    else:
        metric_success += 1
        print("Metric validation passed")

    # # Check dimensions
    # if not (dimensions == row["Dimensions"]):
    #     print(
    #         f"Dimensions mismatch: Expected {expected_dimension}, Got {actual_dimension}")
    #     test_passed = False
    # else:
    #     dimensions_success += 1
    #     print("Dimensions validation passed")

    # Commented out SQL query check
    # query_match, reason = match_sql(query, row["ExpectedQuery"])
    # if not query_match:
    #     print(f"Query mismatch: {reason}")
    #     test_passed = False
    # else:
    #     query_success += 1
    #     print("Query validation passed")

    # Store the result in the global list
    test_results.append({
        "Question": row['Question'],
        "expected_table": expected_table,
        "actual_table": actual_table,
        "expected_metric": expected_metric,
        "actual_metric": actual_metric,
        "expected_dimension": expected_dimension,
        "actual_dimension": actual_dimension,
        "test_result": "Pass" if test_passed else "Fail"
    })

    if test_passed:
        success += 1
        print(f"Row {idx} passed\n")
    else:
        print(f"Row {idx} failed\n")

    return test_passed


def parse_tsv_output(rd):
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

        if parsed_row["Valid"] == "TRUE":
            parsed_row["Valid"] = True
        elif parsed_row["Valid"] == "FALSE":
            parsed_row["Valid"] = False
        else:
            parsed_row["Valid"] = None

        parsed_row["Dimensions"] = parsed_row["Dimensions"].split(',')

        parsed.append(parsed_row)

    return parsed


def write_results_to_csv(filename):
    # Define headers and write results to a CSV file
    headers = ["Question", "expected_table", "actual_table", "expected_metric",
               "actual_metric", "expected_dimension", "actual_dimension", "test_result"]
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for result in test_results:
            writer.writerow(result)
    print(f"Results written to {filename}")


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
    # Output filename can be changed as needed
    write_results_to_csv("test_results.csv")


run()