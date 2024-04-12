import tkinter as tk
from tkinter import ttk
import sqlite3


# Класс Main
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

# Главное окно
    def init_main(self):
        toolbar = tk.Frame(bg='blue violet', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='add.png')
        btn_open_dialog = tk.Button(toolbar, text='Добавить спортсмена ', command=self.open_dialog, bg='blue violet',
                                    bd=0, compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='edit.png')
        btn_edit_dialog = tk.Button(toolbar, text='Редактировать', bg='blueviolet', bd=0, image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='delete.png')
        btn_delete_dialog = tk.Button(toolbar, text='Удалить', bg='blueviolet', bd=0, image=self.delete_img,
                                      compound=tk.TOP, command=self.delete_records)
        btn_delete_dialog.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file='search.png')
        btn_search = tk.Button(toolbar, text='Поиск', bg='blueviolet', bd=0, image=self.search_img,
                               compound=tk.TOP, command=self.open_search_dialog)

        btn_search.pack(side=tk.LEFT)


        self.refresh_img = tk.PhotoImage(file='refresh.png')
        btn_refresh = tk.Button(toolbar, text='Обновить', bg='blueviolet', bd=0, image=self.refresh_img,
                                compound=tk.TOP, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('ID', 'sportsman', 'gym', 'team'), height=15, show='headings')

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('sportsman', width=355, anchor=tk.CENTER)
        self.tree.column('gym', width=100, anchor=tk.CENTER)
        self.tree.column('team', width=150, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('sportsman', text='Спортсмен')
        self.tree.heading('gym', text='Лига')
        self.tree.heading('team', text='Команда')

        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

# Добавление данных
    def records(self, sportsman, gym, team):
        self.db.insert_data(sportsman, gym, team)
        self.view_records()

# Обновление данных
    def update_record(self, sportsman, gym, team):
        self.db.c.execute('''UPDATE athletes SET sportsman=?, league=?, team=? WHERE ID=?''',
                          (sportsman, gym, team, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

# Вывод данных
    def view_records(self):
        self.db.c.execute('''SELECT * FROM athletes''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

# Удаление данных
    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM athletes WHERE id=? ''', (self.tree.set(selection_item, '#1'),))
            self.db.conn.commit()
            self.view_records()

# Поиск данных
    def search_records(self, team):
        team = ('%' + team + '%',)
        self.db.c.execute('''SELECT * FROM athletes WHERE team LIKE ?''', team)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

# Открытие дочернего окна
    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()

    def open_search_dialog(self):
        Search()


# Дочернее окно
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить спортсмена')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        label_sportsman = tk.Label(self, text='Спортсмен')
        label_sportsman.place(x=50, y=50)

        label_select = tk.Label(self, text='Тренажерный зал')
        label_select.place(x=50, y=80)

        label_team = tk.Label(self, text='Команда')
        label_team.place(x=50, y=110)

        self.entry_sportsman = ttk.Entry(self)
        self.entry_sportsman.place(x=200, y=50)

        self.entry_team = ttk.Entry(self)
        self.entry_team.place(x=200, y=110)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=150)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=150)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_sportsman.get(),
                                                                       self.combobox.get(),
                                                                       self.entry_team.get()))

        self.grab_set()
        self.focus_set()


# Класс обновления унаследованный от дочернего окна
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()


    def init_edit(self):
        self.title('Редактировать спортсмена')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=150)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_sportsman.get(),
                                                                          self.combobox.get(),
                                                                          self.entry_team.get()))
        self.btn_ok.destroy()


    def default_data(self):
        self.db.c.execute('''SELECT * FROM athletes WHERE id=?''',
                          (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_sportsman.insert(0, row[1])
        if row[2] != 'Спартак':
            self.combobox.current(1)
        self.entry_team.insert(0, row[3])


# Поиск по спортсмену
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100+400+300')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


# Создание базы данных
class DB:
    def __init__(self):
        self.conn = sqlite3.connect('athletes.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS athletes (id integer primary key, sportsman text, 
            league text, team text)''')
        self.conn.commit()

    def insert_data(self, sportsman, league, team):
        self.c.execute('''INSERT INTO athletes (sportsman, league, team) VALUES (?, ?, ?) ''',
                       (sportsman, league, team))
        self.conn.commit()


# Основной код для запуска
if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Athletes")
    root.geometry("665x450+300+200")
    root.resizable(False, False)
    root.mainloop()

