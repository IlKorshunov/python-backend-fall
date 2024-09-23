import json

def factorial(n: int) -> str:
    result = 1
    if n > 0:
        for i in range(2, n + 1):
            result *= i
    response = {"result": result}
    return json.dumps(response)

