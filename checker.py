import sys

q = 257
p = 1543
g = int(sys.argv[1])
results = list()
for i in range(1, q+1):
    print(f'g^{i} = {pow(g, i, p)}')
    results.append(pow(g, i, p))
results.sort()
print(results)
