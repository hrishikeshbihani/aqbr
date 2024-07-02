from openai_request import make_call_to_openai


def parse_jsonl_data(jsonl_array, title):
  print(jsonl_array)
  jsonl_string_array = map(lambda x: str(x), jsonl_array)
  jsonl_array_string = "".join(jsonl_string_array)
  return """
{title}

{jsonl_array}
""".format(title=title, jsonl_array=jsonl_array_string)


def chart_generator(jsonl_array, title):
    prompt_header = """
    I need some graphs and charts that I can use for presentation. You need to generation URLs of charts.io service which would represent the data I am giving at the end. Ensure that the charts you are generating has the title and labels are well present. You should only give me the URLs and do not write anything else in the output.

    Example Chart for reference: https://quickchart.io/chart?width=1000&height=1000&c={"type":"horizontalBar","data":{"labels":["Name mismatch in the original PAN Card","Third party prompt","Customer Reading from Document","Original PAN not available","Incorrect answer to security question"],"datasets":[{"label":"Current","data":[1,1,1,1,1],"backgroundColor":["blue","blue","blue","blue","blue"]},{"label":"Previous","data":[23,23,21,20,14],"backgroundColor":["orange","orange","orange","orange","orange"]}]},"options":{"plugins":{"datalabels":{"anchor":"end","align":"end","color":"black"}}"title":{"display":true,"text":"Comparison of Current and Previous Issues"}}}
    
    """
    jsonl_data_parsed = parse_jsonl_data(jsonl_array, title)
    prompt = """
    {prompt_header}
    
    The data is as follows: 
    {data}
    """.format(prompt_header=prompt_header, data=jsonl_data_parsed)
    response = make_call_to_openai(prompt, "gpt-3.5-turbo-0125")
    print(response)

    # output = openai_text_completion(system_text, user_text)
    # url_pattern = re.compile(
    #     r'https://quickchart\.io/chart\?width=\d+&height=\d+&c=\{".*?"\}\}\}\}')
    # urls = url_pattern.findall(output)
    # print(output)
    # return urls
