import json
import leximited
from .atoms import Empty, Atom
from .site_data import SiteData


class GridData(object):
    def __init__(self, mfm_grid_state_json_file):
        self.simulation_age = None
        self.grid_is_staggered = None
        self.grid_height = None
        self.grid_width = None
        self.tile_height = None
        self.tile_width = None
        self.owned_width = None
        self.owned_height = None
        self.event_radius = None
        self.event_layer_atoms = []
        self.base_layer_atoms = []
        self.load_file(mfm_grid_state_json_file)
        self.event_layer_atom_data = self.flip_xy(
            self.get_grid_state()["event_layer_atoms"])
        self.event_layer_index = self.index_atoms()
        self.base_layer_atom_data = self.flip_xy(
            self.get_grid_state()["base_layer_atoms"])
        self.base_layer_index = self.index_atoms(base=True)

    def gen_2d_grid_list(self, init):
        """
        generates a 2d list matching the size of our grid with values initialized
        to the object given by init
        """
        return [[init
                 for x in range(0, self.grid_width)]
                for y in range(0, self.grid_height)]

    def index_atoms(self, base=False):
        """
        index atoms in 2d list
        """
        if base:
            atom_data = self.base_layer_atom_data
        else:
            atom_data = self.event_layer_atom_data

        two_d_list = self.gen_2d_grid_list(
            self.atom_factory({"name": "Empty"}))
        i = 0
        for a in two_d_list[0]:
            i += 1
        c = 0
        for a in two_d_list:
            c += 1
        for a_d in atom_data:
            two_d_list[a_d["x"]][a_d["y"]] = self.atom_factory(a_d)
        return two_d_list

    def flip_xy(self, atom_data):
        for ad in atom_data:
            tmp_x = ad["y"]
            tmp_y = ad["x"]
            ad.update({"x": tmp_x, "y": tmp_y})
        return atom_data

    def atom_factory(self, atom_dict):
        """
        return a special atom class type (should be used only for type hinting) or a generic atom
        """
        for k, v in self.get_atom_types().items():
            if atom_dict["name"] == k:
                return v(atom_dict)
        return Atom(atom_dict)

    def get_atom_types(self):
        """
        Overload and update return value to add additional atom types. Should only be used for type hinting.
        Keys must be Ulam Element names to match. Values must be subclasses of Atom.
        """
        return {'Empty': Empty}

    def get_atom_in_site(self, x, y, base=False):
        if base:
            return self.base_layer_index[x][y]
        else:
            return self.event_layer_index[x][y]

    def print_grid_ascii(self, base=False):
        if base:
            index = self.base_layer_index
        else:
            index = self.event_layer_index
        for list in index:
            print(*list, sep='')

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
            'event_layer_atoms': [site.get_dict() for site in self.event_layer_atoms],
            'base_layer_atoms': [site.get_dict() for site in self.base_layer_atoms]
        }

    def load_file(self, path):
        with open(path) as file:
            self.load_json_string(file.read())

    def load_json_string(self, string):
        doc = json.loads(string)
        self.simulation_age = leximited.from_leximited_int(
            doc['simulation_age'])
        self.grid_is_staggered = doc['grid_configuration']['grid_is_staggered']
        self.grid_height = doc['grid_configuration']['grid_height']
        self.grid_width = doc['grid_configuration']['grid_width']
        self.tile_height = doc['tile_configuration']['tile_height']
        self.tile_width = doc['tile_configuration']['tile_width']
        self.owned_height = doc['tile_configuration']['owned_height']
        self.owned_width = doc['tile_configuration']['owned_width']
        self.event_radius = doc['tile_configuration']['event_window_radius']

        event_layer_sites = doc['event_layer_atoms']
        for s in event_layer_sites:
            self.event_layer_atoms.append(SiteData(s))

        base_layer_sites = doc['base_layer_atoms']
        for s in base_layer_sites:
            self.base_layer_atoms.append(SiteData(s))
