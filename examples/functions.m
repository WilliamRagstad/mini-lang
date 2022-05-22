
add1 = (x) => x + 1

print(
    add1(add1(40))
)

pi = 3.141592653589793
tau = () => 2*pi
print(tau(), tau())

f(x) = 2*x + 1
print(f(2))

print( (() => "IIFE")() + " works!" )

// Lambdas
a = () => 1
b = x => 5
c = (y) => 6
d = (x, y) => x + y
e = (x, y) => {
	z = x + y
	z * z
}
print(a(), b(1), c(2), d(3, 4), d(5, 6))
