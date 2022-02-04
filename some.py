grades = [7, 27, 23, 65, 43, 0, 82, 0]
results = []
for i in grades:
    if i > 37:
        rounded = i + (5 - i) % 5
        if (rounded - i) < 3:
            results.append(rounded)
        elif rounded >= 3:
            results.append(i)
    else:
        results.append(i)
print(results)










