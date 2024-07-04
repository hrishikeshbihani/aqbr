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
    prompt_header = """I need charts and graphs to be generated based on the data that I provide. To generate these charts, you can use the quickcharts.io service which generates graphs based on ChartJS specifications. Depending upon the type of data, you can either generate a Bar graph or a Pie chart or line graph.
    
    Give me full URL in the output. For example - https://quickchart.io/chart?width=1000&height=800&c={"type":"doughnut","data":{"labels":["Approved","Rejected"],"datasets":[{"data":[237914,58963],"backgroundColor":["blue","orange","red","green","purple"]}]},"options":{"plugins":{"datalabels":{"anchor":"end","align":"end","color":"black"}},"title":{"display":true,"text":"Previous Profiles Distribution"}}}

    """
    jsonl_data_parsed = parse_jsonl_data(jsonl_array, title)
    prompt = """
    {prompt_header}
    The data is as follows: 
    {data}
    Only output the URL, do not write anything else in the output.
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
