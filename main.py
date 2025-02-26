import tkinter as tk
from src.auth import Auth
from src.gui.main_window import MainWindow

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("300x150")
        
        tk.Label(self, text="Usuário:").pack()
        self.username = tk.Entry(self)
        self.username.pack()
        
        tk.Label(self, text="Senha:").pack()
        self.password = tk.Entry(self, show="*")
        self.password.pack()
        
        btn_login = tk.Button(self, text="Entrar", command=self.login)
        btn_login.pack(pady=10)
    
    def login(self):
        auth = Auth()
        access_level = auth.login(self.username.get(), self.password.get())
        if access_level:
            self.destroy()
            app = MainWindow(access_level)
            app.mainloop()
        else:
            tk.messagebox.showerror("Erro", "Credenciais inválidas!")

if __name__ == "__main__":
    login = LoginWindow()
    login.mainloop()