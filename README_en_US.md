# Air Travel Management System

## 📌 Project Overview

### Overview
A comprehensive air travel management system designed to handle flight operations, bookings, passengers, and user management. Features an intuitive interface with distinct functionalities for administrators and regular users, including flight registration, booking tracking, and basic reporting.

### Objectives
- Automate airline operations management.
- Provide a centralized platform for flight bookings and control.
- Implement role-based access control (admin/user).

### Implemented Features
- **User Authentication**: Login with access levels (admin/user).
- **Flight Management**:
  - Add/edit/delete flights (admin only).
  - View flight statuses (scheduled, in-route, completed).
- **Dashboard**: Real-time flight statistics, bookings, and destinations.
- **Bookings**: Basic interface for future implementation.
- **Reports**: Section under development for data analysis.

---

## 🛠️ Installation Guide

### Prerequisites
- Python 3.10 or higher
- XAMPP (for local MySQL database)
- Python Libraries:
  ```bash
  pip install customtkinter pywinstyles mysql-connector-python pytz

```markdown
# Air Travel Management System

## 📌 Project Overview

### Overview
A comprehensive air travel management system designed to handle flight operations, bookings, passengers, and user management. Features an intuitive interface with distinct functionalities for administrators and regular users, including flight registration, booking tracking, and basic reporting.

### Objectives
- Automate airline operations management.
- Provide a centralized platform for flight bookings and control.
- Implement role-based access control (admin/user).

### Implemented Features
- **User Authentication**: Login with access levels (admin/user).
- **Flight Management**:
  - Add/edit/delete flights (admin only).
  - View flight statuses (scheduled, in-route, completed).
- **Dashboard**: Real-time flight statistics, bookings, and destinations.
- **Bookings**: Basic interface for future implementation.
- **Reports**: Section under development for data analysis.

---

## 🛠️ Installation Guide

### Prerequisites
- Python 3.10 or higher
- XAMPP (for local MySQL database)
- Python Libraries:
  ```bash
  pip install customtkinter pywinstyles mysql-connector-python pytz
  ```

### Step-by-Step Setup
1. **Configure Database**:
   - Start Apache and MySQL via XAMPP.
   - Access `http://localhost/phpmyadmin`.
   - Create a database named `air_travel_management`.
   - Import the `air_travel_management.sql` file (via "Import" tab).

2. **Set Up Python Environment**:
   - Clone the repository:
     ```bash
     git clone https://github.com/your-username/air_travel_management.git
     ```
   - Navigate to the project folder:
     ```bash
     cd air_travel_management
     ```

3. **Run the Application**:
   ```bash
   python main.py
   ```

---

## 📖 User Manual

### Login
- **Default Admin**:
  - Username: `admin`
  - Password: `123` (hashed in the code; change via database for production).
- **Regular Users**: Register via the "Register" button.

### Navigation
- **Dashboard**:
  - View quick stats and upcoming flights.
- **Flights** (Admin only):
  - Add new flights with details like origin, destination, and time.
  - Edit or delete flights using `✏️` or `🗑️` in the table.
- **Bookings** (Under development):
  - Placeholder interface for future features.
- **Settings**:
  - Adjust theme (light/dark) and preferences.

---

## ⚙️ Configuration Guide

### Database
- Modify credentials in `main.py` (line 68):
  ```python
  connection = mysql.connector.connect(
      host="localhost",
      user="root",       # Update if needed
      password="",       # Add your MySQL password
      database="air_travel_management"
  )
  ```

### UI Customization
- Change the theme in `main.py` (lines 18-19):
  ```python
  ctk.set_appearance_mode("dark")  # Options: "System", "Dark", "Light"
  ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"
  ```

---

## 👤 Credits

### Developer
- **Vítor Luciano Cardoso Noe**  
  Individually developed for academic purposes.

### References
- [CustomTkinter Documentation](https://customtkinter.tomschimansky.com/)
- [MySQL Connector/Python](https://dev.mysql.com/doc/connector-python/en/)

---

**Note**: This is a simplified version. For production use, add data validations, robust password encryption, and additional testing.

---

### Repository Files
- `air_travel_management.sql`: Database schema.
- `main.py`: Application source code.
- `README.md`: Project documentation (this file).

### Additional Instructions
1. Ensure MySQL is running via XAMPP before executing `main.py`.
2. To reset passwords or add admins, edit the `users` table directly in phpMyAdmin.
3. The default admin password (`123`) is hashed as `240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9`. Change it in the database for enhanced security.
