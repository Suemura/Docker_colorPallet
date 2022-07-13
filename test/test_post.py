import requests, json

endpoint = "https://ph5yjc0rci.execute-api.ap-northeast-1.amazonaws.com/dev/create_s3_presigned_url"

body = {
    "sessionID" : "testSession"
}

response = requests.post(endpoint, params=body)
print(response.text)
responce_dict = response.json()
presigned_url = responce_dict["body"]["url"]

print("S3 Pre-signed URL : {}".format(presigned_url)) 