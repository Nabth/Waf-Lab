# WAF Lab

Лабораторный стенд для исследования ложных срабатываний (False Positives) WAF и отработки механик тюнинга.

## Архитектура
- **WAF**: OWASP Coraza + OWASP CRS 4.x (через Caddy)
- **Уязвимое приложение**: OWASP Juice Shop

## Запуск
```bash
docker compose up -d
```

Интерфейс доступен по адресу: http://<IP-адрес-ВМ>:8080
