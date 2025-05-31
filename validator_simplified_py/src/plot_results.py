import matplotlib.pyplot as plt
import json

with open('test_results.json') as f:
    data = json.load(f)

rates = [0.1, 0.5, 1, 2, 5, 10]  # Exemplo, substitua pelos seus valores
mrt = [cycle['mrt'] for cycle in data['cycles']]
mrt_avg = [sum(m)/len(m) for m in mrt]

plt.plot(rates, mrt_avg, marker='o', label='MRT')
plt.xlabel('Arrival Rate (pkg/s)')
plt.ylabel('Mean Response Time (s)')
plt.legend()
plt.show()
