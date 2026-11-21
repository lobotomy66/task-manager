import datetime
import uuid

class Task:
    def __init__(self, title, description, status="todo", author="Unknown", created_at=None):
        self.id = str(uuid.uuid4()) # Генерируем уникальный ID
        self.title = title
        self.description = description
        self.status = status # Возможные статусы: "todo", "in_progress", "done"
        self.author = author
        self.created_at = created_at if created_at else datetime.datetime.now()

    def to_dict(self):
        """Преобразует объект Task в словарь для сохранения."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "author": self.author,
            "created_at": self.created_at.isoformat() # Сохраняем дату как строку
        }

    @staticmethod
    def from_dict(data):
        """Создает объект Task из словаря (например, при загрузке из JSON)."""
        task = Task(
            title=data["title"],
            description=data["description"],
            status=data.get("status", "todo"), # По умолчанию "todo", если нет в данных
            author=data.get("author", "Unknown"), # По умолчанию "Unknown"
            created_at=datetime.datetime.fromisoformat(data["created_at"]) # Преобразуем строку обратно в datetime
        )
        task.id = data["id"] # Устанавливаем ID из данных
        return task

    def __repr__(self):
        return f"Task(id='{self.id}', title='{self.title}', status='{self.status}')"
