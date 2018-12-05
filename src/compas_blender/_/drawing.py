

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

