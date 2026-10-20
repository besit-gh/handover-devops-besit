# Nginx как reverse proxy

> Начальный уровень · 35–45 минут · Требуются Linux, HTTP и DNS.

Reverse proxy принимает запрос клиента и передаёт его upstream-сервису. Клиент обращается к публичной точке входа, а внутренний сервис может быть доступен только из внутренней сети.

~~~nginx
server {
    listen 8080;
    server_name _;
    location / {
        proxy_pass http://127.0.0.1:9000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
~~~

Это демонстрационный фрагмент, не готовая production-конфигурация. Перед применением проверь контекст, upstream, доступ, TLS, таймауты и доверенную цепочку прокси. Не доверяй клиентским X-Forwarded-For без корректной настройки доверенных прокси.

~~~bash
nginx -t
curl -i --max-time 5 http://127.0.0.1:8080/
~~~

nginx -t проверяет конфигурацию, но не доказывает, что upstream работает.

## Контрольные вопросы
1. Чем reverse proxy отличается от backend?
2. Для чего передают Host и X-Forwarded-For?
3. Почему nginx -t недостаточно для проверки доступности?
