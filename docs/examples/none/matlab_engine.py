from compas.com import MatlabEngine

matlab = MatlabEngine()
matlab.connect()

A = matlab.double([[1, 0, 1, 3], [2, 3, 4, 7], [-1, -3, -3, -4]])
res = matlab.engine.rref(A, nargout=2)

print(res)
