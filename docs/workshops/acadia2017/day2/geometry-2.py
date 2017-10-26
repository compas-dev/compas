from compas.geometry import add_vectors
from compas.geometry import length_vector

u = (1.0, 0.0, 0.0)
v = (0.0, 1.0, 0.0)

r = add_vectors(u, v)

print(r)
print(length_vector(r))