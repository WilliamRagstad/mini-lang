a = {
	b = {
		c = 15
		print("c =", c)
		c * 2
	}
	print("b =", b)
	// print("c =", c) // Should be an error
	// b + c // Should be an error
	b - 9
}
print("a =", a * 2)

f(x) = {
	x = 5 * x - 2
	print("f(x) =", x)
	x
}
f(f(2))
