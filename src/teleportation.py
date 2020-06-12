from qiskit import *
from qiskit.visualization import plot_histogram as plot_h, plot_bloch_vector as plot_bv, plot_bloch_multivector as plot_bmv
from math import sqrt, pi
from qiskit.quantum_info import random_statevector
from qiskit.extensions import Initialize

s_backend = Aer.get_backend('statevector_simulator')
q_backend = Aer.get_backend('qasm_simulator')
u_backend = Aer.get_backend('unitary_simulator')

def create_circuit():
    
    psi = random_statevector(2)
    init_gate = Initialize(psi.data)

    qr = QuantumRegister(3)
    crz = ClassicalRegister(1)
    crx = ClassicalRegister(1)

    qc = QuantumCircuit(qr, crz, crx)
    
    qc.initialize(psi.data, qr[0])
    
    return [qc, qr, crz, crx]

def create_bell_state(qc, b1, b2):
    """ Assumes that the starting states are 0 and 0, doesn't work otherwise """
    qc.h(b1)
    qc.cx(b1,b2)


def alice_gates(qc, psi, b1):
    qc.cx(psi, b1)
    qc.h(psi)

def measure_and_send(qc, psi, b1, crx, crz):
    qc.measure(psi, crz)
    qc.measure(b1, crx)

def bob_gates(qc, b2, crx, crz):
    qc.x(b2).c_if(crx, 1)
    qc.z(b2).c_if(crz, 1)

def main():
    qc, qr, crz, crx = create_circuit()
    psi = qr[0]
    b1 = qr[1]
    b2 = qr[2]

    print("Input statevector: ")
    print(execute(qc, s_backend).result().get_statevector())

    create_bell_state(qc, b1, b2)
    alice_gates(qc, psi, b1)
    measure_and_send(qc, psi, b1, crx, crz)
    bob_gates(qc, b2, crx, crz)

    print("Output statevector: ")
    print(execute(qc, s_backend).result().get_statevector())

if __name__ == '__main__':
    main()