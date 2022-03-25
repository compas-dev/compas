from compas.geometry import Polyline


# pll=Polyline([[0, 0, 0], [1, 0, 0], [2, 0, 0], [2, 2, 0]])
# print(pll)
# pll.extend(-2.5)
# print(pll)
# pll2 = Polyline([[0, 0, 0], [1, 0, 0], [2, 0, 0], [2, 2, 0]])
# print(pll2)
# pll2.extend((2,2))
# print(pll2)


pll = Polyline([[0, 0, 0], [1, 0, 0], [2, 0, 0], [2, 2, 0]])
print(pll)
pll.shorten(0.5)
print(pll)
pll = Polyline([[0, 0, 0], [1, 0, 0], [2, 0, 0], [2, 2, 0]])
print(pll)
pll.shorten(2)
print(pll)


pll = Polyline([[0, 0, 0], [1, 0, 0], [2, 0, 0], [2, 2, 0]])
print(pll)
pll.shorten((0.5,0.5))
print(pll)

pll = Polyline([[0, 0, 0], [1, 0, 0], [2, 0, 0], [2, 2, 0]])
print(pll)
pll.shorten((1, 0.5))
print(pll)
