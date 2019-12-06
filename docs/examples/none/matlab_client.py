from compas.com import MatlabClient

matlab = MatlabClient(interactive=True)

A = MatlabClient.matrix_from_list([[1, 0, 1, 3], [2, 3, 4, 7], [-1, -3, -3, -4]])

matlab.put('A', A)
matlab.eval('[R, jb] = rref(A);')

R = matlab.get('R')
jb = matlab.get('jb')

print(R)
print(jb)
