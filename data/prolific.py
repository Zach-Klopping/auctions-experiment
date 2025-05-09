import requests
import json

url = "https://api.prolific.com/api/v1/studies/"

headers = {
    "Content-Type": "application/json",
    "Authorization": "Token 2YVS6OR3I5dn_N-rw6O9M09b27JdmpzXtXqxhNoCd2xCACl3d27uSOdWxV2EdMyazov3y8NDuCrwRjnTdHSuo7us-r_ZXXZOfFcykB6NZaeTg5SNlY-8hboZ"
}

payload = json.dumps(
{
  "name": "Auctions Study",
  "description": "Please god please god please god",
  "external_study_url": "https://auctions-experiment-388edd40b64b.herokuapp.com/",
  "reward": 1,
  "total_available_places": 1,
  "prolific_id_option": "question",
  "completion_codes": [
    {
      "code": "ABC123",
      "code_type": "COMPLETED",
      "actions": [
        {
          "action": "MANUALLY_REVIEW"
        }
      ]
    }
  ],
  "estimated_completion_time": 15
})

response = requests.request("POST", url, headers=headers, data=payload)

print(json.dumps(response.json(), indent=2))