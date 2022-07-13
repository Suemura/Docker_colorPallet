import json
import traceback
from src.types.index import RequestError


def functionWrapper(func):
    def wrapper(*args, **kwargs):
        try:
            ret = func(*args, **kwargs)
            return {
                "statusCode": 200,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps(ret, default=str),
            }
        except RequestError as e:
            print(traceback.format_exc())
            responseBody = {"ErrorType": e.errorType, "message": e.message}
            return {
                "statusCode": e.statusCode,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps(responseBody, ensure_ascii=False),
            }
        except Exception:
            print(traceback.format_exc())
            return {
                "statusCode": 500,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": "Internal Server Error",
            }
    return wrapper
