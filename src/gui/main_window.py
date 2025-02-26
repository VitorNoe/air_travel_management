import tkinter as tk
from tkinter import ttk, messagebox
from src.gui import flights, passengers, bookings, baggage, reports, settings

class MainWindow(tk.Tk):
    def __init__(self, access_level):
        super().__init__()
        self.title("Gerenciamento de Viagens Aéreas")
        self.geometry("1200x600")
        
        # Barra de menu
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        
        # Menu Voos
        flight_menu = tk.Menu(menu_bar, tearoff=0)
        flight_menu.add_command(label="Gerenciar Voos", command=lambda: self.show_frame(flights.FlightWindow))
        menu_bar.add_cascade(label="Voos", menu=flight_menu)
        
        # Menu Passageiros (similar para outros módulos)
        # ... (implementar outros menus)
        
        # Container para frames
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        
        self.frames = {}
        for F in (flights.FlightWindow, passengers.PassengerWindow):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(flights.FlightWindow)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()