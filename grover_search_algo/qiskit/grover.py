# -*- coding: utf-8 -*-

import numpy as np
from qiskit import QuantumCircuit
from run_circuit import get_current_state, get_qc_simulation_results, get_qc_actual_results
from qiskit.visualization import plot_histogram

n = 2
grover_circuit = QuantumCircuit(n) # if we use grover_circuit.measure_all() below
# grover_circuit = QuantumCircuit(n, n) # if we grover_circuit.measure() below

for qubit in range(n):
    grover_circuit.h(qubit)

for qubit in range(n):
    grover_circuit.x(qubit)

grover_circuit.cz(0, 1)

# Apply the Oracle for |00⟩ :
for qubit in range(n):
    grover_circuit.x(qubit)

for qubit in range(n):
    grover_circuit.h(qubit)

for qubit in range(n):
    grover_circuit.z(qubit)
grover_circuit.cz(0, 1)

for qubit in range(n):
    grover_circuit.h(qubit)

# # The code to show the current circuit, this line can be put anywhere in code above to visualize the circuit at that point
grover_circuit.draw('mpl')

# The code to get the current state vector, this line can be put anywhere in code above to get the state vector at that point
statevec = get_current_state(grover_circuit)
print(np.round(statevec,2))

# Now before we run the quantum circuit on simulation or actual quantum device, we must add the mesurement units to our circuit above.
# You can choose to put measure to all the qubits i the circuit using 'measure_all' or you could sepcify the qubits you need to measure 'measure'
grover_circuit.measure_all()
# grover_circuit.measure([0,1], [0,1])
grover_circuit.draw('mpl')

# The code below actually run the circuit with multiple times to get the probabilitstic output
# Note: 'get_current_state' func above just display non probabilitic/ Ideal state of the circuit,
#       whereas below code actually simulate a quantum circuit with probabilities/ noises
state_count_dict = get_qc_simulation_results(grover_circuit)
print(state_count_dict)


# Now lets actually run the circuit above on a real Quantum Computer!
results = get_qc_actual_results(grover_circuit) #print(results)

# Below are two ways to get the mesaurement results.
ans_way1 = results.data()
ans_way2 = results.get_counts(grover_circuit)
print(ans_way1, ans_way2)
plot_histogram(ans_way2)

# resultplt = plot_histogram(ans_way2)
# resultplt.show()
# resultplt.savefig("results.png")