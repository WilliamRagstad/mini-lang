a = #{
	key1: 'value1',
	'key2': 'value2',
	'key3': 'value3',
	4: 'value4',
	5: 'value5',
	6: 'value6'
}

print("key1: " + a['key1'], a['key1'] == 'value1')
print("key2: " + a['key2'], a['key2'] == 'value2')
print("5: " + a[5], a[5] == 'value5')
print("6: " + a[6], a[6] == 'value6')

empty = #{}
print("empty: " + empty, empty == #{})

b = #{'one': 1, 2: 2, 'three': '3'}
c = #{'four': 4, 5: 5, 'six': 6}
print("Adding:")
print(b)
print(c)
print("Result:")
print(b + c)

print("Member access:", b.one, b.one == 1)
print("Member access:", b[2], b[2] == 2)

d = #{deeper: #{nested: 42 } }
print("Nested access:", d.deeper.nested, d.deeper.nested == 42)

// Concatenation
e = #{a: 1} + #{b: 2}
print("Concatenation:", e, e == #{a: 1, b: 2})

f = #{a: 1} + #{a: 2}
print("Concatenation:", f, f == #{a: 2})

// Length
print("Size:", map_size(a), map_size(a) == 6)

// Contains
print("Contains:", map_contains(a, 'key1'), map_contains(a, 'key1') == true)
print("Contains:", map_contains(a, 'value1'), map_contains(a, 'value1') == false)
