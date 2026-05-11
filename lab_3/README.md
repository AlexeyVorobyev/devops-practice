# Лабораторная работа 3

Третья лабораторная строится на базе `lab_2`: мы сохраняем стек `Airflow + Spark`, но адаптируем CI/CD-часть задания под `GitHub Actions`.

## Что находится в директории

- `Dockerfile` — кастомный образ Airflow с Java и Spark-зависимостями.
- `docker-compose.yml` — конфигурация для `postgres`, `spark-master`, `spark-worker`, `airflow-init`, `airflow-webserver`, `airflow-scheduler`.
- `dags/compute_metrics_spark_dag.py` — DAG, отправляющий spark-job в Spark.
- `spark/compute_metrics_spark.py` — spark-job на `pyspark`.
- `CHANGES.md` — список отличий от ЛР2.

## Локальная проверка файлов

Из корня репозитория:

```bash
python3 -m py_compile lab_3/dags/compute_metrics_spark_dag.py lab_3/spark/compute_metrics_spark.py
```

## Как запустить сервисы локально

Перейти в директорию лабораторной:

```bash
cd lab_3
```

Поднять стек:

```bash
docker compose up -d
```

Проверить контейнеры:

```bash
docker compose ps
```

## Ручная настройка Airflow Connection

После запуска откройте `http://localhost:8081/`, затем создайте Connection:

- `Connection Id`: `spark_local`
- `Connection Type`: `Spark`
- `Host`: `spark://spark-master`
- `Port`: `7077`

## Адаптация под GitHub Actions

Вместо `GitLab CI` в этой лабораторной используется workflow `.github/workflows/lab_3.yml`.

- workflow реагирует только на изменения в `lab_3/**` и в самом workflow-файле;
- job `test` выполняется всегда при запуске workflow;
- job `build` не запускается автоматически для веток `feature/*`;
- job `deploy` выполняется только для `main`, `master`, `develop`;
- job `deploy` поднимает `docker compose up -d` только как временную проверку сценария запуска внутри CI, а затем показывает состояние через `docker compose ps`.

## Веб-интерфейсы

- Airflow UI: `http://localhost:8081/`
- Spark UI: `http://localhost:4041`
