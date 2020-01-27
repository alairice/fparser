# Copyright (c) 2020 Science and Technology Facilities Council.

# All rights reserved.

# Modifications made as part of the fparser project are distributed
# under the following license:

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:

# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

''' Test the get_child routine provided by utils.py. '''

import pytest
from fparser.api import get_reader


@pytest.mark.usefixtures("f2003_create")
def test_get_child():
    ''' Test the get_child() utility. '''
    from fparser import Fortran2003
    from fparser.utils import walk, get_child
    reader = get_reader("program hello\n"
                        "write(*,*) 'hello'\n"
                        "write(*,*) 'goodbye'\n"
                        "end program hello\n")
    main = Fortran2003.Program(reader)
    prog = get_child(main, Fortran2003.Main_Program)
    exe = get_child(prog, Fortran2003.Execution_Part)
    assert isinstance(exe, Fortran2003.Execution_Part)
    write_stmt = get_child(exe, Fortran2003.Write_Stmt)
    # Check that we got the first write and not the second
    assert "goodbye" not in str(write_stmt)
    # The top level has no Io_Control_Spec children
    assert not get_child(main, Fortran2003.Io_Control_Spec)
    # Check functionality when node has children in `items` and
    # not in `content`
    io_nodes = walk(main.content, Fortran2003.Io_Control_Spec)
    assert not hasattr(io_nodes[0], "content")
    io_unit = get_child(io_nodes[0], Fortran2003.Io_Unit)
    assert isinstance(io_unit, Fortran2003.Io_Unit)
    missing = get_child(io_nodes[0], Fortran2003.Execution_Part)
    assert missing is None
