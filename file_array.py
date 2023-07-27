# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys


class FileArray:
    def __init__(self, filepath, binary=False, cache_size=1024):
        self.filepath = filepath
        self.cache = {}
        self.cache_size = cache_size
        self.binary = binary

    def _read_from_file(self, offset, length):
        try:
            if self.binary:
                mode = 'rb'
            else:
                mode = 'r'
            with open(self.filepath, mode) as file:
                file.seek(offset)
                return file.read(length)
        except MemoryError:
            raise MemoryError("File is too large to be read into memory.")

    def _write_to_file(self, offset, data):
        if self.binary:
            mode = 'r+b'
        else:
            mode = 'r+'
        with open(self.filepath, 'r+b') as file:
            file.seek(offset)
            file.write(data)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._handle_single_item(key)
        elif isinstance(key, slice):
            return self._handle_slice(key)
        else:
            raise TypeError("Invalid argument type.")

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self._write_to_file(key, value)
            self._update_cache(key, value)
        elif isinstance(key, slice):
            self._write_slice(key, value)
        else:
            raise TypeError("Invalid argument type.")

    def _handle_single_item(self, offset):
        if offset in self.cache:
            return self.cache[offset]
        data = self._read_from_file(offset, 1)
        byte_value = data[0]
        self._update_cache(offset, byte_value)
        return byte_value

    def _handle_slice(self, slice_obj):
        start, stop, step = slice_obj.indices(sys.maxsize)
        if step != 1:
            raise ValueError("Slices with step are not supported.")
        length = stop - start
        return self._read_from_file(start, length)

    def _write_slice(self, slice_obj, data):
        start, stop, step = slice_obj.indices(sys.maxsize)
        if step != 1 or stop - start != len(data):
            raise ValueError("Slices with step or mismatched length are not supported.")
        self._write_to_file(start, data)
        for i, byte in enumerate(data):
            self._update_cache(start + i, byte)

    def _update_cache(self, offset, data):
        if len(self.cache) >= self.cache_size:
            self.cache.pop(next(iter(self.cache)))  # Remove the least recently used item
        self.cache[offset] = data