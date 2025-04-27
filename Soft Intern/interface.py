import tkinter as tk
from tkinter import ttk, messagebox
import requests

# API configuration
API_BASE_URL = "http://localhost:5000"

class HealthProgramApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Health Program Management System")
        self.root.geometry("1000x700")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_program_tab()
        self.register_client_tab()
        self.enroll_client_tab()
        self.search_client_tab()
        self.view_profile_tab()
        self.api_info_tab()
        
    def create_program_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Create Health Program")
        
        # Program Name
        tk.Label(tab, text="Program Name:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.program_name_entry = tk.Entry(tab, width=40)
        self.program_name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Program Description
        tk.Label(tab, text="Description:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.program_desc_entry = tk.Text(tab, width=40, height=5)
        self.program_desc_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Create Button
        create_btn = tk.Button(tab, text="Create Program", command=self.create_program)
        create_btn.grid(row=2, column=1, pady=20, sticky=tk.E)
        
    def register_client_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Register Client")
        
        # Client ID
        tk.Label(tab, text="Client ID:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.client_id_entry = tk.Entry(tab, width=40)
        self.client_id_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Name
        tk.Label(tab, text="Full Name:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.client_name_entry = tk.Entry(tab, width=40)
        self.client_name_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Age
        tk.Label(tab, text="Age:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        self.client_age_entry = tk.Entry(tab, width=40)
        self.client_age_entry.grid(row=2, column=1, padx=10, pady=10)
        
        # Gender
        tk.Label(tab, text="Gender:").grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        self.client_gender_var = tk.StringVar()
        self.client_gender_combobox = ttk.Combobox(tab, width=37, textvariable=self.client_gender_var)
        self.client_gender_combobox['values'] = ('Male', 'Female', 'Other')
        self.client_gender_combobox.grid(row=3, column=1, padx=10, pady=10)
        
        # Register Button
        register_btn = tk.Button(tab, text="Register Client", command=self.register_client)
        register_btn.grid(row=4, column=1, pady=20, sticky=tk.E)
        
    def enroll_client_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Enroll Client")
        
        # Client ID
        tk.Label(tab, text="Client ID:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.enroll_client_id_entry = tk.Entry(tab, width=40)
        self.enroll_client_id_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Program Name
        tk.Label(tab, text="Program Name:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.enroll_program_name_entry = tk.Entry(tab, width=40)
        self.enroll_program_name_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Enroll Button
        enroll_btn = tk.Button(tab, text="Enroll Client", command=self.enroll_client)
        enroll_btn.grid(row=2, column=1, pady=20, sticky=tk.E)
        
    def search_client_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Search Client")
        
        # Search Client ID
        tk.Label(tab, text="Client ID:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.search_client_id_entry = tk.Entry(tab, width=40)
        self.search_client_id_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Search Button
        search_btn = tk.Button(tab, text="Search", command=self.search_client)
        search_btn.grid(row=0, column=2, padx=10, pady=10)
        
        # Results Frame
        results_frame = tk.LabelFrame(tab, text="Client Details", padx=10, pady=10)
        results_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky=tk.W+tk.E)
        
        # Result Text
        self.search_result_text = tk.Text(results_frame, width=80, height=10, state=tk.DISABLED)
        self.search_result_text.pack()
        
    def view_profile_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="View Client Profile")
        
        # Client ID
        tk.Label(tab, text="Client ID:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.view_client_id_entry = tk.Entry(tab, width=40)
        self.view_client_id_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # View Button
        view_btn = tk.Button(tab, text="View Profile", command=self.view_profile)
        view_btn.grid(row=0, column=2, padx=10, pady=10)
        
        # Profile Frame
        profile_frame = tk.LabelFrame(tab, text="Client Profile", padx=10, pady=10)
        profile_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky=tk.W+tk.E)
        
        # Profile Text
        self.profile_text = tk.Text(profile_frame, width=80, height=15, state=tk.DISABLED)
        self.profile_text.pack()
        
    def api_info_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="API Information")
        
        # API Info
        info_text = """API Endpoints:
        
1. Create Program: POST /create_program
   - Parameters: name, description
   
2. Register Client: POST /register_client
   - Parameters: client_id, name, age, gender
   
3. Enroll Client: POST /enroll_client
   - Parameters: client_id, program_name
   
4. Search Client: GET /search_client?client_id=<id>
   
5. View Profile: GET /view_profile/<client_id>
"""

        text_widget = tk.Text(tab, wrap=tk.WORD, padx=10, pady=10)
        text_widget.insert(tk.END, info_text)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
    def create_program(self):
        name = self.program_name_entry.get()
        description = self.program_desc_entry.get("1.0", tk.END).strip()
        
        if not name or not description:
            messagebox.showerror("Error", "Program name and description are required!")
            return
            
        try:
            response = requests.post(
                f"{API_BASE_URL}/create_program",
                json={"name": name, "description": description}
            )
            
            if response.status_code == 201:
                messagebox.showinfo("Success", response.json()["message"])
                self.program_name_entry.delete(0, tk.END)
                self.program_desc_entry.delete("1.0", tk.END)
            else:
                messagebox.showerror("Error", response.json()["error"])
        except requests.exceptions.RequestException:
            messagebox.showerror("Error", "Could not connect to the server!")
            
    def register_client(self):
        client_id = self.client_id_entry.get()
        name = self.client_name_entry.get()
        age = self.client_age_entry.get()
        gender = self.client_gender_var.get()
        
        if not client_id or not name or not age or not gender:
            messagebox.showerror("Error", "All fields are required!")
            return
            
        try:
            response = requests.post(
                f"{API_BASE_URL}/register_client",
                json={
                    "client_id": client_id,
                    "name": name,
                    "age": age,
                    "gender": gender
                }
            )
            
            if response.status_code == 201:
                messagebox.showinfo("Success", response.json()["message"])
                self.clear_client_fields()
            else:
                messagebox.showerror("Error", response.json()["error"])
        except requests.exceptions.RequestException:
            messagebox.showerror("Error", "Could not connect to the server!")
            
    def clear_client_fields(self):
        self.client_id_entry.delete(0, tk.END)
        self.client_name_entry.delete(0, tk.END)
        self.client_age_entry.delete(0, tk.END)
        self.client_gender_combobox.set('')
        
    def enroll_client(self):
        client_id = self.enroll_client_id_entry.get()
        program_name = self.enroll_program_name_entry.get()
        
        if not client_id or not program_name:
            messagebox.showerror("Error", "Client ID and Program Name are required!")
            return
            
        try:
            response = requests.post(
                f"{API_BASE_URL}/enroll_client",
                json={
                    "client_id": client_id,
                    "program_name": program_name
                }
            )
            
            if response.status_code == 200:
                messagebox.showinfo("Success", response.json()["message"])
                self.enroll_client_id_entry.delete(0, tk.END)
                self.enroll_program_name_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", response.json()["error"])
        except requests.exceptions.RequestException:
            messagebox.showerror("Error", "Could not connect to the server!")
            
    def search_client(self):
        client_id = self.search_client_id_entry.get()
        
        if not client_id:
            messagebox.showerror("Error", "Client ID is required!")
            return
            
        try:
            response = requests.get(
                f"{API_BASE_URL}/search_client",
                params={"client_id": client_id}
            )
            
            self.search_result_text.config(state=tk.NORMAL)
            self.search_result_text.delete("1.0", tk.END)
            
            if response.status_code == 200:
                client_data = response.json()
                formatted_text = f"ID: {client_data['client_id']}\n"
                formatted_text += f"Name: {client_data['name']}\n"
                formatted_text += f"Age: {client_data['age']}\n"
                formatted_text += f"Gender: {client_data['gender']}\n"
                formatted_text += "Enrolled Programs:\n"
                for program in client_data['enrolled_programs']:
                    formatted_text += f" - {program}\n"
                self.search_result_text.insert(tk.END, formatted_text)
            else:
                self.search_result_text.insert(tk.END, response.json()["error"])
                
            self.search_result_text.config(state=tk.DISABLED)
        except requests.exceptions.RequestException:
            messagebox.showerror("Error", "Could not connect to the server!")
            
    def view_profile(self):
        client_id = self.view_client_id_entry.get()
        
        if not client_id:
            messagebox.showerror("Error", "Client ID is required!")
            return
            
        try:
            response = requests.get(f"{API_BASE_URL}/view_profile/{client_id}")
            
            self.profile_text.config(state=tk.NORMAL)
            self.profile_text.delete("1.0", tk.END)
            
            if response.status_code == 200:
                client_data = response.json()
                formatted_text = f"Client Profile\n{'='*30}\n\n"
                formatted_text += f"ID: {client_data['client_id']}\n"
                formatted_text += f"Name: {client_data['name']}\n"
                formatted_text += f"Age: {client_data['age']}\n"
                formatted_text += f"Gender: {client_data['gender']}\n\n"
                formatted_text += "Enrolled Programs:\n"
                for program in client_data['enrolled_programs']:
                    formatted_text += f" - {program}\n"
                self.profile_text.insert(tk.END, formatted_text)
            else:
                self.profile_text.insert(tk.END, response.json()["error"])
                
            self.profile_text.config(state=tk.DISABLED)
        except requests.exceptions.RequestException:
            messagebox.showerror("Error", "Could not connect to the server!")

if __name__ == "__main__":
    root = tk.Tk()
    app = HealthProgramApp(root)
    root.mainloop()