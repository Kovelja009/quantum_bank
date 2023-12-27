import tkinter as tk
from tkinter import ttk  # Import ttk module for Combobox
from qiskit import QuantumRegister, QuantumCircuit
from q_bank import Quantum_Bank
from user import User
from hacker import Hacker

class BankApp:
    def __init__(self, root, bank, user, hacker, n_qubits=1):
        self.root = root
        self.root.title("Bank, User, and Hacker Interface")
        self.bank_frame = tk.Frame(self.root, bg='lightblue', width=700, height=700)
        self.bank_frame.grid(row=0, column=0, padx=10, pady=100)

        # Create a canvas and scrollbar for the bank safe view
        self.canvas = tk.Canvas(self.bank_frame, bg='lightblue', highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.bank_frame, orient='vertical', command=self.canvas.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.canvas.pack(side='left', fill='both', expand=True)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.inner_frame = tk.Frame(self.canvas, bg='lightblue')
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor='nw')


        self.user_frame = tk.Frame(self.root, bg='lightgreen', width=300, height=700)
        self.user_frame.grid(row=0, column=1, padx=10, pady=100)

        self.hacker_frame = tk.Frame(self.root, bg='lightcoral', width=300, height=700)
        self.hacker_frame.grid(row=0, column=2, padx=10, pady=100)


        self.n_qubits = n_qubits

        # Bank Section
        self.bank = bank
        self.bank_label = tk.Label(self.bank_frame, text="Bank Safe", bg='lightblue')
        self.bank_label.pack()
        self.show_bank_safe()

        # User Section
        self.user = user
        self.user_label = tk.Label(self.user_frame, text=f"User: {self.user.name}", bg='lightgreen')
        self.user_label.pack()

        self.request_button = tk.Button(self.user_frame, text="Request Money", command=self.request_money)
        self.request_button.pack(pady=10)

        self.verify_label = tk.Label(self.user_frame, text="Choose id to verify:", bg='lightgreen')
        self.verify_label.pack()

        self.money_options = [data['uuid'] for data in self.user.money]
        self.money_var = tk.StringVar()
        self.money_dropdown = ttk.Combobox(self.user_frame, textvariable=self.money_var, values=self.money_options)
        self.money_dropdown.pack(pady=10, padx=10)

        self.verify_button = tk.Button(self.user_frame, text="Verify", command=self.verify_money)
        self.verify_button.pack()

        # Hacker Section
        self.hacker = hacker
        self.hacker_label = tk.Label(self.hacker_frame, text=f"Hacker: {self.hacker.name}", bg='lightcoral')
        self.hacker_label.pack()

        self.hack_label = tk.Label(self.hacker_frame, text="Choose id to hack:", bg='lightcoral')
        self.hack_label.pack(pady=10)

        self.uuid_entry = tk.Entry(self.hacker_frame)
        self.uuid_entry.pack(padx=10)


        self.hack_button = tk.Button(self.hacker_frame, text="Try to Hack", command=self.hack_bank)
        self.hack_button.pack(pady=10)
        self.hack_qubits_label = tk.Label(self.hacker_frame, text="", bg='lightcoral')
        self.hack_qubits_label.pack(pady=10)
    
    
    def show_bank_safe(self):
        # Clear the inner frame by destroying its children
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        # Create and display new labels in the inner frame
        for money in self.bank.storage:
            qreg = QuantumRegister(self.n_qubits)
            qc = QuantumCircuit(qreg)
            for gate in money['gate_info']:
                gate_name = gate["name"]
                qargs = gate["qargs"]
                idx = int(qargs[0])

                if gate_name == "x":
                    qc.x(qreg[idx])
                elif gate_name == "s":
                    qc.s(qreg[idx])
                elif gate_name == "h":
                    qc.h(qreg[idx])

            label = tk.Label(self.inner_frame, text=f"\nUUID: {money['uuid']}\n{qc}", bg='lightblue')
            label.pack(anchor='w')

        # Update the canvas and scroll region
        self.inner_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    def request_money(self):
        self.user.request_money(self.n_qubits)
        self.money_options = [data[0] for data in self.user.money]
        self.money_var.set(self.money_options[0])
        self.money_dropdown.config(values=self.money_options)
        self.show_bank_safe()

    def verify_money(self):
        if self.money_var.get() == "":
            self.verify_label.config(text="Please select a money id!")
            return
        selected_money = int(self.money_var.get())
        sq_pair = None
        for money in self.user.money:
            if money[0] == selected_money:
                sq_pair = money
                break

        if sq_pair == None:
            self.verify_label.config(text="Invalid money id!")
            return
        if self.user.verify_money(sq_pair):
            # make popup
            self.verify_label.config(text="Money is valid!")
        else:
            self.verify_label.config(text="Money is invalid!")


    def hack_bank(self):
        # Get the uuid from the entry
        if self.uuid_entry.get() == "":
            self.hack_qubits_label.config(text="Please enter a money id!")
            return

        uuid = int(self.uuid_entry.get())
        if uuid == "":
            self.hack_qubits_label.config(text="Please enter a money id!")
            return
        
        success, qc  = self.hacker.hack(uuid, self.hacker.qc_generator, self.n_qubits, self.bank)
        self.hack_qubits_label.config(text=f"Hacking was successful: {success}\n Qubit generated: \n{qc}")

        pass

if __name__ == "__main__":
    root = tk.Tk()
    bank = Quantum_Bank()
    user = User("Adam", bank)
    hacker = Hacker("Eve")
    app = BankApp(root, bank=bank, user=user, hacker=hacker)
    root.mainloop()
