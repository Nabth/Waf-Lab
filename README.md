# WAF Lab (OWASP Coraza + Juice Shop)

Лабораторный стенд для исследования и устранения ложных срабатываний (False Positives) WAF на современных SPA-приложениях.

## Проблема
Современные Single Page Applications (SPA) и REST API генерируют трафик, который стандартные правила OWASP CRS (Paranoia Level 1) ошибочно принимают за атаки. В результате WAF блокирует легитимные запросы (например, WebSockets или названия API-методов), ломая бизнес-логику.

## Архитектура
- **WAF**: OWASP Coraza + OWASP CRS (через Caddy)
- **Мишень**: OWASP Juice Shop (уязвимое SPA)
- **Эмулятор**: Playwright (имитация действий реального пользователя)

## Кейсы ложных срабатываний (в этом репозитории)
1. **Socket.IO (WebSockets)**: WAF блокирует `POST /socket.io/` из-за `Content-Type: text/plain` (правило `920420`).
2. **REST API Endpoint `whoami`**: WAF блокирует `GET /rest/user/whoami` из-за совпадения имени эндпоинта с Unix-командой `whoami` (правило `932260` RCE).

## Решение
Вместо глобального отключения правил (`SecRuleRemoveById`) используются точечные исключения (`ctl:ruleRemoveTargetById`), которые отключают проверку конкретного параметра только для конкретного URL-адреса.

## Как запустить
1. Клонируйте репозиторий.
2. Запустите стенд:
   ```bash
   docker compose up -d
   ```
   Доступен по адресу: http://localhost:8080

## Как воспроизвести исследование
1. Установите Playwright: pip install playwright && playwright install chromium
2. Запустите эмулятор пользователя: python emulation/user_emulator.py
3. Проверьте логи WAF на наличие блокировок: grep '"is_interrupted":true' logs/audit.log

