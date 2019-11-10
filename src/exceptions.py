class MFMGridParserError(Exception):
    pass


class DataMemberDataError(MFMGridParserError):
    def __init__(self, msg):
        self.msg = msg

