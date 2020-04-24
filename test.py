fname = "test.txt"
count = 0
with open(fname, 'r') as f:
    for line in f:
        count += 1
print("Total number of  is:", count)