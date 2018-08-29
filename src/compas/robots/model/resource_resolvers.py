from compas.datastructures import Mesh

class DefaultMeshResolver(object):
    def can_handle_uri(self, uri):
        supported_scheme = uri.startswith('http:') or uri.startswith(
            'https:') or uri.startswith('file:///')
        supported_format = uri.endswith('.obj')
        return supported_scheme and supported_format

    def resolve(self, uri):
        if uri.startswith('file:///'):
            uri = uri[8:]

        return Mesh.from_obj(uri)
