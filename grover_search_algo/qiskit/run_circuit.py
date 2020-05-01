# -*- coding: utf-8 -*-
# https://pypi.org/project/qiskit-ibmq-provider/
# https://github.com/Qiskit/qiskit-ibmq-provider
# https://qiskit.org/documentation/stubs/qiskit.providers.ibmq.IBMQFactory.enable_account.html
# https://qiskit-staging.mybluemix.net/documentation/release_notes.html
# https://qiskit.org/documentation/getting_started.html

# in case you have issue with inline plots, uncomment the below lines
# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt

# For Simulator
from qiskit import Aer
# For Actual Quantum Experience
from qiskit import IBMQ
from qiskit.providers.ibmq import least_busy
from qiskit.tools.monitor import job_monitor

# For executing Quantum circuit
from qiskit import execute

# https://qiskit.org/documentation/apidoc/aer_provider.html
# Ideal quantum circuit statevector simulator
statevector_sim = Aer.get_backend('statevector_simulator')
# Noisy quantum circuit simulator backend.
qasm_sim = Aer.get_backend('qasm_simulator')

def get_current_state(circuit, backend_sim = statevector_sim):
    job_sim = execute(circuit, backend_sim)
    result = job_sim.result() # print(result)
    state_vec = result.get_statevector()
    return state_vec

def get_qc_simulation_results(circuit, backend_sim = qasm_sim, sim_count = 1024):
    # circuit.measure_all()
    backend = Aer.get_backend('qasm_simulator')
    all_sim_results = execute(circuit, backend=backend, shots=sim_count).result() #print(all_sim_results.to_dict())
    state_count_dict = all_sim_results.get_counts()
    return state_count_dict

# Note, you could always visit: https://quantum-computing.ibm.com/results to see the status of your job submitted on Real Quantum Computer
def get_qc_actual_results(circuit, sim_count = 1024):
    token = open(r"<path to token file>\ibm_token.txt",mode='r').read() # or just copy the token here
    # In case you do not want to save credential on disk, just enable & disable them as required
    provider = IBMQ.enable_account(token)
    provider = IBMQ.get_provider()
    
    # for keeping the credentioal on disk, just save once& then use laod
    # IBMQ.save_account(token)
    # provider = IBMQ.load_account()
    
    # Load IBM Q account and get the least busy backend device
    device = least_busy(provider.backends(simulator=False))
    print("Running on current least busy device: ", device)
    
    # Run our circuit on the least busy backend. Monitor the execution of the job in the queue    
    job = execute(circuit, backend=device, shots=sim_count, max_credits=10)
    job_monitor(job, interval = 2)
    
    # Get the results from the computation, job.result() will wait untill your program is finished
    results = job.result()
    IBMQ.disable_account()
    return results