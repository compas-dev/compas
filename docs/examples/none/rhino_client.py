from compas.com import RhinoClient

Rhino = RhinoClient()

Rhino.start()
Rhino.show()
Rhino.top()

Rhino.AddPoint([0, 0, 0])
