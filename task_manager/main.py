import tkinter as tk
from src.task_manager import TaskManager

if __name__ == "__main__":
    # Создаем экземпляр TaskManager
    # Он автоматически загрузит задачи из data/tasks.json при старте
    task_manager = TaskManager()

    # Создаем главное окно Tkinter
    root = tk.Tk()

    # Создаем экземпляр Interface, передавая ему главное окно и TaskManager
    # Interface будет управлять отображением и взаимодействием с пользователем
    from src.interface import Interface
    app_interface = Interface(root, task_manager)

    # Запускаем главный цикл Tkinter
    root.mainloop()
