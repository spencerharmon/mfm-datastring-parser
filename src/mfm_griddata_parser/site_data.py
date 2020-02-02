import json
from .data_member_data import DataMemberData


class SiteData(object):
    def __init__(self, dict):
        self.x = dict["x"]
        self.y = dict["y"]
        self.symbol = dict["symbol"]
        self.name = dict["name"]
        self.argb = dict["argb"]
        self.data_member_data = DataMemberData(dict["data_string"])
        self.data_members = self.data_member_data.data
        self.data_string_truncated = self.data_member_data.truncated

    def get_json(self):
        return json.dumps(self.get_dict())

    def get_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "symbol": self.symbol,
            "name": self.name,
            "argb": self.argb,
            "data_members": self.data_members,
            "data_string_truncated": self.data_string_truncated
            }
