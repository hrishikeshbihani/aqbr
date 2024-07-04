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
    prompt_header = """You are a data visaualization and analysis expert using chartJS version 2 and height is 800 and widht is 1000 (Adjust height according to the size of labels).
#     Your task is to understand and analyze the data provided to you and create relevant visualization and it should be visually appealing for a business presentation
#     Make a Top 5 horizontal bar chart type if preivous and current data then use dual horizontal bar chart ,
#     Make pie/donut chart (Can use multiple colours if required)
#     If any other chart is revelant create that also (Generate 1-3 charts as required)
#     Chart Should be presentable,labels should be present it should not get cut in the image, data count descending order,no need for tooltip
#     Keep the colour of the bars only blue and orange (use different colour only when required) and always have data labels(options) using plugin chartjs-plugin-datalabels and align end,anchor end,Add chart title,all fonts colour black and bold,you will only provide me with the link of the images of the charts and make sure the links are not 404 and 
# Ensure there is no closing round bracket ) in end of chart link
# Ensure this term has proper qoutes closing -> "align":"end"

# URL: https://quickchart.io/chart?width=1000&height=1000&c={"type":"horizontalBar","data":{"labels":["Name mismatch in the original PAN Card","Third party prompt","Customer Reading from Document","Original PAN not available","Incorrect answer to security question"],"datasets":[{"label":"Current","data":[1,1,1,1,1],"backgroundColor":["blue","blue","blue","blue","blue"]},{"label":"Previous","data":[23,23,21,20,14],"backgroundColor":["orange","orange","orange","orange","orange"]}]},"options":{"plugins":{"datalabels":{"anchor":"end","align":"end","color":"black"}},"title":{"display":true,"text":"Comparison of Current and Previous Issues"}}}

Encode URL: https://quickchart.io/chart?width=1000&height=800&c={"type":"doughnut","data":{"labels":["Approved","Rejected"],"datasets":[{"data":[237914,58963],"backgroundColor":["blue","orange","red","green","purple"]}]},"options":{"plugins":{"datalabels":{"anchor":"end","align":"end","color":"black"}},"title":{"display":true,"text":"Previous Profiles Distribution"}}}

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
