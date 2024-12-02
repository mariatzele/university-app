import customtkinter as ctk
from data import StudentRepository


class App:
    def __init__(self, student_repo: StudentRepository):
        self.student_repo = student_repo
        self.build_app()

    def start(self):
        self.app.mainloop()

    def build_app(self):
        self.app = ctk.CTk()
        self.app.geometry("1000x500")
        self.app.title("University Management")
        self.app.focus_force()

        label = ctk.CTkLabel(
            master=self.app,
            text="University Management",
            font=("Arial", 32, "bold"),
            bg_color="transparent",
        )
        label.pack(anchor="w")
