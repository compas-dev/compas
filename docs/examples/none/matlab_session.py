from compas.com import MatlabSession

m = MatlabSession('test')

print(m.session_name)
print(m.isprime(17))
