import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
import hashlib
from datetime import datetime

class DatabaseHandler:
    def __init__(self):
        self.connection = None
        
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                password='',
                database='air_travel_management'
            )
            return True
        except Error as e:
            messagebox.showerror("Erro de Conexão", f"Falha ao conectar ao MySQL: {e}")
            return False

    def disconnect(self):
        if self.connection:
            self.connection.close()

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gerenciamento de Viagens - Login")
        self.geometry("300x150")
        self.db = DatabaseHandler()
        self.create_widgets()
        
    def create_widgets(self):
        ttk.Label(self, text="Usuário:").pack(pady=5)
        self.entry_user = ttk.Entry(self)
        self.entry_user.pack(pady=5)
        
        ttk.Label(self, text="Senha:").pack(pady=5)
        self.entry_pass = ttk.Entry(self, show="*")
        self.entry_pass.pack(pady=5)
        
        ttk.Button(self, text="Login", command=self.authenticate).pack(pady=10)

    def authenticate(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()
        
        if not self.db.connect():
            return
            
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("SELECT password_hash, access_level FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            
            if result:
                stored_hash = result[0]
                input_hash = hashlib.sha256(password.encode()).hexdigest()
                
                if stored_hash == input_hash:
                    self.destroy()
                    MainWindow(result[1])
                else:
                    messagebox.showerror("Erro", "Credenciais inválidas")
            else:
                messagebox.showerror("Erro", "Usuário não encontrado")
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao autenticar: {e}")
        finally:
            self.db.disconnect()

class MainWindow(tk.Tk):
    def __init__(self, access_level):
        super().__init__()
        self.title("Sistema de Gerenciamento de Viagens")
        self.geometry("1000x600")
        self.db = DatabaseHandler()
        self.access_level = access_level
        self.selected_flight = None
        self.create_interface()

    def create_interface(self):
        self.create_menu()
        self.create_flight_widgets()
        self.load_flights()

    def create_menu(self):
        menu_bar = tk.Menu(self)
        flight_menu = tk.Menu(menu_bar, tearoff=0)
        flight_menu.add_command(label="Gerenciar Voos", command=self.create_flight_widgets)
        menu_bar.add_cascade(label="Voos", menu=flight_menu)
        self.config(menu=menu_bar)

    def create_flight_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

        # Formulário
        form_frame = ttk.LabelFrame(self, text="Detalhes do Voo")
        form_frame.pack(fill=tk.X, padx=10, pady=5)

        fields = [
            ("Companhia Aérea:", "entry", None),
            ("Cidade de Partida:", "entry", None),
            ("País de Partida:", "entry", None),
            ("Cidade de Destino:", "entry", None),
            ("País de Destino:", "entry", None),
            ("Partida Prevista:", "entry", "YYYY-MM-DD HH:MM:SS"),
            ("Chegada Prevista:", "entry", "YYYY-MM-DD HH:MM:SS"),
            ("Status:", "combobox", ["Agendado", "Em rota", "Finalizado", "Cancelado"]),
            ("Voo Internacional:", "checkbutton", None)  # Corrigido aqui
        ]

        self.entries = {}
        for i, (label, field_type, options) in enumerate(fields):
            row = i // 2
            col = (i % 2) * 2
            clean_label = label.replace(":", "").strip()
            
            ttk.Label(form_frame, text=label).grid(row=row, column=col, padx=5, pady=5, sticky=tk.E)
            
            if field_type == "entry":
                entry = ttk.Entry(form_frame)
                if options:
                    entry.insert(0, options)
            elif field_type == "combobox":
                entry = ttk.Combobox(form_frame, values=options)
            elif field_type == "checkbutton":
                entry = ttk.Checkbutton(form_frame, text="Sim")
            
            entry.grid(row=row, column=col+1, padx=5, pady=5, sticky=tk.W)
            self.entries[clean_label] = entry

        # Botões
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Adicionar", command=self.add_flight).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Atualizar", command=self.update_flight).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Excluir", command=self.delete_flight).pack(side=tk.LEFT, padx=5)

        # Lista de voos
        columns = ("ID", "Companhia", "Partida", "Destino", "Partida Prevista", "Status", "Internacional")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
            
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_flight_select)

    def load_flights(self):
        if not self.db.connect():
            return
            
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("""
                SELECT flight_id, airline, 
                CONCAT(departure_city, ', ', departure_country),
                CONCAT(arrival_city, ', ', arrival_country),
                DATE_FORMAT(scheduled_departure, '%%Y-%%m-%%d %%H:%%i'),
                status,
                IF(is_international, 'Sim', 'Não')
                FROM flights
            """)
            
            self.tree.delete(*self.tree.get_children())
            for row in cursor:
                self.tree.insert("", tk.END, values=row)
                
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar voos: {e}")
        finally:
            self.db.disconnect()

    def add_flight(self):
        if not self.db.connect():
            return

        try:
            cursor = self.db.connection.cursor()
            
            # Obter valores
            values = {
                'airline': self.entries["Companhia Aérea"].get(),
                'departure_city': self.entries["Cidade de Partida"].get(),
                'departure_country': self.entries["País de Partida"].get(),
                'arrival_city': self.entries["Cidade de Destino"].get(),
                'arrival_country': self.entries["País de Destino"].get(),
                'scheduled_departure': self.entries["Partida Prevista"].get(),
                'scheduled_arrival': self.entries["Chegada Prevista"].get(),
                'status': self.entries["Status"].get(),
                'is_international': 1 if self.entries["Voo Internacional"].instate(['selected']) else 0  # Corrigido aqui
            }

            # Validar campos
            required = ['airline', 'departure_city', 'departure_country',
                       'arrival_city', 'arrival_country', 'scheduled_departure',
                       'scheduled_arrival', 'status']
            
            for field in required:
                if not values[field]:
                    messagebox.showerror("Erro", f"Campo obrigatório faltando: {field}")
                    return

            # Inserir no banco
            query = """
                INSERT INTO flights (
                    airline, departure_city, departure_country,
                    arrival_city, arrival_country, scheduled_departure,
                    scheduled_arrival, status, is_international
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(query, tuple(values.values()))
            self.db.connection.commit()
            messagebox.showinfo("Sucesso", "Voo adicionado com sucesso!")
            self.load_flights()
            
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao adicionar voo: {e}")
        finally:
            self.db.disconnect()

    def on_flight_select(self, event):
        selected = self.tree.selection()
        if selected:
            self.selected_flight = self.tree.item(selected[0])['values']
            self.load_selected_flight()

    def load_selected_flight(self):
        if self.selected_flight:
            fields = [
                "Companhia Aérea", "Cidade de Partida", "País de Partida",
                "Cidade de Destino", "País de Destino", "Partida Prevista",
                "Chegada Prevista", "Status", "Voo Internacional"
            ]
            
            for i, field in enumerate(fields):
                if field == "Voo Internacional":
                    state = ['selected'] if self.selected_flight[6] == 'Sim' else []
                    self.entries[field].state(state)
                else:
                    entry = self.entries[field]
                    entry.delete(0, tk.END)
                    entry.insert(0, self.selected_flight[i+1])

    def update_flight(self):
        if not self.selected_flight:
            messagebox.showwarning("Aviso", "Nenhum voo selecionado")
            return

        if not self.db.connect():
            return

        try:
            cursor = self.db.connection.cursor()
            
            values = {
                'airline': self.entries["Companhia Aérea"].get(),
                'departure_city': self.entries["Cidade de Partida"].get(),
                'departure_country': self.entries["País de Partida"].get(),
                'arrival_city': self.entries["Cidade de Destino"].get(),
                'arrival_country': self.entries["País de Destino"].get(),
                'scheduled_departure': self.entries["Partida Prevista"].get(),
                'scheduled_arrival': self.entries["Chegada Prevista"].get(),
                'status': self.entries["Status"].get(),
                'is_international': 1 if self.entries["Voo Internacional"].instate(['selected']) else 0,
                'flight_id': self.selected_flight[0]
            }

            query = """
                UPDATE flights SET
                    airline = %s,
                    departure_city = %s,
                    departure_country = %s,
                    arrival_city = %s,
                    arrival_country = %s,
                    scheduled_departure = %s,
                    scheduled_arrival = %s,
                    status = %s,
                    is_international = %s
                WHERE flight_id = %s
            """
            
            cursor.execute(query, (
                values['airline'],
                values['departure_city'],
                values['departure_country'],
                values['arrival_city'],
                values['arrival_country'],
                values['scheduled_departure'],
                values['scheduled_arrival'],
                values['status'],
                values['is_international'],
                values['flight_id']
            ))
            
            self.db.connection.commit()
            messagebox.showinfo("Sucesso", "Voo atualizado com sucesso!")
            self.load_flights()
            
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao atualizar voo: {e}")
        finally:
            self.db.disconnect()

    def delete_flight(self):
        if not self.selected_flight:
            messagebox.showwarning("Aviso", "Nenhum voo selecionado")
            return

        if messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este voo?"):
            if not self.db.connect():
                return

            try:
                cursor = self.db.connection.cursor()
                cursor.execute("DELETE FROM flights WHERE flight_id = %s", (self.selected_flight[0],))
                self.db.connection.commit()
                messagebox.showinfo("Sucesso", "Voo excluído com sucesso!")
                self.load_flights()
                self.selected_flight = None
                
            except Error as e:
                messagebox.showerror("Erro", f"Erro ao excluir voo: {e}")
            finally:
                self.db.disconnect()

if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()