import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


def init_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE partners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_name TEXT NOT NULL,
            name TEXT NOT NULL,
            director_name TEXT,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            rating INTEGER DEFAULT 0
        );
    """)
    return conn


class PartnerEditWindow(tk.Toplevel):
    def __init__(self, parent, db_conn):
        super().__init__(parent)
        self.parent = parent
        self.conn = db_conn

        self.title("CRM: Карточка партнера [Добавление]")
        self.geometry("500x580")
        self.configure(bg="#F4F4F4")

        self.create_widgets()

    def create_widgets(self):
        form = tk.Frame(self, bg="#F4F4F4", padx=25, pady=15)
        form.pack(fill="both", expand=True)

        tk.Label(form, text="Наименование партнера *", bg="#F4F4F4", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.name_entry = tk.Entry(form, font=("Segoe UI", 10))
        self.name_entry.pack(fill="x", pady=(2, 8))

        tk.Label(form, text="Тип партнера *", bg="#F4F4F4", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.type_combo = ttk.Combobox(form, values=["ЗАО", "ООО", "ПАО", "ОАО", "ИП"], state="readonly")
        self.type_combo.current(1)
        self.type_combo.pack(fill="x", pady=(2, 8))

        tk.Label(form, text="Рейтинг (целое неотрицательное число) *", bg="#F4F4F4", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.rating_entry = tk.Entry(form, font=("Segoe UI", 10))
        self.rating_entry.insert(0, "0")
        self.rating_entry.pack(fill="x", pady=(2, 8))

        tk.Label(form, text="Телефон *", bg="#F4F4F4", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.phone_entry = tk.Entry(form, font=("Segoe UI", 10))
        self.phone_entry.pack(fill="x", pady=(2, 8))

        tk.Label(form, text="Email *", bg="#F4F4F4", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.email_entry = tk.Entry(form, font=("Segoe UI", 10))
        self.email_entry.pack(fill="x", pady=(2, 8))

        btn_box = tk.Frame(self, bg="#F4F4F4", padx=25, pady=15)
        btn_box.pack(fill="x", side="bottom")

        tk.Button(btn_box, text="Сохранить", bg="#67BA80", fg="#FFFFFF", font=("Segoe UI", 10, "bold"), command=self.validate_and_save).pack(side="left")
        tk.Button(btn_box, text="Отмена", bg="#FFFFFF", font=("Segoe UI", 10), command=self.destroy).pack(side="right")

    def validate_and_save(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        rating_raw = self.rating_entry.get().strip()

        if not name:
            messagebox.showerror(
                "Ошибка ввода", 
                "Поле 'Наименование партнера' не может быть пустым.\nПожалуйста, введите название компании и повторите попытку."
            )
            return

        if not email or "@" not in email:
            messagebox.showerror(
                "Ошибка ввода", 
                "Поле 'Email' написано некорректно или отсутствует.\nПожалуйста, укажите верный адрес электронной почты."
            )
            return

        try:
            rating = int(rating_raw)
            if rating < 0:
                raise ValueError("Рейтинг не может быть отрицательным")
        except ValueError:
            messagebox.showerror(
                "Ошибка (Error)", 
                "Рейтинг должен быть целым числом от 0.\nПожалуйста, удалите символы/знаки препинания и повторите попытку."
            )
            return


try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO partners (type_name, name, email, phone, rating)
                VALUES (?, ?, ?, ?, ?)
            """, (self.type_combo.get(), name, email, phone, rating))
            self.conn.commit()
            messagebox.showinfo("Успешно", "Данные партнера успешно сохранены в базе данных!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка СУБД", f"Не удалось сохранить данные в БД:\n{str(e)}")


if name == "__main__":
    db = init_db()
    root = tk.Tk()
    root.withdraw()
    win = PartnerEditWindow(root, db)
    root.mainloop()
