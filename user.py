class User:
    def __init__(self, name, bank):
        self.name = name
        self.bank = bank
        self.money = []

    def request_money(self, n_qubits):
        s, qc = self.bank.issue_money(n_qubits)
        self.money.append(s)
        return s, qc

    def verify_money(self, sq_pair):
        return self.bank.verify_money(sq_pair)
    

if __name__ == "__main__":
    from q_bank import Quantum_Bank
    # Create a bank
    bank = Quantum_Bank()

    # Create a user
    alice = User("Alice", bank)

    # Alice requests money from the bank
    sq_pair = alice.request_money(1)

    # Alice verifies her money
    print(alice.verify_money(sq_pair))