import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from .task import Task
from .storage_manager import StorageManager
from .task_manager import TaskManager # Импортируем TaskManager

class Interface:
    def __init__(self, root, task_manager):
        self.root = root
        self.root.title("Менеджер задач v0.2.0")
        self.task_manager = task_manager # Получаем экземпляр TaskManager

        self.tasks_frame = None
        self.task_widgets = {} # Словарь для хранения виджетов задач {task_id: (frame, title_label, ...)}

        self._build_ui()
        self.update_task_display()

    def _build_ui(self):
        """Создает основной интерфейс приложения."""
        # Основная рамка для кнопок управления
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(pady=10, fill=tk.X)

        ttk.Button(control_frame, text="Добавить задачу", command=self.add_task_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Обновить", command=self.update_task_display).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Выход", command=self.root.quit).pack(side=tk.RIGHT, padx=5)

        # Рамка для отображения списка задач
        self.tasks_frame = ttk.Frame(self.root, padding="10")
        self.tasks_frame.pack(fill=tk.BOTH, expand=True)

        # Заголовок для списка задач
        header_frame = ttk.Frame(self.tasks_frame)
        header_frame.pack(fill=tk.X)
        ttk.Label(header_frame, text="ID", width=10, anchor='w', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        ttk.Label(header_frame, text="Название", width=30, anchor='w', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        ttk.Label(header_frame, text="Статус", width=15, anchor='w', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        ttk.Label(header_frame, text="Действия", width=20, anchor='w', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)

    def update_task_display(self):
        """Очищает текущий список задач и отображает актуальный список."""
        # Удаляем все предыдущие виджеты задач
        for widget in self.tasks_frame.winfo_children():
            if widget.winfo_class() != "TFrame" or widget == self.tasks_frame.winfo_children()[0]: # Оставляем заголовок
                 continue
            widget.destroy()
        self.task_widgets.clear() # Очищаем словарь виджетов

        # Получаем все задачи из TaskManager
        tasks = self.task_manager.get_all_tasks()

        # Отображаем каждую задачу
        for task in tasks:
            task_frame = ttk.Frame(self.tasks_frame, relief=tk.GROOVE, borderwidth=1)
            task_frame.pack(fill=tk.X, pady=2)

            # Отображаем информацию о задаче
            ttk.Label(task_frame, text=task.id[:8]+"...", width=10, anchor='w').pack(side=tk.LEFT, padx=5) # Обрезаем ID для краткости
            ttk.Label(task_frame, text=task.title, width=30, anchor='w').pack(side=tk.LEFT, padx=5)
            ttk.Label(task_frame, text=task.status, width=15, anchor='w').pack(side=tk.LEFT, padx=5)

            # Кнопки действий
            actions_frame = ttk.Frame(task_frame)
            actions_frame.pack(side=tk.LEFT, padx=5)

            ttk.Button(actions_frame, text="Изменить", command=lambda t=task: self.edit_task_dialog(t)).pack(side=tk.LEFT, padx=2)
            ttk.Button(actions_frame, text="Удалить", command=lambda t=task: self.delete_task_confirm(t)).pack(side=tk.LEFT, padx=2)
            ttk.Button(actions_frame, text="В работе", command=lambda t=task: self.toggle_status(t, "in_progress")).pack(side=tk.LEFT, padx=2)
            ttk.Button(actions_frame, text="Готово", command=lambda t=task: self.toggle_status(t, "done")).pack(side=tk.LEFT, padx=2)

            self.task_widgets[task.id] = task_frame # Сохраняем виджет для возможного дальнейшего использования

    def add_task_dialog(self):
        """Открывает диалоговое окно для добавления новой задачи."""
        title = simpledialog.askstring("Добавить задачу", "Название задачи:")
        if title:
            description = simpledialog.askstring("Добавить задачу", "Описание задачи:")
            author = simpledialog.askstring("Добавить задачу", "Автор (по умолчанию 'Unknown'):", initialvalue="Unknown")
            if description is not None and author is not None: # Проверяем, что пользователь не нажал "Отмена"
                self.task_manager.create_task(title=title, description=description, author=author)
                self.update_task_display()

    def edit_task_dialog(self, task):
        """Открывает диалоговое окно для редактирования задачи."""
        new_title = simpledialog.askstring("Редактировать задачу", "Новое название:", initialvalue=task.title)
        if new_title is None: return # Пользователь нажал "Отмена"

        new_description = simpledialog.askstring("Редактировать задачу", "Новое описание:", initialvalue=task.description)
        if new_description is None: return

        new_author = simpledialog.askstring("Редактировать задачу", "Новый автор:", initialvalue=task.author)
        if new_author is None: return

        # Обновляем задачу через TaskManager
        self.task_manager.edit_task(
            task_id=task.id,
            title=new_title,
            description=new_description,
            author=new_author
        )
        self.update_task_display()

    def delete_task_confirm(self, task):
        """Запрашивает подтверждение перед удалением задачи."""
        if messagebox.askyesno("Подтверждение удаления", f"Вы уверены, что хотите удалить задачу '{task.title}'?"):
            self.task_manager.delete_task(task.id)
            self.update_task_display()

    def toggle_status(self, task, new_status):
        """Меняет статус задачи (например, с 'todo' на 'in_progress' или 'done')."""
        self.task_manager.toggle_status(task.id, new_status)
        self.update_task_display()

    def ask_confirm(self, message):
        """Показывает диалоговое окно с вопросом (например, для подтверждения выхода)."""
        return messagebox.askyesno("Подтверждение", message)
