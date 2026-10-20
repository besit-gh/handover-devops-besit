# Python HTTP-клиент: таймауты и JSON

> Начальный → средний уровень · 40–50 минут · Требуются Python, HTTP и JSON.

Сетевой запрос должен иметь таймаут, проверять код ответа и отдельно обрабатывать ошибки транспорта и содержимого.

~~~python
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

request = Request(
    "https://example.com/",
    headers={"User-Agent": "devops-training/1.0"},
)

try:
    with urlopen(request, timeout=5) as response:
        status = response.status
        content_type = response.headers.get("Content-Type", "")
        body = response.read(4096)
except HTTPError as error:
    print(f"HTTP error: {error.code}")
except URLError as error:
    print(f"Transport error: {error.reason}")
else:
    print(f"HTTP status: {status}")
    print(f"Content-Type: {content_type}")
    print(f"Bytes read: {len(body)}")
~~~

Пример ограничивает объём читаемых данных, задаёт таймаут и различает HTTP-ошибку и транспортную. Для реального API проверяй ожидаемый статус, content type и структуру ответа; не считай любой ответ 2xx автоматически корректными данными.

## Практика
1. Проверь поведение на HTTP 404.
2. Объясни, почему таймаут нужен даже для внутреннего сервиса.
3. Не печатай в логи авторизационные заголовки и тела с персональными данными.

## Контрольные вопросы
1. Чем HTTPError отличается от URLError?
2. Почему ограничивать читаемый ответ полезно?
3. Почему запрос без таймаута может зависнуть надолго?
