# Импортируем модуль trinter
import tkinter as tk
from tkinter import ttk
import sqlite3

# Создаём класс главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

# Пропишем метод для хранения и инициализации объектов графического интерфейса
    def init_main(self):
        toolbar = tk.Frame(bg="#d7d8e0", bd=2) # Панель интструментов
        toolbar.pack(side=tk.TOP, fill=tk.X) # Добавляем toolbar на главное окно
        self.add_img = tk.PhotoImage(file="./img/add.png") # Достали и зафиксировали иконку
        btn_open_dialog = tk.Button(
            toolbar, bg="#d7d8e0", bd=0, image=self.add_img, command=self.open_dialog
        ) # Кнопка добавления нового контакта на главное окно toolbar
        btn_open_dialog.pack(side=tk.LEFT)

# Создание таблиц, вызываем метод Treeview
        self.tree = ttk.Treeview(
            self, columns=("ID", "name", "tel", "email"), height=45, show="headings"
        ) # Вызываем параметр columns и в этом параметре кортежем передаём поля которые будут у таблицы, после задаём высоту и пропишем параметр show

# Добавляем параметры к нашим колонкам, обращаемся к табличке tree и вызываем метод column
# Указываем колонки, прописываем для неё ширину и выравнивание текста в ячейки
        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("name", width=300, anchor=tk.CENTER)
        self.tree.column("tel", width=150, anchor=tk.CENTER)
        self.tree.column("email", width=150, anchor=tk.CENTER)

# Задаём нашим колонкам удобочитаемые названия то есть добавим подписи к колонкам
# Вызываем метод heading
        self.tree.heading("ID", text="ID")
        self.tree.heading("name", text="ФИО")
        self.tree.heading("tel", text="Телефон")
        self.tree.heading("email", text="E-mail")

# Добавим всё это на наше главное окно
        self.tree.pack(side=tk.LEFT)

# Создаём кнопку на обновление
        self.update_img = tk.PhotoImage(file="./img/update.png") # Выбираем иконку
        btn_edit_dialog = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.update_img,
            command=self.open_update_dialog,
        )
        btn_edit_dialog.pack(side=tk.LEFT)

# Создаём кнопку на удаление
        self.delete_img = tk.PhotoImage(file="./img/delete.png")
        btn_delete = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.delete_img,
            command=self.delete_records,
        )
        btn_delete.pack(side=tk.LEFT)

# Создаём кнопку поиска
        self.search_img = tk.PhotoImage(file="./img/search.png")
        btn_search = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.search_img,
            command=self.open_search_dialog,
        )
        btn_search.pack(side=tk.LEFT)

# Кнопка обновления
        self.refresh_img = tk.PhotoImage(file="./img/refresh.png")
        btn_refresh = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.refresh_img,
            command=self.open_search_dialog,
        )
        btn_refresh.pack(side=tk.LEFT)

# Добавим новый метод, который будет отвечать за вызоз дочернего окна
    def open_dialog(self):
        Child()

# Добавим метод, который будет вызывать метод записи в базу данных
    def records(self, name, tel, email):
        self.db.insert_data(name, tel, email)
        self.view_records() # Атрибут view

# Создаём метод view_records
    def view_records(self):
        self.db.cursor.execute("SELECT * FROM db") # Запрос
        [self.tree.delete(i) for i in self.tree.get_children()] # Удаляем из виджета таблицы всё старое, вызываем метод delete
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()] # Добавляем новую информацию из базы данных

# Метод для открытия окна
    def open_update_dialog(self):
        Update()

# Создаём редактирование данных, добавляем метод update_records
    def update_records(self, name, tel, email):
        self.db.cursor.execute(
            """UPDATE db SET name=?, tel=?, email=? WHERE id=?""",
            (name, tel, email, self.tree.set(self.tree.selection()[0], "#1")),
        ) # Запрос на изменение бд
        self.db.conn.commit()
        self.view_records()

# Создаём метод на удаление
    def delete_records(self):
        for selection_items in self.tree.selection():
            self.db.cursor.execute(
                "DELETE FROM db WHERE id=?", (self.tree.set(selection_items, "#1"))
            ) # Запрос на удаление из базы данных этой записи
        self.db.conn.commit()
        self.view_records()

    def open_search_dialog(self):
        Search()


