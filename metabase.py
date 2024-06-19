import requests
import json
import os

params_dict = [
    {
        "type": "date/single",
        "value": "2024-06-02",
        "id": "607feb1f",
        "target": [
            "variable",
            [
                "template-tag",
                "start_date"
            ]
        ]
    },
    {
        "type": "date/single",
        "value": "2024-06-06",
        "id": "e3d8bd29",
        "target": [
            "variable",
            [
                "template-tag",
                "end_date"
            ]
        ]
    },
    {
        "type": "string/=",
        "id": "fb8b58f0",
        "target": [
            "variable",
            [
                "template-tag",
                "OUID"
            ]
        ]
    },
    {
        "type": "string/=",
        "value": [
            "Asia/Kolkata"
        ],
        "id": "f3bc4548",
        "target": [
            "variable",
            [
                "template-tag",
                "timezone"
            ]
        ]
    },
    {
        "type": "string/=",
        "id": "22bf4090",
        "target": [
            "dimension",
            [
                "template-tag",
                "OUName"
            ]
        ]
    }
]

params_str = json.dumps(params_dict)
url = "https://metabase.idfystaging.com/api/card/1325/query/csv?format_rows=true&parameters={params_str}".format(params_str = params_str)

headers = {
    'x-api-key': os.getenv("METABASE_API_KEY"),
}

response = requests.request("POST", url, headers=headers)
