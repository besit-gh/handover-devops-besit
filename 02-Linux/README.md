# Linux

**Назначение:** Администрирование, диагностика, хранение, сеть, безопасность и автоматизация.

## Предварительные знания
Foundations.

## План курса
1. Файловая система и утилиты
2. Пользователи, группы и права
3. ACL, umask и sudo
4. Процессы, сигналы и /proc
5. systemd и journalctl
6. Пакеты и обновления
7. Сеть и сокеты
8. Диски, mount, fstab и swap
9. CPU, память и inode
10. SSH и hardening
11. cron и timers
12. Проект сопровождения

## Критерий готовности
Уметь объяснить основные механизмы, выполнить типовые операции, проверить результат, диагностировать характерные ошибки и безопасно описать изменения. Практические навыки закрепляются лабораторными заданиями.

## Навигация
- [Путь обучения](../00-Roadmap/learning-path.md)
- [Карта зависимостей](../00-Roadmap/dependency-map.md)
- [Стандарт уроков](../00-Roadmap/lesson-standard.md)
- [Сквозные проекты](../90-Capstone-Projects/README.md)
- [Лаборатории и инциденты](../91-Labs-Incidents/README.md)

> **Статус:** план курса зафиксирован. Подробные уроки наполняются последовательно по стандарту. Первый полный образец — [Программа, процесс и поток](../01-Foundations/03-Program-process-thread.md).

## Дополнительный практический урок
- [Процессы, systemd и журналы](./03-Processes-systemd-and-journal.md)

## Дополнительные уроки
- [Пользователи, группы и права: практическая диагностика](./04-Users-groups-and-permissions.md)
- [Интерактивная лаборатория: права доступа Linux](https://besit-gh.github.io/handover-devops-besit/web-lessons/linux-permissions/) — матрица rwx, калькулятор chmod, виртуальный терминал, блок-схемы, ACL и тест.
- [Процессы и сигналы](./05-Processes-and-signals.md)

## Публикация интерактивного урока
Исходная страница находится в [`web-lessons/linux-permissions/index.html`](../web-lessons/linux-permissions/index.html) и запускается локально без сборки и внешних библиотек. После публикации доступны оба адреса: корень сайта — https://besit-gh.github.io/handover-devops-besit/ и прямой путь урока — https://besit-gh.github.io/handover-devops-besit/web-lessons/linux-permissions/. Workflow [linux-permissions-pages.yml](../.github/workflows/linux-permissions-pages.yml) теперь помещает копию урока и в корень, и в исходный путь, чтобы обе ссылки работали. Публикация запускается автоматически при изменениях в ветке `features`; в настройках репозитория источник GitHub Pages должен быть **GitHub Actions**.
