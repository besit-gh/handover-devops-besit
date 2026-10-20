# Deployment, Service и rollout в Kubernetes

> Начальный уровень · 40–50 минут · Требуются архитектура Kubernetes и YAML.

Deployment управляет ReplicaSet и желаемым количеством реплик приложения. Service предоставляет стабильную сетевую точку доступа к подходящим Pod. Pod могут пересоздаваться, поэтому их IP не следует считать постоянным интерфейсом приложения.

## Перед изменением
Проверь текущий контекст и namespace:

~~~bash
kubectl config current-context
kubectl get deployments -A
kubectl get services -A
~~~

Не выполняй команды apply или rollout в неизвестном кластере. Начни с отдельного учебного namespace и манифестов, которые понимаешь.

## Rollout
При изменении шаблона Pod Deployment может выполнить постепенное обновление. После изменения проверь статус rollout, события и готовность реплик. Завершённый rollout — важный сигнал, но для проверки поведения сервиса нужны также smoke tests и пользовательские метрики.

## Диагностика
- Нет endpoints у Service: проверь selector и labels Pod.
- Pod не Ready: изучи describe, events и logs.
- ImagePullBackOff: проверь имя образа, tag и доступ к registry.
- Новая версия падает: сравни события и логи текущего и предыдущего контейнера.

## Контрольные вопросы
1. Почему Service не привязан к одному Pod IP?
2. Как selector связывает Service с Pod?
3. Какие проверки нужны после rollout?
