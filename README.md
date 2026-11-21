## Классы

1.  **`Task`**:
    *   Представляет собой отдельную задачу.
    *   Поля: `id`, `title`, `description`, `status`, `author`, `created_at`.
    *   Методы: `to_dict()` (для сохранения), `from_dict()` (для загрузки).

2.  **`StorageManager`**:
    *   Отвечает за загрузку и сохранение задач в файл `data/tasks.json`.
    *   Методы: `load_tasks()`, `save_tasks()`, `add_task()`, `get_all_tasks()`, `get_task_by_id()`, `update_task()`, `delete_task()`.

3.  **`Interface`**:
    *   Реализует графический пользовательский интерфейс с использованием Tkinter.
    *   Обеспечивает взаимодействие с пользователем: отображение задач, добавление, редактирование, удаление, изменение статуса.
    *   Методы: `_build_ui()`, `update_task_display()`, `add_task_dialog()`, `edit_task_dialog()`, `delete_task_confirm()`, `toggle_status()`, `ask_confirm()`.

4.  **`TaskManager`**:
    *   Фасад приложения, который связывает `StorageManager` и `Interface`.
    *   Предоставляет высокоуровневые методы для управления задачами (CRUD).
    *   Методы: `create_task()`, `edit_task()`, `delete_task()`, `toggle_status()`, `get_all_tasks()`, `get_task_by_id()`, `run()`.

## Порядок работы

1.  **`src/task.py`**: Реализация класса `Task` с полями и методами `to_dict()` / `from_dict()`.
2.  **`src/storage_manager.py`**: Реализация класса `StorageManager` для работы с JSON файлом (`load`, `save`, `add`, `update`, `delete`).
3.  **`src/interface.py`**: Реализация класса `Interface` как прослойки к Tkinter, с методами `build`, `get_input`, `show_tasks`, `ask_confirm`.
4.  **`src/task_manager.py`**: Реализация класса `TaskManager` как фасада с CRUD-методами и методом `run()` для запуска приложения.
5.  **`main.py`**: Создание экземпляров `TaskManager` и `Interface`, запуск главного цикла Tkinter.
6.  **Проверка**: Перезапустите приложение, чтобы убедиться, что данные сохраняются и загружаются корректно.

## Как запустить

1.  Клонируйте репозиторий (если он будет на GitHub).
2.  Перейдите в корневую директорию проекта.
3.  Установите зависимости (если они есть, в данном случае `requirements.txt` пуст).
4.  Запустите приложение:
    ```bash
    python main.py
    ```
5.  Откроется графический интерфейс менеджера задач.

## Лицензия

Этот проект распространяется под лицензией MIT. Смотрите файл `LICENSE` для получения подробной информации.

