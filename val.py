

arr = []
current_value = 2
last_cell = 6160

while current_value <= last_cell:
    arr.append("B" + str(current_value))
    current_value += 31

print(arr)
