
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
