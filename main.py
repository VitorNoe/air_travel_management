import customtkinter as ctk
import pywinstyles
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime
import pytz
import hashlib
from tkinter import simpledialog
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)

# Configuração do tema
ctk.set_appearance_mode("dark")  # Opções: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Opções: "blue", "green", "dark-blue"
ctk.deactivate_automatic_dpi_awareness()

# Crie uma nova classe personalizada antes da classe AirTravelApp:
class HoverButton(ctk.CTkButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_bg = self.cget("fg_color")
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self.configure(fg_color="#2B5D95", border_color="#4CC9F0", border_width=2)
        
    def on_leave(self, event):
        self.configure(fg_color=self.default_bg, border_width=0)

class AirTravelApp(ctk.CTk):
    def __init__(self):
        super().__init__()  
        self.is_admin = False
        self.current_user_id = None
        pywinstyles.apply_style(self, "acrylic")
        # Configuração da janela principal
        self.title("Sistema de Gerenciamento de Viagens Aéreas")
        self.geometry("1100x700")
        self.minsize(900, 600)
        
        # Variáveis da aplicação
        self.current_user = None
        self.flight_data = []
        
        # Criar layout principal
        self.create_layout()
        if self.is_admin:
            self.users_button = HoverButton(self.sidebar_frame, text="Usuários", command=self.manage_users)
            self.users_button.pack(pady=10, padx=20, fill="x")
        # Tentar conexão com o banco de dados
        self.db_connection = self.connect_database()
        
        # Iniciar com a tela de login
        self.show_login_frame()

    def connect_database(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="air_travel_management"
            )
            return connection
        except mysql.connector.Error as error:
            messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao banco de dados: {error}")
            return None

    def create_layout(self):
        # Criar frame lateral (menu)
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y", padx=0, pady=0)
        self.sidebar_frame.pack_propagate(False)
        
        # Logo da aplicação
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="AirTravel", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(pady=(20, 20))
        
        # Botões do menu
        self.dashboard_button = HoverButton(self.sidebar_frame, text="Dashboard", command=self.show_dashboard)
        self.dashboard_button.pack(pady=10, padx=20, fill="x")
        
        self.flights_button = HoverButton(self.sidebar_frame, text="Voos", command=self.show_flights)
        self.flights_button.pack(pady=10, padx=20, fill="x")
        
        self.booking_button = HoverButton(self.sidebar_frame, text="Reservas", command=self.show_bookings)
        self.booking_button.pack(pady=10, padx=20, fill="x")
        
        self.reports_button = HoverButton(self.sidebar_frame, text="Relatórios", command=self.show_reports)
        self.reports_button.pack(pady=10, padx=20, fill="x")
        
        self.settings_button = HoverButton(self.sidebar_frame, text="Configurações", command=self.show_settings)
        self.settings_button.pack(pady=10, padx=20, fill="x")
        
        # Botão de logout no final do sidebar
        self.logout_button = HoverButton(self.sidebar_frame, text="Sair", fg_color="transparent", 
                                        border_width=2, text_color=("gray10", "gray90"), command=self.logout)
        self.logout_button.pack(pady=10, padx=20, fill="x", side="bottom")
        
        # Informação do usuário no rodapé do sidebar
        self.user_info = ctk.CTkLabel(self.sidebar_frame, text="Não conectado")
        self.user_info.pack(pady=(5, 10), side="bottom")
        
        # Container principal (conteúdo)
        self.main_container = ctk.CTkFrame(self, corner_radius=0)
        self.main_container.pack(side="right", fill="both", expand=True)
        
        # Frames para diferentes telas
        self.login_frame = ctk.CTkFrame(self.main_container, corner_radius=0)
        self.dashboard_frame = ctk.CTkFrame(self.main_container, corner_radius=0)
        self.flights_frame = ctk.CTkFrame(self.main_container, corner_radius=0)
        self.bookings_frame = ctk.CTkFrame(self.main_container, corner_radius=0)
        self.reports_frame = ctk.CTkFrame(self.main_container, corner_radius=0)
        self.settings_frame = ctk.CTkFrame(self.main_container, corner_radius=0)
        
        # Inicialmente, o sidebar fica escondido (aparece após o login)
        self.sidebar_frame.pack_forget()

    def show_login_frame(self):
        # Limpar o container principal
        for widget in self.main_container.winfo_children():
            widget.pack_forget()
        
        # Esconder o sidebar
        self.sidebar_frame.pack_forget()
        
        # Configurar frame de login
        self.login_frame = ctk.CTkFrame(self.main_container)
        self.login_frame.pack(fill="both", expand=True)
        
        # Conteúdo do login centralizado
        login_content = ctk.CTkFrame(self.login_frame, width=400, height=350)
        login_content.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título do login
        login_title = ctk.CTkLabel(login_content, text="Sistema de Gerenciamento de Viagens Aéreas", 
                                font=ctk.CTkFont(size=18, weight="bold"))
        login_title.pack(pady=(20, 30))
        
        # Entradas de texto
        username_label = ctk.CTkLabel(login_content, text="Usuário:")
        username_label.pack(anchor="w", padx=30, pady=(10, 0))
        
        self.username_entry = ctk.CTkEntry(login_content, width=340)
        self.username_entry.pack(padx=30, pady=(5, 15))
        
        password_label = ctk.CTkLabel(login_content, text="Senha:")
        password_label.pack(anchor="w", padx=30, pady=(0, 0))
        
        self.password_entry = ctk.CTkEntry(login_content, width=340, show="*")
        self.password_entry.pack(padx=30, pady=(5, 20))
        
        # Botão de login
        login_button = HoverButton(login_content, text="Entrar", width=340, command=self.perform_login)
        login_button.pack(padx=30, pady=10)
        
        # Checkbox "lembrar-me"
        self.remember_var = tk.BooleanVar()
        remember_checkbox = ctk.CTkCheckBox(login_content, text="Lembrar-me", variable=self.remember_var)
        remember_checkbox.pack(padx=30, pady=(5, 20))
        
        register_button = HoverButton(login_content, text="Registrar", width=340, 
                                    fg_color="transparent", border_width=2,
                                    command=lambda: self.show_register_frame())
        register_button.pack(padx=30, pady=(10, 20))

    def show_register_frame(self):
        register_window = ctk.CTkToplevel(self)
        register_window.title("Registro de Novo Usuário")
        register_window.geometry("500x400")
        
        form_frame = ctk.CTkFrame(register_window)
        form_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Campos do formulário
        ctk.CTkLabel(form_frame, text="Nome de usuário:").pack(pady=5)
        self.reg_username = ctk.CTkEntry(form_frame)
        self.reg_username.pack(pady=5)
        
        ctk.CTkLabel(form_frame, text="Senha:").pack(pady=5)
        self.reg_password = ctk.CTkEntry(form_frame, show="*")
        self.reg_password.pack(pady=5)
        
        ctk.CTkLabel(form_frame, text="Confirmar Senha:").pack(pady=5)
        self.reg_confirm = ctk.CTkEntry(form_frame, show="*")
        self.reg_confirm.pack(pady=5)
        
        btn_frame = ctk.CTkFrame(form_frame)
        btn_frame.pack(pady=20)
        
        HoverButton(btn_frame, text="Cancelar", command=register_window.destroy).pack(side="left", padx=10)
        HoverButton(btn_frame, text="Registrar", command=self.perform_register).pack(side="right", padx=10)
        
    def perform_register(self):
        username = self.reg_username.get()
        password = self.reg_password.get()
        confirm = self.reg_confirm.get()
        
        if password != confirm:
            messagebox.showerror("Erro", "As senhas não coincidem!")
            return
            
        if len(password) < 6:
            messagebox.showerror("Erro", "A senha deve ter pelo menos 6 caracteres!")
            return
            
        try:
            cursor = self.db_connection.cursor()
            # Verificar se usuário já existe
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                messagebox.showerror("Erro", "Nome de usuário já existe!")
                return
                
            # Hash da senha
            hashed_pw = hashlib.sha256(password.encode()).hexdigest()
            
            # Inserir novo usuário
            cursor.execute("""
                INSERT INTO users (username, password_hash, access_level)
                VALUES (%s, %s, 'user')
            """, (username, hashed_pw))
            
            self.db_connection.commit()
            messagebox.showinfo("Sucesso", "Registro realizado com sucesso!")
            self.reg_username.get() and self.reg_username.delete(0, 'end')
            self.reg_password.get() and self.reg_password.delete(0, 'end')
            self.reg_confirm.get() and self.reg_confirm.delete(0, 'end')
            
        except mysql.connector.Error as err:
            messagebox.showerror("Erro de Banco de Dados", f"Erro: {err}")
        
    def perform_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
            
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("""
                SELECT user_id, password_hash, access_level 
                FROM users 
                WHERE username = %s AND is_active = TRUE
            """, (username,))
            
            result = cursor.fetchone()
            
            if result:
                user_id, stored_hash, access_level = result
                input_hash = hashlib.sha256(password.encode()).hexdigest()
                
                if input_hash == stored_hash:
                    self.current_user = username
                    self.current_user_id = user_id
                    self.is_admin = (access_level == 'admin')
                    
                    self.user_info.configure(text=f"Admin: {username}" if self.is_admin else f"Usuário: {username}")
                    self.show_dashboard()
                    self.sidebar_frame.pack(side="left", fill="y")
                    return
                    
            messagebox.showerror("Erro", "Credenciais inválidas!")
            
        except mysql.connector.Error as err:
            messagebox.showerror("Erro de Banco de Dados", f"Erro: {err}")
            
    def logout(self):
        self.current_user = None
        self.show_login_frame()

    def show_dashboard(self):
        # Limpar o container principal
        for widget in self.main_container.winfo_children():
            widget.pack_forget()
        
        # Mostrar frame do dashboard
        self.dashboard_frame = ctk.CTkFrame(self.main_container, corner_radius=0)
        self.dashboard_frame.pack(fill="both", expand=True)
        
        # Título da página
        page_title = ctk.CTkLabel(self.dashboard_frame, text="Dashboard", 
                                font=ctk.CTkFont(size=24, weight="bold"))
        page_title.pack(pady=(20, 20), padx=30, anchor="w")
        
        # Cards com informações resumidas
        cards_frame = ctk.CTkFrame(self.dashboard_frame)
        cards_frame.pack(fill="x", padx=30, pady=15)
        
        # Grid para os cards
        cards_frame.columnconfigure(0, weight=1)
        cards_frame.columnconfigure(1, weight=1)
        cards_frame.columnconfigure(2, weight=1)
        cards_frame.columnconfigure(3, weight=1)
        
        # Card 1: Total de voos
        card1 = self.create_stat_card(cards_frame, "Total de Voos", "186", "flight")
        card1.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # Card 2: Voos Hoje
        card2 = self.create_stat_card(cards_frame, "Voos Hoje", "24", "today")
        card2.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Card 3: Reservas
        card3 = self.create_stat_card(cards_frame, "Reservas", "1,256", "booking")
        card3.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        
        # Card 4: Destinos
        card4 = self.create_stat_card(cards_frame, "Destinos", "42", "location")
        card4.grid(row=0, column=3, padx=10, pady=10, sticky="ew")
        
        # Próximos voos
        upcoming_frame = ctk.CTkFrame(self.dashboard_frame)
        upcoming_frame.pack(fill="both", expand=True, padx=30, pady=15)
        
        upcoming_title = ctk.CTkLabel(upcoming_frame, text="Próximos Voos", 
                                    font=ctk.CTkFont(size=18, weight="bold"))
        upcoming_title.pack(pady=10, padx=15, anchor="w")
        
        # Tabela de próximos voos
        columns = ("voo", "origem", "destino", "horario", "status")
        self.flight_tree = ttk.Treeview(upcoming_frame, columns=columns, show="headings", height=10)
        
        # Definir cabeçalhos
        self.flight_tree.heading("voo", text="Voo")
        self.flight_tree.heading("origem", text="Origem")
        self.flight_tree.heading("destino", text="Destino")
        self.flight_tree.heading("horario", text="Horário")
        self.flight_tree.heading("status", text="Status")
        
        # Definir larguras das colunas
        self.flight_tree.column("voo", width=80)
        self.flight_tree.column("origem", width=150)
        self.flight_tree.column("destino", width=150)
        self.flight_tree.column("horario", width=150)
        self.flight_tree.column("status", width=100)
        
        # Adicionar dados de exemplo
        example_flights = [
            ("AC2154", "São Paulo (GRU)", "Rio de Janeiro (GIG)", "10:30", "Em Tempo"),
            ("LA3721", "Brasília (BSB)", "Fortaleza (FOR)", "11:15", "Atrasado"),
            ("G31092", "Curitiba (CWB)", "Porto Alegre (POA)", "12:00", "Em Tempo"),
            ("AD4520", "Recife (REC)", "Salvador (SSA)", "13:45", "Em Tempo"),
            ("JJ3030", "Belém (BEL)", "Manaus (MAO)", "14:30", "Cancelado"),
        ]
        
        for flight in example_flights:
            self.flight_tree.insert("", tk.END, values=flight)
        
        # Adicionar scrollbar
        scrollbar = ttk.Scrollbar(upcoming_frame, orient=tk.VERTICAL, command=self.flight_tree.yview)
        self.flight_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.flight_tree.pack(fill="both", expand=True, padx=15, pady=10)

    def create_stat_card(self, parent, title, value, icon_name=None):
        card = ctk.CTkFrame(parent, height=120)
        
        title_label = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=14))
        title_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        value_label = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=28, weight="bold"))
        value_label.pack(anchor="w", padx=15, pady=(0, 15))
        
        return card

    def show_flights(self):
        # Limpar o container principal
        for widget in self.main_container.winfo_children():
            widget.pack_forget()
        
        # Configurar o frame de voos
        self.flights_frame = ctk.CTkFrame(self.main_container, corner_radius=0)
        self.flights_frame.pack(fill="both", expand=True)
        
        # Título da página
        page_title = ctk.CTkLabel(self.flights_frame, text="Gerenciamento de Voos", 
                                font=ctk.CTkFont(size=24, weight="bold"))
        page_title.pack(pady=(20, 10), padx=30, anchor="w")
        
        # Frame para filtros e ações
        actions_frame = ctk.CTkFrame(self.flights_frame)
        actions_frame.pack(fill="x", padx=30, pady=15)
        
        # Botão para adicionar novo voo
        add_button = HoverButton(actions_frame, text="Adicionar Voo", width=150, command=self.add_flight)
        if self.is_admin:
            add_button.pack(side="left", padx=(0, 10), pady=10)
        
        # Campo de busca
        search_var = tk.StringVar()
        search_entry = ctk.CTkEntry(actions_frame, width=300, placeholder_text="Buscar voos...")
        search_entry.pack(side="left", padx=10, pady=10)
        
        search_button = HoverButton(actions_frame, text="Buscar", width=100)
        search_button.pack(side="left", padx=10, pady=10)
        
        # Filtros de data
        date_label = ctk.CTkLabel(actions_frame, text="Data:")
        date_label.pack(side="left", padx=(20, 5), pady=10)
        
        date_entry = ctk.CTkEntry(actions_frame, width=150)
        date_entry.pack(side="left", padx=5, pady=10)
        date_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        
        # Frame para a tabela de voos
        table_frame = ctk.CTkFrame(self.flights_frame)
        table_frame.pack(fill="both", expand=True, padx=30, pady=15)
        
        # Tabela de voos
        columns = ("id", "codigo", "origem", "destino", "data", "horario", "capacidade", "status", "acoes")
        self.flights_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        
        # Definir cabeçalhos
        self.flights_table.heading("id", text="ID")
        self.flights_table.heading("codigo", text="Código")
        self.flights_table.heading("origem", text="Origem")
        self.flights_table.heading("destino", text="Destino")
        self.flights_table.heading("data", text="Data")
        self.flights_table.heading("horario", text="Horário")
        self.flights_table.heading("capacidade", text="Capacidade")
        self.flights_table.heading("status", text="Status")
        self.flights_table.heading("acoes", text="Ações")
        
        # Definir larguras das colunas
        self.flights_table.column("id", width=50)
        self.flights_table.column("codigo", width=80)
        self.flights_table.column("origem", width=150)
        self.flights_table.column("destino", width=150)
        self.flights_table.column("data", width=100)
        self.flights_table.column("horario", width=80)
        self.flights_table.column("capacidade", width=100)
        self.flights_table.column("status", width=100)
        self.flights_table.column("acoes", width=100)
        
        # Adicionar dados de exemplo
        example_flights = [
            ("1", "AC2154", "São Paulo (GRU)", "Rio de Janeiro (GIG)", "05/03/2025", "10:30", "180/200", "Em Tempo", ""),
            ("2", "LA3721", "Brasília (BSB)", "Fortaleza (FOR)", "05/03/2025", "11:15", "150/150", "Atrasado", ""),
            ("3", "G31092", "Curitiba (CWB)", "Porto Alegre (POA)", "05/03/2025", "12:00", "90/100", "Em Tempo", ""),
            ("4", "AD4520", "Recife (REC)", "Salvador (SSA)", "05/03/2025", "13:45", "120/120", "Em Tempo", ""),
            ("5", "JJ3030", "Belém (BEL)", "Manaus (MAO)", "05/03/2025", "14:30", "145/200", "Cancelado", ""),
            ("6", "AD4521", "Salvador (SSA)", "Recife (REC)", "06/03/2025", "08:30", "50/120", "Agendado", ""),
            ("7", "G31095", "Porto Alegre (POA)", "Florianópolis (FLN)", "06/03/2025", "09:15", "75/100", "Agendado", ""),
            ("8", "LA3728", "Fortaleza (FOR)", "Brasília (BSB)", "06/03/2025", "16:20", "130/150", "Agendado", ""),
        ]
        
        for flight in example_flights:
            if self.is_admin:
                self.flights_table.insert("", tk.END, values=flight)
        else:
            # Remove a coluna de ações para usuários comuns
            self.flights_table.insert("", tk.END, values=flight[:-1])
        
        # Adicionar ações para cada linha
        for item_id in self.flights_table.get_children():
            self.flights_table.set(item_id, "acoes", "✏️ 🗑️")
        
        # Adicionar scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.flights_table.yview)
        self.flights_table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.flights_table.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Adicionar evento de clique nas ações
        self.flights_table.bind("<ButtonRelease-1>", self.handle_table_click)
        
        # Mostra/oculta coluna de ações conforme permissão
        if self.is_admin:
            self.flights_table.heading("acoes", text="Ações")
            self.flights_table.column("acoes", width=100)
        else:
            self.flights_table.heading("acoes", text="")
            self.flights_table.column("acoes", width=0)

    def handle_table_click(self, event):
        if not self.is_admin:
            return
        # Verificar se clicou na coluna de ações
        region = self.flights_table.identify_region(event.x, event.y)
        if region == "cell":
            column = self.flights_table.identify_column(event.x)
            if column == "#9":  # Coluna de ações
                row_id = self.flights_table.identify_row(event.y)
                if row_id:
                    item = self.flights_table.item(row_id)
                    flight_id = item["values"][0]
                    # Verificar qual parte da célula foi clicada (editar ou excluir)
                    if event.x > self.flights_table.winfo_x() + self.flights_table.column("acoes", "width") - 20:
                        self.delete_flight(flight_id)
                    else:
                        self.edit_flight(flight_id)

    def add_flight(self):
        if not self.is_admin:
            messagebox.showerror("Permissão Negada", "Apenas administradores podem adicionar voos")
            return
        
        # Janela para adicionar novo voo
        add_window = ctk.CTkToplevel(self)
        add_window.title("Adicionar Novo Voo")
        add_window.geometry("600x500")
        add_window.transient(self)  # Define a janela como dependente da principal
        add_window.grab_set()  # Torna a janela modal
        
        # Título
        title_label = ctk.CTkLabel(add_window, text="Adicionar Novo Voo", 
                                font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=(20, 30))
        
        # Frame para o formulário
        form_frame = ctk.CTkFrame(add_window)
        form_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        # Campos do formulário
        # Código do voo
        code_label = ctk.CTkLabel(form_frame, text="Código do Voo:")
        code_label.grid(row=0, column=0, padx=15, pady=10, sticky="w")
        
        code_entry = ctk.CTkEntry(form_frame, width=150)
        code_entry.grid(row=0, column=1, padx=15, pady=10, sticky="w")
        
        # Origem
        origin_label = ctk.CTkLabel(form_frame, text="Origem:")
        origin_label.grid(row=1, column=0, padx=15, pady=10, sticky="w")
        
        origin_entry = ctk.CTkEntry(form_frame, width=250)
        origin_entry.grid(row=1, column=1, padx=15, pady=10, sticky="w")
        
        # Destino
        dest_label = ctk.CTkLabel(form_frame, text="Destino:")
        dest_label.grid(row=2, column=0, padx=15, pady=10, sticky="w")
        
        dest_entry = ctk.CTkEntry(form_frame, width=250)
        dest_entry.grid(row=2, column=1, padx=15, pady=10, sticky="w")
        
        # Data
        date_label = ctk.CTkLabel(form_frame, text="Data:")
        date_label.grid(row=3, column=0, padx=15, pady=10, sticky="w")
        
        date_entry = ctk.CTkEntry(form_frame, width=150)
        date_entry.grid(row=3, column=1, padx=15, pady=10, sticky="w")
        date_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        
        # Horário
        time_label = ctk.CTkLabel(form_frame, text="Horário:")
        time_label.grid(row=4, column=0, padx=15, pady=10, sticky="w")
        
        time_entry = ctk.CTkEntry(form_frame, width=150)
        time_entry.grid(row=4, column=1, padx=15, pady=10, sticky="w")
        time_entry.insert(0, "00:00")
        
        # Capacidade
        capacity_label = ctk.CTkLabel(form_frame, text="Capacidade:")
        capacity_label.grid(row=5, column=0, padx=15, pady=10, sticky="w")
        
        capacity_entry = ctk.CTkEntry(form_frame, width=150)
        capacity_entry.grid(row=5, column=1, padx=15, pady=10, sticky="w")
        capacity_entry.insert(0, "200")
        
        # Status
        status_label = ctk.CTkLabel(form_frame, text="Status:")
        status_label.grid(row=6, column=0, padx=15, pady=10, sticky="w")
        
        status_options = ["Agendado", "Em Tempo", "Atrasado", "Cancelado"]
        status_var = tk.StringVar(value=status_options[0])
        status_combobox = ctk.CTkComboBox(form_frame, values=status_options, variable=status_var, width=150)
        status_combobox.grid(row=6, column=1, padx=15, pady=10, sticky="w")
        
        # Botões
        button_frame = ctk.CTkFrame(add_window)
        button_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        cancel_button = HoverButton(button_frame, text="Cancelar", width=100, fg_color="transparent", 
                                    border_width=2, text_color=("gray10", "gray90"),
                                    command=lambda: add_window.destroy())
        cancel_button.pack(side="left", padx=10, pady=10)
        
        save_button = HoverButton(button_frame, text="Salvar", width=100, 
                                command=lambda: self.save_flight(add_window, code_entry.get(), origin_entry.get(),
                                                                dest_entry.get(), date_entry.get(), time_entry.get(),
                                                                capacity_entry.get(), status_combobox.get()))
        save_button.pack(side="right", padx=10, pady=10)
        
    def manage_users(self):
        if not self.is_admin:
            return
            
        manage_window = ctk.CTkToplevel(self)
        manage_window.title("Gerenciamento de Usuários")
        manage_window.geometry("800x600")    

    def edit_flight(self, flight_id):
        if not self.is_admin:
            messagebox.showerror("Permissão Negada", "Apenas administradores podem editar voos")
            return
        
        # Aqui implementaríamos a edição de um voo existente
        # Semelhante ao add_flight, mas preenchendo os campos com dados existentes
        messagebox.showinfo("Editar Voo", f"Editando voo ID: {flight_id}")
        
    def delete_flight(self, flight_id):
        if not self.is_admin:
            messagebox.showerror("Permissão Negada", "Apenas administradores podem excluir voos")
            return
        if messagebox.askyesno("Confirmar Exclusão", f"Deseja realmente excluir o voo ID: {flight_id}?"):
            # Aqui implementaríamos a exclusão no banco de dados
            messagebox.showinfo("Excluir Voo", f"Voo ID: {flight_id} foi excluído com sucesso!")
    
    def save_flight(self, window, code, origin, dest, date, time, capacity, status):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("""
                INSERT INTO flights (flight_code, departure_city, arrival_city, 
                scheduled_departure, scheduled_arrival, capacity, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (code, origin, dest, 
                datetime.strptime(f"{date} {time}", "%d/%m/%Y %H:%M"), 
                datetime.strptime(f"{date} {time}", "%d/%m/%Y %H:%M") + pytz.timezone('America/Sao_Paulo').localize(datetime.strptime(f"{date} {time}", "%d/%m/%Y %H:%M")).astimezone(pytz.utc).utcoffset(),
                capacity, status))
            
            self.db_connection.commit()
            messagebox.showinfo("Sucesso", "Voo salvo com sucesso!")
            window.destroy()
            self.show_flights()  # Recarrega a lista de voos
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar voo: {str(e)}")

    def show_bookings(self):
        # Limpar o container principal
        for widget in self.main_container.winfo_children():
            widget.pack_forget()
        
        # Configurar o frame de reservas
        self.bookings_frame = ctk.CTkFrame(self.main_container, corner_radius=0)
        self.bookings_frame.pack(fill="both", expand=True)
        
        # Título da página
        page_title = ctk.CTkLabel(self.bookings_frame, text="Gerenciamento de Reservas", 
                                font=ctk.CTkFont(size=24, weight="bold"))
        page_title.pack(pady=(20, 20), padx=30, anchor="w")
        
        # Implementação básica - seria expandido em um sistema real
        message = ctk.CTkLabel(self.bookings_frame, text="Funcionalidade de Reservas em Desenvolvimento", 
                            font=ctk.CTkFont(size=16))
        message.pack(pady=100)

    def show_reports(self):
        # Limpar o container principal
        for widget in self.main_container.winfo_children():
            widget.pack_forget()
        
        # Configurar o frame de relatórios
        self.reports_frame = ctk.CTkFrame(self.main_container, corner_radius=0)
        self.reports_frame.pack(fill="both", expand=True)
        
        # Título da página
        page_title = ctk.CTkLabel(self.reports_frame, text="Relatórios", 
                                font=ctk.CTkFont(size=24, weight="bold"))
        page_title.pack(pady=(20, 20), padx=30, anchor="w")
        
        # Implementação básica - seria expandido em um sistema real
        message = ctk.CTkLabel(self.reports_frame, text="Funcionalidade de Relatórios em Desenvolvimento", 
                            font=ctk.CTkFont(size=16))
        message.pack(pady=100)

    def show_settings(self):
        # Limpar o container principal
        for widget in self.main_container.winfo_children():
            widget.pack_forget()
        
        # Configurar o frame de configurações
        self.settings_frame = ctk.CTkFrame(self.main_container, corner_radius=0)
        self.settings_frame.pack(fill="both", expand=True)
        
        # Título da página
        page_title = ctk.CTkLabel(self.settings_frame, text="Configurações", 
                                font=ctk.CTkFont(size=24, weight="bold"))
        page_title.pack(pady=(20, 20), padx=30, anchor="w")
        
        # Frame para as configurações
        settings_container = ctk.CTkFrame(self.settings_frame)
        settings_container.pack(fill="both", expand=True, padx=30, pady=15)
        
        # Configurações de aparência
        appearance_label = ctk.CTkLabel(settings_container, text="Aparência", 
                                        font=ctk.CTkFont(size=18, weight="bold"))
        appearance_label.pack(pady=10, padx=15, anchor="w")
        
        # Modo de aparência
        appearance_frame = ctk.CTkFrame(settings_container)
        appearance_frame.pack(fill="x", padx=15, pady=10)

if __name__ == "__main__":
    app = AirTravelApp()
    app.mainloop()