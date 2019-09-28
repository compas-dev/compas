from compas.geometry.transformations import transformations as src # change this line to different modules


temp = ''
print(src.__all__)

for func in src.__all__:
    temp += 'from compas.geometry.transformations import {}\n'.format(func)

temp += '\n\n'

for func in src.__all__:
    temp += '''
def test_{}():
    pass

'''.format(func)

print(temp)