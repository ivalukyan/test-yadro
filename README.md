# Test Yadro

FastAPI-приложение для работы с графовыми структурами и их визуализацией/обработкой через REST API.  
Проект использует PostgreSQL, Docker и имеет покрытие тестами через `pytest`.

## 📦 Стек технологий

- Python 3.10
- FastAPI
- PostgreSQL13
- Docker + Docker Compose
- Pytest

## 🚀 Установка и запуск

### 1. Клонировать репозиторий

```bash
git https://github.com/ivalukyan/test-yadro.git
cd test-yadro
```

### 2. Запуск приложения
```bash
docker-compose up -d --build
```


### Tests
```bash
python -m pytest tests/ -v --cov=.
```

### Структура проекта
```
├── src/
│   ├── backend/           # Логика FastAPI-приложения
│   │   ├── main.py
│   │   ├── routers/
│   │   │   └── router_grafs.py   # Основные роуты для работы с графами
│   │   └── schemas/
│   └── database/          # Работа с БД
│       ├── engine.py
│       ├── models.py
│       └── utils.py
├── tests/                 # Тесты на Pytest
│   ├── tests_backend/
│   │   ├── test_routers_graphs.py  # Тесты для роутеров
│   └── tests_database/
├── docker-compose.yml     # Конфигурация для Docker
├── LICENSE                # Лицензия проекта
└── README.md              # Документация проекта
```