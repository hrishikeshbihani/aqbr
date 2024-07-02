import re
from openai_request import make_call_to_openai


def parse_jsonl_data(jsonl_array, title):
  jsonl_string_array = map(lambda x: str(x), jsonl_array)
  jsonl_array_string = "".join(jsonl_string_array)
  return """
{title}

{jsonl_array}
""".format(title=title, jsonl_array=jsonl_array_string)


def chart_generator(jsonl_array, title):
    prompt_header = """
    You are a data visaualization and analysis expert using chartJS version 2 and height is 800 and widht is 1000.
#     Your task is to understand and analyze the data provided to you and create relevant visualization and it should be visually appealing for a business presentation
#     Make a Top 5 horizontal bar chart type if preivous and current data then use dual horizontal bar chart,
#     Make pie chart only if the labels < 4
#     If any other chart is revelant create that also (Generate 1-3 charts as required)
#     Chart Should be presentable,labels should be present it should not get cut in the image, data count descending order,no need for tooltip
#     Keep the colour of the bars only blue and orange (use different colour only when required) and always have data labels(options) using plugin chartjs-plugin-datalabels and align end,anchor end,Add chart title,all fonts colour black,you will only provide me with the link of the images of the charts and make sure the links are not 404,Ensure this term has proper qoutes closing -> "align":"end"

#     Example Chart for reference: https://quickchart.io/chart?width=1000&height=1000&c={"type":"horizontalBar","data":{"labels":["Name mismatch in the original PAN Card","Third party prompt","Customer Reading from Document","Original PAN not available","Incorrect answer to security question"],"datasets":[{"label":"Current","data":[1,1,1,1,1],"backgroundColor":["blue","blue","blue","blue","blue"]},{"label":"Previous","data":[23,23,21,20,14],"backgroundColor":["orange","orange","orange","orange","orange"]}]},"options":{"plugins":{"datalabels":{"anchor":"end","align":"end","color":"black"}},"title":{"display":true,"text":"Comparison of Current and Previous Issues"}}}

Encode URL: https%3A%2F%2Fquickchart.io%2Fchart%3Fwidth%3D1000%26height%3D1000%26c%3D%7B%22type%22%3A%22horizontalBar%22%2C%22data%22%3A%7B%22labels%22%3A%5B%22Name%20mismatch%20in%20the%20original%20PAN%20Card%22%2C%22Third%20party%20prompt%22%2C%22Customer%20Reading%20from%20Document%22%2C%22Original%20PAN%20not%20available%22%2C%22Incorrect%20answer%20to%20security%20question%22%5D%2C%22datasets%22%3A%5B%7B%22label%22%3A%22Current%22%2C%22data%22%3A%5B1%2C1%2C1%2C1%2C1%5D%2C%22backgroundColor%22%3A%5B%22blue%22%2C%22blue%22%2C%22blue%22%2C%22blue%22%2C%22blue%22%5D%7D%2C%7B%22label%22%3A%22Previous%22%2C%22data%22%3A%5B23%2C23%2C21%2C20%2C14%5D%2C%22backgroundColor%22%3A%5B%22orange%22%2C%22orange%22%2C%22orange%22%2C%22orange%22%2C%22orange%22%5D%7D%5D%7D%2C%22options%22%3A%7B%22plugins%22%3A%7B%22datalabels%22%3A%7B%22anchor%22%3A%22end%22%2C%22align%22%3A%22end%22%2C%22color%22%3A%22black%22%7D%7D%2C%22title%22%3A%7B%22display%22%3Atrue%2C%22text%22%3A%22Comparison%20of%20Current%20and%20Previous%20Issues%22%7D%7D%7D

    """
    jsonl_data_parsed = parse_jsonl_data(jsonl_array, title)
    prompt = """
    {prompt_header}
    The data is as follows: 
    {data}
    The link should be complusory valid URL Encoded and give only link,nothing else
    """.format(prompt_header=prompt_header, data=jsonl_data_parsed)
    response = make_call_to_openai(prompt, "gpt-4o")
    print(response)
    url_pattern = re.compile(
       r'https:.*?(?=\s|$)')
    urls = url_pattern.findall(response)
    print("URL",urls)
    return urls
