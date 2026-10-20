# Карта зависимостей

- Foundations → Linux, Networking, Bash, Git.
- Linux + Networking → HTTP, DNS, TLS-PKI, Nginx.
- Git + GitHub + Testing + Docker → CI/CD.
- Linux + SSH + YAML → Ansible.
- Сети + Cloud + Git → Terraform.
- Docker + YAML + Networking + Linux → Kubernetes; Kubernetes + YAML → Helm.
- Метрики → Prometheus → Grafana → SRE.
- JSON + HTTP + логи → Elasticsearch, Logstash, Kibana; Fluent Bit и Loki изучаются как отдельные лог-пайплайны.
- Identity + TLS + политики доступа → Vault.
- Production Operations связывает изменения, инциденты, восстановление и handover; SRE фокусируется на измерении и улучшении надёжности.

## Правила разделения

HTTP, DNS и TLS-PKI имеют отдельные курсы. Testing описывает общие принципы, а инструментальные особенности — соответствующие курсы. GitHub раскрывает платформу, CI/CD — общие принципы доставки. Security задаёт сквозные принципы, а конкретные настройки описываются в курсах технологий.
