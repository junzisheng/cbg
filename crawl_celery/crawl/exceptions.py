class NotTarget(Exception):  # 返回数据但不是目标服务器
    pass


class IPBanned(Exception):
    pass


class DataMiss(Exception):
    pass


class StatusNot200(Exception):
    pass


class SystemBusy(Exception):
    pass


class Empty(Exception):
    pass


class ParamsError(Exception):
    pass


class OterStatus(Exception):
    pass
