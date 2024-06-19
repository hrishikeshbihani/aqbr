def get_url(card_number, start_date, end_date, ou_id, previous_start_date, previous_end_date):
  url = (
      "https://metabase.idfystaging.com/api/card/{card_number}/query/csv?format_rows=true&parameters="
      "["
      "{{\"type\": \"date/single\", \"value\": \"{start_date}\", \"target\": [\"variable\", [\"template-tag\", \"start_date\"]]}},"
      "{{\"type\": \"date/single\", \"value\": \"{end_date}\", \"target\": [\"variable\", [\"template-tag\", \"end_date\"]]}},"
      "{{\"type\": \"string/=\", \"value\": [\"{ou_id}\"], \"target\": [\"variable\", [\"template-tag\", \"ou_id\"]]}},"
      "{{\"type\": \"date/single\", \"value\": \"{previous_start_date}\", \"target\": [\"variable\", [\"template-tag\", \"previous_start_date\"]]}},"
      "{{\"type\": \"date/single\", \"value\": \"{previous_end_date}\", \"target\": [\"variable\", [\"template-tag\", \"previous_end_date\"]]}}"
      "]"
  ).format(card_number=card_number, start_date=start_date, end_date=end_date, ou_id=ou_id, previous_start_date=previous_start_date, previous_end_date=previous_end_date)
  return url

def call_url(url):
  headers = {
      'accept': '*/*',
      'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
      'content-type': 'application/x-www-form-urlencoded',
      'x-api-key': 'mb_N6OuXSal/8tHE9tap8nB5isIcyODEaFWWR0RKFZSgKE=',
      'origin': 'https://metabase.idfystaging.com',
      'priority': 'u=1, i',
      'referer': 'https://metabase.idfystaging.com/dashboard/258-top-reject-and-utv-reasons-maker-checker?tab=33-reject-reasons-by-maker-and-checker&start_date=2024-06-02&end_date=2024-06-06&ouid=&timezone=Asia%2FKolkata&ouname=',
      'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"macOS"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
      'Cookie': 'metabase.DEVICE=51300c22-528e-4ff6-973a-5de6408b36a4; metabase.TIMEOUT=alive'
  }
  response = requests.request("POST", url, headers=headers)
  return response
