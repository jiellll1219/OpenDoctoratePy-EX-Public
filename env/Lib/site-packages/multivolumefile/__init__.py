#!/usr/bin/env python
#
#    multi-volume file library
#    Copyright (C) 2020 Hiroshi Miura
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
import contextlib
import io
import os
import pathlib
from mmap import mmap
from typing import Any, Container, List, Optional, Union

from .stat import stat_result

__all__ = ["stat_result", "open", "MultiVolume"]

BLOCKSIZE = 16384


def open(name: Union[pathlib.Path, str], mode=None, volume=None) -> io.RawIOBase:
    return MultiVolume(name, mode=mode, volume=volume)


class _FileInfo:
    def __init__(self, filename, stat, size):
        self.filename = filename
        self.stat = stat
        self.size = size


class MultiVolume(io.RawIOBase, contextlib.AbstractContextManager):
    def __init__(
        self,
        basename: Union[pathlib.Path, str],
        mode: Optional[str] = "r",
        *,
        volume: Optional[int] = None,
        ext_digits: Optional[int] = 4,
        hex: Optional[bool] = False,
        ext_start: Optional[int] = 1
    ):
        self._mode = mode
        self._closed = False
        self._files = []  # type: List[object]
        self._fileinfo = []  # type: List[_FileInfo]
        self._position = 0
        self._positions = []
        self._digits = ext_digits
        self._start = ext_start
        self._hex = hex
        self.name = str(basename)
        if mode in ["rb", "r", "rt"]:
            self._init_reader(basename)
        elif mode in ["wb", "w", "wt", "xb", "x", "xt", "ab", "a", "at"]:
            if volume is None:
                self._volume_size = 10 * 1024 * 1024  # set default to 10MBytes
            else:
                self._volume_size = volume
            self._init_writer(basename)
        else:
            raise NotImplementedError

    def _glob_files(self, basename):
        if isinstance(basename, str):
            basename = pathlib.Path(basename)
        files = basename.parent.glob(basename.name + ".*")
        return sorted(files)

    def _init_reader(self, basename):
        pos = 0
        self._positions.append(pos)
        filenames = self._glob_files(basename)
        for name in filenames:
            stat = os.stat(name)
            size = os.stat(name).st_size
            self._fileinfo.append(_FileInfo(name, stat, size))
            self._files.append(io.open(name, mode=self._mode))
            pos += size
            self._positions.append(pos)

    def _init_writer(self, basename):
        if isinstance(basename, str):
            basename = pathlib.Path(basename)
        ext = ".{num:0{ext_digit}d}".format(num=self._start, ext_digit=self._digits)
        target = basename.with_name(basename.name + ext)
        if target.exists():
            if self._mode in ["x", "xb", "xt"]:
                raise FileExistsError
            elif self._mode in ["w", "wb", "wt"]:
                file = io.open(target, mode=self._mode)
                self._files.append(file)
                file.truncate(0)
                stat = os.stat(target)
                self._fileinfo.append(_FileInfo(target, stat, self._volume_size))
                self._positions = [0, self._volume_size]
            elif self._mode in ["a", "ab", "at"]:
                filenames = self._glob_files(basename)
                if self._mode == "ab":
                    mode = "rb"
                else:
                    mode = "r"
                pos = 0
                size = 0
                self._positions = [0]
                for i in range(len(filenames)):
                    file = io.open(filenames[i], mode)
                    self._files.append(file)
                    stat = filenames[i].stat()
                    size = stat.st_size
                    self._fileinfo.append(_FileInfo(filenames[i], stat, size))
                    pos += size
                    self._positions.append(pos)
                    self._position = pos
                # last file
                if size >= self._volume_size:
                    self._add_volume()
                else:
                    self._files[-1].close()
                    self._files[-1] = io.open(
                        filenames[len(filenames) - 1], mode=self._mode
                    )
            else:
                raise NotImplementedError
        else:
            file = io.open(target, mode=self._mode)
            self._files.append(file)
            self._fileinfo.append(_FileInfo(target, os.stat(target), self._volume_size))
            self._positions = [0, self._volume_size]

    def _current_index(self):
        for i in range(len(self._positions) - 1):
            if self._positions[i] <= self._position < self._positions[i + 1]:
                pos = self._files[i].tell()
                offset = self._position - self._positions[i]
                if pos != offset:
                    self._files[i].seek(offset, io.SEEK_SET)
                return i
        return len(self._files) - 1

    def read(self, size: int = -1) -> bytes:
        if size == -1:
            return self.readall()
        current = self._current_index()
        file = self._files[current]
        data = file.read(size)
        self._position += len(data)
        return data

    def readall(self) -> bytes:
        result = b""
        data = self.read(BLOCKSIZE)
        while len(data) > 0:
            result += data
            data = self.read(BLOCKSIZE)
        return result

    def readinto(self, b: Union[bytearray, memoryview, Container[Any], mmap]) -> int:
        size = len(b)
        data = self.read(size)
        b[: len(data)] = data
        return len(data)

    def write(
        self, b: Union[bytes, bytearray, memoryview, Container[Any], mmap]
    ) -> None:
        current = self._current_index()
        file = self._files[current]
        pos = file.tell()
        if pos + len(b) > self._volume_size:
            file.write(b[: self._volume_size - pos])
            self._position += self._volume_size - pos
            if current == len(self._files) - 1:
                self._add_volume()
            file = self._files[current + 1]
            file.seek(0)
            self.write(b[self._volume_size - pos :])  # recursive call
        else:
            file.write(b)
            self._position += len(b)

    def _add_volume(self):
        num = len(self._fileinfo) + self._start - 1
        if self._hex:
            last = self._fileinfo[-1].filename
            last_ext = ".{num:0{ext_digit}x}".format(num=num, ext_digit=self._digits)
            assert last.suffix.endswith(last_ext)
            next_ext = ".{num:0{ext_digit}x}".format(
                num=num + 1, ext_digit=self._digits
            )
            next = last.with_suffix(next_ext)
        else:
            last = self._fileinfo[-1].filename
            last_ext = ".{num:0{ext_digit}d}".format(num=num, ext_digit=self._digits)
            assert last.suffix.endswith(last_ext)
            next_ext = ".{num:0{ext_digit}d}".format(
                num=num + 1, ext_digit=self._digits
            )
            next = last.with_suffix(next_ext)
        self._files.append(io.open(next, self._mode))
        stat = os.stat(next)
        self._fileinfo.append(_FileInfo(next, stat, self._volume_size))
        pos = self._positions[-1]
        if pos != self._position:
            self._positions[-1] = self._position
        self._positions.append(self._positions[-1] + self._volume_size)

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        for file in self._files:
            file.close()

    @property
    def closed(self) -> bool:
        return self._closed

    def fileno(self) -> int:
        """
        fileno() is incompatible with other implementations.
        multivolume handle multiple file object so we cannot return single fd.
        """
        raise RuntimeError("fileno() is not supported.")

    def flush(self) -> None:
        if self._closed:
            return
        if self._mode == "wb" or self._mode == "w":
            for file in self._files:
                file.flush()

    def isatty(self) -> bool:
        return False

    def readable(self) -> bool:
        if self._closed:
            return False
        return all([f.readable() for f in self._files])

    def readline(self, size: Optional[int] = -1) -> bytes:
        raise NotImplementedError

    def readlines(self, hint: int = -1) -> List[bytes]:
        raise NotImplementedError

    def seek(self, offset: int, whence: Optional[int] = io.SEEK_SET) -> int:
        if whence == io.SEEK_SET:
            target = offset
        elif whence == io.SEEK_CUR:
            target = self._position + offset
        else:
            target = self._positions[-1] + offset
        self._position = target
        i = len(self._files) - 1
        while i > 0 and target < self._positions[i]:
            i -= 1
        file = self._files[i]
        file.seek(target - self._positions[i], io.SEEK_SET)
        return self._position

    def seekable(self) -> bool:
        if self._mode in ["ab", "at", "a"]:
            return False
        else:
            return all([f.seekable() for f in self._files])

    def tell(self) -> int:
        return self._position

    def truncate(self, size: Optional[int] = None) -> int:
        raise NotImplementedError

    def writable(self) -> bool:
        return self._mode in ["wb", "w", "wt", "x", "xb", "xt", "ab", "a", "at"]

    def writelines(self, lines):
        raise NotImplementedError

    def stat(self) -> stat_result:
        totalsize = 0
        for fi in self._fileinfo:
            totalsize += fi.size
        return stat_result(self._fileinfo[0].stat, totalsize)

    def __del__(self):
        # FIXME
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
