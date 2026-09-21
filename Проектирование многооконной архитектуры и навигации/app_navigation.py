import tkinter as tk


class PartnerEditWindow(tk.Toplevel):
    def __init__(self, parent, mode="add"):
        super().__init__(parent)
        self.parent = parent
        if mode == "add":
            self.title("CRM: Карточка партнера [Добавление]")
        else:
            self.title("CRM: Карточка партнера [Редактирование]")
        self.geometry("500x550")
        self.configure(bg="#F4F4F4")
        self.resizable(False, False)

        header = tk.Frame(self, bg="#FFFFFF", pady=12, padx=15, bd=1, relief="solid")
        header.pack(fill="x")

        title_text = "Новый партнер" if mode == "add" else "Редактирование данных"
        tk.Label(header, text=title_text, font=("Segoe UI", 12, "bold"), bg="#FFFFFF", fg="#222222").pack(side="left")

        body = tk.Frame(self, bg="#F4F4F4", padx=20, pady=20)
        body.pack(fill="both", expand=True)

        tk.Label(body, text="Форма заполнения данных партнера", font=("Segoe UI", 10), bg="#F4F4F4", fg="#555555").pack(pady=20)

        btn_frame = tk.Frame(self, bg="#F4F4F4", pady=15)
        btn_frame.pack(fill="x", side="bottom")

        cancel_btn = tk.Button(
            btn_frame,
            text="Назад",
            font=("Segoe UI", 10),
            bg="#FFFFFF",
            fg="#333333",
            padx=15,
            pady=5,
            command=self.destroy
        )
        cancel_btn.pack(side="right", padx=20)


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CRM: Реестр партнеров")
        self.geometry("750x550")
        self.configure(bg="#F4F4F4")

        header = tk.Frame(self, bg="#FFFFFF", pady=15, padx=20, bd=1, relief="solid")
        header.pack(fill="x")

        tk.Label(header, text="Реестр партнеров", font=("Segoe UI", 14, "bold"), bg="#FFFFFF", fg="#222222").pack(side="left")

        add_btn = tk.Button(
            header,
            text="+ Добавить партнера",
            font=("Segoe UI", 10, "bold"),
            bg="#67BA80",
            fg="#FFFFFF",
            padx=10,
            pady=5,
            relief="flat",
            command=self.open_add_partner_window
        )
        add_btn.pack(side="right")

        content = tk.Frame(self, bg="#F4F4F4", padx=20, pady=20)
        content.pack(fill="both", expand=True)

        tk.Label(content, text="Список партнеров загружен. Нажмите кнопку выше для добавления.", font=("Segoe UI", 10), bg="#F4F4F4", fg="#666666").pack(anchor="w")

    def open_add_partner_window(self):
        PartnerEditWindow(self, mode="add")


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
