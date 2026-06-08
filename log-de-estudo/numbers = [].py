numbers = []
for i in range (5):
    number = float(input(f"write the {i + 1}º number: "))
    numbers.append(number)

maxi_number = max(numbers)
print(f"the biggiest number you write is {maxi_number} ")
