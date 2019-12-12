from compas.com import MatlabProcess

matlab = MatlabProcess()

matlab.start()

matlab.write_value('a', 37)
matlab.run_command('res = isprime(a);')

print(matlab.read_value('res'))
print(matlab.run_command('res = isprime(a);', ivars={'a': 17}, ovars={'res': None}))
print(matlab.ws_data)
