# Лабораторная работа 2

Эта лабораторная подключает Airflow к Spark и запускает spark-job через `SparkSubmitOperator`.

## Что находится в директории

- `Dockerfile` — кастомный образ Airflow с Java и Spark-зависимостями.
- `docker-compose.yml` — конфигурация для `postgres`, `spark-master`, `spark-worker`, `airflow-init`, `airflow-webserver`, `airflow-scheduler`.
- `dags/compute_metrics_spark_dag.py` — DAG, отправляющий spark-job в Spark.
- `spark/compute_metrics_spark.py` — spark-job на `pyspark` и `SparkSession`.
- `CHANGES.md` — список отличий от ЛР1.

## Что делает DAG

DAG `compute_metrics_spark` запускает spark-job через `SparkSubmitOperator`. Сам spark-job:

1. создаёт SparkSession;
2. подготавливает набор чисел;
3. считает сумму, среднее и максимум средствами Spark;
4. выводит результат в лог;
5. завершает SparkSession.

## Локальная проверка файлов

Из корня репозитория:

```bash
python3 -m unittest lab_2/tests/test_lab2_structure.py -v
python3 -m py_compile lab_2/dags/compute_metrics_spark_dag.py lab_2/spark/compute_metrics_spark.py
```

## Как запустить сервисы

Перейти в директорию лабораторной:

```bash
cd lab_2
```

Поднять стек:

```bash
docker compose up -d
```

Проверить контейнеры:

```bash
docker ps
```

## Ручная настройка Airflow Connection

После запуска откройте `http://localhost:8080/`, затем создайте Connection:

- `Connection Id`: `spark_local`
- `Connection Type`: `Spark`
- `Host`: `spark://spark-master`
- `Port`: `7077`

Имя подключения должно совпадать с `conn_id`, указанным в DAG.

## Веб-интерфейсы

- Airflow UI: `http://localhost:8080/`
- Spark UI: `http://localhost:4040`

## Примечания

- Для запуска spark-job используются `apache-airflow-providers-apache-spark` и `pyspark`.
- `spark-master` доступен по `spark://spark-master:7077` внутри docker-сети.
