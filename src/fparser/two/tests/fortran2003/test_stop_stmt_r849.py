# Copyright (c) 2018 Science and Technology Facilities Council

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

'''Test Fortran 2003 rule R849: this file tests the support for the
STOP Statement e.g.

    stop "some message here"

'''

import pytest
from fparser.two.Fortran2003 import Stop_Stmt
from fparser.two.utils import NoMatchError


@pytest.mark.usefixtures("f2003_create")
def test_stop_stmt():
    '''
    Tests for rule R849. The optional 'stop code' following a STOP must
    be either a scalar-char-constant or one or more digits.

    '''
    tcls = Stop_Stmt
    obj = tcls('stop')
    assert isinstance(obj, tcls), repr(obj)
    assert str(obj) == 'STOP'

    obj = tcls('stop 123')
    assert isinstance(obj, tcls), repr(obj)
    assert str(obj) == 'STOP 123'

    obj = tcls('stop   \'hey you\'')
    assert isinstance(obj, tcls), repr(obj)
    assert str(obj) == "STOP 'hey you'"

    obj = tcls('stop   "hey" // " you"')
    assert isinstance(obj, tcls), repr(obj)
    assert str(obj) == 'STOP "hey" // " you"'


@pytest.mark.usefixtures("f2003_create")
def test_stop_stmt_nomatch():
    '''
    Check that the stop statement does not match invalid statements.
    '''
    tcls = Stop_Stmt
    with pytest.raises(NoMatchError):
        tcls('stop   "hey" + " you"')
