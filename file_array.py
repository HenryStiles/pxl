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

class FileArray:
    def __init__(self, filepath, block_size=524288, binary=True):  # Default block size set to 512KB
        self.filepath = filepath
        self.block_size = block_size
        self.binary = binary
        self.cache = {}
        self.file_length = self._get_file_length()

    
    def _get_file_length(self):
        with open(self.filepath, 'rb') as file:
            file.seek(0, 2)
            return file.tell()

    def _read_block_from_file(self, block_index):
        mode = 'rb' if self.binary else 'r'
        offset = block_index * self.block_size
        with open(self.filepath, mode) as file:
            file.seek(offset)
            return file.read(self.block_size)

    def _write_block_to_file(self, block_index, data):
        mode = 'r+b' if self.binary else 'r+'
        offset = block_index * self.block_size
        with open(self.filepath, mode) as file:
            file.seek(offset)
            file.write(data)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._get_single_item(key)
        elif isinstance(key, slice):
            return self._get_slice(key)
        else:
            raise TypeError("Invalid key type.")

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self._set_single_item(key, value)
        elif isinstance(key, slice):
            self._set_slice(key, value)
        else:
            raise TypeError("Invalid key type.")

    def _get_single_item(self, offset):
        block_index = offset // self.block_size
        block_offset = offset % self.block_size

        if block_index not in self.cache:
            self.cache[block_index] = self._read_block_from_file(block_index)

        if self.binary:
            return self.cache[block_index][block_offset: block_offset + 1]
        else:
            return self.cache[block_index][block_offset]

    def _set_single_item(self, offset, value):
        block_index = offset // self.block_size
        block_offset = offset % self.block_size

        if block_index not in self.cache:
            self.cache[block_index] = self._read_block_from_file(block_index)

        if self.binary:
            self.cache[block_index] = (self.cache[block_index][:block_offset] + value +
                                       self.cache[block_index][block_offset + 1:])
        else:
            self.cache[block_index] = self.cache[block_index][:block_offset] + value + self.cache[block_index][block_offset + 1:]

        self._write_block_to_file(block_index, self.cache[block_index])

    def _get_slice(self, slice_obj):
        start, stop, step = slice_obj.indices(self.file_length)
        if step != 1:
            raise ValueError("Slices with step are not currently supported.")

        data = b'' if self.binary else ''
        for i in range(start, stop):
            data += self.__getitem__(i)

        return data

    def _set_slice(self, slice_obj, value):
        start, stop, step = slice_obj.indices(self.file_length)
        if step != 1 or len(value) != stop - start:
            raise ValueError("Slices with step or mismatched length are not supported.")

        for i, val in enumerate(value):
            self.__setitem__(start + i, val)
