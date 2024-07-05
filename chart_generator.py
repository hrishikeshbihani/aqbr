import re
from openai_request import make_call_to_openai
import requests


def parse_jsonl_data(jsonl_array, title):
  jsonl_string_array = map(lambda x: str(x), jsonl_array)
  jsonl_array_string = "".join(jsonl_string_array)
  return """
{title}

{jsonl_array}
""".format(title=title, jsonl_array=jsonl_array_string)


def chart_generator(jsonl_array, title):
    prompt_header = """You are a data visualization and analysis expert tasked with generating graphs using the QuickChart.io service, which supports ChartJS specifications. The generated graphs should have a height of 800 and a width of 1000 (adjust height according to the size of labels).

Your task is to analyze the provided data and create relevant visualizations that are visually appealing for a business presentation. Follow these guidelines:

Graph Type:

1. If applicable, use a dual horizontal bar chart.
2. Generate a pie or donut chart with multiple colors if necessary.

Design Specifications:

1. Ensure the chart is presentable and labels are fully visible (no labels should be cut off).
2. Tooltips are not required.
3. Use blue and orange colors for bars (use other colors only if necessary).
4. Always include data labels using the ChartJS plugin chartjs-plugin-datalabels with options align: end and anchor: end.
5. Add a chart title.
6. All fonts should be black and bold.

Output:

Provide only the link to the images of the charts. Do not write anything else.

Example URL: https://quickchart.io/chart?width=1000&height=1000&c={"type":"horizontalBar","data":{"labels":["Name mismatch in the original PAN Card","Third party prompt","Customer Reading from Document","Original PAN not available","Incorrect answer to security question"],"datasets":[{"label":"Current","data":[1,1,1,1,1],"backgroundColor":["blue","blue","blue","blue","blue"]},{"label":"Previous","data":[23,23,21,20,14],"backgroundColor":["orange","orange","orange","orange","orange"]}]},"options":{"plugins":{"datalabels":{"anchor":"end","align":"end","color":"black"}},"title":{"display"
,"text":"Comparison of Current and Previous Issues"}}}

    """
    jsonl_data_parsed = parse_jsonl_data(jsonl_array, title)
    prompt = """
    {prompt_header}
    The data is as follows: 
    {data}
    Only one output the URL, do not write anything else in the output.
    """.format(prompt_header=prompt_header, data=jsonl_data_parsed)
    response = make_call_to_openai(prompt, "gpt-4o")
    return response


def fix_chart_io_url(url):
    prompt = """Given below is a URL of charts.io. This URL returns a graph/chart in png format based on the data that is passed in its query params. The JSON in this query params seems to be incorrect. Please correct the URL by correctly formatting the JSON in params. Only output the array of full corrected URL in string format. Do not write anything else. 
    
    
    
    {url}
    """.format(url=url)
    response = make_call_to_openai(prompt, "gpt-4o")
    return response


def check_chartio_url_response(url):
    try:
        response = requests.get(url)
        status_code = response.status_code
        if 400 <= status_code < 500:
            return fix_chart_io_url(url)
        return url
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
