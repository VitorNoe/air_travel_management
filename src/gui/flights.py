import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry 
from src.database import Database

class FlightWindow(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.db = Database()
        self.controller = controller
        self.create_widgets()
        self.load_flights()

    def create_widgets(self):
        # Treeview para exibir voos
        self.tree = ttk.Treeview(self, columns=(
            "ID", "Companhia", "Partida", "Cidade Origem", 
            "Cidade Destino", "Status", "Internacional"
        ), show="headings")
        
        # Configurar cabeçalhos
        self.tree.heading("ID", text="ID")
        self.tree.heading("Companhia", text="Companhia Aérea")
        self.tree.heading("Partida", text="Partida")
        self.tree.heading("Cidade Origem", text="Origem")
        self.tree.heading("Cidade Destino", text="Destino")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Internacional", text="Internacional")
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Botões
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        
        btn_add = tk.Button(btn_frame, text="Adicionar Voo", command=self.open_add_window)
        btn_add.pack(side=tk.LEFT, padx=5)
        
        btn_refresh = tk.Button(btn_frame, text="Atualizar", command=self.load_flights)
        btn_refresh.pack(side=tk.LEFT, padx=5)

    def load_flights(self):
        # Limpar dados existentes
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        query = """SELECT 
            flight_id, airline, scheduled_departure,
            CONCAT(departure_city, ' (', departure_country, ')'),
            CONCAT(arrival_city, ' (', arrival_country, ')'),
            status, is_international
            FROM flights"""
            
        flights = self.db.fetch_data(query)
        for row in flights:
            self.tree.insert("", "end", values=row)

    def open_add_window(self):
        add_window = tk.Toplevel(self)
        add_window.title("Novo Voo")
        add_window.geometry("400x500")
        
        # Campos do formulário
        fields = [
            ("Companhia Aérea:", "airline"),
            ("Cidade de Origem:", "departure_city"),
            ("País de Origem:", "departure_country"),
            ("Cidade de Destino:", "arrival_city"),
            ("País de Destino:", "arrival_country"),
            ("Partida Programada:", "scheduled_departure"),
            ("Chegada Programada:", "scheduled_arrival"),
            ("Status:", "status"),
            ("Voo Internacional:", "is_international")
        ]
        
        entries = {}
        
        for i, (label, field) in enumerate(fields):
            tk.Label(add_window, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            
            if "scheduled" in field:
                entry = DateEntry(add_window, date_pattern="yyyy-mm-dd HH:mm:ss")
            elif field == "status":
                entry = ttk.Combobox(add_window, values=["Agendado", "Em rota", "Finalizado", "Cancelado"])
            elif field == "is_international":
                entry = ttk.Combobox(add_window, values=["Sim", "Não"])
            else:
                entry = tk.Entry(add_window)
                
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="we")
            entries[field] = entry
        
        # Botão de salvar
        btn_save = tk.Button(add_window, text="Salvar", 
                           command=lambda: self.save_flight(entries, add_window))
        btn_save.grid(row=len(fields)+1, column=1, sticky="e", padx=5, pady=10)

    def save_flight(self, entries, window):
        try:
            # Converter dados para formato do banco
            is_international = 1 if entries["is_international"].get() == "Sim" else 0
            
            query = """INSERT INTO flights (
                airline, departure_city, departure_country,
                arrival_city, arrival_country, scheduled_departure,
                scheduled_arrival, status, is_international
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            
            params = (
                entries["airline"].get(),
                entries["departure_city"].get(),
                entries["departure_country"].get(),
                entries["arrival_city"].get(),
                entries["arrival_country"].get(),
                entries["scheduled_departure"].get(),
                entries["scheduled_arrival"].get(),
                entries["status"].get(),
                is_international
            )
            
            self.db.execute_query(query, params)
            messagebox.showinfo("Sucesso", "Voo cadastrado com sucesso!")
            window.destroy()
            self.load_flights()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar voo:\n{str(e)}")