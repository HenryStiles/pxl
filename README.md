# PXL Assembler and Disassembler
Utilities to disassemble PXL to a readable format and an assembler to do the inverse.

# History
This is a fork of the dual licensed Artifex code I originally wrote, other engineers have worked on it as well.

# Purpose.
I wanted to improve the code a bit, but also wanted to experiment with creating an indexing abstraction over a file (see file_array.py).  The client sees a regular array but it is really reading from offsets in the file.  A caching scheme is used.

# License
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
