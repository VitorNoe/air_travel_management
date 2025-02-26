import tkinter as tk
from tkinter import ttk
from src.database import Database

class PassengerWindow(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.db = Database()
        self.create_widgets()
        
    def create_widgets(self):
        label = tk.Label(self, text="Gerenciamento de Passageiros (Em desenvolvimento)")
        label.pack(pady=20)