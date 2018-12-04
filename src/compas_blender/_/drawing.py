
#    'xdraw_labels',
#    'xdraw_points',
    'xdraw_lines',
#    'xdraw_geodesics',
#    'xdraw_polylines',
#    'xdraw_faces',
#    'xdraw_cylinders',
#    'xdraw_pipes',
#    'xdraw_spheres',
#    'xdraw_mesh',

#    'delete_all_materials',
#    'create_material',
#    'draw_cuboid',
#    'draw_cubes',
#    'draw_pipes',
#    'draw_plane',
#    'draw_spheres',
#    'draw_points',
#    'xdraw_cubes',
#    'xdraw_faces',
#    'xdraw_labels',
#    'xdraw_mesh',
#    'xdraw_pipes',
#    'xdraw_pointcloud',
#    'xdraw_points',
#    'xdraw_spheres',
#    'xdraw_texts',


#def draw_cuboid(Lx=1, Ly=1, Lz=1, pos=[0, 0, 0], layer=0, color=[1, 1, 1], wire=True):
#    """ Draw a cuboid.

#    Parameters:
#        Lx (float): Length in x.
#        Ly (float): Length in y.
#        Lz (float): Length in z.
#        pos (list): Centroid position [x, y, z].
#        layer (int): Layer number.
#        color (list): Material color.
#        wire (bool): Show wires for faces.

#    Returns:
#        obj: Created cube object.
#    """
#    bpy.ops.mesh.primitive_cube_add(radius=1, location=pos)
#    cube = bpy.context.object
#    cube.dimensions = [Lx, Ly, Lz]
#    cube.show_wire = wire
#    material = create_material(color=color)
#    cube.data.materials.append(material)
#    set_object_layer(object=cube, layer=layer)
#    cube.select = False
#    return cube


#def draw_plane(Lx=1, Ly=1, dx=0.5, dy=0.5, name='plane', layer=0, color=[1, 1, 1], wire=True, bracing=None):
#    """ Create a plane mesh in x-y.

#    Parameters:
#        Lx (float): Length of the plane in x.
#        Ly (float): Length of the plane in y.
#        dx (float): Spacing in x direction.
#        dy (float): Spacing in y direction.
#        name (str): Name for Blender mesh.
#        layer (int): Layer to draw the plane on.
#        color (list): Material color.
#        wire (bool): Show wires for faces.
#        bracing (str): None, 'cross', 'diagonals-right' or 'diagonals-left'.

#    Returns:
#        obj: Created plane Blender mesh object.
#    """
#    nx = int(Lx / dx)
#    ny = int(Ly / dy)
#    x = [i * dx for i in range(nx + 1)]
#    y = [i * dy for i in range(ny + 1)]
#    vertices = [[xi, yi, 0] for yi in y for xi in x]
#    if not bracing:
#        faces = [[(j + 0) * (nx + 1) + i + 0, (j + 0) * (nx + 1) + i + 1,
#                  (j + 1) * (nx + 1) + i + 1, (j + 1) * (nx + 1) + i + 0]
#                 for i in range(nx) for j in range(ny)]
#    else:
#        faces = []
#        for i in range(nx):
#            for j in range(ny):
#                face = [(j + 0) * (nx + 1) + i + 0, (j + 0) * (nx + 1) + i + 1,
#                        (j + 1) * (nx + 1) + i + 1, (j + 1) * (nx + 1) + i + 0]
#                if bracing == 'cross':
#                    n = len(vertices)
#                    vertices.append(centroid_points([vertices[k] for k in face]))
#                    faces.extend([[face[0], face[1], n], [face[1], face[2], n],
#                                  [face[2], face[3], n], [face[3], face[0], n]])
#                elif bracing == 'diagonals-right':
#                    faces.extend([[face[0], face[1], face[2]], [face[2], face[3], face[0]]])
#                elif bracing == 'diagonals-left':
#                    faces.extend([[face[1], face[2], face[3]], [face[3], face[0], face[1]]])
#    bmesh = xdraw_mesh(name, vertices=vertices, faces=faces, layer=layer, color=color, wire=wire)
#    material = create_material(color=color)
#    bmesh.data.materials.append(material)
#    bmesh.select = False
#    return bmesh



#def xdraw_faces(faces, alpha=1):
#    """ Draw a set of faces.

#    Parameters:
#        faces (list): {'color':, 'points':, 'name':, 'layer': }.
#        alpha (float): Alpha [0, 1].

#    Returns:
#        None
#    """
#    for face in faces:
#        color = face.get('color', [1, 1, 1])
#        points = face['points']
#        name = face.get('name', 'face')
#        indices = [list(range(len(points)))]
#        layer = face.get('layer')
#        xdraw_mesh(name=name, vertices=points, faces=indices, color=color, layer=layer, alpha=alpha)


#def xdraw_labels(labels):
#    """ Draw pointcloud text labels.

#    Parameters:
#        labels (dic): {'pos':, 'name':, 'layer':}.

#    Returns:
#        list: Created label objects (bmeshes).
#    """
#    objects = xdraw_pointcloud(points=labels)
#    set_objects_show_name(objects=objects, show=True)
#    return objects





#def xdraw_pointcloud(points):
#    """ Draw a set of points using Blender mesh vertices.

#    Parameters:
#        points (dic): {'pos':, 'name':, 'layer':}.

#    Returns:
#        list: Created point objects (bmeshes).
#    """
#    object = xdraw_mesh(name='pt', vertices=[[0, 0, 0]])
#    objects = []
#    for point in points:
#        copy = object.copy()
#        copy.location = Vector(point.get('pos', [0, 0, 0]))
#        copy.name = point.get('name', 'point')
#        copy.data = copy.data.copy()
#        set_object_layer(object=copy, layer=point.get('layer', 0))
#        objects.append(copy)
#    delete_object(object=object)
#    return _link_objects(objects)




#def xdraw_texts(texts):
#    """ Draw a set of text objects.

#    Parameters:
#        texts (list): {'radius':, 'pos':, 'color':, 'name':, 'text':, 'layer':}.

#    Returns:
#        list: Created text objects.
#    """
#    bpy.ops.object.text_add(view_align=True)
#    object = bpy.context.object
#    objects = []
#    for text in texts:
#        copy = object.copy()
#        copy.scale *= text.get('radius', 1)
#        copy.location = Vector(text.get('pos', [0, 0, 0]))
#        copy.name = text.get('name', 'text')
#        copy.data.body = text.get('text', 'text')
#        copy.data = copy.data.copy()
#        material = create_material(color=text.get('color', [1, 1, 1]))
#        copy.data.materials.append(material)
#        set_object_layer(object=copy, layer=text.get('layer', 0))
#        objects.append(copy)
#    delete_object(object=object)
#    return _link_objects(objects)



#    xdraw_texts([{'radius': 0.5, 'pos': [5, 0, 0], 'color': [0, 0, 1], 'text': 'TEXT', 'layer': 1}])

#    points = [{'pos': [i[0], i[1], i[2] + 2], 'radius': 0.01, 'layer': 1} for i in list(rand(10, 3))]
#    xdraw_points(points)

#    draw_plane(Lx=1, Ly=1, dx=0.5, dy=0.5, bracing='cross', color=[1, 0, 1], layer=1)

#    draw_cuboid(Lx=1, Ly=3, Lz=2, pos=[2, 0, 0], color=[1, 1, 0], layer=1)
