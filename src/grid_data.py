import json
from src.site_data import SiteData


class GridData(object):
    def __init__(self):
        self.sitelist = []

    def get_json(self):
        return json.dumps(self.get_grid_state())

    def get_grid_state(self):
        return [site.get_dict() for site in self.sitelist]

    def load_file(self, path):
        with open(path) as file:
            sites = json.loads(file.read())
            for s in sites:
                self.sitelist.append(SiteData(s))

    def load_json_string(self, string):
        sites = json.loads(string)
        for s in sites:
            self.sitelist.append(SiteData(s))

