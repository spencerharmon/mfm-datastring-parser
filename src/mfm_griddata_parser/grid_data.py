import json
from .site_data import SiteData


class GridData(object):
    def __init__(self):
        self.grid_is_staggered = None
        self.grid_height = None
        self.grid_width = None
        self.tile_height = None
        self.tile_width = None
        self.owned_width = None
        self.owned_height = None
        self.event_radius = None
        self.nonempty_sitelist = []

    def get_json(self, indent=2):
        return json.dumps(self.get_grid_state(), indent=indent)

    def get_grid_state(self):
        return {
            'grid_configuration': {
                'grid_is_staggered': self.grid_is_staggered,
                'grid_height': self.grid_height,
                'grid_width': self.grid_width
            },
            'tile_configuration': {
                'tile_height': self.tile_height,
                'tile_width': self.tile_width,
                'owned_height': self.owned_height,
                'owned_width': self.owned_width,
                'event_window_radius': self.event_radius
            },
            'non_empty_site_list': [site.get_dict() for site in self.nonempty_sitelist]
        }

    def load_file(self, path):
        with open(path) as file:
            self.load_json_string(file.read())

    def load_json_string(self, string):
        doc = json.loads(string)
        self.grid_is_staggered = doc['grid_configuration']['grid_is_staggered']
        self.grid_height = doc['grid_configuration']['grid_height']
        self.grid_width = doc['grid_configuration']['grid_width']
        self.tile_height = doc['tile_configuration']['tile_height']
        self.tile_width = doc['tile_configuration']['tile_width']
        self.owned_height = doc['tile_configuration']['owned_height']
        self.owned_width = doc['tile_configuration']['owned_width']
        self.event_radius = doc['tile_configuration']['event_window_radius']

        sites = doc['non_empty_site_list']
        for s in sites:
            self.nonempty_sitelist.append(SiteData(s))

