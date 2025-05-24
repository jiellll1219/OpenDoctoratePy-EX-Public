class stat_result:
    def __init__(self, stat, size):
        self._stat = stat
        self._size = size

    @property
    def st_size(self):
        return self._size

    @property
    def st_mode(self):
        return self._stat.st_mode

    @property
    def st_ino(self):
        return 0

    @property
    def st_dev(self):
        return self._stat.st_dev

    @property
    def st_nlink(self):
        return self._stat.st_nlink

    @property
    def st_uid(self):
        return self._stat.st_uid

    @property
    def st_gid(self):
        return self._stat.st_gid

    @property
    def st_atime(self):
        return self._stat.st_atime

    @property
    def st_ctime(self):
        return self._stat.st_ctime

    @property
    def st_mtime(self):
        return self._stat.st_mtime

    @property
    def st_atime_ns(self):
        return self._stat.st_atime_ns

    @property
    def st_ctime_ns(self):
        return self._stat.st_ctime_ns

    @property
    def st_mtime_ns(self):
        return self._stat.st_mtime_ns
