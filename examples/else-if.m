
if (true) print("it was true") else print("it was false")

if false {
	print("it was true")
} else {
	print("it was false")
}

rec(x) = {
	if x <= 0 {
		0
	} else {
		x + rec(x - 1)
	}
}
print(rec(10))
