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

// Filter
b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print("Filter:", list_filter(b, (x) => x % 2 == 0), list_filter(b, (x) => x % 2 == 0) == [2, 4, 6, 8, 10])
print("Filter:", list_filter(b, (x) => x % 2 == 1), list_filter(b, (x) => x % 2 == 1) == [1, 3, 5, 7, 9])
print("Filter:", list_filter(b, (x) => x > 5), list_filter(b, (x) => x > 5) == [6, 7, 8, 9, 10])
print("Filter:", list_filter(b, (x) => x < 5), list_filter(b, (x) => x < 5) == [1, 2, 3, 4])

// Reduce
c = [1, 2, 3, 4, 5]
print("Reduce:", list_reduce(c, (x, y) => x + y), list_reduce(c, (x, y) => x + y) == 15)
// With initial value
print("Reduce:", list_reduce(c, (x, y) => x * y, 1), list_reduce(c, (x, y) => x * y, 1) == 120)
// Start at 100 and subtract all values in the list from it
print("Reduce:", list_reduce(c, (acc, val) => acc - val, 100), list_reduce(c, (acc, val) => acc - val, 100) == 85)

// Group by
d = [1, 2, 3, 4, 5, 6, 7, 8, 9]
print("Group by:",
      list_group_by(d, (x) => x % 2 == 0),
      list_group_by(d, (x) => x % 2 == 0)[false],
      list_group_by(d, (x) => x % 2 == 0)[true],
      list_group_by(d, (x) => x % 2 == 0) == #{false: [1, 3, 5, 7, 9], true: [2, 4, 6, 8]})

// Ranges
print("Range:", 0 .. 10, 0 .. 10 == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
a = 5
b = 10
print("Range:", a .. b, a .. b == [5, 6, 7, 8, 9])
