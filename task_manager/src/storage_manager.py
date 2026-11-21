import json
import os
from .task import Task # Импортируем класс Task из того же пакета

class StorageManager:
    def __init__(self, filepath="data/tasks.json"):
        self.filepath = filepath
        self.tasks = self._load_tasks() # Загружаем задачи при инициализации

    def _load_tasks(self):
        """Загружает задачи из JSON файла."""
        if not os.path.exists(self.filepath):
            return {} # Возвращаем пустой словарь, если файл не существует
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Преобразуем загруженные словари обратно в объекты Task
                tasks_dict = {task_id: Task.from_dict(task_data) for task_id, task_data in data.items()}
                return tasks_dict
        except (json.JSONDecodeError, FileNotFoundError):
            return {} # Возвращаем пустой словарь в случае ошибки чтения или пустого файла

    def _save_tasks(self):
        """Сохраняет текущее состояние задач в JSON файл."""
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                # Преобразуем объекты Task в словари перед сохранением
                tasks_data = {task_id: task.to_dict() for task_id, task in self.tasks.items()}
                json.dump(tasks_data, f, indent=4, ensure_ascii=False)
        except IOError:
            print(f"Ошибка: Не удалось сохранить задачи в файл {self.filepath}")

    def add_task(self, title, description, author="Unknown"):
        """Добавляет новую задачу."""
        new_task = Task(title=title, description=description, author=author)
        self.tasks[new_task.id] = new_task
        self._save_tasks()
        return new_task

    def get_all_tasks(self):
        """Возвращает все задачи."""
        return list(self.tasks.values())

    def get_task_by_id(self, task_id):
        """Возвращает задачу по её ID."""
        return self.tasks.get(task_id)

    def update_task(self, task_id, **kwargs):
        """Обновляет существующую задачу."""
        task = self.get_task_by_id(task_id)
        if task:
            for key, value in kwargs.items():
                if hasattr(task, key): # Проверяем, есть ли такой атрибут у объекта Task
                    setattr(task, key, value)
            self._save_tasks()
            return True
        return False

    def delete_task(self, task_id):
        """Удаляет задачу по её ID."""
        if task_id in self.tasks:
            del self.tasks[task_id]
            self._save_tasks()
            return True
        return False
