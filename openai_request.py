import logging
import requests
import json
import datetime
from openai import OpenAI
open_ai_client = OpenAI()
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f'openai_call_logs/logfile_{timestamp}.log'
# Set up logging configuration
logging.basicConfig(
    filename=filename,  # Log file name
    filemode='a',        # Append mode ('w' for overwrite)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
    datefmt='%Y-%m-%d %H:%M:%S',  # Date format
    level=logging.DEBUG  # Log level
)
logger = logging.getLogger()


def make_call_to_openai(prompt):
  logger.info(prompt)
  url = "https://api.openai.com/v1/chat/completions"
  payload = json.dumps({
    "model": "gpt-4o",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": prompt
          }
        ]
      }
    ],
    "max_tokens": 1500
  })
  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer api_key_goes_here',
    'Cookie': '__cf_bm=rXD8QGnnR.3ZwpE6cVLmRIUiisK7OLOXcLJdP4Oj2pU-1717140354-1.0.1.1-8tPW2Gba2FJZtuL0Uumj7y8keMT2sv61psMFn32tbTZtYQeKpcHVYwHFdiAuv9VazjVM4Eb6uZ3GpJbMHqwVcg; _cfuvid=1pG74ojeUhECcNrA1pepiKG0BhN31hokp4w6e4Tul1k-1717136312953-0.0.1.1-604800000'
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  logger.info(response.text)


with open('prompt.txt', 'r') as file:
    prompt = file.read()
    make_call_to_openai(prompt)
    
    
def openai_text_completion(system_text, user_text):
    try:
        completion = open_ai_client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": system_text},
                {"role": "user", "content": user_text},
            ],
            temperature=1.1,
            max_tokens=4096
        )
        if (
            completion
            and completion.choices[0]
            and completion.choices[0].message
            and completion.choices[0].message.content
        ):
            return completion.choices[0].message.content
        raise Exception(
            f"Exception in openai_text_completion. Response: {json.dumps(completion)}"
        )

    except Exception as err:
        raise Exception("Error in openai text completion. Error: {err}".format(err=err))

