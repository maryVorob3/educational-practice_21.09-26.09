import tkinter as tk
from tkinter import ttk


class PlaceholderEntry(tk.Entry):
    def __init__(self, container, placeholder, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = '#888888'
        self.default_fg_color = self['fg']

        self.put_placeholder()
        self.bind("<FocusIn>", self.focus_in)
        self.bind("<FocusOut>", self.focus_out)

    def put_placeholder(self):
        if not self.get():
            self.insert(0, self.placeholder)
            self['fg'] = self.placeholder_color

    def focus_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def focus_out(self, *args):
        if not self.get():
            self.put_placeholder()


class PartnerEditWindow(tk.Toplevel):
    def __init__(self, parent, mode="add"):
        super().__init__(parent)
        self.parent = parent
        self.mode = mode
        self.title("CRM: Карточка партнера [Добавление]" if mode == "add" else "CRM: Карточка партнера [Редактирование]")
        self.geometry("520x640")
        self.configure(bg="#F4F4F4")
        self.resizable(False, False)

        header = tk.Frame(self, bg="#FFFFFF", pady=12, padx=20, bd=1, relief="solid")
        header.pack(fill="x")
        
        title_lbl = "Создание карточки партнера" if self.mode == "add" else "Редактирование карточки"
        tk.Label(header, text=title_lbl, font=("Segoe UI", 12, "bold"), bg="#FFFFFF", fg="#222222").pack(side="left")

        form = tk.Frame(self, bg="#F4F4F4", padx=25, pady=15)
        form.pack(fill="both", expand=True)

        tk.Label(form, text="Наименование партнера *", font=("Segoe UI", 9, "bold"), bg="#F4F4F4").pack(anchor="w", pady=(5, 2))
        self.name_entry = PlaceholderEntry(form, "Например: ООО 'СтройМонтаж'", font=("Segoe UI", 10), bd=1, relief="solid")
        self.name_entry.pack(fill="x", ipady=4)

        tk.Label(form, text="Тип партнера * (только выбор из списка)", font=("Segoe UI", 9, "bold"), bg="#F4F4F4").pack(anchor="w", pady=(10, 2))
        # state="readonly" полностью исключает некорректный ручной ввод
        self.type_combo = ttk.Combobox(form, values=["ЗАО", "ООО", "ПАО", "ОАО", "ИП"], font=("Segoe UI", 10), state="readonly")
        self.type_combo.current(1)
        self.type_combo.pack(fill="x", ipady=3)

        tk.Label(form, text="Рейтинг (целое неотрицательное число) *", font=("Segoe UI", 9, "bold"), bg="#F4F4F4").pack(anchor="w", pady=(10, 2))
        self.rating_entry = tk.Entry(form, font=("Segoe UI", 10), bd=1, relief="solid")
        self.rating_entry.insert(0, "0")
        self.rating_entry.pack(fill="x", ipady=4)

        tk.Label(form, text="Юридический адрес", font=("Segoe UI", 9, "bold"), bg="#F4F4F4").pack(anchor="w", pady=(10, 2))
        self.address_entry = PlaceholderEntry(form, "г. Москва, ул. Примерная, д. 1", font=("Segoe UI", 10), bd=1, relief="solid")
        self.address_entry.pack(fill="x", ipady=4)

        tk.Label(form, text="ФИО директора", font=("Segoe UI", 9, "bold"), bg="#F4F4F4").pack(anchor="w", pady=(10, 2))
        self.director_entry = PlaceholderEntry(form, "Иванов Иван Иванович", font=("Segoe UI", 10), bd=1, relief="solid")
        self.director_entry.pack(fill="x", ipady=4)

        tk.Label(form, text="Телефон *", font=("Segoe UI", 9, "bold"), bg="#F4F4F4").pack(anchor="w", pady=(10, 2))
        self.phone_entry = PlaceholderEntry(form, "+7 (999) 000-00-00", font=("Segoe UI", 10), bd=1, relief="solid")
        self.phone_entry.pack(fill="x", ipady=4)

        tk.Label(form, text="Электронная почта (Email) *", font=("Segoe UI", 9, "bold"), bg="#F4F4F4").pack(anchor="w", pady=(10, 2))
        self.email_entry = PlaceholderEntry(form, "partner@company.ru", font=("Segoe UI", 10), bd=1, relief="solid")
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
