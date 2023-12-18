from qiskit import QuantumRegister, QuantumCircuit
import random

class Hacker:
    def __init__(self, name):
        self.name = name

    # hacker tries to get money information from the bank
    # given that somehow information about uuid is leaked
    # general function for hacking, takes in a method that
    # returns a quantum circuit and based on that tries to verify
    # the money
    def hack(self, uuid, q_hack_method, n_qubits, bank, n_quantum_states=4):
        qc = q_hack_method(n_qubits, n_quantum_states)
        print(qc)
        was_successful = bank.verify_money((uuid, qc))
        return was_successful, qc
    
    # method for generating quantum circuit that will be used
    def qc_generator(self, n_qubits, n_quantum_states):

        # hidden tecnique for generating states that will be used
        rand_nums = [(len(self.name)+ random.randint(0, 3))%n_quantum_states for i in range(n_qubits)]
        
        qreg = QuantumRegister(n_qubits)
        qc = QuantumCircuit(qreg)
        for i in range(n_qubits):
            # |0> 
            if rand_nums[i] == 0:
                pass

            # |1>
            elif rand_nums[i] == 1:
                qc.x(qreg[i])

            # |+>
            elif rand_nums[i] == 2:
                qc.h(qreg[i])

            # |->
            elif rand_nums[i] == 3:
                qc.x(qreg[i])
                qc.h(qreg[i])

            # |i+>
            elif rand_nums[i] == 4:
                qc.h(qreg[i])
                qc.s(qreg[i])

            # |i->
            elif rand_nums[i] == 5:
                qc.x(qreg[i])
                qc.h(qreg[i])
                qc.s(qreg[i])

        return qc
    
if __name__ == "__main__":
    from q_bank import Quantum_Bank
    # Create a bank
    bank = Quantum_Bank()

    # Create a hacker
    bob = Hacker("Bob")

    # Bob tries to hack the bank
    was_successful, qc = bob.hack(1002, bob.qc_generator, 1, bank)

    # verify if the hack was successful
    print(f'{bob.name} was successful: {was_successful}')