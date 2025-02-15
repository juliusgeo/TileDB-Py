# quickstart_dense.py
#
# LICENSE
#
# The MIT License
#
# Copyright (c) 2023 TileDB, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# DESCRIPTION
#
# Please refer to the TileDB and TileDB-Py documentation for more information:
#   https://docs.tiledb.com/main/how-to
#   https://tiledb-inc-tiledb.readthedocs-hosted.com/projects/tiledb-py/en/stable/python-api.html
#
# When run, this program will create a simple 1D dense array with a dimension label, write
# some data to it, and read a slice of the data back.
#


import numpy as np

import tiledb


def create_array(uri: str):
    """Create array schema with dimension labels"""
    dim1 = tiledb.Dim("d1", domain=(1, 5))
    dim2 = tiledb.Dim("d2", domain=(1, 5))
    dom = tiledb.Domain(dim1, dim2)
    att = tiledb.Attr("a1", dtype=np.int64)
    dim_labels = {
        0: {"l1": dim1.create_label_schema("decreasing", np.int64)},
        1: {
            "l2": dim2.create_label_schema("increasing", np.int64),
            "l3": dim2.create_label_schema("increasing", np.float64),
        },
    }
    schema = tiledb.ArraySchema(domain=dom, attrs=(att,), dim_labels=dim_labels)
    tiledb.Array.create(uri, schema)


def write_array(uri: str):
    """Write attribute and label data to the array"""
    a1_data = np.reshape(np.arange(1, 26), (5, 5))
    l1_data = np.arange(5, 0, -1)
    l2_data = np.arange(-2, 3)
    l3_data = np.linspace(-1.0, 1.0, 5)
    with tiledb.open(uri, "w") as array:
        array[:] = {"a1": a1_data, "l1": l1_data, "l2": l2_data, "l3": l3_data}


def read_array(uri: str):
    """Read the array from the dimension label"""

    with tiledb.open(uri, "r") as array:

        data1 = array.label_index(["l2"])[1, -1:1]
        print("Reading array on [[1, -1:1]] with label 'l2' on dim2")
        for name, value in data1.items():
            print(f"  '{name}'={value}")

        data2 = array.label_index(["l1", "l2"])[4:5, -2:2]
        print("Reading array on [[4:5, -2:2]] with label 'l1' on dim1 and 'l2' on dim2")
        for name, value in data2.items():
            print(f"  '{name}'={value}")

        data3 = array.label_index(["l3"])[1, 0.0:2.0]
        print("Reading array on [[1, 0.0:2.0]] with label 'l3' on dim2")
        for name, value in data3.items():
            print(f"  '{name}'={value}")


if __name__ == "__main__":

    # Name of the array to create.
    ARRAY_NAME = "quickstart_labels"

    LIBVERSION = tiledb.libtiledb.version()

    if LIBVERSION[0] == 2 and LIBVERSION[1] < 15:
        print(
            f"Dimension labels requires libtiledb version >= 2.15.0. Current version is"
            f" {LIBVERSION[0]}.{LIBVERSION[1]}.{LIBVERSION[2]}"
        )

    else:

        # Only create and write to the array if it doesn't already exist.
        if tiledb.object_type(ARRAY_NAME) != "array":
            create_array(ARRAY_NAME)
            write_array(ARRAY_NAME)

        # Read from the array and print output.
        read_array(ARRAY_NAME)
