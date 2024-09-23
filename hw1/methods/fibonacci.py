import json

def fibonacci(n: int) -> str:
    if n == 0:
        return json.dumps({"result": 0})
    def fib(n: int) -> int:
        if n == 1 or n == 2:
            return 1
        return fib(n-1) + fib(n-2)
    result = fib(n)
    response = {"result": result}
    return json.dumps(response)