# Создадим метод, который будет искать записи в бд по имени, будет очищать таблицу главного окна и добавлять на неё строки из выбранных запросов
    def search_records(self, name):
        name = "%" + name + "%"
        self.db.cursor.execute("SELECT * FROM db WHERE name LIKE ?", (name,)) #сюда передаем кортеж (name), а не просто name

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()]


# Создаём класс дочернего окна
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

# Пропишем метод для хранения и инициализации объектов графического интерфейса
    def init_child(self):
        self.title("Добавить") # Заголовок
        self.geometry("400x220") # Размеры окна
        self.resizable(False, False) # Ограничение изменения размеров окна

        self.grab_set() # Метод grab_set
        self.focus_set() # Захватываем focus

# Создадим форму ввода данных для нашего дочернего окна
        label_name = tk.Label(self, text="ФИО:")
        label_name.place(x=50, y=50)
        label_select = tk.Label(self, text="Телефон:")
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text="E-mail:")
        label_sum.place(x=50, y=110)

# Строки для ввода
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=80)
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=110)

# Кнопка для закрытия дочернего окна
        self.btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        self.btn_cancel.place(x=220, y=170)

# Кнопка для добавления дочернего окна
        self.btn_ok = ttk.Button(self, text="Добавить")
        self.btn_ok.place(x=300, y=170)

# Отслеживаем щелчок по кнопке
        self.btn_ok.bind(
            "<Button-1>",
            lambda event: self.view.records(
                self.entry_name.get(), self.entry_email.get(), self.entry_tel.get()
            ),
        )


# Создаём класс Update
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

# Создадим метод, который будет отвечать за хранение и инициализацию объектов нашего интерфейса
    def init_update(self):
        self.title("Редактирование контакта") # Название
        btn_edit = ttk.Button(self, text="Редактировать") # Кнопка для редактирования
        btn_edit.place(x=205, y=170)
        btn_edit.bind(
            "<Button-1>",
            lambda event: self.view.update_records(
                self.entry_name.get(), self.entry_email.get(), self.entry_tel.get()
            ),
        ) # Отслеживание кнопки
        btn_edit.bind("<Button-1>", lambda event: self.destroy(), add="+")
        self.btn_ok.destroy()

# Создаём метод default_data
    def default_data(self):
        self.db.cursor.execute(
            "SELECT * FROM db WHERE id=?",
            self.view.tree.set(self.view.tree.selection()[0], "#1"),
        ) # Запрос 

        row = self.db.cursor.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_tel.insert(0, row[3])


# Создаём класс Search
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

# Создадим метод init 
    def init_search(self):
        self.title("Поиск контакта")
        self.geometry("300x100")
        self.resizable(False, False)

# Пропишем поле для поиска по имени
        label_search = tk.Label(self, text="Имя:")
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=100, y=20, width=150)

# Кнопка для закрытия
        btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy) #тут не должно быть скобок у self.destroy
        btn_cancel.place(x=185, y=50)

# Кнопка для поиска
        search_btn = ttk.Button(self, text="Найти")
        search_btn.place(x=105, y=50)
        search_btn.bind(
            "<Button-1>",
            lambda event: self.view.search_records(self.entry_search.get()),
        )
        search_btn.bind("<Button-1>", lambda event: self.destroy(), add="+")


# Создаём класс DB
class DB:
    def __init__(self):
        self.conn = sqlite3.connect("db.db") # Соединение с базой данных
        self.cursor = self.conn.cursor() # Объект класса cursor
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS db (
                id INTEGER PRIMARY KEY,
                name TEXT,
                tel TEXT,
                email TEXT
            )"""
        ) # Запрос на создание самой базы данных и на создание таблицы
        self.conn.commit()

# Метод для добавления данных в нашу базу данных
    def insert_data(self, name, tel, email):
        self.cursor.execute(
            """INSERT INTO db(name, tel, email) VALUES(?, ?, ?)""", (name, tel, email)
        )
        self.conn.commit()



# Создаём главное окно root
if __name__ == "__main__":
    root = tk.Tk()
    db = DB() # Экземпляр класса DB
    app = Main(root) # Объект класса Main
    app.pack() # Применяем метод pack
    root.title("Телефонная книга") # Заголовок главного окна
    root.geometry("665x450") # Размеры главного окна
    root.resizable(False, False) # Ограничение изменения размеров окна
    root.mainloop() # Прописываем цикл событий
