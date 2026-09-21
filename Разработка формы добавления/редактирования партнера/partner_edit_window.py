import tkinter as tk
from tkinter import ttk


class PartnerEditWindow(tk.Toplevel):
    def __init__(self, parent, mode="add"):
        super().__init__(parent)
        self.parent = parent
        self.mode = mode
        self.title("CRM: Карточка партнера [Добавление]" if mode == "add" else "CRM: Карточка партнера [Редактирование]")
        self.geometry("520x620")
        self.configure(bg="#F4F4F4")
        self.resizable(False, False)

        header = tk.Frame(self, bg="#FFFFFF", pady=12, padx=20, bd=1, relief="solid")
        header.pack(fill="x")
        
        title_lbl = "Создание карточки партнера" if self.mode == "add" else "Редактирование карточки"
        tk.Label(header, text=title_lbl, font=("Segoe UI", 12, "bold"), bg="#FFFFFF", fg="#222222").pack(side="left")

        form = tk.Frame(self, bg="#F4F4F4", padx=25, pady=15)
        form.pack(fill="both", expand=True)

        tk.Label(form, text="Наименование партнера *", font=("Segoe UI", 9, "bold"), bg="#F4F4F4").pack(anchor="w", pady=(5, 2))
        self.name_entry = tk.Entry(form, font=("Segoe UI", 10), bd=1, relief="solid")
        self.name_entry.pack(fill="x", ipady=4)

        tk.Label(form, text="Тип партнера *", font=("Segoe UI", 9, "bold"), bg="#F4F4F4").pack(anchor="w", pady=(10, 2))
        self.type_combo = ttk.Combobox(form, values=["ЗАО", "ООО", "ПАО", "ОАО", "ИП"], font=("Segoe UI", 10), state="readonly")
        self.type_combo.current(1)
        self.type_combo.pack(fill="x", ipady=3)

        tk.Label(form, text="Рейтинг (целое неотрицательное число) *", font=("Segoe UI", 9, "bold"), bg="#F4F4F4").pack(anchor="w", pady=(10, 2))
        self.rating_entry = tk.Entry(form, font=("Segoe UI", 10), bd=1, relief="solid")
        self.rating_entry.insert(0, "0")
        self.rating_entry.pack(fill="x", ipady=4)

        tk.Label(form, text="Юридический адрес", font=("Segoe UI", 9, "bold"), bg="#F4F4F4").pack(anchor="w", pady=(10, 2))
        self.address_entry = tk.Entry(form, font=("Segoe UI", 10), bd=1, relief="solid")
        self.address_entry.pack(fill="x", ipady=4)

        tk.Label(form, text="ФИО директора", font=("Segoe UI", 9, "bold"), bg="#F4F4F4").pack(anchor="w", pady=(10, 2))
        self.director_entry = tk.Entry(form, font=("Segoe UI", 10), bd=1, relief="solid")
        self.director_entry.pack(fill="x", ipady=4)

        tk.Label(form, text="Телефон (Формат: +7 XXX XXX-XX-XX) *", font=("Segoe UI", 9, "bold"), bg="#F4F4F4").pack(anchor="w", pady=(10, 2))
        self.phone_entry = tk.Entry(form, font=("Segoe UI", 10), bd=1, relief="solid", fg="#888888")
        self.phone_entry.insert(0, "+7 ")
        self.phone_entry.pack(fill="x", ipady=4)

        tk.Label(form, text="Электронная почта (Email) *", font=("Segoe UI", 9, "bold"), bg="#F4F4F4").pack(anchor="w", pady=(10, 2))
        self.email_entry = tk.Entry(form, font=("Segoe UI", 10), bd=1, relief="solid")
        self.email_entry.pack(fill="x", ipady=4)

        btn_box = tk.Frame(self, bg="#F4F4F4", padx=25, pady=15)
        btn_box.pack(fill="x", side="bottom")

        tk.Button(btn_box, text="Сохранить", font=("Segoe UI", 10, "bold"), bg="#67BA80", fg="#FFFFFF", padx=15, pady=6, relief="flat").pack(side="left")
        tk.Button(btn_box, text="Отмена", font=("Segoe UI", 10), bg="#FFFFFF", fg="#333333", padx=15, pady=6, command=self.destroy).pack(side="right")


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    win = PartnerEditWindow(root)
    root.mainloop()
