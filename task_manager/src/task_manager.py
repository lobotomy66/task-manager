from .task import Task
from .storage_manager import StorageManager
from .interface import Interface
import datetime

class TaskManager:
    def __init__(self, storage_filepath="data/tasks.json"):
        self.storage_manager = StorageManager(filepath=storage_filepath)
        self.tasks = {} # Словарь для хранения задач {id: Task_object}
        self._load_tasks() # Загружаем задачи при инициализации

    def _load_tasks(self):
        """Загружает задачи из StorageManager."""
        loaded_tasks = self.storage_manager.get_all_tasks()
        for task in loaded_tasks:
            self.tasks[task.id] = task

    def create_task(self, title, description, author="Unknown"):
        """Создает новую задачу и сохраняет ее."""
        if not title: # Простая валидация
            print("Ошибка: Название задачи не может быть пустым.")
            return None
        new_task = self.storage_manager.add_task(title=title, description=description, author=author)
        self.tasks[new_task.id] = new_task # Обновляем внутренний словарь
        return new_task

    def edit_task(self, task_id, title=None, description=None, status=None, author=None):
        """Редактирует существующую задачу."""
        task = self.tasks.get(task_id)
        if not task:
            print(f"Ошибка: Задача с ID {task_id} не найдена.")
            return False

        update_data = {}
        if title is not None: update_data['title'] = title
        if description is not None: update_data['description'] = description
        if status is not None: update_data['status'] = status
        if author is not None: update_data['author'] = author

        if self.storage_manager.update_task(task_id, **update_data):
            # Обновляем объект в памяти, если сохранение прошло успешно
            for key, value in update_data.items():
                setattr(task, key, value)
            return True
        return False

    def delete_task(self, task_id):
        """Удаляет задачу."""
        if self.storage_manager.delete_task(task_id):
            if task_id in self.tasks:
                del self.tasks[task_id]
            return True
        return False

    def toggle_status(self, task_id, new_status):
        """Меняет статус задачи."""
        task = self.tasks.get(task_id)
        if not task:
            print(f"Ошибка: Задача с ID {task_id} не найдена.")
            return False
        # Простая валидация статуса
        if new_status not in ["todo", "in_progress", "done"]:
            print(f"Ошибка: Недопустимый статус '{new_status}'.")
            return False

        return self.edit_task(task_id, status=new_status)

    def get_all_tasks(self):
        """Возвращает список всех задач."""
        return list(self.tasks.values())

    def get_task_by_id(self, task_id):
        """Возвращает задачу по ID."""
        return self.tasks.get(task_id)

    def run(self):
        """Запускает интерфейс приложения."""
        import tkinter as tk
        root = tk.Tk()
        # Передаем экземпляр TaskManager в Interface
        interface = Interface(root, self)
        root.mainloop()
