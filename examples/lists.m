my_list = [1, 2, 3, 4]
print("First element:", my_list[0])
print(my_list)
my_list


// Map
add_one(x) = x + 1
a = [512, 64, 8, 1]
print("Map:", list_map(a, add_one), list_map(a, add_one) == [513, 65, 9, 2])
print("Map:", list_map(a, (x) => x * x), list_map(a, (x) => x * x) == [262144, 4096, 64, 1])
print("Map:", list_map(a, (x) => x / 2), list_map(a, (x) => x / 2) == [256, 32, 4, 0.5])
print("Map:", list_map(a, (x) => x - 1), list_map(a, (x) => x - 1) == [511, 63, 7, 0])
print("Map:", list_map(a, (x) => x % 2), list_map(a, (x) => x % 2) == [0, 0, 0, 1])
