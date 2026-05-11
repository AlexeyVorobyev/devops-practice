import pathlib
import unittest


class Lab4BootstrapTests(unittest.TestCase):
    def test_lab4_contains_expected_baseline_files(self):
        expected_paths = [
            "lab_4/.gitignore",
            "lab_4/Dockerfile",
            "lab_4/README.md",
            "lab_4/docker-compose.yml",
            "lab_4/dags/compute_metrics_spark_dag.py",
            "lab_4/spark/compute_metrics_spark.py",
            "lab_4/tests/test_lab4_observability.py",
            "lab_4/lab4.pdf",
        ]

        for path in expected_paths:
            with self.subTest(path=path):
                self.assertTrue(pathlib.Path(path).exists(), path)

    def test_lab4_does_not_keep_lab3_pdf(self):
        self.assertFalse(pathlib.Path("lab_4/lab3.pdf").exists())


class Lab4DocumentationTests(unittest.TestCase):
    def test_readme_mentions_observability_services_and_automatic_setup(self):
        readme = pathlib.Path("lab_4/README.md").read_text(encoding="utf-8")

        self.assertIn("Loki", readme)
        self.assertIn("Alloy", readme)
        self.assertIn("Prometheus", readme)
        self.assertIn("Grafana", readme)
        self.assertIn("spark_local", readme)
        self.assertIn("создается автоматически", readme)

    def test_changes_file_mentions_lab4_delta_from_lab3(self):
        changes = pathlib.Path("lab_4/CHANGES.md").read_text(encoding="utf-8")

        self.assertIn("lab_4", changes)
        self.assertIn("lab_3", changes)
        self.assertIn("Grafana", changes)
        self.assertIn("Prometheus", changes)
        self.assertIn("Loki", changes)

    def test_local_agents_mentions_lab4_observability_files(self):
        agents = pathlib.Path("lab_4/AGENTS.md").read_text(encoding="utf-8")

        self.assertIn("lab_4", agents)
        self.assertIn("alloy.config", agents)
        self.assertIn("prometheus.yml", agents)
        self.assertIn("grafana", agents)

    def test_root_agents_mentions_lab4_structure(self):
        root_agents = pathlib.Path("AGENTS.md").read_text(encoding="utf-8")

        self.assertIn("lab_4/", root_agents)
        self.assertIn("lab_4/dags/", root_agents)
        self.assertIn("lab_4/spark/", root_agents)
        self.assertIn("lab_4/tests/", root_agents)


class Lab4ComposeTests(unittest.TestCase):
    def test_compose_contains_observability_services(self):
        compose = pathlib.Path("lab_4/docker-compose.yml").read_text(encoding="utf-8")

        self.assertIn("loki:", compose)
        self.assertIn("alloy:", compose)
        self.assertIn("prometheus:", compose)
        self.assertIn("grafana:", compose)
        self.assertIn("statsd-exporter:", compose)

    def test_compose_automates_airflow_connection_and_logs_permissions(self):
        compose = pathlib.Path("lab_4/docker-compose.yml").read_text(encoding="utf-8")

        self.assertIn("AIRFLOW_CONN_SPARK_LOCAL", compose)
        self.assertIn("spark://spark-master:7077", compose)
        self.assertIn("AIRFLOW__METRICS__STATSD_ON", compose)
        self.assertIn("AIRFLOW__METRICS__STATSD_HOST", compose)
        self.assertIn("AIRFLOW__METRICS__STATSD_PORT", compose)
        self.assertIn('user: "0:0"', compose)
        self.assertIn("chmod -R 777 /opt/airflow/logs", compose)
        self.assertIn("airflow dags unpause compute_metrics_spark", compose)
        self.assertIn("su -s /bin/bash airflow -c", compose)

    def test_alloy_and_prometheus_configs_exist(self):
        alloy = pathlib.Path("lab_4/alloy.config").read_text(encoding="utf-8")
        prometheus = pathlib.Path("lab_4/prometheus.yml").read_text(encoding="utf-8")

        self.assertIn("/opt/logs/dag_id=*/run_id=*/task_id=*/*.log", alloy)
        self.assertIn("http://loki:3100/loki/api/v1/push", alloy)
        self.assertIn("job_name: 'airflow'", prometheus)
        self.assertIn("statsd-exporter:9102", prometheus)


class Lab4GrafanaProvisioningTests(unittest.TestCase):
    def test_datasource_provisioning_contains_loki_and_prometheus(self):
        datasources = pathlib.Path(
            "lab_4/grafana/provisioning/datasources/datasources.yml"
        ).read_text(encoding="utf-8")

        self.assertIn("name: Loki", datasources)
        self.assertIn("uid: loki", datasources)
        self.assertIn("http://loki:3100", datasources)
        self.assertIn("name: Prometheus", datasources)
        self.assertIn("uid: prometheus", datasources)
        self.assertIn("http://prometheus:9090", datasources)

    def test_dashboard_provisioning_points_to_dashboard_directory(self):
        dashboards = pathlib.Path(
            "lab_4/grafana/provisioning/dashboards/dashboards.yml"
        ).read_text(encoding="utf-8")

        self.assertIn("lab4-dashboards", dashboards)
        self.assertIn("/etc/grafana/dashboards", dashboards)
        self.assertIn("Lab 4", dashboards)

    def test_dashboard_json_contains_logs_and_metrics_panels(self):
        dashboard = pathlib.Path(
            "lab_4/grafana/dashboards/lab4-overview.json"
        ).read_text(encoding="utf-8")

        self.assertIn("Lab 4 Overview", dashboard)
        self.assertIn("Airflow Logs", dashboard)
        self.assertIn("Airflow Up", dashboard)
        self.assertIn("Scheduler Heartbeats", dashboard)
        self.assertIn('{job=\\"airflow_logs\\"}', dashboard)
        self.assertIn('up{job=\\"airflow\\"}', dashboard)
        self.assertIn('airflow_scheduler_heartbeat_total', dashboard)


class Lab4DagAutomationTests(unittest.TestCase):
    def test_dag_is_unpaused_on_creation(self):
        dag = pathlib.Path("lab_4/dags/compute_metrics_spark_dag.py").read_text(
            encoding="utf-8"
        )

        self.assertIn("is_paused_upon_creation=False", dag)


if __name__ == "__main__":
    unittest.main()
