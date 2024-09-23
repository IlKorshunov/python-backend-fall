import json
from typing import List

def mean(array: List[float]) -> str:
    res = 0
    for i in array:
        res += i
    result = res / len(array) 
    response = {"result": result}
    return json.dumps(response)
