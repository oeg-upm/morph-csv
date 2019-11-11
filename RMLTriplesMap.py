class RMLTriplesMap:
    def __init__(self, logical_source, subject_map, predicate_object_maps):
        self.logical_source = logical_source
        self.subject_map = subject_map
        self.predicate_object_maps = predicate_object_maps
