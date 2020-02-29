import json

class SiteData(object):
    def __init__(self, dict):
        self.x = dict["x"]
        self.y = dict["y"]
        self.symbol = dict["symbol"]
        self.name = dict["name"]
        self.argb = dict["argb"]
        self.data_members = dict["data_members"]

    def get_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "symbol": self.symbol,
            "name": self.name,
            "argb": self.argb,
            "data_members": self.data_members,
            }
