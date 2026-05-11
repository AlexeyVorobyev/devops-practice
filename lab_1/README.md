# Лабораторная работа 1

В этой директории находится простое выполнение задания по развертыванию Apache Airflow через `docker compose` с собственным DAG.

## Состав

- `Dockerfile` собирает кастомный образ на базе `apache/airflow:2.7.1`
- `docker-compose.yml` поднимает `postgres`, `airflow-init`, `airflow-webserver`, `airflow-scheduler`
- `dags/compute_metrics_dag.py` содержит пользовательский DAG
- `dags/compute_metrics_logic.py` содержит вычислительную логику DAG

## Что делает DAG

DAG `compute_metrics` состоит из нескольких шагов:

1. подготавливает список чисел;
2. считает сумму;
3. считает среднее значение;
4. считает максимальное число;
5. собирает итоговый отчет и пишет его в лог.

Это намеренно простой, но не тривиальный DAG: он состоит из нескольких тасков и выполняет небольшие вычисления.

## Локальная проверка Python-логики

Из корня репозитория:

```bash
python3 -m unittest lab_1/tests/test_compute_metrics_logic.py -v
```

## Как запустить Airflow

Перейти в директорию лабораторной:

```bash
cd lab_1
```

Собрать и запустить сервисы:

```bash
docker compose up -d
```

Проверить контейнеры:

```bash
docker ps
```

В нормальном состоянии должны быть контейнеры `postgres`, `airflow-webserver`, `airflow-scheduler`. Контейнер `airflow-init` выполнится и завершится после инициализации базы и создания пользователя.

## Доступ к интерфейсу

Airflow будет доступен по адресу:

```text
http://localhost:8080/
```

Логин и пароль по текущей конфигурации:

```text
airflow / airflow
```

## Примечания

- Example DAG отключены через `AIRFLOW__CORE__LOAD_EXAMPLES=false`
- Используется `LocalExecutor`
- `redis`, `airflow-worker`, `airflow-triggerer`, `airflow-cli`, `flower` не используются
