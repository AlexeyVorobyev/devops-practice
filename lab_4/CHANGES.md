# Изменения в ЛР4 относительно ЛР3

- База `Airflow + Spark` перенесена из `lab_3` в отдельную директорию `lab_4`.
- В `lab_4` добавлен observability-стек из `Loki`, `Alloy`, `Prometheus` и `Grafana`.
- Логи Airflow собираются через `Alloy` и отправляются в `Loki`.
- Метрики Airflow экспортируются через `statsd-exporter`, затем собираются в `Prometheus` и отображаются в `Grafana`.
- Datasource и dashboard `Grafana`, а также connection `spark_local`, настраиваются автоматически через код.
