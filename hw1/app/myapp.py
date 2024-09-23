import json
from typing import List

from methods.factorial import factorial
from methods.fibonacci import fibonacci
from methods.mean import mean

async def myapp(scope, receive, send) -> None:
    path = scope['path']
    if path == "/factorial":
        query_str = scope['query_string'].decode('utf-8')
        n = query_str.lstrip('n=')
        if await validate_and_process_number(n, send):
            res = factorial(int(n))
            print(res)
    elif path.startswith("/fibonacci/"):
        n = path.lstrip("/fibonacci/")
        if await validate_and_process_number(n, send):
            res = fibonacci(int(n))
    elif path == "/mean":
        req = await receive()
        body = req["body"].decode('utf-8')
        if await validate_and_process_array(body, send):
            res = mean(json.loads(body))
    else:
        await send_ans(404, b'not found', 'text/plain', send)
        
    await send_ans(200, res.encode('utf-8'), "application/json", send)
    return

async def validate_and_process_number(value, send) -> bool:
    try:
        value = int(value)
        if value < 0:
            await send_ans(400, b'Bad Request: number must be greater than 0', 'text/plain', send)
            return False
    except ValueError:
        await send_ans(422, b'Unprocessable Entity: invalid number', 'text/plain', send)
        return False
    return True

async def validate_and_process_array(body, send) -> bool:
    try:
        data = json.loads(body)
        if not isinstance(data, list) or not all(isinstance(element, (float, int)) for element in data):
            await send_ans(422, b'Unprocessable Entity: all elements must be floats', 'text/plain', send)
            return False
        if len(data) == 0:
            await send_ans(400, b'Bad Request: array cannot be empty', 'text/plain', send)
            return False
    except (ValueError, json.JSONDecodeError):
        await send_ans(422, b'Unprocessable Entity: invalid JSON', 'text/plain', send)
        return False
    return True


async def send_ans(status, body, content_type, send) -> None:
    await send({
        'type': 'http.response.start',
        'status': status,
        'headers': [(b'content-type', content_type)],
    })

    
    await send({
        "type": "http.response.body",
        "body": body,
    })
