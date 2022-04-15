a = #{
	'key1': 'value1',
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
