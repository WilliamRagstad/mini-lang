a = #{b: #{c: 40}}
print(a.b.c + 2)
print(a.b['' + 'c'] + 2)
print(a['b']['c'] + 2)

b = [1, 2, 3]
print(b[1] * b[1] * b[1] * (b[1] + b[2]) + b[2] - b[0])

ns = #{func: (x) => x * 2 + 5}
print(ns.func(5))

l = [1, 2, 3][2]
print(l, l == 3)
