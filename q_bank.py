from qiskit import QuantumRegister, QuantumCircuit, Aer, transpile, assemble
import numpy as np
import json

class Quantum_Bank:
    def __init__(self, storage_path='bank_safe.json', n_quantum_states=4):
        self.storage_path = storage_path
        self.n_quantum_states = n_quantum_states
        self.current_uuid = 1000
        self.storage = []
        self.laod_from_storage()

    def laod_from_storage(self):
        # Load money from JSON file
        try:
            with open(self.storage_path, 'r') as f:
                self.storage = json.load(f)
        except:
            pass

        # find the largest uuid
        has_entry = False
        for money in self.storage:
            has_entry = True
            if money["uuid"] > self.current_uuid:
                self.current_uuid = money["uuid"]
        
        if has_entry:
            self.current_uuid += 1



    def _true_random(self, n_numbers=1):

        # Calculate the number of qubits needed
        n_qubits = (self.n_quantum_states - 1).bit_length()

        # Create a quantum register of n qubits
        qreg = QuantumRegister(n_qubits)
        qc = QuantumCircuit(qreg)

        # Apply Hadamard gates to all qubits
        qc.h(qreg)

        # Measure all qubits
        qc.measure_all()

        # Simulate the circuit
        simulator = Aer.get_backend('qasm_simulator')
        job = assemble(transpile(qc, simulator), shots=n_numbers)
        result = simulator.run(job).result()
        counts = result.get_counts()

        # Convert the outputs to an integers
        rnd_list = []
        for rand, count in counts.items():
            rnd_list += [int(rand, base=2) for i in range(count)]

        return rnd_list
    

    def create_money(self, n_qubits=1):
        
        qreg = QuantumRegister(n_qubits)
        qc = QuantumCircuit(qreg)

        true_randoms = self._true_random(n_qubits)

        for i in range(n_qubits):
            # |0> 
            if true_randoms[i] == 0:
                pass

            # |1>
            elif true_randoms[i] == 1:
                qc.x(qreg[i])

            # |+>
            elif true_randoms[i] == 2:
                qc.h(qreg[i])

            # |->
            elif true_randoms[i] == 3:
                qc.x(qreg[i])
                qc.h(qreg[i])

            # |i+>
            elif true_randoms[i] == 4:
                qc.h(qreg[i])
                qc.s(qreg[i])

            # |i->
            elif true_randoms[i] == 5:
                qc.x(qreg[i])
                qc.h(qreg[i])
                qc.s(qreg[i])

        return qc

    def issue_money(self, n_qubits=1):
        qc = self.create_money(n_qubits)
        s = self.current_uuid
        self.current_uuid += 1
        self.store_money((s, qc))
        return s, qc

    def verify_money(self, sq_pair):
        s, qc = sq_pair

        # Format gate information for the given quantum circuit
        gate_info = []
        for instr, qargs, cargs in qc.data:
            gate_info.append({
                "name": instr.name,
                "qargs": [q.index for q in qargs]
            })

        # Check if the given quantum circuit is in the bank
        for money in self.storage:
            if money["uuid"] == s:
                if money["gate_info"] == gate_info:
                    return True
        return False

    def store_money(self, sq_pair):
        s, qc = sq_pair

        # Format gate information for a JSON file
        gate_info = []
        for instr, qargs, cargs in qc.data:
            gate_info.append({
                "name": instr.name,
                "qargs": [q.index for q in qargs]
            })

        money_info = {
            "uuid": s,
            "gate_info": gate_info
        }
        
        # Save new entry to the JSON file
        self.storage.append(money_info)
        with open(self.storage_path, 'w') as f:
            json.dump(self.storage, f)


if __name__ == "__main__":
    qb = Quantum_Bank()
    s, qc = qb.issue_money(1)
    print(qb.verify_money((s, qc)))