import tkinter as tk
from tkinter import ttk
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
            legal_address TEXT,
            rating INTEGER DEFAULT 0
        );
    """)
    cursor.executemany("""
        INSERT INTO partners (type_name, name, director_name, email, phone, legal_address, rating)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, [
        ("ЗАО", "База Строитель", "Иванова Светлана Сергеевна", "info@stroitel.ru", "+7 223 322 22 32", "г. Москва, ул. Ленина 5", 10),
        ("ООО", "Паркет 29", "Петров Петр Петрович", "parket29@mail.ru", "+7 921 555 44 33", "г. СПб, ул. Мира 12", 15),
        ("ПАО", "Стройкомплект", "Сидоров Алексей Владимирович", "stroy@corp.ru", "+7 905 111 22 33", "г. Казань, ул. Полевая 1", 8)
    ])
    conn.commit()
    return conn


class PartnerEditWindow(tk.Toplevel):
    def __init__(self, parent, db_conn, mode="add", partner_id=None):
        super().__init__(parent)
        self.parent = parent
        self.conn = db_conn
        self.mode = mode
        self.partner_id = partner_id

        self.title("CRM: Карточка партнера [Добавление]" if mode == "add" else "CRM: Карточка партнера [Редактирование]")
        self.geometry("520x600")
        self.configure(bg="#F4F4F4")

        self.create_widgets()
        if self.mode == "edit" and self.partner_id:
            self.load_partner_data()

    def create_widgets(self):
        form = tk.Frame(self, bg="#F4F4F4", padx=25, pady=15)
        form.pack(fill="both", expand=True)

        tk.Label(form, text="Наименование *", bg="#F4F4F4", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.name_entry = tk.Entry(form, font=("Segoe UI", 10))
        self.name_entry.pack(fill="x", pady=(2, 8))

        tk.Label(form, text="Тип партнера *", bg="#F4F4F4", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.type_combo = ttk.Combobox(form, values=["ЗАО", "ООО", "ПАО", "ОАО", "ИП"], state="readonly")
        self.type_combo.current(1)
        self.type_combo.pack(fill="x", pady=(2, 8))

        tk.Label(form, text="Рейтинг *", bg="#F4F4F4", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.rating_entry = tk.Entry(form, font=("Segoe UI", 10))
        self.rating_entry.insert(0, "0")
        self.rating_entry.pack(fill="x", pady=(2, 8))

        tk.Label(form, text="Директор", bg="#F4F4F4", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.director_entry = tk.Entry(form, font=("Segoe UI", 10))
        self.director_entry.pack(fill="x", pady=(2, 8))

        tk.Label(form, text="Телефон *", bg="#F4F4F4", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.phone_entry = tk.Entry(form, font=("Segoe UI", 10))
        self.phone_entry.pack(fill="x", pady=(2, 8))

        tk.Label(form, text="Email *", bg="#F4F4F4", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.email_entry = tk.Entry(form, font=("Segoe UI", 10))
        self.email_entry.pack(fill="x", pady=(2, 8))

        btn_box = tk.Frame(self, bg="#F4F4F4", padx=25, pady=15)
        btn_box.pack(fill="x", side="bottom")

        tk.Button(btn_box, text="Сохранить", bg="#67BA80", fg="#FFFFFF", font=("Segoe UI", 10, "bold"), command=self.save_data).pack(side="left")
        tk.Button(btn_box, text="Отмена", bg="#FFFFFF", font=("Segoe UI", 10), command=self.destroy).pack(side="right")

    def load_partner_data(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT type_name, name, director_name, email, phone, rating FROM partners WHERE id=?", (self.partner_id,))
        row = cursor.fetchone()
        if row:
            self.type_combo.set(row[0])
            self.name_entry.insert(0, row[1])
            self.director_entry.insert(0, row[2] or "")
            self.email_entry.insert(0, row[3])
            self.phone_entry.insert(0, row[4])
            self.rating_entry.delete(0, tk.END)
            self.rating_entry.insert(0, str(row[5]))

    def save_data(self):
        cursor = self.conn.cursor()
        if self.mode == "add":
            cursor.execute("""
                INSERT INTO partners (type_name, name, director_name, email, phone, rating)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (self.type_combo.get(), self.name_entry.get(), self.director_entry.get(), self.email_entry.get(), self.phone_entry.get(), int(self.rating_entry.get())))
        else:
            cursor.execute("""
                UPDATE partners 
                SET type_name=?, name=?, director_name=?, email=?, phone=?, rating=?
                WHERE id=?
            """, (self.type_combo.get(), self.name_entry.get(), self.director_entry.get(), self.email_entry.get(), self.phone_entry.get(), int(self.rating_entry.get()), self.partner_id))
        
        self.conn.commit()
        self.parent.refresh_list()
        self.destroy()


class MainWindow(tk.Tk):
    def __init__(self, db_conn):
        super().__init__()
        self.conn = db_conn
        self.title("CRM: Реестр партнеров")
        self.geometry("750x550")
        self.configure(bg="#F4F4F4")

        header = tk.Frame(self, bg="#FFFFFF", pady=15, padx=20)
        header.pack(fill="x")
        tk.Label(header, text="Партнеры компании", font=("Segoe UI", 14, "bold"), bg="#FFFFFF").pack(side="left")
        tk.Button(header, text="+ Добавить партнера", bg="#67BA80", fg="#FFFFFF", font=("Segoe UI", 10, "bold"), command=self.add_partner).pack(side="right")

        self.list_frame = tk.Frame(self, bg="#F4F4F4", padx=20, pady=10)
        self.list_frame.pack(fill="both", expand=True)

        self.refresh_list()

    def refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        cursor = self.conn.cursor()
        cursor.execute("SELECT id, type_name, name, director_name, phone, rating FROM partners ORDER BY id DESC")
        rows = cursor.fetchall()

        for r in rows:
            card = tk.Frame(self.list_frame, bg="#FFFFFF", bd=1, relief="solid", padx=12, pady=8)
            card.pack(fill="x", pady=4)
            card.bind("<Double-Button-1>", lambda e, pid=r[0]: self.edit_partner(pid))
            
            tk.Label(card, text=f"{r[1]} | {r[2]} (Двойной клик для редактирования)", font=("Segoe UI", 10, "bold"), bg="#FFFFFF").pack(anchor="w")
            tk.Label(card, text=f"Директор: {r[3]} | Тел: {r[4]} | Рейтинг: {r[5]}", font=("Segoe UI", 9), bg="#FFFFFF", fg="#555555").pack(anchor="w")

    def add_partner(self):
        PartnerEditWindow(self, self.conn, mode="add")

    def edit_partner(self, partner_id):
        PartnerEditWindow(self, self.conn, mode="edit", partner_id=partner_id)


if __name__ == "__main__":
    db = init_db()
    app = MainWindow(db)
    app.mainloop()
