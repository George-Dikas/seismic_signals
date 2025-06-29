with open('1.txt', 'r', encoding='utf-8') as file:
    num_lines = sum(1 for line in file)

print(f"Το σύνολο των γραμμών είναι: {num_lines}")