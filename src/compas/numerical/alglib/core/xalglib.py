###########################################################################
# ALGLIB 3.13.0 (source code generated 2017-12-29)
# Copyright (c) Sergey Bochkanov (ALGLIB project).
# 
# >>> SOURCE LICENSE >>>
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation (www.fsf.org); either version 2 of the 
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# A copy of the GNU General Public License is available at
# http://www.fsf.org/licensing/licenses
# >>> END OF LICENSE >>>
##########################################################################



import sys
import os
import clr
import System

DT_BOOL = 1
DT_INT = 2
DT_REAL = 3
DT_COMPLEX = 4

X_SET     = 1 # data are copied into x-vector/matrix; previous contents of x-structure is freed
X_CREATE  = 2 # x-vector/matrix is created, its previous contents is ignored
X_REWRITE = 3 # data are copied into x-structure; size of Python structure must be equal to the x-structure size

curdir = os.path.dirname(__file__)
if curdir=="":
    curdir = "."
_net_candidates = []
_net_candidates.append(os.path.join(os.path.abspath(curdir),"alglibnet2.dll"))
# _net_candidates.append(os.path.join(os.path.relpath(curdir),"alglibnet2.dll"))
_net_candidates.append(os.path.join(sys.prefix,"alglibnet2.dll"))
_net_candidates.append(os.path.join(os.sep+"usr","local","alglibnet2.dll"))
for _candidate in _net_candidates:
    if os.path.isfile(_candidate):
        clr.AddReferenceToFileAndPath(_candidate)
        import alglib as _net_alglib
        break

def xsign(val):
    if val<0.0:
        return -1.0
    if val>0.0:
        return +1.0
    return 0.0
    
def setnworkers(nworkers):
    _net_alglib.setnworkers(nworkers)

#
# Checks that all values from list V are equal and returns first one.
# In case they are not equal, this function throws RuntimeError with message MSG.
#
def check_equality_and_get(v,msg):
    cnt = len(v)
    r = v[0]
    i = 1
    while i<cnt:
        if v[i]!=r:
            raise RuntimeError(msg)
        i += 1
    return r


#
# safe vector length:
# * returns list length.
# * throws ValueError if 'v' is not list (it uses
#   'msg' parameter to generate error message
#
def safe_len(msg,v):
    if type(v)!=list:
        raise ValueError(msg)
    return len(v)

#
# safe matrix size
# * returns number of columns
# * throws ValueError if 'v' is not rectangular matrix 
#   (list of lists of same size)
#   it uses 'msg' parameter to generate error message
#
def safe_cols(msg,v):
    if type(v)!=list:
        raise ValueError(msg)
    if len(v)==0:
        return 0
    if type(v[0])!=list:
        raise ValueError(msg)
    cols = len(v[0])
    for x in v:
        if type(x)!=list:
            raise ValueError(msg)
        if len(x)!=cols:
            raise ValueError(msg)
    return cols

#
# safe matrix size
# * returns number of rows
# * throws ValueError if 'v' is not rectangular matrix 
#   (list of lists of same size)
#   it uses 'msg' parameter to generate error message
#
def safe_rows(msg,v):
    if type(v)!=list:
        raise ValueError(msg)
    if len(v)==0:
        return 0
    if type(v[0])!=list:
        raise ValueError(msg)
    cols = len(v[0])
    for x in v:
        if type(x)!=list:
            raise ValueError(msg)
        if len(x)!=cols:
            raise ValueError(msg)
    return len(v)

def create_real_vector(cnt):
    if cnt<=0:
        return []
    return [0]*cnt

def create_real_matrix(rows, cols):
    if rows<=0 or cols<=0:
        return [[]]
    matrix = []
    row = 0
    while row<rows:
        matrix += [[0]*cols]
        row += 1
    return matrix

def is_bool(v):
    try:
        tmp = bool(v)
    except:
        return False
    return True

def is_int(v):
    try:
        tmp = int(v)
    except:
        return False
    return True

def is_real(v):
    try:
        tmp = float(v)
    except:
        return False
    return True

def is_complex(v):
    try:
        tmp = complex(v)
    except:
        return False
    return True

def is_bool_vector(v):
    if type(v)!=list:
        return False
    for x in v:
        try:
            tmp = bool(x)
        except:
            return False
    return True

def is_bool_matrix(v):
    if type(v)!=list:
        return False
    if len(v)==0:
        return True
    if type(v[0])!=list:
        return False
    rows = len(v)
    cols = len(v[0])
    for x in v:
        if type(x)!=list:
            return False
        if len(x)!=cols:
            return False
        for y in x:
            try:
                tmp = bool(y)
            except:
                return False
    return True

def is_int_vector(v):
    if type(v)!=list:
        return False
    for x in v:
        try:
            tmp = int(x)
        except:
            return False
    return True

def is_int_matrix(v):
    if type(v)!=list:
        return False
    if len(v)==0:
        return True
    if type(v[0])!=list:
        return False
    rows = len(v)
    cols = len(v[0])
    for x in v:
        if type(x)!=list:
            return False
        if len(x)!=cols:
            return False
        for y in x:
            try:
                tmp = int(y)
            except:
                return False
    return True

def is_real_vector(v):
    if type(v)!=list:
        return False
    for x in v:
        try:
            tmp = float(x)
        except:
            return False
    return True

def is_real_matrix(v):
    if type(v)!=list:
        return False
    if len(v)==0:
        return True
    if type(v[0])!=list:
        return False
    rows = len(v)
    cols = len(v[0])
    for x in v:
        if type(x)!=list:
            return False
        if len(x)!=cols:
            return False
        for y in x:
            try:
                tmp = float(y)
            except:
                return False
    return True

def is_complex_vector(v):
    if type(v)!=list:
        return False
    for x in v:
        try:
            tmp = complex(x)
        except:
            return False
    return True

def is_complex_matrix(v):
    if type(v)!=list:
        return False
    if len(v)==0:
        return True
    if type(v[0])!=list:
        return False
    rows = len(v)
    cols = len(v[0])
    for x in v:
        if type(x)!=list:
            return False
        if len(x)!=cols:
            return False
        for y in x:
            try:
                tmp = complex(y)
            except:
                return False
    return True

#
# conversion from list to .NET 1-dimensional array:
#
# Parameters:
# v     list
# dt    datatype
# msg   error message (exception with this message is thrown in case of error)
#
# Returns .NET array
#
def net_from_list(v, dt, msg = ""):
    #
    # check types
    #
    if dt==DT_BOOL:
        if not is_bool_vector(v):
            raise ValueError(msg if msg!="" else "can't cast to bool_vector")
        x = System.Array.CreateInstance(bool, len(v))
    if dt==DT_INT:
        if not is_int_vector(v):
            raise ValueError(msg if msg!="" else "can't cast to int_vector")
        x = System.Array.CreateInstance(int, len(v))
    if dt==DT_REAL:
        if not is_real_vector(v):
            raise ValueError(msg if msg!="" else "can't cast to real_vector")
        x = System.Array.CreateInstance(float, len(v))
    if dt==DT_COMPLEX:
        if not is_complex_vector(v):
            raise ValueError(msg if msg!="" else "can't cast to complex_vector")
        x = System.Array.CreateInstance(_net_alglib.complex, len(v))
    
    #
    # copy
    #
    copy_list_to_net(v, x, dt)
    return x


#
# conversion from list of lists to .NET 2-dimensional array:
#
# Parameters:
# v     list of lists
# dt    datatype
# msg   error message (exception with this message is thrown in case of error)
#
# Returns .NET array
#
def net_from_listlist(v, dt, msg = ""):
    #
    # check types
    #
    if dt==DT_BOOL:
        if not is_bool_matrix(v):
            raise ValueError(msg if msg!="" else "can't cast to bool_matrix")
    if dt==DT_INT:
        if not is_int_matrix(v):
            raise ValueError(msg if msg!="" else "can't cast to int_matrix")
    if dt==DT_REAL:
        if not is_real_matrix(v):
            raise ValueError(msg if msg!="" else "can't cast to real_matrix")
    if dt==DT_COMPLEX:
        if not is_complex_matrix(v):
            raise ValueError(msg if msg!="" else "can't cast to complex_matrix")
    
    #
    # determine size
    #
    rows = len(v)
    if rows>0:
        cols = len(v[0])
    else:
        cols = 0
    if cols==0:
        rows = 0
    
    #
    # allocation
    #
    if dt==DT_BOOL:
        x = System.Array.CreateInstance(bool, rows, cols)
    if dt==DT_INT:
        x = System.Array.CreateInstance(int, rows, cols)
    if dt==DT_REAL:
        x = System.Array.CreateInstance(float, rows, cols)
    if dt==DT_COMPLEX:
        x = System.Array.CreateInstance(_net_alglib.complex, rows, cols)
    
    #
    # copy
    #
    copy_listlist_to_net(v, x, dt)
    return x


#
# conversion from .NET vector to Python vector
#
# Parameters:
# * x       .NET vector
# * dt      datatype code
#
def list_from_net(x, dt):
    cnt = x.GetLength(0)
    if cnt==0:
        return []
    r = [0]*cnt
    if dt==DT_COMPLEX:
        i = 0
        while i<cnt:
            r[i] = complex(x[i].x, x[i].y)
            i += 1
    else:
        i = 0
        while i<cnt:
            r[i] = x[i]
            i += 1
    return r


#
# conversion from NET-matrix to Python matrix
#
# Parameters:
# * x       .NET matrix
# * dt      datatype code
#
def listlist_from_net(x, dt):
    if x.GetLength(0)==0 or x.GetLength(1)==0:
        return [[]]
    r = create_real_matrix(x.GetLength(0), x.GetLength(1))
    m = x.GetLength(0)
    n = x.GetLength(1)
    i = 0
    while i<m:
        dstrow = r[i]
        j = 0
        while j<n:
            if dt==DT_COMPLEX:
                dstrow[j] = complex(x[i,j].x, x[i,j].y)
            else:
                dstrow[j] = x[i,j]
            j += 1
        i += 1
    return r


#
# this function copies NET-vector to previously allocated list 
# which should be large enough to store x-vector.
#
# invalid access to list is generated if list is too small.
#
# Parameters:
# * x       NET-vector
# * r       list which stores result
# * dt      datatype code
#
def copy_net_to_list(x, r, dt):
    cnt = x.GetLength(0)
    if dt==DT_COMPLEX:
        i = 0
        while i<cnt:
            r[i] = complex(x[i].x, x[i].y)
            i += 1
    else:
        i = 0
        while i<cnt:
            r[i] = x[i]
            i += 1
    return


#
# conversion from NET-matrix to Python matrix
#
# Parameters:
# * x       .NET matrix
# * t       list of lists which stores result
# * dt      datatype code
#
def copy_net_to_listlist(x, r, dt):
    m = x.GetLength(0)
    n = x.GetLength(1)
    i = 0
    while i<m:
        dstrow = r[i]
        j = 0
        while j<n:
            if dt==DT_COMPLEX:
                dstrow[j] = complex(x[i,j].x, x[i,j].y)
            else:
                dstrow[j] = x[i,j]
            j += 1
        i += 1
    return


#
# This function copies contents of V to preallocated NET array X.
# This function makes no checks regarding its arguments.
# If X is too short, invalid access to X will be generated.
#
# Parameters:
# v     list
# x     NET array
# dt    datatype
#
def copy_list_to_net(v, x, dt):
    #
    # copy
    #
    cnt = len(v)
    if dt==DT_BOOL:
        i = 0
        while i<cnt:
            x[i] =   bool(v[i])
            i += 1
    if dt==DT_INT:
        i = 0
        while i<cnt:
            x[i] =    int(v[i])
            i += 1
    if dt==DT_REAL:
        i = 0
        while i<cnt:
            x[i] = float(v[i])
            i += 1
    if dt==DT_COMPLEX:
        i = 0
        while i<cnt:
            tmp = complex(v[i])
            x[i] = _net_alglib.complex(tmp.real,tmp.imag)
            i += 1


#
# This function copies contents of V to preallocated NET 2D array X.
# This function makes no checks regarding its arguments.
# If X is too short, invalid access to X will be generated.
#
# Parameters:
# v     list of lists
# x     NET 2D array
# dt    datatype
#
def copy_listlist_to_net(v, x, dt):
    #
    # determine size
    #
    rows = len(v)
    if rows>0:
        cols = len(v[0])
    else:
        cols = 0
    if cols==0:
        rows = 0
    
    #
    # copy
    #
    i = 0
    while i<rows:
        row = v[i]
        j = 0
        while j<cols:
            if dt==DT_BOOL:
                x[i,j] = bool(row[j])
            if dt==DT_INT:
                x[i,j] = int(row[j])
            if dt==DT_REAL:
                x[i,j] = float(row[j])
            if dt==DT_COMPLEX:
                tmp = complex(row[j])
                x[i,j] = _net_alglib.complex(tmp.real,tmp.imag)
            j += 1
        i += 1



class kdtreerequestbuffer(object):
    def __init__(self,ptr):
        self.ptr = ptr


class kdtree(object):
    def __init__(self,ptr):
        self.ptr = ptr
def kdtreeserialize(obj):
    try:
        return _net_alglib.kdtreeserialize(obj.ptr)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

def kdtreeunserialize(s_in):
    try:
        return kdtree(_net_alglib.kdtreeunserialize(s_in))
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)
def kdtreebuild(*functionargs):
    # unpack inputs
    if len(functionargs)==5:
        # full-form call
        xy, n, nx, ny, normtype = functionargs
        friendly_form = False
    elif len(functionargs)==4:
        # short-form call
        xy, nx, ny, normtype = functionargs
        n = check_equality_and_get([safe_rows("'kdtreebuild': incorrect parameters",xy)],"Error while calling 'kdtreebuild': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'kdtreebuild': function must have 5 or 4 parameters")

    # convert to .NET types
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.kdtreebuild' must be real matrix")
    _net_n = n
    _net_nx = nx
    _net_ny = ny
    _net_normtype = normtype
    try:

        # call function
        _net_kdt = _net_alglib.kdtreebuild(_net_xy, _net_n, _net_nx, _net_ny, _net_normtype)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    kdt = kdtree(_net_kdt)

    # return
    return kdt

def kdtreebuildtagged(*functionargs):
    # unpack inputs
    if len(functionargs)==6:
        # full-form call
        xy, tags, n, nx, ny, normtype = functionargs
        friendly_form = False
    elif len(functionargs)==5:
        # short-form call
        xy, tags, nx, ny, normtype = functionargs
        n = check_equality_and_get([safe_rows("'kdtreebuildtagged': incorrect parameters",xy), safe_len("'kdtreebuildtagged': incorrect parameters",tags)],"Error while calling 'kdtreebuildtagged': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'kdtreebuildtagged': function must have 6 or 5 parameters")

    # convert to .NET types
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.kdtreebuildtagged' must be real matrix")
    _net_tags = net_from_list(tags, DT_INT, "ALGLIB: parameter 'tags' of 'xalglib.kdtreebuildtagged' must be int vector")
    _net_n = n
    _net_nx = nx
    _net_ny = ny
    _net_normtype = normtype
    try:

        # call function
        _net_kdt = _net_alglib.kdtreebuildtagged(_net_xy, _net_tags, _net_n, _net_nx, _net_ny, _net_normtype)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    kdt = kdtree(_net_kdt)

    # return
    return kdt

def kdtreecreaterequestbuffer(*functionargs):
    # unpack inputs
    kdt,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_kdt = kdt.ptr
    try:

        # call function
        _net_buf = _net_alglib.kdtreecreaterequestbuffer(_net_kdt)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    buf = kdtreerequestbuffer(_net_buf)

    # return
    return buf

def kdtreequeryknn(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        kdt, x, k, selfmatch = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        kdt, x, k = functionargs
        selfmatch = check_equality_and_get([True],"Error while calling 'kdtreequeryknn': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'kdtreequeryknn': function must have 4 or 3 parameters")

    # convert to .NET types
    _net_kdt = kdt.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.kdtreequeryknn' must be real vector")
    _net_k = k
    _net_selfmatch = selfmatch
    try:

        # call function
        _net_result = _net_alglib.kdtreequeryknn(_net_kdt, _net_x, _net_k, _net_selfmatch)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def kdtreetsqueryknn(*functionargs):
    # unpack inputs
    if len(functionargs)==5:
        # full-form call
        kdt, buf, x, k, selfmatch = functionargs
        friendly_form = False
    elif len(functionargs)==4:
        # short-form call
        kdt, buf, x, k = functionargs
        selfmatch = check_equality_and_get([True],"Error while calling 'kdtreetsqueryknn': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'kdtreetsqueryknn': function must have 5 or 4 parameters")

    # convert to .NET types
    _net_kdt = kdt.ptr
    _net_buf = buf.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.kdtreetsqueryknn' must be real vector")
    _net_k = k
    _net_selfmatch = selfmatch
    try:

        # call function
        _net_result = _net_alglib.kdtreetsqueryknn(_net_kdt, _net_buf, _net_x, _net_k, _net_selfmatch)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def kdtreequeryrnn(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        kdt, x, r, selfmatch = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        kdt, x, r = functionargs
        selfmatch = check_equality_and_get([True],"Error while calling 'kdtreequeryrnn': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'kdtreequeryrnn': function must have 4 or 3 parameters")

    # convert to .NET types
    _net_kdt = kdt.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.kdtreequeryrnn' must be real vector")
    _net_r = r
    _net_selfmatch = selfmatch
    try:

        # call function
        _net_result = _net_alglib.kdtreequeryrnn(_net_kdt, _net_x, _net_r, _net_selfmatch)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def kdtreetsqueryrnn(*functionargs):
    # unpack inputs
    if len(functionargs)==5:
        # full-form call
        kdt, buf, x, r, selfmatch = functionargs
        friendly_form = False
    elif len(functionargs)==4:
        # short-form call
        kdt, buf, x, r = functionargs
        selfmatch = check_equality_and_get([True],"Error while calling 'kdtreetsqueryrnn': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'kdtreetsqueryrnn': function must have 5 or 4 parameters")

    # convert to .NET types
    _net_kdt = kdt.ptr
    _net_buf = buf.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.kdtreetsqueryrnn' must be real vector")
    _net_r = r
    _net_selfmatch = selfmatch
    try:

        # call function
        _net_result = _net_alglib.kdtreetsqueryrnn(_net_kdt, _net_buf, _net_x, _net_r, _net_selfmatch)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def kdtreequeryaknn(*functionargs):
    # unpack inputs
    if len(functionargs)==5:
        # full-form call
        kdt, x, k, selfmatch, eps = functionargs
        friendly_form = False
    elif len(functionargs)==4:
        # short-form call
        kdt, x, k, eps = functionargs
        selfmatch = check_equality_and_get([True],"Error while calling 'kdtreequeryaknn': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'kdtreequeryaknn': function must have 5 or 4 parameters")

    # convert to .NET types
    _net_kdt = kdt.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.kdtreequeryaknn' must be real vector")
    _net_k = k
    _net_selfmatch = selfmatch
    _net_eps = eps
    try:

        # call function
        _net_result = _net_alglib.kdtreequeryaknn(_net_kdt, _net_x, _net_k, _net_selfmatch, _net_eps)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def kdtreetsqueryaknn(*functionargs):
    # unpack inputs
    if len(functionargs)==6:
        # full-form call
        kdt, buf, x, k, selfmatch, eps = functionargs
        friendly_form = False
    elif len(functionargs)==5:
        # short-form call
        kdt, buf, x, k, eps = functionargs
        selfmatch = check_equality_and_get([True],"Error while calling 'kdtreetsqueryaknn': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'kdtreetsqueryaknn': function must have 6 or 5 parameters")

    # convert to .NET types
    _net_kdt = kdt.ptr
    _net_buf = buf.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.kdtreetsqueryaknn' must be real vector")
    _net_k = k
    _net_selfmatch = selfmatch
    _net_eps = eps
    try:

        # call function
        _net_result = _net_alglib.kdtreetsqueryaknn(_net_kdt, _net_buf, _net_x, _net_k, _net_selfmatch, _net_eps)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def kdtreequerybox(*functionargs):
    # unpack inputs
    kdt, boxmin, boxmax = functionargs
    friendly_form = False

    # convert to .NET types
    _net_kdt = kdt.ptr
    _net_boxmin = net_from_list(boxmin, DT_REAL, "ALGLIB: parameter 'boxmin' of 'xalglib.kdtreequerybox' must be real vector")
    _net_boxmax = net_from_list(boxmax, DT_REAL, "ALGLIB: parameter 'boxmax' of 'xalglib.kdtreequerybox' must be real vector")
    try:

        # call function
        _net_result = _net_alglib.kdtreequerybox(_net_kdt, _net_boxmin, _net_boxmax)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def kdtreetsquerybox(*functionargs):
    # unpack inputs
    kdt, buf, boxmin, boxmax = functionargs
    friendly_form = False

    # convert to .NET types
    _net_kdt = kdt.ptr
    _net_buf = buf.ptr
    _net_boxmin = net_from_list(boxmin, DT_REAL, "ALGLIB: parameter 'boxmin' of 'xalglib.kdtreetsquerybox' must be real vector")
    _net_boxmax = net_from_list(boxmax, DT_REAL, "ALGLIB: parameter 'boxmax' of 'xalglib.kdtreetsquerybox' must be real vector")
    try:

        # call function
        _net_result = _net_alglib.kdtreetsquerybox(_net_kdt, _net_buf, _net_boxmin, _net_boxmax)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def kdtreequeryresultsx(*functionargs):
    # unpack inputs
    kdt, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_kdt = kdt.ptr
    _net_x = net_from_listlist(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.kdtreequeryresultsx' must be real matrix")
    try:

        # call function
        _net_x = _net_alglib.kdtreequeryresultsx(_net_kdt, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = listlist_from_net(_net_x, DT_REAL)

    # return
    return x

def kdtreequeryresultsxy(*functionargs):
    # unpack inputs
    kdt, xy = functionargs
    friendly_form = False

    # convert to .NET types
    _net_kdt = kdt.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.kdtreequeryresultsxy' must be real matrix")
    try:

        # call function
        _net_xy = _net_alglib.kdtreequeryresultsxy(_net_kdt, _net_xy)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    xy = listlist_from_net(_net_xy, DT_REAL)

    # return
    return xy

def kdtreequeryresultstags(*functionargs):
    # unpack inputs
    kdt, tags = functionargs
    friendly_form = False

    # convert to .NET types
    _net_kdt = kdt.ptr
    _net_tags = net_from_list(tags, DT_INT, "ALGLIB: parameter 'tags' of 'xalglib.kdtreequeryresultstags' must be int vector")
    try:

        # call function
        _net_tags = _net_alglib.kdtreequeryresultstags(_net_kdt, _net_tags)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    tags = list_from_net(_net_tags, DT_INT)

    # return
    return tags

def kdtreequeryresultsdistances(*functionargs):
    # unpack inputs
    kdt, r = functionargs
    friendly_form = False

    # convert to .NET types
    _net_kdt = kdt.ptr
    _net_r = net_from_list(r, DT_REAL, "ALGLIB: parameter 'r' of 'xalglib.kdtreequeryresultsdistances' must be real vector")
    try:

        # call function
        _net_r = _net_alglib.kdtreequeryresultsdistances(_net_kdt, _net_r)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    r = list_from_net(_net_r, DT_REAL)

    # return
    return r

def kdtreetsqueryresultsx(*functionargs):
    # unpack inputs
    kdt, buf, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_kdt = kdt.ptr
    _net_buf = buf.ptr
    _net_x = net_from_listlist(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.kdtreetsqueryresultsx' must be real matrix")
    try:

        # call function
        _net_x = _net_alglib.kdtreetsqueryresultsx(_net_kdt, _net_buf, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = listlist_from_net(_net_x, DT_REAL)

    # return
    return x

def kdtreetsqueryresultsxy(*functionargs):
    # unpack inputs
    kdt, buf, xy = functionargs
    friendly_form = False

    # convert to .NET types
    _net_kdt = kdt.ptr
    _net_buf = buf.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.kdtreetsqueryresultsxy' must be real matrix")
    try:

        # call function
        _net_xy = _net_alglib.kdtreetsqueryresultsxy(_net_kdt, _net_buf, _net_xy)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    xy = listlist_from_net(_net_xy, DT_REAL)

    # return
    return xy

def kdtreetsqueryresultstags(*functionargs):
    # unpack inputs
    kdt, buf, tags = functionargs
    friendly_form = False

    # convert to .NET types
    _net_kdt = kdt.ptr
    _net_buf = buf.ptr
    _net_tags = net_from_list(tags, DT_INT, "ALGLIB: parameter 'tags' of 'xalglib.kdtreetsqueryresultstags' must be int vector")
    try:

        # call function
        _net_tags = _net_alglib.kdtreetsqueryresultstags(_net_kdt, _net_buf, _net_tags)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    tags = list_from_net(_net_tags, DT_INT)

    # return
    return tags

def kdtreetsqueryresultsdistances(*functionargs):
    # unpack inputs
    kdt, buf, r = functionargs
    friendly_form = False

    # convert to .NET types
    _net_kdt = kdt.ptr
    _net_buf = buf.ptr
    _net_r = net_from_list(r, DT_REAL, "ALGLIB: parameter 'r' of 'xalglib.kdtreetsqueryresultsdistances' must be real vector")
    try:

        # call function
        _net_r = _net_alglib.kdtreetsqueryresultsdistances(_net_kdt, _net_buf, _net_r)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    r = list_from_net(_net_r, DT_REAL)

    # return
    return r

def kdtreequeryresultsxi(*functionargs):
    # unpack inputs
    kdt,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_kdt = kdt.ptr
    try:

        # call function
        _net_x = _net_alglib.kdtreequeryresultsxi(_net_kdt)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = listlist_from_net(_net_x, DT_REAL)

    # return
    return x

def kdtreequeryresultsxyi(*functionargs):
    # unpack inputs
    kdt,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_kdt = kdt.ptr
    try:

        # call function
        _net_xy = _net_alglib.kdtreequeryresultsxyi(_net_kdt)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    xy = listlist_from_net(_net_xy, DT_REAL)

    # return
    return xy

def kdtreequeryresultstagsi(*functionargs):
    # unpack inputs
    kdt,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_kdt = kdt.ptr
    try:

        # call function
        _net_tags = _net_alglib.kdtreequeryresultstagsi(_net_kdt)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    tags = list_from_net(_net_tags, DT_INT)

    # return
    return tags

def kdtreequeryresultsdistancesi(*functionargs):
    # unpack inputs
    kdt,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_kdt = kdt.ptr
    try:

        # call function
        _net_r = _net_alglib.kdtreequeryresultsdistancesi(_net_kdt)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    r = list_from_net(_net_r, DT_REAL)

    # return
    return r



class hqrndstate(object):
    def __init__(self,ptr):
        self.ptr = ptr
def hqrndrandomize(*functionargs):
    # unpack inputs
    friendly_form = False

    # convert to .NET types
    try:

        # call function
        _net_state = _net_alglib.hqrndrandomize()
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = hqrndstate(_net_state)

    # return
    return state

def hqrndseed(*functionargs):
    # unpack inputs
    s1, s2 = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s1 = s1
    _net_s2 = s2
    try:

        # call function
        _net_state = _net_alglib.hqrndseed(_net_s1, _net_s2)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = hqrndstate(_net_state)

    # return
    return state

def hqrnduniformr(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_result = _net_alglib.hqrnduniformr(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def hqrnduniformi(*functionargs):
    # unpack inputs
    state, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_n = n
    try:

        # call function
        _net_result = _net_alglib.hqrnduniformi(_net_state, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def hqrndnormal(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_result = _net_alglib.hqrndnormal(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def hqrndunit2(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_x, _net_y = _net_alglib.hqrndunit2(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = _net_x
    y = _net_y

    # return
    return (x, y)

def hqrndnormal2(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_x1, _net_x2 = _net_alglib.hqrndnormal2(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x1 = _net_x1
    x2 = _net_x2

    # return
    return (x1, x2)

def hqrndexponential(*functionargs):
    # unpack inputs
    state, lambdav = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_lambdav = lambdav
    try:

        # call function
        _net_result = _net_alglib.hqrndexponential(_net_state, _net_lambdav)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def hqrnddiscrete(*functionargs):
    # unpack inputs
    state, x, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.hqrnddiscrete' must be real vector")
    _net_n = n
    try:

        # call function
        _net_result = _net_alglib.hqrnddiscrete(_net_state, _net_x, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def hqrndcontinuous(*functionargs):
    # unpack inputs
    state, x, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.hqrndcontinuous' must be real vector")
    _net_n = n
    try:

        # call function
        _net_result = _net_alglib.hqrndcontinuous(_net_state, _net_x, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result



class xdebugrecord1(object):
    def __init__(self):
        self.i = 0
        self.c = 0
        self.a = []


def net_from_xdebugrecord1(x,v):
    x.i = int(v.i)
    tmp = complex(v.c)
    x.c = _net_alglib.complex(tmp.real,tmp.imag)
    x.a = net_from_list(v.a, DT_REAL)
    return




def xdebugrecord1_from_net(x):
    r = xdebugrecord1()
    r.i = x.i
    r.c = complex(x.c.x,x.c.y)
    r.a = list_from_net(x.a, DT_REAL)
    return r


def xdebuginitrecord1(*functionargs):
    # unpack inputs
    friendly_form = False

    # convert to .NET types
    try:

        # call function
        _net_rec1 = _net_alglib.xdebuginitrecord1()
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    rec1 = xdebugrecord1_from_net(_net_rec1)

    # return
    return rec1

def xdebugb1count(*functionargs):
    # unpack inputs
    a,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_list(a, DT_BOOL, "ALGLIB: parameter 'a' of 'xalglib.xdebugb1count' must be bool vector")
    try:

        # call function
        _net_result = _net_alglib.xdebugb1count(_net_a)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def xdebugb1not(*functionargs):
    # unpack inputs
    a,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_list(a, DT_BOOL, "ALGLIB: parameter 'a' of 'xalglib.xdebugb1not' must be bool vector")
    try:

        # call function
        _net_a = _net_alglib.xdebugb1not(_net_a)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = list_from_net(_net_a, DT_BOOL)

    # return
    return a

def xdebugb1appendcopy(*functionargs):
    # unpack inputs
    a,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_list(a, DT_BOOL, "ALGLIB: parameter 'a' of 'xalglib.xdebugb1appendcopy' must be bool vector")
    try:

        # call function
        _net_a = _net_alglib.xdebugb1appendcopy(_net_a)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = list_from_net(_net_a, DT_BOOL)

    # return
    return a

def xdebugb1outeven(*functionargs):
    # unpack inputs
    n,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    try:

        # call function
        _net_a = _net_alglib.xdebugb1outeven(_net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = list_from_net(_net_a, DT_BOOL)

    # return
    return a

def xdebugi1sum(*functionargs):
    # unpack inputs
    a,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_list(a, DT_INT, "ALGLIB: parameter 'a' of 'xalglib.xdebugi1sum' must be int vector")
    try:

        # call function
        _net_result = _net_alglib.xdebugi1sum(_net_a)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def xdebugi1neg(*functionargs):
    # unpack inputs
    a,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_list(a, DT_INT, "ALGLIB: parameter 'a' of 'xalglib.xdebugi1neg' must be int vector")
    try:

        # call function
        _net_a = _net_alglib.xdebugi1neg(_net_a)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = list_from_net(_net_a, DT_INT)

    # return
    return a

def xdebugi1appendcopy(*functionargs):
    # unpack inputs
    a,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_list(a, DT_INT, "ALGLIB: parameter 'a' of 'xalglib.xdebugi1appendcopy' must be int vector")
    try:

        # call function
        _net_a = _net_alglib.xdebugi1appendcopy(_net_a)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = list_from_net(_net_a, DT_INT)

    # return
    return a

def xdebugi1outeven(*functionargs):
    # unpack inputs
    n,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    try:

        # call function
        _net_a = _net_alglib.xdebugi1outeven(_net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = list_from_net(_net_a, DT_INT)

    # return
    return a

def xdebugr1sum(*functionargs):
    # unpack inputs
    a,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_list(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.xdebugr1sum' must be real vector")
    try:

        # call function
        _net_result = _net_alglib.xdebugr1sum(_net_a)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def xdebugr1neg(*functionargs):
    # unpack inputs
    a,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_list(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.xdebugr1neg' must be real vector")
    try:

        # call function
        _net_a = _net_alglib.xdebugr1neg(_net_a)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = list_from_net(_net_a, DT_REAL)

    # return
    return a

def xdebugr1appendcopy(*functionargs):
    # unpack inputs
    a,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_list(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.xdebugr1appendcopy' must be real vector")
    try:

        # call function
        _net_a = _net_alglib.xdebugr1appendcopy(_net_a)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = list_from_net(_net_a, DT_REAL)

    # return
    return a

def xdebugr1outeven(*functionargs):
    # unpack inputs
    n,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    try:

        # call function
        _net_a = _net_alglib.xdebugr1outeven(_net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = list_from_net(_net_a, DT_REAL)

    # return
    return a

def xdebugc1sum(*functionargs):
    # unpack inputs
    a,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_list(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.xdebugc1sum' must be complex vector")
    try:

        # call function
        _net_result = _net_alglib.xdebugc1sum(_net_a)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = complex(_net_result.x,_net_result.y)

    # return
    return result

def xdebugc1neg(*functionargs):
    # unpack inputs
    a,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_list(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.xdebugc1neg' must be complex vector")
    try:

        # call function
        _net_a = _net_alglib.xdebugc1neg(_net_a)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = list_from_net(_net_a, DT_COMPLEX)

    # return
    return a

def xdebugc1appendcopy(*functionargs):
    # unpack inputs
    a,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_list(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.xdebugc1appendcopy' must be complex vector")
    try:

        # call function
        _net_a = _net_alglib.xdebugc1appendcopy(_net_a)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = list_from_net(_net_a, DT_COMPLEX)

    # return
    return a

def xdebugc1outeven(*functionargs):
    # unpack inputs
    n,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    try:

        # call function
        _net_a = _net_alglib.xdebugc1outeven(_net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = list_from_net(_net_a, DT_COMPLEX)

    # return
    return a

def xdebugb2count(*functionargs):
    # unpack inputs
    a,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_BOOL, "ALGLIB: parameter 'a' of 'xalglib.xdebugb2count' must be bool matrix")
    try:

        # call function
        _net_result = _net_alglib.xdebugb2count(_net_a)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def xdebugb2not(*functionargs):
    # unpack inputs
    a,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_BOOL, "ALGLIB: parameter 'a' of 'xalglib.xdebugb2not' must be bool matrix")
    try:

        # call function
        _net_a = _net_alglib.xdebugb2not(_net_a)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_BOOL)

    # return
    return a

def xdebugb2transpose(*functionargs):
    # unpack inputs
    a,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_BOOL, "ALGLIB: parameter 'a' of 'xalglib.xdebugb2transpose' must be bool matrix")
    try:

        # call function
        _net_a = _net_alglib.xdebugb2transpose(_net_a)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_BOOL)

    # return
    return a

def xdebugb2outsin(*functionargs):
    # unpack inputs
    m, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    try:

        # call function
        _net_a = _net_alglib.xdebugb2outsin(_net_m, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_BOOL)

    # return
    return a

def xdebugi2sum(*functionargs):
    # unpack inputs
    a,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_INT, "ALGLIB: parameter 'a' of 'xalglib.xdebugi2sum' must be int matrix")
    try:

        # call function
        _net_result = _net_alglib.xdebugi2sum(_net_a)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def xdebugi2neg(*functionargs):
    # unpack inputs
    a,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_INT, "ALGLIB: parameter 'a' of 'xalglib.xdebugi2neg' must be int matrix")
    try:

        # call function
        _net_a = _net_alglib.xdebugi2neg(_net_a)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_INT)

    # return
    return a

def xdebugi2transpose(*functionargs):
    # unpack inputs
    a,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_INT, "ALGLIB: parameter 'a' of 'xalglib.xdebugi2transpose' must be int matrix")
    try:

        # call function
        _net_a = _net_alglib.xdebugi2transpose(_net_a)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_INT)

    # return
    return a

def xdebugi2outsin(*functionargs):
    # unpack inputs
    m, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    try:

        # call function
        _net_a = _net_alglib.xdebugi2outsin(_net_m, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_INT)

    # return
    return a

def xdebugr2sum(*functionargs):
    # unpack inputs
    a,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.xdebugr2sum' must be real matrix")
    try:

        # call function
        _net_result = _net_alglib.xdebugr2sum(_net_a)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def xdebugr2neg(*functionargs):
    # unpack inputs
    a,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.xdebugr2neg' must be real matrix")
    try:

        # call function
        _net_a = _net_alglib.xdebugr2neg(_net_a)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)

    # return
    return a

def xdebugr2transpose(*functionargs):
    # unpack inputs
    a,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.xdebugr2transpose' must be real matrix")
    try:

        # call function
        _net_a = _net_alglib.xdebugr2transpose(_net_a)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)

    # return
    return a

def xdebugr2outsin(*functionargs):
    # unpack inputs
    m, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    try:

        # call function
        _net_a = _net_alglib.xdebugr2outsin(_net_m, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)

    # return
    return a

def xdebugc2sum(*functionargs):
    # unpack inputs
    a,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.xdebugc2sum' must be complex matrix")
    try:

        # call function
        _net_result = _net_alglib.xdebugc2sum(_net_a)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = complex(_net_result.x,_net_result.y)

    # return
    return result

def xdebugc2neg(*functionargs):
    # unpack inputs
    a,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.xdebugc2neg' must be complex matrix")
    try:

        # call function
        _net_a = _net_alglib.xdebugc2neg(_net_a)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_COMPLEX)

    # return
    return a

def xdebugc2transpose(*functionargs):
    # unpack inputs
    a,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.xdebugc2transpose' must be complex matrix")
    try:

        # call function
        _net_a = _net_alglib.xdebugc2transpose(_net_a)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_COMPLEX)

    # return
    return a

def xdebugc2outsincos(*functionargs):
    # unpack inputs
    m, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    try:

        # call function
        _net_a = _net_alglib.xdebugc2outsincos(_net_m, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_COMPLEX)

    # return
    return a

def xdebugmaskedbiasedproductsum(*functionargs):
    # unpack inputs
    m, n, a, b, c = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.xdebugmaskedbiasedproductsum' must be real matrix")
    _net_b = net_from_listlist(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.xdebugmaskedbiasedproductsum' must be real matrix")
    _net_c = net_from_listlist(c, DT_BOOL, "ALGLIB: parameter 'c' of 'xalglib.xdebugmaskedbiasedproductsum' must be bool matrix")
    try:

        # call function
        _net_result = _net_alglib.xdebugmaskedbiasedproductsum(_net_m, _net_n, _net_a, _net_b, _net_c)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result



class odesolverstate(object):
    def __init__(self,ptr):
        self.ptr = ptr


class odesolverreport(object):
    def __init__(self):
        self.nfev = 0
        self.terminationtype = 0


def net_from_odesolverreport(x,v):
    x.nfev = int(v.nfev)
    x.terminationtype = int(v.terminationtype)
    return




def odesolverreport_from_net(x):
    r = odesolverreport()
    r.nfev = x.nfev
    r.terminationtype = x.terminationtype
    return r


def odesolverrkck(*functionargs):
    # unpack inputs
    if len(functionargs)==6:
        # full-form call
        y, n, x, m, eps, h = functionargs
        friendly_form = False
    elif len(functionargs)==4:
        # short-form call
        y, x, eps, h = functionargs
        n = check_equality_and_get([safe_len("'odesolverrkck': incorrect parameters",y)],"Error while calling 'odesolverrkck': looks like one of arguments has wrong size")
        m = check_equality_and_get([safe_len("'odesolverrkck': incorrect parameters",x)],"Error while calling 'odesolverrkck': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'odesolverrkck': function must have 6 or 4 parameters")

    # convert to .NET types
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.odesolverrkck' must be real vector")
    _net_n = n
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.odesolverrkck' must be real vector")
    _net_m = m
    _net_eps = eps
    _net_h = h
    try:

        # call function
        _net_state = _net_alglib.odesolverrkck(_net_y, _net_n, _net_x, _net_m, _net_eps, _net_h)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = odesolverstate(_net_state)

    # return
    return state



def odesolversolve(state, dy, param = None):
    # initialize reverse communication variables
    _net_y = state.ptr.y
    _py_y = create_real_vector(_net_y.GetLength(0))
    _net_dy = state.ptr.dy
    _py_dy = create_real_vector(_net_dy.GetLength(0))
    
    # algorithm iterations
    while True:
        try:
            result = _net_alglib.odesolveriteration(state.ptr)
        except _net_alglib.alglibexception as e:
            raise RuntimeError(e.msg)
        if not result:
            break
        if state.ptr.needdy:
            copy_net_to_list(_net_y, _py_y, DT_REAL)
            dy(_py_y, state.ptr.x, _py_dy, param)
            copy_list_to_net(_py_dy, _net_dy, DT_REAL)
            continue
        raise RuntimeError("ALGLIB: unexpected error in 'odesolversolve'")
    return


def odesolverresults(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_m, _net_xtbl, _net_ytbl, _net_rep = _net_alglib.odesolverresults(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    m = _net_m
    xtbl = list_from_net(_net_xtbl, DT_REAL)
    ytbl = listlist_from_net(_net_ytbl, DT_REAL)
    rep = odesolverreport_from_net(_net_rep)

    # return
    return (m, xtbl, ytbl, rep)



class sparsematrix(object):
    def __init__(self,ptr):
        self.ptr = ptr


class sparsebuffers(object):
    def __init__(self,ptr):
        self.ptr = ptr
def sparsecreate(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        m, n, k = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        m, n = functionargs
        k = check_equality_and_get([0],"Error while calling 'sparsecreate': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'sparsecreate': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_m = m
    _net_n = n
    _net_k = k
    try:

        # call function
        _net_s = _net_alglib.sparsecreate(_net_m, _net_n, _net_k)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    s = sparsematrix(_net_s)

    # return
    return s

def sparsecreatebuf(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        m, n, k, s = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        m, n, s = functionargs
        k = check_equality_and_get([0],"Error while calling 'sparsecreatebuf': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'sparsecreatebuf': function must have 4 or 3 parameters")

    # convert to .NET types
    _net_m = m
    _net_n = n
    _net_k = k
    _net_s = s.ptr
    try:

        # call function
        _net_alglib.sparsecreatebuf(_net_m, _net_n, _net_k, _net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def sparsecreatecrs(*functionargs):
    # unpack inputs
    m, n, ner = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    _net_ner = net_from_list(ner, DT_INT, "ALGLIB: parameter 'ner' of 'xalglib.sparsecreatecrs' must be int vector")
    try:

        # call function
        _net_s = _net_alglib.sparsecreatecrs(_net_m, _net_n, _net_ner)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    s = sparsematrix(_net_s)

    # return
    return s

def sparsecreatecrsbuf(*functionargs):
    # unpack inputs
    m, n, ner, s = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    _net_ner = net_from_list(ner, DT_INT, "ALGLIB: parameter 'ner' of 'xalglib.sparsecreatecrsbuf' must be int vector")
    _net_s = s.ptr
    try:

        # call function
        _net_alglib.sparsecreatecrsbuf(_net_m, _net_n, _net_ner, _net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def sparsecreatesks(*functionargs):
    # unpack inputs
    m, n, d, u = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    _net_d = net_from_list(d, DT_INT, "ALGLIB: parameter 'd' of 'xalglib.sparsecreatesks' must be int vector")
    _net_u = net_from_list(u, DT_INT, "ALGLIB: parameter 'u' of 'xalglib.sparsecreatesks' must be int vector")
    try:

        # call function
        _net_s = _net_alglib.sparsecreatesks(_net_m, _net_n, _net_d, _net_u)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    s = sparsematrix(_net_s)

    # return
    return s

def sparsecreatesksbuf(*functionargs):
    # unpack inputs
    m, n, d, u, s = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    _net_d = net_from_list(d, DT_INT, "ALGLIB: parameter 'd' of 'xalglib.sparsecreatesksbuf' must be int vector")
    _net_u = net_from_list(u, DT_INT, "ALGLIB: parameter 'u' of 'xalglib.sparsecreatesksbuf' must be int vector")
    _net_s = s.ptr
    try:

        # call function
        _net_alglib.sparsecreatesksbuf(_net_m, _net_n, _net_d, _net_u, _net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def sparsecreatesksband(*functionargs):
    # unpack inputs
    m, n, bw = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    _net_bw = bw
    try:

        # call function
        _net_s = _net_alglib.sparsecreatesksband(_net_m, _net_n, _net_bw)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    s = sparsematrix(_net_s)

    # return
    return s

def sparsecreatesksbandbuf(*functionargs):
    # unpack inputs
    m, n, bw, s = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    _net_bw = bw
    _net_s = s.ptr
    try:

        # call function
        _net_alglib.sparsecreatesksbandbuf(_net_m, _net_n, _net_bw, _net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def sparsecopy(*functionargs):
    # unpack inputs
    s0,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s0 = s0.ptr
    try:

        # call function
        _net_s1 = _net_alglib.sparsecopy(_net_s0)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    s1 = sparsematrix(_net_s1)

    # return
    return s1

def sparsecopybuf(*functionargs):
    # unpack inputs
    s0, s1 = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s0 = s0.ptr
    _net_s1 = s1.ptr
    try:

        # call function
        _net_alglib.sparsecopybuf(_net_s0, _net_s1)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def sparseswap(*functionargs):
    # unpack inputs
    s0, s1 = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s0 = s0.ptr
    _net_s1 = s1.ptr
    try:

        # call function
        _net_alglib.sparseswap(_net_s0, _net_s1)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def sparseadd(*functionargs):
    # unpack inputs
    s, i, j, v = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_i = i
    _net_j = j
    _net_v = v
    try:

        # call function
        _net_alglib.sparseadd(_net_s, _net_i, _net_j, _net_v)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def sparseset(*functionargs):
    # unpack inputs
    s, i, j, v = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_i = i
    _net_j = j
    _net_v = v
    try:

        # call function
        _net_alglib.sparseset(_net_s, _net_i, _net_j, _net_v)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def sparseget(*functionargs):
    # unpack inputs
    s, i, j = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_i = i
    _net_j = j
    try:

        # call function
        _net_result = _net_alglib.sparseget(_net_s, _net_i, _net_j)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def sparsegetdiagonal(*functionargs):
    # unpack inputs
    s, i = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_i = i
    try:

        # call function
        _net_result = _net_alglib.sparsegetdiagonal(_net_s, _net_i)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def sparsemv(*functionargs):
    # unpack inputs
    s, x, y = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.sparsemv' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.sparsemv' must be real vector")
    try:

        # call function
        _net_y = _net_alglib.sparsemv(_net_s, _net_x, _net_y)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    y = list_from_net(_net_y, DT_REAL)

    # return
    return y

def sparsemtv(*functionargs):
    # unpack inputs
    s, x, y = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.sparsemtv' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.sparsemtv' must be real vector")
    try:

        # call function
        _net_y = _net_alglib.sparsemtv(_net_s, _net_x, _net_y)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    y = list_from_net(_net_y, DT_REAL)

    # return
    return y

def sparsemv2(*functionargs):
    # unpack inputs
    s, x, y0, y1 = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.sparsemv2' must be real vector")
    _net_y0 = net_from_list(y0, DT_REAL, "ALGLIB: parameter 'y0' of 'xalglib.sparsemv2' must be real vector")
    _net_y1 = net_from_list(y1, DT_REAL, "ALGLIB: parameter 'y1' of 'xalglib.sparsemv2' must be real vector")
    try:

        # call function
        _net_y0, _net_y1 = _net_alglib.sparsemv2(_net_s, _net_x, _net_y0, _net_y1)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    y0 = list_from_net(_net_y0, DT_REAL)
    y1 = list_from_net(_net_y1, DT_REAL)

    # return
    return (y0, y1)

def sparsesmv(*functionargs):
    # unpack inputs
    s, isupper, x, y = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_isupper = isupper
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.sparsesmv' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.sparsesmv' must be real vector")
    try:

        # call function
        _net_y = _net_alglib.sparsesmv(_net_s, _net_isupper, _net_x, _net_y)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    y = list_from_net(_net_y, DT_REAL)

    # return
    return y

def sparsevsmv(*functionargs):
    # unpack inputs
    s, isupper, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_isupper = isupper
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.sparsevsmv' must be real vector")
    try:

        # call function
        _net_result = _net_alglib.sparsevsmv(_net_s, _net_isupper, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def sparsemm(*functionargs):
    # unpack inputs
    s, a, k, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.sparsemm' must be real matrix")
    _net_k = k
    _net_b = net_from_listlist(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.sparsemm' must be real matrix")
    try:

        # call function
        _net_b = _net_alglib.sparsemm(_net_s, _net_a, _net_k, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = listlist_from_net(_net_b, DT_REAL)

    # return
    return b

def sparsemtm(*functionargs):
    # unpack inputs
    s, a, k, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.sparsemtm' must be real matrix")
    _net_k = k
    _net_b = net_from_listlist(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.sparsemtm' must be real matrix")
    try:

        # call function
        _net_b = _net_alglib.sparsemtm(_net_s, _net_a, _net_k, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = listlist_from_net(_net_b, DT_REAL)

    # return
    return b

def sparsemm2(*functionargs):
    # unpack inputs
    s, a, k, b0, b1 = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.sparsemm2' must be real matrix")
    _net_k = k
    _net_b0 = net_from_listlist(b0, DT_REAL, "ALGLIB: parameter 'b0' of 'xalglib.sparsemm2' must be real matrix")
    _net_b1 = net_from_listlist(b1, DT_REAL, "ALGLIB: parameter 'b1' of 'xalglib.sparsemm2' must be real matrix")
    try:

        # call function
        _net_b0, _net_b1 = _net_alglib.sparsemm2(_net_s, _net_a, _net_k, _net_b0, _net_b1)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b0 = listlist_from_net(_net_b0, DT_REAL)
    b1 = listlist_from_net(_net_b1, DT_REAL)

    # return
    return (b0, b1)

def sparsesmm(*functionargs):
    # unpack inputs
    s, isupper, a, k, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_isupper = isupper
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.sparsesmm' must be real matrix")
    _net_k = k
    _net_b = net_from_listlist(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.sparsesmm' must be real matrix")
    try:

        # call function
        _net_b = _net_alglib.sparsesmm(_net_s, _net_isupper, _net_a, _net_k, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = listlist_from_net(_net_b, DT_REAL)

    # return
    return b

def sparsetrmv(*functionargs):
    # unpack inputs
    s, isupper, isunit, optype, x, y = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_isupper = isupper
    _net_isunit = isunit
    _net_optype = optype
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.sparsetrmv' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.sparsetrmv' must be real vector")
    try:

        # call function
        _net_x, _net_y = _net_alglib.sparsetrmv(_net_s, _net_isupper, _net_isunit, _net_optype, _net_x, _net_y)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = list_from_net(_net_x, DT_REAL)
    y = list_from_net(_net_y, DT_REAL)

    # return
    return (x, y)

def sparsetrsv(*functionargs):
    # unpack inputs
    s, isupper, isunit, optype, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_isupper = isupper
    _net_isunit = isunit
    _net_optype = optype
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.sparsetrsv' must be real vector")
    try:

        # call function
        _net_x = _net_alglib.sparsetrsv(_net_s, _net_isupper, _net_isunit, _net_optype, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = list_from_net(_net_x, DT_REAL)

    # return
    return x

def sparseresizematrix(*functionargs):
    # unpack inputs
    s,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    try:

        # call function
        _net_alglib.sparseresizematrix(_net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def sparseenumerate(*functionargs):
    # unpack inputs
    s, t0, t1 = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_t0 = t0
    _net_t1 = t1
    try:

        # call function
        _net_result, _net_t0, _net_t1, _net_i, _net_j, _net_v = _net_alglib.sparseenumerate(_net_s, _net_t0, _net_t1)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result
    t0 = _net_t0
    t1 = _net_t1
    i = _net_i
    j = _net_j
    v = _net_v

    # return
    return (result, t0, t1, i, j, v)

def sparserewriteexisting(*functionargs):
    # unpack inputs
    s, i, j, v = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_i = i
    _net_j = j
    _net_v = v
    try:

        # call function
        _net_result = _net_alglib.sparserewriteexisting(_net_s, _net_i, _net_j, _net_v)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def sparsegetrow(*functionargs):
    # unpack inputs
    s, i, irow = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_i = i
    _net_irow = net_from_list(irow, DT_REAL, "ALGLIB: parameter 'irow' of 'xalglib.sparsegetrow' must be real vector")
    try:

        # call function
        _net_irow = _net_alglib.sparsegetrow(_net_s, _net_i, _net_irow)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    irow = list_from_net(_net_irow, DT_REAL)

    # return
    return irow

def sparsegetcompressedrow(*functionargs):
    # unpack inputs
    s, i, colidx, vals = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_i = i
    _net_colidx = net_from_list(colidx, DT_INT, "ALGLIB: parameter 'colidx' of 'xalglib.sparsegetcompressedrow' must be int vector")
    _net_vals = net_from_list(vals, DT_REAL, "ALGLIB: parameter 'vals' of 'xalglib.sparsegetcompressedrow' must be real vector")
    try:

        # call function
        _net_colidx, _net_vals, _net_nzcnt = _net_alglib.sparsegetcompressedrow(_net_s, _net_i, _net_colidx, _net_vals)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    colidx = list_from_net(_net_colidx, DT_INT)
    vals = list_from_net(_net_vals, DT_REAL)
    nzcnt = _net_nzcnt

    # return
    return (colidx, vals, nzcnt)

def sparsetransposesks(*functionargs):
    # unpack inputs
    s,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    try:

        # call function
        _net_alglib.sparsetransposesks(_net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def sparseconvertto(*functionargs):
    # unpack inputs
    s0, fmt = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s0 = s0.ptr
    _net_fmt = fmt
    try:

        # call function
        _net_alglib.sparseconvertto(_net_s0, _net_fmt)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def sparsecopytobuf(*functionargs):
    # unpack inputs
    s0, fmt, s1 = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s0 = s0.ptr
    _net_fmt = fmt
    _net_s1 = s1.ptr
    try:

        # call function
        _net_alglib.sparsecopytobuf(_net_s0, _net_fmt, _net_s1)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def sparseconverttohash(*functionargs):
    # unpack inputs
    s,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    try:

        # call function
        _net_alglib.sparseconverttohash(_net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def sparsecopytohash(*functionargs):
    # unpack inputs
    s0,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s0 = s0.ptr
    try:

        # call function
        _net_s1 = _net_alglib.sparsecopytohash(_net_s0)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    s1 = sparsematrix(_net_s1)

    # return
    return s1

def sparsecopytohashbuf(*functionargs):
    # unpack inputs
    s0, s1 = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s0 = s0.ptr
    _net_s1 = s1.ptr
    try:

        # call function
        _net_alglib.sparsecopytohashbuf(_net_s0, _net_s1)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def sparseconverttocrs(*functionargs):
    # unpack inputs
    s,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    try:

        # call function
        _net_alglib.sparseconverttocrs(_net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def sparsecopytocrs(*functionargs):
    # unpack inputs
    s0,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s0 = s0.ptr
    try:

        # call function
        _net_s1 = _net_alglib.sparsecopytocrs(_net_s0)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    s1 = sparsematrix(_net_s1)

    # return
    return s1

def sparsecopytocrsbuf(*functionargs):
    # unpack inputs
    s0, s1 = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s0 = s0.ptr
    _net_s1 = s1.ptr
    try:

        # call function
        _net_alglib.sparsecopytocrsbuf(_net_s0, _net_s1)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def sparseconverttosks(*functionargs):
    # unpack inputs
    s,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    try:

        # call function
        _net_alglib.sparseconverttosks(_net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def sparsecopytosks(*functionargs):
    # unpack inputs
    s0,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s0 = s0.ptr
    try:

        # call function
        _net_s1 = _net_alglib.sparsecopytosks(_net_s0)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    s1 = sparsematrix(_net_s1)

    # return
    return s1

def sparsecopytosksbuf(*functionargs):
    # unpack inputs
    s0, s1 = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s0 = s0.ptr
    _net_s1 = s1.ptr
    try:

        # call function
        _net_alglib.sparsecopytosksbuf(_net_s0, _net_s1)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def sparsegetmatrixtype(*functionargs):
    # unpack inputs
    s,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    try:

        # call function
        _net_result = _net_alglib.sparsegetmatrixtype(_net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def sparseishash(*functionargs):
    # unpack inputs
    s,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    try:

        # call function
        _net_result = _net_alglib.sparseishash(_net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def sparseiscrs(*functionargs):
    # unpack inputs
    s,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    try:

        # call function
        _net_result = _net_alglib.sparseiscrs(_net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def sparseissks(*functionargs):
    # unpack inputs
    s,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    try:

        # call function
        _net_result = _net_alglib.sparseissks(_net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def sparsefree(*functionargs):
    # unpack inputs
    friendly_form = False

    # convert to .NET types
    try:

        # call function
        _net_s = _net_alglib.sparsefree()
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    s = sparsematrix(_net_s)

    # return
    return s

def sparsegetnrows(*functionargs):
    # unpack inputs
    s,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    try:

        # call function
        _net_result = _net_alglib.sparsegetnrows(_net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def sparsegetncols(*functionargs):
    # unpack inputs
    s,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    try:

        # call function
        _net_result = _net_alglib.sparsegetncols(_net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def sparsegetuppercount(*functionargs):
    # unpack inputs
    s,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    try:

        # call function
        _net_result = _net_alglib.sparsegetuppercount(_net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def sparsegetlowercount(*functionargs):
    # unpack inputs
    s,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    try:

        # call function
        _net_result = _net_alglib.sparsegetlowercount(_net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def cmatrixtranspose(*functionargs):
    # unpack inputs
    m, n, a, ia, ja, b, ib, jb = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.cmatrixtranspose' must be complex matrix")
    _net_ia = ia
    _net_ja = ja
    _net_b = net_from_listlist(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.cmatrixtranspose' must be complex matrix")
    _net_ib = ib
    _net_jb = jb
    try:

        # call function
        _net_b = _net_alglib.cmatrixtranspose(_net_m, _net_n, _net_a, _net_ia, _net_ja, _net_b, _net_ib, _net_jb)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = listlist_from_net(_net_b, DT_COMPLEX)

    # return
    return b

def rmatrixtranspose(*functionargs):
    # unpack inputs
    m, n, a, ia, ja, b, ib, jb = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixtranspose' must be real matrix")
    _net_ia = ia
    _net_ja = ja
    _net_b = net_from_listlist(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.rmatrixtranspose' must be real matrix")
    _net_ib = ib
    _net_jb = jb
    try:

        # call function
        _net_b = _net_alglib.rmatrixtranspose(_net_m, _net_n, _net_a, _net_ia, _net_ja, _net_b, _net_ib, _net_jb)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = listlist_from_net(_net_b, DT_REAL)

    # return
    return b

def rmatrixenforcesymmetricity(*functionargs):
    # unpack inputs
    a, n, isupper = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixenforcesymmetricity' must be real matrix")
    _net_n = n
    _net_isupper = isupper
    try:

        # call function
        _net_a = _net_alglib.rmatrixenforcesymmetricity(_net_a, _net_n, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)

    # return
    return a

def cmatrixcopy(*functionargs):
    # unpack inputs
    m, n, a, ia, ja, b, ib, jb = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.cmatrixcopy' must be complex matrix")
    _net_ia = ia
    _net_ja = ja
    _net_b = net_from_listlist(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.cmatrixcopy' must be complex matrix")
    _net_ib = ib
    _net_jb = jb
    try:

        # call function
        _net_b = _net_alglib.cmatrixcopy(_net_m, _net_n, _net_a, _net_ia, _net_ja, _net_b, _net_ib, _net_jb)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = listlist_from_net(_net_b, DT_COMPLEX)

    # return
    return b

def rmatrixcopy(*functionargs):
    # unpack inputs
    m, n, a, ia, ja, b, ib, jb = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixcopy' must be real matrix")
    _net_ia = ia
    _net_ja = ja
    _net_b = net_from_listlist(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.rmatrixcopy' must be real matrix")
    _net_ib = ib
    _net_jb = jb
    try:

        # call function
        _net_b = _net_alglib.rmatrixcopy(_net_m, _net_n, _net_a, _net_ia, _net_ja, _net_b, _net_ib, _net_jb)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = listlist_from_net(_net_b, DT_REAL)

    # return
    return b

def rmatrixger(*functionargs):
    # unpack inputs
    m, n, a, ia, ja, alpha, u, iu, v, iv = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixger' must be real matrix")
    _net_ia = ia
    _net_ja = ja
    _net_alpha = alpha
    _net_u = net_from_list(u, DT_REAL, "ALGLIB: parameter 'u' of 'xalglib.rmatrixger' must be real vector")
    _net_iu = iu
    _net_v = net_from_list(v, DT_REAL, "ALGLIB: parameter 'v' of 'xalglib.rmatrixger' must be real vector")
    _net_iv = iv
    try:

        # call function
        _net_a = _net_alglib.rmatrixger(_net_m, _net_n, _net_a, _net_ia, _net_ja, _net_alpha, _net_u, _net_iu, _net_v, _net_iv)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)

    # return
    return a

def cmatrixrank1(*functionargs):
    # unpack inputs
    m, n, a, ia, ja, u, iu, v, iv = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.cmatrixrank1' must be complex matrix")
    _net_ia = ia
    _net_ja = ja
    _net_u = net_from_list(u, DT_COMPLEX, "ALGLIB: parameter 'u' of 'xalglib.cmatrixrank1' must be complex vector")
    _net_iu = iu
    _net_v = net_from_list(v, DT_COMPLEX, "ALGLIB: parameter 'v' of 'xalglib.cmatrixrank1' must be complex vector")
    _net_iv = iv
    try:

        # call function
        _net_a, _net_u, _net_v = _net_alglib.cmatrixrank1(_net_m, _net_n, _net_a, _net_ia, _net_ja, _net_u, _net_iu, _net_v, _net_iv)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_COMPLEX)
    u = list_from_net(_net_u, DT_COMPLEX)
    v = list_from_net(_net_v, DT_COMPLEX)

    # return
    return (a, u, v)

def rmatrixrank1(*functionargs):
    # unpack inputs
    m, n, a, ia, ja, u, iu, v, iv = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixrank1' must be real matrix")
    _net_ia = ia
    _net_ja = ja
    _net_u = net_from_list(u, DT_REAL, "ALGLIB: parameter 'u' of 'xalglib.rmatrixrank1' must be real vector")
    _net_iu = iu
    _net_v = net_from_list(v, DT_REAL, "ALGLIB: parameter 'v' of 'xalglib.rmatrixrank1' must be real vector")
    _net_iv = iv
    try:

        # call function
        _net_a, _net_u, _net_v = _net_alglib.rmatrixrank1(_net_m, _net_n, _net_a, _net_ia, _net_ja, _net_u, _net_iu, _net_v, _net_iv)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)
    u = list_from_net(_net_u, DT_REAL)
    v = list_from_net(_net_v, DT_REAL)

    # return
    return (a, u, v)

def rmatrixgemv(*functionargs):
    # unpack inputs
    m, n, alpha, a, ia, ja, opa, x, ix, beta, y, iy = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    _net_alpha = alpha
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixgemv' must be real matrix")
    _net_ia = ia
    _net_ja = ja
    _net_opa = opa
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.rmatrixgemv' must be real vector")
    _net_ix = ix
    _net_beta = beta
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.rmatrixgemv' must be real vector")
    _net_iy = iy
    try:

        # call function
        _net_y = _net_alglib.rmatrixgemv(_net_m, _net_n, _net_alpha, _net_a, _net_ia, _net_ja, _net_opa, _net_x, _net_ix, _net_beta, _net_y, _net_iy)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    y = list_from_net(_net_y, DT_REAL)

    # return
    return y

def cmatrixmv(*functionargs):
    # unpack inputs
    m, n, a, ia, ja, opa, x, ix, y, iy = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.cmatrixmv' must be complex matrix")
    _net_ia = ia
    _net_ja = ja
    _net_opa = opa
    _net_x = net_from_list(x, DT_COMPLEX, "ALGLIB: parameter 'x' of 'xalglib.cmatrixmv' must be complex vector")
    _net_ix = ix
    _net_y = net_from_list(y, DT_COMPLEX, "ALGLIB: parameter 'y' of 'xalglib.cmatrixmv' must be complex vector")
    _net_iy = iy
    try:

        # call function
        _net_y = _net_alglib.cmatrixmv(_net_m, _net_n, _net_a, _net_ia, _net_ja, _net_opa, _net_x, _net_ix, _net_y, _net_iy)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    y = list_from_net(_net_y, DT_COMPLEX)

    # return
    return y

def rmatrixmv(*functionargs):
    # unpack inputs
    m, n, a, ia, ja, opa, x, ix, y, iy = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixmv' must be real matrix")
    _net_ia = ia
    _net_ja = ja
    _net_opa = opa
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.rmatrixmv' must be real vector")
    _net_ix = ix
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.rmatrixmv' must be real vector")
    _net_iy = iy
    try:

        # call function
        _net_y = _net_alglib.rmatrixmv(_net_m, _net_n, _net_a, _net_ia, _net_ja, _net_opa, _net_x, _net_ix, _net_y, _net_iy)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    y = list_from_net(_net_y, DT_REAL)

    # return
    return y

def rmatrixsymv(*functionargs):
    # unpack inputs
    n, alpha, a, ia, ja, isupper, x, ix, beta, y, iy = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    _net_alpha = alpha
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixsymv' must be real matrix")
    _net_ia = ia
    _net_ja = ja
    _net_isupper = isupper
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.rmatrixsymv' must be real vector")
    _net_ix = ix
    _net_beta = beta
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.rmatrixsymv' must be real vector")
    _net_iy = iy
    try:

        # call function
        _net_y = _net_alglib.rmatrixsymv(_net_n, _net_alpha, _net_a, _net_ia, _net_ja, _net_isupper, _net_x, _net_ix, _net_beta, _net_y, _net_iy)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    y = list_from_net(_net_y, DT_REAL)

    # return
    return y

def rmatrixsyvmv(*functionargs):
    # unpack inputs
    n, a, ia, ja, isupper, x, ix, tmp = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixsyvmv' must be real matrix")
    _net_ia = ia
    _net_ja = ja
    _net_isupper = isupper
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.rmatrixsyvmv' must be real vector")
    _net_ix = ix
    _net_tmp = net_from_list(tmp, DT_REAL, "ALGLIB: parameter 'tmp' of 'xalglib.rmatrixsyvmv' must be real vector")
    try:

        # call function
        _net_result, _net_tmp = _net_alglib.rmatrixsyvmv(_net_n, _net_a, _net_ia, _net_ja, _net_isupper, _net_x, _net_ix, _net_tmp)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result
    tmp = list_from_net(_net_tmp, DT_REAL)

    # return
    return (result, tmp)

def rmatrixtrsv(*functionargs):
    # unpack inputs
    n, a, ia, ja, isupper, isunit, optype, x, ix = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixtrsv' must be real matrix")
    _net_ia = ia
    _net_ja = ja
    _net_isupper = isupper
    _net_isunit = isunit
    _net_optype = optype
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.rmatrixtrsv' must be real vector")
    _net_ix = ix
    try:

        # call function
        _net_x = _net_alglib.rmatrixtrsv(_net_n, _net_a, _net_ia, _net_ja, _net_isupper, _net_isunit, _net_optype, _net_x, _net_ix)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = list_from_net(_net_x, DT_REAL)

    # return
    return x

def cmatrixrighttrsm(*functionargs):
    # unpack inputs
    m, n, a, i1, j1, isupper, isunit, optype, x, i2, j2 = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.cmatrixrighttrsm' must be complex matrix")
    _net_i1 = i1
    _net_j1 = j1
    _net_isupper = isupper
    _net_isunit = isunit
    _net_optype = optype
    _net_x = net_from_listlist(x, DT_COMPLEX, "ALGLIB: parameter 'x' of 'xalglib.cmatrixrighttrsm' must be complex matrix")
    _net_i2 = i2
    _net_j2 = j2
    try:

        # call function
        _net_x = _net_alglib.cmatrixrighttrsm(_net_m, _net_n, _net_a, _net_i1, _net_j1, _net_isupper, _net_isunit, _net_optype, _net_x, _net_i2, _net_j2)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = listlist_from_net(_net_x, DT_COMPLEX)

    # return
    return x

def smp_cmatrixrighttrsm(*functionargs):
    # unpack inputs
    m, n, a, i1, j1, isupper, isunit, optype, x, i2, j2 = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.smp_cmatrixrighttrsm' must be complex matrix")
    _net_i1 = i1
    _net_j1 = j1
    _net_isupper = isupper
    _net_isunit = isunit
    _net_optype = optype
    _net_x = net_from_listlist(x, DT_COMPLEX, "ALGLIB: parameter 'x' of 'xalglib.smp_cmatrixrighttrsm' must be complex matrix")
    _net_i2 = i2
    _net_j2 = j2
    try:

        # call function
        _net_x = _net_alglib.smp_cmatrixrighttrsm(_net_m, _net_n, _net_a, _net_i1, _net_j1, _net_isupper, _net_isunit, _net_optype, _net_x, _net_i2, _net_j2)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = listlist_from_net(_net_x, DT_COMPLEX)

    # return
    return x

def cmatrixlefttrsm(*functionargs):
    # unpack inputs
    m, n, a, i1, j1, isupper, isunit, optype, x, i2, j2 = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.cmatrixlefttrsm' must be complex matrix")
    _net_i1 = i1
    _net_j1 = j1
    _net_isupper = isupper
    _net_isunit = isunit
    _net_optype = optype
    _net_x = net_from_listlist(x, DT_COMPLEX, "ALGLIB: parameter 'x' of 'xalglib.cmatrixlefttrsm' must be complex matrix")
    _net_i2 = i2
    _net_j2 = j2
    try:

        # call function
        _net_x = _net_alglib.cmatrixlefttrsm(_net_m, _net_n, _net_a, _net_i1, _net_j1, _net_isupper, _net_isunit, _net_optype, _net_x, _net_i2, _net_j2)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = listlist_from_net(_net_x, DT_COMPLEX)

    # return
    return x

def smp_cmatrixlefttrsm(*functionargs):
    # unpack inputs
    m, n, a, i1, j1, isupper, isunit, optype, x, i2, j2 = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.smp_cmatrixlefttrsm' must be complex matrix")
    _net_i1 = i1
    _net_j1 = j1
    _net_isupper = isupper
    _net_isunit = isunit
    _net_optype = optype
    _net_x = net_from_listlist(x, DT_COMPLEX, "ALGLIB: parameter 'x' of 'xalglib.smp_cmatrixlefttrsm' must be complex matrix")
    _net_i2 = i2
    _net_j2 = j2
    try:

        # call function
        _net_x = _net_alglib.smp_cmatrixlefttrsm(_net_m, _net_n, _net_a, _net_i1, _net_j1, _net_isupper, _net_isunit, _net_optype, _net_x, _net_i2, _net_j2)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = listlist_from_net(_net_x, DT_COMPLEX)

    # return
    return x

def rmatrixrighttrsm(*functionargs):
    # unpack inputs
    m, n, a, i1, j1, isupper, isunit, optype, x, i2, j2 = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixrighttrsm' must be real matrix")
    _net_i1 = i1
    _net_j1 = j1
    _net_isupper = isupper
    _net_isunit = isunit
    _net_optype = optype
    _net_x = net_from_listlist(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.rmatrixrighttrsm' must be real matrix")
    _net_i2 = i2
    _net_j2 = j2
    try:

        # call function
        _net_x = _net_alglib.rmatrixrighttrsm(_net_m, _net_n, _net_a, _net_i1, _net_j1, _net_isupper, _net_isunit, _net_optype, _net_x, _net_i2, _net_j2)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = listlist_from_net(_net_x, DT_REAL)

    # return
    return x

def smp_rmatrixrighttrsm(*functionargs):
    # unpack inputs
    m, n, a, i1, j1, isupper, isunit, optype, x, i2, j2 = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smp_rmatrixrighttrsm' must be real matrix")
    _net_i1 = i1
    _net_j1 = j1
    _net_isupper = isupper
    _net_isunit = isunit
    _net_optype = optype
    _net_x = net_from_listlist(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.smp_rmatrixrighttrsm' must be real matrix")
    _net_i2 = i2
    _net_j2 = j2
    try:

        # call function
        _net_x = _net_alglib.smp_rmatrixrighttrsm(_net_m, _net_n, _net_a, _net_i1, _net_j1, _net_isupper, _net_isunit, _net_optype, _net_x, _net_i2, _net_j2)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = listlist_from_net(_net_x, DT_REAL)

    # return
    return x

def rmatrixlefttrsm(*functionargs):
    # unpack inputs
    m, n, a, i1, j1, isupper, isunit, optype, x, i2, j2 = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixlefttrsm' must be real matrix")
    _net_i1 = i1
    _net_j1 = j1
    _net_isupper = isupper
    _net_isunit = isunit
    _net_optype = optype
    _net_x = net_from_listlist(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.rmatrixlefttrsm' must be real matrix")
    _net_i2 = i2
    _net_j2 = j2
    try:

        # call function
        _net_x = _net_alglib.rmatrixlefttrsm(_net_m, _net_n, _net_a, _net_i1, _net_j1, _net_isupper, _net_isunit, _net_optype, _net_x, _net_i2, _net_j2)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = listlist_from_net(_net_x, DT_REAL)

    # return
    return x

def smp_rmatrixlefttrsm(*functionargs):
    # unpack inputs
    m, n, a, i1, j1, isupper, isunit, optype, x, i2, j2 = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smp_rmatrixlefttrsm' must be real matrix")
    _net_i1 = i1
    _net_j1 = j1
    _net_isupper = isupper
    _net_isunit = isunit
    _net_optype = optype
    _net_x = net_from_listlist(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.smp_rmatrixlefttrsm' must be real matrix")
    _net_i2 = i2
    _net_j2 = j2
    try:

        # call function
        _net_x = _net_alglib.smp_rmatrixlefttrsm(_net_m, _net_n, _net_a, _net_i1, _net_j1, _net_isupper, _net_isunit, _net_optype, _net_x, _net_i2, _net_j2)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = listlist_from_net(_net_x, DT_REAL)

    # return
    return x

def cmatrixherk(*functionargs):
    # unpack inputs
    n, k, alpha, a, ia, ja, optypea, beta, c, ic, jc, isupper = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    _net_k = k
    _net_alpha = alpha
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.cmatrixherk' must be complex matrix")
    _net_ia = ia
    _net_ja = ja
    _net_optypea = optypea
    _net_beta = beta
    _net_c = net_from_listlist(c, DT_COMPLEX, "ALGLIB: parameter 'c' of 'xalglib.cmatrixherk' must be complex matrix")
    _net_ic = ic
    _net_jc = jc
    _net_isupper = isupper
    try:

        # call function
        _net_c = _net_alglib.cmatrixherk(_net_n, _net_k, _net_alpha, _net_a, _net_ia, _net_ja, _net_optypea, _net_beta, _net_c, _net_ic, _net_jc, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = listlist_from_net(_net_c, DT_COMPLEX)

    # return
    return c

def smp_cmatrixherk(*functionargs):
    # unpack inputs
    n, k, alpha, a, ia, ja, optypea, beta, c, ic, jc, isupper = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    _net_k = k
    _net_alpha = alpha
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.smp_cmatrixherk' must be complex matrix")
    _net_ia = ia
    _net_ja = ja
    _net_optypea = optypea
    _net_beta = beta
    _net_c = net_from_listlist(c, DT_COMPLEX, "ALGLIB: parameter 'c' of 'xalglib.smp_cmatrixherk' must be complex matrix")
    _net_ic = ic
    _net_jc = jc
    _net_isupper = isupper
    try:

        # call function
        _net_c = _net_alglib.smp_cmatrixherk(_net_n, _net_k, _net_alpha, _net_a, _net_ia, _net_ja, _net_optypea, _net_beta, _net_c, _net_ic, _net_jc, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = listlist_from_net(_net_c, DT_COMPLEX)

    # return
    return c

def rmatrixsyrk(*functionargs):
    # unpack inputs
    n, k, alpha, a, ia, ja, optypea, beta, c, ic, jc, isupper = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    _net_k = k
    _net_alpha = alpha
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixsyrk' must be real matrix")
    _net_ia = ia
    _net_ja = ja
    _net_optypea = optypea
    _net_beta = beta
    _net_c = net_from_listlist(c, DT_REAL, "ALGLIB: parameter 'c' of 'xalglib.rmatrixsyrk' must be real matrix")
    _net_ic = ic
    _net_jc = jc
    _net_isupper = isupper
    try:

        # call function
        _net_c = _net_alglib.rmatrixsyrk(_net_n, _net_k, _net_alpha, _net_a, _net_ia, _net_ja, _net_optypea, _net_beta, _net_c, _net_ic, _net_jc, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = listlist_from_net(_net_c, DT_REAL)

    # return
    return c

def smp_rmatrixsyrk(*functionargs):
    # unpack inputs
    n, k, alpha, a, ia, ja, optypea, beta, c, ic, jc, isupper = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    _net_k = k
    _net_alpha = alpha
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smp_rmatrixsyrk' must be real matrix")
    _net_ia = ia
    _net_ja = ja
    _net_optypea = optypea
    _net_beta = beta
    _net_c = net_from_listlist(c, DT_REAL, "ALGLIB: parameter 'c' of 'xalglib.smp_rmatrixsyrk' must be real matrix")
    _net_ic = ic
    _net_jc = jc
    _net_isupper = isupper
    try:

        # call function
        _net_c = _net_alglib.smp_rmatrixsyrk(_net_n, _net_k, _net_alpha, _net_a, _net_ia, _net_ja, _net_optypea, _net_beta, _net_c, _net_ic, _net_jc, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = listlist_from_net(_net_c, DT_REAL)

    # return
    return c

def cmatrixgemm(*functionargs):
    # unpack inputs
    m, n, k, alpha, a, ia, ja, optypea, b, ib, jb, optypeb, beta, c, ic, jc = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    _net_k = k
    _cplx_alpha = complex(alpha)
    _net_alpha = _net_alglib.complex(_cplx_alpha.real,_cplx_alpha.imag)
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.cmatrixgemm' must be complex matrix")
    _net_ia = ia
    _net_ja = ja
    _net_optypea = optypea
    _net_b = net_from_listlist(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.cmatrixgemm' must be complex matrix")
    _net_ib = ib
    _net_jb = jb
    _net_optypeb = optypeb
    _cplx_beta = complex(beta)
    _net_beta = _net_alglib.complex(_cplx_beta.real,_cplx_beta.imag)
    _net_c = net_from_listlist(c, DT_COMPLEX, "ALGLIB: parameter 'c' of 'xalglib.cmatrixgemm' must be complex matrix")
    _net_ic = ic
    _net_jc = jc
    try:

        # call function
        _net_c = _net_alglib.cmatrixgemm(_net_m, _net_n, _net_k, _net_alpha, _net_a, _net_ia, _net_ja, _net_optypea, _net_b, _net_ib, _net_jb, _net_optypeb, _net_beta, _net_c, _net_ic, _net_jc)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = listlist_from_net(_net_c, DT_COMPLEX)

    # return
    return c

def smp_cmatrixgemm(*functionargs):
    # unpack inputs
    m, n, k, alpha, a, ia, ja, optypea, b, ib, jb, optypeb, beta, c, ic, jc = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    _net_k = k
    _cplx_alpha = complex(alpha)
    _net_alpha = _net_alglib.complex(_cplx_alpha.real,_cplx_alpha.imag)
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.smp_cmatrixgemm' must be complex matrix")
    _net_ia = ia
    _net_ja = ja
    _net_optypea = optypea
    _net_b = net_from_listlist(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.smp_cmatrixgemm' must be complex matrix")
    _net_ib = ib
    _net_jb = jb
    _net_optypeb = optypeb
    _cplx_beta = complex(beta)
    _net_beta = _net_alglib.complex(_cplx_beta.real,_cplx_beta.imag)
    _net_c = net_from_listlist(c, DT_COMPLEX, "ALGLIB: parameter 'c' of 'xalglib.smp_cmatrixgemm' must be complex matrix")
    _net_ic = ic
    _net_jc = jc
    try:

        # call function
        _net_c = _net_alglib.smp_cmatrixgemm(_net_m, _net_n, _net_k, _net_alpha, _net_a, _net_ia, _net_ja, _net_optypea, _net_b, _net_ib, _net_jb, _net_optypeb, _net_beta, _net_c, _net_ic, _net_jc)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = listlist_from_net(_net_c, DT_COMPLEX)

    # return
    return c

def rmatrixgemm(*functionargs):
    # unpack inputs
    m, n, k, alpha, a, ia, ja, optypea, b, ib, jb, optypeb, beta, c, ic, jc = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    _net_k = k
    _net_alpha = alpha
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixgemm' must be real matrix")
    _net_ia = ia
    _net_ja = ja
    _net_optypea = optypea
    _net_b = net_from_listlist(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.rmatrixgemm' must be real matrix")
    _net_ib = ib
    _net_jb = jb
    _net_optypeb = optypeb
    _net_beta = beta
    _net_c = net_from_listlist(c, DT_REAL, "ALGLIB: parameter 'c' of 'xalglib.rmatrixgemm' must be real matrix")
    _net_ic = ic
    _net_jc = jc
    try:

        # call function
        _net_c = _net_alglib.rmatrixgemm(_net_m, _net_n, _net_k, _net_alpha, _net_a, _net_ia, _net_ja, _net_optypea, _net_b, _net_ib, _net_jb, _net_optypeb, _net_beta, _net_c, _net_ic, _net_jc)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = listlist_from_net(_net_c, DT_REAL)

    # return
    return c

def smp_rmatrixgemm(*functionargs):
    # unpack inputs
    m, n, k, alpha, a, ia, ja, optypea, b, ib, jb, optypeb, beta, c, ic, jc = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    _net_k = k
    _net_alpha = alpha
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smp_rmatrixgemm' must be real matrix")
    _net_ia = ia
    _net_ja = ja
    _net_optypea = optypea
    _net_b = net_from_listlist(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.smp_rmatrixgemm' must be real matrix")
    _net_ib = ib
    _net_jb = jb
    _net_optypeb = optypeb
    _net_beta = beta
    _net_c = net_from_listlist(c, DT_REAL, "ALGLIB: parameter 'c' of 'xalglib.smp_rmatrixgemm' must be real matrix")
    _net_ic = ic
    _net_jc = jc
    try:

        # call function
        _net_c = _net_alglib.smp_rmatrixgemm(_net_m, _net_n, _net_k, _net_alpha, _net_a, _net_ia, _net_ja, _net_optypea, _net_b, _net_ib, _net_jb, _net_optypeb, _net_beta, _net_c, _net_ic, _net_jc)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = listlist_from_net(_net_c, DT_REAL)

    # return
    return c

def cmatrixsyrk(*functionargs):
    # unpack inputs
    n, k, alpha, a, ia, ja, optypea, beta, c, ic, jc, isupper = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    _net_k = k
    _net_alpha = alpha
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.cmatrixsyrk' must be complex matrix")
    _net_ia = ia
    _net_ja = ja
    _net_optypea = optypea
    _net_beta = beta
    _net_c = net_from_listlist(c, DT_COMPLEX, "ALGLIB: parameter 'c' of 'xalglib.cmatrixsyrk' must be complex matrix")
    _net_ic = ic
    _net_jc = jc
    _net_isupper = isupper
    try:

        # call function
        _net_c = _net_alglib.cmatrixsyrk(_net_n, _net_k, _net_alpha, _net_a, _net_ia, _net_ja, _net_optypea, _net_beta, _net_c, _net_ic, _net_jc, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = listlist_from_net(_net_c, DT_COMPLEX)

    # return
    return c

def smp_cmatrixsyrk(*functionargs):
    # unpack inputs
    n, k, alpha, a, ia, ja, optypea, beta, c, ic, jc, isupper = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    _net_k = k
    _net_alpha = alpha
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.smp_cmatrixsyrk' must be complex matrix")
    _net_ia = ia
    _net_ja = ja
    _net_optypea = optypea
    _net_beta = beta
    _net_c = net_from_listlist(c, DT_COMPLEX, "ALGLIB: parameter 'c' of 'xalglib.smp_cmatrixsyrk' must be complex matrix")
    _net_ic = ic
    _net_jc = jc
    _net_isupper = isupper
    try:

        # call function
        _net_c = _net_alglib.smp_cmatrixsyrk(_net_n, _net_k, _net_alpha, _net_a, _net_ia, _net_ja, _net_optypea, _net_beta, _net_c, _net_ic, _net_jc, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = listlist_from_net(_net_c, DT_COMPLEX)

    # return
    return c

def rmatrixrndorthogonal(*functionargs):
    # unpack inputs
    n,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    try:

        # call function
        _net_a = _net_alglib.rmatrixrndorthogonal(_net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)

    # return
    return a

def rmatrixrndcond(*functionargs):
    # unpack inputs
    n, c = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    _net_c = c
    try:

        # call function
        _net_a = _net_alglib.rmatrixrndcond(_net_n, _net_c)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)

    # return
    return a

def cmatrixrndorthogonal(*functionargs):
    # unpack inputs
    n,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    try:

        # call function
        _net_a = _net_alglib.cmatrixrndorthogonal(_net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_COMPLEX)

    # return
    return a

def cmatrixrndcond(*functionargs):
    # unpack inputs
    n, c = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    _net_c = c
    try:

        # call function
        _net_a = _net_alglib.cmatrixrndcond(_net_n, _net_c)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_COMPLEX)

    # return
    return a

def smatrixrndcond(*functionargs):
    # unpack inputs
    n, c = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    _net_c = c
    try:

        # call function
        _net_a = _net_alglib.smatrixrndcond(_net_n, _net_c)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)

    # return
    return a

def spdmatrixrndcond(*functionargs):
    # unpack inputs
    n, c = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    _net_c = c
    try:

        # call function
        _net_a = _net_alglib.spdmatrixrndcond(_net_n, _net_c)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)

    # return
    return a

def hmatrixrndcond(*functionargs):
    # unpack inputs
    n, c = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    _net_c = c
    try:

        # call function
        _net_a = _net_alglib.hmatrixrndcond(_net_n, _net_c)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_COMPLEX)

    # return
    return a

def hpdmatrixrndcond(*functionargs):
    # unpack inputs
    n, c = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    _net_c = c
    try:

        # call function
        _net_a = _net_alglib.hpdmatrixrndcond(_net_n, _net_c)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_COMPLEX)

    # return
    return a

def rmatrixrndorthogonalfromtheright(*functionargs):
    # unpack inputs
    a, m, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixrndorthogonalfromtheright' must be real matrix")
    _net_m = m
    _net_n = n
    try:

        # call function
        _net_a = _net_alglib.rmatrixrndorthogonalfromtheright(_net_a, _net_m, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)

    # return
    return a

def rmatrixrndorthogonalfromtheleft(*functionargs):
    # unpack inputs
    a, m, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixrndorthogonalfromtheleft' must be real matrix")
    _net_m = m
    _net_n = n
    try:

        # call function
        _net_a = _net_alglib.rmatrixrndorthogonalfromtheleft(_net_a, _net_m, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)

    # return
    return a

def cmatrixrndorthogonalfromtheright(*functionargs):
    # unpack inputs
    a, m, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.cmatrixrndorthogonalfromtheright' must be complex matrix")
    _net_m = m
    _net_n = n
    try:

        # call function
        _net_a = _net_alglib.cmatrixrndorthogonalfromtheright(_net_a, _net_m, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_COMPLEX)

    # return
    return a

def cmatrixrndorthogonalfromtheleft(*functionargs):
    # unpack inputs
    a, m, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.cmatrixrndorthogonalfromtheleft' must be complex matrix")
    _net_m = m
    _net_n = n
    try:

        # call function
        _net_a = _net_alglib.cmatrixrndorthogonalfromtheleft(_net_a, _net_m, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_COMPLEX)

    # return
    return a

def smatrixrndmultiply(*functionargs):
    # unpack inputs
    a, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smatrixrndmultiply' must be real matrix")
    _net_n = n
    try:

        # call function
        _net_a = _net_alglib.smatrixrndmultiply(_net_a, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)

    # return
    return a

def hmatrixrndmultiply(*functionargs):
    # unpack inputs
    a, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.hmatrixrndmultiply' must be complex matrix")
    _net_n = n
    try:

        # call function
        _net_a = _net_alglib.hmatrixrndmultiply(_net_a, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_COMPLEX)

    # return
    return a

def rmatrixlu(*functionargs):
    # unpack inputs
    a, m, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixlu' must be real matrix")
    _net_m = m
    _net_n = n
    try:

        # call function
        _net_a, _net_pivots = _net_alglib.rmatrixlu(_net_a, _net_m, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)
    pivots = list_from_net(_net_pivots, DT_INT)

    # return
    return (a, pivots)

def smp_rmatrixlu(*functionargs):
    # unpack inputs
    a, m, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smp_rmatrixlu' must be real matrix")
    _net_m = m
    _net_n = n
    try:

        # call function
        _net_a, _net_pivots = _net_alglib.smp_rmatrixlu(_net_a, _net_m, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)
    pivots = list_from_net(_net_pivots, DT_INT)

    # return
    return (a, pivots)

def cmatrixlu(*functionargs):
    # unpack inputs
    a, m, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.cmatrixlu' must be complex matrix")
    _net_m = m
    _net_n = n
    try:

        # call function
        _net_a, _net_pivots = _net_alglib.cmatrixlu(_net_a, _net_m, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_COMPLEX)
    pivots = list_from_net(_net_pivots, DT_INT)

    # return
    return (a, pivots)

def smp_cmatrixlu(*functionargs):
    # unpack inputs
    a, m, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.smp_cmatrixlu' must be complex matrix")
    _net_m = m
    _net_n = n
    try:

        # call function
        _net_a, _net_pivots = _net_alglib.smp_cmatrixlu(_net_a, _net_m, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_COMPLEX)
    pivots = list_from_net(_net_pivots, DT_INT)

    # return
    return (a, pivots)

def hpdmatrixcholesky(*functionargs):
    # unpack inputs
    a, n, isupper = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.hpdmatrixcholesky' must be complex matrix")
    _net_n = n
    _net_isupper = isupper
    try:

        # call function
        _net_result, _net_a = _net_alglib.hpdmatrixcholesky(_net_a, _net_n, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result
    a = listlist_from_net(_net_a, DT_COMPLEX)

    # return
    return (result, a)

def smp_hpdmatrixcholesky(*functionargs):
    # unpack inputs
    a, n, isupper = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.smp_hpdmatrixcholesky' must be complex matrix")
    _net_n = n
    _net_isupper = isupper
    try:

        # call function
        _net_result, _net_a = _net_alglib.smp_hpdmatrixcholesky(_net_a, _net_n, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result
    a = listlist_from_net(_net_a, DT_COMPLEX)

    # return
    return (result, a)

def spdmatrixcholesky(*functionargs):
    # unpack inputs
    a, n, isupper = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.spdmatrixcholesky' must be real matrix")
    _net_n = n
    _net_isupper = isupper
    try:

        # call function
        _net_result, _net_a = _net_alglib.spdmatrixcholesky(_net_a, _net_n, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result
    a = listlist_from_net(_net_a, DT_REAL)

    # return
    return (result, a)

def smp_spdmatrixcholesky(*functionargs):
    # unpack inputs
    a, n, isupper = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smp_spdmatrixcholesky' must be real matrix")
    _net_n = n
    _net_isupper = isupper
    try:

        # call function
        _net_result, _net_a = _net_alglib.smp_spdmatrixcholesky(_net_a, _net_n, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result
    a = listlist_from_net(_net_a, DT_REAL)

    # return
    return (result, a)

def spdmatrixcholeskyupdateadd1(*functionargs):
    # unpack inputs
    a, n, isupper, u = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.spdmatrixcholeskyupdateadd1' must be real matrix")
    _net_n = n
    _net_isupper = isupper
    _net_u = net_from_list(u, DT_REAL, "ALGLIB: parameter 'u' of 'xalglib.spdmatrixcholeskyupdateadd1' must be real vector")
    try:

        # call function
        _net_a = _net_alglib.spdmatrixcholeskyupdateadd1(_net_a, _net_n, _net_isupper, _net_u)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)

    # return
    return a

def spdmatrixcholeskyupdatefix(*functionargs):
    # unpack inputs
    a, n, isupper, fix = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.spdmatrixcholeskyupdatefix' must be real matrix")
    _net_n = n
    _net_isupper = isupper
    _net_fix = net_from_list(fix, DT_BOOL, "ALGLIB: parameter 'fix' of 'xalglib.spdmatrixcholeskyupdatefix' must be bool vector")
    try:

        # call function
        _net_a = _net_alglib.spdmatrixcholeskyupdatefix(_net_a, _net_n, _net_isupper, _net_fix)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)

    # return
    return a

def spdmatrixcholeskyupdateadd1buf(*functionargs):
    # unpack inputs
    a, n, isupper, u, bufr = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.spdmatrixcholeskyupdateadd1buf' must be real matrix")
    _net_n = n
    _net_isupper = isupper
    _net_u = net_from_list(u, DT_REAL, "ALGLIB: parameter 'u' of 'xalglib.spdmatrixcholeskyupdateadd1buf' must be real vector")
    _net_bufr = net_from_list(bufr, DT_REAL, "ALGLIB: parameter 'bufr' of 'xalglib.spdmatrixcholeskyupdateadd1buf' must be real vector")
    try:

        # call function
        _net_a, _net_bufr = _net_alglib.spdmatrixcholeskyupdateadd1buf(_net_a, _net_n, _net_isupper, _net_u, _net_bufr)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)
    bufr = list_from_net(_net_bufr, DT_REAL)

    # return
    return (a, bufr)

def spdmatrixcholeskyupdatefixbuf(*functionargs):
    # unpack inputs
    a, n, isupper, fix, bufr = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.spdmatrixcholeskyupdatefixbuf' must be real matrix")
    _net_n = n
    _net_isupper = isupper
    _net_fix = net_from_list(fix, DT_BOOL, "ALGLIB: parameter 'fix' of 'xalglib.spdmatrixcholeskyupdatefixbuf' must be bool vector")
    _net_bufr = net_from_list(bufr, DT_REAL, "ALGLIB: parameter 'bufr' of 'xalglib.spdmatrixcholeskyupdatefixbuf' must be real vector")
    try:

        # call function
        _net_a, _net_bufr = _net_alglib.spdmatrixcholeskyupdatefixbuf(_net_a, _net_n, _net_isupper, _net_fix, _net_bufr)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)
    bufr = list_from_net(_net_bufr, DT_REAL)

    # return
    return (a, bufr)

def sparsecholeskyskyline(*functionargs):
    # unpack inputs
    a, n, isupper = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = a.ptr
    _net_n = n
    _net_isupper = isupper
    try:

        # call function
        _net_result = _net_alglib.sparsecholeskyskyline(_net_a, _net_n, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def rmatrixrcond1(*functionargs):
    # unpack inputs
    a, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixrcond1' must be real matrix")
    _net_n = n
    try:

        # call function
        _net_result = _net_alglib.rmatrixrcond1(_net_a, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def rmatrixrcondinf(*functionargs):
    # unpack inputs
    a, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixrcondinf' must be real matrix")
    _net_n = n
    try:

        # call function
        _net_result = _net_alglib.rmatrixrcondinf(_net_a, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def spdmatrixrcond(*functionargs):
    # unpack inputs
    a, n, isupper = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.spdmatrixrcond' must be real matrix")
    _net_n = n
    _net_isupper = isupper
    try:

        # call function
        _net_result = _net_alglib.spdmatrixrcond(_net_a, _net_n, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def rmatrixtrrcond1(*functionargs):
    # unpack inputs
    a, n, isupper, isunit = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixtrrcond1' must be real matrix")
    _net_n = n
    _net_isupper = isupper
    _net_isunit = isunit
    try:

        # call function
        _net_result = _net_alglib.rmatrixtrrcond1(_net_a, _net_n, _net_isupper, _net_isunit)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def rmatrixtrrcondinf(*functionargs):
    # unpack inputs
    a, n, isupper, isunit = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixtrrcondinf' must be real matrix")
    _net_n = n
    _net_isupper = isupper
    _net_isunit = isunit
    try:

        # call function
        _net_result = _net_alglib.rmatrixtrrcondinf(_net_a, _net_n, _net_isupper, _net_isunit)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def hpdmatrixrcond(*functionargs):
    # unpack inputs
    a, n, isupper = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.hpdmatrixrcond' must be complex matrix")
    _net_n = n
    _net_isupper = isupper
    try:

        # call function
        _net_result = _net_alglib.hpdmatrixrcond(_net_a, _net_n, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def cmatrixrcond1(*functionargs):
    # unpack inputs
    a, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.cmatrixrcond1' must be complex matrix")
    _net_n = n
    try:

        # call function
        _net_result = _net_alglib.cmatrixrcond1(_net_a, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def cmatrixrcondinf(*functionargs):
    # unpack inputs
    a, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.cmatrixrcondinf' must be complex matrix")
    _net_n = n
    try:

        # call function
        _net_result = _net_alglib.cmatrixrcondinf(_net_a, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def rmatrixlurcond1(*functionargs):
    # unpack inputs
    lua, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_lua = net_from_listlist(lua, DT_REAL, "ALGLIB: parameter 'lua' of 'xalglib.rmatrixlurcond1' must be real matrix")
    _net_n = n
    try:

        # call function
        _net_result = _net_alglib.rmatrixlurcond1(_net_lua, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def rmatrixlurcondinf(*functionargs):
    # unpack inputs
    lua, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_lua = net_from_listlist(lua, DT_REAL, "ALGLIB: parameter 'lua' of 'xalglib.rmatrixlurcondinf' must be real matrix")
    _net_n = n
    try:

        # call function
        _net_result = _net_alglib.rmatrixlurcondinf(_net_lua, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def spdmatrixcholeskyrcond(*functionargs):
    # unpack inputs
    a, n, isupper = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.spdmatrixcholeskyrcond' must be real matrix")
    _net_n = n
    _net_isupper = isupper
    try:

        # call function
        _net_result = _net_alglib.spdmatrixcholeskyrcond(_net_a, _net_n, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def hpdmatrixcholeskyrcond(*functionargs):
    # unpack inputs
    a, n, isupper = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.hpdmatrixcholeskyrcond' must be complex matrix")
    _net_n = n
    _net_isupper = isupper
    try:

        # call function
        _net_result = _net_alglib.hpdmatrixcholeskyrcond(_net_a, _net_n, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def cmatrixlurcond1(*functionargs):
    # unpack inputs
    lua, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_lua = net_from_listlist(lua, DT_COMPLEX, "ALGLIB: parameter 'lua' of 'xalglib.cmatrixlurcond1' must be complex matrix")
    _net_n = n
    try:

        # call function
        _net_result = _net_alglib.cmatrixlurcond1(_net_lua, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def cmatrixlurcondinf(*functionargs):
    # unpack inputs
    lua, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_lua = net_from_listlist(lua, DT_COMPLEX, "ALGLIB: parameter 'lua' of 'xalglib.cmatrixlurcondinf' must be complex matrix")
    _net_n = n
    try:

        # call function
        _net_result = _net_alglib.cmatrixlurcondinf(_net_lua, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def cmatrixtrrcond1(*functionargs):
    # unpack inputs
    a, n, isupper, isunit = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.cmatrixtrrcond1' must be complex matrix")
    _net_n = n
    _net_isupper = isupper
    _net_isunit = isunit
    try:

        # call function
        _net_result = _net_alglib.cmatrixtrrcond1(_net_a, _net_n, _net_isupper, _net_isunit)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def cmatrixtrrcondinf(*functionargs):
    # unpack inputs
    a, n, isupper, isunit = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.cmatrixtrrcondinf' must be complex matrix")
    _net_n = n
    _net_isupper = isupper
    _net_isunit = isunit
    try:

        # call function
        _net_result = _net_alglib.cmatrixtrrcondinf(_net_a, _net_n, _net_isupper, _net_isunit)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result



class matinvreport(object):
    def __init__(self):
        self.r1 = 0
        self.rinf = 0


def net_from_matinvreport(x,v):
    x.r1 = float(v.r1)
    x.rinf = float(v.rinf)
    return




def matinvreport_from_net(x):
    r = matinvreport()
    r.r1 = x.r1
    r.rinf = x.rinf
    return r


def rmatrixluinverse(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        a, pivots, n = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        a, pivots = functionargs
        n = check_equality_and_get([safe_cols("'rmatrixluinverse': incorrect parameters",a), safe_rows("'rmatrixluinverse': incorrect parameters",a), safe_len("'rmatrixluinverse': incorrect parameters",pivots)],"Error while calling 'rmatrixluinverse': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'rmatrixluinverse': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixluinverse' must be real matrix")
    _net_pivots = net_from_list(pivots, DT_INT, "ALGLIB: parameter 'pivots' of 'xalglib.rmatrixluinverse' must be int vector")
    _net_n = n
    try:

        # call function
        _net_a, _net_info, _net_rep = _net_alglib.rmatrixluinverse(_net_a, _net_pivots, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)
    info = _net_info
    rep = matinvreport_from_net(_net_rep)

    # return
    return (a, info, rep)

def smp_rmatrixluinverse(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        a, pivots, n = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        a, pivots = functionargs
        n = check_equality_and_get([safe_cols("'smp_rmatrixluinverse': incorrect parameters",a), safe_rows("'smp_rmatrixluinverse': incorrect parameters",a), safe_len("'smp_rmatrixluinverse': incorrect parameters",pivots)],"Error while calling 'smp_rmatrixluinverse': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'smp_rmatrixluinverse': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smp_rmatrixluinverse' must be real matrix")
    _net_pivots = net_from_list(pivots, DT_INT, "ALGLIB: parameter 'pivots' of 'xalglib.smp_rmatrixluinverse' must be int vector")
    _net_n = n
    try:

        # call function
        _net_a, _net_info, _net_rep = _net_alglib.smp_rmatrixluinverse(_net_a, _net_pivots, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)
    info = _net_info
    rep = matinvreport_from_net(_net_rep)

    # return
    return (a, info, rep)

def rmatrixinverse(*functionargs):
    # unpack inputs
    if len(functionargs)==2:
        # full-form call
        a, n = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        a,  = functionargs
        n = check_equality_and_get([safe_cols("'rmatrixinverse': incorrect parameters",a), safe_rows("'rmatrixinverse': incorrect parameters",a)],"Error while calling 'rmatrixinverse': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'rmatrixinverse': function must have 2 or 1 parameters")

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixinverse' must be real matrix")
    _net_n = n
    try:

        # call function
        _net_a, _net_info, _net_rep = _net_alglib.rmatrixinverse(_net_a, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)
    info = _net_info
    rep = matinvreport_from_net(_net_rep)

    # return
    return (a, info, rep)

def smp_rmatrixinverse(*functionargs):
    # unpack inputs
    if len(functionargs)==2:
        # full-form call
        a, n = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        a,  = functionargs
        n = check_equality_and_get([safe_cols("'smp_rmatrixinverse': incorrect parameters",a), safe_rows("'smp_rmatrixinverse': incorrect parameters",a)],"Error while calling 'smp_rmatrixinverse': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'smp_rmatrixinverse': function must have 2 or 1 parameters")

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smp_rmatrixinverse' must be real matrix")
    _net_n = n
    try:

        # call function
        _net_a, _net_info, _net_rep = _net_alglib.smp_rmatrixinverse(_net_a, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)
    info = _net_info
    rep = matinvreport_from_net(_net_rep)

    # return
    return (a, info, rep)

def cmatrixluinverse(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        a, pivots, n = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        a, pivots = functionargs
        n = check_equality_and_get([safe_cols("'cmatrixluinverse': incorrect parameters",a), safe_rows("'cmatrixluinverse': incorrect parameters",a), safe_len("'cmatrixluinverse': incorrect parameters",pivots)],"Error while calling 'cmatrixluinverse': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'cmatrixluinverse': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.cmatrixluinverse' must be complex matrix")
    _net_pivots = net_from_list(pivots, DT_INT, "ALGLIB: parameter 'pivots' of 'xalglib.cmatrixluinverse' must be int vector")
    _net_n = n
    try:

        # call function
        _net_a, _net_info, _net_rep = _net_alglib.cmatrixluinverse(_net_a, _net_pivots, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_COMPLEX)
    info = _net_info
    rep = matinvreport_from_net(_net_rep)

    # return
    return (a, info, rep)

def smp_cmatrixluinverse(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        a, pivots, n = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        a, pivots = functionargs
        n = check_equality_and_get([safe_cols("'smp_cmatrixluinverse': incorrect parameters",a), safe_rows("'smp_cmatrixluinverse': incorrect parameters",a), safe_len("'smp_cmatrixluinverse': incorrect parameters",pivots)],"Error while calling 'smp_cmatrixluinverse': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'smp_cmatrixluinverse': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.smp_cmatrixluinverse' must be complex matrix")
    _net_pivots = net_from_list(pivots, DT_INT, "ALGLIB: parameter 'pivots' of 'xalglib.smp_cmatrixluinverse' must be int vector")
    _net_n = n
    try:

        # call function
        _net_a, _net_info, _net_rep = _net_alglib.smp_cmatrixluinverse(_net_a, _net_pivots, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_COMPLEX)
    info = _net_info
    rep = matinvreport_from_net(_net_rep)

    # return
    return (a, info, rep)

def cmatrixinverse(*functionargs):
    # unpack inputs
    if len(functionargs)==2:
        # full-form call
        a, n = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        a,  = functionargs
        n = check_equality_and_get([safe_cols("'cmatrixinverse': incorrect parameters",a), safe_rows("'cmatrixinverse': incorrect parameters",a)],"Error while calling 'cmatrixinverse': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'cmatrixinverse': function must have 2 or 1 parameters")

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.cmatrixinverse' must be complex matrix")
    _net_n = n
    try:

        # call function
        _net_a, _net_info, _net_rep = _net_alglib.cmatrixinverse(_net_a, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_COMPLEX)
    info = _net_info
    rep = matinvreport_from_net(_net_rep)

    # return
    return (a, info, rep)

def smp_cmatrixinverse(*functionargs):
    # unpack inputs
    if len(functionargs)==2:
        # full-form call
        a, n = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        a,  = functionargs
        n = check_equality_and_get([safe_cols("'smp_cmatrixinverse': incorrect parameters",a), safe_rows("'smp_cmatrixinverse': incorrect parameters",a)],"Error while calling 'smp_cmatrixinverse': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'smp_cmatrixinverse': function must have 2 or 1 parameters")

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.smp_cmatrixinverse' must be complex matrix")
    _net_n = n
    try:

        # call function
        _net_a, _net_info, _net_rep = _net_alglib.smp_cmatrixinverse(_net_a, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_COMPLEX)
    info = _net_info
    rep = matinvreport_from_net(_net_rep)

    # return
    return (a, info, rep)

def spdmatrixcholeskyinverse(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        a, n, isupper = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        a,  = functionargs
        n = check_equality_and_get([safe_cols("'spdmatrixcholeskyinverse': incorrect parameters",a), safe_rows("'spdmatrixcholeskyinverse': incorrect parameters",a)],"Error while calling 'spdmatrixcholeskyinverse': looks like one of arguments has wrong size")
        isupper = check_equality_and_get([False],"Error while calling 'spdmatrixcholeskyinverse': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'spdmatrixcholeskyinverse': function must have 3 or 1 parameters")

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.spdmatrixcholeskyinverse' must be real matrix")
    _net_n = n
    _net_isupper = isupper
    try:

        # call function
        _net_a, _net_info, _net_rep = _net_alglib.spdmatrixcholeskyinverse(_net_a, _net_n, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)
    info = _net_info
    rep = matinvreport_from_net(_net_rep)

    # return
    return (a, info, rep)

def smp_spdmatrixcholeskyinverse(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        a, n, isupper = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        a,  = functionargs
        n = check_equality_and_get([safe_cols("'smp_spdmatrixcholeskyinverse': incorrect parameters",a), safe_rows("'smp_spdmatrixcholeskyinverse': incorrect parameters",a)],"Error while calling 'smp_spdmatrixcholeskyinverse': looks like one of arguments has wrong size")
        isupper = check_equality_and_get([False],"Error while calling 'smp_spdmatrixcholeskyinverse': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'smp_spdmatrixcholeskyinverse': function must have 3 or 1 parameters")

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smp_spdmatrixcholeskyinverse' must be real matrix")
    _net_n = n
    _net_isupper = isupper
    try:

        # call function
        _net_a, _net_info, _net_rep = _net_alglib.smp_spdmatrixcholeskyinverse(_net_a, _net_n, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)
    info = _net_info
    rep = matinvreport_from_net(_net_rep)

    # return
    return (a, info, rep)

def spdmatrixinverse(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        a, n, isupper = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        a,  = functionargs
        n = check_equality_and_get([safe_cols("'spdmatrixinverse': incorrect parameters",a), safe_rows("'spdmatrixinverse': incorrect parameters",a)],"Error while calling 'spdmatrixinverse': looks like one of arguments has wrong size")
        isupper = check_equality_and_get([False],"Error while calling 'spdmatrixinverse': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'spdmatrixinverse': function must have 3 or 1 parameters")

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.spdmatrixinverse' must be real matrix")
    if friendly_form and (not _net_alglib.ap.issymmetric(_net_a)):
        raise ValueError("ALGLIB: parameter 'a' of 'xalglib.spdmatrixinverse' must be symmetric matrix")
    _net_n = n
    _net_isupper = isupper
    try:

        # call function
        _net_a, _net_info, _net_rep = _net_alglib.spdmatrixinverse(_net_a, _net_n, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    if friendly_form and (not _net_alglib.ap.forcesymmetric(_net_a)):
        raise RuntimeError("ALGLIB: internal error while post-processing parameter 'a' of 'xalglib.spdmatrixinverse'")
    a = listlist_from_net(_net_a, DT_REAL)
    info = _net_info
    rep = matinvreport_from_net(_net_rep)

    # return
    return (a, info, rep)

def smp_spdmatrixinverse(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        a, n, isupper = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        a,  = functionargs
        n = check_equality_and_get([safe_cols("'smp_spdmatrixinverse': incorrect parameters",a), safe_rows("'smp_spdmatrixinverse': incorrect parameters",a)],"Error while calling 'smp_spdmatrixinverse': looks like one of arguments has wrong size")
        isupper = check_equality_and_get([False],"Error while calling 'smp_spdmatrixinverse': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'smp_spdmatrixinverse': function must have 3 or 1 parameters")

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smp_spdmatrixinverse' must be real matrix")
    if friendly_form and (not _net_alglib.ap.issymmetric(_net_a)):
        raise ValueError("ALGLIB: parameter 'a' of 'xalglib.smp_spdmatrixinverse' must be symmetric matrix")
    _net_n = n
    _net_isupper = isupper
    try:

        # call function
        _net_a, _net_info, _net_rep = _net_alglib.smp_spdmatrixinverse(_net_a, _net_n, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    if friendly_form and (not _net_alglib.ap.forcesymmetric(_net_a)):
        raise RuntimeError("ALGLIB: internal error while post-processing parameter 'a' of 'xalglib.smp_spdmatrixinverse'")
    a = listlist_from_net(_net_a, DT_REAL)
    info = _net_info
    rep = matinvreport_from_net(_net_rep)

    # return
    return (a, info, rep)

def hpdmatrixcholeskyinverse(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        a, n, isupper = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        a,  = functionargs
        n = check_equality_and_get([safe_cols("'hpdmatrixcholeskyinverse': incorrect parameters",a), safe_rows("'hpdmatrixcholeskyinverse': incorrect parameters",a)],"Error while calling 'hpdmatrixcholeskyinverse': looks like one of arguments has wrong size")
        isupper = check_equality_and_get([False],"Error while calling 'hpdmatrixcholeskyinverse': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'hpdmatrixcholeskyinverse': function must have 3 or 1 parameters")

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.hpdmatrixcholeskyinverse' must be complex matrix")
    _net_n = n
    _net_isupper = isupper
    try:

        # call function
        _net_a, _net_info, _net_rep = _net_alglib.hpdmatrixcholeskyinverse(_net_a, _net_n, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_COMPLEX)
    info = _net_info
    rep = matinvreport_from_net(_net_rep)

    # return
    return (a, info, rep)

def smp_hpdmatrixcholeskyinverse(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        a, n, isupper = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        a,  = functionargs
        n = check_equality_and_get([safe_cols("'smp_hpdmatrixcholeskyinverse': incorrect parameters",a), safe_rows("'smp_hpdmatrixcholeskyinverse': incorrect parameters",a)],"Error while calling 'smp_hpdmatrixcholeskyinverse': looks like one of arguments has wrong size")
        isupper = check_equality_and_get([False],"Error while calling 'smp_hpdmatrixcholeskyinverse': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'smp_hpdmatrixcholeskyinverse': function must have 3 or 1 parameters")

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.smp_hpdmatrixcholeskyinverse' must be complex matrix")
    _net_n = n
    _net_isupper = isupper
    try:

        # call function
        _net_a, _net_info, _net_rep = _net_alglib.smp_hpdmatrixcholeskyinverse(_net_a, _net_n, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_COMPLEX)
    info = _net_info
    rep = matinvreport_from_net(_net_rep)

    # return
    return (a, info, rep)

def hpdmatrixinverse(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        a, n, isupper = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        a,  = functionargs
        n = check_equality_and_get([safe_cols("'hpdmatrixinverse': incorrect parameters",a), safe_rows("'hpdmatrixinverse': incorrect parameters",a)],"Error while calling 'hpdmatrixinverse': looks like one of arguments has wrong size")
        isupper = check_equality_and_get([False],"Error while calling 'hpdmatrixinverse': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'hpdmatrixinverse': function must have 3 or 1 parameters")

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.hpdmatrixinverse' must be complex matrix")
    if friendly_form and (not _net_alglib.ap.ishermitian(_net_a)):
        raise ValueError("ALGLIB: parameter 'a' of 'xalglib.hpdmatrixinverse' must be Hermitian matrix")
    _net_n = n
    _net_isupper = isupper
    try:

        # call function
        _net_a, _net_info, _net_rep = _net_alglib.hpdmatrixinverse(_net_a, _net_n, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    if friendly_form and (not _net_alglib.ap.forcehermitian(_net_a)):
        raise RuntimeError("ALGLIB: internal error while post-processing parameter 'a' of 'xalglib.hpdmatrixinverse'")
    a = listlist_from_net(_net_a, DT_COMPLEX)
    info = _net_info
    rep = matinvreport_from_net(_net_rep)

    # return
    return (a, info, rep)

def smp_hpdmatrixinverse(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        a, n, isupper = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        a,  = functionargs
        n = check_equality_and_get([safe_cols("'smp_hpdmatrixinverse': incorrect parameters",a), safe_rows("'smp_hpdmatrixinverse': incorrect parameters",a)],"Error while calling 'smp_hpdmatrixinverse': looks like one of arguments has wrong size")
        isupper = check_equality_and_get([False],"Error while calling 'smp_hpdmatrixinverse': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'smp_hpdmatrixinverse': function must have 3 or 1 parameters")

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.smp_hpdmatrixinverse' must be complex matrix")
    if friendly_form and (not _net_alglib.ap.ishermitian(_net_a)):
        raise ValueError("ALGLIB: parameter 'a' of 'xalglib.smp_hpdmatrixinverse' must be Hermitian matrix")
    _net_n = n
    _net_isupper = isupper
    try:

        # call function
        _net_a, _net_info, _net_rep = _net_alglib.smp_hpdmatrixinverse(_net_a, _net_n, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    if friendly_form and (not _net_alglib.ap.forcehermitian(_net_a)):
        raise RuntimeError("ALGLIB: internal error while post-processing parameter 'a' of 'xalglib.smp_hpdmatrixinverse'")
    a = listlist_from_net(_net_a, DT_COMPLEX)
    info = _net_info
    rep = matinvreport_from_net(_net_rep)

    # return
    return (a, info, rep)

def rmatrixtrinverse(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        a, n, isupper, isunit = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        a, isupper = functionargs
        n = check_equality_and_get([safe_cols("'rmatrixtrinverse': incorrect parameters",a), safe_rows("'rmatrixtrinverse': incorrect parameters",a)],"Error while calling 'rmatrixtrinverse': looks like one of arguments has wrong size")
        isunit = check_equality_and_get([False],"Error while calling 'rmatrixtrinverse': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'rmatrixtrinverse': function must have 4 or 2 parameters")

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixtrinverse' must be real matrix")
    _net_n = n
    _net_isupper = isupper
    _net_isunit = isunit
    try:

        # call function
        _net_a, _net_info, _net_rep = _net_alglib.rmatrixtrinverse(_net_a, _net_n, _net_isupper, _net_isunit)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)
    info = _net_info
    rep = matinvreport_from_net(_net_rep)

    # return
    return (a, info, rep)

def smp_rmatrixtrinverse(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        a, n, isupper, isunit = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        a, isupper = functionargs
        n = check_equality_and_get([safe_cols("'smp_rmatrixtrinverse': incorrect parameters",a), safe_rows("'smp_rmatrixtrinverse': incorrect parameters",a)],"Error while calling 'smp_rmatrixtrinverse': looks like one of arguments has wrong size")
        isunit = check_equality_and_get([False],"Error while calling 'smp_rmatrixtrinverse': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'smp_rmatrixtrinverse': function must have 4 or 2 parameters")

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smp_rmatrixtrinverse' must be real matrix")
    _net_n = n
    _net_isupper = isupper
    _net_isunit = isunit
    try:

        # call function
        _net_a, _net_info, _net_rep = _net_alglib.smp_rmatrixtrinverse(_net_a, _net_n, _net_isupper, _net_isunit)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)
    info = _net_info
    rep = matinvreport_from_net(_net_rep)

    # return
    return (a, info, rep)

def cmatrixtrinverse(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        a, n, isupper, isunit = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        a, isupper = functionargs
        n = check_equality_and_get([safe_cols("'cmatrixtrinverse': incorrect parameters",a), safe_rows("'cmatrixtrinverse': incorrect parameters",a)],"Error while calling 'cmatrixtrinverse': looks like one of arguments has wrong size")
        isunit = check_equality_and_get([False],"Error while calling 'cmatrixtrinverse': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'cmatrixtrinverse': function must have 4 or 2 parameters")

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.cmatrixtrinverse' must be complex matrix")
    _net_n = n
    _net_isupper = isupper
    _net_isunit = isunit
    try:

        # call function
        _net_a, _net_info, _net_rep = _net_alglib.cmatrixtrinverse(_net_a, _net_n, _net_isupper, _net_isunit)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_COMPLEX)
    info = _net_info
    rep = matinvreport_from_net(_net_rep)

    # return
    return (a, info, rep)

def smp_cmatrixtrinverse(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        a, n, isupper, isunit = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        a, isupper = functionargs
        n = check_equality_and_get([safe_cols("'smp_cmatrixtrinverse': incorrect parameters",a), safe_rows("'smp_cmatrixtrinverse': incorrect parameters",a)],"Error while calling 'smp_cmatrixtrinverse': looks like one of arguments has wrong size")
        isunit = check_equality_and_get([False],"Error while calling 'smp_cmatrixtrinverse': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'smp_cmatrixtrinverse': function must have 4 or 2 parameters")

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.smp_cmatrixtrinverse' must be complex matrix")
    _net_n = n
    _net_isupper = isupper
    _net_isunit = isunit
    try:

        # call function
        _net_a, _net_info, _net_rep = _net_alglib.smp_cmatrixtrinverse(_net_a, _net_n, _net_isupper, _net_isunit)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_COMPLEX)
    info = _net_info
    rep = matinvreport_from_net(_net_rep)

    # return
    return (a, info, rep)

def rmatrixqr(*functionargs):
    # unpack inputs
    a, m, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixqr' must be real matrix")
    _net_m = m
    _net_n = n
    try:

        # call function
        _net_a, _net_tau = _net_alglib.rmatrixqr(_net_a, _net_m, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)
    tau = list_from_net(_net_tau, DT_REAL)

    # return
    return (a, tau)

def smp_rmatrixqr(*functionargs):
    # unpack inputs
    a, m, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smp_rmatrixqr' must be real matrix")
    _net_m = m
    _net_n = n
    try:

        # call function
        _net_a, _net_tau = _net_alglib.smp_rmatrixqr(_net_a, _net_m, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)
    tau = list_from_net(_net_tau, DT_REAL)

    # return
    return (a, tau)

def rmatrixlq(*functionargs):
    # unpack inputs
    a, m, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixlq' must be real matrix")
    _net_m = m
    _net_n = n
    try:

        # call function
        _net_a, _net_tau = _net_alglib.rmatrixlq(_net_a, _net_m, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)
    tau = list_from_net(_net_tau, DT_REAL)

    # return
    return (a, tau)

def smp_rmatrixlq(*functionargs):
    # unpack inputs
    a, m, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smp_rmatrixlq' must be real matrix")
    _net_m = m
    _net_n = n
    try:

        # call function
        _net_a, _net_tau = _net_alglib.smp_rmatrixlq(_net_a, _net_m, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)
    tau = list_from_net(_net_tau, DT_REAL)

    # return
    return (a, tau)

def cmatrixqr(*functionargs):
    # unpack inputs
    a, m, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.cmatrixqr' must be complex matrix")
    _net_m = m
    _net_n = n
    try:

        # call function
        _net_a, _net_tau = _net_alglib.cmatrixqr(_net_a, _net_m, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_COMPLEX)
    tau = list_from_net(_net_tau, DT_COMPLEX)

    # return
    return (a, tau)

def smp_cmatrixqr(*functionargs):
    # unpack inputs
    a, m, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.smp_cmatrixqr' must be complex matrix")
    _net_m = m
    _net_n = n
    try:

        # call function
        _net_a, _net_tau = _net_alglib.smp_cmatrixqr(_net_a, _net_m, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_COMPLEX)
    tau = list_from_net(_net_tau, DT_COMPLEX)

    # return
    return (a, tau)

def cmatrixlq(*functionargs):
    # unpack inputs
    a, m, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.cmatrixlq' must be complex matrix")
    _net_m = m
    _net_n = n
    try:

        # call function
        _net_a, _net_tau = _net_alglib.cmatrixlq(_net_a, _net_m, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_COMPLEX)
    tau = list_from_net(_net_tau, DT_COMPLEX)

    # return
    return (a, tau)

def smp_cmatrixlq(*functionargs):
    # unpack inputs
    a, m, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.smp_cmatrixlq' must be complex matrix")
    _net_m = m
    _net_n = n
    try:

        # call function
        _net_a, _net_tau = _net_alglib.smp_cmatrixlq(_net_a, _net_m, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_COMPLEX)
    tau = list_from_net(_net_tau, DT_COMPLEX)

    # return
    return (a, tau)

def rmatrixqrunpackq(*functionargs):
    # unpack inputs
    a, m, n, tau, qcolumns = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixqrunpackq' must be real matrix")
    _net_m = m
    _net_n = n
    _net_tau = net_from_list(tau, DT_REAL, "ALGLIB: parameter 'tau' of 'xalglib.rmatrixqrunpackq' must be real vector")
    _net_qcolumns = qcolumns
    try:

        # call function
        _net_q = _net_alglib.rmatrixqrunpackq(_net_a, _net_m, _net_n, _net_tau, _net_qcolumns)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    q = listlist_from_net(_net_q, DT_REAL)

    # return
    return q

def smp_rmatrixqrunpackq(*functionargs):
    # unpack inputs
    a, m, n, tau, qcolumns = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smp_rmatrixqrunpackq' must be real matrix")
    _net_m = m
    _net_n = n
    _net_tau = net_from_list(tau, DT_REAL, "ALGLIB: parameter 'tau' of 'xalglib.smp_rmatrixqrunpackq' must be real vector")
    _net_qcolumns = qcolumns
    try:

        # call function
        _net_q = _net_alglib.smp_rmatrixqrunpackq(_net_a, _net_m, _net_n, _net_tau, _net_qcolumns)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    q = listlist_from_net(_net_q, DT_REAL)

    # return
    return q

def rmatrixqrunpackr(*functionargs):
    # unpack inputs
    a, m, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixqrunpackr' must be real matrix")
    _net_m = m
    _net_n = n
    try:

        # call function
        _net_r = _net_alglib.rmatrixqrunpackr(_net_a, _net_m, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    r = listlist_from_net(_net_r, DT_REAL)

    # return
    return r

def rmatrixlqunpackq(*functionargs):
    # unpack inputs
    a, m, n, tau, qrows = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixlqunpackq' must be real matrix")
    _net_m = m
    _net_n = n
    _net_tau = net_from_list(tau, DT_REAL, "ALGLIB: parameter 'tau' of 'xalglib.rmatrixlqunpackq' must be real vector")
    _net_qrows = qrows
    try:

        # call function
        _net_q = _net_alglib.rmatrixlqunpackq(_net_a, _net_m, _net_n, _net_tau, _net_qrows)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    q = listlist_from_net(_net_q, DT_REAL)

    # return
    return q

def smp_rmatrixlqunpackq(*functionargs):
    # unpack inputs
    a, m, n, tau, qrows = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smp_rmatrixlqunpackq' must be real matrix")
    _net_m = m
    _net_n = n
    _net_tau = net_from_list(tau, DT_REAL, "ALGLIB: parameter 'tau' of 'xalglib.smp_rmatrixlqunpackq' must be real vector")
    _net_qrows = qrows
    try:

        # call function
        _net_q = _net_alglib.smp_rmatrixlqunpackq(_net_a, _net_m, _net_n, _net_tau, _net_qrows)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    q = listlist_from_net(_net_q, DT_REAL)

    # return
    return q

def rmatrixlqunpackl(*functionargs):
    # unpack inputs
    a, m, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixlqunpackl' must be real matrix")
    _net_m = m
    _net_n = n
    try:

        # call function
        _net_l = _net_alglib.rmatrixlqunpackl(_net_a, _net_m, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    l = listlist_from_net(_net_l, DT_REAL)

    # return
    return l

def cmatrixqrunpackq(*functionargs):
    # unpack inputs
    a, m, n, tau, qcolumns = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.cmatrixqrunpackq' must be complex matrix")
    _net_m = m
    _net_n = n
    _net_tau = net_from_list(tau, DT_COMPLEX, "ALGLIB: parameter 'tau' of 'xalglib.cmatrixqrunpackq' must be complex vector")
    _net_qcolumns = qcolumns
    try:

        # call function
        _net_q = _net_alglib.cmatrixqrunpackq(_net_a, _net_m, _net_n, _net_tau, _net_qcolumns)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    q = listlist_from_net(_net_q, DT_COMPLEX)

    # return
    return q

def smp_cmatrixqrunpackq(*functionargs):
    # unpack inputs
    a, m, n, tau, qcolumns = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.smp_cmatrixqrunpackq' must be complex matrix")
    _net_m = m
    _net_n = n
    _net_tau = net_from_list(tau, DT_COMPLEX, "ALGLIB: parameter 'tau' of 'xalglib.smp_cmatrixqrunpackq' must be complex vector")
    _net_qcolumns = qcolumns
    try:

        # call function
        _net_q = _net_alglib.smp_cmatrixqrunpackq(_net_a, _net_m, _net_n, _net_tau, _net_qcolumns)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    q = listlist_from_net(_net_q, DT_COMPLEX)

    # return
    return q

def cmatrixqrunpackr(*functionargs):
    # unpack inputs
    a, m, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.cmatrixqrunpackr' must be complex matrix")
    _net_m = m
    _net_n = n
    try:

        # call function
        _net_r = _net_alglib.cmatrixqrunpackr(_net_a, _net_m, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    r = listlist_from_net(_net_r, DT_COMPLEX)

    # return
    return r

def cmatrixlqunpackq(*functionargs):
    # unpack inputs
    a, m, n, tau, qrows = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.cmatrixlqunpackq' must be complex matrix")
    _net_m = m
    _net_n = n
    _net_tau = net_from_list(tau, DT_COMPLEX, "ALGLIB: parameter 'tau' of 'xalglib.cmatrixlqunpackq' must be complex vector")
    _net_qrows = qrows
    try:

        # call function
        _net_q = _net_alglib.cmatrixlqunpackq(_net_a, _net_m, _net_n, _net_tau, _net_qrows)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    q = listlist_from_net(_net_q, DT_COMPLEX)

    # return
    return q

def smp_cmatrixlqunpackq(*functionargs):
    # unpack inputs
    a, m, n, tau, qrows = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.smp_cmatrixlqunpackq' must be complex matrix")
    _net_m = m
    _net_n = n
    _net_tau = net_from_list(tau, DT_COMPLEX, "ALGLIB: parameter 'tau' of 'xalglib.smp_cmatrixlqunpackq' must be complex vector")
    _net_qrows = qrows
    try:

        # call function
        _net_q = _net_alglib.smp_cmatrixlqunpackq(_net_a, _net_m, _net_n, _net_tau, _net_qrows)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    q = listlist_from_net(_net_q, DT_COMPLEX)

    # return
    return q

def cmatrixlqunpackl(*functionargs):
    # unpack inputs
    a, m, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.cmatrixlqunpackl' must be complex matrix")
    _net_m = m
    _net_n = n
    try:

        # call function
        _net_l = _net_alglib.cmatrixlqunpackl(_net_a, _net_m, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    l = listlist_from_net(_net_l, DT_COMPLEX)

    # return
    return l

def rmatrixbd(*functionargs):
    # unpack inputs
    a, m, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixbd' must be real matrix")
    _net_m = m
    _net_n = n
    try:

        # call function
        _net_a, _net_tauq, _net_taup = _net_alglib.rmatrixbd(_net_a, _net_m, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)
    tauq = list_from_net(_net_tauq, DT_REAL)
    taup = list_from_net(_net_taup, DT_REAL)

    # return
    return (a, tauq, taup)

def rmatrixbdunpackq(*functionargs):
    # unpack inputs
    qp, m, n, tauq, qcolumns = functionargs
    friendly_form = False

    # convert to .NET types
    _net_qp = net_from_listlist(qp, DT_REAL, "ALGLIB: parameter 'qp' of 'xalglib.rmatrixbdunpackq' must be real matrix")
    _net_m = m
    _net_n = n
    _net_tauq = net_from_list(tauq, DT_REAL, "ALGLIB: parameter 'tauq' of 'xalglib.rmatrixbdunpackq' must be real vector")
    _net_qcolumns = qcolumns
    try:

        # call function
        _net_q = _net_alglib.rmatrixbdunpackq(_net_qp, _net_m, _net_n, _net_tauq, _net_qcolumns)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    q = listlist_from_net(_net_q, DT_REAL)

    # return
    return q

def rmatrixbdmultiplybyq(*functionargs):
    # unpack inputs
    qp, m, n, tauq, z, zrows, zcolumns, fromtheright, dotranspose = functionargs
    friendly_form = False

    # convert to .NET types
    _net_qp = net_from_listlist(qp, DT_REAL, "ALGLIB: parameter 'qp' of 'xalglib.rmatrixbdmultiplybyq' must be real matrix")
    _net_m = m
    _net_n = n
    _net_tauq = net_from_list(tauq, DT_REAL, "ALGLIB: parameter 'tauq' of 'xalglib.rmatrixbdmultiplybyq' must be real vector")
    _net_z = net_from_listlist(z, DT_REAL, "ALGLIB: parameter 'z' of 'xalglib.rmatrixbdmultiplybyq' must be real matrix")
    _net_zrows = zrows
    _net_zcolumns = zcolumns
    _net_fromtheright = fromtheright
    _net_dotranspose = dotranspose
    try:

        # call function
        _net_z = _net_alglib.rmatrixbdmultiplybyq(_net_qp, _net_m, _net_n, _net_tauq, _net_z, _net_zrows, _net_zcolumns, _net_fromtheright, _net_dotranspose)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    z = listlist_from_net(_net_z, DT_REAL)

    # return
    return z

def rmatrixbdunpackpt(*functionargs):
    # unpack inputs
    qp, m, n, taup, ptrows = functionargs
    friendly_form = False

    # convert to .NET types
    _net_qp = net_from_listlist(qp, DT_REAL, "ALGLIB: parameter 'qp' of 'xalglib.rmatrixbdunpackpt' must be real matrix")
    _net_m = m
    _net_n = n
    _net_taup = net_from_list(taup, DT_REAL, "ALGLIB: parameter 'taup' of 'xalglib.rmatrixbdunpackpt' must be real vector")
    _net_ptrows = ptrows
    try:

        # call function
        _net_pt = _net_alglib.rmatrixbdunpackpt(_net_qp, _net_m, _net_n, _net_taup, _net_ptrows)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    pt = listlist_from_net(_net_pt, DT_REAL)

    # return
    return pt

def rmatrixbdmultiplybyp(*functionargs):
    # unpack inputs
    qp, m, n, taup, z, zrows, zcolumns, fromtheright, dotranspose = functionargs
    friendly_form = False

    # convert to .NET types
    _net_qp = net_from_listlist(qp, DT_REAL, "ALGLIB: parameter 'qp' of 'xalglib.rmatrixbdmultiplybyp' must be real matrix")
    _net_m = m
    _net_n = n
    _net_taup = net_from_list(taup, DT_REAL, "ALGLIB: parameter 'taup' of 'xalglib.rmatrixbdmultiplybyp' must be real vector")
    _net_z = net_from_listlist(z, DT_REAL, "ALGLIB: parameter 'z' of 'xalglib.rmatrixbdmultiplybyp' must be real matrix")
    _net_zrows = zrows
    _net_zcolumns = zcolumns
    _net_fromtheright = fromtheright
    _net_dotranspose = dotranspose
    try:

        # call function
        _net_z = _net_alglib.rmatrixbdmultiplybyp(_net_qp, _net_m, _net_n, _net_taup, _net_z, _net_zrows, _net_zcolumns, _net_fromtheright, _net_dotranspose)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    z = listlist_from_net(_net_z, DT_REAL)

    # return
    return z

def rmatrixbdunpackdiagonals(*functionargs):
    # unpack inputs
    b, m, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_b = net_from_listlist(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.rmatrixbdunpackdiagonals' must be real matrix")
    _net_m = m
    _net_n = n
    try:

        # call function
        _net_isupper, _net_d, _net_e = _net_alglib.rmatrixbdunpackdiagonals(_net_b, _net_m, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    isupper = _net_isupper
    d = list_from_net(_net_d, DT_REAL)
    e = list_from_net(_net_e, DT_REAL)

    # return
    return (isupper, d, e)

def rmatrixhessenberg(*functionargs):
    # unpack inputs
    a, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixhessenberg' must be real matrix")
    _net_n = n
    try:

        # call function
        _net_a, _net_tau = _net_alglib.rmatrixhessenberg(_net_a, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)
    tau = list_from_net(_net_tau, DT_REAL)

    # return
    return (a, tau)

def rmatrixhessenbergunpackq(*functionargs):
    # unpack inputs
    a, n, tau = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixhessenbergunpackq' must be real matrix")
    _net_n = n
    _net_tau = net_from_list(tau, DT_REAL, "ALGLIB: parameter 'tau' of 'xalglib.rmatrixhessenbergunpackq' must be real vector")
    try:

        # call function
        _net_q = _net_alglib.rmatrixhessenbergunpackq(_net_a, _net_n, _net_tau)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    q = listlist_from_net(_net_q, DT_REAL)

    # return
    return q

def rmatrixhessenbergunpackh(*functionargs):
    # unpack inputs
    a, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixhessenbergunpackh' must be real matrix")
    _net_n = n
    try:

        # call function
        _net_h = _net_alglib.rmatrixhessenbergunpackh(_net_a, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    h = listlist_from_net(_net_h, DT_REAL)

    # return
    return h

def smatrixtd(*functionargs):
    # unpack inputs
    a, n, isupper = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smatrixtd' must be real matrix")
    _net_n = n
    _net_isupper = isupper
    try:

        # call function
        _net_a, _net_tau, _net_d, _net_e = _net_alglib.smatrixtd(_net_a, _net_n, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)
    tau = list_from_net(_net_tau, DT_REAL)
    d = list_from_net(_net_d, DT_REAL)
    e = list_from_net(_net_e, DT_REAL)

    # return
    return (a, tau, d, e)

def smatrixtdunpackq(*functionargs):
    # unpack inputs
    a, n, isupper, tau = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smatrixtdunpackq' must be real matrix")
    _net_n = n
    _net_isupper = isupper
    _net_tau = net_from_list(tau, DT_REAL, "ALGLIB: parameter 'tau' of 'xalglib.smatrixtdunpackq' must be real vector")
    try:

        # call function
        _net_q = _net_alglib.smatrixtdunpackq(_net_a, _net_n, _net_isupper, _net_tau)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    q = listlist_from_net(_net_q, DT_REAL)

    # return
    return q

def hmatrixtd(*functionargs):
    # unpack inputs
    a, n, isupper = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.hmatrixtd' must be complex matrix")
    _net_n = n
    _net_isupper = isupper
    try:

        # call function
        _net_a, _net_tau, _net_d, _net_e = _net_alglib.hmatrixtd(_net_a, _net_n, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_COMPLEX)
    tau = list_from_net(_net_tau, DT_COMPLEX)
    d = list_from_net(_net_d, DT_REAL)
    e = list_from_net(_net_e, DT_REAL)

    # return
    return (a, tau, d, e)

def hmatrixtdunpackq(*functionargs):
    # unpack inputs
    a, n, isupper, tau = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.hmatrixtdunpackq' must be complex matrix")
    _net_n = n
    _net_isupper = isupper
    _net_tau = net_from_list(tau, DT_COMPLEX, "ALGLIB: parameter 'tau' of 'xalglib.hmatrixtdunpackq' must be complex vector")
    try:

        # call function
        _net_q = _net_alglib.hmatrixtdunpackq(_net_a, _net_n, _net_isupper, _net_tau)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    q = listlist_from_net(_net_q, DT_COMPLEX)

    # return
    return q

def rmatrixbdsvd(*functionargs):
    # unpack inputs
    d, e, n, isupper, isfractionalaccuracyrequired, u, nru, c, ncc, vt, ncvt = functionargs
    friendly_form = False

    # convert to .NET types
    _net_d = net_from_list(d, DT_REAL, "ALGLIB: parameter 'd' of 'xalglib.rmatrixbdsvd' must be real vector")
    _net_e = net_from_list(e, DT_REAL, "ALGLIB: parameter 'e' of 'xalglib.rmatrixbdsvd' must be real vector")
    _net_n = n
    _net_isupper = isupper
    _net_isfractionalaccuracyrequired = isfractionalaccuracyrequired
    _net_u = net_from_listlist(u, DT_REAL, "ALGLIB: parameter 'u' of 'xalglib.rmatrixbdsvd' must be real matrix")
    _net_nru = nru
    _net_c = net_from_listlist(c, DT_REAL, "ALGLIB: parameter 'c' of 'xalglib.rmatrixbdsvd' must be real matrix")
    _net_ncc = ncc
    _net_vt = net_from_listlist(vt, DT_REAL, "ALGLIB: parameter 'vt' of 'xalglib.rmatrixbdsvd' must be real matrix")
    _net_ncvt = ncvt
    try:

        # call function
        _net_result, _net_d, _net_u, _net_c, _net_vt = _net_alglib.rmatrixbdsvd(_net_d, _net_e, _net_n, _net_isupper, _net_isfractionalaccuracyrequired, _net_u, _net_nru, _net_c, _net_ncc, _net_vt, _net_ncvt)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result
    d = list_from_net(_net_d, DT_REAL)
    u = listlist_from_net(_net_u, DT_REAL)
    c = listlist_from_net(_net_c, DT_REAL)
    vt = listlist_from_net(_net_vt, DT_REAL)

    # return
    return (result, d, u, c, vt)

def rmatrixsvd(*functionargs):
    # unpack inputs
    a, m, n, uneeded, vtneeded, additionalmemory = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixsvd' must be real matrix")
    _net_m = m
    _net_n = n
    _net_uneeded = uneeded
    _net_vtneeded = vtneeded
    _net_additionalmemory = additionalmemory
    try:

        # call function
        _net_result, _net_w, _net_u, _net_vt = _net_alglib.rmatrixsvd(_net_a, _net_m, _net_n, _net_uneeded, _net_vtneeded, _net_additionalmemory)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result
    w = list_from_net(_net_w, DT_REAL)
    u = listlist_from_net(_net_u, DT_REAL)
    vt = listlist_from_net(_net_vt, DT_REAL)

    # return
    return (result, w, u, vt)

def smp_rmatrixsvd(*functionargs):
    # unpack inputs
    a, m, n, uneeded, vtneeded, additionalmemory = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smp_rmatrixsvd' must be real matrix")
    _net_m = m
    _net_n = n
    _net_uneeded = uneeded
    _net_vtneeded = vtneeded
    _net_additionalmemory = additionalmemory
    try:

        # call function
        _net_result, _net_w, _net_u, _net_vt = _net_alglib.smp_rmatrixsvd(_net_a, _net_m, _net_n, _net_uneeded, _net_vtneeded, _net_additionalmemory)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result
    w = list_from_net(_net_w, DT_REAL)
    u = listlist_from_net(_net_u, DT_REAL)
    vt = listlist_from_net(_net_vt, DT_REAL)

    # return
    return (result, w, u, vt)



class minlbfgsstate(object):
    def __init__(self,ptr):
        self.ptr = ptr


class minlbfgsreport(object):
    def __init__(self):
        self.iterationscount = 0
        self.nfev = 0
        self.varidx = 0
        self.terminationtype = 0


def net_from_minlbfgsreport(x,v):
    x.iterationscount = int(v.iterationscount)
    x.nfev = int(v.nfev)
    x.varidx = int(v.varidx)
    x.terminationtype = int(v.terminationtype)
    return




def minlbfgsreport_from_net(x):
    r = minlbfgsreport()
    r.iterationscount = x.iterationscount
    r.nfev = x.nfev
    r.varidx = x.varidx
    r.terminationtype = x.terminationtype
    return r


def minlbfgscreate(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        n, m, x = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        m, x = functionargs
        n = check_equality_and_get([safe_len("'minlbfgscreate': incorrect parameters",x)],"Error while calling 'minlbfgscreate': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'minlbfgscreate': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_n = n
    _net_m = m
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.minlbfgscreate' must be real vector")
    try:

        # call function
        _net_state = _net_alglib.minlbfgscreate(_net_n, _net_m, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = minlbfgsstate(_net_state)

    # return
    return state

def minlbfgscreatef(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        n, m, x, diffstep = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        m, x, diffstep = functionargs
        n = check_equality_and_get([safe_len("'minlbfgscreatef': incorrect parameters",x)],"Error while calling 'minlbfgscreatef': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'minlbfgscreatef': function must have 4 or 3 parameters")

    # convert to .NET types
    _net_n = n
    _net_m = m
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.minlbfgscreatef' must be real vector")
    _net_diffstep = diffstep
    try:

        # call function
        _net_state = _net_alglib.minlbfgscreatef(_net_n, _net_m, _net_x, _net_diffstep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = minlbfgsstate(_net_state)

    # return
    return state

def minlbfgssetcond(*functionargs):
    # unpack inputs
    state, epsg, epsf, epsx, maxits = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_epsg = epsg
    _net_epsf = epsf
    _net_epsx = epsx
    _net_maxits = maxits
    try:

        # call function
        _net_alglib.minlbfgssetcond(_net_state, _net_epsg, _net_epsf, _net_epsx, _net_maxits)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minlbfgssetxrep(*functionargs):
    # unpack inputs
    state, needxrep = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_needxrep = needxrep
    try:

        # call function
        _net_alglib.minlbfgssetxrep(_net_state, _net_needxrep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minlbfgssetstpmax(*functionargs):
    # unpack inputs
    state, stpmax = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_stpmax = stpmax
    try:

        # call function
        _net_alglib.minlbfgssetstpmax(_net_state, _net_stpmax)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minlbfgssetscale(*functionargs):
    # unpack inputs
    state, s = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_s = net_from_list(s, DT_REAL, "ALGLIB: parameter 's' of 'xalglib.minlbfgssetscale' must be real vector")
    try:

        # call function
        _net_alglib.minlbfgssetscale(_net_state, _net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minlbfgssetprecdefault(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_alglib.minlbfgssetprecdefault(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minlbfgssetpreccholesky(*functionargs):
    # unpack inputs
    state, p, isupper = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_p = net_from_listlist(p, DT_REAL, "ALGLIB: parameter 'p' of 'xalglib.minlbfgssetpreccholesky' must be real matrix")
    _net_isupper = isupper
    try:

        # call function
        _net_alglib.minlbfgssetpreccholesky(_net_state, _net_p, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minlbfgssetprecdiag(*functionargs):
    # unpack inputs
    state, d = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_d = net_from_list(d, DT_REAL, "ALGLIB: parameter 'd' of 'xalglib.minlbfgssetprecdiag' must be real vector")
    try:

        # call function
        _net_alglib.minlbfgssetprecdiag(_net_state, _net_d)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minlbfgssetprecscale(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_alglib.minlbfgssetprecscale(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return



def minlbfgsoptimize_f(state, func, rep = None, param = None):
    _net_x  = state.ptr.x
    _py_x = create_real_vector(_net_x.GetLength(0))
    while True:
        try:
            result = _net_alglib.minlbfgsiteration(state.ptr)
        except _net_alglib.alglibexception as e:
            raise RuntimeError(e.msg)
        if not result:
            break
        if state.ptr.needf:
            copy_net_to_list(_net_x, _py_x, DT_REAL)

            fvalue = func(_py_x, param)
            state.ptr.f = fvalue
            continue
        if state.ptr.xupdated:
            if not (rep is None):
                copy_net_to_list(_net_x, _py_x, DT_REAL)
                rep(_py_x, state.ptr.f, param)
            continue
        raise RuntimeError("ALGLIB: error in 'minlbfgsoptimize' (some derivatives were not provided?)")
    return


def minlbfgsoptimize_g(state, grad, rep = None, param = None):
    _net_x  = state.ptr.x
    _py_x = create_real_vector(_net_x.GetLength(0))
    _net_g  = state.ptr.g
    _py_g = create_real_vector(_net_g.GetLength(0))
    while True:
        try:
            result = _net_alglib.minlbfgsiteration(state.ptr)
        except _net_alglib.alglibexception as e:
            raise RuntimeError(e.msg)
        if not result:
            break
        if state.ptr.needfg:
            copy_net_to_list(_net_x, _py_x, DT_REAL)

            fvalue = grad(_py_x, _py_g, param)
            state.ptr.f = fvalue
            copy_list_to_net(_py_g, _net_g, DT_REAL)
            continue
        if state.ptr.xupdated:
            if not (rep is None):
                copy_net_to_list(_net_x, _py_x, DT_REAL)
                rep(_py_x, state.ptr.f, param)
            continue
        raise RuntimeError("ALGLIB: error in 'minlbfgsoptimize' (some derivatives were not provided?)")
    return


def minlbfgsresults(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_x, _net_rep = _net_alglib.minlbfgsresults(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = list_from_net(_net_x, DT_REAL)
    rep = minlbfgsreport_from_net(_net_rep)

    # return
    return (x, rep)

def minlbfgsresultsbuf(*functionargs):
    # unpack inputs
    state, x, rep = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.minlbfgsresultsbuf' must be real vector")
    _net_rep = _net_alglib.minlbfgsreport()
    net_from_minlbfgsreport(_net_rep, rep)
    try:

        # call function
        _net_x, _net_rep = _net_alglib.minlbfgsresultsbuf(_net_state, _net_x, _net_rep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = list_from_net(_net_x, DT_REAL)
    rep = minlbfgsreport_from_net(_net_rep)

    # return
    return (x, rep)

def minlbfgsrestartfrom(*functionargs):
    # unpack inputs
    state, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.minlbfgsrestartfrom' must be real vector")
    try:

        # call function
        _net_alglib.minlbfgsrestartfrom(_net_state, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minlbfgsrequesttermination(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_alglib.minlbfgsrequesttermination(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minlbfgssetgradientcheck(*functionargs):
    # unpack inputs
    state, teststep = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_teststep = teststep
    try:

        # call function
        _net_alglib.minlbfgssetgradientcheck(_net_state, _net_teststep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return



class densesolverreport(object):
    def __init__(self):
        self.r1 = 0
        self.rinf = 0


def net_from_densesolverreport(x,v):
    x.r1 = float(v.r1)
    x.rinf = float(v.rinf)
    return




def densesolverreport_from_net(x):
    r = densesolverreport()
    r.r1 = x.r1
    r.rinf = x.rinf
    return r




class densesolverlsreport(object):
    def __init__(self):
        self.r2 = 0
        self.cx = [[]]
        self.n = 0
        self.k = 0


def net_from_densesolverlsreport(x,v):
    x.r2 = float(v.r2)
    x.cx = net_from_listlist(v.cx, DT_REAL)
    x.n = int(v.n)
    x.k = int(v.k)
    return




def densesolverlsreport_from_net(x):
    r = densesolverlsreport()
    r.r2 = x.r2
    r.cx = listlist_from_net(x.cx, DT_REAL)
    r.n = x.n
    r.k = x.k
    return r


def rmatrixsolve(*functionargs):
    # unpack inputs
    a, n, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixsolve' must be real matrix")
    _net_n = n
    _net_b = net_from_list(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.rmatrixsolve' must be real vector")
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.rmatrixsolve(_net_a, _net_n, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverreport_from_net(_net_rep)
    x = list_from_net(_net_x, DT_REAL)

    # return
    return (info, rep, x)

def smp_rmatrixsolve(*functionargs):
    # unpack inputs
    a, n, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smp_rmatrixsolve' must be real matrix")
    _net_n = n
    _net_b = net_from_list(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.smp_rmatrixsolve' must be real vector")
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.smp_rmatrixsolve(_net_a, _net_n, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverreport_from_net(_net_rep)
    x = list_from_net(_net_x, DT_REAL)

    # return
    return (info, rep, x)

def rmatrixsolvefast(*functionargs):
    # unpack inputs
    a, n, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixsolvefast' must be real matrix")
    _net_n = n
    _net_b = net_from_list(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.rmatrixsolvefast' must be real vector")
    try:

        # call function
        _net_b, _net_info = _net_alglib.rmatrixsolvefast(_net_a, _net_n, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = list_from_net(_net_b, DT_REAL)
    info = _net_info

    # return
    return (b, info)

def smp_rmatrixsolvefast(*functionargs):
    # unpack inputs
    a, n, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smp_rmatrixsolvefast' must be real matrix")
    _net_n = n
    _net_b = net_from_list(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.smp_rmatrixsolvefast' must be real vector")
    try:

        # call function
        _net_b, _net_info = _net_alglib.smp_rmatrixsolvefast(_net_a, _net_n, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = list_from_net(_net_b, DT_REAL)
    info = _net_info

    # return
    return (b, info)

def rmatrixsolvem(*functionargs):
    # unpack inputs
    a, n, b, m, rfs = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixsolvem' must be real matrix")
    _net_n = n
    _net_b = net_from_listlist(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.rmatrixsolvem' must be real matrix")
    _net_m = m
    _net_rfs = rfs
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.rmatrixsolvem(_net_a, _net_n, _net_b, _net_m, _net_rfs)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverreport_from_net(_net_rep)
    x = listlist_from_net(_net_x, DT_REAL)

    # return
    return (info, rep, x)

def smp_rmatrixsolvem(*functionargs):
    # unpack inputs
    a, n, b, m, rfs = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smp_rmatrixsolvem' must be real matrix")
    _net_n = n
    _net_b = net_from_listlist(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.smp_rmatrixsolvem' must be real matrix")
    _net_m = m
    _net_rfs = rfs
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.smp_rmatrixsolvem(_net_a, _net_n, _net_b, _net_m, _net_rfs)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverreport_from_net(_net_rep)
    x = listlist_from_net(_net_x, DT_REAL)

    # return
    return (info, rep, x)

def rmatrixsolvemfast(*functionargs):
    # unpack inputs
    a, n, b, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixsolvemfast' must be real matrix")
    _net_n = n
    _net_b = net_from_listlist(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.rmatrixsolvemfast' must be real matrix")
    _net_m = m
    try:

        # call function
        _net_b, _net_info = _net_alglib.rmatrixsolvemfast(_net_a, _net_n, _net_b, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = listlist_from_net(_net_b, DT_REAL)
    info = _net_info

    # return
    return (b, info)

def smp_rmatrixsolvemfast(*functionargs):
    # unpack inputs
    a, n, b, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smp_rmatrixsolvemfast' must be real matrix")
    _net_n = n
    _net_b = net_from_listlist(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.smp_rmatrixsolvemfast' must be real matrix")
    _net_m = m
    try:

        # call function
        _net_b, _net_info = _net_alglib.smp_rmatrixsolvemfast(_net_a, _net_n, _net_b, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = listlist_from_net(_net_b, DT_REAL)
    info = _net_info

    # return
    return (b, info)

def rmatrixlusolve(*functionargs):
    # unpack inputs
    lua, p, n, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_lua = net_from_listlist(lua, DT_REAL, "ALGLIB: parameter 'lua' of 'xalglib.rmatrixlusolve' must be real matrix")
    _net_p = net_from_list(p, DT_INT, "ALGLIB: parameter 'p' of 'xalglib.rmatrixlusolve' must be int vector")
    _net_n = n
    _net_b = net_from_list(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.rmatrixlusolve' must be real vector")
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.rmatrixlusolve(_net_lua, _net_p, _net_n, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverreport_from_net(_net_rep)
    x = list_from_net(_net_x, DT_REAL)

    # return
    return (info, rep, x)

def rmatrixlusolvefast(*functionargs):
    # unpack inputs
    lua, p, n, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_lua = net_from_listlist(lua, DT_REAL, "ALGLIB: parameter 'lua' of 'xalglib.rmatrixlusolvefast' must be real matrix")
    _net_p = net_from_list(p, DT_INT, "ALGLIB: parameter 'p' of 'xalglib.rmatrixlusolvefast' must be int vector")
    _net_n = n
    _net_b = net_from_list(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.rmatrixlusolvefast' must be real vector")
    try:

        # call function
        _net_b, _net_info = _net_alglib.rmatrixlusolvefast(_net_lua, _net_p, _net_n, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = list_from_net(_net_b, DT_REAL)
    info = _net_info

    # return
    return (b, info)

def rmatrixlusolvem(*functionargs):
    # unpack inputs
    lua, p, n, b, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_lua = net_from_listlist(lua, DT_REAL, "ALGLIB: parameter 'lua' of 'xalglib.rmatrixlusolvem' must be real matrix")
    _net_p = net_from_list(p, DT_INT, "ALGLIB: parameter 'p' of 'xalglib.rmatrixlusolvem' must be int vector")
    _net_n = n
    _net_b = net_from_listlist(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.rmatrixlusolvem' must be real matrix")
    _net_m = m
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.rmatrixlusolvem(_net_lua, _net_p, _net_n, _net_b, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverreport_from_net(_net_rep)
    x = listlist_from_net(_net_x, DT_REAL)

    # return
    return (info, rep, x)

def smp_rmatrixlusolvem(*functionargs):
    # unpack inputs
    lua, p, n, b, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_lua = net_from_listlist(lua, DT_REAL, "ALGLIB: parameter 'lua' of 'xalglib.smp_rmatrixlusolvem' must be real matrix")
    _net_p = net_from_list(p, DT_INT, "ALGLIB: parameter 'p' of 'xalglib.smp_rmatrixlusolvem' must be int vector")
    _net_n = n
    _net_b = net_from_listlist(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.smp_rmatrixlusolvem' must be real matrix")
    _net_m = m
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.smp_rmatrixlusolvem(_net_lua, _net_p, _net_n, _net_b, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverreport_from_net(_net_rep)
    x = listlist_from_net(_net_x, DT_REAL)

    # return
    return (info, rep, x)

def rmatrixlusolvemfast(*functionargs):
    # unpack inputs
    lua, p, n, b, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_lua = net_from_listlist(lua, DT_REAL, "ALGLIB: parameter 'lua' of 'xalglib.rmatrixlusolvemfast' must be real matrix")
    _net_p = net_from_list(p, DT_INT, "ALGLIB: parameter 'p' of 'xalglib.rmatrixlusolvemfast' must be int vector")
    _net_n = n
    _net_b = net_from_listlist(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.rmatrixlusolvemfast' must be real matrix")
    _net_m = m
    try:

        # call function
        _net_b, _net_info = _net_alglib.rmatrixlusolvemfast(_net_lua, _net_p, _net_n, _net_b, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = listlist_from_net(_net_b, DT_REAL)
    info = _net_info

    # return
    return (b, info)

def smp_rmatrixlusolvemfast(*functionargs):
    # unpack inputs
    lua, p, n, b, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_lua = net_from_listlist(lua, DT_REAL, "ALGLIB: parameter 'lua' of 'xalglib.smp_rmatrixlusolvemfast' must be real matrix")
    _net_p = net_from_list(p, DT_INT, "ALGLIB: parameter 'p' of 'xalglib.smp_rmatrixlusolvemfast' must be int vector")
    _net_n = n
    _net_b = net_from_listlist(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.smp_rmatrixlusolvemfast' must be real matrix")
    _net_m = m
    try:

        # call function
        _net_b, _net_info = _net_alglib.smp_rmatrixlusolvemfast(_net_lua, _net_p, _net_n, _net_b, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = listlist_from_net(_net_b, DT_REAL)
    info = _net_info

    # return
    return (b, info)

def rmatrixmixedsolve(*functionargs):
    # unpack inputs
    a, lua, p, n, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixmixedsolve' must be real matrix")
    _net_lua = net_from_listlist(lua, DT_REAL, "ALGLIB: parameter 'lua' of 'xalglib.rmatrixmixedsolve' must be real matrix")
    _net_p = net_from_list(p, DT_INT, "ALGLIB: parameter 'p' of 'xalglib.rmatrixmixedsolve' must be int vector")
    _net_n = n
    _net_b = net_from_list(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.rmatrixmixedsolve' must be real vector")
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.rmatrixmixedsolve(_net_a, _net_lua, _net_p, _net_n, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverreport_from_net(_net_rep)
    x = list_from_net(_net_x, DT_REAL)

    # return
    return (info, rep, x)

def rmatrixmixedsolvem(*functionargs):
    # unpack inputs
    a, lua, p, n, b, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixmixedsolvem' must be real matrix")
    _net_lua = net_from_listlist(lua, DT_REAL, "ALGLIB: parameter 'lua' of 'xalglib.rmatrixmixedsolvem' must be real matrix")
    _net_p = net_from_list(p, DT_INT, "ALGLIB: parameter 'p' of 'xalglib.rmatrixmixedsolvem' must be int vector")
    _net_n = n
    _net_b = net_from_listlist(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.rmatrixmixedsolvem' must be real matrix")
    _net_m = m
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.rmatrixmixedsolvem(_net_a, _net_lua, _net_p, _net_n, _net_b, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverreport_from_net(_net_rep)
    x = listlist_from_net(_net_x, DT_REAL)

    # return
    return (info, rep, x)

def cmatrixsolvem(*functionargs):
    # unpack inputs
    a, n, b, m, rfs = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.cmatrixsolvem' must be complex matrix")
    _net_n = n
    _net_b = net_from_listlist(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.cmatrixsolvem' must be complex matrix")
    _net_m = m
    _net_rfs = rfs
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.cmatrixsolvem(_net_a, _net_n, _net_b, _net_m, _net_rfs)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverreport_from_net(_net_rep)
    x = listlist_from_net(_net_x, DT_COMPLEX)

    # return
    return (info, rep, x)

def smp_cmatrixsolvem(*functionargs):
    # unpack inputs
    a, n, b, m, rfs = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.smp_cmatrixsolvem' must be complex matrix")
    _net_n = n
    _net_b = net_from_listlist(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.smp_cmatrixsolvem' must be complex matrix")
    _net_m = m
    _net_rfs = rfs
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.smp_cmatrixsolvem(_net_a, _net_n, _net_b, _net_m, _net_rfs)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverreport_from_net(_net_rep)
    x = listlist_from_net(_net_x, DT_COMPLEX)

    # return
    return (info, rep, x)

def cmatrixsolvemfast(*functionargs):
    # unpack inputs
    a, n, b, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.cmatrixsolvemfast' must be complex matrix")
    _net_n = n
    _net_b = net_from_listlist(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.cmatrixsolvemfast' must be complex matrix")
    _net_m = m
    try:

        # call function
        _net_b, _net_info = _net_alglib.cmatrixsolvemfast(_net_a, _net_n, _net_b, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = listlist_from_net(_net_b, DT_COMPLEX)
    info = _net_info

    # return
    return (b, info)

def smp_cmatrixsolvemfast(*functionargs):
    # unpack inputs
    a, n, b, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.smp_cmatrixsolvemfast' must be complex matrix")
    _net_n = n
    _net_b = net_from_listlist(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.smp_cmatrixsolvemfast' must be complex matrix")
    _net_m = m
    try:

        # call function
        _net_b, _net_info = _net_alglib.smp_cmatrixsolvemfast(_net_a, _net_n, _net_b, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = listlist_from_net(_net_b, DT_COMPLEX)
    info = _net_info

    # return
    return (b, info)

def cmatrixsolve(*functionargs):
    # unpack inputs
    a, n, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.cmatrixsolve' must be complex matrix")
    _net_n = n
    _net_b = net_from_list(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.cmatrixsolve' must be complex vector")
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.cmatrixsolve(_net_a, _net_n, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverreport_from_net(_net_rep)
    x = list_from_net(_net_x, DT_COMPLEX)

    # return
    return (info, rep, x)

def smp_cmatrixsolve(*functionargs):
    # unpack inputs
    a, n, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.smp_cmatrixsolve' must be complex matrix")
    _net_n = n
    _net_b = net_from_list(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.smp_cmatrixsolve' must be complex vector")
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.smp_cmatrixsolve(_net_a, _net_n, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverreport_from_net(_net_rep)
    x = list_from_net(_net_x, DT_COMPLEX)

    # return
    return (info, rep, x)

def cmatrixsolvefast(*functionargs):
    # unpack inputs
    a, n, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.cmatrixsolvefast' must be complex matrix")
    _net_n = n
    _net_b = net_from_list(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.cmatrixsolvefast' must be complex vector")
    try:

        # call function
        _net_b, _net_info = _net_alglib.cmatrixsolvefast(_net_a, _net_n, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = list_from_net(_net_b, DT_COMPLEX)
    info = _net_info

    # return
    return (b, info)

def smp_cmatrixsolvefast(*functionargs):
    # unpack inputs
    a, n, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.smp_cmatrixsolvefast' must be complex matrix")
    _net_n = n
    _net_b = net_from_list(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.smp_cmatrixsolvefast' must be complex vector")
    try:

        # call function
        _net_b, _net_info = _net_alglib.smp_cmatrixsolvefast(_net_a, _net_n, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = list_from_net(_net_b, DT_COMPLEX)
    info = _net_info

    # return
    return (b, info)

def cmatrixlusolvem(*functionargs):
    # unpack inputs
    lua, p, n, b, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_lua = net_from_listlist(lua, DT_COMPLEX, "ALGLIB: parameter 'lua' of 'xalglib.cmatrixlusolvem' must be complex matrix")
    _net_p = net_from_list(p, DT_INT, "ALGLIB: parameter 'p' of 'xalglib.cmatrixlusolvem' must be int vector")
    _net_n = n
    _net_b = net_from_listlist(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.cmatrixlusolvem' must be complex matrix")
    _net_m = m
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.cmatrixlusolvem(_net_lua, _net_p, _net_n, _net_b, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverreport_from_net(_net_rep)
    x = listlist_from_net(_net_x, DT_COMPLEX)

    # return
    return (info, rep, x)

def smp_cmatrixlusolvem(*functionargs):
    # unpack inputs
    lua, p, n, b, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_lua = net_from_listlist(lua, DT_COMPLEX, "ALGLIB: parameter 'lua' of 'xalglib.smp_cmatrixlusolvem' must be complex matrix")
    _net_p = net_from_list(p, DT_INT, "ALGLIB: parameter 'p' of 'xalglib.smp_cmatrixlusolvem' must be int vector")
    _net_n = n
    _net_b = net_from_listlist(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.smp_cmatrixlusolvem' must be complex matrix")
    _net_m = m
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.smp_cmatrixlusolvem(_net_lua, _net_p, _net_n, _net_b, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverreport_from_net(_net_rep)
    x = listlist_from_net(_net_x, DT_COMPLEX)

    # return
    return (info, rep, x)

def cmatrixlusolvemfast(*functionargs):
    # unpack inputs
    lua, p, n, b, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_lua = net_from_listlist(lua, DT_COMPLEX, "ALGLIB: parameter 'lua' of 'xalglib.cmatrixlusolvemfast' must be complex matrix")
    _net_p = net_from_list(p, DT_INT, "ALGLIB: parameter 'p' of 'xalglib.cmatrixlusolvemfast' must be int vector")
    _net_n = n
    _net_b = net_from_listlist(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.cmatrixlusolvemfast' must be complex matrix")
    _net_m = m
    try:

        # call function
        _net_b, _net_info = _net_alglib.cmatrixlusolvemfast(_net_lua, _net_p, _net_n, _net_b, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = listlist_from_net(_net_b, DT_COMPLEX)
    info = _net_info

    # return
    return (b, info)

def smp_cmatrixlusolvemfast(*functionargs):
    # unpack inputs
    lua, p, n, b, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_lua = net_from_listlist(lua, DT_COMPLEX, "ALGLIB: parameter 'lua' of 'xalglib.smp_cmatrixlusolvemfast' must be complex matrix")
    _net_p = net_from_list(p, DT_INT, "ALGLIB: parameter 'p' of 'xalglib.smp_cmatrixlusolvemfast' must be int vector")
    _net_n = n
    _net_b = net_from_listlist(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.smp_cmatrixlusolvemfast' must be complex matrix")
    _net_m = m
    try:

        # call function
        _net_b, _net_info = _net_alglib.smp_cmatrixlusolvemfast(_net_lua, _net_p, _net_n, _net_b, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = listlist_from_net(_net_b, DT_COMPLEX)
    info = _net_info

    # return
    return (b, info)

def cmatrixlusolve(*functionargs):
    # unpack inputs
    lua, p, n, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_lua = net_from_listlist(lua, DT_COMPLEX, "ALGLIB: parameter 'lua' of 'xalglib.cmatrixlusolve' must be complex matrix")
    _net_p = net_from_list(p, DT_INT, "ALGLIB: parameter 'p' of 'xalglib.cmatrixlusolve' must be int vector")
    _net_n = n
    _net_b = net_from_list(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.cmatrixlusolve' must be complex vector")
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.cmatrixlusolve(_net_lua, _net_p, _net_n, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverreport_from_net(_net_rep)
    x = list_from_net(_net_x, DT_COMPLEX)

    # return
    return (info, rep, x)

def cmatrixlusolvefast(*functionargs):
    # unpack inputs
    lua, p, n, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_lua = net_from_listlist(lua, DT_COMPLEX, "ALGLIB: parameter 'lua' of 'xalglib.cmatrixlusolvefast' must be complex matrix")
    _net_p = net_from_list(p, DT_INT, "ALGLIB: parameter 'p' of 'xalglib.cmatrixlusolvefast' must be int vector")
    _net_n = n
    _net_b = net_from_list(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.cmatrixlusolvefast' must be complex vector")
    try:

        # call function
        _net_b, _net_info = _net_alglib.cmatrixlusolvefast(_net_lua, _net_p, _net_n, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = list_from_net(_net_b, DT_COMPLEX)
    info = _net_info

    # return
    return (b, info)

def cmatrixmixedsolvem(*functionargs):
    # unpack inputs
    a, lua, p, n, b, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.cmatrixmixedsolvem' must be complex matrix")
    _net_lua = net_from_listlist(lua, DT_COMPLEX, "ALGLIB: parameter 'lua' of 'xalglib.cmatrixmixedsolvem' must be complex matrix")
    _net_p = net_from_list(p, DT_INT, "ALGLIB: parameter 'p' of 'xalglib.cmatrixmixedsolvem' must be int vector")
    _net_n = n
    _net_b = net_from_listlist(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.cmatrixmixedsolvem' must be complex matrix")
    _net_m = m
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.cmatrixmixedsolvem(_net_a, _net_lua, _net_p, _net_n, _net_b, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverreport_from_net(_net_rep)
    x = listlist_from_net(_net_x, DT_COMPLEX)

    # return
    return (info, rep, x)

def cmatrixmixedsolve(*functionargs):
    # unpack inputs
    a, lua, p, n, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.cmatrixmixedsolve' must be complex matrix")
    _net_lua = net_from_listlist(lua, DT_COMPLEX, "ALGLIB: parameter 'lua' of 'xalglib.cmatrixmixedsolve' must be complex matrix")
    _net_p = net_from_list(p, DT_INT, "ALGLIB: parameter 'p' of 'xalglib.cmatrixmixedsolve' must be int vector")
    _net_n = n
    _net_b = net_from_list(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.cmatrixmixedsolve' must be complex vector")
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.cmatrixmixedsolve(_net_a, _net_lua, _net_p, _net_n, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverreport_from_net(_net_rep)
    x = list_from_net(_net_x, DT_COMPLEX)

    # return
    return (info, rep, x)

def spdmatrixsolvem(*functionargs):
    # unpack inputs
    a, n, isupper, b, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.spdmatrixsolvem' must be real matrix")
    _net_n = n
    _net_isupper = isupper
    _net_b = net_from_listlist(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.spdmatrixsolvem' must be real matrix")
    _net_m = m
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.spdmatrixsolvem(_net_a, _net_n, _net_isupper, _net_b, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverreport_from_net(_net_rep)
    x = listlist_from_net(_net_x, DT_REAL)

    # return
    return (info, rep, x)

def smp_spdmatrixsolvem(*functionargs):
    # unpack inputs
    a, n, isupper, b, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smp_spdmatrixsolvem' must be real matrix")
    _net_n = n
    _net_isupper = isupper
    _net_b = net_from_listlist(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.smp_spdmatrixsolvem' must be real matrix")
    _net_m = m
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.smp_spdmatrixsolvem(_net_a, _net_n, _net_isupper, _net_b, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverreport_from_net(_net_rep)
    x = listlist_from_net(_net_x, DT_REAL)

    # return
    return (info, rep, x)

def spdmatrixsolvemfast(*functionargs):
    # unpack inputs
    a, n, isupper, b, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.spdmatrixsolvemfast' must be real matrix")
    _net_n = n
    _net_isupper = isupper
    _net_b = net_from_listlist(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.spdmatrixsolvemfast' must be real matrix")
    _net_m = m
    try:

        # call function
        _net_b, _net_info = _net_alglib.spdmatrixsolvemfast(_net_a, _net_n, _net_isupper, _net_b, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = listlist_from_net(_net_b, DT_REAL)
    info = _net_info

    # return
    return (b, info)

def smp_spdmatrixsolvemfast(*functionargs):
    # unpack inputs
    a, n, isupper, b, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smp_spdmatrixsolvemfast' must be real matrix")
    _net_n = n
    _net_isupper = isupper
    _net_b = net_from_listlist(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.smp_spdmatrixsolvemfast' must be real matrix")
    _net_m = m
    try:

        # call function
        _net_b, _net_info = _net_alglib.smp_spdmatrixsolvemfast(_net_a, _net_n, _net_isupper, _net_b, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = listlist_from_net(_net_b, DT_REAL)
    info = _net_info

    # return
    return (b, info)

def spdmatrixsolve(*functionargs):
    # unpack inputs
    a, n, isupper, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.spdmatrixsolve' must be real matrix")
    _net_n = n
    _net_isupper = isupper
    _net_b = net_from_list(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.spdmatrixsolve' must be real vector")
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.spdmatrixsolve(_net_a, _net_n, _net_isupper, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverreport_from_net(_net_rep)
    x = list_from_net(_net_x, DT_REAL)

    # return
    return (info, rep, x)

def smp_spdmatrixsolve(*functionargs):
    # unpack inputs
    a, n, isupper, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smp_spdmatrixsolve' must be real matrix")
    _net_n = n
    _net_isupper = isupper
    _net_b = net_from_list(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.smp_spdmatrixsolve' must be real vector")
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.smp_spdmatrixsolve(_net_a, _net_n, _net_isupper, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverreport_from_net(_net_rep)
    x = list_from_net(_net_x, DT_REAL)

    # return
    return (info, rep, x)

def spdmatrixsolvefast(*functionargs):
    # unpack inputs
    a, n, isupper, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.spdmatrixsolvefast' must be real matrix")
    _net_n = n
    _net_isupper = isupper
    _net_b = net_from_list(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.spdmatrixsolvefast' must be real vector")
    try:

        # call function
        _net_b, _net_info = _net_alglib.spdmatrixsolvefast(_net_a, _net_n, _net_isupper, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = list_from_net(_net_b, DT_REAL)
    info = _net_info

    # return
    return (b, info)

def smp_spdmatrixsolvefast(*functionargs):
    # unpack inputs
    a, n, isupper, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smp_spdmatrixsolvefast' must be real matrix")
    _net_n = n
    _net_isupper = isupper
    _net_b = net_from_list(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.smp_spdmatrixsolvefast' must be real vector")
    try:

        # call function
        _net_b, _net_info = _net_alglib.smp_spdmatrixsolvefast(_net_a, _net_n, _net_isupper, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = list_from_net(_net_b, DT_REAL)
    info = _net_info

    # return
    return (b, info)

def spdmatrixcholeskysolvem(*functionargs):
    # unpack inputs
    cha, n, isupper, b, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_cha = net_from_listlist(cha, DT_REAL, "ALGLIB: parameter 'cha' of 'xalglib.spdmatrixcholeskysolvem' must be real matrix")
    _net_n = n
    _net_isupper = isupper
    _net_b = net_from_listlist(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.spdmatrixcholeskysolvem' must be real matrix")
    _net_m = m
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.spdmatrixcholeskysolvem(_net_cha, _net_n, _net_isupper, _net_b, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverreport_from_net(_net_rep)
    x = listlist_from_net(_net_x, DT_REAL)

    # return
    return (info, rep, x)

def smp_spdmatrixcholeskysolvem(*functionargs):
    # unpack inputs
    cha, n, isupper, b, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_cha = net_from_listlist(cha, DT_REAL, "ALGLIB: parameter 'cha' of 'xalglib.smp_spdmatrixcholeskysolvem' must be real matrix")
    _net_n = n
    _net_isupper = isupper
    _net_b = net_from_listlist(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.smp_spdmatrixcholeskysolvem' must be real matrix")
    _net_m = m
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.smp_spdmatrixcholeskysolvem(_net_cha, _net_n, _net_isupper, _net_b, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverreport_from_net(_net_rep)
    x = listlist_from_net(_net_x, DT_REAL)

    # return
    return (info, rep, x)

def spdmatrixcholeskysolvemfast(*functionargs):
    # unpack inputs
    cha, n, isupper, b, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_cha = net_from_listlist(cha, DT_REAL, "ALGLIB: parameter 'cha' of 'xalglib.spdmatrixcholeskysolvemfast' must be real matrix")
    _net_n = n
    _net_isupper = isupper
    _net_b = net_from_listlist(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.spdmatrixcholeskysolvemfast' must be real matrix")
    _net_m = m
    try:

        # call function
        _net_b, _net_info = _net_alglib.spdmatrixcholeskysolvemfast(_net_cha, _net_n, _net_isupper, _net_b, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = listlist_from_net(_net_b, DT_REAL)
    info = _net_info

    # return
    return (b, info)

def smp_spdmatrixcholeskysolvemfast(*functionargs):
    # unpack inputs
    cha, n, isupper, b, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_cha = net_from_listlist(cha, DT_REAL, "ALGLIB: parameter 'cha' of 'xalglib.smp_spdmatrixcholeskysolvemfast' must be real matrix")
    _net_n = n
    _net_isupper = isupper
    _net_b = net_from_listlist(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.smp_spdmatrixcholeskysolvemfast' must be real matrix")
    _net_m = m
    try:

        # call function
        _net_b, _net_info = _net_alglib.smp_spdmatrixcholeskysolvemfast(_net_cha, _net_n, _net_isupper, _net_b, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = listlist_from_net(_net_b, DT_REAL)
    info = _net_info

    # return
    return (b, info)

def spdmatrixcholeskysolve(*functionargs):
    # unpack inputs
    cha, n, isupper, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_cha = net_from_listlist(cha, DT_REAL, "ALGLIB: parameter 'cha' of 'xalglib.spdmatrixcholeskysolve' must be real matrix")
    _net_n = n
    _net_isupper = isupper
    _net_b = net_from_list(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.spdmatrixcholeskysolve' must be real vector")
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.spdmatrixcholeskysolve(_net_cha, _net_n, _net_isupper, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverreport_from_net(_net_rep)
    x = list_from_net(_net_x, DT_REAL)

    # return
    return (info, rep, x)

def spdmatrixcholeskysolvefast(*functionargs):
    # unpack inputs
    cha, n, isupper, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_cha = net_from_listlist(cha, DT_REAL, "ALGLIB: parameter 'cha' of 'xalglib.spdmatrixcholeskysolvefast' must be real matrix")
    _net_n = n
    _net_isupper = isupper
    _net_b = net_from_list(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.spdmatrixcholeskysolvefast' must be real vector")
    try:

        # call function
        _net_b, _net_info = _net_alglib.spdmatrixcholeskysolvefast(_net_cha, _net_n, _net_isupper, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = list_from_net(_net_b, DT_REAL)
    info = _net_info

    # return
    return (b, info)

def hpdmatrixsolvem(*functionargs):
    # unpack inputs
    a, n, isupper, b, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.hpdmatrixsolvem' must be complex matrix")
    _net_n = n
    _net_isupper = isupper
    _net_b = net_from_listlist(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.hpdmatrixsolvem' must be complex matrix")
    _net_m = m
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.hpdmatrixsolvem(_net_a, _net_n, _net_isupper, _net_b, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverreport_from_net(_net_rep)
    x = listlist_from_net(_net_x, DT_COMPLEX)

    # return
    return (info, rep, x)

def smp_hpdmatrixsolvem(*functionargs):
    # unpack inputs
    a, n, isupper, b, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.smp_hpdmatrixsolvem' must be complex matrix")
    _net_n = n
    _net_isupper = isupper
    _net_b = net_from_listlist(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.smp_hpdmatrixsolvem' must be complex matrix")
    _net_m = m
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.smp_hpdmatrixsolvem(_net_a, _net_n, _net_isupper, _net_b, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverreport_from_net(_net_rep)
    x = listlist_from_net(_net_x, DT_COMPLEX)

    # return
    return (info, rep, x)

def hpdmatrixsolvemfast(*functionargs):
    # unpack inputs
    a, n, isupper, b, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.hpdmatrixsolvemfast' must be complex matrix")
    _net_n = n
    _net_isupper = isupper
    _net_b = net_from_listlist(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.hpdmatrixsolvemfast' must be complex matrix")
    _net_m = m
    try:

        # call function
        _net_b, _net_info = _net_alglib.hpdmatrixsolvemfast(_net_a, _net_n, _net_isupper, _net_b, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = listlist_from_net(_net_b, DT_COMPLEX)
    info = _net_info

    # return
    return (b, info)

def smp_hpdmatrixsolvemfast(*functionargs):
    # unpack inputs
    a, n, isupper, b, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.smp_hpdmatrixsolvemfast' must be complex matrix")
    _net_n = n
    _net_isupper = isupper
    _net_b = net_from_listlist(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.smp_hpdmatrixsolvemfast' must be complex matrix")
    _net_m = m
    try:

        # call function
        _net_b, _net_info = _net_alglib.smp_hpdmatrixsolvemfast(_net_a, _net_n, _net_isupper, _net_b, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = listlist_from_net(_net_b, DT_COMPLEX)
    info = _net_info

    # return
    return (b, info)

def hpdmatrixsolve(*functionargs):
    # unpack inputs
    a, n, isupper, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.hpdmatrixsolve' must be complex matrix")
    _net_n = n
    _net_isupper = isupper
    _net_b = net_from_list(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.hpdmatrixsolve' must be complex vector")
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.hpdmatrixsolve(_net_a, _net_n, _net_isupper, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverreport_from_net(_net_rep)
    x = list_from_net(_net_x, DT_COMPLEX)

    # return
    return (info, rep, x)

def smp_hpdmatrixsolve(*functionargs):
    # unpack inputs
    a, n, isupper, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.smp_hpdmatrixsolve' must be complex matrix")
    _net_n = n
    _net_isupper = isupper
    _net_b = net_from_list(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.smp_hpdmatrixsolve' must be complex vector")
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.smp_hpdmatrixsolve(_net_a, _net_n, _net_isupper, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverreport_from_net(_net_rep)
    x = list_from_net(_net_x, DT_COMPLEX)

    # return
    return (info, rep, x)

def hpdmatrixsolvefast(*functionargs):
    # unpack inputs
    a, n, isupper, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.hpdmatrixsolvefast' must be complex matrix")
    _net_n = n
    _net_isupper = isupper
    _net_b = net_from_list(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.hpdmatrixsolvefast' must be complex vector")
    try:

        # call function
        _net_b, _net_info = _net_alglib.hpdmatrixsolvefast(_net_a, _net_n, _net_isupper, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = list_from_net(_net_b, DT_COMPLEX)
    info = _net_info

    # return
    return (b, info)

def smp_hpdmatrixsolvefast(*functionargs):
    # unpack inputs
    a, n, isupper, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.smp_hpdmatrixsolvefast' must be complex matrix")
    _net_n = n
    _net_isupper = isupper
    _net_b = net_from_list(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.smp_hpdmatrixsolvefast' must be complex vector")
    try:

        # call function
        _net_b, _net_info = _net_alglib.smp_hpdmatrixsolvefast(_net_a, _net_n, _net_isupper, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = list_from_net(_net_b, DT_COMPLEX)
    info = _net_info

    # return
    return (b, info)

def hpdmatrixcholeskysolvem(*functionargs):
    # unpack inputs
    cha, n, isupper, b, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_cha = net_from_listlist(cha, DT_COMPLEX, "ALGLIB: parameter 'cha' of 'xalglib.hpdmatrixcholeskysolvem' must be complex matrix")
    _net_n = n
    _net_isupper = isupper
    _net_b = net_from_listlist(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.hpdmatrixcholeskysolvem' must be complex matrix")
    _net_m = m
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.hpdmatrixcholeskysolvem(_net_cha, _net_n, _net_isupper, _net_b, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverreport_from_net(_net_rep)
    x = listlist_from_net(_net_x, DT_COMPLEX)

    # return
    return (info, rep, x)

def smp_hpdmatrixcholeskysolvem(*functionargs):
    # unpack inputs
    cha, n, isupper, b, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_cha = net_from_listlist(cha, DT_COMPLEX, "ALGLIB: parameter 'cha' of 'xalglib.smp_hpdmatrixcholeskysolvem' must be complex matrix")
    _net_n = n
    _net_isupper = isupper
    _net_b = net_from_listlist(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.smp_hpdmatrixcholeskysolvem' must be complex matrix")
    _net_m = m
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.smp_hpdmatrixcholeskysolvem(_net_cha, _net_n, _net_isupper, _net_b, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverreport_from_net(_net_rep)
    x = listlist_from_net(_net_x, DT_COMPLEX)

    # return
    return (info, rep, x)

def hpdmatrixcholeskysolvemfast(*functionargs):
    # unpack inputs
    cha, n, isupper, b, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_cha = net_from_listlist(cha, DT_COMPLEX, "ALGLIB: parameter 'cha' of 'xalglib.hpdmatrixcholeskysolvemfast' must be complex matrix")
    _net_n = n
    _net_isupper = isupper
    _net_b = net_from_listlist(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.hpdmatrixcholeskysolvemfast' must be complex matrix")
    _net_m = m
    try:

        # call function
        _net_b, _net_info = _net_alglib.hpdmatrixcholeskysolvemfast(_net_cha, _net_n, _net_isupper, _net_b, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = listlist_from_net(_net_b, DT_COMPLEX)
    info = _net_info

    # return
    return (b, info)

def smp_hpdmatrixcholeskysolvemfast(*functionargs):
    # unpack inputs
    cha, n, isupper, b, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_cha = net_from_listlist(cha, DT_COMPLEX, "ALGLIB: parameter 'cha' of 'xalglib.smp_hpdmatrixcholeskysolvemfast' must be complex matrix")
    _net_n = n
    _net_isupper = isupper
    _net_b = net_from_listlist(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.smp_hpdmatrixcholeskysolvemfast' must be complex matrix")
    _net_m = m
    try:

        # call function
        _net_b, _net_info = _net_alglib.smp_hpdmatrixcholeskysolvemfast(_net_cha, _net_n, _net_isupper, _net_b, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = listlist_from_net(_net_b, DT_COMPLEX)
    info = _net_info

    # return
    return (b, info)

def hpdmatrixcholeskysolve(*functionargs):
    # unpack inputs
    cha, n, isupper, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_cha = net_from_listlist(cha, DT_COMPLEX, "ALGLIB: parameter 'cha' of 'xalglib.hpdmatrixcholeskysolve' must be complex matrix")
    _net_n = n
    _net_isupper = isupper
    _net_b = net_from_list(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.hpdmatrixcholeskysolve' must be complex vector")
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.hpdmatrixcholeskysolve(_net_cha, _net_n, _net_isupper, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverreport_from_net(_net_rep)
    x = list_from_net(_net_x, DT_COMPLEX)

    # return
    return (info, rep, x)

def hpdmatrixcholeskysolvefast(*functionargs):
    # unpack inputs
    cha, n, isupper, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_cha = net_from_listlist(cha, DT_COMPLEX, "ALGLIB: parameter 'cha' of 'xalglib.hpdmatrixcholeskysolvefast' must be complex matrix")
    _net_n = n
    _net_isupper = isupper
    _net_b = net_from_list(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.hpdmatrixcholeskysolvefast' must be complex vector")
    try:

        # call function
        _net_b, _net_info = _net_alglib.hpdmatrixcholeskysolvefast(_net_cha, _net_n, _net_isupper, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = list_from_net(_net_b, DT_COMPLEX)
    info = _net_info

    # return
    return (b, info)

def rmatrixsolvels(*functionargs):
    # unpack inputs
    a, nrows, ncols, b, threshold = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixsolvels' must be real matrix")
    _net_nrows = nrows
    _net_ncols = ncols
    _net_b = net_from_list(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.rmatrixsolvels' must be real vector")
    _net_threshold = threshold
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.rmatrixsolvels(_net_a, _net_nrows, _net_ncols, _net_b, _net_threshold)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverlsreport_from_net(_net_rep)
    x = list_from_net(_net_x, DT_REAL)

    # return
    return (info, rep, x)

def smp_rmatrixsolvels(*functionargs):
    # unpack inputs
    a, nrows, ncols, b, threshold = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smp_rmatrixsolvels' must be real matrix")
    _net_nrows = nrows
    _net_ncols = ncols
    _net_b = net_from_list(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.smp_rmatrixsolvels' must be real vector")
    _net_threshold = threshold
    try:

        # call function
        _net_info, _net_rep, _net_x = _net_alglib.smp_rmatrixsolvels(_net_a, _net_nrows, _net_ncols, _net_b, _net_threshold)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = densesolverlsreport_from_net(_net_rep)
    x = list_from_net(_net_x, DT_REAL)

    # return
    return (info, rep, x)



class normestimatorstate(object):
    def __init__(self,ptr):
        self.ptr = ptr
def normestimatorcreate(*functionargs):
    # unpack inputs
    m, n, nstart, nits = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    _net_nstart = nstart
    _net_nits = nits
    try:

        # call function
        _net_state = _net_alglib.normestimatorcreate(_net_m, _net_n, _net_nstart, _net_nits)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = normestimatorstate(_net_state)

    # return
    return state

def normestimatorsetseed(*functionargs):
    # unpack inputs
    state, seedval = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_seedval = seedval
    try:

        # call function
        _net_alglib.normestimatorsetseed(_net_state, _net_seedval)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def normestimatorestimatesparse(*functionargs):
    # unpack inputs
    state, a = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_a = a.ptr
    try:

        # call function
        _net_alglib.normestimatorestimatesparse(_net_state, _net_a)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def normestimatorresults(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_nrm = _net_alglib.normestimatorresults(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    nrm = _net_nrm

    # return
    return nrm



class linlsqrstate(object):
    def __init__(self,ptr):
        self.ptr = ptr


class linlsqrreport(object):
    def __init__(self):
        self.iterationscount = 0
        self.nmv = 0
        self.terminationtype = 0


def net_from_linlsqrreport(x,v):
    x.iterationscount = int(v.iterationscount)
    x.nmv = int(v.nmv)
    x.terminationtype = int(v.terminationtype)
    return




def linlsqrreport_from_net(x):
    r = linlsqrreport()
    r.iterationscount = x.iterationscount
    r.nmv = x.nmv
    r.terminationtype = x.terminationtype
    return r


def linlsqrcreate(*functionargs):
    # unpack inputs
    m, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    _net_n = n
    try:

        # call function
        _net_state = _net_alglib.linlsqrcreate(_net_m, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = linlsqrstate(_net_state)

    # return
    return state

def linlsqrsetprecunit(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_alglib.linlsqrsetprecunit(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def linlsqrsetprecdiag(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_alglib.linlsqrsetprecdiag(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def linlsqrsetlambdai(*functionargs):
    # unpack inputs
    state, lambdai = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_lambdai = lambdai
    try:

        # call function
        _net_alglib.linlsqrsetlambdai(_net_state, _net_lambdai)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def linlsqrsolvesparse(*functionargs):
    # unpack inputs
    state, a, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_a = a.ptr
    _net_b = net_from_list(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.linlsqrsolvesparse' must be real vector")
    try:

        # call function
        _net_alglib.linlsqrsolvesparse(_net_state, _net_a, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def linlsqrsetcond(*functionargs):
    # unpack inputs
    state, epsa, epsb, maxits = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_epsa = epsa
    _net_epsb = epsb
    _net_maxits = maxits
    try:

        # call function
        _net_alglib.linlsqrsetcond(_net_state, _net_epsa, _net_epsb, _net_maxits)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def linlsqrresults(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_x, _net_rep = _net_alglib.linlsqrresults(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = list_from_net(_net_x, DT_REAL)
    rep = linlsqrreport_from_net(_net_rep)

    # return
    return (x, rep)

def linlsqrsetxrep(*functionargs):
    # unpack inputs
    state, needxrep = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_needxrep = needxrep
    try:

        # call function
        _net_alglib.linlsqrsetxrep(_net_state, _net_needxrep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return



class mincgstate(object):
    def __init__(self,ptr):
        self.ptr = ptr


class mincgreport(object):
    def __init__(self):
        self.iterationscount = 0
        self.nfev = 0
        self.varidx = 0
        self.terminationtype = 0


def net_from_mincgreport(x,v):
    x.iterationscount = int(v.iterationscount)
    x.nfev = int(v.nfev)
    x.varidx = int(v.varidx)
    x.terminationtype = int(v.terminationtype)
    return




def mincgreport_from_net(x):
    r = mincgreport()
    r.iterationscount = x.iterationscount
    r.nfev = x.nfev
    r.varidx = x.varidx
    r.terminationtype = x.terminationtype
    return r


def mincgcreate(*functionargs):
    # unpack inputs
    if len(functionargs)==2:
        # full-form call
        n, x = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        x,  = functionargs
        n = check_equality_and_get([safe_len("'mincgcreate': incorrect parameters",x)],"Error while calling 'mincgcreate': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'mincgcreate': function must have 2 or 1 parameters")

    # convert to .NET types
    _net_n = n
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.mincgcreate' must be real vector")
    try:

        # call function
        _net_state = _net_alglib.mincgcreate(_net_n, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = mincgstate(_net_state)

    # return
    return state

def mincgcreatef(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        n, x, diffstep = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        x, diffstep = functionargs
        n = check_equality_and_get([safe_len("'mincgcreatef': incorrect parameters",x)],"Error while calling 'mincgcreatef': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'mincgcreatef': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_n = n
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.mincgcreatef' must be real vector")
    _net_diffstep = diffstep
    try:

        # call function
        _net_state = _net_alglib.mincgcreatef(_net_n, _net_x, _net_diffstep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = mincgstate(_net_state)

    # return
    return state

def mincgsetcond(*functionargs):
    # unpack inputs
    state, epsg, epsf, epsx, maxits = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_epsg = epsg
    _net_epsf = epsf
    _net_epsx = epsx
    _net_maxits = maxits
    try:

        # call function
        _net_alglib.mincgsetcond(_net_state, _net_epsg, _net_epsf, _net_epsx, _net_maxits)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mincgsetscale(*functionargs):
    # unpack inputs
    state, s = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_s = net_from_list(s, DT_REAL, "ALGLIB: parameter 's' of 'xalglib.mincgsetscale' must be real vector")
    try:

        # call function
        _net_alglib.mincgsetscale(_net_state, _net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mincgsetxrep(*functionargs):
    # unpack inputs
    state, needxrep = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_needxrep = needxrep
    try:

        # call function
        _net_alglib.mincgsetxrep(_net_state, _net_needxrep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mincgsetcgtype(*functionargs):
    # unpack inputs
    state, cgtype = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_cgtype = cgtype
    try:

        # call function
        _net_alglib.mincgsetcgtype(_net_state, _net_cgtype)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mincgsetstpmax(*functionargs):
    # unpack inputs
    state, stpmax = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_stpmax = stpmax
    try:

        # call function
        _net_alglib.mincgsetstpmax(_net_state, _net_stpmax)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mincgsuggeststep(*functionargs):
    # unpack inputs
    state, stp = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_stp = stp
    try:

        # call function
        _net_alglib.mincgsuggeststep(_net_state, _net_stp)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mincgsetprecdefault(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_alglib.mincgsetprecdefault(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mincgsetprecdiag(*functionargs):
    # unpack inputs
    state, d = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_d = net_from_list(d, DT_REAL, "ALGLIB: parameter 'd' of 'xalglib.mincgsetprecdiag' must be real vector")
    try:

        # call function
        _net_alglib.mincgsetprecdiag(_net_state, _net_d)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mincgsetprecscale(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_alglib.mincgsetprecscale(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return



def mincgoptimize_f(state, func, rep = None, param = None):
    _net_x  = state.ptr.x
    _py_x = create_real_vector(_net_x.GetLength(0))
    while True:
        try:
            result = _net_alglib.mincgiteration(state.ptr)
        except _net_alglib.alglibexception as e:
            raise RuntimeError(e.msg)
        if not result:
            break
        if state.ptr.needf:
            copy_net_to_list(_net_x, _py_x, DT_REAL)

            fvalue = func(_py_x, param)
            state.ptr.f = fvalue
            continue
        if state.ptr.xupdated:
            if not (rep is None):
                copy_net_to_list(_net_x, _py_x, DT_REAL)
                rep(_py_x, state.ptr.f, param)
            continue
        raise RuntimeError("ALGLIB: error in 'mincgoptimize' (some derivatives were not provided?)")
    return


def mincgoptimize_g(state, grad, rep = None, param = None):
    _net_x  = state.ptr.x
    _py_x = create_real_vector(_net_x.GetLength(0))
    _net_g  = state.ptr.g
    _py_g = create_real_vector(_net_g.GetLength(0))
    while True:
        try:
            result = _net_alglib.mincgiteration(state.ptr)
        except _net_alglib.alglibexception as e:
            raise RuntimeError(e.msg)
        if not result:
            break
        if state.ptr.needfg:
            copy_net_to_list(_net_x, _py_x, DT_REAL)

            fvalue = grad(_py_x, _py_g, param)
            state.ptr.f = fvalue
            copy_list_to_net(_py_g, _net_g, DT_REAL)
            continue
        if state.ptr.xupdated:
            if not (rep is None):
                copy_net_to_list(_net_x, _py_x, DT_REAL)
                rep(_py_x, state.ptr.f, param)
            continue
        raise RuntimeError("ALGLIB: error in 'mincgoptimize' (some derivatives were not provided?)")
    return


def mincgresults(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_x, _net_rep = _net_alglib.mincgresults(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = list_from_net(_net_x, DT_REAL)
    rep = mincgreport_from_net(_net_rep)

    # return
    return (x, rep)

def mincgresultsbuf(*functionargs):
    # unpack inputs
    state, x, rep = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.mincgresultsbuf' must be real vector")
    _net_rep = _net_alglib.mincgreport()
    net_from_mincgreport(_net_rep, rep)
    try:

        # call function
        _net_x, _net_rep = _net_alglib.mincgresultsbuf(_net_state, _net_x, _net_rep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = list_from_net(_net_x, DT_REAL)
    rep = mincgreport_from_net(_net_rep)

    # return
    return (x, rep)

def mincgrestartfrom(*functionargs):
    # unpack inputs
    state, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.mincgrestartfrom' must be real vector")
    try:

        # call function
        _net_alglib.mincgrestartfrom(_net_state, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mincgrequesttermination(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_alglib.mincgrequesttermination(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mincgsetgradientcheck(*functionargs):
    # unpack inputs
    state, teststep = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_teststep = teststep
    try:

        # call function
        _net_alglib.mincgsetgradientcheck(_net_state, _net_teststep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return



class minbleicstate(object):
    def __init__(self,ptr):
        self.ptr = ptr


class minbleicreport(object):
    def __init__(self):
        self.iterationscount = 0
        self.nfev = 0
        self.varidx = 0
        self.terminationtype = 0
        self.debugeqerr = 0
        self.debugfs = 0
        self.debugff = 0
        self.debugdx = 0
        self.debugfeasqpits = 0
        self.debugfeasgpaits = 0
        self.inneriterationscount = 0
        self.outeriterationscount = 0


def net_from_minbleicreport(x,v):
    x.iterationscount = int(v.iterationscount)
    x.nfev = int(v.nfev)
    x.varidx = int(v.varidx)
    x.terminationtype = int(v.terminationtype)
    x.debugeqerr = float(v.debugeqerr)
    x.debugfs = float(v.debugfs)
    x.debugff = float(v.debugff)
    x.debugdx = float(v.debugdx)
    x.debugfeasqpits = int(v.debugfeasqpits)
    x.debugfeasgpaits = int(v.debugfeasgpaits)
    x.inneriterationscount = int(v.inneriterationscount)
    x.outeriterationscount = int(v.outeriterationscount)
    return




def minbleicreport_from_net(x):
    r = minbleicreport()
    r.iterationscount = x.iterationscount
    r.nfev = x.nfev
    r.varidx = x.varidx
    r.terminationtype = x.terminationtype
    r.debugeqerr = x.debugeqerr
    r.debugfs = x.debugfs
    r.debugff = x.debugff
    r.debugdx = x.debugdx
    r.debugfeasqpits = x.debugfeasqpits
    r.debugfeasgpaits = x.debugfeasgpaits
    r.inneriterationscount = x.inneriterationscount
    r.outeriterationscount = x.outeriterationscount
    return r


def minbleiccreate(*functionargs):
    # unpack inputs
    if len(functionargs)==2:
        # full-form call
        n, x = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        x,  = functionargs
        n = check_equality_and_get([safe_len("'minbleiccreate': incorrect parameters",x)],"Error while calling 'minbleiccreate': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'minbleiccreate': function must have 2 or 1 parameters")

    # convert to .NET types
    _net_n = n
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.minbleiccreate' must be real vector")
    try:

        # call function
        _net_state = _net_alglib.minbleiccreate(_net_n, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = minbleicstate(_net_state)

    # return
    return state

def minbleiccreatef(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        n, x, diffstep = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        x, diffstep = functionargs
        n = check_equality_and_get([safe_len("'minbleiccreatef': incorrect parameters",x)],"Error while calling 'minbleiccreatef': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'minbleiccreatef': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_n = n
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.minbleiccreatef' must be real vector")
    _net_diffstep = diffstep
    try:

        # call function
        _net_state = _net_alglib.minbleiccreatef(_net_n, _net_x, _net_diffstep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = minbleicstate(_net_state)

    # return
    return state

def minbleicsetbc(*functionargs):
    # unpack inputs
    state, bndl, bndu = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_bndl = net_from_list(bndl, DT_REAL, "ALGLIB: parameter 'bndl' of 'xalglib.minbleicsetbc' must be real vector")
    _net_bndu = net_from_list(bndu, DT_REAL, "ALGLIB: parameter 'bndu' of 'xalglib.minbleicsetbc' must be real vector")
    try:

        # call function
        _net_alglib.minbleicsetbc(_net_state, _net_bndl, _net_bndu)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minbleicsetlc(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        state, c, ct, k = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        state, c, ct = functionargs
        k = check_equality_and_get([safe_rows("'minbleicsetlc': incorrect parameters",c), safe_len("'minbleicsetlc': incorrect parameters",ct)],"Error while calling 'minbleicsetlc': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'minbleicsetlc': function must have 4 or 3 parameters")

    # convert to .NET types
    _net_state = state.ptr
    _net_c = net_from_listlist(c, DT_REAL, "ALGLIB: parameter 'c' of 'xalglib.minbleicsetlc' must be real matrix")
    _net_ct = net_from_list(ct, DT_INT, "ALGLIB: parameter 'ct' of 'xalglib.minbleicsetlc' must be int vector")
    _net_k = k
    try:

        # call function
        _net_alglib.minbleicsetlc(_net_state, _net_c, _net_ct, _net_k)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minbleicsetcond(*functionargs):
    # unpack inputs
    state, epsg, epsf, epsx, maxits = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_epsg = epsg
    _net_epsf = epsf
    _net_epsx = epsx
    _net_maxits = maxits
    try:

        # call function
        _net_alglib.minbleicsetcond(_net_state, _net_epsg, _net_epsf, _net_epsx, _net_maxits)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minbleicsetscale(*functionargs):
    # unpack inputs
    state, s = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_s = net_from_list(s, DT_REAL, "ALGLIB: parameter 's' of 'xalglib.minbleicsetscale' must be real vector")
    try:

        # call function
        _net_alglib.minbleicsetscale(_net_state, _net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minbleicsetprecdefault(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_alglib.minbleicsetprecdefault(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minbleicsetprecdiag(*functionargs):
    # unpack inputs
    state, d = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_d = net_from_list(d, DT_REAL, "ALGLIB: parameter 'd' of 'xalglib.minbleicsetprecdiag' must be real vector")
    try:

        # call function
        _net_alglib.minbleicsetprecdiag(_net_state, _net_d)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minbleicsetprecscale(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_alglib.minbleicsetprecscale(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minbleicsetxrep(*functionargs):
    # unpack inputs
    state, needxrep = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_needxrep = needxrep
    try:

        # call function
        _net_alglib.minbleicsetxrep(_net_state, _net_needxrep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minbleicsetstpmax(*functionargs):
    # unpack inputs
    state, stpmax = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_stpmax = stpmax
    try:

        # call function
        _net_alglib.minbleicsetstpmax(_net_state, _net_stpmax)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return



def minbleicoptimize_f(state, func, rep = None, param = None):
    _net_x  = state.ptr.x
    _py_x = create_real_vector(_net_x.GetLength(0))
    while True:
        try:
            result = _net_alglib.minbleiciteration(state.ptr)
        except _net_alglib.alglibexception as e:
            raise RuntimeError(e.msg)
        if not result:
            break
        if state.ptr.needf:
            copy_net_to_list(_net_x, _py_x, DT_REAL)

            fvalue = func(_py_x, param)
            state.ptr.f = fvalue
            continue
        if state.ptr.xupdated:
            if not (rep is None):
                copy_net_to_list(_net_x, _py_x, DT_REAL)
                rep(_py_x, state.ptr.f, param)
            continue
        raise RuntimeError("ALGLIB: error in 'minbleicoptimize' (some derivatives were not provided?)")
    return


def minbleicoptimize_g(state, grad, rep = None, param = None):
    _net_x  = state.ptr.x
    _py_x = create_real_vector(_net_x.GetLength(0))
    _net_g  = state.ptr.g
    _py_g = create_real_vector(_net_g.GetLength(0))
    while True:
        try:
            result = _net_alglib.minbleiciteration(state.ptr)
        except _net_alglib.alglibexception as e:
            raise RuntimeError(e.msg)
        if not result:
            break
        if state.ptr.needfg:
            copy_net_to_list(_net_x, _py_x, DT_REAL)

            fvalue = grad(_py_x, _py_g, param)
            state.ptr.f = fvalue
            copy_list_to_net(_py_g, _net_g, DT_REAL)
            continue
        if state.ptr.xupdated:
            if not (rep is None):
                copy_net_to_list(_net_x, _py_x, DT_REAL)
                rep(_py_x, state.ptr.f, param)
            continue
        raise RuntimeError("ALGLIB: error in 'minbleicoptimize' (some derivatives were not provided?)")
    return


def minbleicresults(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_x, _net_rep = _net_alglib.minbleicresults(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = list_from_net(_net_x, DT_REAL)
    rep = minbleicreport_from_net(_net_rep)

    # return
    return (x, rep)

def minbleicresultsbuf(*functionargs):
    # unpack inputs
    state, x, rep = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.minbleicresultsbuf' must be real vector")
    _net_rep = _net_alglib.minbleicreport()
    net_from_minbleicreport(_net_rep, rep)
    try:

        # call function
        _net_x, _net_rep = _net_alglib.minbleicresultsbuf(_net_state, _net_x, _net_rep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = list_from_net(_net_x, DT_REAL)
    rep = minbleicreport_from_net(_net_rep)

    # return
    return (x, rep)

def minbleicrestartfrom(*functionargs):
    # unpack inputs
    state, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.minbleicrestartfrom' must be real vector")
    try:

        # call function
        _net_alglib.minbleicrestartfrom(_net_state, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minbleicrequesttermination(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_alglib.minbleicrequesttermination(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minbleicsetgradientcheck(*functionargs):
    # unpack inputs
    state, teststep = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_teststep = teststep
    try:

        # call function
        _net_alglib.minbleicsetgradientcheck(_net_state, _net_teststep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return



class minqpstate(object):
    def __init__(self,ptr):
        self.ptr = ptr


class minqpreport(object):
    def __init__(self):
        self.inneriterationscount = 0
        self.outeriterationscount = 0
        self.nmv = 0
        self.ncholesky = 0
        self.terminationtype = 0


def net_from_minqpreport(x,v):
    x.inneriterationscount = int(v.inneriterationscount)
    x.outeriterationscount = int(v.outeriterationscount)
    x.nmv = int(v.nmv)
    x.ncholesky = int(v.ncholesky)
    x.terminationtype = int(v.terminationtype)
    return




def minqpreport_from_net(x):
    r = minqpreport()
    r.inneriterationscount = x.inneriterationscount
    r.outeriterationscount = x.outeriterationscount
    r.nmv = x.nmv
    r.ncholesky = x.ncholesky
    r.terminationtype = x.terminationtype
    return r


def minqpcreate(*functionargs):
    # unpack inputs
    n,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    try:

        # call function
        _net_state = _net_alglib.minqpcreate(_net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = minqpstate(_net_state)

    # return
    return state

def minqpsetlinearterm(*functionargs):
    # unpack inputs
    state, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_b = net_from_list(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.minqpsetlinearterm' must be real vector")
    try:

        # call function
        _net_alglib.minqpsetlinearterm(_net_state, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minqpsetquadraticterm(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        state, a, isupper = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        state, a = functionargs
        isupper = check_equality_and_get([False],"Error while calling 'minqpsetquadraticterm': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'minqpsetquadraticterm': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_state = state.ptr
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.minqpsetquadraticterm' must be real matrix")
    if friendly_form and (not _net_alglib.ap.issymmetric(_net_a)):
        raise ValueError("ALGLIB: parameter 'a' of 'xalglib.minqpsetquadraticterm' must be symmetric matrix")
    _net_isupper = isupper
    try:

        # call function
        _net_alglib.minqpsetquadraticterm(_net_state, _net_a, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minqpsetquadratictermsparse(*functionargs):
    # unpack inputs
    state, a, isupper = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_a = a.ptr
    _net_isupper = isupper
    try:

        # call function
        _net_alglib.minqpsetquadratictermsparse(_net_state, _net_a, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minqpsetstartingpoint(*functionargs):
    # unpack inputs
    state, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.minqpsetstartingpoint' must be real vector")
    try:

        # call function
        _net_alglib.minqpsetstartingpoint(_net_state, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minqpsetorigin(*functionargs):
    # unpack inputs
    state, xorigin = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_xorigin = net_from_list(xorigin, DT_REAL, "ALGLIB: parameter 'xorigin' of 'xalglib.minqpsetorigin' must be real vector")
    try:

        # call function
        _net_alglib.minqpsetorigin(_net_state, _net_xorigin)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minqpsetscale(*functionargs):
    # unpack inputs
    state, s = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_s = net_from_list(s, DT_REAL, "ALGLIB: parameter 's' of 'xalglib.minqpsetscale' must be real vector")
    try:

        # call function
        _net_alglib.minqpsetscale(_net_state, _net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minqpsetscaleautodiag(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_alglib.minqpsetscaleautodiag(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minqpsetalgocholesky(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_alglib.minqpsetalgocholesky(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minqpsetalgobleic(*functionargs):
    # unpack inputs
    state, epsg, epsf, epsx, maxits = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_epsg = epsg
    _net_epsf = epsf
    _net_epsx = epsx
    _net_maxits = maxits
    try:

        # call function
        _net_alglib.minqpsetalgobleic(_net_state, _net_epsg, _net_epsf, _net_epsx, _net_maxits)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minqpsetalgodenseaul(*functionargs):
    # unpack inputs
    state, epsx, rho, itscnt = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_epsx = epsx
    _net_rho = rho
    _net_itscnt = itscnt
    try:

        # call function
        _net_alglib.minqpsetalgodenseaul(_net_state, _net_epsx, _net_rho, _net_itscnt)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minqpsetalgoquickqp(*functionargs):
    # unpack inputs
    state, epsg, epsf, epsx, maxouterits, usenewton = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_epsg = epsg
    _net_epsf = epsf
    _net_epsx = epsx
    _net_maxouterits = maxouterits
    _net_usenewton = usenewton
    try:

        # call function
        _net_alglib.minqpsetalgoquickqp(_net_state, _net_epsg, _net_epsf, _net_epsx, _net_maxouterits, _net_usenewton)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minqpsetbc(*functionargs):
    # unpack inputs
    state, bndl, bndu = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_bndl = net_from_list(bndl, DT_REAL, "ALGLIB: parameter 'bndl' of 'xalglib.minqpsetbc' must be real vector")
    _net_bndu = net_from_list(bndu, DT_REAL, "ALGLIB: parameter 'bndu' of 'xalglib.minqpsetbc' must be real vector")
    try:

        # call function
        _net_alglib.minqpsetbc(_net_state, _net_bndl, _net_bndu)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minqpsetlc(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        state, c, ct, k = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        state, c, ct = functionargs
        k = check_equality_and_get([safe_rows("'minqpsetlc': incorrect parameters",c), safe_len("'minqpsetlc': incorrect parameters",ct)],"Error while calling 'minqpsetlc': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'minqpsetlc': function must have 4 or 3 parameters")

    # convert to .NET types
    _net_state = state.ptr
    _net_c = net_from_listlist(c, DT_REAL, "ALGLIB: parameter 'c' of 'xalglib.minqpsetlc' must be real matrix")
    _net_ct = net_from_list(ct, DT_INT, "ALGLIB: parameter 'ct' of 'xalglib.minqpsetlc' must be int vector")
    _net_k = k
    try:

        # call function
        _net_alglib.minqpsetlc(_net_state, _net_c, _net_ct, _net_k)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minqpsetlcsparse(*functionargs):
    # unpack inputs
    state, c, ct, k = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_c = c.ptr
    _net_ct = net_from_list(ct, DT_INT, "ALGLIB: parameter 'ct' of 'xalglib.minqpsetlcsparse' must be int vector")
    _net_k = k
    try:

        # call function
        _net_alglib.minqpsetlcsparse(_net_state, _net_c, _net_ct, _net_k)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minqpsetlcmixed(*functionargs):
    # unpack inputs
    state, densec, densect, densek, sparsec, sparsect, sparsek = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_densec = net_from_listlist(densec, DT_REAL, "ALGLIB: parameter 'densec' of 'xalglib.minqpsetlcmixed' must be real matrix")
    _net_densect = net_from_list(densect, DT_INT, "ALGLIB: parameter 'densect' of 'xalglib.minqpsetlcmixed' must be int vector")
    _net_densek = densek
    _net_sparsec = sparsec.ptr
    _net_sparsect = net_from_list(sparsect, DT_INT, "ALGLIB: parameter 'sparsect' of 'xalglib.minqpsetlcmixed' must be int vector")
    _net_sparsek = sparsek
    try:

        # call function
        _net_alglib.minqpsetlcmixed(_net_state, _net_densec, _net_densect, _net_densek, _net_sparsec, _net_sparsect, _net_sparsek)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minqpoptimize(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_alglib.minqpoptimize(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minqpresults(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_x, _net_rep = _net_alglib.minqpresults(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = list_from_net(_net_x, DT_REAL)
    rep = minqpreport_from_net(_net_rep)

    # return
    return (x, rep)

def minqpresultsbuf(*functionargs):
    # unpack inputs
    state, x, rep = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.minqpresultsbuf' must be real vector")
    _net_rep = _net_alglib.minqpreport()
    net_from_minqpreport(_net_rep, rep)
    try:

        # call function
        _net_x, _net_rep = _net_alglib.minqpresultsbuf(_net_state, _net_x, _net_rep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = list_from_net(_net_x, DT_REAL)
    rep = minqpreport_from_net(_net_rep)

    # return
    return (x, rep)



class minnlcstate(object):
    def __init__(self,ptr):
        self.ptr = ptr


class minnlcreport(object):
    def __init__(self):
        self.iterationscount = 0
        self.nfev = 0
        self.varidx = 0
        self.funcidx = 0
        self.terminationtype = 0
        self.dbgphase0its = 0


def net_from_minnlcreport(x,v):
    x.iterationscount = int(v.iterationscount)
    x.nfev = int(v.nfev)
    x.varidx = int(v.varidx)
    x.funcidx = int(v.funcidx)
    x.terminationtype = int(v.terminationtype)
    x.dbgphase0its = int(v.dbgphase0its)
    return




def minnlcreport_from_net(x):
    r = minnlcreport()
    r.iterationscount = x.iterationscount
    r.nfev = x.nfev
    r.varidx = x.varidx
    r.funcidx = x.funcidx
    r.terminationtype = x.terminationtype
    r.dbgphase0its = x.dbgphase0its
    return r


def minnlccreate(*functionargs):
    # unpack inputs
    if len(functionargs)==2:
        # full-form call
        n, x = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        x,  = functionargs
        n = check_equality_and_get([safe_len("'minnlccreate': incorrect parameters",x)],"Error while calling 'minnlccreate': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'minnlccreate': function must have 2 or 1 parameters")

    # convert to .NET types
    _net_n = n
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.minnlccreate' must be real vector")
    try:

        # call function
        _net_state = _net_alglib.minnlccreate(_net_n, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = minnlcstate(_net_state)

    # return
    return state

def minnlccreatef(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        n, x, diffstep = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        x, diffstep = functionargs
        n = check_equality_and_get([safe_len("'minnlccreatef': incorrect parameters",x)],"Error while calling 'minnlccreatef': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'minnlccreatef': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_n = n
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.minnlccreatef' must be real vector")
    _net_diffstep = diffstep
    try:

        # call function
        _net_state = _net_alglib.minnlccreatef(_net_n, _net_x, _net_diffstep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = minnlcstate(_net_state)

    # return
    return state

def minnlcsetbc(*functionargs):
    # unpack inputs
    state, bndl, bndu = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_bndl = net_from_list(bndl, DT_REAL, "ALGLIB: parameter 'bndl' of 'xalglib.minnlcsetbc' must be real vector")
    _net_bndu = net_from_list(bndu, DT_REAL, "ALGLIB: parameter 'bndu' of 'xalglib.minnlcsetbc' must be real vector")
    try:

        # call function
        _net_alglib.minnlcsetbc(_net_state, _net_bndl, _net_bndu)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minnlcsetlc(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        state, c, ct, k = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        state, c, ct = functionargs
        k = check_equality_and_get([safe_rows("'minnlcsetlc': incorrect parameters",c), safe_len("'minnlcsetlc': incorrect parameters",ct)],"Error while calling 'minnlcsetlc': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'minnlcsetlc': function must have 4 or 3 parameters")

    # convert to .NET types
    _net_state = state.ptr
    _net_c = net_from_listlist(c, DT_REAL, "ALGLIB: parameter 'c' of 'xalglib.minnlcsetlc' must be real matrix")
    _net_ct = net_from_list(ct, DT_INT, "ALGLIB: parameter 'ct' of 'xalglib.minnlcsetlc' must be int vector")
    _net_k = k
    try:

        # call function
        _net_alglib.minnlcsetlc(_net_state, _net_c, _net_ct, _net_k)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minnlcsetnlc(*functionargs):
    # unpack inputs
    state, nlec, nlic = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_nlec = nlec
    _net_nlic = nlic
    try:

        # call function
        _net_alglib.minnlcsetnlc(_net_state, _net_nlec, _net_nlic)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minnlcsetcond(*functionargs):
    # unpack inputs
    state, epsg, epsf, epsx, maxits = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_epsg = epsg
    _net_epsf = epsf
    _net_epsx = epsx
    _net_maxits = maxits
    try:

        # call function
        _net_alglib.minnlcsetcond(_net_state, _net_epsg, _net_epsf, _net_epsx, _net_maxits)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minnlcsetscale(*functionargs):
    # unpack inputs
    state, s = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_s = net_from_list(s, DT_REAL, "ALGLIB: parameter 's' of 'xalglib.minnlcsetscale' must be real vector")
    try:

        # call function
        _net_alglib.minnlcsetscale(_net_state, _net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minnlcsetprecinexact(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_alglib.minnlcsetprecinexact(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minnlcsetprecexactlowrank(*functionargs):
    # unpack inputs
    state, updatefreq = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_updatefreq = updatefreq
    try:

        # call function
        _net_alglib.minnlcsetprecexactlowrank(_net_state, _net_updatefreq)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minnlcsetprecexactrobust(*functionargs):
    # unpack inputs
    state, updatefreq = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_updatefreq = updatefreq
    try:

        # call function
        _net_alglib.minnlcsetprecexactrobust(_net_state, _net_updatefreq)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minnlcsetprecnone(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_alglib.minnlcsetprecnone(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minnlcsetstpmax(*functionargs):
    # unpack inputs
    state, stpmax = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_stpmax = stpmax
    try:

        # call function
        _net_alglib.minnlcsetstpmax(_net_state, _net_stpmax)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minnlcsetalgoaul(*functionargs):
    # unpack inputs
    state, rho, itscnt = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_rho = rho
    _net_itscnt = itscnt
    try:

        # call function
        _net_alglib.minnlcsetalgoaul(_net_state, _net_rho, _net_itscnt)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minnlcsetxrep(*functionargs):
    # unpack inputs
    state, needxrep = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_needxrep = needxrep
    try:

        # call function
        _net_alglib.minnlcsetxrep(_net_state, _net_needxrep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return



def minnlcoptimize_v(state, fvec, rep = None, param = None):
    _net_x  = state.ptr.x
    _py_x = create_real_vector(_net_x.GetLength(0))
    _net_fi  = state.ptr.fi
    _py_fi = create_real_vector(_net_fi.GetLength(0))
    while True:
        try:
            result = _net_alglib.minnlciteration(state.ptr)
        except _net_alglib.alglibexception as e:
            raise RuntimeError(e.msg)
        if not result:
            break
        if state.ptr.needfi:
            copy_net_to_list(_net_x, _py_x, DT_REAL)

            fvec(_py_x, _py_fi, param)
            copy_list_to_net(_py_fi, _net_fi, DT_REAL)
            continue
        if state.ptr.xupdated:
            if not (rep is None):
                copy_net_to_list(_net_x, _py_x, DT_REAL)
                rep(_py_x, state.ptr.f, param)
            continue
        raise RuntimeError("ALGLIB: error in 'minnlcoptimize' (some derivatives were not provided?)")
    return


def minnlcoptimize_j(state, jac, rep = None, param = None):
    _net_x  = state.ptr.x
    _py_x = create_real_vector(_net_x.GetLength(0))
    _net_fi  = state.ptr.fi
    _py_fi = create_real_vector(_net_fi.GetLength(0))
    _net_j  = state.ptr.j
    _py_j = create_real_matrix(_net_j.GetLength(0),_net_j.GetLength(1))
    while True:
        try:
            result = _net_alglib.minnlciteration(state.ptr)
        except _net_alglib.alglibexception as e:
            raise RuntimeError(e.msg)
        if not result:
            break
        if state.ptr.needfij:
            copy_net_to_list(_net_x, _py_x, DT_REAL)

            jac(_py_x, _py_fi, _py_j, param)
            copy_list_to_net(_py_fi, _net_fi, DT_REAL)
            copy_listlist_to_net(_py_j, _net_j, DT_REAL)
            continue
        if state.ptr.xupdated:
            if not (rep is None):
                copy_net_to_list(_net_x, _py_x, DT_REAL)
                rep(_py_x, state.ptr.f, param)
            continue
        raise RuntimeError("ALGLIB: error in 'minnlcoptimize' (some derivatives were not provided?)")
    return


def minnlcresults(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_x, _net_rep = _net_alglib.minnlcresults(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = list_from_net(_net_x, DT_REAL)
    rep = minnlcreport_from_net(_net_rep)

    # return
    return (x, rep)

def minnlcresultsbuf(*functionargs):
    # unpack inputs
    state, x, rep = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.minnlcresultsbuf' must be real vector")
    _net_rep = _net_alglib.minnlcreport()
    net_from_minnlcreport(_net_rep, rep)
    try:

        # call function
        _net_x, _net_rep = _net_alglib.minnlcresultsbuf(_net_state, _net_x, _net_rep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = list_from_net(_net_x, DT_REAL)
    rep = minnlcreport_from_net(_net_rep)

    # return
    return (x, rep)

def minnlcrestartfrom(*functionargs):
    # unpack inputs
    state, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.minnlcrestartfrom' must be real vector")
    try:

        # call function
        _net_alglib.minnlcrestartfrom(_net_state, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minnlcsetgradientcheck(*functionargs):
    # unpack inputs
    state, teststep = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_teststep = teststep
    try:

        # call function
        _net_alglib.minnlcsetgradientcheck(_net_state, _net_teststep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return



class minbcstate(object):
    def __init__(self,ptr):
        self.ptr = ptr


class minbcreport(object):
    def __init__(self):
        self.iterationscount = 0
        self.nfev = 0
        self.varidx = 0
        self.terminationtype = 0


def net_from_minbcreport(x,v):
    x.iterationscount = int(v.iterationscount)
    x.nfev = int(v.nfev)
    x.varidx = int(v.varidx)
    x.terminationtype = int(v.terminationtype)
    return




def minbcreport_from_net(x):
    r = minbcreport()
    r.iterationscount = x.iterationscount
    r.nfev = x.nfev
    r.varidx = x.varidx
    r.terminationtype = x.terminationtype
    return r


def minbccreate(*functionargs):
    # unpack inputs
    if len(functionargs)==2:
        # full-form call
        n, x = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        x,  = functionargs
        n = check_equality_and_get([safe_len("'minbccreate': incorrect parameters",x)],"Error while calling 'minbccreate': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'minbccreate': function must have 2 or 1 parameters")

    # convert to .NET types
    _net_n = n
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.minbccreate' must be real vector")
    try:

        # call function
        _net_state = _net_alglib.minbccreate(_net_n, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = minbcstate(_net_state)

    # return
    return state

def minbccreatef(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        n, x, diffstep = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        x, diffstep = functionargs
        n = check_equality_and_get([safe_len("'minbccreatef': incorrect parameters",x)],"Error while calling 'minbccreatef': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'minbccreatef': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_n = n
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.minbccreatef' must be real vector")
    _net_diffstep = diffstep
    try:

        # call function
        _net_state = _net_alglib.minbccreatef(_net_n, _net_x, _net_diffstep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = minbcstate(_net_state)

    # return
    return state

def minbcsetbc(*functionargs):
    # unpack inputs
    state, bndl, bndu = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_bndl = net_from_list(bndl, DT_REAL, "ALGLIB: parameter 'bndl' of 'xalglib.minbcsetbc' must be real vector")
    _net_bndu = net_from_list(bndu, DT_REAL, "ALGLIB: parameter 'bndu' of 'xalglib.minbcsetbc' must be real vector")
    try:

        # call function
        _net_alglib.minbcsetbc(_net_state, _net_bndl, _net_bndu)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minbcsetcond(*functionargs):
    # unpack inputs
    state, epsg, epsf, epsx, maxits = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_epsg = epsg
    _net_epsf = epsf
    _net_epsx = epsx
    _net_maxits = maxits
    try:

        # call function
        _net_alglib.minbcsetcond(_net_state, _net_epsg, _net_epsf, _net_epsx, _net_maxits)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minbcsetscale(*functionargs):
    # unpack inputs
    state, s = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_s = net_from_list(s, DT_REAL, "ALGLIB: parameter 's' of 'xalglib.minbcsetscale' must be real vector")
    try:

        # call function
        _net_alglib.minbcsetscale(_net_state, _net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minbcsetprecdefault(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_alglib.minbcsetprecdefault(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minbcsetprecdiag(*functionargs):
    # unpack inputs
    state, d = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_d = net_from_list(d, DT_REAL, "ALGLIB: parameter 'd' of 'xalglib.minbcsetprecdiag' must be real vector")
    try:

        # call function
        _net_alglib.minbcsetprecdiag(_net_state, _net_d)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minbcsetprecscale(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_alglib.minbcsetprecscale(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minbcsetxrep(*functionargs):
    # unpack inputs
    state, needxrep = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_needxrep = needxrep
    try:

        # call function
        _net_alglib.minbcsetxrep(_net_state, _net_needxrep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minbcsetstpmax(*functionargs):
    # unpack inputs
    state, stpmax = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_stpmax = stpmax
    try:

        # call function
        _net_alglib.minbcsetstpmax(_net_state, _net_stpmax)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return



def minbcoptimize_f(state, func, rep = None, param = None):
    _net_x  = state.ptr.x
    _py_x = create_real_vector(_net_x.GetLength(0))
    while True:
        try:
            result = _net_alglib.minbciteration(state.ptr)
        except _net_alglib.alglibexception as e:
            raise RuntimeError(e.msg)
        if not result:
            break
        if state.ptr.needf:
            copy_net_to_list(_net_x, _py_x, DT_REAL)

            fvalue = func(_py_x, param)
            state.ptr.f = fvalue
            continue
        if state.ptr.xupdated:
            if not (rep is None):
                copy_net_to_list(_net_x, _py_x, DT_REAL)
                rep(_py_x, state.ptr.f, param)
            continue
        raise RuntimeError("ALGLIB: error in 'minbcoptimize' (some derivatives were not provided?)")
    return


def minbcoptimize_g(state, grad, rep = None, param = None):
    _net_x  = state.ptr.x
    _py_x = create_real_vector(_net_x.GetLength(0))
    _net_g  = state.ptr.g
    _py_g = create_real_vector(_net_g.GetLength(0))
    while True:
        try:
            result = _net_alglib.minbciteration(state.ptr)
        except _net_alglib.alglibexception as e:
            raise RuntimeError(e.msg)
        if not result:
            break
        if state.ptr.needfg:
            copy_net_to_list(_net_x, _py_x, DT_REAL)

            fvalue = grad(_py_x, _py_g, param)
            state.ptr.f = fvalue
            copy_list_to_net(_py_g, _net_g, DT_REAL)
            continue
        if state.ptr.xupdated:
            if not (rep is None):
                copy_net_to_list(_net_x, _py_x, DT_REAL)
                rep(_py_x, state.ptr.f, param)
            continue
        raise RuntimeError("ALGLIB: error in 'minbcoptimize' (some derivatives were not provided?)")
    return


def minbcresults(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_x, _net_rep = _net_alglib.minbcresults(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = list_from_net(_net_x, DT_REAL)
    rep = minbcreport_from_net(_net_rep)

    # return
    return (x, rep)

def minbcresultsbuf(*functionargs):
    # unpack inputs
    state, x, rep = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.minbcresultsbuf' must be real vector")
    _net_rep = _net_alglib.minbcreport()
    net_from_minbcreport(_net_rep, rep)
    try:

        # call function
        _net_x, _net_rep = _net_alglib.minbcresultsbuf(_net_state, _net_x, _net_rep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = list_from_net(_net_x, DT_REAL)
    rep = minbcreport_from_net(_net_rep)

    # return
    return (x, rep)

def minbcrestartfrom(*functionargs):
    # unpack inputs
    state, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.minbcrestartfrom' must be real vector")
    try:

        # call function
        _net_alglib.minbcrestartfrom(_net_state, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minbcrequesttermination(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_alglib.minbcrequesttermination(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minbcsetgradientcheck(*functionargs):
    # unpack inputs
    state, teststep = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_teststep = teststep
    try:

        # call function
        _net_alglib.minbcsetgradientcheck(_net_state, _net_teststep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return



class minnsstate(object):
    def __init__(self,ptr):
        self.ptr = ptr


class minnsreport(object):
    def __init__(self):
        self.iterationscount = 0
        self.nfev = 0
        self.cerr = 0
        self.lcerr = 0
        self.nlcerr = 0
        self.terminationtype = 0
        self.varidx = 0
        self.funcidx = 0


def net_from_minnsreport(x,v):
    x.iterationscount = int(v.iterationscount)
    x.nfev = int(v.nfev)
    x.cerr = float(v.cerr)
    x.lcerr = float(v.lcerr)
    x.nlcerr = float(v.nlcerr)
    x.terminationtype = int(v.terminationtype)
    x.varidx = int(v.varidx)
    x.funcidx = int(v.funcidx)
    return




def minnsreport_from_net(x):
    r = minnsreport()
    r.iterationscount = x.iterationscount
    r.nfev = x.nfev
    r.cerr = x.cerr
    r.lcerr = x.lcerr
    r.nlcerr = x.nlcerr
    r.terminationtype = x.terminationtype
    r.varidx = x.varidx
    r.funcidx = x.funcidx
    return r


def minnscreate(*functionargs):
    # unpack inputs
    if len(functionargs)==2:
        # full-form call
        n, x = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        x,  = functionargs
        n = check_equality_and_get([safe_len("'minnscreate': incorrect parameters",x)],"Error while calling 'minnscreate': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'minnscreate': function must have 2 or 1 parameters")

    # convert to .NET types
    _net_n = n
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.minnscreate' must be real vector")
    try:

        # call function
        _net_state = _net_alglib.minnscreate(_net_n, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = minnsstate(_net_state)

    # return
    return state

def minnscreatef(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        n, x, diffstep = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        x, diffstep = functionargs
        n = check_equality_and_get([safe_len("'minnscreatef': incorrect parameters",x)],"Error while calling 'minnscreatef': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'minnscreatef': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_n = n
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.minnscreatef' must be real vector")
    _net_diffstep = diffstep
    try:

        # call function
        _net_state = _net_alglib.minnscreatef(_net_n, _net_x, _net_diffstep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = minnsstate(_net_state)

    # return
    return state

def minnssetbc(*functionargs):
    # unpack inputs
    state, bndl, bndu = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_bndl = net_from_list(bndl, DT_REAL, "ALGLIB: parameter 'bndl' of 'xalglib.minnssetbc' must be real vector")
    _net_bndu = net_from_list(bndu, DT_REAL, "ALGLIB: parameter 'bndu' of 'xalglib.minnssetbc' must be real vector")
    try:

        # call function
        _net_alglib.minnssetbc(_net_state, _net_bndl, _net_bndu)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minnssetlc(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        state, c, ct, k = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        state, c, ct = functionargs
        k = check_equality_and_get([safe_rows("'minnssetlc': incorrect parameters",c), safe_len("'minnssetlc': incorrect parameters",ct)],"Error while calling 'minnssetlc': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'minnssetlc': function must have 4 or 3 parameters")

    # convert to .NET types
    _net_state = state.ptr
    _net_c = net_from_listlist(c, DT_REAL, "ALGLIB: parameter 'c' of 'xalglib.minnssetlc' must be real matrix")
    _net_ct = net_from_list(ct, DT_INT, "ALGLIB: parameter 'ct' of 'xalglib.minnssetlc' must be int vector")
    _net_k = k
    try:

        # call function
        _net_alglib.minnssetlc(_net_state, _net_c, _net_ct, _net_k)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minnssetnlc(*functionargs):
    # unpack inputs
    state, nlec, nlic = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_nlec = nlec
    _net_nlic = nlic
    try:

        # call function
        _net_alglib.minnssetnlc(_net_state, _net_nlec, _net_nlic)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minnssetcond(*functionargs):
    # unpack inputs
    state, epsx, maxits = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_epsx = epsx
    _net_maxits = maxits
    try:

        # call function
        _net_alglib.minnssetcond(_net_state, _net_epsx, _net_maxits)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minnssetscale(*functionargs):
    # unpack inputs
    state, s = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_s = net_from_list(s, DT_REAL, "ALGLIB: parameter 's' of 'xalglib.minnssetscale' must be real vector")
    try:

        # call function
        _net_alglib.minnssetscale(_net_state, _net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minnssetalgoags(*functionargs):
    # unpack inputs
    state, radius, penalty = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_radius = radius
    _net_penalty = penalty
    try:

        # call function
        _net_alglib.minnssetalgoags(_net_state, _net_radius, _net_penalty)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minnssetxrep(*functionargs):
    # unpack inputs
    state, needxrep = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_needxrep = needxrep
    try:

        # call function
        _net_alglib.minnssetxrep(_net_state, _net_needxrep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minnsrequesttermination(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_alglib.minnsrequesttermination(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return



def minnsoptimize_v(state, fvec, rep = None, param = None):
    _net_x  = state.ptr.x
    _py_x = create_real_vector(_net_x.GetLength(0))
    _net_fi  = state.ptr.fi
    _py_fi = create_real_vector(_net_fi.GetLength(0))
    while True:
        try:
            result = _net_alglib.minnsiteration(state.ptr)
        except _net_alglib.alglibexception as e:
            raise RuntimeError(e.msg)
        if not result:
            break
        if state.ptr.needfi:
            copy_net_to_list(_net_x, _py_x, DT_REAL)

            fvec(_py_x, _py_fi, param)
            copy_list_to_net(_py_fi, _net_fi, DT_REAL)
            continue
        if state.ptr.xupdated:
            if not (rep is None):
                copy_net_to_list(_net_x, _py_x, DT_REAL)
                rep(_py_x, state.ptr.f, param)
            continue
        raise RuntimeError("ALGLIB: error in 'minnsoptimize' (some derivatives were not provided?)")
    return


def minnsoptimize_j(state, jac, rep = None, param = None):
    _net_x  = state.ptr.x
    _py_x = create_real_vector(_net_x.GetLength(0))
    _net_fi  = state.ptr.fi
    _py_fi = create_real_vector(_net_fi.GetLength(0))
    _net_j  = state.ptr.j
    _py_j = create_real_matrix(_net_j.GetLength(0),_net_j.GetLength(1))
    while True:
        try:
            result = _net_alglib.minnsiteration(state.ptr)
        except _net_alglib.alglibexception as e:
            raise RuntimeError(e.msg)
        if not result:
            break
        if state.ptr.needfij:
            copy_net_to_list(_net_x, _py_x, DT_REAL)

            jac(_py_x, _py_fi, _py_j, param)
            copy_list_to_net(_py_fi, _net_fi, DT_REAL)
            copy_listlist_to_net(_py_j, _net_j, DT_REAL)
            continue
        if state.ptr.xupdated:
            if not (rep is None):
                copy_net_to_list(_net_x, _py_x, DT_REAL)
                rep(_py_x, state.ptr.f, param)
            continue
        raise RuntimeError("ALGLIB: error in 'minnsoptimize' (some derivatives were not provided?)")
    return


def minnsresults(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_x, _net_rep = _net_alglib.minnsresults(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = list_from_net(_net_x, DT_REAL)
    rep = minnsreport_from_net(_net_rep)

    # return
    return (x, rep)

def minnsresultsbuf(*functionargs):
    # unpack inputs
    state, x, rep = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.minnsresultsbuf' must be real vector")
    _net_rep = _net_alglib.minnsreport()
    net_from_minnsreport(_net_rep, rep)
    try:

        # call function
        _net_x, _net_rep = _net_alglib.minnsresultsbuf(_net_state, _net_x, _net_rep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = list_from_net(_net_x, DT_REAL)
    rep = minnsreport_from_net(_net_rep)

    # return
    return (x, rep)

def minnsrestartfrom(*functionargs):
    # unpack inputs
    state, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.minnsrestartfrom' must be real vector")
    try:

        # call function
        _net_alglib.minnsrestartfrom(_net_state, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return



class minasastate(object):
    def __init__(self,ptr):
        self.ptr = ptr


class minasareport(object):
    def __init__(self):
        self.iterationscount = 0
        self.nfev = 0
        self.terminationtype = 0
        self.activeconstraints = 0


def net_from_minasareport(x,v):
    x.iterationscount = int(v.iterationscount)
    x.nfev = int(v.nfev)
    x.terminationtype = int(v.terminationtype)
    x.activeconstraints = int(v.activeconstraints)
    return




def minasareport_from_net(x):
    r = minasareport()
    r.iterationscount = x.iterationscount
    r.nfev = x.nfev
    r.terminationtype = x.terminationtype
    r.activeconstraints = x.activeconstraints
    return r


def minlbfgssetdefaultpreconditioner(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_alglib.minlbfgssetdefaultpreconditioner(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minlbfgssetcholeskypreconditioner(*functionargs):
    # unpack inputs
    state, p, isupper = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_p = net_from_listlist(p, DT_REAL, "ALGLIB: parameter 'p' of 'xalglib.minlbfgssetcholeskypreconditioner' must be real matrix")
    _net_isupper = isupper
    try:

        # call function
        _net_alglib.minlbfgssetcholeskypreconditioner(_net_state, _net_p, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minbleicsetbarrierwidth(*functionargs):
    # unpack inputs
    state, mu = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_mu = mu
    try:

        # call function
        _net_alglib.minbleicsetbarrierwidth(_net_state, _net_mu)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minbleicsetbarrierdecay(*functionargs):
    # unpack inputs
    state, mudecay = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_mudecay = mudecay
    try:

        # call function
        _net_alglib.minbleicsetbarrierdecay(_net_state, _net_mudecay)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minasacreate(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        n, x, bndl, bndu = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        x, bndl, bndu = functionargs
        n = check_equality_and_get([safe_len("'minasacreate': incorrect parameters",x), safe_len("'minasacreate': incorrect parameters",bndl), safe_len("'minasacreate': incorrect parameters",bndu)],"Error while calling 'minasacreate': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'minasacreate': function must have 4 or 3 parameters")

    # convert to .NET types
    _net_n = n
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.minasacreate' must be real vector")
    _net_bndl = net_from_list(bndl, DT_REAL, "ALGLIB: parameter 'bndl' of 'xalglib.minasacreate' must be real vector")
    _net_bndu = net_from_list(bndu, DT_REAL, "ALGLIB: parameter 'bndu' of 'xalglib.minasacreate' must be real vector")
    try:

        # call function
        _net_state = _net_alglib.minasacreate(_net_n, _net_x, _net_bndl, _net_bndu)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = minasastate(_net_state)

    # return
    return state

def minasasetcond(*functionargs):
    # unpack inputs
    state, epsg, epsf, epsx, maxits = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_epsg = epsg
    _net_epsf = epsf
    _net_epsx = epsx
    _net_maxits = maxits
    try:

        # call function
        _net_alglib.minasasetcond(_net_state, _net_epsg, _net_epsf, _net_epsx, _net_maxits)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minasasetxrep(*functionargs):
    # unpack inputs
    state, needxrep = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_needxrep = needxrep
    try:

        # call function
        _net_alglib.minasasetxrep(_net_state, _net_needxrep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minasasetalgorithm(*functionargs):
    # unpack inputs
    state, algotype = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_algotype = algotype
    try:

        # call function
        _net_alglib.minasasetalgorithm(_net_state, _net_algotype)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minasasetstpmax(*functionargs):
    # unpack inputs
    state, stpmax = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_stpmax = stpmax
    try:

        # call function
        _net_alglib.minasasetstpmax(_net_state, _net_stpmax)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return



def minasaoptimize_g(state, grad, rep = None, param = None):
    _net_x  = state.ptr.x
    _py_x = create_real_vector(_net_x.GetLength(0))
    _net_g  = state.ptr.g
    _py_g = create_real_vector(_net_g.GetLength(0))
    while True:
        try:
            result = _net_alglib.minasaiteration(state.ptr)
        except _net_alglib.alglibexception as e:
            raise RuntimeError(e.msg)
        if not result:
            break
        if state.ptr.needfg:
            copy_net_to_list(_net_x, _py_x, DT_REAL)

            fvalue = grad(_py_x, _py_g, param)
            state.ptr.f = fvalue
            copy_list_to_net(_py_g, _net_g, DT_REAL)
            continue
        if state.ptr.xupdated:
            if not (rep is None):
                copy_net_to_list(_net_x, _py_x, DT_REAL)
                rep(_py_x, state.ptr.f, param)
            continue
        raise RuntimeError("ALGLIB: error in 'minasaoptimize' (some derivatives were not provided?)")
    return


def minasaresults(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_x, _net_rep = _net_alglib.minasaresults(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = list_from_net(_net_x, DT_REAL)
    rep = minasareport_from_net(_net_rep)

    # return
    return (x, rep)

def minasaresultsbuf(*functionargs):
    # unpack inputs
    state, x, rep = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.minasaresultsbuf' must be real vector")
    _net_rep = _net_alglib.minasareport()
    net_from_minasareport(_net_rep, rep)
    try:

        # call function
        _net_x, _net_rep = _net_alglib.minasaresultsbuf(_net_state, _net_x, _net_rep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = list_from_net(_net_x, DT_REAL)
    rep = minasareport_from_net(_net_rep)

    # return
    return (x, rep)

def minasarestartfrom(*functionargs):
    # unpack inputs
    state, x, bndl, bndu = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.minasarestartfrom' must be real vector")
    _net_bndl = net_from_list(bndl, DT_REAL, "ALGLIB: parameter 'bndl' of 'xalglib.minasarestartfrom' must be real vector")
    _net_bndu = net_from_list(bndu, DT_REAL, "ALGLIB: parameter 'bndu' of 'xalglib.minasarestartfrom' must be real vector")
    try:

        # call function
        _net_alglib.minasarestartfrom(_net_state, _net_x, _net_bndl, _net_bndu)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return



class minlmstate(object):
    def __init__(self,ptr):
        self.ptr = ptr


class minlmreport(object):
    def __init__(self):
        self.iterationscount = 0
        self.terminationtype = 0
        self.funcidx = 0
        self.varidx = 0
        self.nfunc = 0
        self.njac = 0
        self.ngrad = 0
        self.nhess = 0
        self.ncholesky = 0


def net_from_minlmreport(x,v):
    x.iterationscount = int(v.iterationscount)
    x.terminationtype = int(v.terminationtype)
    x.funcidx = int(v.funcidx)
    x.varidx = int(v.varidx)
    x.nfunc = int(v.nfunc)
    x.njac = int(v.njac)
    x.ngrad = int(v.ngrad)
    x.nhess = int(v.nhess)
    x.ncholesky = int(v.ncholesky)
    return




def minlmreport_from_net(x):
    r = minlmreport()
    r.iterationscount = x.iterationscount
    r.terminationtype = x.terminationtype
    r.funcidx = x.funcidx
    r.varidx = x.varidx
    r.nfunc = x.nfunc
    r.njac = x.njac
    r.ngrad = x.ngrad
    r.nhess = x.nhess
    r.ncholesky = x.ncholesky
    return r


def minlmcreatevj(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        n, m, x = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        m, x = functionargs
        n = check_equality_and_get([safe_len("'minlmcreatevj': incorrect parameters",x)],"Error while calling 'minlmcreatevj': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'minlmcreatevj': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_n = n
    _net_m = m
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.minlmcreatevj' must be real vector")
    try:

        # call function
        _net_state = _net_alglib.minlmcreatevj(_net_n, _net_m, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = minlmstate(_net_state)

    # return
    return state

def minlmcreatev(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        n, m, x, diffstep = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        m, x, diffstep = functionargs
        n = check_equality_and_get([safe_len("'minlmcreatev': incorrect parameters",x)],"Error while calling 'minlmcreatev': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'minlmcreatev': function must have 4 or 3 parameters")

    # convert to .NET types
    _net_n = n
    _net_m = m
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.minlmcreatev' must be real vector")
    _net_diffstep = diffstep
    try:

        # call function
        _net_state = _net_alglib.minlmcreatev(_net_n, _net_m, _net_x, _net_diffstep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = minlmstate(_net_state)

    # return
    return state

def minlmcreatefgh(*functionargs):
    # unpack inputs
    if len(functionargs)==2:
        # full-form call
        n, x = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        x,  = functionargs
        n = check_equality_and_get([safe_len("'minlmcreatefgh': incorrect parameters",x)],"Error while calling 'minlmcreatefgh': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'minlmcreatefgh': function must have 2 or 1 parameters")

    # convert to .NET types
    _net_n = n
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.minlmcreatefgh' must be real vector")
    try:

        # call function
        _net_state = _net_alglib.minlmcreatefgh(_net_n, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = minlmstate(_net_state)

    # return
    return state

def minlmsetcond(*functionargs):
    # unpack inputs
    state, epsx, maxits = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_epsx = epsx
    _net_maxits = maxits
    try:

        # call function
        _net_alglib.minlmsetcond(_net_state, _net_epsx, _net_maxits)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minlmsetxrep(*functionargs):
    # unpack inputs
    state, needxrep = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_needxrep = needxrep
    try:

        # call function
        _net_alglib.minlmsetxrep(_net_state, _net_needxrep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minlmsetstpmax(*functionargs):
    # unpack inputs
    state, stpmax = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_stpmax = stpmax
    try:

        # call function
        _net_alglib.minlmsetstpmax(_net_state, _net_stpmax)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minlmsetscale(*functionargs):
    # unpack inputs
    state, s = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_s = net_from_list(s, DT_REAL, "ALGLIB: parameter 's' of 'xalglib.minlmsetscale' must be real vector")
    try:

        # call function
        _net_alglib.minlmsetscale(_net_state, _net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minlmsetbc(*functionargs):
    # unpack inputs
    state, bndl, bndu = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_bndl = net_from_list(bndl, DT_REAL, "ALGLIB: parameter 'bndl' of 'xalglib.minlmsetbc' must be real vector")
    _net_bndu = net_from_list(bndu, DT_REAL, "ALGLIB: parameter 'bndu' of 'xalglib.minlmsetbc' must be real vector")
    try:

        # call function
        _net_alglib.minlmsetbc(_net_state, _net_bndl, _net_bndu)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minlmsetlc(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        state, c, ct, k = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        state, c, ct = functionargs
        k = check_equality_and_get([safe_rows("'minlmsetlc': incorrect parameters",c), safe_len("'minlmsetlc': incorrect parameters",ct)],"Error while calling 'minlmsetlc': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'minlmsetlc': function must have 4 or 3 parameters")

    # convert to .NET types
    _net_state = state.ptr
    _net_c = net_from_listlist(c, DT_REAL, "ALGLIB: parameter 'c' of 'xalglib.minlmsetlc' must be real matrix")
    _net_ct = net_from_list(ct, DT_INT, "ALGLIB: parameter 'ct' of 'xalglib.minlmsetlc' must be int vector")
    _net_k = k
    try:

        # call function
        _net_alglib.minlmsetlc(_net_state, _net_c, _net_ct, _net_k)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minlmsetacctype(*functionargs):
    # unpack inputs
    state, acctype = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_acctype = acctype
    try:

        # call function
        _net_alglib.minlmsetacctype(_net_state, _net_acctype)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return



def minlmoptimize_v(state, fvec, rep = None, param = None):
    _net_x  = state.ptr.x
    _py_x = create_real_vector(_net_x.GetLength(0))
    _net_fi  = state.ptr.fi
    _py_fi = create_real_vector(_net_fi.GetLength(0))
    while True:
        try:
            result = _net_alglib.minlmiteration(state.ptr)
        except _net_alglib.alglibexception as e:
            raise RuntimeError(e.msg)
        if not result:
            break
        if state.ptr.needfi:
            copy_net_to_list(_net_x, _py_x, DT_REAL)

            fvec(_py_x, _py_fi, param)
            copy_list_to_net(_py_fi, _net_fi, DT_REAL)
            continue
        if state.ptr.xupdated:
            if not (rep is None):
                copy_net_to_list(_net_x, _py_x, DT_REAL)
                rep(_py_x, state.ptr.f, param)
            continue
        raise RuntimeError("ALGLIB: error in 'minlmoptimize' (some derivatives were not provided?)")
    return


def minlmoptimize_vj(state, fvec, jac, rep = None, param = None):
    _net_x  = state.ptr.x
    _py_x = create_real_vector(_net_x.GetLength(0))
    _net_fi  = state.ptr.fi
    _py_fi = create_real_vector(_net_fi.GetLength(0))
    _net_j  = state.ptr.j
    _py_j = create_real_matrix(_net_j.GetLength(0),_net_j.GetLength(1))
    while True:
        try:
            result = _net_alglib.minlmiteration(state.ptr)
        except _net_alglib.alglibexception as e:
            raise RuntimeError(e.msg)
        if not result:
            break
        if state.ptr.needfi:
            copy_net_to_list(_net_x, _py_x, DT_REAL)

            fvec(_py_x, _py_fi, param)
            copy_list_to_net(_py_fi, _net_fi, DT_REAL)
            continue
        if state.ptr.needfij:
            copy_net_to_list(_net_x, _py_x, DT_REAL)

            jac(_py_x, _py_fi, _py_j, param)
            copy_list_to_net(_py_fi, _net_fi, DT_REAL)
            copy_listlist_to_net(_py_j, _net_j, DT_REAL)
            continue
        if state.ptr.xupdated:
            if not (rep is None):
                copy_net_to_list(_net_x, _py_x, DT_REAL)
                rep(_py_x, state.ptr.f, param)
            continue
        raise RuntimeError("ALGLIB: error in 'minlmoptimize' (some derivatives were not provided?)")
    return


def minlmoptimize_fgh(state, func, grad, hess, rep = None, param = None):
    _net_x  = state.ptr.x
    _py_x = create_real_vector(_net_x.GetLength(0))
    _net_g  = state.ptr.g
    _py_g = create_real_vector(_net_g.GetLength(0))
    _net_h  = state.ptr.h
    _py_h = create_real_matrix(_net_h.GetLength(0),_net_h.GetLength(1))
    while True:
        try:
            result = _net_alglib.minlmiteration(state.ptr)
        except _net_alglib.alglibexception as e:
            raise RuntimeError(e.msg)
        if not result:
            break
        if state.ptr.needf:
            copy_net_to_list(_net_x, _py_x, DT_REAL)

            fvalue = func(_py_x, param)
            state.ptr.f = fvalue
            continue
        if state.ptr.needfg:
            copy_net_to_list(_net_x, _py_x, DT_REAL)

            fvalue = grad(_py_x, _py_g, param)
            state.ptr.f = fvalue
            copy_list_to_net(_py_g, _net_g, DT_REAL)
            continue
        if state.ptr.needfgh:
            copy_net_to_list(_net_x, _py_x, DT_REAL)

            fvalue = hess(_py_x, _py_g, _py_h, param)
            state.ptr.f = fvalue
            copy_list_to_net(_py_g, _net_g, DT_REAL)
            copy_listlist_to_net(_py_h, _net_h, DT_REAL)
            continue
        if state.ptr.xupdated:
            if not (rep is None):
                copy_net_to_list(_net_x, _py_x, DT_REAL)
                rep(_py_x, state.ptr.f, param)
            continue
        raise RuntimeError("ALGLIB: error in 'minlmoptimize' (some derivatives were not provided?)")
    return


def minlmoptimize_fj(state, func, jac, rep = None, param = None):
    _net_x  = state.ptr.x
    _py_x = create_real_vector(_net_x.GetLength(0))
    _net_fi  = state.ptr.fi
    _py_fi = create_real_vector(_net_fi.GetLength(0))
    _net_j  = state.ptr.j
    _py_j = create_real_matrix(_net_j.GetLength(0),_net_j.GetLength(1))
    while True:
        try:
            result = _net_alglib.minlmiteration(state.ptr)
        except _net_alglib.alglibexception as e:
            raise RuntimeError(e.msg)
        if not result:
            break
        if state.ptr.needf:
            copy_net_to_list(_net_x, _py_x, DT_REAL)

            fvalue = func(_py_x, param)
            state.ptr.f = fvalue
            continue
        if state.ptr.needfij:
            copy_net_to_list(_net_x, _py_x, DT_REAL)

            jac(_py_x, _py_fi, _py_j, param)
            copy_list_to_net(_py_fi, _net_fi, DT_REAL)
            copy_listlist_to_net(_py_j, _net_j, DT_REAL)
            continue
        if state.ptr.xupdated:
            if not (rep is None):
                copy_net_to_list(_net_x, _py_x, DT_REAL)
                rep(_py_x, state.ptr.f, param)
            continue
        raise RuntimeError("ALGLIB: error in 'minlmoptimize' (some derivatives were not provided?)")
    return


def minlmoptimize_fgj(state, func, grad, jac, rep = None, param = None):
    _net_x  = state.ptr.x
    _py_x = create_real_vector(_net_x.GetLength(0))
    _net_g  = state.ptr.g
    _py_g = create_real_vector(_net_g.GetLength(0))
    _net_fi  = state.ptr.fi
    _py_fi = create_real_vector(_net_fi.GetLength(0))
    _net_j  = state.ptr.j
    _py_j = create_real_matrix(_net_j.GetLength(0),_net_j.GetLength(1))
    while True:
        try:
            result = _net_alglib.minlmiteration(state.ptr)
        except _net_alglib.alglibexception as e:
            raise RuntimeError(e.msg)
        if not result:
            break
        if state.ptr.needf:
            copy_net_to_list(_net_x, _py_x, DT_REAL)

            fvalue = func(_py_x, param)
            state.ptr.f = fvalue
            continue
        if state.ptr.needfg:
            copy_net_to_list(_net_x, _py_x, DT_REAL)

            fvalue = grad(_py_x, _py_g, param)
            state.ptr.f = fvalue
            copy_list_to_net(_py_g, _net_g, DT_REAL)
            continue
        if state.ptr.needfij:
            copy_net_to_list(_net_x, _py_x, DT_REAL)

            jac(_py_x, _py_fi, _py_j, param)
            copy_list_to_net(_py_fi, _net_fi, DT_REAL)
            copy_listlist_to_net(_py_j, _net_j, DT_REAL)
            continue
        if state.ptr.xupdated:
            if not (rep is None):
                copy_net_to_list(_net_x, _py_x, DT_REAL)
                rep(_py_x, state.ptr.f, param)
            continue
        raise RuntimeError("ALGLIB: error in 'minlmoptimize' (some derivatives were not provided?)")
    return


def minlmresults(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_x, _net_rep = _net_alglib.minlmresults(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = list_from_net(_net_x, DT_REAL)
    rep = minlmreport_from_net(_net_rep)

    # return
    return (x, rep)

def minlmresultsbuf(*functionargs):
    # unpack inputs
    state, x, rep = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.minlmresultsbuf' must be real vector")
    _net_rep = _net_alglib.minlmreport()
    net_from_minlmreport(_net_rep, rep)
    try:

        # call function
        _net_x, _net_rep = _net_alglib.minlmresultsbuf(_net_state, _net_x, _net_rep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = list_from_net(_net_x, DT_REAL)
    rep = minlmreport_from_net(_net_rep)

    # return
    return (x, rep)

def minlmrestartfrom(*functionargs):
    # unpack inputs
    state, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.minlmrestartfrom' must be real vector")
    try:

        # call function
        _net_alglib.minlmrestartfrom(_net_state, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minlmrequesttermination(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_alglib.minlmrequesttermination(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def minlmcreatevgj(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        n, m, x = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        m, x = functionargs
        n = check_equality_and_get([safe_len("'minlmcreatevgj': incorrect parameters",x)],"Error while calling 'minlmcreatevgj': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'minlmcreatevgj': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_n = n
    _net_m = m
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.minlmcreatevgj' must be real vector")
    try:

        # call function
        _net_state = _net_alglib.minlmcreatevgj(_net_n, _net_m, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = minlmstate(_net_state)

    # return
    return state

def minlmcreatefgj(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        n, m, x = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        m, x = functionargs
        n = check_equality_and_get([safe_len("'minlmcreatefgj': incorrect parameters",x)],"Error while calling 'minlmcreatefgj': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'minlmcreatefgj': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_n = n
    _net_m = m
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.minlmcreatefgj' must be real vector")
    try:

        # call function
        _net_state = _net_alglib.minlmcreatefgj(_net_n, _net_m, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = minlmstate(_net_state)

    # return
    return state

def minlmcreatefj(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        n, m, x = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        m, x = functionargs
        n = check_equality_and_get([safe_len("'minlmcreatefj': incorrect parameters",x)],"Error while calling 'minlmcreatefj': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'minlmcreatefj': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_n = n
    _net_m = m
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.minlmcreatefj' must be real vector")
    try:

        # call function
        _net_state = _net_alglib.minlmcreatefj(_net_n, _net_m, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = minlmstate(_net_state)

    # return
    return state

def minlmsetgradientcheck(*functionargs):
    # unpack inputs
    state, teststep = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_teststep = teststep
    try:

        # call function
        _net_alglib.minlmsetgradientcheck(_net_state, _net_teststep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return



class eigsubspacestate(object):
    def __init__(self,ptr):
        self.ptr = ptr


class eigsubspacereport(object):
    def __init__(self):
        self.iterationscount = 0


def net_from_eigsubspacereport(x,v):
    x.iterationscount = int(v.iterationscount)
    return




def eigsubspacereport_from_net(x):
    r = eigsubspacereport()
    r.iterationscount = x.iterationscount
    return r


def eigsubspacecreate(*functionargs):
    # unpack inputs
    n, k = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    _net_k = k
    try:

        # call function
        _net_state = _net_alglib.eigsubspacecreate(_net_n, _net_k)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = eigsubspacestate(_net_state)

    # return
    return state

def eigsubspacecreatebuf(*functionargs):
    # unpack inputs
    n, k, state = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    _net_k = k
    _net_state = state.ptr
    try:

        # call function
        _net_alglib.eigsubspacecreatebuf(_net_n, _net_k, _net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def eigsubspacesetcond(*functionargs):
    # unpack inputs
    state, eps, maxits = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_eps = eps
    _net_maxits = maxits
    try:

        # call function
        _net_alglib.eigsubspacesetcond(_net_state, _net_eps, _net_maxits)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def eigsubspacesetwarmstart(*functionargs):
    # unpack inputs
    state, usewarmstart = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_usewarmstart = usewarmstart
    try:

        # call function
        _net_alglib.eigsubspacesetwarmstart(_net_state, _net_usewarmstart)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def eigsubspaceoocstart(*functionargs):
    # unpack inputs
    state, mtype = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_mtype = mtype
    try:

        # call function
        _net_alglib.eigsubspaceoocstart(_net_state, _net_mtype)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def eigsubspaceooccontinue(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_result = _net_alglib.eigsubspaceooccontinue(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def eigsubspaceoocgetrequestinfo(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_requesttype, _net_requestsize = _net_alglib.eigsubspaceoocgetrequestinfo(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    requesttype = _net_requesttype
    requestsize = _net_requestsize

    # return
    return (requesttype, requestsize)

def eigsubspaceoocgetrequestdata(*functionargs):
    # unpack inputs
    state, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_x = net_from_listlist(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.eigsubspaceoocgetrequestdata' must be real matrix")
    try:

        # call function
        _net_x = _net_alglib.eigsubspaceoocgetrequestdata(_net_state, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = listlist_from_net(_net_x, DT_REAL)

    # return
    return x

def eigsubspaceoocsendresult(*functionargs):
    # unpack inputs
    state, ax = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_ax = net_from_listlist(ax, DT_REAL, "ALGLIB: parameter 'ax' of 'xalglib.eigsubspaceoocsendresult' must be real matrix")
    try:

        # call function
        _net_alglib.eigsubspaceoocsendresult(_net_state, _net_ax)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def eigsubspaceoocstop(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_w, _net_z, _net_rep = _net_alglib.eigsubspaceoocstop(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    w = list_from_net(_net_w, DT_REAL)
    z = listlist_from_net(_net_z, DT_REAL)
    rep = eigsubspacereport_from_net(_net_rep)

    # return
    return (w, z, rep)

def eigsubspacesolvedenses(*functionargs):
    # unpack inputs
    state, a, isupper = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.eigsubspacesolvedenses' must be real matrix")
    _net_isupper = isupper
    try:

        # call function
        _net_w, _net_z, _net_rep = _net_alglib.eigsubspacesolvedenses(_net_state, _net_a, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    w = list_from_net(_net_w, DT_REAL)
    z = listlist_from_net(_net_z, DT_REAL)
    rep = eigsubspacereport_from_net(_net_rep)

    # return
    return (w, z, rep)

def smp_eigsubspacesolvedenses(*functionargs):
    # unpack inputs
    state, a, isupper = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smp_eigsubspacesolvedenses' must be real matrix")
    _net_isupper = isupper
    try:

        # call function
        _net_w, _net_z, _net_rep = _net_alglib.smp_eigsubspacesolvedenses(_net_state, _net_a, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    w = list_from_net(_net_w, DT_REAL)
    z = listlist_from_net(_net_z, DT_REAL)
    rep = eigsubspacereport_from_net(_net_rep)

    # return
    return (w, z, rep)

def eigsubspacesolvesparses(*functionargs):
    # unpack inputs
    state, a, isupper = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_a = a.ptr
    _net_isupper = isupper
    try:

        # call function
        _net_w, _net_z, _net_rep = _net_alglib.eigsubspacesolvesparses(_net_state, _net_a, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    w = list_from_net(_net_w, DT_REAL)
    z = listlist_from_net(_net_z, DT_REAL)
    rep = eigsubspacereport_from_net(_net_rep)

    # return
    return (w, z, rep)

def smatrixevd(*functionargs):
    # unpack inputs
    a, n, zneeded, isupper = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smatrixevd' must be real matrix")
    _net_n = n
    _net_zneeded = zneeded
    _net_isupper = isupper
    try:

        # call function
        _net_result, _net_d, _net_z = _net_alglib.smatrixevd(_net_a, _net_n, _net_zneeded, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result
    d = list_from_net(_net_d, DT_REAL)
    z = listlist_from_net(_net_z, DT_REAL)

    # return
    return (result, d, z)

def smatrixevdr(*functionargs):
    # unpack inputs
    a, n, zneeded, isupper, b1, b2 = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smatrixevdr' must be real matrix")
    _net_n = n
    _net_zneeded = zneeded
    _net_isupper = isupper
    _net_b1 = b1
    _net_b2 = b2
    try:

        # call function
        _net_result, _net_m, _net_w, _net_z = _net_alglib.smatrixevdr(_net_a, _net_n, _net_zneeded, _net_isupper, _net_b1, _net_b2)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result
    m = _net_m
    w = list_from_net(_net_w, DT_REAL)
    z = listlist_from_net(_net_z, DT_REAL)

    # return
    return (result, m, w, z)

def smatrixevdi(*functionargs):
    # unpack inputs
    a, n, zneeded, isupper, i1, i2 = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smatrixevdi' must be real matrix")
    _net_n = n
    _net_zneeded = zneeded
    _net_isupper = isupper
    _net_i1 = i1
    _net_i2 = i2
    try:

        # call function
        _net_result, _net_w, _net_z = _net_alglib.smatrixevdi(_net_a, _net_n, _net_zneeded, _net_isupper, _net_i1, _net_i2)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result
    w = list_from_net(_net_w, DT_REAL)
    z = listlist_from_net(_net_z, DT_REAL)

    # return
    return (result, w, z)

def hmatrixevd(*functionargs):
    # unpack inputs
    a, n, zneeded, isupper = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.hmatrixevd' must be complex matrix")
    _net_n = n
    _net_zneeded = zneeded
    _net_isupper = isupper
    try:

        # call function
        _net_result, _net_d, _net_z = _net_alglib.hmatrixevd(_net_a, _net_n, _net_zneeded, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result
    d = list_from_net(_net_d, DT_REAL)
    z = listlist_from_net(_net_z, DT_COMPLEX)

    # return
    return (result, d, z)

def hmatrixevdr(*functionargs):
    # unpack inputs
    a, n, zneeded, isupper, b1, b2 = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.hmatrixevdr' must be complex matrix")
    _net_n = n
    _net_zneeded = zneeded
    _net_isupper = isupper
    _net_b1 = b1
    _net_b2 = b2
    try:

        # call function
        _net_result, _net_m, _net_w, _net_z = _net_alglib.hmatrixevdr(_net_a, _net_n, _net_zneeded, _net_isupper, _net_b1, _net_b2)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result
    m = _net_m
    w = list_from_net(_net_w, DT_REAL)
    z = listlist_from_net(_net_z, DT_COMPLEX)

    # return
    return (result, m, w, z)

def hmatrixevdi(*functionargs):
    # unpack inputs
    a, n, zneeded, isupper, i1, i2 = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.hmatrixevdi' must be complex matrix")
    _net_n = n
    _net_zneeded = zneeded
    _net_isupper = isupper
    _net_i1 = i1
    _net_i2 = i2
    try:

        # call function
        _net_result, _net_w, _net_z = _net_alglib.hmatrixevdi(_net_a, _net_n, _net_zneeded, _net_isupper, _net_i1, _net_i2)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result
    w = list_from_net(_net_w, DT_REAL)
    z = listlist_from_net(_net_z, DT_COMPLEX)

    # return
    return (result, w, z)

def smatrixtdevd(*functionargs):
    # unpack inputs
    d, e, n, zneeded, z = functionargs
    friendly_form = False

    # convert to .NET types
    _net_d = net_from_list(d, DT_REAL, "ALGLIB: parameter 'd' of 'xalglib.smatrixtdevd' must be real vector")
    _net_e = net_from_list(e, DT_REAL, "ALGLIB: parameter 'e' of 'xalglib.smatrixtdevd' must be real vector")
    _net_n = n
    _net_zneeded = zneeded
    _net_z = net_from_listlist(z, DT_REAL, "ALGLIB: parameter 'z' of 'xalglib.smatrixtdevd' must be real matrix")
    try:

        # call function
        _net_result, _net_d, _net_z = _net_alglib.smatrixtdevd(_net_d, _net_e, _net_n, _net_zneeded, _net_z)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result
    d = list_from_net(_net_d, DT_REAL)
    z = listlist_from_net(_net_z, DT_REAL)

    # return
    return (result, d, z)

def smatrixtdevdr(*functionargs):
    # unpack inputs
    d, e, n, zneeded, a, b, z = functionargs
    friendly_form = False

    # convert to .NET types
    _net_d = net_from_list(d, DT_REAL, "ALGLIB: parameter 'd' of 'xalglib.smatrixtdevdr' must be real vector")
    _net_e = net_from_list(e, DT_REAL, "ALGLIB: parameter 'e' of 'xalglib.smatrixtdevdr' must be real vector")
    _net_n = n
    _net_zneeded = zneeded
    _net_a = a
    _net_b = b
    _net_z = net_from_listlist(z, DT_REAL, "ALGLIB: parameter 'z' of 'xalglib.smatrixtdevdr' must be real matrix")
    try:

        # call function
        _net_result, _net_d, _net_m, _net_z = _net_alglib.smatrixtdevdr(_net_d, _net_e, _net_n, _net_zneeded, _net_a, _net_b, _net_z)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result
    d = list_from_net(_net_d, DT_REAL)
    m = _net_m
    z = listlist_from_net(_net_z, DT_REAL)

    # return
    return (result, d, m, z)

def smatrixtdevdi(*functionargs):
    # unpack inputs
    d, e, n, zneeded, i1, i2, z = functionargs
    friendly_form = False

    # convert to .NET types
    _net_d = net_from_list(d, DT_REAL, "ALGLIB: parameter 'd' of 'xalglib.smatrixtdevdi' must be real vector")
    _net_e = net_from_list(e, DT_REAL, "ALGLIB: parameter 'e' of 'xalglib.smatrixtdevdi' must be real vector")
    _net_n = n
    _net_zneeded = zneeded
    _net_i1 = i1
    _net_i2 = i2
    _net_z = net_from_listlist(z, DT_REAL, "ALGLIB: parameter 'z' of 'xalglib.smatrixtdevdi' must be real matrix")
    try:

        # call function
        _net_result, _net_d, _net_z = _net_alglib.smatrixtdevdi(_net_d, _net_e, _net_n, _net_zneeded, _net_i1, _net_i2, _net_z)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result
    d = list_from_net(_net_d, DT_REAL)
    z = listlist_from_net(_net_z, DT_REAL)

    # return
    return (result, d, z)

def rmatrixevd(*functionargs):
    # unpack inputs
    a, n, vneeded = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixevd' must be real matrix")
    _net_n = n
    _net_vneeded = vneeded
    try:

        # call function
        _net_result, _net_wr, _net_wi, _net_vl, _net_vr = _net_alglib.rmatrixevd(_net_a, _net_n, _net_vneeded)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result
    wr = list_from_net(_net_wr, DT_REAL)
    wi = list_from_net(_net_wi, DT_REAL)
    vl = listlist_from_net(_net_vl, DT_REAL)
    vr = listlist_from_net(_net_vr, DT_REAL)

    # return
    return (result, wr, wi, vl, vr)

def samplemoments(*functionargs):
    # unpack inputs
    if len(functionargs)==2:
        # full-form call
        x, n = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        x,  = functionargs
        n = check_equality_and_get([safe_len("'samplemoments': incorrect parameters",x)],"Error while calling 'samplemoments': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'samplemoments': function must have 2 or 1 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.samplemoments' must be real vector")
    _net_n = n
    try:

        # call function
        _net_mean, _net_variance, _net_skewness, _net_kurtosis = _net_alglib.samplemoments(_net_x, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    mean = _net_mean
    variance = _net_variance
    skewness = _net_skewness
    kurtosis = _net_kurtosis

    # return
    return (mean, variance, skewness, kurtosis)

def samplemean(*functionargs):
    # unpack inputs
    if len(functionargs)==2:
        # full-form call
        x, n = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        x,  = functionargs
        n = check_equality_and_get([safe_len("'samplemean': incorrect parameters",x)],"Error while calling 'samplemean': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'samplemean': function must have 2 or 1 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.samplemean' must be real vector")
    _net_n = n
    try:

        # call function
        _net_result = _net_alglib.samplemean(_net_x, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def samplevariance(*functionargs):
    # unpack inputs
    if len(functionargs)==2:
        # full-form call
        x, n = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        x,  = functionargs
        n = check_equality_and_get([safe_len("'samplevariance': incorrect parameters",x)],"Error while calling 'samplevariance': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'samplevariance': function must have 2 or 1 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.samplevariance' must be real vector")
    _net_n = n
    try:

        # call function
        _net_result = _net_alglib.samplevariance(_net_x, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def sampleskewness(*functionargs):
    # unpack inputs
    if len(functionargs)==2:
        # full-form call
        x, n = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        x,  = functionargs
        n = check_equality_and_get([safe_len("'sampleskewness': incorrect parameters",x)],"Error while calling 'sampleskewness': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'sampleskewness': function must have 2 or 1 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.sampleskewness' must be real vector")
    _net_n = n
    try:

        # call function
        _net_result = _net_alglib.sampleskewness(_net_x, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def samplekurtosis(*functionargs):
    # unpack inputs
    if len(functionargs)==2:
        # full-form call
        x, n = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        x,  = functionargs
        n = check_equality_and_get([safe_len("'samplekurtosis': incorrect parameters",x)],"Error while calling 'samplekurtosis': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'samplekurtosis': function must have 2 or 1 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.samplekurtosis' must be real vector")
    _net_n = n
    try:

        # call function
        _net_result = _net_alglib.samplekurtosis(_net_x, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def sampleadev(*functionargs):
    # unpack inputs
    if len(functionargs)==2:
        # full-form call
        x, n = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        x,  = functionargs
        n = check_equality_and_get([safe_len("'sampleadev': incorrect parameters",x)],"Error while calling 'sampleadev': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'sampleadev': function must have 2 or 1 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.sampleadev' must be real vector")
    _net_n = n
    try:

        # call function
        _net_adev = _net_alglib.sampleadev(_net_x, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    adev = _net_adev

    # return
    return adev

def samplemedian(*functionargs):
    # unpack inputs
    if len(functionargs)==2:
        # full-form call
        x, n = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        x,  = functionargs
        n = check_equality_and_get([safe_len("'samplemedian': incorrect parameters",x)],"Error while calling 'samplemedian': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'samplemedian': function must have 2 or 1 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.samplemedian' must be real vector")
    _net_n = n
    try:

        # call function
        _net_median = _net_alglib.samplemedian(_net_x, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    median = _net_median

    # return
    return median

def samplepercentile(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        x, n, p = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        x, p = functionargs
        n = check_equality_and_get([safe_len("'samplepercentile': incorrect parameters",x)],"Error while calling 'samplepercentile': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'samplepercentile': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.samplepercentile' must be real vector")
    _net_n = n
    _net_p = p
    try:

        # call function
        _net_v = _net_alglib.samplepercentile(_net_x, _net_n, _net_p)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    v = _net_v

    # return
    return v

def cov2(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        x, y, n = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        x, y = functionargs
        n = check_equality_and_get([safe_len("'cov2': incorrect parameters",x), safe_len("'cov2': incorrect parameters",y)],"Error while calling 'cov2': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'cov2': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.cov2' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.cov2' must be real vector")
    _net_n = n
    try:

        # call function
        _net_result = _net_alglib.cov2(_net_x, _net_y, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def pearsoncorr2(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        x, y, n = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        x, y = functionargs
        n = check_equality_and_get([safe_len("'pearsoncorr2': incorrect parameters",x), safe_len("'pearsoncorr2': incorrect parameters",y)],"Error while calling 'pearsoncorr2': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'pearsoncorr2': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.pearsoncorr2' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.pearsoncorr2' must be real vector")
    _net_n = n
    try:

        # call function
        _net_result = _net_alglib.pearsoncorr2(_net_x, _net_y, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def spearmancorr2(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        x, y, n = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        x, y = functionargs
        n = check_equality_and_get([safe_len("'spearmancorr2': incorrect parameters",x), safe_len("'spearmancorr2': incorrect parameters",y)],"Error while calling 'spearmancorr2': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'spearmancorr2': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.spearmancorr2' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.spearmancorr2' must be real vector")
    _net_n = n
    try:

        # call function
        _net_result = _net_alglib.spearmancorr2(_net_x, _net_y, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def covm(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        x, n, m = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        x,  = functionargs
        n = check_equality_and_get([safe_rows("'covm': incorrect parameters",x)],"Error while calling 'covm': looks like one of arguments has wrong size")
        m = check_equality_and_get([safe_cols("'covm': incorrect parameters",x)],"Error while calling 'covm': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'covm': function must have 3 or 1 parameters")

    # convert to .NET types
    _net_x = net_from_listlist(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.covm' must be real matrix")
    _net_n = n
    _net_m = m
    try:

        # call function
        _net_c = _net_alglib.covm(_net_x, _net_n, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = listlist_from_net(_net_c, DT_REAL)

    # return
    return c

def smp_covm(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        x, n, m = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        x,  = functionargs
        n = check_equality_and_get([safe_rows("'smp_covm': incorrect parameters",x)],"Error while calling 'smp_covm': looks like one of arguments has wrong size")
        m = check_equality_and_get([safe_cols("'smp_covm': incorrect parameters",x)],"Error while calling 'smp_covm': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'smp_covm': function must have 3 or 1 parameters")

    # convert to .NET types
    _net_x = net_from_listlist(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.smp_covm' must be real matrix")
    _net_n = n
    _net_m = m
    try:

        # call function
        _net_c = _net_alglib.smp_covm(_net_x, _net_n, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = listlist_from_net(_net_c, DT_REAL)

    # return
    return c

def pearsoncorrm(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        x, n, m = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        x,  = functionargs
        n = check_equality_and_get([safe_rows("'pearsoncorrm': incorrect parameters",x)],"Error while calling 'pearsoncorrm': looks like one of arguments has wrong size")
        m = check_equality_and_get([safe_cols("'pearsoncorrm': incorrect parameters",x)],"Error while calling 'pearsoncorrm': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'pearsoncorrm': function must have 3 or 1 parameters")

    # convert to .NET types
    _net_x = net_from_listlist(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.pearsoncorrm' must be real matrix")
    _net_n = n
    _net_m = m
    try:

        # call function
        _net_c = _net_alglib.pearsoncorrm(_net_x, _net_n, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = listlist_from_net(_net_c, DT_REAL)

    # return
    return c

def smp_pearsoncorrm(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        x, n, m = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        x,  = functionargs
        n = check_equality_and_get([safe_rows("'smp_pearsoncorrm': incorrect parameters",x)],"Error while calling 'smp_pearsoncorrm': looks like one of arguments has wrong size")
        m = check_equality_and_get([safe_cols("'smp_pearsoncorrm': incorrect parameters",x)],"Error while calling 'smp_pearsoncorrm': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'smp_pearsoncorrm': function must have 3 or 1 parameters")

    # convert to .NET types
    _net_x = net_from_listlist(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.smp_pearsoncorrm' must be real matrix")
    _net_n = n
    _net_m = m
    try:

        # call function
        _net_c = _net_alglib.smp_pearsoncorrm(_net_x, _net_n, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = listlist_from_net(_net_c, DT_REAL)

    # return
    return c

def spearmancorrm(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        x, n, m = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        x,  = functionargs
        n = check_equality_and_get([safe_rows("'spearmancorrm': incorrect parameters",x)],"Error while calling 'spearmancorrm': looks like one of arguments has wrong size")
        m = check_equality_and_get([safe_cols("'spearmancorrm': incorrect parameters",x)],"Error while calling 'spearmancorrm': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'spearmancorrm': function must have 3 or 1 parameters")

    # convert to .NET types
    _net_x = net_from_listlist(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.spearmancorrm' must be real matrix")
    _net_n = n
    _net_m = m
    try:

        # call function
        _net_c = _net_alglib.spearmancorrm(_net_x, _net_n, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = listlist_from_net(_net_c, DT_REAL)

    # return
    return c

def smp_spearmancorrm(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        x, n, m = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        x,  = functionargs
        n = check_equality_and_get([safe_rows("'smp_spearmancorrm': incorrect parameters",x)],"Error while calling 'smp_spearmancorrm': looks like one of arguments has wrong size")
        m = check_equality_and_get([safe_cols("'smp_spearmancorrm': incorrect parameters",x)],"Error while calling 'smp_spearmancorrm': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'smp_spearmancorrm': function must have 3 or 1 parameters")

    # convert to .NET types
    _net_x = net_from_listlist(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.smp_spearmancorrm' must be real matrix")
    _net_n = n
    _net_m = m
    try:

        # call function
        _net_c = _net_alglib.smp_spearmancorrm(_net_x, _net_n, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = listlist_from_net(_net_c, DT_REAL)

    # return
    return c

def covm2(*functionargs):
    # unpack inputs
    if len(functionargs)==5:
        # full-form call
        x, y, n, m1, m2 = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        x, y = functionargs
        n = check_equality_and_get([safe_rows("'covm2': incorrect parameters",x), safe_rows("'covm2': incorrect parameters",y)],"Error while calling 'covm2': looks like one of arguments has wrong size")
        m1 = check_equality_and_get([safe_cols("'covm2': incorrect parameters",x)],"Error while calling 'covm2': looks like one of arguments has wrong size")
        m2 = check_equality_and_get([safe_cols("'covm2': incorrect parameters",y)],"Error while calling 'covm2': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'covm2': function must have 5 or 2 parameters")

    # convert to .NET types
    _net_x = net_from_listlist(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.covm2' must be real matrix")
    _net_y = net_from_listlist(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.covm2' must be real matrix")
    _net_n = n
    _net_m1 = m1
    _net_m2 = m2
    try:

        # call function
        _net_c = _net_alglib.covm2(_net_x, _net_y, _net_n, _net_m1, _net_m2)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = listlist_from_net(_net_c, DT_REAL)

    # return
    return c

def smp_covm2(*functionargs):
    # unpack inputs
    if len(functionargs)==5:
        # full-form call
        x, y, n, m1, m2 = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        x, y = functionargs
        n = check_equality_and_get([safe_rows("'smp_covm2': incorrect parameters",x), safe_rows("'smp_covm2': incorrect parameters",y)],"Error while calling 'smp_covm2': looks like one of arguments has wrong size")
        m1 = check_equality_and_get([safe_cols("'smp_covm2': incorrect parameters",x)],"Error while calling 'smp_covm2': looks like one of arguments has wrong size")
        m2 = check_equality_and_get([safe_cols("'smp_covm2': incorrect parameters",y)],"Error while calling 'smp_covm2': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'smp_covm2': function must have 5 or 2 parameters")

    # convert to .NET types
    _net_x = net_from_listlist(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.smp_covm2' must be real matrix")
    _net_y = net_from_listlist(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.smp_covm2' must be real matrix")
    _net_n = n
    _net_m1 = m1
    _net_m2 = m2
    try:

        # call function
        _net_c = _net_alglib.smp_covm2(_net_x, _net_y, _net_n, _net_m1, _net_m2)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = listlist_from_net(_net_c, DT_REAL)

    # return
    return c

def pearsoncorrm2(*functionargs):
    # unpack inputs
    if len(functionargs)==5:
        # full-form call
        x, y, n, m1, m2 = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        x, y = functionargs
        n = check_equality_and_get([safe_rows("'pearsoncorrm2': incorrect parameters",x), safe_rows("'pearsoncorrm2': incorrect parameters",y)],"Error while calling 'pearsoncorrm2': looks like one of arguments has wrong size")
        m1 = check_equality_and_get([safe_cols("'pearsoncorrm2': incorrect parameters",x)],"Error while calling 'pearsoncorrm2': looks like one of arguments has wrong size")
        m2 = check_equality_and_get([safe_cols("'pearsoncorrm2': incorrect parameters",y)],"Error while calling 'pearsoncorrm2': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'pearsoncorrm2': function must have 5 or 2 parameters")

    # convert to .NET types
    _net_x = net_from_listlist(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.pearsoncorrm2' must be real matrix")
    _net_y = net_from_listlist(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.pearsoncorrm2' must be real matrix")
    _net_n = n
    _net_m1 = m1
    _net_m2 = m2
    try:

        # call function
        _net_c = _net_alglib.pearsoncorrm2(_net_x, _net_y, _net_n, _net_m1, _net_m2)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = listlist_from_net(_net_c, DT_REAL)

    # return
    return c

def smp_pearsoncorrm2(*functionargs):
    # unpack inputs
    if len(functionargs)==5:
        # full-form call
        x, y, n, m1, m2 = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        x, y = functionargs
        n = check_equality_and_get([safe_rows("'smp_pearsoncorrm2': incorrect parameters",x), safe_rows("'smp_pearsoncorrm2': incorrect parameters",y)],"Error while calling 'smp_pearsoncorrm2': looks like one of arguments has wrong size")
        m1 = check_equality_and_get([safe_cols("'smp_pearsoncorrm2': incorrect parameters",x)],"Error while calling 'smp_pearsoncorrm2': looks like one of arguments has wrong size")
        m2 = check_equality_and_get([safe_cols("'smp_pearsoncorrm2': incorrect parameters",y)],"Error while calling 'smp_pearsoncorrm2': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'smp_pearsoncorrm2': function must have 5 or 2 parameters")

    # convert to .NET types
    _net_x = net_from_listlist(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.smp_pearsoncorrm2' must be real matrix")
    _net_y = net_from_listlist(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.smp_pearsoncorrm2' must be real matrix")
    _net_n = n
    _net_m1 = m1
    _net_m2 = m2
    try:

        # call function
        _net_c = _net_alglib.smp_pearsoncorrm2(_net_x, _net_y, _net_n, _net_m1, _net_m2)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = listlist_from_net(_net_c, DT_REAL)

    # return
    return c

def spearmancorrm2(*functionargs):
    # unpack inputs
    if len(functionargs)==5:
        # full-form call
        x, y, n, m1, m2 = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        x, y = functionargs
        n = check_equality_and_get([safe_rows("'spearmancorrm2': incorrect parameters",x), safe_rows("'spearmancorrm2': incorrect parameters",y)],"Error while calling 'spearmancorrm2': looks like one of arguments has wrong size")
        m1 = check_equality_and_get([safe_cols("'spearmancorrm2': incorrect parameters",x)],"Error while calling 'spearmancorrm2': looks like one of arguments has wrong size")
        m2 = check_equality_and_get([safe_cols("'spearmancorrm2': incorrect parameters",y)],"Error while calling 'spearmancorrm2': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'spearmancorrm2': function must have 5 or 2 parameters")

    # convert to .NET types
    _net_x = net_from_listlist(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.spearmancorrm2' must be real matrix")
    _net_y = net_from_listlist(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.spearmancorrm2' must be real matrix")
    _net_n = n
    _net_m1 = m1
    _net_m2 = m2
    try:

        # call function
        _net_c = _net_alglib.spearmancorrm2(_net_x, _net_y, _net_n, _net_m1, _net_m2)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = listlist_from_net(_net_c, DT_REAL)

    # return
    return c

def smp_spearmancorrm2(*functionargs):
    # unpack inputs
    if len(functionargs)==5:
        # full-form call
        x, y, n, m1, m2 = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        x, y = functionargs
        n = check_equality_and_get([safe_rows("'smp_spearmancorrm2': incorrect parameters",x), safe_rows("'smp_spearmancorrm2': incorrect parameters",y)],"Error while calling 'smp_spearmancorrm2': looks like one of arguments has wrong size")
        m1 = check_equality_and_get([safe_cols("'smp_spearmancorrm2': incorrect parameters",x)],"Error while calling 'smp_spearmancorrm2': looks like one of arguments has wrong size")
        m2 = check_equality_and_get([safe_cols("'smp_spearmancorrm2': incorrect parameters",y)],"Error while calling 'smp_spearmancorrm2': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'smp_spearmancorrm2': function must have 5 or 2 parameters")

    # convert to .NET types
    _net_x = net_from_listlist(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.smp_spearmancorrm2' must be real matrix")
    _net_y = net_from_listlist(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.smp_spearmancorrm2' must be real matrix")
    _net_n = n
    _net_m1 = m1
    _net_m2 = m2
    try:

        # call function
        _net_c = _net_alglib.smp_spearmancorrm2(_net_x, _net_y, _net_n, _net_m1, _net_m2)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = listlist_from_net(_net_c, DT_REAL)

    # return
    return c

def rankdata(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        xy, npoints, nfeatures = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        xy,  = functionargs
        npoints = check_equality_and_get([safe_rows("'rankdata': incorrect parameters",xy)],"Error while calling 'rankdata': looks like one of arguments has wrong size")
        nfeatures = check_equality_and_get([safe_cols("'rankdata': incorrect parameters",xy)],"Error while calling 'rankdata': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'rankdata': function must have 3 or 1 parameters")

    # convert to .NET types
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.rankdata' must be real matrix")
    _net_npoints = npoints
    _net_nfeatures = nfeatures
    try:

        # call function
        _net_xy = _net_alglib.rankdata(_net_xy, _net_npoints, _net_nfeatures)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    xy = listlist_from_net(_net_xy, DT_REAL)

    # return
    return xy

def smp_rankdata(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        xy, npoints, nfeatures = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        xy,  = functionargs
        npoints = check_equality_and_get([safe_rows("'smp_rankdata': incorrect parameters",xy)],"Error while calling 'smp_rankdata': looks like one of arguments has wrong size")
        nfeatures = check_equality_and_get([safe_cols("'smp_rankdata': incorrect parameters",xy)],"Error while calling 'smp_rankdata': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'smp_rankdata': function must have 3 or 1 parameters")

    # convert to .NET types
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.smp_rankdata' must be real matrix")
    _net_npoints = npoints
    _net_nfeatures = nfeatures
    try:

        # call function
        _net_xy = _net_alglib.smp_rankdata(_net_xy, _net_npoints, _net_nfeatures)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    xy = listlist_from_net(_net_xy, DT_REAL)

    # return
    return xy

def rankdatacentered(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        xy, npoints, nfeatures = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        xy,  = functionargs
        npoints = check_equality_and_get([safe_rows("'rankdatacentered': incorrect parameters",xy)],"Error while calling 'rankdatacentered': looks like one of arguments has wrong size")
        nfeatures = check_equality_and_get([safe_cols("'rankdatacentered': incorrect parameters",xy)],"Error while calling 'rankdatacentered': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'rankdatacentered': function must have 3 or 1 parameters")

    # convert to .NET types
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.rankdatacentered' must be real matrix")
    _net_npoints = npoints
    _net_nfeatures = nfeatures
    try:

        # call function
        _net_xy = _net_alglib.rankdatacentered(_net_xy, _net_npoints, _net_nfeatures)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    xy = listlist_from_net(_net_xy, DT_REAL)

    # return
    return xy

def smp_rankdatacentered(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        xy, npoints, nfeatures = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        xy,  = functionargs
        npoints = check_equality_and_get([safe_rows("'smp_rankdatacentered': incorrect parameters",xy)],"Error while calling 'smp_rankdatacentered': looks like one of arguments has wrong size")
        nfeatures = check_equality_and_get([safe_cols("'smp_rankdatacentered': incorrect parameters",xy)],"Error while calling 'smp_rankdatacentered': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'smp_rankdatacentered': function must have 3 or 1 parameters")

    # convert to .NET types
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.smp_rankdatacentered' must be real matrix")
    _net_npoints = npoints
    _net_nfeatures = nfeatures
    try:

        # call function
        _net_xy = _net_alglib.smp_rankdatacentered(_net_xy, _net_npoints, _net_nfeatures)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    xy = listlist_from_net(_net_xy, DT_REAL)

    # return
    return xy

def pearsoncorrelation(*functionargs):
    # unpack inputs
    x, y, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.pearsoncorrelation' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.pearsoncorrelation' must be real vector")
    _net_n = n
    try:

        # call function
        _net_result = _net_alglib.pearsoncorrelation(_net_x, _net_y, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def spearmanrankcorrelation(*functionargs):
    # unpack inputs
    x, y, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.spearmanrankcorrelation' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.spearmanrankcorrelation' must be real vector")
    _net_n = n
    try:

        # call function
        _net_result = _net_alglib.spearmanrankcorrelation(_net_x, _net_y, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def pcabuildbasis(*functionargs):
    # unpack inputs
    x, npoints, nvars = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_listlist(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.pcabuildbasis' must be real matrix")
    _net_npoints = npoints
    _net_nvars = nvars
    try:

        # call function
        _net_info, _net_s2, _net_v = _net_alglib.pcabuildbasis(_net_x, _net_npoints, _net_nvars)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    s2 = list_from_net(_net_s2, DT_REAL)
    v = listlist_from_net(_net_v, DT_REAL)

    # return
    return (info, s2, v)

def smp_pcabuildbasis(*functionargs):
    # unpack inputs
    x, npoints, nvars = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_listlist(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.smp_pcabuildbasis' must be real matrix")
    _net_npoints = npoints
    _net_nvars = nvars
    try:

        # call function
        _net_info, _net_s2, _net_v = _net_alglib.smp_pcabuildbasis(_net_x, _net_npoints, _net_nvars)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    s2 = list_from_net(_net_s2, DT_REAL)
    v = listlist_from_net(_net_v, DT_REAL)

    # return
    return (info, s2, v)

def pcatruncatedsubspace(*functionargs):
    # unpack inputs
    x, npoints, nvars, nneeded, eps, maxits = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_listlist(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.pcatruncatedsubspace' must be real matrix")
    _net_npoints = npoints
    _net_nvars = nvars
    _net_nneeded = nneeded
    _net_eps = eps
    _net_maxits = maxits
    try:

        # call function
        _net_s2, _net_v = _net_alglib.pcatruncatedsubspace(_net_x, _net_npoints, _net_nvars, _net_nneeded, _net_eps, _net_maxits)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    s2 = list_from_net(_net_s2, DT_REAL)
    v = listlist_from_net(_net_v, DT_REAL)

    # return
    return (s2, v)

def smp_pcatruncatedsubspace(*functionargs):
    # unpack inputs
    x, npoints, nvars, nneeded, eps, maxits = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_listlist(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.smp_pcatruncatedsubspace' must be real matrix")
    _net_npoints = npoints
    _net_nvars = nvars
    _net_nneeded = nneeded
    _net_eps = eps
    _net_maxits = maxits
    try:

        # call function
        _net_s2, _net_v = _net_alglib.smp_pcatruncatedsubspace(_net_x, _net_npoints, _net_nvars, _net_nneeded, _net_eps, _net_maxits)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    s2 = list_from_net(_net_s2, DT_REAL)
    v = listlist_from_net(_net_v, DT_REAL)

    # return
    return (s2, v)

def dsoptimalsplit2(*functionargs):
    # unpack inputs
    a, c, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_list(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.dsoptimalsplit2' must be real vector")
    _net_c = net_from_list(c, DT_INT, "ALGLIB: parameter 'c' of 'xalglib.dsoptimalsplit2' must be int vector")
    _net_n = n
    try:

        # call function
        _net_info, _net_threshold, _net_pal, _net_pbl, _net_par, _net_pbr, _net_cve = _net_alglib.dsoptimalsplit2(_net_a, _net_c, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    threshold = _net_threshold
    pal = _net_pal
    pbl = _net_pbl
    par = _net_par
    pbr = _net_pbr
    cve = _net_cve

    # return
    return (info, threshold, pal, pbl, par, pbr, cve)

def dsoptimalsplit2fast(*functionargs):
    # unpack inputs
    a, c, tiesbuf, cntbuf, bufr, bufi, n, nc, alpha = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_list(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.dsoptimalsplit2fast' must be real vector")
    _net_c = net_from_list(c, DT_INT, "ALGLIB: parameter 'c' of 'xalglib.dsoptimalsplit2fast' must be int vector")
    _net_tiesbuf = net_from_list(tiesbuf, DT_INT, "ALGLIB: parameter 'tiesbuf' of 'xalglib.dsoptimalsplit2fast' must be int vector")
    _net_cntbuf = net_from_list(cntbuf, DT_INT, "ALGLIB: parameter 'cntbuf' of 'xalglib.dsoptimalsplit2fast' must be int vector")
    _net_bufr = net_from_list(bufr, DT_REAL, "ALGLIB: parameter 'bufr' of 'xalglib.dsoptimalsplit2fast' must be real vector")
    _net_bufi = net_from_list(bufi, DT_INT, "ALGLIB: parameter 'bufi' of 'xalglib.dsoptimalsplit2fast' must be int vector")
    _net_n = n
    _net_nc = nc
    _net_alpha = alpha
    try:

        # call function
        _net_a, _net_c, _net_tiesbuf, _net_cntbuf, _net_bufr, _net_bufi, _net_info, _net_threshold, _net_rms, _net_cvrms = _net_alglib.dsoptimalsplit2fast(_net_a, _net_c, _net_tiesbuf, _net_cntbuf, _net_bufr, _net_bufi, _net_n, _net_nc, _net_alpha)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = list_from_net(_net_a, DT_REAL)
    c = list_from_net(_net_c, DT_INT)
    tiesbuf = list_from_net(_net_tiesbuf, DT_INT)
    cntbuf = list_from_net(_net_cntbuf, DT_INT)
    bufr = list_from_net(_net_bufr, DT_REAL)
    bufi = list_from_net(_net_bufi, DT_INT)
    info = _net_info
    threshold = _net_threshold
    rms = _net_rms
    cvrms = _net_cvrms

    # return
    return (a, c, tiesbuf, cntbuf, bufr, bufi, info, threshold, rms, cvrms)



class modelerrors(object):
    def __init__(self):
        self.relclserror = 0
        self.avgce = 0
        self.rmserror = 0
        self.avgerror = 0
        self.avgrelerror = 0


def net_from_modelerrors(x,v):
    x.relclserror = float(v.relclserror)
    x.avgce = float(v.avgce)
    x.rmserror = float(v.rmserror)
    x.avgerror = float(v.avgerror)
    x.avgrelerror = float(v.avgrelerror)
    return




def modelerrors_from_net(x):
    r = modelerrors()
    r.relclserror = x.relclserror
    r.avgce = x.avgce
    r.rmserror = x.rmserror
    r.avgerror = x.avgerror
    r.avgrelerror = x.avgrelerror
    return r




class multilayerperceptron(object):
    def __init__(self,ptr):
        self.ptr = ptr
def mlpserialize(obj):
    try:
        return _net_alglib.mlpserialize(obj.ptr)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

def mlpunserialize(s_in):
    try:
        return multilayerperceptron(_net_alglib.mlpunserialize(s_in))
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)
def mlpcreate0(*functionargs):
    # unpack inputs
    nin, nout = functionargs
    friendly_form = False

    # convert to .NET types
    _net_nin = nin
    _net_nout = nout
    try:

        # call function
        _net_network = _net_alglib.mlpcreate0(_net_nin, _net_nout)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    network = multilayerperceptron(_net_network)

    # return
    return network

def mlpcreate1(*functionargs):
    # unpack inputs
    nin, nhid, nout = functionargs
    friendly_form = False

    # convert to .NET types
    _net_nin = nin
    _net_nhid = nhid
    _net_nout = nout
    try:

        # call function
        _net_network = _net_alglib.mlpcreate1(_net_nin, _net_nhid, _net_nout)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    network = multilayerperceptron(_net_network)

    # return
    return network

def mlpcreate2(*functionargs):
    # unpack inputs
    nin, nhid1, nhid2, nout = functionargs
    friendly_form = False

    # convert to .NET types
    _net_nin = nin
    _net_nhid1 = nhid1
    _net_nhid2 = nhid2
    _net_nout = nout
    try:

        # call function
        _net_network = _net_alglib.mlpcreate2(_net_nin, _net_nhid1, _net_nhid2, _net_nout)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    network = multilayerperceptron(_net_network)

    # return
    return network

def mlpcreateb0(*functionargs):
    # unpack inputs
    nin, nout, b, d = functionargs
    friendly_form = False

    # convert to .NET types
    _net_nin = nin
    _net_nout = nout
    _net_b = b
    _net_d = d
    try:

        # call function
        _net_network = _net_alglib.mlpcreateb0(_net_nin, _net_nout, _net_b, _net_d)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    network = multilayerperceptron(_net_network)

    # return
    return network

def mlpcreateb1(*functionargs):
    # unpack inputs
    nin, nhid, nout, b, d = functionargs
    friendly_form = False

    # convert to .NET types
    _net_nin = nin
    _net_nhid = nhid
    _net_nout = nout
    _net_b = b
    _net_d = d
    try:

        # call function
        _net_network = _net_alglib.mlpcreateb1(_net_nin, _net_nhid, _net_nout, _net_b, _net_d)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    network = multilayerperceptron(_net_network)

    # return
    return network

def mlpcreateb2(*functionargs):
    # unpack inputs
    nin, nhid1, nhid2, nout, b, d = functionargs
    friendly_form = False

    # convert to .NET types
    _net_nin = nin
    _net_nhid1 = nhid1
    _net_nhid2 = nhid2
    _net_nout = nout
    _net_b = b
    _net_d = d
    try:

        # call function
        _net_network = _net_alglib.mlpcreateb2(_net_nin, _net_nhid1, _net_nhid2, _net_nout, _net_b, _net_d)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    network = multilayerperceptron(_net_network)

    # return
    return network

def mlpcreater0(*functionargs):
    # unpack inputs
    nin, nout, a, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_nin = nin
    _net_nout = nout
    _net_a = a
    _net_b = b
    try:

        # call function
        _net_network = _net_alglib.mlpcreater0(_net_nin, _net_nout, _net_a, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    network = multilayerperceptron(_net_network)

    # return
    return network

def mlpcreater1(*functionargs):
    # unpack inputs
    nin, nhid, nout, a, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_nin = nin
    _net_nhid = nhid
    _net_nout = nout
    _net_a = a
    _net_b = b
    try:

        # call function
        _net_network = _net_alglib.mlpcreater1(_net_nin, _net_nhid, _net_nout, _net_a, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    network = multilayerperceptron(_net_network)

    # return
    return network

def mlpcreater2(*functionargs):
    # unpack inputs
    nin, nhid1, nhid2, nout, a, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_nin = nin
    _net_nhid1 = nhid1
    _net_nhid2 = nhid2
    _net_nout = nout
    _net_a = a
    _net_b = b
    try:

        # call function
        _net_network = _net_alglib.mlpcreater2(_net_nin, _net_nhid1, _net_nhid2, _net_nout, _net_a, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    network = multilayerperceptron(_net_network)

    # return
    return network

def mlpcreatec0(*functionargs):
    # unpack inputs
    nin, nout = functionargs
    friendly_form = False

    # convert to .NET types
    _net_nin = nin
    _net_nout = nout
    try:

        # call function
        _net_network = _net_alglib.mlpcreatec0(_net_nin, _net_nout)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    network = multilayerperceptron(_net_network)

    # return
    return network

def mlpcreatec1(*functionargs):
    # unpack inputs
    nin, nhid, nout = functionargs
    friendly_form = False

    # convert to .NET types
    _net_nin = nin
    _net_nhid = nhid
    _net_nout = nout
    try:

        # call function
        _net_network = _net_alglib.mlpcreatec1(_net_nin, _net_nhid, _net_nout)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    network = multilayerperceptron(_net_network)

    # return
    return network

def mlpcreatec2(*functionargs):
    # unpack inputs
    nin, nhid1, nhid2, nout = functionargs
    friendly_form = False

    # convert to .NET types
    _net_nin = nin
    _net_nhid1 = nhid1
    _net_nhid2 = nhid2
    _net_nout = nout
    try:

        # call function
        _net_network = _net_alglib.mlpcreatec2(_net_nin, _net_nhid1, _net_nhid2, _net_nout)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    network = multilayerperceptron(_net_network)

    # return
    return network

def mlpcopy(*functionargs):
    # unpack inputs
    network1,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network1 = network1.ptr
    try:

        # call function
        _net_network2 = _net_alglib.mlpcopy(_net_network1)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    network2 = multilayerperceptron(_net_network2)

    # return
    return network2

def mlpcopytunableparameters(*functionargs):
    # unpack inputs
    network1, network2 = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network1 = network1.ptr
    _net_network2 = network2.ptr
    try:

        # call function
        _net_alglib.mlpcopytunableparameters(_net_network1, _net_network2)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mlprandomize(*functionargs):
    # unpack inputs
    network,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    try:

        # call function
        _net_alglib.mlprandomize(_net_network)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mlprandomizefull(*functionargs):
    # unpack inputs
    network,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    try:

        # call function
        _net_alglib.mlprandomizefull(_net_network)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mlpinitpreprocessor(*functionargs):
    # unpack inputs
    network, xy, ssize = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mlpinitpreprocessor' must be real matrix")
    _net_ssize = ssize
    try:

        # call function
        _net_alglib.mlpinitpreprocessor(_net_network, _net_xy, _net_ssize)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mlpproperties(*functionargs):
    # unpack inputs
    network,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    try:

        # call function
        _net_nin, _net_nout, _net_wcount = _net_alglib.mlpproperties(_net_network)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    nin = _net_nin
    nout = _net_nout
    wcount = _net_wcount

    # return
    return (nin, nout, wcount)

def mlpgetinputscount(*functionargs):
    # unpack inputs
    network,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    try:

        # call function
        _net_result = _net_alglib.mlpgetinputscount(_net_network)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def mlpgetoutputscount(*functionargs):
    # unpack inputs
    network,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    try:

        # call function
        _net_result = _net_alglib.mlpgetoutputscount(_net_network)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def mlpgetweightscount(*functionargs):
    # unpack inputs
    network,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    try:

        # call function
        _net_result = _net_alglib.mlpgetweightscount(_net_network)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def mlpissoftmax(*functionargs):
    # unpack inputs
    network,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    try:

        # call function
        _net_result = _net_alglib.mlpissoftmax(_net_network)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def mlpgetlayerscount(*functionargs):
    # unpack inputs
    network,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    try:

        # call function
        _net_result = _net_alglib.mlpgetlayerscount(_net_network)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def mlpgetlayersize(*functionargs):
    # unpack inputs
    network, k = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_k = k
    try:

        # call function
        _net_result = _net_alglib.mlpgetlayersize(_net_network, _net_k)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def mlpgetinputscaling(*functionargs):
    # unpack inputs
    network, i = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_i = i
    try:

        # call function
        _net_mean, _net_sigma = _net_alglib.mlpgetinputscaling(_net_network, _net_i)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    mean = _net_mean
    sigma = _net_sigma

    # return
    return (mean, sigma)

def mlpgetoutputscaling(*functionargs):
    # unpack inputs
    network, i = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_i = i
    try:

        # call function
        _net_mean, _net_sigma = _net_alglib.mlpgetoutputscaling(_net_network, _net_i)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    mean = _net_mean
    sigma = _net_sigma

    # return
    return (mean, sigma)

def mlpgetneuroninfo(*functionargs):
    # unpack inputs
    network, k, i = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_k = k
    _net_i = i
    try:

        # call function
        _net_fkind, _net_threshold = _net_alglib.mlpgetneuroninfo(_net_network, _net_k, _net_i)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    fkind = _net_fkind
    threshold = _net_threshold

    # return
    return (fkind, threshold)

def mlpgetweight(*functionargs):
    # unpack inputs
    network, k0, i0, k1, i1 = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_k0 = k0
    _net_i0 = i0
    _net_k1 = k1
    _net_i1 = i1
    try:

        # call function
        _net_result = _net_alglib.mlpgetweight(_net_network, _net_k0, _net_i0, _net_k1, _net_i1)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def mlpsetinputscaling(*functionargs):
    # unpack inputs
    network, i, mean, sigma = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_i = i
    _net_mean = mean
    _net_sigma = sigma
    try:

        # call function
        _net_alglib.mlpsetinputscaling(_net_network, _net_i, _net_mean, _net_sigma)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mlpsetoutputscaling(*functionargs):
    # unpack inputs
    network, i, mean, sigma = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_i = i
    _net_mean = mean
    _net_sigma = sigma
    try:

        # call function
        _net_alglib.mlpsetoutputscaling(_net_network, _net_i, _net_mean, _net_sigma)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mlpsetneuroninfo(*functionargs):
    # unpack inputs
    network, k, i, fkind, threshold = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_k = k
    _net_i = i
    _net_fkind = fkind
    _net_threshold = threshold
    try:

        # call function
        _net_alglib.mlpsetneuroninfo(_net_network, _net_k, _net_i, _net_fkind, _net_threshold)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mlpsetweight(*functionargs):
    # unpack inputs
    network, k0, i0, k1, i1, w = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_k0 = k0
    _net_i0 = i0
    _net_k1 = k1
    _net_i1 = i1
    _net_w = w
    try:

        # call function
        _net_alglib.mlpsetweight(_net_network, _net_k0, _net_i0, _net_k1, _net_i1, _net_w)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mlpactivationfunction(*functionargs):
    # unpack inputs
    net, k = functionargs
    friendly_form = False

    # convert to .NET types
    _net_net = net
    _net_k = k
    try:

        # call function
        _net_f, _net_df, _net_d2f = _net_alglib.mlpactivationfunction(_net_net, _net_k)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    f = _net_f
    df = _net_df
    d2f = _net_d2f

    # return
    return (f, df, d2f)

def mlpprocess(*functionargs):
    # unpack inputs
    network, x, y = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.mlpprocess' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.mlpprocess' must be real vector")
    try:

        # call function
        _net_y = _net_alglib.mlpprocess(_net_network, _net_x, _net_y)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    y = list_from_net(_net_y, DT_REAL)

    # return
    return y

def mlpprocessi(*functionargs):
    # unpack inputs
    network, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.mlpprocessi' must be real vector")
    try:

        # call function
        _net_y = _net_alglib.mlpprocessi(_net_network, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    y = list_from_net(_net_y, DT_REAL)

    # return
    return y

def mlperror(*functionargs):
    # unpack inputs
    network, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mlperror' must be real matrix")
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.mlperror(_net_network, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def smp_mlperror(*functionargs):
    # unpack inputs
    network, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.smp_mlperror' must be real matrix")
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.smp_mlperror(_net_network, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def mlperrorsparse(*functionargs):
    # unpack inputs
    network, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = xy.ptr
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.mlperrorsparse(_net_network, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def smp_mlperrorsparse(*functionargs):
    # unpack inputs
    network, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = xy.ptr
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.smp_mlperrorsparse(_net_network, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def mlperrorn(*functionargs):
    # unpack inputs
    network, xy, ssize = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mlperrorn' must be real matrix")
    _net_ssize = ssize
    try:

        # call function
        _net_result = _net_alglib.mlperrorn(_net_network, _net_xy, _net_ssize)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def mlpclserror(*functionargs):
    # unpack inputs
    network, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mlpclserror' must be real matrix")
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.mlpclserror(_net_network, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def smp_mlpclserror(*functionargs):
    # unpack inputs
    network, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.smp_mlpclserror' must be real matrix")
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.smp_mlpclserror(_net_network, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def mlprelclserror(*functionargs):
    # unpack inputs
    network, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mlprelclserror' must be real matrix")
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.mlprelclserror(_net_network, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def smp_mlprelclserror(*functionargs):
    # unpack inputs
    network, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.smp_mlprelclserror' must be real matrix")
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.smp_mlprelclserror(_net_network, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def mlprelclserrorsparse(*functionargs):
    # unpack inputs
    network, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = xy.ptr
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.mlprelclserrorsparse(_net_network, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def smp_mlprelclserrorsparse(*functionargs):
    # unpack inputs
    network, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = xy.ptr
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.smp_mlprelclserrorsparse(_net_network, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def mlpavgce(*functionargs):
    # unpack inputs
    network, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mlpavgce' must be real matrix")
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.mlpavgce(_net_network, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def smp_mlpavgce(*functionargs):
    # unpack inputs
    network, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.smp_mlpavgce' must be real matrix")
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.smp_mlpavgce(_net_network, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def mlpavgcesparse(*functionargs):
    # unpack inputs
    network, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = xy.ptr
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.mlpavgcesparse(_net_network, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def smp_mlpavgcesparse(*functionargs):
    # unpack inputs
    network, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = xy.ptr
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.smp_mlpavgcesparse(_net_network, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def mlprmserror(*functionargs):
    # unpack inputs
    network, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mlprmserror' must be real matrix")
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.mlprmserror(_net_network, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def smp_mlprmserror(*functionargs):
    # unpack inputs
    network, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.smp_mlprmserror' must be real matrix")
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.smp_mlprmserror(_net_network, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def mlprmserrorsparse(*functionargs):
    # unpack inputs
    network, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = xy.ptr
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.mlprmserrorsparse(_net_network, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def smp_mlprmserrorsparse(*functionargs):
    # unpack inputs
    network, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = xy.ptr
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.smp_mlprmserrorsparse(_net_network, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def mlpavgerror(*functionargs):
    # unpack inputs
    network, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mlpavgerror' must be real matrix")
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.mlpavgerror(_net_network, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def smp_mlpavgerror(*functionargs):
    # unpack inputs
    network, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.smp_mlpavgerror' must be real matrix")
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.smp_mlpavgerror(_net_network, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def mlpavgerrorsparse(*functionargs):
    # unpack inputs
    network, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = xy.ptr
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.mlpavgerrorsparse(_net_network, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def smp_mlpavgerrorsparse(*functionargs):
    # unpack inputs
    network, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = xy.ptr
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.smp_mlpavgerrorsparse(_net_network, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def mlpavgrelerror(*functionargs):
    # unpack inputs
    network, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mlpavgrelerror' must be real matrix")
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.mlpavgrelerror(_net_network, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def smp_mlpavgrelerror(*functionargs):
    # unpack inputs
    network, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.smp_mlpavgrelerror' must be real matrix")
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.smp_mlpavgrelerror(_net_network, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def mlpavgrelerrorsparse(*functionargs):
    # unpack inputs
    network, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = xy.ptr
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.mlpavgrelerrorsparse(_net_network, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def smp_mlpavgrelerrorsparse(*functionargs):
    # unpack inputs
    network, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = xy.ptr
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.smp_mlpavgrelerrorsparse(_net_network, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def mlpgrad(*functionargs):
    # unpack inputs
    network, x, desiredy, grad = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.mlpgrad' must be real vector")
    _net_desiredy = net_from_list(desiredy, DT_REAL, "ALGLIB: parameter 'desiredy' of 'xalglib.mlpgrad' must be real vector")
    _net_grad = net_from_list(grad, DT_REAL, "ALGLIB: parameter 'grad' of 'xalglib.mlpgrad' must be real vector")
    try:

        # call function
        _net_e, _net_grad = _net_alglib.mlpgrad(_net_network, _net_x, _net_desiredy, _net_grad)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    e = _net_e
    grad = list_from_net(_net_grad, DT_REAL)

    # return
    return (e, grad)

def mlpgradn(*functionargs):
    # unpack inputs
    network, x, desiredy, grad = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.mlpgradn' must be real vector")
    _net_desiredy = net_from_list(desiredy, DT_REAL, "ALGLIB: parameter 'desiredy' of 'xalglib.mlpgradn' must be real vector")
    _net_grad = net_from_list(grad, DT_REAL, "ALGLIB: parameter 'grad' of 'xalglib.mlpgradn' must be real vector")
    try:

        # call function
        _net_e, _net_grad = _net_alglib.mlpgradn(_net_network, _net_x, _net_desiredy, _net_grad)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    e = _net_e
    grad = list_from_net(_net_grad, DT_REAL)

    # return
    return (e, grad)

def mlpgradbatch(*functionargs):
    # unpack inputs
    network, xy, ssize, grad = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mlpgradbatch' must be real matrix")
    _net_ssize = ssize
    _net_grad = net_from_list(grad, DT_REAL, "ALGLIB: parameter 'grad' of 'xalglib.mlpgradbatch' must be real vector")
    try:

        # call function
        _net_e, _net_grad = _net_alglib.mlpgradbatch(_net_network, _net_xy, _net_ssize, _net_grad)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    e = _net_e
    grad = list_from_net(_net_grad, DT_REAL)

    # return
    return (e, grad)

def smp_mlpgradbatch(*functionargs):
    # unpack inputs
    network, xy, ssize, grad = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.smp_mlpgradbatch' must be real matrix")
    _net_ssize = ssize
    _net_grad = net_from_list(grad, DT_REAL, "ALGLIB: parameter 'grad' of 'xalglib.smp_mlpgradbatch' must be real vector")
    try:

        # call function
        _net_e, _net_grad = _net_alglib.smp_mlpgradbatch(_net_network, _net_xy, _net_ssize, _net_grad)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    e = _net_e
    grad = list_from_net(_net_grad, DT_REAL)

    # return
    return (e, grad)

def mlpgradbatchsparse(*functionargs):
    # unpack inputs
    network, xy, ssize, grad = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = xy.ptr
    _net_ssize = ssize
    _net_grad = net_from_list(grad, DT_REAL, "ALGLIB: parameter 'grad' of 'xalglib.mlpgradbatchsparse' must be real vector")
    try:

        # call function
        _net_e, _net_grad = _net_alglib.mlpgradbatchsparse(_net_network, _net_xy, _net_ssize, _net_grad)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    e = _net_e
    grad = list_from_net(_net_grad, DT_REAL)

    # return
    return (e, grad)

def smp_mlpgradbatchsparse(*functionargs):
    # unpack inputs
    network, xy, ssize, grad = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = xy.ptr
    _net_ssize = ssize
    _net_grad = net_from_list(grad, DT_REAL, "ALGLIB: parameter 'grad' of 'xalglib.smp_mlpgradbatchsparse' must be real vector")
    try:

        # call function
        _net_e, _net_grad = _net_alglib.smp_mlpgradbatchsparse(_net_network, _net_xy, _net_ssize, _net_grad)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    e = _net_e
    grad = list_from_net(_net_grad, DT_REAL)

    # return
    return (e, grad)

def mlpgradbatchsubset(*functionargs):
    # unpack inputs
    network, xy, setsize, idx, subsetsize, grad = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mlpgradbatchsubset' must be real matrix")
    _net_setsize = setsize
    _net_idx = net_from_list(idx, DT_INT, "ALGLIB: parameter 'idx' of 'xalglib.mlpgradbatchsubset' must be int vector")
    _net_subsetsize = subsetsize
    _net_grad = net_from_list(grad, DT_REAL, "ALGLIB: parameter 'grad' of 'xalglib.mlpgradbatchsubset' must be real vector")
    try:

        # call function
        _net_e, _net_grad = _net_alglib.mlpgradbatchsubset(_net_network, _net_xy, _net_setsize, _net_idx, _net_subsetsize, _net_grad)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    e = _net_e
    grad = list_from_net(_net_grad, DT_REAL)

    # return
    return (e, grad)

def smp_mlpgradbatchsubset(*functionargs):
    # unpack inputs
    network, xy, setsize, idx, subsetsize, grad = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.smp_mlpgradbatchsubset' must be real matrix")
    _net_setsize = setsize
    _net_idx = net_from_list(idx, DT_INT, "ALGLIB: parameter 'idx' of 'xalglib.smp_mlpgradbatchsubset' must be int vector")
    _net_subsetsize = subsetsize
    _net_grad = net_from_list(grad, DT_REAL, "ALGLIB: parameter 'grad' of 'xalglib.smp_mlpgradbatchsubset' must be real vector")
    try:

        # call function
        _net_e, _net_grad = _net_alglib.smp_mlpgradbatchsubset(_net_network, _net_xy, _net_setsize, _net_idx, _net_subsetsize, _net_grad)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    e = _net_e
    grad = list_from_net(_net_grad, DT_REAL)

    # return
    return (e, grad)

def mlpgradbatchsparsesubset(*functionargs):
    # unpack inputs
    network, xy, setsize, idx, subsetsize, grad = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = xy.ptr
    _net_setsize = setsize
    _net_idx = net_from_list(idx, DT_INT, "ALGLIB: parameter 'idx' of 'xalglib.mlpgradbatchsparsesubset' must be int vector")
    _net_subsetsize = subsetsize
    _net_grad = net_from_list(grad, DT_REAL, "ALGLIB: parameter 'grad' of 'xalglib.mlpgradbatchsparsesubset' must be real vector")
    try:

        # call function
        _net_e, _net_grad = _net_alglib.mlpgradbatchsparsesubset(_net_network, _net_xy, _net_setsize, _net_idx, _net_subsetsize, _net_grad)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    e = _net_e
    grad = list_from_net(_net_grad, DT_REAL)

    # return
    return (e, grad)

def smp_mlpgradbatchsparsesubset(*functionargs):
    # unpack inputs
    network, xy, setsize, idx, subsetsize, grad = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = xy.ptr
    _net_setsize = setsize
    _net_idx = net_from_list(idx, DT_INT, "ALGLIB: parameter 'idx' of 'xalglib.smp_mlpgradbatchsparsesubset' must be int vector")
    _net_subsetsize = subsetsize
    _net_grad = net_from_list(grad, DT_REAL, "ALGLIB: parameter 'grad' of 'xalglib.smp_mlpgradbatchsparsesubset' must be real vector")
    try:

        # call function
        _net_e, _net_grad = _net_alglib.smp_mlpgradbatchsparsesubset(_net_network, _net_xy, _net_setsize, _net_idx, _net_subsetsize, _net_grad)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    e = _net_e
    grad = list_from_net(_net_grad, DT_REAL)

    # return
    return (e, grad)

def mlpgradnbatch(*functionargs):
    # unpack inputs
    network, xy, ssize, grad = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mlpgradnbatch' must be real matrix")
    _net_ssize = ssize
    _net_grad = net_from_list(grad, DT_REAL, "ALGLIB: parameter 'grad' of 'xalglib.mlpgradnbatch' must be real vector")
    try:

        # call function
        _net_e, _net_grad = _net_alglib.mlpgradnbatch(_net_network, _net_xy, _net_ssize, _net_grad)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    e = _net_e
    grad = list_from_net(_net_grad, DT_REAL)

    # return
    return (e, grad)

def mlphessiannbatch(*functionargs):
    # unpack inputs
    network, xy, ssize, grad, h = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mlphessiannbatch' must be real matrix")
    _net_ssize = ssize
    _net_grad = net_from_list(grad, DT_REAL, "ALGLIB: parameter 'grad' of 'xalglib.mlphessiannbatch' must be real vector")
    _net_h = net_from_listlist(h, DT_REAL, "ALGLIB: parameter 'h' of 'xalglib.mlphessiannbatch' must be real matrix")
    try:

        # call function
        _net_e, _net_grad, _net_h = _net_alglib.mlphessiannbatch(_net_network, _net_xy, _net_ssize, _net_grad, _net_h)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    e = _net_e
    grad = list_from_net(_net_grad, DT_REAL)
    h = listlist_from_net(_net_h, DT_REAL)

    # return
    return (e, grad, h)

def mlphessianbatch(*functionargs):
    # unpack inputs
    network, xy, ssize, grad, h = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mlphessianbatch' must be real matrix")
    _net_ssize = ssize
    _net_grad = net_from_list(grad, DT_REAL, "ALGLIB: parameter 'grad' of 'xalglib.mlphessianbatch' must be real vector")
    _net_h = net_from_listlist(h, DT_REAL, "ALGLIB: parameter 'h' of 'xalglib.mlphessianbatch' must be real matrix")
    try:

        # call function
        _net_e, _net_grad, _net_h = _net_alglib.mlphessianbatch(_net_network, _net_xy, _net_ssize, _net_grad, _net_h)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    e = _net_e
    grad = list_from_net(_net_grad, DT_REAL)
    h = listlist_from_net(_net_h, DT_REAL)

    # return
    return (e, grad, h)

def mlpallerrorssubset(*functionargs):
    # unpack inputs
    network, xy, setsize, subset, subsetsize = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mlpallerrorssubset' must be real matrix")
    _net_setsize = setsize
    _net_subset = net_from_list(subset, DT_INT, "ALGLIB: parameter 'subset' of 'xalglib.mlpallerrorssubset' must be int vector")
    _net_subsetsize = subsetsize
    try:

        # call function
        _net_rep = _net_alglib.mlpallerrorssubset(_net_network, _net_xy, _net_setsize, _net_subset, _net_subsetsize)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    rep = modelerrors_from_net(_net_rep)

    # return
    return rep

def smp_mlpallerrorssubset(*functionargs):
    # unpack inputs
    network, xy, setsize, subset, subsetsize = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.smp_mlpallerrorssubset' must be real matrix")
    _net_setsize = setsize
    _net_subset = net_from_list(subset, DT_INT, "ALGLIB: parameter 'subset' of 'xalglib.smp_mlpallerrorssubset' must be int vector")
    _net_subsetsize = subsetsize
    try:

        # call function
        _net_rep = _net_alglib.smp_mlpallerrorssubset(_net_network, _net_xy, _net_setsize, _net_subset, _net_subsetsize)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    rep = modelerrors_from_net(_net_rep)

    # return
    return rep

def mlpallerrorssparsesubset(*functionargs):
    # unpack inputs
    network, xy, setsize, subset, subsetsize = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = xy.ptr
    _net_setsize = setsize
    _net_subset = net_from_list(subset, DT_INT, "ALGLIB: parameter 'subset' of 'xalglib.mlpallerrorssparsesubset' must be int vector")
    _net_subsetsize = subsetsize
    try:

        # call function
        _net_rep = _net_alglib.mlpallerrorssparsesubset(_net_network, _net_xy, _net_setsize, _net_subset, _net_subsetsize)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    rep = modelerrors_from_net(_net_rep)

    # return
    return rep

def smp_mlpallerrorssparsesubset(*functionargs):
    # unpack inputs
    network, xy, setsize, subset, subsetsize = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = xy.ptr
    _net_setsize = setsize
    _net_subset = net_from_list(subset, DT_INT, "ALGLIB: parameter 'subset' of 'xalglib.smp_mlpallerrorssparsesubset' must be int vector")
    _net_subsetsize = subsetsize
    try:

        # call function
        _net_rep = _net_alglib.smp_mlpallerrorssparsesubset(_net_network, _net_xy, _net_setsize, _net_subset, _net_subsetsize)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    rep = modelerrors_from_net(_net_rep)

    # return
    return rep

def mlperrorsubset(*functionargs):
    # unpack inputs
    network, xy, setsize, subset, subsetsize = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mlperrorsubset' must be real matrix")
    _net_setsize = setsize
    _net_subset = net_from_list(subset, DT_INT, "ALGLIB: parameter 'subset' of 'xalglib.mlperrorsubset' must be int vector")
    _net_subsetsize = subsetsize
    try:

        # call function
        _net_result = _net_alglib.mlperrorsubset(_net_network, _net_xy, _net_setsize, _net_subset, _net_subsetsize)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def smp_mlperrorsubset(*functionargs):
    # unpack inputs
    network, xy, setsize, subset, subsetsize = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.smp_mlperrorsubset' must be real matrix")
    _net_setsize = setsize
    _net_subset = net_from_list(subset, DT_INT, "ALGLIB: parameter 'subset' of 'xalglib.smp_mlperrorsubset' must be int vector")
    _net_subsetsize = subsetsize
    try:

        # call function
        _net_result = _net_alglib.smp_mlperrorsubset(_net_network, _net_xy, _net_setsize, _net_subset, _net_subsetsize)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def mlperrorsparsesubset(*functionargs):
    # unpack inputs
    network, xy, setsize, subset, subsetsize = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = xy.ptr
    _net_setsize = setsize
    _net_subset = net_from_list(subset, DT_INT, "ALGLIB: parameter 'subset' of 'xalglib.mlperrorsparsesubset' must be int vector")
    _net_subsetsize = subsetsize
    try:

        # call function
        _net_result = _net_alglib.mlperrorsparsesubset(_net_network, _net_xy, _net_setsize, _net_subset, _net_subsetsize)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def smp_mlperrorsparsesubset(*functionargs):
    # unpack inputs
    network, xy, setsize, subset, subsetsize = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = xy.ptr
    _net_setsize = setsize
    _net_subset = net_from_list(subset, DT_INT, "ALGLIB: parameter 'subset' of 'xalglib.smp_mlperrorsparsesubset' must be int vector")
    _net_subsetsize = subsetsize
    try:

        # call function
        _net_result = _net_alglib.smp_mlperrorsparsesubset(_net_network, _net_xy, _net_setsize, _net_subset, _net_subsetsize)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def fisherlda(*functionargs):
    # unpack inputs
    xy, npoints, nvars, nclasses = functionargs
    friendly_form = False

    # convert to .NET types
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.fisherlda' must be real matrix")
    _net_npoints = npoints
    _net_nvars = nvars
    _net_nclasses = nclasses
    try:

        # call function
        _net_info, _net_w = _net_alglib.fisherlda(_net_xy, _net_npoints, _net_nvars, _net_nclasses)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    w = list_from_net(_net_w, DT_REAL)

    # return
    return (info, w)

def fisherldan(*functionargs):
    # unpack inputs
    xy, npoints, nvars, nclasses = functionargs
    friendly_form = False

    # convert to .NET types
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.fisherldan' must be real matrix")
    _net_npoints = npoints
    _net_nvars = nvars
    _net_nclasses = nclasses
    try:

        # call function
        _net_info, _net_w = _net_alglib.fisherldan(_net_xy, _net_npoints, _net_nvars, _net_nclasses)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    w = listlist_from_net(_net_w, DT_REAL)

    # return
    return (info, w)

def smp_fisherldan(*functionargs):
    # unpack inputs
    xy, npoints, nvars, nclasses = functionargs
    friendly_form = False

    # convert to .NET types
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.smp_fisherldan' must be real matrix")
    _net_npoints = npoints
    _net_nvars = nvars
    _net_nclasses = nclasses
    try:

        # call function
        _net_info, _net_w = _net_alglib.smp_fisherldan(_net_xy, _net_npoints, _net_nvars, _net_nclasses)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    w = listlist_from_net(_net_w, DT_REAL)

    # return
    return (info, w)



class ssamodel(object):
    def __init__(self,ptr):
        self.ptr = ptr
def ssacreate(*functionargs):
    # unpack inputs
    friendly_form = False

    # convert to .NET types
    try:

        # call function
        _net_s = _net_alglib.ssacreate()
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    s = ssamodel(_net_s)

    # return
    return s

def ssasetwindow(*functionargs):
    # unpack inputs
    s, windowwidth = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_windowwidth = windowwidth
    try:

        # call function
        _net_alglib.ssasetwindow(_net_s, _net_windowwidth)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def ssasetseed(*functionargs):
    # unpack inputs
    s, seed = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_seed = seed
    try:

        # call function
        _net_alglib.ssasetseed(_net_s, _net_seed)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def ssasetpoweruplength(*functionargs):
    # unpack inputs
    s, pwlen = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_pwlen = pwlen
    try:

        # call function
        _net_alglib.ssasetpoweruplength(_net_s, _net_pwlen)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def ssasetmemorylimit(*functionargs):
    # unpack inputs
    s, memlimit = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_memlimit = memlimit
    try:

        # call function
        _net_alglib.ssasetmemorylimit(_net_s, _net_memlimit)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def ssaaddsequence(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        s, x, n = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        s, x = functionargs
        n = check_equality_and_get([safe_len("'ssaaddsequence': incorrect parameters",x)],"Error while calling 'ssaaddsequence': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'ssaaddsequence': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_s = s.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.ssaaddsequence' must be real vector")
    _net_n = n
    try:

        # call function
        _net_alglib.ssaaddsequence(_net_s, _net_x, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def ssaappendpointandupdate(*functionargs):
    # unpack inputs
    s, x, updateits = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_x = x
    _net_updateits = updateits
    try:

        # call function
        _net_alglib.ssaappendpointandupdate(_net_s, _net_x, _net_updateits)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def ssaappendsequenceandupdate(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        s, x, nticks, updateits = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        s, x, updateits = functionargs
        nticks = check_equality_and_get([safe_len("'ssaappendsequenceandupdate': incorrect parameters",x)],"Error while calling 'ssaappendsequenceandupdate': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'ssaappendsequenceandupdate': function must have 4 or 3 parameters")

    # convert to .NET types
    _net_s = s.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.ssaappendsequenceandupdate' must be real vector")
    _net_nticks = nticks
    _net_updateits = updateits
    try:

        # call function
        _net_alglib.ssaappendsequenceandupdate(_net_s, _net_x, _net_nticks, _net_updateits)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def ssasetalgoprecomputed(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        s, a, windowwidth, nbasis = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        s, a = functionargs
        windowwidth = check_equality_and_get([safe_rows("'ssasetalgoprecomputed': incorrect parameters",a)],"Error while calling 'ssasetalgoprecomputed': looks like one of arguments has wrong size")
        nbasis = check_equality_and_get([safe_cols("'ssasetalgoprecomputed': incorrect parameters",a)],"Error while calling 'ssasetalgoprecomputed': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'ssasetalgoprecomputed': function must have 4 or 2 parameters")

    # convert to .NET types
    _net_s = s.ptr
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.ssasetalgoprecomputed' must be real matrix")
    _net_windowwidth = windowwidth
    _net_nbasis = nbasis
    try:

        # call function
        _net_alglib.ssasetalgoprecomputed(_net_s, _net_a, _net_windowwidth, _net_nbasis)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def ssasetalgotopkdirect(*functionargs):
    # unpack inputs
    s, topk = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_topk = topk
    try:

        # call function
        _net_alglib.ssasetalgotopkdirect(_net_s, _net_topk)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def ssasetalgotopkrealtime(*functionargs):
    # unpack inputs
    s, topk = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_topk = topk
    try:

        # call function
        _net_alglib.ssasetalgotopkrealtime(_net_s, _net_topk)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def ssacleardata(*functionargs):
    # unpack inputs
    s,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    try:

        # call function
        _net_alglib.ssacleardata(_net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def ssagetbasis(*functionargs):
    # unpack inputs
    s,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    try:

        # call function
        _net_a, _net_sv, _net_windowwidth, _net_nbasis = _net_alglib.ssagetbasis(_net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)
    sv = list_from_net(_net_sv, DT_REAL)
    windowwidth = _net_windowwidth
    nbasis = _net_nbasis

    # return
    return (a, sv, windowwidth, nbasis)

def ssagetlrr(*functionargs):
    # unpack inputs
    s,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    try:

        # call function
        _net_a, _net_windowwidth = _net_alglib.ssagetlrr(_net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = list_from_net(_net_a, DT_REAL)
    windowwidth = _net_windowwidth

    # return
    return (a, windowwidth)

def ssaanalyzelastwindow(*functionargs):
    # unpack inputs
    s,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    try:

        # call function
        _net_trend, _net_noise, _net_nticks = _net_alglib.ssaanalyzelastwindow(_net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    trend = list_from_net(_net_trend, DT_REAL)
    noise = list_from_net(_net_noise, DT_REAL)
    nticks = _net_nticks

    # return
    return (trend, noise, nticks)

def ssaanalyzelast(*functionargs):
    # unpack inputs
    s, nticks = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_nticks = nticks
    try:

        # call function
        _net_trend, _net_noise = _net_alglib.ssaanalyzelast(_net_s, _net_nticks)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    trend = list_from_net(_net_trend, DT_REAL)
    noise = list_from_net(_net_noise, DT_REAL)

    # return
    return (trend, noise)

def ssaanalyzesequence(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        s, data, nticks = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        s, data = functionargs
        nticks = check_equality_and_get([safe_len("'ssaanalyzesequence': incorrect parameters",data)],"Error while calling 'ssaanalyzesequence': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'ssaanalyzesequence': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_s = s.ptr
    _net_data = net_from_list(data, DT_REAL, "ALGLIB: parameter 'data' of 'xalglib.ssaanalyzesequence' must be real vector")
    _net_nticks = nticks
    try:

        # call function
        _net_trend, _net_noise = _net_alglib.ssaanalyzesequence(_net_s, _net_data, _net_nticks)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    trend = list_from_net(_net_trend, DT_REAL)
    noise = list_from_net(_net_noise, DT_REAL)

    # return
    return (trend, noise)

def ssaforecastlast(*functionargs):
    # unpack inputs
    s, nticks = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_nticks = nticks
    try:

        # call function
        _net_trend = _net_alglib.ssaforecastlast(_net_s, _net_nticks)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    trend = list_from_net(_net_trend, DT_REAL)

    # return
    return trend

def ssaforecastsequence(*functionargs):
    # unpack inputs
    if len(functionargs)==5:
        # full-form call
        s, data, datalen, forecastlen, applysmoothing = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        s, data, forecastlen = functionargs
        datalen = check_equality_and_get([safe_len("'ssaforecastsequence': incorrect parameters",data)],"Error while calling 'ssaforecastsequence': looks like one of arguments has wrong size")
        applysmoothing = check_equality_and_get([True],"Error while calling 'ssaforecastsequence': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'ssaforecastsequence': function must have 5 or 3 parameters")

    # convert to .NET types
    _net_s = s.ptr
    _net_data = net_from_list(data, DT_REAL, "ALGLIB: parameter 'data' of 'xalglib.ssaforecastsequence' must be real vector")
    _net_datalen = datalen
    _net_forecastlen = forecastlen
    _net_applysmoothing = applysmoothing
    try:

        # call function
        _net_trend = _net_alglib.ssaforecastsequence(_net_s, _net_data, _net_datalen, _net_forecastlen, _net_applysmoothing)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    trend = list_from_net(_net_trend, DT_REAL)

    # return
    return trend

def ssaforecastavglast(*functionargs):
    # unpack inputs
    s, m, nticks = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_m = m
    _net_nticks = nticks
    try:

        # call function
        _net_trend = _net_alglib.ssaforecastavglast(_net_s, _net_m, _net_nticks)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    trend = list_from_net(_net_trend, DT_REAL)

    # return
    return trend

def ssaforecastavgsequence(*functionargs):
    # unpack inputs
    if len(functionargs)==6:
        # full-form call
        s, data, datalen, m, forecastlen, applysmoothing = functionargs
        friendly_form = False
    elif len(functionargs)==4:
        # short-form call
        s, data, m, forecastlen = functionargs
        datalen = check_equality_and_get([safe_len("'ssaforecastavgsequence': incorrect parameters",data)],"Error while calling 'ssaforecastavgsequence': looks like one of arguments has wrong size")
        applysmoothing = check_equality_and_get([True],"Error while calling 'ssaforecastavgsequence': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'ssaforecastavgsequence': function must have 6 or 4 parameters")

    # convert to .NET types
    _net_s = s.ptr
    _net_data = net_from_list(data, DT_REAL, "ALGLIB: parameter 'data' of 'xalglib.ssaforecastavgsequence' must be real vector")
    _net_datalen = datalen
    _net_m = m
    _net_forecastlen = forecastlen
    _net_applysmoothing = applysmoothing
    try:

        # call function
        _net_trend = _net_alglib.ssaforecastavgsequence(_net_s, _net_data, _net_datalen, _net_m, _net_forecastlen, _net_applysmoothing)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    trend = list_from_net(_net_trend, DT_REAL)

    # return
    return trend

def gammafunction(*functionargs):
    # unpack inputs
    x,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.gammafunction(_net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def lngamma(*functionargs):
    # unpack inputs
    x,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = x
    try:

        # call function
        _net_result, _net_sgngam = _net_alglib.lngamma(_net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result
    sgngam = _net_sgngam

    # return
    return (result, sgngam)

def errorfunction(*functionargs):
    # unpack inputs
    x,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.errorfunction(_net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def errorfunctionc(*functionargs):
    # unpack inputs
    x,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.errorfunctionc(_net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def normaldistribution(*functionargs):
    # unpack inputs
    x,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.normaldistribution(_net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def inverf(*functionargs):
    # unpack inputs
    e,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_e = e
    try:

        # call function
        _net_result = _net_alglib.inverf(_net_e)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def invnormaldistribution(*functionargs):
    # unpack inputs
    y0,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_y0 = y0
    try:

        # call function
        _net_result = _net_alglib.invnormaldistribution(_net_y0)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def incompletegamma(*functionargs):
    # unpack inputs
    a, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = a
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.incompletegamma(_net_a, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def incompletegammac(*functionargs):
    # unpack inputs
    a, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = a
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.incompletegammac(_net_a, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def invincompletegammac(*functionargs):
    # unpack inputs
    a, y0 = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = a
    _net_y0 = y0
    try:

        # call function
        _net_result = _net_alglib.invincompletegammac(_net_a, _net_y0)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result



class linearmodel(object):
    def __init__(self,ptr):
        self.ptr = ptr


class lrreport(object):
    def __init__(self):
        self.c = [[]]
        self.rmserror = 0
        self.avgerror = 0
        self.avgrelerror = 0
        self.cvrmserror = 0
        self.cvavgerror = 0
        self.cvavgrelerror = 0
        self.ncvdefects = 0
        self.cvdefects = []


def net_from_lrreport(x,v):
    x.c = net_from_listlist(v.c, DT_REAL)
    x.rmserror = float(v.rmserror)
    x.avgerror = float(v.avgerror)
    x.avgrelerror = float(v.avgrelerror)
    x.cvrmserror = float(v.cvrmserror)
    x.cvavgerror = float(v.cvavgerror)
    x.cvavgrelerror = float(v.cvavgrelerror)
    x.ncvdefects = int(v.ncvdefects)
    x.cvdefects = net_from_list(v.cvdefects, DT_INT)
    return




def lrreport_from_net(x):
    r = lrreport()
    r.c = listlist_from_net(x.c, DT_REAL)
    r.rmserror = x.rmserror
    r.avgerror = x.avgerror
    r.avgrelerror = x.avgrelerror
    r.cvrmserror = x.cvrmserror
    r.cvavgerror = x.cvavgerror
    r.cvavgrelerror = x.cvavgrelerror
    r.ncvdefects = x.ncvdefects
    r.cvdefects = list_from_net(x.cvdefects, DT_INT)
    return r


def lrbuild(*functionargs):
    # unpack inputs
    xy, npoints, nvars = functionargs
    friendly_form = False

    # convert to .NET types
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.lrbuild' must be real matrix")
    _net_npoints = npoints
    _net_nvars = nvars
    try:

        # call function
        _net_info, _net_lm, _net_ar = _net_alglib.lrbuild(_net_xy, _net_npoints, _net_nvars)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    lm = linearmodel(_net_lm)
    ar = lrreport_from_net(_net_ar)

    # return
    return (info, lm, ar)

def lrbuilds(*functionargs):
    # unpack inputs
    xy, s, npoints, nvars = functionargs
    friendly_form = False

    # convert to .NET types
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.lrbuilds' must be real matrix")
    _net_s = net_from_list(s, DT_REAL, "ALGLIB: parameter 's' of 'xalglib.lrbuilds' must be real vector")
    _net_npoints = npoints
    _net_nvars = nvars
    try:

        # call function
        _net_info, _net_lm, _net_ar = _net_alglib.lrbuilds(_net_xy, _net_s, _net_npoints, _net_nvars)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    lm = linearmodel(_net_lm)
    ar = lrreport_from_net(_net_ar)

    # return
    return (info, lm, ar)

def lrbuildzs(*functionargs):
    # unpack inputs
    xy, s, npoints, nvars = functionargs
    friendly_form = False

    # convert to .NET types
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.lrbuildzs' must be real matrix")
    _net_s = net_from_list(s, DT_REAL, "ALGLIB: parameter 's' of 'xalglib.lrbuildzs' must be real vector")
    _net_npoints = npoints
    _net_nvars = nvars
    try:

        # call function
        _net_info, _net_lm, _net_ar = _net_alglib.lrbuildzs(_net_xy, _net_s, _net_npoints, _net_nvars)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    lm = linearmodel(_net_lm)
    ar = lrreport_from_net(_net_ar)

    # return
    return (info, lm, ar)

def lrbuildz(*functionargs):
    # unpack inputs
    xy, npoints, nvars = functionargs
    friendly_form = False

    # convert to .NET types
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.lrbuildz' must be real matrix")
    _net_npoints = npoints
    _net_nvars = nvars
    try:

        # call function
        _net_info, _net_lm, _net_ar = _net_alglib.lrbuildz(_net_xy, _net_npoints, _net_nvars)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    lm = linearmodel(_net_lm)
    ar = lrreport_from_net(_net_ar)

    # return
    return (info, lm, ar)

def lrunpack(*functionargs):
    # unpack inputs
    lm,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_lm = lm.ptr
    try:

        # call function
        _net_v, _net_nvars = _net_alglib.lrunpack(_net_lm)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    v = list_from_net(_net_v, DT_REAL)
    nvars = _net_nvars

    # return
    return (v, nvars)

def lrpack(*functionargs):
    # unpack inputs
    v, nvars = functionargs
    friendly_form = False

    # convert to .NET types
    _net_v = net_from_list(v, DT_REAL, "ALGLIB: parameter 'v' of 'xalglib.lrpack' must be real vector")
    _net_nvars = nvars
    try:

        # call function
        _net_lm = _net_alglib.lrpack(_net_v, _net_nvars)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    lm = linearmodel(_net_lm)

    # return
    return lm

def lrprocess(*functionargs):
    # unpack inputs
    lm, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_lm = lm.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.lrprocess' must be real vector")
    try:

        # call function
        _net_result = _net_alglib.lrprocess(_net_lm, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def lrrmserror(*functionargs):
    # unpack inputs
    lm, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_lm = lm.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.lrrmserror' must be real matrix")
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.lrrmserror(_net_lm, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def lravgerror(*functionargs):
    # unpack inputs
    lm, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_lm = lm.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.lravgerror' must be real matrix")
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.lravgerror(_net_lm, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def lravgrelerror(*functionargs):
    # unpack inputs
    lm, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_lm = lm.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.lravgrelerror' must be real matrix")
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.lravgrelerror(_net_lm, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def filtersma(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        x, n, k = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        x, k = functionargs
        n = check_equality_and_get([safe_len("'filtersma': incorrect parameters",x)],"Error while calling 'filtersma': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'filtersma': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.filtersma' must be real vector")
    _net_n = n
    _net_k = k
    try:

        # call function
        _net_x = _net_alglib.filtersma(_net_x, _net_n, _net_k)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = list_from_net(_net_x, DT_REAL)

    # return
    return x

def filterema(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        x, n, alpha = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        x, alpha = functionargs
        n = check_equality_and_get([safe_len("'filterema': incorrect parameters",x)],"Error while calling 'filterema': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'filterema': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.filterema' must be real vector")
    _net_n = n
    _net_alpha = alpha
    try:

        # call function
        _net_x = _net_alglib.filterema(_net_x, _net_n, _net_alpha)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = list_from_net(_net_x, DT_REAL)

    # return
    return x

def filterlrma(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        x, n, k = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        x, k = functionargs
        n = check_equality_and_get([safe_len("'filterlrma': incorrect parameters",x)],"Error while calling 'filterlrma': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'filterlrma': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.filterlrma' must be real vector")
    _net_n = n
    _net_k = k
    try:

        # call function
        _net_x = _net_alglib.filterlrma(_net_x, _net_n, _net_k)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = list_from_net(_net_x, DT_REAL)

    # return
    return x



class logitmodel(object):
    def __init__(self,ptr):
        self.ptr = ptr


class mnlreport(object):
    def __init__(self):
        self.ngrad = 0
        self.nhess = 0


def net_from_mnlreport(x,v):
    x.ngrad = int(v.ngrad)
    x.nhess = int(v.nhess)
    return




def mnlreport_from_net(x):
    r = mnlreport()
    r.ngrad = x.ngrad
    r.nhess = x.nhess
    return r


def mnltrainh(*functionargs):
    # unpack inputs
    xy, npoints, nvars, nclasses = functionargs
    friendly_form = False

    # convert to .NET types
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mnltrainh' must be real matrix")
    _net_npoints = npoints
    _net_nvars = nvars
    _net_nclasses = nclasses
    try:

        # call function
        _net_info, _net_lm, _net_rep = _net_alglib.mnltrainh(_net_xy, _net_npoints, _net_nvars, _net_nclasses)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    lm = logitmodel(_net_lm)
    rep = mnlreport_from_net(_net_rep)

    # return
    return (info, lm, rep)

def mnlprocess(*functionargs):
    # unpack inputs
    lm, x, y = functionargs
    friendly_form = False

    # convert to .NET types
    _net_lm = lm.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.mnlprocess' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.mnlprocess' must be real vector")
    try:

        # call function
        _net_y = _net_alglib.mnlprocess(_net_lm, _net_x, _net_y)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    y = list_from_net(_net_y, DT_REAL)

    # return
    return y

def mnlprocessi(*functionargs):
    # unpack inputs
    lm, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_lm = lm.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.mnlprocessi' must be real vector")
    try:

        # call function
        _net_y = _net_alglib.mnlprocessi(_net_lm, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    y = list_from_net(_net_y, DT_REAL)

    # return
    return y

def mnlunpack(*functionargs):
    # unpack inputs
    lm,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_lm = lm.ptr
    try:

        # call function
        _net_a, _net_nvars, _net_nclasses = _net_alglib.mnlunpack(_net_lm)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = listlist_from_net(_net_a, DT_REAL)
    nvars = _net_nvars
    nclasses = _net_nclasses

    # return
    return (a, nvars, nclasses)

def mnlpack(*functionargs):
    # unpack inputs
    a, nvars, nclasses = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.mnlpack' must be real matrix")
    _net_nvars = nvars
    _net_nclasses = nclasses
    try:

        # call function
        _net_lm = _net_alglib.mnlpack(_net_a, _net_nvars, _net_nclasses)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    lm = logitmodel(_net_lm)

    # return
    return lm

def mnlavgce(*functionargs):
    # unpack inputs
    lm, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_lm = lm.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mnlavgce' must be real matrix")
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.mnlavgce(_net_lm, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def mnlrelclserror(*functionargs):
    # unpack inputs
    lm, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_lm = lm.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mnlrelclserror' must be real matrix")
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.mnlrelclserror(_net_lm, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def mnlrmserror(*functionargs):
    # unpack inputs
    lm, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_lm = lm.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mnlrmserror' must be real matrix")
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.mnlrmserror(_net_lm, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def mnlavgerror(*functionargs):
    # unpack inputs
    lm, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_lm = lm.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mnlavgerror' must be real matrix")
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.mnlavgerror(_net_lm, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def mnlavgrelerror(*functionargs):
    # unpack inputs
    lm, xy, ssize = functionargs
    friendly_form = False

    # convert to .NET types
    _net_lm = lm.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mnlavgrelerror' must be real matrix")
    _net_ssize = ssize
    try:

        # call function
        _net_result = _net_alglib.mnlavgrelerror(_net_lm, _net_xy, _net_ssize)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def mnlclserror(*functionargs):
    # unpack inputs
    lm, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_lm = lm.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mnlclserror' must be real matrix")
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.mnlclserror(_net_lm, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result



class mcpdstate(object):
    def __init__(self,ptr):
        self.ptr = ptr


class mcpdreport(object):
    def __init__(self):
        self.inneriterationscount = 0
        self.outeriterationscount = 0
        self.nfev = 0
        self.terminationtype = 0


def net_from_mcpdreport(x,v):
    x.inneriterationscount = int(v.inneriterationscount)
    x.outeriterationscount = int(v.outeriterationscount)
    x.nfev = int(v.nfev)
    x.terminationtype = int(v.terminationtype)
    return




def mcpdreport_from_net(x):
    r = mcpdreport()
    r.inneriterationscount = x.inneriterationscount
    r.outeriterationscount = x.outeriterationscount
    r.nfev = x.nfev
    r.terminationtype = x.terminationtype
    return r


def mcpdcreate(*functionargs):
    # unpack inputs
    n,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    try:

        # call function
        _net_s = _net_alglib.mcpdcreate(_net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    s = mcpdstate(_net_s)

    # return
    return s

def mcpdcreateentry(*functionargs):
    # unpack inputs
    n, entrystate = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    _net_entrystate = entrystate
    try:

        # call function
        _net_s = _net_alglib.mcpdcreateentry(_net_n, _net_entrystate)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    s = mcpdstate(_net_s)

    # return
    return s

def mcpdcreateexit(*functionargs):
    # unpack inputs
    n, exitstate = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    _net_exitstate = exitstate
    try:

        # call function
        _net_s = _net_alglib.mcpdcreateexit(_net_n, _net_exitstate)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    s = mcpdstate(_net_s)

    # return
    return s

def mcpdcreateentryexit(*functionargs):
    # unpack inputs
    n, entrystate, exitstate = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    _net_entrystate = entrystate
    _net_exitstate = exitstate
    try:

        # call function
        _net_s = _net_alglib.mcpdcreateentryexit(_net_n, _net_entrystate, _net_exitstate)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    s = mcpdstate(_net_s)

    # return
    return s

def mcpdaddtrack(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        s, xy, k = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        s, xy = functionargs
        k = check_equality_and_get([safe_rows("'mcpdaddtrack': incorrect parameters",xy)],"Error while calling 'mcpdaddtrack': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'mcpdaddtrack': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_s = s.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mcpdaddtrack' must be real matrix")
    _net_k = k
    try:

        # call function
        _net_alglib.mcpdaddtrack(_net_s, _net_xy, _net_k)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mcpdsetec(*functionargs):
    # unpack inputs
    s, ec = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_ec = net_from_listlist(ec, DT_REAL, "ALGLIB: parameter 'ec' of 'xalglib.mcpdsetec' must be real matrix")
    try:

        # call function
        _net_alglib.mcpdsetec(_net_s, _net_ec)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mcpdaddec(*functionargs):
    # unpack inputs
    s, i, j, c = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_i = i
    _net_j = j
    _net_c = c
    try:

        # call function
        _net_alglib.mcpdaddec(_net_s, _net_i, _net_j, _net_c)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mcpdsetbc(*functionargs):
    # unpack inputs
    s, bndl, bndu = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_bndl = net_from_listlist(bndl, DT_REAL, "ALGLIB: parameter 'bndl' of 'xalglib.mcpdsetbc' must be real matrix")
    _net_bndu = net_from_listlist(bndu, DT_REAL, "ALGLIB: parameter 'bndu' of 'xalglib.mcpdsetbc' must be real matrix")
    try:

        # call function
        _net_alglib.mcpdsetbc(_net_s, _net_bndl, _net_bndu)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mcpdaddbc(*functionargs):
    # unpack inputs
    s, i, j, bndl, bndu = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_i = i
    _net_j = j
    _net_bndl = bndl
    _net_bndu = bndu
    try:

        # call function
        _net_alglib.mcpdaddbc(_net_s, _net_i, _net_j, _net_bndl, _net_bndu)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mcpdsetlc(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        s, c, ct, k = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        s, c, ct = functionargs
        k = check_equality_and_get([safe_rows("'mcpdsetlc': incorrect parameters",c), safe_len("'mcpdsetlc': incorrect parameters",ct)],"Error while calling 'mcpdsetlc': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'mcpdsetlc': function must have 4 or 3 parameters")

    # convert to .NET types
    _net_s = s.ptr
    _net_c = net_from_listlist(c, DT_REAL, "ALGLIB: parameter 'c' of 'xalglib.mcpdsetlc' must be real matrix")
    _net_ct = net_from_list(ct, DT_INT, "ALGLIB: parameter 'ct' of 'xalglib.mcpdsetlc' must be int vector")
    _net_k = k
    try:

        # call function
        _net_alglib.mcpdsetlc(_net_s, _net_c, _net_ct, _net_k)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mcpdsettikhonovregularizer(*functionargs):
    # unpack inputs
    s, v = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_v = v
    try:

        # call function
        _net_alglib.mcpdsettikhonovregularizer(_net_s, _net_v)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mcpdsetprior(*functionargs):
    # unpack inputs
    s, pp = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_pp = net_from_listlist(pp, DT_REAL, "ALGLIB: parameter 'pp' of 'xalglib.mcpdsetprior' must be real matrix")
    try:

        # call function
        _net_alglib.mcpdsetprior(_net_s, _net_pp)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mcpdsetpredictionweights(*functionargs):
    # unpack inputs
    s, pw = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_pw = net_from_list(pw, DT_REAL, "ALGLIB: parameter 'pw' of 'xalglib.mcpdsetpredictionweights' must be real vector")
    try:

        # call function
        _net_alglib.mcpdsetpredictionweights(_net_s, _net_pw)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mcpdsolve(*functionargs):
    # unpack inputs
    s,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    try:

        # call function
        _net_alglib.mcpdsolve(_net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mcpdresults(*functionargs):
    # unpack inputs
    s,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    try:

        # call function
        _net_p, _net_rep = _net_alglib.mcpdresults(_net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    p = listlist_from_net(_net_p, DT_REAL)
    rep = mcpdreport_from_net(_net_rep)

    # return
    return (p, rep)



class mlpensemble(object):
    def __init__(self,ptr):
        self.ptr = ptr
def mlpeserialize(obj):
    try:
        return _net_alglib.mlpeserialize(obj.ptr)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

def mlpeunserialize(s_in):
    try:
        return mlpensemble(_net_alglib.mlpeunserialize(s_in))
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)
def mlpecreate0(*functionargs):
    # unpack inputs
    nin, nout, ensemblesize = functionargs
    friendly_form = False

    # convert to .NET types
    _net_nin = nin
    _net_nout = nout
    _net_ensemblesize = ensemblesize
    try:

        # call function
        _net_ensemble = _net_alglib.mlpecreate0(_net_nin, _net_nout, _net_ensemblesize)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    ensemble = mlpensemble(_net_ensemble)

    # return
    return ensemble

def mlpecreate1(*functionargs):
    # unpack inputs
    nin, nhid, nout, ensemblesize = functionargs
    friendly_form = False

    # convert to .NET types
    _net_nin = nin
    _net_nhid = nhid
    _net_nout = nout
    _net_ensemblesize = ensemblesize
    try:

        # call function
        _net_ensemble = _net_alglib.mlpecreate1(_net_nin, _net_nhid, _net_nout, _net_ensemblesize)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    ensemble = mlpensemble(_net_ensemble)

    # return
    return ensemble

def mlpecreate2(*functionargs):
    # unpack inputs
    nin, nhid1, nhid2, nout, ensemblesize = functionargs
    friendly_form = False

    # convert to .NET types
    _net_nin = nin
    _net_nhid1 = nhid1
    _net_nhid2 = nhid2
    _net_nout = nout
    _net_ensemblesize = ensemblesize
    try:

        # call function
        _net_ensemble = _net_alglib.mlpecreate2(_net_nin, _net_nhid1, _net_nhid2, _net_nout, _net_ensemblesize)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    ensemble = mlpensemble(_net_ensemble)

    # return
    return ensemble

def mlpecreateb0(*functionargs):
    # unpack inputs
    nin, nout, b, d, ensemblesize = functionargs
    friendly_form = False

    # convert to .NET types
    _net_nin = nin
    _net_nout = nout
    _net_b = b
    _net_d = d
    _net_ensemblesize = ensemblesize
    try:

        # call function
        _net_ensemble = _net_alglib.mlpecreateb0(_net_nin, _net_nout, _net_b, _net_d, _net_ensemblesize)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    ensemble = mlpensemble(_net_ensemble)

    # return
    return ensemble

def mlpecreateb1(*functionargs):
    # unpack inputs
    nin, nhid, nout, b, d, ensemblesize = functionargs
    friendly_form = False

    # convert to .NET types
    _net_nin = nin
    _net_nhid = nhid
    _net_nout = nout
    _net_b = b
    _net_d = d
    _net_ensemblesize = ensemblesize
    try:

        # call function
        _net_ensemble = _net_alglib.mlpecreateb1(_net_nin, _net_nhid, _net_nout, _net_b, _net_d, _net_ensemblesize)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    ensemble = mlpensemble(_net_ensemble)

    # return
    return ensemble

def mlpecreateb2(*functionargs):
    # unpack inputs
    nin, nhid1, nhid2, nout, b, d, ensemblesize = functionargs
    friendly_form = False

    # convert to .NET types
    _net_nin = nin
    _net_nhid1 = nhid1
    _net_nhid2 = nhid2
    _net_nout = nout
    _net_b = b
    _net_d = d
    _net_ensemblesize = ensemblesize
    try:

        # call function
        _net_ensemble = _net_alglib.mlpecreateb2(_net_nin, _net_nhid1, _net_nhid2, _net_nout, _net_b, _net_d, _net_ensemblesize)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    ensemble = mlpensemble(_net_ensemble)

    # return
    return ensemble

def mlpecreater0(*functionargs):
    # unpack inputs
    nin, nout, a, b, ensemblesize = functionargs
    friendly_form = False

    # convert to .NET types
    _net_nin = nin
    _net_nout = nout
    _net_a = a
    _net_b = b
    _net_ensemblesize = ensemblesize
    try:

        # call function
        _net_ensemble = _net_alglib.mlpecreater0(_net_nin, _net_nout, _net_a, _net_b, _net_ensemblesize)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    ensemble = mlpensemble(_net_ensemble)

    # return
    return ensemble

def mlpecreater1(*functionargs):
    # unpack inputs
    nin, nhid, nout, a, b, ensemblesize = functionargs
    friendly_form = False

    # convert to .NET types
    _net_nin = nin
    _net_nhid = nhid
    _net_nout = nout
    _net_a = a
    _net_b = b
    _net_ensemblesize = ensemblesize
    try:

        # call function
        _net_ensemble = _net_alglib.mlpecreater1(_net_nin, _net_nhid, _net_nout, _net_a, _net_b, _net_ensemblesize)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    ensemble = mlpensemble(_net_ensemble)

    # return
    return ensemble

def mlpecreater2(*functionargs):
    # unpack inputs
    nin, nhid1, nhid2, nout, a, b, ensemblesize = functionargs
    friendly_form = False

    # convert to .NET types
    _net_nin = nin
    _net_nhid1 = nhid1
    _net_nhid2 = nhid2
    _net_nout = nout
    _net_a = a
    _net_b = b
    _net_ensemblesize = ensemblesize
    try:

        # call function
        _net_ensemble = _net_alglib.mlpecreater2(_net_nin, _net_nhid1, _net_nhid2, _net_nout, _net_a, _net_b, _net_ensemblesize)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    ensemble = mlpensemble(_net_ensemble)

    # return
    return ensemble

def mlpecreatec0(*functionargs):
    # unpack inputs
    nin, nout, ensemblesize = functionargs
    friendly_form = False

    # convert to .NET types
    _net_nin = nin
    _net_nout = nout
    _net_ensemblesize = ensemblesize
    try:

        # call function
        _net_ensemble = _net_alglib.mlpecreatec0(_net_nin, _net_nout, _net_ensemblesize)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    ensemble = mlpensemble(_net_ensemble)

    # return
    return ensemble

def mlpecreatec1(*functionargs):
    # unpack inputs
    nin, nhid, nout, ensemblesize = functionargs
    friendly_form = False

    # convert to .NET types
    _net_nin = nin
    _net_nhid = nhid
    _net_nout = nout
    _net_ensemblesize = ensemblesize
    try:

        # call function
        _net_ensemble = _net_alglib.mlpecreatec1(_net_nin, _net_nhid, _net_nout, _net_ensemblesize)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    ensemble = mlpensemble(_net_ensemble)

    # return
    return ensemble

def mlpecreatec2(*functionargs):
    # unpack inputs
    nin, nhid1, nhid2, nout, ensemblesize = functionargs
    friendly_form = False

    # convert to .NET types
    _net_nin = nin
    _net_nhid1 = nhid1
    _net_nhid2 = nhid2
    _net_nout = nout
    _net_ensemblesize = ensemblesize
    try:

        # call function
        _net_ensemble = _net_alglib.mlpecreatec2(_net_nin, _net_nhid1, _net_nhid2, _net_nout, _net_ensemblesize)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    ensemble = mlpensemble(_net_ensemble)

    # return
    return ensemble

def mlpecreatefromnetwork(*functionargs):
    # unpack inputs
    network, ensemblesize = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_ensemblesize = ensemblesize
    try:

        # call function
        _net_ensemble = _net_alglib.mlpecreatefromnetwork(_net_network, _net_ensemblesize)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    ensemble = mlpensemble(_net_ensemble)

    # return
    return ensemble

def mlperandomize(*functionargs):
    # unpack inputs
    ensemble,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_ensemble = ensemble.ptr
    try:

        # call function
        _net_alglib.mlperandomize(_net_ensemble)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mlpeproperties(*functionargs):
    # unpack inputs
    ensemble,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_ensemble = ensemble.ptr
    try:

        # call function
        _net_nin, _net_nout = _net_alglib.mlpeproperties(_net_ensemble)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    nin = _net_nin
    nout = _net_nout

    # return
    return (nin, nout)

def mlpeissoftmax(*functionargs):
    # unpack inputs
    ensemble,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_ensemble = ensemble.ptr
    try:

        # call function
        _net_result = _net_alglib.mlpeissoftmax(_net_ensemble)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def mlpeprocess(*functionargs):
    # unpack inputs
    ensemble, x, y = functionargs
    friendly_form = False

    # convert to .NET types
    _net_ensemble = ensemble.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.mlpeprocess' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.mlpeprocess' must be real vector")
    try:

        # call function
        _net_y = _net_alglib.mlpeprocess(_net_ensemble, _net_x, _net_y)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    y = list_from_net(_net_y, DT_REAL)

    # return
    return y

def mlpeprocessi(*functionargs):
    # unpack inputs
    ensemble, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_ensemble = ensemble.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.mlpeprocessi' must be real vector")
    try:

        # call function
        _net_y = _net_alglib.mlpeprocessi(_net_ensemble, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    y = list_from_net(_net_y, DT_REAL)

    # return
    return y

def mlperelclserror(*functionargs):
    # unpack inputs
    ensemble, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_ensemble = ensemble.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mlperelclserror' must be real matrix")
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.mlperelclserror(_net_ensemble, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def mlpeavgce(*functionargs):
    # unpack inputs
    ensemble, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_ensemble = ensemble.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mlpeavgce' must be real matrix")
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.mlpeavgce(_net_ensemble, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def mlpermserror(*functionargs):
    # unpack inputs
    ensemble, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_ensemble = ensemble.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mlpermserror' must be real matrix")
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.mlpermserror(_net_ensemble, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def mlpeavgerror(*functionargs):
    # unpack inputs
    ensemble, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_ensemble = ensemble.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mlpeavgerror' must be real matrix")
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.mlpeavgerror(_net_ensemble, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def mlpeavgrelerror(*functionargs):
    # unpack inputs
    ensemble, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_ensemble = ensemble.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mlpeavgrelerror' must be real matrix")
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.mlpeavgrelerror(_net_ensemble, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result



class mlpreport(object):
    def __init__(self):
        self.relclserror = 0
        self.avgce = 0
        self.rmserror = 0
        self.avgerror = 0
        self.avgrelerror = 0
        self.ngrad = 0
        self.nhess = 0
        self.ncholesky = 0


def net_from_mlpreport(x,v):
    x.relclserror = float(v.relclserror)
    x.avgce = float(v.avgce)
    x.rmserror = float(v.rmserror)
    x.avgerror = float(v.avgerror)
    x.avgrelerror = float(v.avgrelerror)
    x.ngrad = int(v.ngrad)
    x.nhess = int(v.nhess)
    x.ncholesky = int(v.ncholesky)
    return




def mlpreport_from_net(x):
    r = mlpreport()
    r.relclserror = x.relclserror
    r.avgce = x.avgce
    r.rmserror = x.rmserror
    r.avgerror = x.avgerror
    r.avgrelerror = x.avgrelerror
    r.ngrad = x.ngrad
    r.nhess = x.nhess
    r.ncholesky = x.ncholesky
    return r




class mlpcvreport(object):
    def __init__(self):
        self.relclserror = 0
        self.avgce = 0
        self.rmserror = 0
        self.avgerror = 0
        self.avgrelerror = 0


def net_from_mlpcvreport(x,v):
    x.relclserror = float(v.relclserror)
    x.avgce = float(v.avgce)
    x.rmserror = float(v.rmserror)
    x.avgerror = float(v.avgerror)
    x.avgrelerror = float(v.avgrelerror)
    return




def mlpcvreport_from_net(x):
    r = mlpcvreport()
    r.relclserror = x.relclserror
    r.avgce = x.avgce
    r.rmserror = x.rmserror
    r.avgerror = x.avgerror
    r.avgrelerror = x.avgrelerror
    return r




class mlptrainer(object):
    def __init__(self,ptr):
        self.ptr = ptr
def mlptrainlm(*functionargs):
    # unpack inputs
    network, xy, npoints, decay, restarts = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mlptrainlm' must be real matrix")
    _net_npoints = npoints
    _net_decay = decay
    _net_restarts = restarts
    try:

        # call function
        _net_info, _net_rep = _net_alglib.mlptrainlm(_net_network, _net_xy, _net_npoints, _net_decay, _net_restarts)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = mlpreport_from_net(_net_rep)

    # return
    return (info, rep)

def mlptrainlbfgs(*functionargs):
    # unpack inputs
    network, xy, npoints, decay, restarts, wstep, maxits = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mlptrainlbfgs' must be real matrix")
    _net_npoints = npoints
    _net_decay = decay
    _net_restarts = restarts
    _net_wstep = wstep
    _net_maxits = maxits
    try:

        # call function
        _net_info, _net_rep = _net_alglib.mlptrainlbfgs(_net_network, _net_xy, _net_npoints, _net_decay, _net_restarts, _net_wstep, _net_maxits)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = mlpreport_from_net(_net_rep)

    # return
    return (info, rep)

def mlptraines(*functionargs):
    # unpack inputs
    network, trnxy, trnsize, valxy, valsize, decay, restarts = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_trnxy = net_from_listlist(trnxy, DT_REAL, "ALGLIB: parameter 'trnxy' of 'xalglib.mlptraines' must be real matrix")
    _net_trnsize = trnsize
    _net_valxy = net_from_listlist(valxy, DT_REAL, "ALGLIB: parameter 'valxy' of 'xalglib.mlptraines' must be real matrix")
    _net_valsize = valsize
    _net_decay = decay
    _net_restarts = restarts
    try:

        # call function
        _net_info, _net_rep = _net_alglib.mlptraines(_net_network, _net_trnxy, _net_trnsize, _net_valxy, _net_valsize, _net_decay, _net_restarts)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = mlpreport_from_net(_net_rep)

    # return
    return (info, rep)

def mlpkfoldcvlbfgs(*functionargs):
    # unpack inputs
    network, xy, npoints, decay, restarts, wstep, maxits, foldscount = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mlpkfoldcvlbfgs' must be real matrix")
    _net_npoints = npoints
    _net_decay = decay
    _net_restarts = restarts
    _net_wstep = wstep
    _net_maxits = maxits
    _net_foldscount = foldscount
    try:

        # call function
        _net_info, _net_rep, _net_cvrep = _net_alglib.mlpkfoldcvlbfgs(_net_network, _net_xy, _net_npoints, _net_decay, _net_restarts, _net_wstep, _net_maxits, _net_foldscount)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = mlpreport_from_net(_net_rep)
    cvrep = mlpcvreport_from_net(_net_cvrep)

    # return
    return (info, rep, cvrep)

def mlpkfoldcvlm(*functionargs):
    # unpack inputs
    network, xy, npoints, decay, restarts, foldscount = functionargs
    friendly_form = False

    # convert to .NET types
    _net_network = network.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mlpkfoldcvlm' must be real matrix")
    _net_npoints = npoints
    _net_decay = decay
    _net_restarts = restarts
    _net_foldscount = foldscount
    try:

        # call function
        _net_info, _net_rep, _net_cvrep = _net_alglib.mlpkfoldcvlm(_net_network, _net_xy, _net_npoints, _net_decay, _net_restarts, _net_foldscount)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = mlpreport_from_net(_net_rep)
    cvrep = mlpcvreport_from_net(_net_cvrep)

    # return
    return (info, rep, cvrep)

def mlpkfoldcv(*functionargs):
    # unpack inputs
    s, network, nrestarts, foldscount = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_network = network.ptr
    _net_nrestarts = nrestarts
    _net_foldscount = foldscount
    try:

        # call function
        _net_rep = _net_alglib.mlpkfoldcv(_net_s, _net_network, _net_nrestarts, _net_foldscount)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    rep = mlpreport_from_net(_net_rep)

    # return
    return rep

def smp_mlpkfoldcv(*functionargs):
    # unpack inputs
    s, network, nrestarts, foldscount = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_network = network.ptr
    _net_nrestarts = nrestarts
    _net_foldscount = foldscount
    try:

        # call function
        _net_rep = _net_alglib.smp_mlpkfoldcv(_net_s, _net_network, _net_nrestarts, _net_foldscount)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    rep = mlpreport_from_net(_net_rep)

    # return
    return rep

def mlpcreatetrainer(*functionargs):
    # unpack inputs
    nin, nout = functionargs
    friendly_form = False

    # convert to .NET types
    _net_nin = nin
    _net_nout = nout
    try:

        # call function
        _net_s = _net_alglib.mlpcreatetrainer(_net_nin, _net_nout)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    s = mlptrainer(_net_s)

    # return
    return s

def mlpcreatetrainercls(*functionargs):
    # unpack inputs
    nin, nclasses = functionargs
    friendly_form = False

    # convert to .NET types
    _net_nin = nin
    _net_nclasses = nclasses
    try:

        # call function
        _net_s = _net_alglib.mlpcreatetrainercls(_net_nin, _net_nclasses)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    s = mlptrainer(_net_s)

    # return
    return s

def mlpsetdataset(*functionargs):
    # unpack inputs
    s, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mlpsetdataset' must be real matrix")
    _net_npoints = npoints
    try:

        # call function
        _net_alglib.mlpsetdataset(_net_s, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mlpsetsparsedataset(*functionargs):
    # unpack inputs
    s, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_xy = xy.ptr
    _net_npoints = npoints
    try:

        # call function
        _net_alglib.mlpsetsparsedataset(_net_s, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mlpsetdecay(*functionargs):
    # unpack inputs
    s, decay = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_decay = decay
    try:

        # call function
        _net_alglib.mlpsetdecay(_net_s, _net_decay)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mlpsetcond(*functionargs):
    # unpack inputs
    s, wstep, maxits = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_wstep = wstep
    _net_maxits = maxits
    try:

        # call function
        _net_alglib.mlpsetcond(_net_s, _net_wstep, _net_maxits)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mlpsetalgobatch(*functionargs):
    # unpack inputs
    s,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    try:

        # call function
        _net_alglib.mlpsetalgobatch(_net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mlptrainnetwork(*functionargs):
    # unpack inputs
    s, network, nrestarts = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_network = network.ptr
    _net_nrestarts = nrestarts
    try:

        # call function
        _net_rep = _net_alglib.mlptrainnetwork(_net_s, _net_network, _net_nrestarts)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    rep = mlpreport_from_net(_net_rep)

    # return
    return rep

def smp_mlptrainnetwork(*functionargs):
    # unpack inputs
    s, network, nrestarts = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_network = network.ptr
    _net_nrestarts = nrestarts
    try:

        # call function
        _net_rep = _net_alglib.smp_mlptrainnetwork(_net_s, _net_network, _net_nrestarts)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    rep = mlpreport_from_net(_net_rep)

    # return
    return rep

def mlpstarttraining(*functionargs):
    # unpack inputs
    s, network, randomstart = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_network = network.ptr
    _net_randomstart = randomstart
    try:

        # call function
        _net_alglib.mlpstarttraining(_net_s, _net_network, _net_randomstart)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def mlpcontinuetraining(*functionargs):
    # unpack inputs
    s, network = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_network = network.ptr
    try:

        # call function
        _net_result = _net_alglib.mlpcontinuetraining(_net_s, _net_network)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def smp_mlpcontinuetraining(*functionargs):
    # unpack inputs
    s, network = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_network = network.ptr
    try:

        # call function
        _net_result = _net_alglib.smp_mlpcontinuetraining(_net_s, _net_network)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def mlpebagginglm(*functionargs):
    # unpack inputs
    ensemble, xy, npoints, decay, restarts = functionargs
    friendly_form = False

    # convert to .NET types
    _net_ensemble = ensemble.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mlpebagginglm' must be real matrix")
    _net_npoints = npoints
    _net_decay = decay
    _net_restarts = restarts
    try:

        # call function
        _net_info, _net_rep, _net_ooberrors = _net_alglib.mlpebagginglm(_net_ensemble, _net_xy, _net_npoints, _net_decay, _net_restarts)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = mlpreport_from_net(_net_rep)
    ooberrors = mlpcvreport_from_net(_net_ooberrors)

    # return
    return (info, rep, ooberrors)

def mlpebagginglbfgs(*functionargs):
    # unpack inputs
    ensemble, xy, npoints, decay, restarts, wstep, maxits = functionargs
    friendly_form = False

    # convert to .NET types
    _net_ensemble = ensemble.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mlpebagginglbfgs' must be real matrix")
    _net_npoints = npoints
    _net_decay = decay
    _net_restarts = restarts
    _net_wstep = wstep
    _net_maxits = maxits
    try:

        # call function
        _net_info, _net_rep, _net_ooberrors = _net_alglib.mlpebagginglbfgs(_net_ensemble, _net_xy, _net_npoints, _net_decay, _net_restarts, _net_wstep, _net_maxits)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = mlpreport_from_net(_net_rep)
    ooberrors = mlpcvreport_from_net(_net_ooberrors)

    # return
    return (info, rep, ooberrors)

def mlpetraines(*functionargs):
    # unpack inputs
    ensemble, xy, npoints, decay, restarts = functionargs
    friendly_form = False

    # convert to .NET types
    _net_ensemble = ensemble.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.mlpetraines' must be real matrix")
    _net_npoints = npoints
    _net_decay = decay
    _net_restarts = restarts
    try:

        # call function
        _net_info, _net_rep = _net_alglib.mlpetraines(_net_ensemble, _net_xy, _net_npoints, _net_decay, _net_restarts)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    rep = mlpreport_from_net(_net_rep)

    # return
    return (info, rep)

def mlptrainensemblees(*functionargs):
    # unpack inputs
    s, ensemble, nrestarts = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_ensemble = ensemble.ptr
    _net_nrestarts = nrestarts
    try:

        # call function
        _net_rep = _net_alglib.mlptrainensemblees(_net_s, _net_ensemble, _net_nrestarts)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    rep = mlpreport_from_net(_net_rep)

    # return
    return rep

def smp_mlptrainensemblees(*functionargs):
    # unpack inputs
    s, ensemble, nrestarts = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_ensemble = ensemble.ptr
    _net_nrestarts = nrestarts
    try:

        # call function
        _net_rep = _net_alglib.smp_mlptrainensemblees(_net_s, _net_ensemble, _net_nrestarts)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    rep = mlpreport_from_net(_net_rep)

    # return
    return rep



class clusterizerstate(object):
    def __init__(self,ptr):
        self.ptr = ptr


class ahcreport(object):
    def __init__(self):
        self.terminationtype = 0
        self.npoints = 0
        self.p = []
        self.z = [[]]
        self.pz = [[]]
        self.pm = [[]]
        self.mergedist = []


def net_from_ahcreport(x,v):
    x.terminationtype = int(v.terminationtype)
    x.npoints = int(v.npoints)
    x.p = net_from_list(v.p, DT_INT)
    x.z = net_from_listlist(v.z, DT_INT)
    x.pz = net_from_listlist(v.pz, DT_INT)
    x.pm = net_from_listlist(v.pm, DT_INT)
    x.mergedist = net_from_list(v.mergedist, DT_REAL)
    return




def ahcreport_from_net(x):
    r = ahcreport()
    r.terminationtype = x.terminationtype
    r.npoints = x.npoints
    r.p = list_from_net(x.p, DT_INT)
    r.z = listlist_from_net(x.z, DT_INT)
    r.pz = listlist_from_net(x.pz, DT_INT)
    r.pm = listlist_from_net(x.pm, DT_INT)
    r.mergedist = list_from_net(x.mergedist, DT_REAL)
    return r




class kmeansreport(object):
    def __init__(self):
        self.npoints = 0
        self.nfeatures = 0
        self.terminationtype = 0
        self.iterationscount = 0
        self.energy = 0
        self.k = 0
        self.c = [[]]
        self.cidx = []


def net_from_kmeansreport(x,v):
    x.npoints = int(v.npoints)
    x.nfeatures = int(v.nfeatures)
    x.terminationtype = int(v.terminationtype)
    x.iterationscount = int(v.iterationscount)
    x.energy = float(v.energy)
    x.k = int(v.k)
    x.c = net_from_listlist(v.c, DT_REAL)
    x.cidx = net_from_list(v.cidx, DT_INT)
    return




def kmeansreport_from_net(x):
    r = kmeansreport()
    r.npoints = x.npoints
    r.nfeatures = x.nfeatures
    r.terminationtype = x.terminationtype
    r.iterationscount = x.iterationscount
    r.energy = x.energy
    r.k = x.k
    r.c = listlist_from_net(x.c, DT_REAL)
    r.cidx = list_from_net(x.cidx, DT_INT)
    return r


def clusterizercreate(*functionargs):
    # unpack inputs
    friendly_form = False

    # convert to .NET types
    try:

        # call function
        _net_s = _net_alglib.clusterizercreate()
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    s = clusterizerstate(_net_s)

    # return
    return s

def clusterizersetpoints(*functionargs):
    # unpack inputs
    if len(functionargs)==5:
        # full-form call
        s, xy, npoints, nfeatures, disttype = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        s, xy, disttype = functionargs
        npoints = check_equality_and_get([safe_rows("'clusterizersetpoints': incorrect parameters",xy)],"Error while calling 'clusterizersetpoints': looks like one of arguments has wrong size")
        nfeatures = check_equality_and_get([safe_cols("'clusterizersetpoints': incorrect parameters",xy)],"Error while calling 'clusterizersetpoints': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'clusterizersetpoints': function must have 5 or 3 parameters")

    # convert to .NET types
    _net_s = s.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.clusterizersetpoints' must be real matrix")
    _net_npoints = npoints
    _net_nfeatures = nfeatures
    _net_disttype = disttype
    try:

        # call function
        _net_alglib.clusterizersetpoints(_net_s, _net_xy, _net_npoints, _net_nfeatures, _net_disttype)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def clusterizersetdistances(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        s, d, npoints, isupper = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        s, d, isupper = functionargs
        npoints = check_equality_and_get([safe_rows("'clusterizersetdistances': incorrect parameters",d), safe_cols("'clusterizersetdistances': incorrect parameters",d)],"Error while calling 'clusterizersetdistances': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'clusterizersetdistances': function must have 4 or 3 parameters")

    # convert to .NET types
    _net_s = s.ptr
    _net_d = net_from_listlist(d, DT_REAL, "ALGLIB: parameter 'd' of 'xalglib.clusterizersetdistances' must be real matrix")
    _net_npoints = npoints
    _net_isupper = isupper
    try:

        # call function
        _net_alglib.clusterizersetdistances(_net_s, _net_d, _net_npoints, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def clusterizersetahcalgo(*functionargs):
    # unpack inputs
    s, algo = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_algo = algo
    try:

        # call function
        _net_alglib.clusterizersetahcalgo(_net_s, _net_algo)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def clusterizersetkmeanslimits(*functionargs):
    # unpack inputs
    s, restarts, maxits = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_restarts = restarts
    _net_maxits = maxits
    try:

        # call function
        _net_alglib.clusterizersetkmeanslimits(_net_s, _net_restarts, _net_maxits)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def clusterizersetkmeansinit(*functionargs):
    # unpack inputs
    s, initalgo = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_initalgo = initalgo
    try:

        # call function
        _net_alglib.clusterizersetkmeansinit(_net_s, _net_initalgo)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def clusterizersetseed(*functionargs):
    # unpack inputs
    s, seed = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_seed = seed
    try:

        # call function
        _net_alglib.clusterizersetseed(_net_s, _net_seed)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def clusterizerrunahc(*functionargs):
    # unpack inputs
    s,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    try:

        # call function
        _net_rep = _net_alglib.clusterizerrunahc(_net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    rep = ahcreport_from_net(_net_rep)

    # return
    return rep

def smp_clusterizerrunahc(*functionargs):
    # unpack inputs
    s,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    try:

        # call function
        _net_rep = _net_alglib.smp_clusterizerrunahc(_net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    rep = ahcreport_from_net(_net_rep)

    # return
    return rep

def clusterizerrunkmeans(*functionargs):
    # unpack inputs
    s, k = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_k = k
    try:

        # call function
        _net_rep = _net_alglib.clusterizerrunkmeans(_net_s, _net_k)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    rep = kmeansreport_from_net(_net_rep)

    # return
    return rep

def smp_clusterizerrunkmeans(*functionargs):
    # unpack inputs
    s, k = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_k = k
    try:

        # call function
        _net_rep = _net_alglib.smp_clusterizerrunkmeans(_net_s, _net_k)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    rep = kmeansreport_from_net(_net_rep)

    # return
    return rep

def clusterizergetdistances(*functionargs):
    # unpack inputs
    xy, npoints, nfeatures, disttype = functionargs
    friendly_form = False

    # convert to .NET types
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.clusterizergetdistances' must be real matrix")
    _net_npoints = npoints
    _net_nfeatures = nfeatures
    _net_disttype = disttype
    try:

        # call function
        _net_d = _net_alglib.clusterizergetdistances(_net_xy, _net_npoints, _net_nfeatures, _net_disttype)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    d = listlist_from_net(_net_d, DT_REAL)

    # return
    return d

def smp_clusterizergetdistances(*functionargs):
    # unpack inputs
    xy, npoints, nfeatures, disttype = functionargs
    friendly_form = False

    # convert to .NET types
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.smp_clusterizergetdistances' must be real matrix")
    _net_npoints = npoints
    _net_nfeatures = nfeatures
    _net_disttype = disttype
    try:

        # call function
        _net_d = _net_alglib.smp_clusterizergetdistances(_net_xy, _net_npoints, _net_nfeatures, _net_disttype)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    d = listlist_from_net(_net_d, DT_REAL)

    # return
    return d

def clusterizergetkclusters(*functionargs):
    # unpack inputs
    rep, k = functionargs
    friendly_form = False

    # convert to .NET types
    _net_rep = _net_alglib.ahcreport()
    net_from_ahcreport(_net_rep, rep)
    _net_k = k
    try:

        # call function
        _net_cidx, _net_cz = _net_alglib.clusterizergetkclusters(_net_rep, _net_k)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    cidx = list_from_net(_net_cidx, DT_INT)
    cz = list_from_net(_net_cz, DT_INT)

    # return
    return (cidx, cz)

def clusterizerseparatedbydist(*functionargs):
    # unpack inputs
    rep, r = functionargs
    friendly_form = False

    # convert to .NET types
    _net_rep = _net_alglib.ahcreport()
    net_from_ahcreport(_net_rep, rep)
    _net_r = r
    try:

        # call function
        _net_k, _net_cidx, _net_cz = _net_alglib.clusterizerseparatedbydist(_net_rep, _net_r)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    k = _net_k
    cidx = list_from_net(_net_cidx, DT_INT)
    cz = list_from_net(_net_cz, DT_INT)

    # return
    return (k, cidx, cz)

def clusterizerseparatedbycorr(*functionargs):
    # unpack inputs
    rep, r = functionargs
    friendly_form = False

    # convert to .NET types
    _net_rep = _net_alglib.ahcreport()
    net_from_ahcreport(_net_rep, rep)
    _net_r = r
    try:

        # call function
        _net_k, _net_cidx, _net_cz = _net_alglib.clusterizerseparatedbycorr(_net_rep, _net_r)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    k = _net_k
    cidx = list_from_net(_net_cidx, DT_INT)
    cz = list_from_net(_net_cz, DT_INT)

    # return
    return (k, cidx, cz)



class decisionforest(object):
    def __init__(self,ptr):
        self.ptr = ptr


class dfreport(object):
    def __init__(self):
        self.relclserror = 0
        self.avgce = 0
        self.rmserror = 0
        self.avgerror = 0
        self.avgrelerror = 0
        self.oobrelclserror = 0
        self.oobavgce = 0
        self.oobrmserror = 0
        self.oobavgerror = 0
        self.oobavgrelerror = 0


def net_from_dfreport(x,v):
    x.relclserror = float(v.relclserror)
    x.avgce = float(v.avgce)
    x.rmserror = float(v.rmserror)
    x.avgerror = float(v.avgerror)
    x.avgrelerror = float(v.avgrelerror)
    x.oobrelclserror = float(v.oobrelclserror)
    x.oobavgce = float(v.oobavgce)
    x.oobrmserror = float(v.oobrmserror)
    x.oobavgerror = float(v.oobavgerror)
    x.oobavgrelerror = float(v.oobavgrelerror)
    return




def dfreport_from_net(x):
    r = dfreport()
    r.relclserror = x.relclserror
    r.avgce = x.avgce
    r.rmserror = x.rmserror
    r.avgerror = x.avgerror
    r.avgrelerror = x.avgrelerror
    r.oobrelclserror = x.oobrelclserror
    r.oobavgce = x.oobavgce
    r.oobrmserror = x.oobrmserror
    r.oobavgerror = x.oobavgerror
    r.oobavgrelerror = x.oobavgrelerror
    return r


def dfserialize(obj):
    try:
        return _net_alglib.dfserialize(obj.ptr)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

def dfunserialize(s_in):
    try:
        return decisionforest(_net_alglib.dfunserialize(s_in))
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)
def dfbuildrandomdecisionforest(*functionargs):
    # unpack inputs
    xy, npoints, nvars, nclasses, ntrees, r = functionargs
    friendly_form = False

    # convert to .NET types
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.dfbuildrandomdecisionforest' must be real matrix")
    _net_npoints = npoints
    _net_nvars = nvars
    _net_nclasses = nclasses
    _net_ntrees = ntrees
    _net_r = r
    try:

        # call function
        _net_info, _net_df, _net_rep = _net_alglib.dfbuildrandomdecisionforest(_net_xy, _net_npoints, _net_nvars, _net_nclasses, _net_ntrees, _net_r)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    df = decisionforest(_net_df)
    rep = dfreport_from_net(_net_rep)

    # return
    return (info, df, rep)

def dfbuildrandomdecisionforestx1(*functionargs):
    # unpack inputs
    xy, npoints, nvars, nclasses, ntrees, nrndvars, r = functionargs
    friendly_form = False

    # convert to .NET types
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.dfbuildrandomdecisionforestx1' must be real matrix")
    _net_npoints = npoints
    _net_nvars = nvars
    _net_nclasses = nclasses
    _net_ntrees = ntrees
    _net_nrndvars = nrndvars
    _net_r = r
    try:

        # call function
        _net_info, _net_df, _net_rep = _net_alglib.dfbuildrandomdecisionforestx1(_net_xy, _net_npoints, _net_nvars, _net_nclasses, _net_ntrees, _net_nrndvars, _net_r)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    df = decisionforest(_net_df)
    rep = dfreport_from_net(_net_rep)

    # return
    return (info, df, rep)

def dfprocess(*functionargs):
    # unpack inputs
    df, x, y = functionargs
    friendly_form = False

    # convert to .NET types
    _net_df = df.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.dfprocess' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.dfprocess' must be real vector")
    try:

        # call function
        _net_y = _net_alglib.dfprocess(_net_df, _net_x, _net_y)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    y = list_from_net(_net_y, DT_REAL)

    # return
    return y

def dfprocessi(*functionargs):
    # unpack inputs
    df, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_df = df.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.dfprocessi' must be real vector")
    try:

        # call function
        _net_y = _net_alglib.dfprocessi(_net_df, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    y = list_from_net(_net_y, DT_REAL)

    # return
    return y

def dfrelclserror(*functionargs):
    # unpack inputs
    df, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_df = df.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.dfrelclserror' must be real matrix")
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.dfrelclserror(_net_df, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def dfavgce(*functionargs):
    # unpack inputs
    df, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_df = df.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.dfavgce' must be real matrix")
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.dfavgce(_net_df, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def dfrmserror(*functionargs):
    # unpack inputs
    df, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_df = df.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.dfrmserror' must be real matrix")
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.dfrmserror(_net_df, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def dfavgerror(*functionargs):
    # unpack inputs
    df, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_df = df.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.dfavgerror' must be real matrix")
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.dfavgerror(_net_df, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def dfavgrelerror(*functionargs):
    # unpack inputs
    df, xy, npoints = functionargs
    friendly_form = False

    # convert to .NET types
    _net_df = df.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.dfavgrelerror' must be real matrix")
    _net_npoints = npoints
    try:

        # call function
        _net_result = _net_alglib.dfavgrelerror(_net_df, _net_xy, _net_npoints)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def kmeansgenerate(*functionargs):
    # unpack inputs
    xy, npoints, nvars, k, restarts = functionargs
    friendly_form = False

    # convert to .NET types
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.kmeansgenerate' must be real matrix")
    _net_npoints = npoints
    _net_nvars = nvars
    _net_k = k
    _net_restarts = restarts
    try:

        # call function
        _net_info, _net_c, _net_xyc = _net_alglib.kmeansgenerate(_net_xy, _net_npoints, _net_nvars, _net_k, _net_restarts)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    c = listlist_from_net(_net_c, DT_REAL)
    xyc = list_from_net(_net_xyc, DT_INT)

    # return
    return (info, c, xyc)

def gqgeneraterec(*functionargs):
    # unpack inputs
    alpha, beta, mu0, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_alpha = net_from_list(alpha, DT_REAL, "ALGLIB: parameter 'alpha' of 'xalglib.gqgeneraterec' must be real vector")
    _net_beta = net_from_list(beta, DT_REAL, "ALGLIB: parameter 'beta' of 'xalglib.gqgeneraterec' must be real vector")
    _net_mu0 = mu0
    _net_n = n
    try:

        # call function
        _net_info, _net_x, _net_w = _net_alglib.gqgeneraterec(_net_alpha, _net_beta, _net_mu0, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    x = list_from_net(_net_x, DT_REAL)
    w = list_from_net(_net_w, DT_REAL)

    # return
    return (info, x, w)

def gqgenerategausslobattorec(*functionargs):
    # unpack inputs
    alpha, beta, mu0, a, b, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_alpha = net_from_list(alpha, DT_REAL, "ALGLIB: parameter 'alpha' of 'xalglib.gqgenerategausslobattorec' must be real vector")
    _net_beta = net_from_list(beta, DT_REAL, "ALGLIB: parameter 'beta' of 'xalglib.gqgenerategausslobattorec' must be real vector")
    _net_mu0 = mu0
    _net_a = a
    _net_b = b
    _net_n = n
    try:

        # call function
        _net_info, _net_x, _net_w = _net_alglib.gqgenerategausslobattorec(_net_alpha, _net_beta, _net_mu0, _net_a, _net_b, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    x = list_from_net(_net_x, DT_REAL)
    w = list_from_net(_net_w, DT_REAL)

    # return
    return (info, x, w)

def gqgenerategaussradaurec(*functionargs):
    # unpack inputs
    alpha, beta, mu0, a, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_alpha = net_from_list(alpha, DT_REAL, "ALGLIB: parameter 'alpha' of 'xalglib.gqgenerategaussradaurec' must be real vector")
    _net_beta = net_from_list(beta, DT_REAL, "ALGLIB: parameter 'beta' of 'xalglib.gqgenerategaussradaurec' must be real vector")
    _net_mu0 = mu0
    _net_a = a
    _net_n = n
    try:

        # call function
        _net_info, _net_x, _net_w = _net_alglib.gqgenerategaussradaurec(_net_alpha, _net_beta, _net_mu0, _net_a, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    x = list_from_net(_net_x, DT_REAL)
    w = list_from_net(_net_w, DT_REAL)

    # return
    return (info, x, w)

def gqgenerategausslegendre(*functionargs):
    # unpack inputs
    n,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    try:

        # call function
        _net_info, _net_x, _net_w = _net_alglib.gqgenerategausslegendre(_net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    x = list_from_net(_net_x, DT_REAL)
    w = list_from_net(_net_w, DT_REAL)

    # return
    return (info, x, w)

def gqgenerategaussjacobi(*functionargs):
    # unpack inputs
    n, alpha, beta = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    _net_alpha = alpha
    _net_beta = beta
    try:

        # call function
        _net_info, _net_x, _net_w = _net_alglib.gqgenerategaussjacobi(_net_n, _net_alpha, _net_beta)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    x = list_from_net(_net_x, DT_REAL)
    w = list_from_net(_net_w, DT_REAL)

    # return
    return (info, x, w)

def gqgenerategausslaguerre(*functionargs):
    # unpack inputs
    n, alpha = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    _net_alpha = alpha
    try:

        # call function
        _net_info, _net_x, _net_w = _net_alglib.gqgenerategausslaguerre(_net_n, _net_alpha)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    x = list_from_net(_net_x, DT_REAL)
    w = list_from_net(_net_w, DT_REAL)

    # return
    return (info, x, w)

def gqgenerategausshermite(*functionargs):
    # unpack inputs
    n,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    try:

        # call function
        _net_info, _net_x, _net_w = _net_alglib.gqgenerategausshermite(_net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    x = list_from_net(_net_x, DT_REAL)
    w = list_from_net(_net_w, DT_REAL)

    # return
    return (info, x, w)

def gkqgeneraterec(*functionargs):
    # unpack inputs
    alpha, beta, mu0, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_alpha = net_from_list(alpha, DT_REAL, "ALGLIB: parameter 'alpha' of 'xalglib.gkqgeneraterec' must be real vector")
    _net_beta = net_from_list(beta, DT_REAL, "ALGLIB: parameter 'beta' of 'xalglib.gkqgeneraterec' must be real vector")
    _net_mu0 = mu0
    _net_n = n
    try:

        # call function
        _net_info, _net_x, _net_wkronrod, _net_wgauss = _net_alglib.gkqgeneraterec(_net_alpha, _net_beta, _net_mu0, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    x = list_from_net(_net_x, DT_REAL)
    wkronrod = list_from_net(_net_wkronrod, DT_REAL)
    wgauss = list_from_net(_net_wgauss, DT_REAL)

    # return
    return (info, x, wkronrod, wgauss)

def gkqgenerategausslegendre(*functionargs):
    # unpack inputs
    n,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    try:

        # call function
        _net_info, _net_x, _net_wkronrod, _net_wgauss = _net_alglib.gkqgenerategausslegendre(_net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    x = list_from_net(_net_x, DT_REAL)
    wkronrod = list_from_net(_net_wkronrod, DT_REAL)
    wgauss = list_from_net(_net_wgauss, DT_REAL)

    # return
    return (info, x, wkronrod, wgauss)

def gkqgenerategaussjacobi(*functionargs):
    # unpack inputs
    n, alpha, beta = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    _net_alpha = alpha
    _net_beta = beta
    try:

        # call function
        _net_info, _net_x, _net_wkronrod, _net_wgauss = _net_alglib.gkqgenerategaussjacobi(_net_n, _net_alpha, _net_beta)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    x = list_from_net(_net_x, DT_REAL)
    wkronrod = list_from_net(_net_wkronrod, DT_REAL)
    wgauss = list_from_net(_net_wgauss, DT_REAL)

    # return
    return (info, x, wkronrod, wgauss)

def gkqlegendrecalc(*functionargs):
    # unpack inputs
    n,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    try:

        # call function
        _net_info, _net_x, _net_wkronrod, _net_wgauss = _net_alglib.gkqlegendrecalc(_net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    x = list_from_net(_net_x, DT_REAL)
    wkronrod = list_from_net(_net_wkronrod, DT_REAL)
    wgauss = list_from_net(_net_wgauss, DT_REAL)

    # return
    return (info, x, wkronrod, wgauss)

def gkqlegendretbl(*functionargs):
    # unpack inputs
    n,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    try:

        # call function
        _net_x, _net_wkronrod, _net_wgauss, _net_eps = _net_alglib.gkqlegendretbl(_net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = list_from_net(_net_x, DT_REAL)
    wkronrod = list_from_net(_net_wkronrod, DT_REAL)
    wgauss = list_from_net(_net_wgauss, DT_REAL)
    eps = _net_eps

    # return
    return (x, wkronrod, wgauss, eps)



class autogkreport(object):
    def __init__(self):
        self.terminationtype = 0
        self.nfev = 0
        self.nintervals = 0


def net_from_autogkreport(x,v):
    x.terminationtype = int(v.terminationtype)
    x.nfev = int(v.nfev)
    x.nintervals = int(v.nintervals)
    return




def autogkreport_from_net(x):
    r = autogkreport()
    r.terminationtype = x.terminationtype
    r.nfev = x.nfev
    r.nintervals = x.nintervals
    return r




class autogkstate(object):
    def __init__(self,ptr):
        self.ptr = ptr
def autogksmooth(*functionargs):
    # unpack inputs
    a, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = a
    _net_b = b
    try:

        # call function
        _net_state = _net_alglib.autogksmooth(_net_a, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = autogkstate(_net_state)

    # return
    return state

def autogksmoothw(*functionargs):
    # unpack inputs
    a, b, xwidth = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = a
    _net_b = b
    _net_xwidth = xwidth
    try:

        # call function
        _net_state = _net_alglib.autogksmoothw(_net_a, _net_b, _net_xwidth)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = autogkstate(_net_state)

    # return
    return state

def autogksingular(*functionargs):
    # unpack inputs
    a, b, alpha, beta = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = a
    _net_b = b
    _net_alpha = alpha
    _net_beta = beta
    try:

        # call function
        _net_state = _net_alglib.autogksingular(_net_a, _net_b, _net_alpha, _net_beta)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = autogkstate(_net_state)

    # return
    return state



def autogkintegrate(state, func, param = None):
    # algorithm iterations
    while True:
        try:
            result = _net_alglib.autogkiteration(state.ptr)
        except _net_alglib.alglibexception as e:
            raise RuntimeError(e.msg)
        if not result:
            break
        if state.ptr.needf:
            state.ptr.f = func(state.ptr.x, state.ptr.xminusa, state.ptr.bminusx, param)
            continue
        raise RuntimeError("ALGLIB: unexpected error in 'autogkintegrate'")
    return

def autogkresults(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_v, _net_rep = _net_alglib.autogkresults(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    v = _net_v
    rep = autogkreport_from_net(_net_rep)

    # return
    return (v, rep)

def fftc1d(*functionargs):
    # unpack inputs
    if len(functionargs)==2:
        # full-form call
        a, n = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        a,  = functionargs
        n = check_equality_and_get([safe_len("'fftc1d': incorrect parameters",a)],"Error while calling 'fftc1d': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'fftc1d': function must have 2 or 1 parameters")

    # convert to .NET types
    _net_a = net_from_list(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.fftc1d' must be complex vector")
    _net_n = n
    try:

        # call function
        _net_a = _net_alglib.fftc1d(_net_a, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = list_from_net(_net_a, DT_COMPLEX)

    # return
    return a

def fftc1dinv(*functionargs):
    # unpack inputs
    if len(functionargs)==2:
        # full-form call
        a, n = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        a,  = functionargs
        n = check_equality_and_get([safe_len("'fftc1dinv': incorrect parameters",a)],"Error while calling 'fftc1dinv': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'fftc1dinv': function must have 2 or 1 parameters")

    # convert to .NET types
    _net_a = net_from_list(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.fftc1dinv' must be complex vector")
    _net_n = n
    try:

        # call function
        _net_a = _net_alglib.fftc1dinv(_net_a, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = list_from_net(_net_a, DT_COMPLEX)

    # return
    return a

def fftr1d(*functionargs):
    # unpack inputs
    if len(functionargs)==2:
        # full-form call
        a, n = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        a,  = functionargs
        n = check_equality_and_get([safe_len("'fftr1d': incorrect parameters",a)],"Error while calling 'fftr1d': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'fftr1d': function must have 2 or 1 parameters")

    # convert to .NET types
    _net_a = net_from_list(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.fftr1d' must be real vector")
    _net_n = n
    try:

        # call function
        _net_f = _net_alglib.fftr1d(_net_a, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    f = list_from_net(_net_f, DT_COMPLEX)

    # return
    return f

def fftr1dinv(*functionargs):
    # unpack inputs
    if len(functionargs)==2:
        # full-form call
        f, n = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        f,  = functionargs
        n = check_equality_and_get([safe_len("'fftr1dinv': incorrect parameters",f)],"Error while calling 'fftr1dinv': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'fftr1dinv': function must have 2 or 1 parameters")

    # convert to .NET types
    _net_f = net_from_list(f, DT_COMPLEX, "ALGLIB: parameter 'f' of 'xalglib.fftr1dinv' must be complex vector")
    _net_n = n
    try:

        # call function
        _net_a = _net_alglib.fftr1dinv(_net_f, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = list_from_net(_net_a, DT_REAL)

    # return
    return a

def fhtr1d(*functionargs):
    # unpack inputs
    a, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_list(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.fhtr1d' must be real vector")
    _net_n = n
    try:

        # call function
        _net_a = _net_alglib.fhtr1d(_net_a, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = list_from_net(_net_a, DT_REAL)

    # return
    return a

def fhtr1dinv(*functionargs):
    # unpack inputs
    a, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_list(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.fhtr1dinv' must be real vector")
    _net_n = n
    try:

        # call function
        _net_a = _net_alglib.fhtr1dinv(_net_a, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = list_from_net(_net_a, DT_REAL)

    # return
    return a

def convc1d(*functionargs):
    # unpack inputs
    a, m, b, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_list(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.convc1d' must be complex vector")
    _net_m = m
    _net_b = net_from_list(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.convc1d' must be complex vector")
    _net_n = n
    try:

        # call function
        _net_r = _net_alglib.convc1d(_net_a, _net_m, _net_b, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    r = list_from_net(_net_r, DT_COMPLEX)

    # return
    return r

def convc1dinv(*functionargs):
    # unpack inputs
    a, m, b, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_list(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.convc1dinv' must be complex vector")
    _net_m = m
    _net_b = net_from_list(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.convc1dinv' must be complex vector")
    _net_n = n
    try:

        # call function
        _net_r = _net_alglib.convc1dinv(_net_a, _net_m, _net_b, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    r = list_from_net(_net_r, DT_COMPLEX)

    # return
    return r

def convc1dcircular(*functionargs):
    # unpack inputs
    s, m, r, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = net_from_list(s, DT_COMPLEX, "ALGLIB: parameter 's' of 'xalglib.convc1dcircular' must be complex vector")
    _net_m = m
    _net_r = net_from_list(r, DT_COMPLEX, "ALGLIB: parameter 'r' of 'xalglib.convc1dcircular' must be complex vector")
    _net_n = n
    try:

        # call function
        _net_c = _net_alglib.convc1dcircular(_net_s, _net_m, _net_r, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = list_from_net(_net_c, DT_COMPLEX)

    # return
    return c

def convc1dcircularinv(*functionargs):
    # unpack inputs
    a, m, b, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_list(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.convc1dcircularinv' must be complex vector")
    _net_m = m
    _net_b = net_from_list(b, DT_COMPLEX, "ALGLIB: parameter 'b' of 'xalglib.convc1dcircularinv' must be complex vector")
    _net_n = n
    try:

        # call function
        _net_r = _net_alglib.convc1dcircularinv(_net_a, _net_m, _net_b, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    r = list_from_net(_net_r, DT_COMPLEX)

    # return
    return r

def convr1d(*functionargs):
    # unpack inputs
    a, m, b, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_list(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.convr1d' must be real vector")
    _net_m = m
    _net_b = net_from_list(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.convr1d' must be real vector")
    _net_n = n
    try:

        # call function
        _net_r = _net_alglib.convr1d(_net_a, _net_m, _net_b, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    r = list_from_net(_net_r, DT_REAL)

    # return
    return r

def convr1dinv(*functionargs):
    # unpack inputs
    a, m, b, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_list(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.convr1dinv' must be real vector")
    _net_m = m
    _net_b = net_from_list(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.convr1dinv' must be real vector")
    _net_n = n
    try:

        # call function
        _net_r = _net_alglib.convr1dinv(_net_a, _net_m, _net_b, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    r = list_from_net(_net_r, DT_REAL)

    # return
    return r

def convr1dcircular(*functionargs):
    # unpack inputs
    s, m, r, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = net_from_list(s, DT_REAL, "ALGLIB: parameter 's' of 'xalglib.convr1dcircular' must be real vector")
    _net_m = m
    _net_r = net_from_list(r, DT_REAL, "ALGLIB: parameter 'r' of 'xalglib.convr1dcircular' must be real vector")
    _net_n = n
    try:

        # call function
        _net_c = _net_alglib.convr1dcircular(_net_s, _net_m, _net_r, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = list_from_net(_net_c, DT_REAL)

    # return
    return c

def convr1dcircularinv(*functionargs):
    # unpack inputs
    a, m, b, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_list(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.convr1dcircularinv' must be real vector")
    _net_m = m
    _net_b = net_from_list(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.convr1dcircularinv' must be real vector")
    _net_n = n
    try:

        # call function
        _net_r = _net_alglib.convr1dcircularinv(_net_a, _net_m, _net_b, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    r = list_from_net(_net_r, DT_REAL)

    # return
    return r

def corrc1d(*functionargs):
    # unpack inputs
    signal, n, pattern, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_signal = net_from_list(signal, DT_COMPLEX, "ALGLIB: parameter 'signal' of 'xalglib.corrc1d' must be complex vector")
    _net_n = n
    _net_pattern = net_from_list(pattern, DT_COMPLEX, "ALGLIB: parameter 'pattern' of 'xalglib.corrc1d' must be complex vector")
    _net_m = m
    try:

        # call function
        _net_r = _net_alglib.corrc1d(_net_signal, _net_n, _net_pattern, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    r = list_from_net(_net_r, DT_COMPLEX)

    # return
    return r

def corrc1dcircular(*functionargs):
    # unpack inputs
    signal, m, pattern, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_signal = net_from_list(signal, DT_COMPLEX, "ALGLIB: parameter 'signal' of 'xalglib.corrc1dcircular' must be complex vector")
    _net_m = m
    _net_pattern = net_from_list(pattern, DT_COMPLEX, "ALGLIB: parameter 'pattern' of 'xalglib.corrc1dcircular' must be complex vector")
    _net_n = n
    try:

        # call function
        _net_c = _net_alglib.corrc1dcircular(_net_signal, _net_m, _net_pattern, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = list_from_net(_net_c, DT_COMPLEX)

    # return
    return c

def corrr1d(*functionargs):
    # unpack inputs
    signal, n, pattern, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_signal = net_from_list(signal, DT_REAL, "ALGLIB: parameter 'signal' of 'xalglib.corrr1d' must be real vector")
    _net_n = n
    _net_pattern = net_from_list(pattern, DT_REAL, "ALGLIB: parameter 'pattern' of 'xalglib.corrr1d' must be real vector")
    _net_m = m
    try:

        # call function
        _net_r = _net_alglib.corrr1d(_net_signal, _net_n, _net_pattern, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    r = list_from_net(_net_r, DT_REAL)

    # return
    return r

def corrr1dcircular(*functionargs):
    # unpack inputs
    signal, m, pattern, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_signal = net_from_list(signal, DT_REAL, "ALGLIB: parameter 'signal' of 'xalglib.corrr1dcircular' must be real vector")
    _net_m = m
    _net_pattern = net_from_list(pattern, DT_REAL, "ALGLIB: parameter 'pattern' of 'xalglib.corrr1dcircular' must be real vector")
    _net_n = n
    try:

        # call function
        _net_c = _net_alglib.corrr1dcircular(_net_signal, _net_m, _net_pattern, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = list_from_net(_net_c, DT_REAL)

    # return
    return c



class idwinterpolant(object):
    def __init__(self,ptr):
        self.ptr = ptr
def idwcalc(*functionargs):
    # unpack inputs
    z, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_z = z.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.idwcalc' must be real vector")
    try:

        # call function
        _net_result = _net_alglib.idwcalc(_net_z, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def idwbuildmodifiedshepard(*functionargs):
    # unpack inputs
    xy, n, nx, d, nq, nw = functionargs
    friendly_form = False

    # convert to .NET types
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.idwbuildmodifiedshepard' must be real matrix")
    _net_n = n
    _net_nx = nx
    _net_d = d
    _net_nq = nq
    _net_nw = nw
    try:

        # call function
        _net_z = _net_alglib.idwbuildmodifiedshepard(_net_xy, _net_n, _net_nx, _net_d, _net_nq, _net_nw)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    z = idwinterpolant(_net_z)

    # return
    return z

def idwbuildmodifiedshepardr(*functionargs):
    # unpack inputs
    xy, n, nx, r = functionargs
    friendly_form = False

    # convert to .NET types
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.idwbuildmodifiedshepardr' must be real matrix")
    _net_n = n
    _net_nx = nx
    _net_r = r
    try:

        # call function
        _net_z = _net_alglib.idwbuildmodifiedshepardr(_net_xy, _net_n, _net_nx, _net_r)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    z = idwinterpolant(_net_z)

    # return
    return z

def idwbuildnoisy(*functionargs):
    # unpack inputs
    xy, n, nx, d, nq, nw = functionargs
    friendly_form = False

    # convert to .NET types
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.idwbuildnoisy' must be real matrix")
    _net_n = n
    _net_nx = nx
    _net_d = d
    _net_nq = nq
    _net_nw = nw
    try:

        # call function
        _net_z = _net_alglib.idwbuildnoisy(_net_xy, _net_n, _net_nx, _net_d, _net_nq, _net_nw)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    z = idwinterpolant(_net_z)

    # return
    return z



class barycentricinterpolant(object):
    def __init__(self,ptr):
        self.ptr = ptr
def barycentriccalc(*functionargs):
    # unpack inputs
    b, t = functionargs
    friendly_form = False

    # convert to .NET types
    _net_b = b.ptr
    _net_t = t
    try:

        # call function
        _net_result = _net_alglib.barycentriccalc(_net_b, _net_t)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def barycentricdiff1(*functionargs):
    # unpack inputs
    b, t = functionargs
    friendly_form = False

    # convert to .NET types
    _net_b = b.ptr
    _net_t = t
    try:

        # call function
        _net_f, _net_df = _net_alglib.barycentricdiff1(_net_b, _net_t)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    f = _net_f
    df = _net_df

    # return
    return (f, df)

def barycentricdiff2(*functionargs):
    # unpack inputs
    b, t = functionargs
    friendly_form = False

    # convert to .NET types
    _net_b = b.ptr
    _net_t = t
    try:

        # call function
        _net_f, _net_df, _net_d2f = _net_alglib.barycentricdiff2(_net_b, _net_t)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    f = _net_f
    df = _net_df
    d2f = _net_d2f

    # return
    return (f, df, d2f)

def barycentriclintransx(*functionargs):
    # unpack inputs
    b, ca, cb = functionargs
    friendly_form = False

    # convert to .NET types
    _net_b = b.ptr
    _net_ca = ca
    _net_cb = cb
    try:

        # call function
        _net_alglib.barycentriclintransx(_net_b, _net_ca, _net_cb)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def barycentriclintransy(*functionargs):
    # unpack inputs
    b, ca, cb = functionargs
    friendly_form = False

    # convert to .NET types
    _net_b = b.ptr
    _net_ca = ca
    _net_cb = cb
    try:

        # call function
        _net_alglib.barycentriclintransy(_net_b, _net_ca, _net_cb)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def barycentricunpack(*functionargs):
    # unpack inputs
    b,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_b = b.ptr
    try:

        # call function
        _net_n, _net_x, _net_y, _net_w = _net_alglib.barycentricunpack(_net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    n = _net_n
    x = list_from_net(_net_x, DT_REAL)
    y = list_from_net(_net_y, DT_REAL)
    w = list_from_net(_net_w, DT_REAL)

    # return
    return (n, x, y, w)

def barycentricbuildxyw(*functionargs):
    # unpack inputs
    x, y, w, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.barycentricbuildxyw' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.barycentricbuildxyw' must be real vector")
    _net_w = net_from_list(w, DT_REAL, "ALGLIB: parameter 'w' of 'xalglib.barycentricbuildxyw' must be real vector")
    _net_n = n
    try:

        # call function
        _net_b = _net_alglib.barycentricbuildxyw(_net_x, _net_y, _net_w, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = barycentricinterpolant(_net_b)

    # return
    return b

def barycentricbuildfloaterhormann(*functionargs):
    # unpack inputs
    x, y, n, d = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.barycentricbuildfloaterhormann' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.barycentricbuildfloaterhormann' must be real vector")
    _net_n = n
    _net_d = d
    try:

        # call function
        _net_b = _net_alglib.barycentricbuildfloaterhormann(_net_x, _net_y, _net_n, _net_d)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = barycentricinterpolant(_net_b)

    # return
    return b



class spline1dinterpolant(object):
    def __init__(self,ptr):
        self.ptr = ptr


class spline1dfitreport(object):
    def __init__(self):
        self.taskrcond = 0
        self.rmserror = 0
        self.avgerror = 0
        self.avgrelerror = 0
        self.maxerror = 0


def net_from_spline1dfitreport(x,v):
    x.taskrcond = float(v.taskrcond)
    x.rmserror = float(v.rmserror)
    x.avgerror = float(v.avgerror)
    x.avgrelerror = float(v.avgrelerror)
    x.maxerror = float(v.maxerror)
    return




def spline1dfitreport_from_net(x):
    r = spline1dfitreport()
    r.taskrcond = x.taskrcond
    r.rmserror = x.rmserror
    r.avgerror = x.avgerror
    r.avgrelerror = x.avgrelerror
    r.maxerror = x.maxerror
    return r


def spline1dbuildlinear(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        x, y, n = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        x, y = functionargs
        n = check_equality_and_get([safe_len("'spline1dbuildlinear': incorrect parameters",x), safe_len("'spline1dbuildlinear': incorrect parameters",y)],"Error while calling 'spline1dbuildlinear': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'spline1dbuildlinear': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.spline1dbuildlinear' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.spline1dbuildlinear' must be real vector")
    _net_n = n
    try:

        # call function
        _net_c = _net_alglib.spline1dbuildlinear(_net_x, _net_y, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = spline1dinterpolant(_net_c)

    # return
    return c

def spline1dbuildcubic(*functionargs):
    # unpack inputs
    if len(functionargs)==7:
        # full-form call
        x, y, n, boundltype, boundl, boundrtype, boundr = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        x, y = functionargs
        n = check_equality_and_get([safe_len("'spline1dbuildcubic': incorrect parameters",x), safe_len("'spline1dbuildcubic': incorrect parameters",y)],"Error while calling 'spline1dbuildcubic': looks like one of arguments has wrong size")
        boundltype = check_equality_and_get([0],"Error while calling 'spline1dbuildcubic': looks like one of arguments has wrong size")
        boundl = check_equality_and_get([0],"Error while calling 'spline1dbuildcubic': looks like one of arguments has wrong size")
        boundrtype = check_equality_and_get([0],"Error while calling 'spline1dbuildcubic': looks like one of arguments has wrong size")
        boundr = check_equality_and_get([0],"Error while calling 'spline1dbuildcubic': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'spline1dbuildcubic': function must have 7 or 2 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.spline1dbuildcubic' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.spline1dbuildcubic' must be real vector")
    _net_n = n
    _net_boundltype = boundltype
    _net_boundl = boundl
    _net_boundrtype = boundrtype
    _net_boundr = boundr
    try:

        # call function
        _net_c = _net_alglib.spline1dbuildcubic(_net_x, _net_y, _net_n, _net_boundltype, _net_boundl, _net_boundrtype, _net_boundr)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = spline1dinterpolant(_net_c)

    # return
    return c

def spline1dgriddiffcubic(*functionargs):
    # unpack inputs
    if len(functionargs)==7:
        # full-form call
        x, y, n, boundltype, boundl, boundrtype, boundr = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        x, y = functionargs
        n = check_equality_and_get([safe_len("'spline1dgriddiffcubic': incorrect parameters",x), safe_len("'spline1dgriddiffcubic': incorrect parameters",y)],"Error while calling 'spline1dgriddiffcubic': looks like one of arguments has wrong size")
        boundltype = check_equality_and_get([0],"Error while calling 'spline1dgriddiffcubic': looks like one of arguments has wrong size")
        boundl = check_equality_and_get([0],"Error while calling 'spline1dgriddiffcubic': looks like one of arguments has wrong size")
        boundrtype = check_equality_and_get([0],"Error while calling 'spline1dgriddiffcubic': looks like one of arguments has wrong size")
        boundr = check_equality_and_get([0],"Error while calling 'spline1dgriddiffcubic': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'spline1dgriddiffcubic': function must have 7 or 2 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.spline1dgriddiffcubic' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.spline1dgriddiffcubic' must be real vector")
    _net_n = n
    _net_boundltype = boundltype
    _net_boundl = boundl
    _net_boundrtype = boundrtype
    _net_boundr = boundr
    try:

        # call function
        _net_d = _net_alglib.spline1dgriddiffcubic(_net_x, _net_y, _net_n, _net_boundltype, _net_boundl, _net_boundrtype, _net_boundr)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    d = list_from_net(_net_d, DT_REAL)

    # return
    return d

def spline1dgriddiff2cubic(*functionargs):
    # unpack inputs
    if len(functionargs)==7:
        # full-form call
        x, y, n, boundltype, boundl, boundrtype, boundr = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        x, y = functionargs
        n = check_equality_and_get([safe_len("'spline1dgriddiff2cubic': incorrect parameters",x), safe_len("'spline1dgriddiff2cubic': incorrect parameters",y)],"Error while calling 'spline1dgriddiff2cubic': looks like one of arguments has wrong size")
        boundltype = check_equality_and_get([0],"Error while calling 'spline1dgriddiff2cubic': looks like one of arguments has wrong size")
        boundl = check_equality_and_get([0],"Error while calling 'spline1dgriddiff2cubic': looks like one of arguments has wrong size")
        boundrtype = check_equality_and_get([0],"Error while calling 'spline1dgriddiff2cubic': looks like one of arguments has wrong size")
        boundr = check_equality_and_get([0],"Error while calling 'spline1dgriddiff2cubic': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'spline1dgriddiff2cubic': function must have 7 or 2 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.spline1dgriddiff2cubic' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.spline1dgriddiff2cubic' must be real vector")
    _net_n = n
    _net_boundltype = boundltype
    _net_boundl = boundl
    _net_boundrtype = boundrtype
    _net_boundr = boundr
    try:

        # call function
        _net_d1, _net_d2 = _net_alglib.spline1dgriddiff2cubic(_net_x, _net_y, _net_n, _net_boundltype, _net_boundl, _net_boundrtype, _net_boundr)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    d1 = list_from_net(_net_d1, DT_REAL)
    d2 = list_from_net(_net_d2, DT_REAL)

    # return
    return (d1, d2)

def spline1dconvcubic(*functionargs):
    # unpack inputs
    if len(functionargs)==9:
        # full-form call
        x, y, n, boundltype, boundl, boundrtype, boundr, x2, n2 = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        x, y, x2 = functionargs
        n = check_equality_and_get([safe_len("'spline1dconvcubic': incorrect parameters",x), safe_len("'spline1dconvcubic': incorrect parameters",y)],"Error while calling 'spline1dconvcubic': looks like one of arguments has wrong size")
        boundltype = check_equality_and_get([0],"Error while calling 'spline1dconvcubic': looks like one of arguments has wrong size")
        boundl = check_equality_and_get([0],"Error while calling 'spline1dconvcubic': looks like one of arguments has wrong size")
        boundrtype = check_equality_and_get([0],"Error while calling 'spline1dconvcubic': looks like one of arguments has wrong size")
        boundr = check_equality_and_get([0],"Error while calling 'spline1dconvcubic': looks like one of arguments has wrong size")
        n2 = check_equality_and_get([safe_len("'spline1dconvcubic': incorrect parameters",x2)],"Error while calling 'spline1dconvcubic': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'spline1dconvcubic': function must have 9 or 3 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.spline1dconvcubic' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.spline1dconvcubic' must be real vector")
    _net_n = n
    _net_boundltype = boundltype
    _net_boundl = boundl
    _net_boundrtype = boundrtype
    _net_boundr = boundr
    _net_x2 = net_from_list(x2, DT_REAL, "ALGLIB: parameter 'x2' of 'xalglib.spline1dconvcubic' must be real vector")
    _net_n2 = n2
    try:

        # call function
        _net_y2 = _net_alglib.spline1dconvcubic(_net_x, _net_y, _net_n, _net_boundltype, _net_boundl, _net_boundrtype, _net_boundr, _net_x2, _net_n2)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    y2 = list_from_net(_net_y2, DT_REAL)

    # return
    return y2

def spline1dconvdiffcubic(*functionargs):
    # unpack inputs
    if len(functionargs)==9:
        # full-form call
        x, y, n, boundltype, boundl, boundrtype, boundr, x2, n2 = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        x, y, x2 = functionargs
        n = check_equality_and_get([safe_len("'spline1dconvdiffcubic': incorrect parameters",x), safe_len("'spline1dconvdiffcubic': incorrect parameters",y)],"Error while calling 'spline1dconvdiffcubic': looks like one of arguments has wrong size")
        boundltype = check_equality_and_get([0],"Error while calling 'spline1dconvdiffcubic': looks like one of arguments has wrong size")
        boundl = check_equality_and_get([0],"Error while calling 'spline1dconvdiffcubic': looks like one of arguments has wrong size")
        boundrtype = check_equality_and_get([0],"Error while calling 'spline1dconvdiffcubic': looks like one of arguments has wrong size")
        boundr = check_equality_and_get([0],"Error while calling 'spline1dconvdiffcubic': looks like one of arguments has wrong size")
        n2 = check_equality_and_get([safe_len("'spline1dconvdiffcubic': incorrect parameters",x2)],"Error while calling 'spline1dconvdiffcubic': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'spline1dconvdiffcubic': function must have 9 or 3 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.spline1dconvdiffcubic' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.spline1dconvdiffcubic' must be real vector")
    _net_n = n
    _net_boundltype = boundltype
    _net_boundl = boundl
    _net_boundrtype = boundrtype
    _net_boundr = boundr
    _net_x2 = net_from_list(x2, DT_REAL, "ALGLIB: parameter 'x2' of 'xalglib.spline1dconvdiffcubic' must be real vector")
    _net_n2 = n2
    try:

        # call function
        _net_y2, _net_d2 = _net_alglib.spline1dconvdiffcubic(_net_x, _net_y, _net_n, _net_boundltype, _net_boundl, _net_boundrtype, _net_boundr, _net_x2, _net_n2)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    y2 = list_from_net(_net_y2, DT_REAL)
    d2 = list_from_net(_net_d2, DT_REAL)

    # return
    return (y2, d2)

def spline1dconvdiff2cubic(*functionargs):
    # unpack inputs
    if len(functionargs)==9:
        # full-form call
        x, y, n, boundltype, boundl, boundrtype, boundr, x2, n2 = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        x, y, x2 = functionargs
        n = check_equality_and_get([safe_len("'spline1dconvdiff2cubic': incorrect parameters",x), safe_len("'spline1dconvdiff2cubic': incorrect parameters",y)],"Error while calling 'spline1dconvdiff2cubic': looks like one of arguments has wrong size")
        boundltype = check_equality_and_get([0],"Error while calling 'spline1dconvdiff2cubic': looks like one of arguments has wrong size")
        boundl = check_equality_and_get([0],"Error while calling 'spline1dconvdiff2cubic': looks like one of arguments has wrong size")
        boundrtype = check_equality_and_get([0],"Error while calling 'spline1dconvdiff2cubic': looks like one of arguments has wrong size")
        boundr = check_equality_and_get([0],"Error while calling 'spline1dconvdiff2cubic': looks like one of arguments has wrong size")
        n2 = check_equality_and_get([safe_len("'spline1dconvdiff2cubic': incorrect parameters",x2)],"Error while calling 'spline1dconvdiff2cubic': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'spline1dconvdiff2cubic': function must have 9 or 3 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.spline1dconvdiff2cubic' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.spline1dconvdiff2cubic' must be real vector")
    _net_n = n
    _net_boundltype = boundltype
    _net_boundl = boundl
    _net_boundrtype = boundrtype
    _net_boundr = boundr
    _net_x2 = net_from_list(x2, DT_REAL, "ALGLIB: parameter 'x2' of 'xalglib.spline1dconvdiff2cubic' must be real vector")
    _net_n2 = n2
    try:

        # call function
        _net_y2, _net_d2, _net_dd2 = _net_alglib.spline1dconvdiff2cubic(_net_x, _net_y, _net_n, _net_boundltype, _net_boundl, _net_boundrtype, _net_boundr, _net_x2, _net_n2)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    y2 = list_from_net(_net_y2, DT_REAL)
    d2 = list_from_net(_net_d2, DT_REAL)
    dd2 = list_from_net(_net_dd2, DT_REAL)

    # return
    return (y2, d2, dd2)

def spline1dbuildcatmullrom(*functionargs):
    # unpack inputs
    if len(functionargs)==5:
        # full-form call
        x, y, n, boundtype, tension = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        x, y = functionargs
        n = check_equality_and_get([safe_len("'spline1dbuildcatmullrom': incorrect parameters",x), safe_len("'spline1dbuildcatmullrom': incorrect parameters",y)],"Error while calling 'spline1dbuildcatmullrom': looks like one of arguments has wrong size")
        boundtype = check_equality_and_get([0],"Error while calling 'spline1dbuildcatmullrom': looks like one of arguments has wrong size")
        tension = check_equality_and_get([0],"Error while calling 'spline1dbuildcatmullrom': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'spline1dbuildcatmullrom': function must have 5 or 2 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.spline1dbuildcatmullrom' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.spline1dbuildcatmullrom' must be real vector")
    _net_n = n
    _net_boundtype = boundtype
    _net_tension = tension
    try:

        # call function
        _net_c = _net_alglib.spline1dbuildcatmullrom(_net_x, _net_y, _net_n, _net_boundtype, _net_tension)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = spline1dinterpolant(_net_c)

    # return
    return c

def spline1dbuildhermite(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        x, y, d, n = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        x, y, d = functionargs
        n = check_equality_and_get([safe_len("'spline1dbuildhermite': incorrect parameters",x), safe_len("'spline1dbuildhermite': incorrect parameters",y), safe_len("'spline1dbuildhermite': incorrect parameters",d)],"Error while calling 'spline1dbuildhermite': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'spline1dbuildhermite': function must have 4 or 3 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.spline1dbuildhermite' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.spline1dbuildhermite' must be real vector")
    _net_d = net_from_list(d, DT_REAL, "ALGLIB: parameter 'd' of 'xalglib.spline1dbuildhermite' must be real vector")
    _net_n = n
    try:

        # call function
        _net_c = _net_alglib.spline1dbuildhermite(_net_x, _net_y, _net_d, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = spline1dinterpolant(_net_c)

    # return
    return c

def spline1dbuildakima(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        x, y, n = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        x, y = functionargs
        n = check_equality_and_get([safe_len("'spline1dbuildakima': incorrect parameters",x), safe_len("'spline1dbuildakima': incorrect parameters",y)],"Error while calling 'spline1dbuildakima': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'spline1dbuildakima': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.spline1dbuildakima' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.spline1dbuildakima' must be real vector")
    _net_n = n
    try:

        # call function
        _net_c = _net_alglib.spline1dbuildakima(_net_x, _net_y, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = spline1dinterpolant(_net_c)

    # return
    return c

def spline1dcalc(*functionargs):
    # unpack inputs
    c, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_c = c.ptr
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.spline1dcalc(_net_c, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def spline1ddiff(*functionargs):
    # unpack inputs
    c, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_c = c.ptr
    _net_x = x
    try:

        # call function
        _net_s, _net_ds, _net_d2s = _net_alglib.spline1ddiff(_net_c, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    s = _net_s
    ds = _net_ds
    d2s = _net_d2s

    # return
    return (s, ds, d2s)

def spline1dunpack(*functionargs):
    # unpack inputs
    c,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_c = c.ptr
    try:

        # call function
        _net_n, _net_tbl = _net_alglib.spline1dunpack(_net_c)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    n = _net_n
    tbl = listlist_from_net(_net_tbl, DT_REAL)

    # return
    return (n, tbl)

def spline1dlintransx(*functionargs):
    # unpack inputs
    c, a, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_c = c.ptr
    _net_a = a
    _net_b = b
    try:

        # call function
        _net_alglib.spline1dlintransx(_net_c, _net_a, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def spline1dlintransy(*functionargs):
    # unpack inputs
    c, a, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_c = c.ptr
    _net_a = a
    _net_b = b
    try:

        # call function
        _net_alglib.spline1dlintransy(_net_c, _net_a, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def spline1dintegrate(*functionargs):
    # unpack inputs
    c, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_c = c.ptr
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.spline1dintegrate(_net_c, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def spline1dfitpenalized(*functionargs):
    # unpack inputs
    if len(functionargs)==5:
        # full-form call
        x, y, n, m, rho = functionargs
        friendly_form = False
    elif len(functionargs)==4:
        # short-form call
        x, y, m, rho = functionargs
        n = check_equality_and_get([safe_len("'spline1dfitpenalized': incorrect parameters",x), safe_len("'spline1dfitpenalized': incorrect parameters",y)],"Error while calling 'spline1dfitpenalized': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'spline1dfitpenalized': function must have 5 or 4 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.spline1dfitpenalized' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.spline1dfitpenalized' must be real vector")
    _net_n = n
    _net_m = m
    _net_rho = rho
    try:

        # call function
        _net_info, _net_s, _net_rep = _net_alglib.spline1dfitpenalized(_net_x, _net_y, _net_n, _net_m, _net_rho)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    s = spline1dinterpolant(_net_s)
    rep = spline1dfitreport_from_net(_net_rep)

    # return
    return (info, s, rep)

def smp_spline1dfitpenalized(*functionargs):
    # unpack inputs
    if len(functionargs)==5:
        # full-form call
        x, y, n, m, rho = functionargs
        friendly_form = False
    elif len(functionargs)==4:
        # short-form call
        x, y, m, rho = functionargs
        n = check_equality_and_get([safe_len("'smp_spline1dfitpenalized': incorrect parameters",x), safe_len("'smp_spline1dfitpenalized': incorrect parameters",y)],"Error while calling 'smp_spline1dfitpenalized': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'smp_spline1dfitpenalized': function must have 5 or 4 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.smp_spline1dfitpenalized' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.smp_spline1dfitpenalized' must be real vector")
    _net_n = n
    _net_m = m
    _net_rho = rho
    try:

        # call function
        _net_info, _net_s, _net_rep = _net_alglib.smp_spline1dfitpenalized(_net_x, _net_y, _net_n, _net_m, _net_rho)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    s = spline1dinterpolant(_net_s)
    rep = spline1dfitreport_from_net(_net_rep)

    # return
    return (info, s, rep)

def spline1dfitpenalizedw(*functionargs):
    # unpack inputs
    if len(functionargs)==6:
        # full-form call
        x, y, w, n, m, rho = functionargs
        friendly_form = False
    elif len(functionargs)==5:
        # short-form call
        x, y, w, m, rho = functionargs
        n = check_equality_and_get([safe_len("'spline1dfitpenalizedw': incorrect parameters",x), safe_len("'spline1dfitpenalizedw': incorrect parameters",y), safe_len("'spline1dfitpenalizedw': incorrect parameters",w)],"Error while calling 'spline1dfitpenalizedw': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'spline1dfitpenalizedw': function must have 6 or 5 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.spline1dfitpenalizedw' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.spline1dfitpenalizedw' must be real vector")
    _net_w = net_from_list(w, DT_REAL, "ALGLIB: parameter 'w' of 'xalglib.spline1dfitpenalizedw' must be real vector")
    _net_n = n
    _net_m = m
    _net_rho = rho
    try:

        # call function
        _net_info, _net_s, _net_rep = _net_alglib.spline1dfitpenalizedw(_net_x, _net_y, _net_w, _net_n, _net_m, _net_rho)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    s = spline1dinterpolant(_net_s)
    rep = spline1dfitreport_from_net(_net_rep)

    # return
    return (info, s, rep)

def smp_spline1dfitpenalizedw(*functionargs):
    # unpack inputs
    if len(functionargs)==6:
        # full-form call
        x, y, w, n, m, rho = functionargs
        friendly_form = False
    elif len(functionargs)==5:
        # short-form call
        x, y, w, m, rho = functionargs
        n = check_equality_and_get([safe_len("'smp_spline1dfitpenalizedw': incorrect parameters",x), safe_len("'smp_spline1dfitpenalizedw': incorrect parameters",y), safe_len("'smp_spline1dfitpenalizedw': incorrect parameters",w)],"Error while calling 'smp_spline1dfitpenalizedw': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'smp_spline1dfitpenalizedw': function must have 6 or 5 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.smp_spline1dfitpenalizedw' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.smp_spline1dfitpenalizedw' must be real vector")
    _net_w = net_from_list(w, DT_REAL, "ALGLIB: parameter 'w' of 'xalglib.smp_spline1dfitpenalizedw' must be real vector")
    _net_n = n
    _net_m = m
    _net_rho = rho
    try:

        # call function
        _net_info, _net_s, _net_rep = _net_alglib.smp_spline1dfitpenalizedw(_net_x, _net_y, _net_w, _net_n, _net_m, _net_rho)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    s = spline1dinterpolant(_net_s)
    rep = spline1dfitreport_from_net(_net_rep)

    # return
    return (info, s, rep)

def spline1dbuildmonotone(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        x, y, n = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        x, y = functionargs
        n = check_equality_and_get([safe_len("'spline1dbuildmonotone': incorrect parameters",x), safe_len("'spline1dbuildmonotone': incorrect parameters",y)],"Error while calling 'spline1dbuildmonotone': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'spline1dbuildmonotone': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.spline1dbuildmonotone' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.spline1dbuildmonotone' must be real vector")
    _net_n = n
    try:

        # call function
        _net_c = _net_alglib.spline1dbuildmonotone(_net_x, _net_y, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = spline1dinterpolant(_net_c)

    # return
    return c



class pspline2interpolant(object):
    def __init__(self,ptr):
        self.ptr = ptr


class pspline3interpolant(object):
    def __init__(self,ptr):
        self.ptr = ptr
def pspline2build(*functionargs):
    # unpack inputs
    xy, n, st, pt = functionargs
    friendly_form = False

    # convert to .NET types
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.pspline2build' must be real matrix")
    _net_n = n
    _net_st = st
    _net_pt = pt
    try:

        # call function
        _net_p = _net_alglib.pspline2build(_net_xy, _net_n, _net_st, _net_pt)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    p = pspline2interpolant(_net_p)

    # return
    return p

def pspline3build(*functionargs):
    # unpack inputs
    xy, n, st, pt = functionargs
    friendly_form = False

    # convert to .NET types
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.pspline3build' must be real matrix")
    _net_n = n
    _net_st = st
    _net_pt = pt
    try:

        # call function
        _net_p = _net_alglib.pspline3build(_net_xy, _net_n, _net_st, _net_pt)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    p = pspline3interpolant(_net_p)

    # return
    return p

def pspline2buildperiodic(*functionargs):
    # unpack inputs
    xy, n, st, pt = functionargs
    friendly_form = False

    # convert to .NET types
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.pspline2buildperiodic' must be real matrix")
    _net_n = n
    _net_st = st
    _net_pt = pt
    try:

        # call function
        _net_p = _net_alglib.pspline2buildperiodic(_net_xy, _net_n, _net_st, _net_pt)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    p = pspline2interpolant(_net_p)

    # return
    return p

def pspline3buildperiodic(*functionargs):
    # unpack inputs
    xy, n, st, pt = functionargs
    friendly_form = False

    # convert to .NET types
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.pspline3buildperiodic' must be real matrix")
    _net_n = n
    _net_st = st
    _net_pt = pt
    try:

        # call function
        _net_p = _net_alglib.pspline3buildperiodic(_net_xy, _net_n, _net_st, _net_pt)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    p = pspline3interpolant(_net_p)

    # return
    return p

def pspline2parametervalues(*functionargs):
    # unpack inputs
    p,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_p = p.ptr
    try:

        # call function
        _net_n, _net_t = _net_alglib.pspline2parametervalues(_net_p)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    n = _net_n
    t = list_from_net(_net_t, DT_REAL)

    # return
    return (n, t)

def pspline3parametervalues(*functionargs):
    # unpack inputs
    p,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_p = p.ptr
    try:

        # call function
        _net_n, _net_t = _net_alglib.pspline3parametervalues(_net_p)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    n = _net_n
    t = list_from_net(_net_t, DT_REAL)

    # return
    return (n, t)

def pspline2calc(*functionargs):
    # unpack inputs
    p, t = functionargs
    friendly_form = False

    # convert to .NET types
    _net_p = p.ptr
    _net_t = t
    try:

        # call function
        _net_x, _net_y = _net_alglib.pspline2calc(_net_p, _net_t)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = _net_x
    y = _net_y

    # return
    return (x, y)

def pspline3calc(*functionargs):
    # unpack inputs
    p, t = functionargs
    friendly_form = False

    # convert to .NET types
    _net_p = p.ptr
    _net_t = t
    try:

        # call function
        _net_x, _net_y, _net_z = _net_alglib.pspline3calc(_net_p, _net_t)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = _net_x
    y = _net_y
    z = _net_z

    # return
    return (x, y, z)

def pspline2tangent(*functionargs):
    # unpack inputs
    p, t = functionargs
    friendly_form = False

    # convert to .NET types
    _net_p = p.ptr
    _net_t = t
    try:

        # call function
        _net_x, _net_y = _net_alglib.pspline2tangent(_net_p, _net_t)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = _net_x
    y = _net_y

    # return
    return (x, y)

def pspline3tangent(*functionargs):
    # unpack inputs
    p, t = functionargs
    friendly_form = False

    # convert to .NET types
    _net_p = p.ptr
    _net_t = t
    try:

        # call function
        _net_x, _net_y, _net_z = _net_alglib.pspline3tangent(_net_p, _net_t)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = _net_x
    y = _net_y
    z = _net_z

    # return
    return (x, y, z)

def pspline2diff(*functionargs):
    # unpack inputs
    p, t = functionargs
    friendly_form = False

    # convert to .NET types
    _net_p = p.ptr
    _net_t = t
    try:

        # call function
        _net_x, _net_dx, _net_y, _net_dy = _net_alglib.pspline2diff(_net_p, _net_t)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = _net_x
    dx = _net_dx
    y = _net_y
    dy = _net_dy

    # return
    return (x, dx, y, dy)

def pspline3diff(*functionargs):
    # unpack inputs
    p, t = functionargs
    friendly_form = False

    # convert to .NET types
    _net_p = p.ptr
    _net_t = t
    try:

        # call function
        _net_x, _net_dx, _net_y, _net_dy, _net_z, _net_dz = _net_alglib.pspline3diff(_net_p, _net_t)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = _net_x
    dx = _net_dx
    y = _net_y
    dy = _net_dy
    z = _net_z
    dz = _net_dz

    # return
    return (x, dx, y, dy, z, dz)

def pspline2diff2(*functionargs):
    # unpack inputs
    p, t = functionargs
    friendly_form = False

    # convert to .NET types
    _net_p = p.ptr
    _net_t = t
    try:

        # call function
        _net_x, _net_dx, _net_d2x, _net_y, _net_dy, _net_d2y = _net_alglib.pspline2diff2(_net_p, _net_t)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = _net_x
    dx = _net_dx
    d2x = _net_d2x
    y = _net_y
    dy = _net_dy
    d2y = _net_d2y

    # return
    return (x, dx, d2x, y, dy, d2y)

def pspline3diff2(*functionargs):
    # unpack inputs
    p, t = functionargs
    friendly_form = False

    # convert to .NET types
    _net_p = p.ptr
    _net_t = t
    try:

        # call function
        _net_x, _net_dx, _net_d2x, _net_y, _net_dy, _net_d2y, _net_z, _net_dz, _net_d2z = _net_alglib.pspline3diff2(_net_p, _net_t)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = _net_x
    dx = _net_dx
    d2x = _net_d2x
    y = _net_y
    dy = _net_dy
    d2y = _net_d2y
    z = _net_z
    dz = _net_dz
    d2z = _net_d2z

    # return
    return (x, dx, d2x, y, dy, d2y, z, dz, d2z)

def pspline2arclength(*functionargs):
    # unpack inputs
    p, a, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_p = p.ptr
    _net_a = a
    _net_b = b
    try:

        # call function
        _net_result = _net_alglib.pspline2arclength(_net_p, _net_a, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def pspline3arclength(*functionargs):
    # unpack inputs
    p, a, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_p = p.ptr
    _net_a = a
    _net_b = b
    try:

        # call function
        _net_result = _net_alglib.pspline3arclength(_net_p, _net_a, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def parametricrdpfixed(*functionargs):
    # unpack inputs
    x, n, d, stopm, stopeps = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_listlist(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.parametricrdpfixed' must be real matrix")
    _net_n = n
    _net_d = d
    _net_stopm = stopm
    _net_stopeps = stopeps
    try:

        # call function
        _net_x2, _net_idx2, _net_nsections = _net_alglib.parametricrdpfixed(_net_x, _net_n, _net_d, _net_stopm, _net_stopeps)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x2 = listlist_from_net(_net_x2, DT_REAL)
    idx2 = list_from_net(_net_idx2, DT_INT)
    nsections = _net_nsections

    # return
    return (x2, idx2, nsections)



class spline3dinterpolant(object):
    def __init__(self,ptr):
        self.ptr = ptr
def spline3dcalc(*functionargs):
    # unpack inputs
    c, x, y, z = functionargs
    friendly_form = False

    # convert to .NET types
    _net_c = c.ptr
    _net_x = x
    _net_y = y
    _net_z = z
    try:

        # call function
        _net_result = _net_alglib.spline3dcalc(_net_c, _net_x, _net_y, _net_z)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def spline3dlintransxyz(*functionargs):
    # unpack inputs
    c, ax, bx, ay, by, az, bz = functionargs
    friendly_form = False

    # convert to .NET types
    _net_c = c.ptr
    _net_ax = ax
    _net_bx = bx
    _net_ay = ay
    _net_by = by
    _net_az = az
    _net_bz = bz
    try:

        # call function
        _net_alglib.spline3dlintransxyz(_net_c, _net_ax, _net_bx, _net_ay, _net_by, _net_az, _net_bz)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def spline3dlintransf(*functionargs):
    # unpack inputs
    c, a, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_c = c.ptr
    _net_a = a
    _net_b = b
    try:

        # call function
        _net_alglib.spline3dlintransf(_net_c, _net_a, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def spline3dresampletrilinear(*functionargs):
    # unpack inputs
    a, oldzcount, oldycount, oldxcount, newzcount, newycount, newxcount = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_list(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.spline3dresampletrilinear' must be real vector")
    _net_oldzcount = oldzcount
    _net_oldycount = oldycount
    _net_oldxcount = oldxcount
    _net_newzcount = newzcount
    _net_newycount = newycount
    _net_newxcount = newxcount
    try:

        # call function
        _net_b = _net_alglib.spline3dresampletrilinear(_net_a, _net_oldzcount, _net_oldycount, _net_oldxcount, _net_newzcount, _net_newycount, _net_newxcount)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = list_from_net(_net_b, DT_REAL)

    # return
    return b

def spline3dbuildtrilinearv(*functionargs):
    # unpack inputs
    x, n, y, m, z, l, f, d = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.spline3dbuildtrilinearv' must be real vector")
    _net_n = n
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.spline3dbuildtrilinearv' must be real vector")
    _net_m = m
    _net_z = net_from_list(z, DT_REAL, "ALGLIB: parameter 'z' of 'xalglib.spline3dbuildtrilinearv' must be real vector")
    _net_l = l
    _net_f = net_from_list(f, DT_REAL, "ALGLIB: parameter 'f' of 'xalglib.spline3dbuildtrilinearv' must be real vector")
    _net_d = d
    try:

        # call function
        _net_c = _net_alglib.spline3dbuildtrilinearv(_net_x, _net_n, _net_y, _net_m, _net_z, _net_l, _net_f, _net_d)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = spline3dinterpolant(_net_c)

    # return
    return c

def spline3dcalcvbuf(*functionargs):
    # unpack inputs
    c, x, y, z, f = functionargs
    friendly_form = False

    # convert to .NET types
    _net_c = c.ptr
    _net_x = x
    _net_y = y
    _net_z = z
    _net_f = net_from_list(f, DT_REAL, "ALGLIB: parameter 'f' of 'xalglib.spline3dcalcvbuf' must be real vector")
    try:

        # call function
        _net_f = _net_alglib.spline3dcalcvbuf(_net_c, _net_x, _net_y, _net_z, _net_f)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    f = list_from_net(_net_f, DT_REAL)

    # return
    return f

def spline3dcalcv(*functionargs):
    # unpack inputs
    c, x, y, z = functionargs
    friendly_form = False

    # convert to .NET types
    _net_c = c.ptr
    _net_x = x
    _net_y = y
    _net_z = z
    try:

        # call function
        _net_f = _net_alglib.spline3dcalcv(_net_c, _net_x, _net_y, _net_z)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    f = list_from_net(_net_f, DT_REAL)

    # return
    return f

def spline3dunpackv(*functionargs):
    # unpack inputs
    c,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_c = c.ptr
    try:

        # call function
        _net_n, _net_m, _net_l, _net_d, _net_stype, _net_tbl = _net_alglib.spline3dunpackv(_net_c)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    n = _net_n
    m = _net_m
    l = _net_l
    d = _net_d
    stype = _net_stype
    tbl = listlist_from_net(_net_tbl, DT_REAL)

    # return
    return (n, m, l, d, stype, tbl)

def polynomialbar2cheb(*functionargs):
    # unpack inputs
    p, a, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_p = p.ptr
    _net_a = a
    _net_b = b
    try:

        # call function
        _net_t = _net_alglib.polynomialbar2cheb(_net_p, _net_a, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    t = list_from_net(_net_t, DT_REAL)

    # return
    return t

def polynomialcheb2bar(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        t, n, a, b = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        t, a, b = functionargs
        n = check_equality_and_get([safe_len("'polynomialcheb2bar': incorrect parameters",t)],"Error while calling 'polynomialcheb2bar': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'polynomialcheb2bar': function must have 4 or 3 parameters")

    # convert to .NET types
    _net_t = net_from_list(t, DT_REAL, "ALGLIB: parameter 't' of 'xalglib.polynomialcheb2bar' must be real vector")
    _net_n = n
    _net_a = a
    _net_b = b
    try:

        # call function
        _net_p = _net_alglib.polynomialcheb2bar(_net_t, _net_n, _net_a, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    p = barycentricinterpolant(_net_p)

    # return
    return p

def polynomialbar2pow(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        p, c, s = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        p,  = functionargs
        c = check_equality_and_get([0],"Error while calling 'polynomialbar2pow': looks like one of arguments has wrong size")
        s = check_equality_and_get([1],"Error while calling 'polynomialbar2pow': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'polynomialbar2pow': function must have 3 or 1 parameters")

    # convert to .NET types
    _net_p = p.ptr
    _net_c = c
    _net_s = s
    try:

        # call function
        _net_a = _net_alglib.polynomialbar2pow(_net_p, _net_c, _net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = list_from_net(_net_a, DT_REAL)

    # return
    return a

def polynomialpow2bar(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        a, n, c, s = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        a,  = functionargs
        n = check_equality_and_get([safe_len("'polynomialpow2bar': incorrect parameters",a)],"Error while calling 'polynomialpow2bar': looks like one of arguments has wrong size")
        c = check_equality_and_get([0],"Error while calling 'polynomialpow2bar': looks like one of arguments has wrong size")
        s = check_equality_and_get([1],"Error while calling 'polynomialpow2bar': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'polynomialpow2bar': function must have 4 or 1 parameters")

    # convert to .NET types
    _net_a = net_from_list(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.polynomialpow2bar' must be real vector")
    _net_n = n
    _net_c = c
    _net_s = s
    try:

        # call function
        _net_p = _net_alglib.polynomialpow2bar(_net_a, _net_n, _net_c, _net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    p = barycentricinterpolant(_net_p)

    # return
    return p

def polynomialbuild(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        x, y, n = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        x, y = functionargs
        n = check_equality_and_get([safe_len("'polynomialbuild': incorrect parameters",x), safe_len("'polynomialbuild': incorrect parameters",y)],"Error while calling 'polynomialbuild': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'polynomialbuild': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.polynomialbuild' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.polynomialbuild' must be real vector")
    _net_n = n
    try:

        # call function
        _net_p = _net_alglib.polynomialbuild(_net_x, _net_y, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    p = barycentricinterpolant(_net_p)

    # return
    return p

def polynomialbuildeqdist(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        a, b, y, n = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        a, b, y = functionargs
        n = check_equality_and_get([safe_len("'polynomialbuildeqdist': incorrect parameters",y)],"Error while calling 'polynomialbuildeqdist': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'polynomialbuildeqdist': function must have 4 or 3 parameters")

    # convert to .NET types
    _net_a = a
    _net_b = b
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.polynomialbuildeqdist' must be real vector")
    _net_n = n
    try:

        # call function
        _net_p = _net_alglib.polynomialbuildeqdist(_net_a, _net_b, _net_y, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    p = barycentricinterpolant(_net_p)

    # return
    return p

def polynomialbuildcheb1(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        a, b, y, n = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        a, b, y = functionargs
        n = check_equality_and_get([safe_len("'polynomialbuildcheb1': incorrect parameters",y)],"Error while calling 'polynomialbuildcheb1': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'polynomialbuildcheb1': function must have 4 or 3 parameters")

    # convert to .NET types
    _net_a = a
    _net_b = b
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.polynomialbuildcheb1' must be real vector")
    _net_n = n
    try:

        # call function
        _net_p = _net_alglib.polynomialbuildcheb1(_net_a, _net_b, _net_y, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    p = barycentricinterpolant(_net_p)

    # return
    return p

def polynomialbuildcheb2(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        a, b, y, n = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        a, b, y = functionargs
        n = check_equality_and_get([safe_len("'polynomialbuildcheb2': incorrect parameters",y)],"Error while calling 'polynomialbuildcheb2': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'polynomialbuildcheb2': function must have 4 or 3 parameters")

    # convert to .NET types
    _net_a = a
    _net_b = b
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.polynomialbuildcheb2' must be real vector")
    _net_n = n
    try:

        # call function
        _net_p = _net_alglib.polynomialbuildcheb2(_net_a, _net_b, _net_y, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    p = barycentricinterpolant(_net_p)

    # return
    return p

def polynomialcalceqdist(*functionargs):
    # unpack inputs
    if len(functionargs)==5:
        # full-form call
        a, b, f, n, t = functionargs
        friendly_form = False
    elif len(functionargs)==4:
        # short-form call
        a, b, f, t = functionargs
        n = check_equality_and_get([safe_len("'polynomialcalceqdist': incorrect parameters",f)],"Error while calling 'polynomialcalceqdist': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'polynomialcalceqdist': function must have 5 or 4 parameters")

    # convert to .NET types
    _net_a = a
    _net_b = b
    _net_f = net_from_list(f, DT_REAL, "ALGLIB: parameter 'f' of 'xalglib.polynomialcalceqdist' must be real vector")
    _net_n = n
    _net_t = t
    try:

        # call function
        _net_result = _net_alglib.polynomialcalceqdist(_net_a, _net_b, _net_f, _net_n, _net_t)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def polynomialcalccheb1(*functionargs):
    # unpack inputs
    if len(functionargs)==5:
        # full-form call
        a, b, f, n, t = functionargs
        friendly_form = False
    elif len(functionargs)==4:
        # short-form call
        a, b, f, t = functionargs
        n = check_equality_and_get([safe_len("'polynomialcalccheb1': incorrect parameters",f)],"Error while calling 'polynomialcalccheb1': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'polynomialcalccheb1': function must have 5 or 4 parameters")

    # convert to .NET types
    _net_a = a
    _net_b = b
    _net_f = net_from_list(f, DT_REAL, "ALGLIB: parameter 'f' of 'xalglib.polynomialcalccheb1' must be real vector")
    _net_n = n
    _net_t = t
    try:

        # call function
        _net_result = _net_alglib.polynomialcalccheb1(_net_a, _net_b, _net_f, _net_n, _net_t)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def polynomialcalccheb2(*functionargs):
    # unpack inputs
    if len(functionargs)==5:
        # full-form call
        a, b, f, n, t = functionargs
        friendly_form = False
    elif len(functionargs)==4:
        # short-form call
        a, b, f, t = functionargs
        n = check_equality_and_get([safe_len("'polynomialcalccheb2': incorrect parameters",f)],"Error while calling 'polynomialcalccheb2': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'polynomialcalccheb2': function must have 5 or 4 parameters")

    # convert to .NET types
    _net_a = a
    _net_b = b
    _net_f = net_from_list(f, DT_REAL, "ALGLIB: parameter 'f' of 'xalglib.polynomialcalccheb2' must be real vector")
    _net_n = n
    _net_t = t
    try:

        # call function
        _net_result = _net_alglib.polynomialcalccheb2(_net_a, _net_b, _net_f, _net_n, _net_t)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result



class polynomialfitreport(object):
    def __init__(self):
        self.taskrcond = 0
        self.rmserror = 0
        self.avgerror = 0
        self.avgrelerror = 0
        self.maxerror = 0


def net_from_polynomialfitreport(x,v):
    x.taskrcond = float(v.taskrcond)
    x.rmserror = float(v.rmserror)
    x.avgerror = float(v.avgerror)
    x.avgrelerror = float(v.avgrelerror)
    x.maxerror = float(v.maxerror)
    return




def polynomialfitreport_from_net(x):
    r = polynomialfitreport()
    r.taskrcond = x.taskrcond
    r.rmserror = x.rmserror
    r.avgerror = x.avgerror
    r.avgrelerror = x.avgrelerror
    r.maxerror = x.maxerror
    return r




class barycentricfitreport(object):
    def __init__(self):
        self.taskrcond = 0
        self.dbest = 0
        self.rmserror = 0
        self.avgerror = 0
        self.avgrelerror = 0
        self.maxerror = 0


def net_from_barycentricfitreport(x,v):
    x.taskrcond = float(v.taskrcond)
    x.dbest = int(v.dbest)
    x.rmserror = float(v.rmserror)
    x.avgerror = float(v.avgerror)
    x.avgrelerror = float(v.avgrelerror)
    x.maxerror = float(v.maxerror)
    return




def barycentricfitreport_from_net(x):
    r = barycentricfitreport()
    r.taskrcond = x.taskrcond
    r.dbest = x.dbest
    r.rmserror = x.rmserror
    r.avgerror = x.avgerror
    r.avgrelerror = x.avgrelerror
    r.maxerror = x.maxerror
    return r




class lsfitreport(object):
    def __init__(self):
        self.taskrcond = 0
        self.iterationscount = 0
        self.varidx = 0
        self.rmserror = 0
        self.avgerror = 0
        self.avgrelerror = 0
        self.maxerror = 0
        self.wrmserror = 0
        self.covpar = [[]]
        self.errpar = []
        self.errcurve = []
        self.noise = []
        self.r2 = 0


def net_from_lsfitreport(x,v):
    x.taskrcond = float(v.taskrcond)
    x.iterationscount = int(v.iterationscount)
    x.varidx = int(v.varidx)
    x.rmserror = float(v.rmserror)
    x.avgerror = float(v.avgerror)
    x.avgrelerror = float(v.avgrelerror)
    x.maxerror = float(v.maxerror)
    x.wrmserror = float(v.wrmserror)
    x.covpar = net_from_listlist(v.covpar, DT_REAL)
    x.errpar = net_from_list(v.errpar, DT_REAL)
    x.errcurve = net_from_list(v.errcurve, DT_REAL)
    x.noise = net_from_list(v.noise, DT_REAL)
    x.r2 = float(v.r2)
    return




def lsfitreport_from_net(x):
    r = lsfitreport()
    r.taskrcond = x.taskrcond
    r.iterationscount = x.iterationscount
    r.varidx = x.varidx
    r.rmserror = x.rmserror
    r.avgerror = x.avgerror
    r.avgrelerror = x.avgrelerror
    r.maxerror = x.maxerror
    r.wrmserror = x.wrmserror
    r.covpar = listlist_from_net(x.covpar, DT_REAL)
    r.errpar = list_from_net(x.errpar, DT_REAL)
    r.errcurve = list_from_net(x.errcurve, DT_REAL)
    r.noise = list_from_net(x.noise, DT_REAL)
    r.r2 = x.r2
    return r




class lsfitstate(object):
    def __init__(self,ptr):
        self.ptr = ptr
def lstfitpiecewiselinearrdpfixed(*functionargs):
    # unpack inputs
    x, y, n, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.lstfitpiecewiselinearrdpfixed' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.lstfitpiecewiselinearrdpfixed' must be real vector")
    _net_n = n
    _net_m = m
    try:

        # call function
        _net_x2, _net_y2, _net_nsections = _net_alglib.lstfitpiecewiselinearrdpfixed(_net_x, _net_y, _net_n, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x2 = list_from_net(_net_x2, DT_REAL)
    y2 = list_from_net(_net_y2, DT_REAL)
    nsections = _net_nsections

    # return
    return (x2, y2, nsections)

def lstfitpiecewiselinearrdp(*functionargs):
    # unpack inputs
    x, y, n, eps = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.lstfitpiecewiselinearrdp' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.lstfitpiecewiselinearrdp' must be real vector")
    _net_n = n
    _net_eps = eps
    try:

        # call function
        _net_x2, _net_y2, _net_nsections = _net_alglib.lstfitpiecewiselinearrdp(_net_x, _net_y, _net_n, _net_eps)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x2 = list_from_net(_net_x2, DT_REAL)
    y2 = list_from_net(_net_y2, DT_REAL)
    nsections = _net_nsections

    # return
    return (x2, y2, nsections)

def polynomialfit(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        x, y, n, m = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        x, y, m = functionargs
        n = check_equality_and_get([safe_len("'polynomialfit': incorrect parameters",x), safe_len("'polynomialfit': incorrect parameters",y)],"Error while calling 'polynomialfit': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'polynomialfit': function must have 4 or 3 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.polynomialfit' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.polynomialfit' must be real vector")
    _net_n = n
    _net_m = m
    try:

        # call function
        _net_info, _net_p, _net_rep = _net_alglib.polynomialfit(_net_x, _net_y, _net_n, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    p = barycentricinterpolant(_net_p)
    rep = polynomialfitreport_from_net(_net_rep)

    # return
    return (info, p, rep)

def smp_polynomialfit(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        x, y, n, m = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        x, y, m = functionargs
        n = check_equality_and_get([safe_len("'smp_polynomialfit': incorrect parameters",x), safe_len("'smp_polynomialfit': incorrect parameters",y)],"Error while calling 'smp_polynomialfit': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'smp_polynomialfit': function must have 4 or 3 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.smp_polynomialfit' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.smp_polynomialfit' must be real vector")
    _net_n = n
    _net_m = m
    try:

        # call function
        _net_info, _net_p, _net_rep = _net_alglib.smp_polynomialfit(_net_x, _net_y, _net_n, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    p = barycentricinterpolant(_net_p)
    rep = polynomialfitreport_from_net(_net_rep)

    # return
    return (info, p, rep)

def polynomialfitwc(*functionargs):
    # unpack inputs
    if len(functionargs)==9:
        # full-form call
        x, y, w, n, xc, yc, dc, k, m = functionargs
        friendly_form = False
    elif len(functionargs)==7:
        # short-form call
        x, y, w, xc, yc, dc, m = functionargs
        n = check_equality_and_get([safe_len("'polynomialfitwc': incorrect parameters",x), safe_len("'polynomialfitwc': incorrect parameters",y), safe_len("'polynomialfitwc': incorrect parameters",w)],"Error while calling 'polynomialfitwc': looks like one of arguments has wrong size")
        k = check_equality_and_get([safe_len("'polynomialfitwc': incorrect parameters",xc), safe_len("'polynomialfitwc': incorrect parameters",yc), safe_len("'polynomialfitwc': incorrect parameters",dc)],"Error while calling 'polynomialfitwc': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'polynomialfitwc': function must have 9 or 7 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.polynomialfitwc' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.polynomialfitwc' must be real vector")
    _net_w = net_from_list(w, DT_REAL, "ALGLIB: parameter 'w' of 'xalglib.polynomialfitwc' must be real vector")
    _net_n = n
    _net_xc = net_from_list(xc, DT_REAL, "ALGLIB: parameter 'xc' of 'xalglib.polynomialfitwc' must be real vector")
    _net_yc = net_from_list(yc, DT_REAL, "ALGLIB: parameter 'yc' of 'xalglib.polynomialfitwc' must be real vector")
    _net_dc = net_from_list(dc, DT_INT, "ALGLIB: parameter 'dc' of 'xalglib.polynomialfitwc' must be int vector")
    _net_k = k
    _net_m = m
    try:

        # call function
        _net_info, _net_p, _net_rep = _net_alglib.polynomialfitwc(_net_x, _net_y, _net_w, _net_n, _net_xc, _net_yc, _net_dc, _net_k, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    p = barycentricinterpolant(_net_p)
    rep = polynomialfitreport_from_net(_net_rep)

    # return
    return (info, p, rep)

def smp_polynomialfitwc(*functionargs):
    # unpack inputs
    if len(functionargs)==9:
        # full-form call
        x, y, w, n, xc, yc, dc, k, m = functionargs
        friendly_form = False
    elif len(functionargs)==7:
        # short-form call
        x, y, w, xc, yc, dc, m = functionargs
        n = check_equality_and_get([safe_len("'smp_polynomialfitwc': incorrect parameters",x), safe_len("'smp_polynomialfitwc': incorrect parameters",y), safe_len("'smp_polynomialfitwc': incorrect parameters",w)],"Error while calling 'smp_polynomialfitwc': looks like one of arguments has wrong size")
        k = check_equality_and_get([safe_len("'smp_polynomialfitwc': incorrect parameters",xc), safe_len("'smp_polynomialfitwc': incorrect parameters",yc), safe_len("'smp_polynomialfitwc': incorrect parameters",dc)],"Error while calling 'smp_polynomialfitwc': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'smp_polynomialfitwc': function must have 9 or 7 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.smp_polynomialfitwc' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.smp_polynomialfitwc' must be real vector")
    _net_w = net_from_list(w, DT_REAL, "ALGLIB: parameter 'w' of 'xalglib.smp_polynomialfitwc' must be real vector")
    _net_n = n
    _net_xc = net_from_list(xc, DT_REAL, "ALGLIB: parameter 'xc' of 'xalglib.smp_polynomialfitwc' must be real vector")
    _net_yc = net_from_list(yc, DT_REAL, "ALGLIB: parameter 'yc' of 'xalglib.smp_polynomialfitwc' must be real vector")
    _net_dc = net_from_list(dc, DT_INT, "ALGLIB: parameter 'dc' of 'xalglib.smp_polynomialfitwc' must be int vector")
    _net_k = k
    _net_m = m
    try:

        # call function
        _net_info, _net_p, _net_rep = _net_alglib.smp_polynomialfitwc(_net_x, _net_y, _net_w, _net_n, _net_xc, _net_yc, _net_dc, _net_k, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    p = barycentricinterpolant(_net_p)
    rep = polynomialfitreport_from_net(_net_rep)

    # return
    return (info, p, rep)

def logisticcalc4(*functionargs):
    # unpack inputs
    x, a, b, c, d = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = x
    _net_a = a
    _net_b = b
    _net_c = c
    _net_d = d
    try:

        # call function
        _net_result = _net_alglib.logisticcalc4(_net_x, _net_a, _net_b, _net_c, _net_d)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def logisticcalc5(*functionargs):
    # unpack inputs
    x, a, b, c, d, g = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = x
    _net_a = a
    _net_b = b
    _net_c = c
    _net_d = d
    _net_g = g
    try:

        # call function
        _net_result = _net_alglib.logisticcalc5(_net_x, _net_a, _net_b, _net_c, _net_d, _net_g)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def logisticfit4(*functionargs):
    # unpack inputs
    x, y, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.logisticfit4' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.logisticfit4' must be real vector")
    _net_n = n
    try:

        # call function
        _net_a, _net_b, _net_c, _net_d, _net_rep = _net_alglib.logisticfit4(_net_x, _net_y, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = _net_a
    b = _net_b
    c = _net_c
    d = _net_d
    rep = lsfitreport_from_net(_net_rep)

    # return
    return (a, b, c, d, rep)

def logisticfit4ec(*functionargs):
    # unpack inputs
    x, y, n, cnstrleft, cnstrright = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.logisticfit4ec' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.logisticfit4ec' must be real vector")
    _net_n = n
    _net_cnstrleft = cnstrleft
    _net_cnstrright = cnstrright
    try:

        # call function
        _net_a, _net_b, _net_c, _net_d, _net_rep = _net_alglib.logisticfit4ec(_net_x, _net_y, _net_n, _net_cnstrleft, _net_cnstrright)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = _net_a
    b = _net_b
    c = _net_c
    d = _net_d
    rep = lsfitreport_from_net(_net_rep)

    # return
    return (a, b, c, d, rep)

def logisticfit5(*functionargs):
    # unpack inputs
    x, y, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.logisticfit5' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.logisticfit5' must be real vector")
    _net_n = n
    try:

        # call function
        _net_a, _net_b, _net_c, _net_d, _net_g, _net_rep = _net_alglib.logisticfit5(_net_x, _net_y, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = _net_a
    b = _net_b
    c = _net_c
    d = _net_d
    g = _net_g
    rep = lsfitreport_from_net(_net_rep)

    # return
    return (a, b, c, d, g, rep)

def logisticfit5ec(*functionargs):
    # unpack inputs
    x, y, n, cnstrleft, cnstrright = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.logisticfit5ec' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.logisticfit5ec' must be real vector")
    _net_n = n
    _net_cnstrleft = cnstrleft
    _net_cnstrright = cnstrright
    try:

        # call function
        _net_a, _net_b, _net_c, _net_d, _net_g, _net_rep = _net_alglib.logisticfit5ec(_net_x, _net_y, _net_n, _net_cnstrleft, _net_cnstrright)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = _net_a
    b = _net_b
    c = _net_c
    d = _net_d
    g = _net_g
    rep = lsfitreport_from_net(_net_rep)

    # return
    return (a, b, c, d, g, rep)

def logisticfit45x(*functionargs):
    # unpack inputs
    x, y, n, cnstrleft, cnstrright, is4pl, lambdav, epsx, rscnt = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.logisticfit45x' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.logisticfit45x' must be real vector")
    _net_n = n
    _net_cnstrleft = cnstrleft
    _net_cnstrright = cnstrright
    _net_is4pl = is4pl
    _net_lambdav = lambdav
    _net_epsx = epsx
    _net_rscnt = rscnt
    try:

        # call function
        _net_a, _net_b, _net_c, _net_d, _net_g, _net_rep = _net_alglib.logisticfit45x(_net_x, _net_y, _net_n, _net_cnstrleft, _net_cnstrright, _net_is4pl, _net_lambdav, _net_epsx, _net_rscnt)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    a = _net_a
    b = _net_b
    c = _net_c
    d = _net_d
    g = _net_g
    rep = lsfitreport_from_net(_net_rep)

    # return
    return (a, b, c, d, g, rep)

def barycentricfitfloaterhormannwc(*functionargs):
    # unpack inputs
    x, y, w, n, xc, yc, dc, k, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.barycentricfitfloaterhormannwc' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.barycentricfitfloaterhormannwc' must be real vector")
    _net_w = net_from_list(w, DT_REAL, "ALGLIB: parameter 'w' of 'xalglib.barycentricfitfloaterhormannwc' must be real vector")
    _net_n = n
    _net_xc = net_from_list(xc, DT_REAL, "ALGLIB: parameter 'xc' of 'xalglib.barycentricfitfloaterhormannwc' must be real vector")
    _net_yc = net_from_list(yc, DT_REAL, "ALGLIB: parameter 'yc' of 'xalglib.barycentricfitfloaterhormannwc' must be real vector")
    _net_dc = net_from_list(dc, DT_INT, "ALGLIB: parameter 'dc' of 'xalglib.barycentricfitfloaterhormannwc' must be int vector")
    _net_k = k
    _net_m = m
    try:

        # call function
        _net_info, _net_b, _net_rep = _net_alglib.barycentricfitfloaterhormannwc(_net_x, _net_y, _net_w, _net_n, _net_xc, _net_yc, _net_dc, _net_k, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    b = barycentricinterpolant(_net_b)
    rep = barycentricfitreport_from_net(_net_rep)

    # return
    return (info, b, rep)

def smp_barycentricfitfloaterhormannwc(*functionargs):
    # unpack inputs
    x, y, w, n, xc, yc, dc, k, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.smp_barycentricfitfloaterhormannwc' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.smp_barycentricfitfloaterhormannwc' must be real vector")
    _net_w = net_from_list(w, DT_REAL, "ALGLIB: parameter 'w' of 'xalglib.smp_barycentricfitfloaterhormannwc' must be real vector")
    _net_n = n
    _net_xc = net_from_list(xc, DT_REAL, "ALGLIB: parameter 'xc' of 'xalglib.smp_barycentricfitfloaterhormannwc' must be real vector")
    _net_yc = net_from_list(yc, DT_REAL, "ALGLIB: parameter 'yc' of 'xalglib.smp_barycentricfitfloaterhormannwc' must be real vector")
    _net_dc = net_from_list(dc, DT_INT, "ALGLIB: parameter 'dc' of 'xalglib.smp_barycentricfitfloaterhormannwc' must be int vector")
    _net_k = k
    _net_m = m
    try:

        # call function
        _net_info, _net_b, _net_rep = _net_alglib.smp_barycentricfitfloaterhormannwc(_net_x, _net_y, _net_w, _net_n, _net_xc, _net_yc, _net_dc, _net_k, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    b = barycentricinterpolant(_net_b)
    rep = barycentricfitreport_from_net(_net_rep)

    # return
    return (info, b, rep)

def barycentricfitfloaterhormann(*functionargs):
    # unpack inputs
    x, y, n, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.barycentricfitfloaterhormann' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.barycentricfitfloaterhormann' must be real vector")
    _net_n = n
    _net_m = m
    try:

        # call function
        _net_info, _net_b, _net_rep = _net_alglib.barycentricfitfloaterhormann(_net_x, _net_y, _net_n, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    b = barycentricinterpolant(_net_b)
    rep = barycentricfitreport_from_net(_net_rep)

    # return
    return (info, b, rep)

def smp_barycentricfitfloaterhormann(*functionargs):
    # unpack inputs
    x, y, n, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.smp_barycentricfitfloaterhormann' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.smp_barycentricfitfloaterhormann' must be real vector")
    _net_n = n
    _net_m = m
    try:

        # call function
        _net_info, _net_b, _net_rep = _net_alglib.smp_barycentricfitfloaterhormann(_net_x, _net_y, _net_n, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    b = barycentricinterpolant(_net_b)
    rep = barycentricfitreport_from_net(_net_rep)

    # return
    return (info, b, rep)

def spline1dfitcubicwc(*functionargs):
    # unpack inputs
    if len(functionargs)==9:
        # full-form call
        x, y, w, n, xc, yc, dc, k, m = functionargs
        friendly_form = False
    elif len(functionargs)==7:
        # short-form call
        x, y, w, xc, yc, dc, m = functionargs
        n = check_equality_and_get([safe_len("'spline1dfitcubicwc': incorrect parameters",x), safe_len("'spline1dfitcubicwc': incorrect parameters",y), safe_len("'spline1dfitcubicwc': incorrect parameters",w)],"Error while calling 'spline1dfitcubicwc': looks like one of arguments has wrong size")
        k = check_equality_and_get([safe_len("'spline1dfitcubicwc': incorrect parameters",xc), safe_len("'spline1dfitcubicwc': incorrect parameters",yc), safe_len("'spline1dfitcubicwc': incorrect parameters",dc)],"Error while calling 'spline1dfitcubicwc': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'spline1dfitcubicwc': function must have 9 or 7 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.spline1dfitcubicwc' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.spline1dfitcubicwc' must be real vector")
    _net_w = net_from_list(w, DT_REAL, "ALGLIB: parameter 'w' of 'xalglib.spline1dfitcubicwc' must be real vector")
    _net_n = n
    _net_xc = net_from_list(xc, DT_REAL, "ALGLIB: parameter 'xc' of 'xalglib.spline1dfitcubicwc' must be real vector")
    _net_yc = net_from_list(yc, DT_REAL, "ALGLIB: parameter 'yc' of 'xalglib.spline1dfitcubicwc' must be real vector")
    _net_dc = net_from_list(dc, DT_INT, "ALGLIB: parameter 'dc' of 'xalglib.spline1dfitcubicwc' must be int vector")
    _net_k = k
    _net_m = m
    try:

        # call function
        _net_info, _net_s, _net_rep = _net_alglib.spline1dfitcubicwc(_net_x, _net_y, _net_w, _net_n, _net_xc, _net_yc, _net_dc, _net_k, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    s = spline1dinterpolant(_net_s)
    rep = spline1dfitreport_from_net(_net_rep)

    # return
    return (info, s, rep)

def smp_spline1dfitcubicwc(*functionargs):
    # unpack inputs
    if len(functionargs)==9:
        # full-form call
        x, y, w, n, xc, yc, dc, k, m = functionargs
        friendly_form = False
    elif len(functionargs)==7:
        # short-form call
        x, y, w, xc, yc, dc, m = functionargs
        n = check_equality_and_get([safe_len("'smp_spline1dfitcubicwc': incorrect parameters",x), safe_len("'smp_spline1dfitcubicwc': incorrect parameters",y), safe_len("'smp_spline1dfitcubicwc': incorrect parameters",w)],"Error while calling 'smp_spline1dfitcubicwc': looks like one of arguments has wrong size")
        k = check_equality_and_get([safe_len("'smp_spline1dfitcubicwc': incorrect parameters",xc), safe_len("'smp_spline1dfitcubicwc': incorrect parameters",yc), safe_len("'smp_spline1dfitcubicwc': incorrect parameters",dc)],"Error while calling 'smp_spline1dfitcubicwc': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'smp_spline1dfitcubicwc': function must have 9 or 7 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.smp_spline1dfitcubicwc' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.smp_spline1dfitcubicwc' must be real vector")
    _net_w = net_from_list(w, DT_REAL, "ALGLIB: parameter 'w' of 'xalglib.smp_spline1dfitcubicwc' must be real vector")
    _net_n = n
    _net_xc = net_from_list(xc, DT_REAL, "ALGLIB: parameter 'xc' of 'xalglib.smp_spline1dfitcubicwc' must be real vector")
    _net_yc = net_from_list(yc, DT_REAL, "ALGLIB: parameter 'yc' of 'xalglib.smp_spline1dfitcubicwc' must be real vector")
    _net_dc = net_from_list(dc, DT_INT, "ALGLIB: parameter 'dc' of 'xalglib.smp_spline1dfitcubicwc' must be int vector")
    _net_k = k
    _net_m = m
    try:

        # call function
        _net_info, _net_s, _net_rep = _net_alglib.smp_spline1dfitcubicwc(_net_x, _net_y, _net_w, _net_n, _net_xc, _net_yc, _net_dc, _net_k, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    s = spline1dinterpolant(_net_s)
    rep = spline1dfitreport_from_net(_net_rep)

    # return
    return (info, s, rep)

def spline1dfithermitewc(*functionargs):
    # unpack inputs
    if len(functionargs)==9:
        # full-form call
        x, y, w, n, xc, yc, dc, k, m = functionargs
        friendly_form = False
    elif len(functionargs)==7:
        # short-form call
        x, y, w, xc, yc, dc, m = functionargs
        n = check_equality_and_get([safe_len("'spline1dfithermitewc': incorrect parameters",x), safe_len("'spline1dfithermitewc': incorrect parameters",y), safe_len("'spline1dfithermitewc': incorrect parameters",w)],"Error while calling 'spline1dfithermitewc': looks like one of arguments has wrong size")
        k = check_equality_and_get([safe_len("'spline1dfithermitewc': incorrect parameters",xc), safe_len("'spline1dfithermitewc': incorrect parameters",yc), safe_len("'spline1dfithermitewc': incorrect parameters",dc)],"Error while calling 'spline1dfithermitewc': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'spline1dfithermitewc': function must have 9 or 7 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.spline1dfithermitewc' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.spline1dfithermitewc' must be real vector")
    _net_w = net_from_list(w, DT_REAL, "ALGLIB: parameter 'w' of 'xalglib.spline1dfithermitewc' must be real vector")
    _net_n = n
    _net_xc = net_from_list(xc, DT_REAL, "ALGLIB: parameter 'xc' of 'xalglib.spline1dfithermitewc' must be real vector")
    _net_yc = net_from_list(yc, DT_REAL, "ALGLIB: parameter 'yc' of 'xalglib.spline1dfithermitewc' must be real vector")
    _net_dc = net_from_list(dc, DT_INT, "ALGLIB: parameter 'dc' of 'xalglib.spline1dfithermitewc' must be int vector")
    _net_k = k
    _net_m = m
    try:

        # call function
        _net_info, _net_s, _net_rep = _net_alglib.spline1dfithermitewc(_net_x, _net_y, _net_w, _net_n, _net_xc, _net_yc, _net_dc, _net_k, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    s = spline1dinterpolant(_net_s)
    rep = spline1dfitreport_from_net(_net_rep)

    # return
    return (info, s, rep)

def smp_spline1dfithermitewc(*functionargs):
    # unpack inputs
    if len(functionargs)==9:
        # full-form call
        x, y, w, n, xc, yc, dc, k, m = functionargs
        friendly_form = False
    elif len(functionargs)==7:
        # short-form call
        x, y, w, xc, yc, dc, m = functionargs
        n = check_equality_and_get([safe_len("'smp_spline1dfithermitewc': incorrect parameters",x), safe_len("'smp_spline1dfithermitewc': incorrect parameters",y), safe_len("'smp_spline1dfithermitewc': incorrect parameters",w)],"Error while calling 'smp_spline1dfithermitewc': looks like one of arguments has wrong size")
        k = check_equality_and_get([safe_len("'smp_spline1dfithermitewc': incorrect parameters",xc), safe_len("'smp_spline1dfithermitewc': incorrect parameters",yc), safe_len("'smp_spline1dfithermitewc': incorrect parameters",dc)],"Error while calling 'smp_spline1dfithermitewc': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'smp_spline1dfithermitewc': function must have 9 or 7 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.smp_spline1dfithermitewc' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.smp_spline1dfithermitewc' must be real vector")
    _net_w = net_from_list(w, DT_REAL, "ALGLIB: parameter 'w' of 'xalglib.smp_spline1dfithermitewc' must be real vector")
    _net_n = n
    _net_xc = net_from_list(xc, DT_REAL, "ALGLIB: parameter 'xc' of 'xalglib.smp_spline1dfithermitewc' must be real vector")
    _net_yc = net_from_list(yc, DT_REAL, "ALGLIB: parameter 'yc' of 'xalglib.smp_spline1dfithermitewc' must be real vector")
    _net_dc = net_from_list(dc, DT_INT, "ALGLIB: parameter 'dc' of 'xalglib.smp_spline1dfithermitewc' must be int vector")
    _net_k = k
    _net_m = m
    try:

        # call function
        _net_info, _net_s, _net_rep = _net_alglib.smp_spline1dfithermitewc(_net_x, _net_y, _net_w, _net_n, _net_xc, _net_yc, _net_dc, _net_k, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    s = spline1dinterpolant(_net_s)
    rep = spline1dfitreport_from_net(_net_rep)

    # return
    return (info, s, rep)

def spline1dfitcubic(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        x, y, n, m = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        x, y, m = functionargs
        n = check_equality_and_get([safe_len("'spline1dfitcubic': incorrect parameters",x), safe_len("'spline1dfitcubic': incorrect parameters",y)],"Error while calling 'spline1dfitcubic': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'spline1dfitcubic': function must have 4 or 3 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.spline1dfitcubic' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.spline1dfitcubic' must be real vector")
    _net_n = n
    _net_m = m
    try:

        # call function
        _net_info, _net_s, _net_rep = _net_alglib.spline1dfitcubic(_net_x, _net_y, _net_n, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    s = spline1dinterpolant(_net_s)
    rep = spline1dfitreport_from_net(_net_rep)

    # return
    return (info, s, rep)

def smp_spline1dfitcubic(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        x, y, n, m = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        x, y, m = functionargs
        n = check_equality_and_get([safe_len("'smp_spline1dfitcubic': incorrect parameters",x), safe_len("'smp_spline1dfitcubic': incorrect parameters",y)],"Error while calling 'smp_spline1dfitcubic': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'smp_spline1dfitcubic': function must have 4 or 3 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.smp_spline1dfitcubic' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.smp_spline1dfitcubic' must be real vector")
    _net_n = n
    _net_m = m
    try:

        # call function
        _net_info, _net_s, _net_rep = _net_alglib.smp_spline1dfitcubic(_net_x, _net_y, _net_n, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    s = spline1dinterpolant(_net_s)
    rep = spline1dfitreport_from_net(_net_rep)

    # return
    return (info, s, rep)

def spline1dfithermite(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        x, y, n, m = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        x, y, m = functionargs
        n = check_equality_and_get([safe_len("'spline1dfithermite': incorrect parameters",x), safe_len("'spline1dfithermite': incorrect parameters",y)],"Error while calling 'spline1dfithermite': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'spline1dfithermite': function must have 4 or 3 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.spline1dfithermite' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.spline1dfithermite' must be real vector")
    _net_n = n
    _net_m = m
    try:

        # call function
        _net_info, _net_s, _net_rep = _net_alglib.spline1dfithermite(_net_x, _net_y, _net_n, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    s = spline1dinterpolant(_net_s)
    rep = spline1dfitreport_from_net(_net_rep)

    # return
    return (info, s, rep)

def smp_spline1dfithermite(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        x, y, n, m = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        x, y, m = functionargs
        n = check_equality_and_get([safe_len("'smp_spline1dfithermite': incorrect parameters",x), safe_len("'smp_spline1dfithermite': incorrect parameters",y)],"Error while calling 'smp_spline1dfithermite': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'smp_spline1dfithermite': function must have 4 or 3 parameters")

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.smp_spline1dfithermite' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.smp_spline1dfithermite' must be real vector")
    _net_n = n
    _net_m = m
    try:

        # call function
        _net_info, _net_s, _net_rep = _net_alglib.smp_spline1dfithermite(_net_x, _net_y, _net_n, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    s = spline1dinterpolant(_net_s)
    rep = spline1dfitreport_from_net(_net_rep)

    # return
    return (info, s, rep)

def lsfitlinearw(*functionargs):
    # unpack inputs
    if len(functionargs)==5:
        # full-form call
        y, w, fmatrix, n, m = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        y, w, fmatrix = functionargs
        n = check_equality_and_get([safe_len("'lsfitlinearw': incorrect parameters",y), safe_len("'lsfitlinearw': incorrect parameters",w), safe_rows("'lsfitlinearw': incorrect parameters",fmatrix)],"Error while calling 'lsfitlinearw': looks like one of arguments has wrong size")
        m = check_equality_and_get([safe_cols("'lsfitlinearw': incorrect parameters",fmatrix)],"Error while calling 'lsfitlinearw': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'lsfitlinearw': function must have 5 or 3 parameters")

    # convert to .NET types
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.lsfitlinearw' must be real vector")
    _net_w = net_from_list(w, DT_REAL, "ALGLIB: parameter 'w' of 'xalglib.lsfitlinearw' must be real vector")
    _net_fmatrix = net_from_listlist(fmatrix, DT_REAL, "ALGLIB: parameter 'fmatrix' of 'xalglib.lsfitlinearw' must be real matrix")
    _net_n = n
    _net_m = m
    try:

        # call function
        _net_info, _net_c, _net_rep = _net_alglib.lsfitlinearw(_net_y, _net_w, _net_fmatrix, _net_n, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    c = list_from_net(_net_c, DT_REAL)
    rep = lsfitreport_from_net(_net_rep)

    # return
    return (info, c, rep)

def smp_lsfitlinearw(*functionargs):
    # unpack inputs
    if len(functionargs)==5:
        # full-form call
        y, w, fmatrix, n, m = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        y, w, fmatrix = functionargs
        n = check_equality_and_get([safe_len("'smp_lsfitlinearw': incorrect parameters",y), safe_len("'smp_lsfitlinearw': incorrect parameters",w), safe_rows("'smp_lsfitlinearw': incorrect parameters",fmatrix)],"Error while calling 'smp_lsfitlinearw': looks like one of arguments has wrong size")
        m = check_equality_and_get([safe_cols("'smp_lsfitlinearw': incorrect parameters",fmatrix)],"Error while calling 'smp_lsfitlinearw': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'smp_lsfitlinearw': function must have 5 or 3 parameters")

    # convert to .NET types
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.smp_lsfitlinearw' must be real vector")
    _net_w = net_from_list(w, DT_REAL, "ALGLIB: parameter 'w' of 'xalglib.smp_lsfitlinearw' must be real vector")
    _net_fmatrix = net_from_listlist(fmatrix, DT_REAL, "ALGLIB: parameter 'fmatrix' of 'xalglib.smp_lsfitlinearw' must be real matrix")
    _net_n = n
    _net_m = m
    try:

        # call function
        _net_info, _net_c, _net_rep = _net_alglib.smp_lsfitlinearw(_net_y, _net_w, _net_fmatrix, _net_n, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    c = list_from_net(_net_c, DT_REAL)
    rep = lsfitreport_from_net(_net_rep)

    # return
    return (info, c, rep)

def lsfitlinearwc(*functionargs):
    # unpack inputs
    if len(functionargs)==7:
        # full-form call
        y, w, fmatrix, cmatrix, n, m, k = functionargs
        friendly_form = False
    elif len(functionargs)==4:
        # short-form call
        y, w, fmatrix, cmatrix = functionargs
        n = check_equality_and_get([safe_len("'lsfitlinearwc': incorrect parameters",y), safe_len("'lsfitlinearwc': incorrect parameters",w), safe_rows("'lsfitlinearwc': incorrect parameters",fmatrix)],"Error while calling 'lsfitlinearwc': looks like one of arguments has wrong size")
        m = check_equality_and_get([safe_cols("'lsfitlinearwc': incorrect parameters",fmatrix), safe_cols("'lsfitlinearwc': incorrect parameters",cmatrix)-1],"Error while calling 'lsfitlinearwc': looks like one of arguments has wrong size")
        k = check_equality_and_get([safe_rows("'lsfitlinearwc': incorrect parameters",cmatrix)],"Error while calling 'lsfitlinearwc': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'lsfitlinearwc': function must have 7 or 4 parameters")

    # convert to .NET types
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.lsfitlinearwc' must be real vector")
    _net_w = net_from_list(w, DT_REAL, "ALGLIB: parameter 'w' of 'xalglib.lsfitlinearwc' must be real vector")
    _net_fmatrix = net_from_listlist(fmatrix, DT_REAL, "ALGLIB: parameter 'fmatrix' of 'xalglib.lsfitlinearwc' must be real matrix")
    _net_cmatrix = net_from_listlist(cmatrix, DT_REAL, "ALGLIB: parameter 'cmatrix' of 'xalglib.lsfitlinearwc' must be real matrix")
    _net_n = n
    _net_m = m
    _net_k = k
    try:

        # call function
        _net_info, _net_c, _net_rep = _net_alglib.lsfitlinearwc(_net_y, _net_w, _net_fmatrix, _net_cmatrix, _net_n, _net_m, _net_k)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    c = list_from_net(_net_c, DT_REAL)
    rep = lsfitreport_from_net(_net_rep)

    # return
    return (info, c, rep)

def smp_lsfitlinearwc(*functionargs):
    # unpack inputs
    if len(functionargs)==7:
        # full-form call
        y, w, fmatrix, cmatrix, n, m, k = functionargs
        friendly_form = False
    elif len(functionargs)==4:
        # short-form call
        y, w, fmatrix, cmatrix = functionargs
        n = check_equality_and_get([safe_len("'smp_lsfitlinearwc': incorrect parameters",y), safe_len("'smp_lsfitlinearwc': incorrect parameters",w), safe_rows("'smp_lsfitlinearwc': incorrect parameters",fmatrix)],"Error while calling 'smp_lsfitlinearwc': looks like one of arguments has wrong size")
        m = check_equality_and_get([safe_cols("'smp_lsfitlinearwc': incorrect parameters",fmatrix), safe_cols("'smp_lsfitlinearwc': incorrect parameters",cmatrix)-1],"Error while calling 'smp_lsfitlinearwc': looks like one of arguments has wrong size")
        k = check_equality_and_get([safe_rows("'smp_lsfitlinearwc': incorrect parameters",cmatrix)],"Error while calling 'smp_lsfitlinearwc': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'smp_lsfitlinearwc': function must have 7 or 4 parameters")

    # convert to .NET types
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.smp_lsfitlinearwc' must be real vector")
    _net_w = net_from_list(w, DT_REAL, "ALGLIB: parameter 'w' of 'xalglib.smp_lsfitlinearwc' must be real vector")
    _net_fmatrix = net_from_listlist(fmatrix, DT_REAL, "ALGLIB: parameter 'fmatrix' of 'xalglib.smp_lsfitlinearwc' must be real matrix")
    _net_cmatrix = net_from_listlist(cmatrix, DT_REAL, "ALGLIB: parameter 'cmatrix' of 'xalglib.smp_lsfitlinearwc' must be real matrix")
    _net_n = n
    _net_m = m
    _net_k = k
    try:

        # call function
        _net_info, _net_c, _net_rep = _net_alglib.smp_lsfitlinearwc(_net_y, _net_w, _net_fmatrix, _net_cmatrix, _net_n, _net_m, _net_k)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    c = list_from_net(_net_c, DT_REAL)
    rep = lsfitreport_from_net(_net_rep)

    # return
    return (info, c, rep)

def lsfitlinear(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        y, fmatrix, n, m = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        y, fmatrix = functionargs
        n = check_equality_and_get([safe_len("'lsfitlinear': incorrect parameters",y), safe_rows("'lsfitlinear': incorrect parameters",fmatrix)],"Error while calling 'lsfitlinear': looks like one of arguments has wrong size")
        m = check_equality_and_get([safe_cols("'lsfitlinear': incorrect parameters",fmatrix)],"Error while calling 'lsfitlinear': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'lsfitlinear': function must have 4 or 2 parameters")

    # convert to .NET types
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.lsfitlinear' must be real vector")
    _net_fmatrix = net_from_listlist(fmatrix, DT_REAL, "ALGLIB: parameter 'fmatrix' of 'xalglib.lsfitlinear' must be real matrix")
    _net_n = n
    _net_m = m
    try:

        # call function
        _net_info, _net_c, _net_rep = _net_alglib.lsfitlinear(_net_y, _net_fmatrix, _net_n, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    c = list_from_net(_net_c, DT_REAL)
    rep = lsfitreport_from_net(_net_rep)

    # return
    return (info, c, rep)

def smp_lsfitlinear(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        y, fmatrix, n, m = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        y, fmatrix = functionargs
        n = check_equality_and_get([safe_len("'smp_lsfitlinear': incorrect parameters",y), safe_rows("'smp_lsfitlinear': incorrect parameters",fmatrix)],"Error while calling 'smp_lsfitlinear': looks like one of arguments has wrong size")
        m = check_equality_and_get([safe_cols("'smp_lsfitlinear': incorrect parameters",fmatrix)],"Error while calling 'smp_lsfitlinear': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'smp_lsfitlinear': function must have 4 or 2 parameters")

    # convert to .NET types
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.smp_lsfitlinear' must be real vector")
    _net_fmatrix = net_from_listlist(fmatrix, DT_REAL, "ALGLIB: parameter 'fmatrix' of 'xalglib.smp_lsfitlinear' must be real matrix")
    _net_n = n
    _net_m = m
    try:

        # call function
        _net_info, _net_c, _net_rep = _net_alglib.smp_lsfitlinear(_net_y, _net_fmatrix, _net_n, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    c = list_from_net(_net_c, DT_REAL)
    rep = lsfitreport_from_net(_net_rep)

    # return
    return (info, c, rep)

def lsfitlinearc(*functionargs):
    # unpack inputs
    if len(functionargs)==6:
        # full-form call
        y, fmatrix, cmatrix, n, m, k = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        y, fmatrix, cmatrix = functionargs
        n = check_equality_and_get([safe_len("'lsfitlinearc': incorrect parameters",y), safe_rows("'lsfitlinearc': incorrect parameters",fmatrix)],"Error while calling 'lsfitlinearc': looks like one of arguments has wrong size")
        m = check_equality_and_get([safe_cols("'lsfitlinearc': incorrect parameters",fmatrix), safe_cols("'lsfitlinearc': incorrect parameters",cmatrix)-1],"Error while calling 'lsfitlinearc': looks like one of arguments has wrong size")
        k = check_equality_and_get([safe_rows("'lsfitlinearc': incorrect parameters",cmatrix)],"Error while calling 'lsfitlinearc': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'lsfitlinearc': function must have 6 or 3 parameters")

    # convert to .NET types
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.lsfitlinearc' must be real vector")
    _net_fmatrix = net_from_listlist(fmatrix, DT_REAL, "ALGLIB: parameter 'fmatrix' of 'xalglib.lsfitlinearc' must be real matrix")
    _net_cmatrix = net_from_listlist(cmatrix, DT_REAL, "ALGLIB: parameter 'cmatrix' of 'xalglib.lsfitlinearc' must be real matrix")
    _net_n = n
    _net_m = m
    _net_k = k
    try:

        # call function
        _net_info, _net_c, _net_rep = _net_alglib.lsfitlinearc(_net_y, _net_fmatrix, _net_cmatrix, _net_n, _net_m, _net_k)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    c = list_from_net(_net_c, DT_REAL)
    rep = lsfitreport_from_net(_net_rep)

    # return
    return (info, c, rep)

def smp_lsfitlinearc(*functionargs):
    # unpack inputs
    if len(functionargs)==6:
        # full-form call
        y, fmatrix, cmatrix, n, m, k = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        y, fmatrix, cmatrix = functionargs
        n = check_equality_and_get([safe_len("'smp_lsfitlinearc': incorrect parameters",y), safe_rows("'smp_lsfitlinearc': incorrect parameters",fmatrix)],"Error while calling 'smp_lsfitlinearc': looks like one of arguments has wrong size")
        m = check_equality_and_get([safe_cols("'smp_lsfitlinearc': incorrect parameters",fmatrix), safe_cols("'smp_lsfitlinearc': incorrect parameters",cmatrix)-1],"Error while calling 'smp_lsfitlinearc': looks like one of arguments has wrong size")
        k = check_equality_and_get([safe_rows("'smp_lsfitlinearc': incorrect parameters",cmatrix)],"Error while calling 'smp_lsfitlinearc': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'smp_lsfitlinearc': function must have 6 or 3 parameters")

    # convert to .NET types
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.smp_lsfitlinearc' must be real vector")
    _net_fmatrix = net_from_listlist(fmatrix, DT_REAL, "ALGLIB: parameter 'fmatrix' of 'xalglib.smp_lsfitlinearc' must be real matrix")
    _net_cmatrix = net_from_listlist(cmatrix, DT_REAL, "ALGLIB: parameter 'cmatrix' of 'xalglib.smp_lsfitlinearc' must be real matrix")
    _net_n = n
    _net_m = m
    _net_k = k
    try:

        # call function
        _net_info, _net_c, _net_rep = _net_alglib.smp_lsfitlinearc(_net_y, _net_fmatrix, _net_cmatrix, _net_n, _net_m, _net_k)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    c = list_from_net(_net_c, DT_REAL)
    rep = lsfitreport_from_net(_net_rep)

    # return
    return (info, c, rep)

def lsfitcreatewf(*functionargs):
    # unpack inputs
    if len(functionargs)==8:
        # full-form call
        x, y, w, c, n, m, k, diffstep = functionargs
        friendly_form = False
    elif len(functionargs)==5:
        # short-form call
        x, y, w, c, diffstep = functionargs
        n = check_equality_and_get([safe_rows("'lsfitcreatewf': incorrect parameters",x), safe_len("'lsfitcreatewf': incorrect parameters",y), safe_len("'lsfitcreatewf': incorrect parameters",w)],"Error while calling 'lsfitcreatewf': looks like one of arguments has wrong size")
        m = check_equality_and_get([safe_cols("'lsfitcreatewf': incorrect parameters",x)],"Error while calling 'lsfitcreatewf': looks like one of arguments has wrong size")
        k = check_equality_and_get([safe_len("'lsfitcreatewf': incorrect parameters",c)],"Error while calling 'lsfitcreatewf': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'lsfitcreatewf': function must have 8 or 5 parameters")

    # convert to .NET types
    _net_x = net_from_listlist(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.lsfitcreatewf' must be real matrix")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.lsfitcreatewf' must be real vector")
    _net_w = net_from_list(w, DT_REAL, "ALGLIB: parameter 'w' of 'xalglib.lsfitcreatewf' must be real vector")
    _net_c = net_from_list(c, DT_REAL, "ALGLIB: parameter 'c' of 'xalglib.lsfitcreatewf' must be real vector")
    _net_n = n
    _net_m = m
    _net_k = k
    _net_diffstep = diffstep
    try:

        # call function
        _net_state = _net_alglib.lsfitcreatewf(_net_x, _net_y, _net_w, _net_c, _net_n, _net_m, _net_k, _net_diffstep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = lsfitstate(_net_state)

    # return
    return state

def lsfitcreatef(*functionargs):
    # unpack inputs
    if len(functionargs)==7:
        # full-form call
        x, y, c, n, m, k, diffstep = functionargs
        friendly_form = False
    elif len(functionargs)==4:
        # short-form call
        x, y, c, diffstep = functionargs
        n = check_equality_and_get([safe_rows("'lsfitcreatef': incorrect parameters",x), safe_len("'lsfitcreatef': incorrect parameters",y)],"Error while calling 'lsfitcreatef': looks like one of arguments has wrong size")
        m = check_equality_and_get([safe_cols("'lsfitcreatef': incorrect parameters",x)],"Error while calling 'lsfitcreatef': looks like one of arguments has wrong size")
        k = check_equality_and_get([safe_len("'lsfitcreatef': incorrect parameters",c)],"Error while calling 'lsfitcreatef': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'lsfitcreatef': function must have 7 or 4 parameters")

    # convert to .NET types
    _net_x = net_from_listlist(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.lsfitcreatef' must be real matrix")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.lsfitcreatef' must be real vector")
    _net_c = net_from_list(c, DT_REAL, "ALGLIB: parameter 'c' of 'xalglib.lsfitcreatef' must be real vector")
    _net_n = n
    _net_m = m
    _net_k = k
    _net_diffstep = diffstep
    try:

        # call function
        _net_state = _net_alglib.lsfitcreatef(_net_x, _net_y, _net_c, _net_n, _net_m, _net_k, _net_diffstep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = lsfitstate(_net_state)

    # return
    return state

def lsfitcreatewfg(*functionargs):
    # unpack inputs
    if len(functionargs)==8:
        # full-form call
        x, y, w, c, n, m, k, cheapfg = functionargs
        friendly_form = False
    elif len(functionargs)==5:
        # short-form call
        x, y, w, c, cheapfg = functionargs
        n = check_equality_and_get([safe_rows("'lsfitcreatewfg': incorrect parameters",x), safe_len("'lsfitcreatewfg': incorrect parameters",y), safe_len("'lsfitcreatewfg': incorrect parameters",w)],"Error while calling 'lsfitcreatewfg': looks like one of arguments has wrong size")
        m = check_equality_and_get([safe_cols("'lsfitcreatewfg': incorrect parameters",x)],"Error while calling 'lsfitcreatewfg': looks like one of arguments has wrong size")
        k = check_equality_and_get([safe_len("'lsfitcreatewfg': incorrect parameters",c)],"Error while calling 'lsfitcreatewfg': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'lsfitcreatewfg': function must have 8 or 5 parameters")

    # convert to .NET types
    _net_x = net_from_listlist(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.lsfitcreatewfg' must be real matrix")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.lsfitcreatewfg' must be real vector")
    _net_w = net_from_list(w, DT_REAL, "ALGLIB: parameter 'w' of 'xalglib.lsfitcreatewfg' must be real vector")
    _net_c = net_from_list(c, DT_REAL, "ALGLIB: parameter 'c' of 'xalglib.lsfitcreatewfg' must be real vector")
    _net_n = n
    _net_m = m
    _net_k = k
    _net_cheapfg = cheapfg
    try:

        # call function
        _net_state = _net_alglib.lsfitcreatewfg(_net_x, _net_y, _net_w, _net_c, _net_n, _net_m, _net_k, _net_cheapfg)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = lsfitstate(_net_state)

    # return
    return state

def lsfitcreatefg(*functionargs):
    # unpack inputs
    if len(functionargs)==7:
        # full-form call
        x, y, c, n, m, k, cheapfg = functionargs
        friendly_form = False
    elif len(functionargs)==4:
        # short-form call
        x, y, c, cheapfg = functionargs
        n = check_equality_and_get([safe_rows("'lsfitcreatefg': incorrect parameters",x), safe_len("'lsfitcreatefg': incorrect parameters",y)],"Error while calling 'lsfitcreatefg': looks like one of arguments has wrong size")
        m = check_equality_and_get([safe_cols("'lsfitcreatefg': incorrect parameters",x)],"Error while calling 'lsfitcreatefg': looks like one of arguments has wrong size")
        k = check_equality_and_get([safe_len("'lsfitcreatefg': incorrect parameters",c)],"Error while calling 'lsfitcreatefg': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'lsfitcreatefg': function must have 7 or 4 parameters")

    # convert to .NET types
    _net_x = net_from_listlist(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.lsfitcreatefg' must be real matrix")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.lsfitcreatefg' must be real vector")
    _net_c = net_from_list(c, DT_REAL, "ALGLIB: parameter 'c' of 'xalglib.lsfitcreatefg' must be real vector")
    _net_n = n
    _net_m = m
    _net_k = k
    _net_cheapfg = cheapfg
    try:

        # call function
        _net_state = _net_alglib.lsfitcreatefg(_net_x, _net_y, _net_c, _net_n, _net_m, _net_k, _net_cheapfg)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = lsfitstate(_net_state)

    # return
    return state

def lsfitcreatewfgh(*functionargs):
    # unpack inputs
    if len(functionargs)==7:
        # full-form call
        x, y, w, c, n, m, k = functionargs
        friendly_form = False
    elif len(functionargs)==4:
        # short-form call
        x, y, w, c = functionargs
        n = check_equality_and_get([safe_rows("'lsfitcreatewfgh': incorrect parameters",x), safe_len("'lsfitcreatewfgh': incorrect parameters",y), safe_len("'lsfitcreatewfgh': incorrect parameters",w)],"Error while calling 'lsfitcreatewfgh': looks like one of arguments has wrong size")
        m = check_equality_and_get([safe_cols("'lsfitcreatewfgh': incorrect parameters",x)],"Error while calling 'lsfitcreatewfgh': looks like one of arguments has wrong size")
        k = check_equality_and_get([safe_len("'lsfitcreatewfgh': incorrect parameters",c)],"Error while calling 'lsfitcreatewfgh': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'lsfitcreatewfgh': function must have 7 or 4 parameters")

    # convert to .NET types
    _net_x = net_from_listlist(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.lsfitcreatewfgh' must be real matrix")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.lsfitcreatewfgh' must be real vector")
    _net_w = net_from_list(w, DT_REAL, "ALGLIB: parameter 'w' of 'xalglib.lsfitcreatewfgh' must be real vector")
    _net_c = net_from_list(c, DT_REAL, "ALGLIB: parameter 'c' of 'xalglib.lsfitcreatewfgh' must be real vector")
    _net_n = n
    _net_m = m
    _net_k = k
    try:

        # call function
        _net_state = _net_alglib.lsfitcreatewfgh(_net_x, _net_y, _net_w, _net_c, _net_n, _net_m, _net_k)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = lsfitstate(_net_state)

    # return
    return state

def lsfitcreatefgh(*functionargs):
    # unpack inputs
    if len(functionargs)==6:
        # full-form call
        x, y, c, n, m, k = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        x, y, c = functionargs
        n = check_equality_and_get([safe_rows("'lsfitcreatefgh': incorrect parameters",x), safe_len("'lsfitcreatefgh': incorrect parameters",y)],"Error while calling 'lsfitcreatefgh': looks like one of arguments has wrong size")
        m = check_equality_and_get([safe_cols("'lsfitcreatefgh': incorrect parameters",x)],"Error while calling 'lsfitcreatefgh': looks like one of arguments has wrong size")
        k = check_equality_and_get([safe_len("'lsfitcreatefgh': incorrect parameters",c)],"Error while calling 'lsfitcreatefgh': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'lsfitcreatefgh': function must have 6 or 3 parameters")

    # convert to .NET types
    _net_x = net_from_listlist(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.lsfitcreatefgh' must be real matrix")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.lsfitcreatefgh' must be real vector")
    _net_c = net_from_list(c, DT_REAL, "ALGLIB: parameter 'c' of 'xalglib.lsfitcreatefgh' must be real vector")
    _net_n = n
    _net_m = m
    _net_k = k
    try:

        # call function
        _net_state = _net_alglib.lsfitcreatefgh(_net_x, _net_y, _net_c, _net_n, _net_m, _net_k)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = lsfitstate(_net_state)

    # return
    return state

def lsfitsetcond(*functionargs):
    # unpack inputs
    state, epsx, maxits = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_epsx = epsx
    _net_maxits = maxits
    try:

        # call function
        _net_alglib.lsfitsetcond(_net_state, _net_epsx, _net_maxits)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def lsfitsetstpmax(*functionargs):
    # unpack inputs
    state, stpmax = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_stpmax = stpmax
    try:

        # call function
        _net_alglib.lsfitsetstpmax(_net_state, _net_stpmax)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def lsfitsetxrep(*functionargs):
    # unpack inputs
    state, needxrep = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_needxrep = needxrep
    try:

        # call function
        _net_alglib.lsfitsetxrep(_net_state, _net_needxrep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def lsfitsetscale(*functionargs):
    # unpack inputs
    state, s = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_s = net_from_list(s, DT_REAL, "ALGLIB: parameter 's' of 'xalglib.lsfitsetscale' must be real vector")
    try:

        # call function
        _net_alglib.lsfitsetscale(_net_state, _net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def lsfitsetbc(*functionargs):
    # unpack inputs
    state, bndl, bndu = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_bndl = net_from_list(bndl, DT_REAL, "ALGLIB: parameter 'bndl' of 'xalglib.lsfitsetbc' must be real vector")
    _net_bndu = net_from_list(bndu, DT_REAL, "ALGLIB: parameter 'bndu' of 'xalglib.lsfitsetbc' must be real vector")
    try:

        # call function
        _net_alglib.lsfitsetbc(_net_state, _net_bndl, _net_bndu)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def lsfitsetlc(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        state, c, ct, k = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        state, c, ct = functionargs
        k = check_equality_and_get([safe_rows("'lsfitsetlc': incorrect parameters",c), safe_len("'lsfitsetlc': incorrect parameters",ct)],"Error while calling 'lsfitsetlc': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'lsfitsetlc': function must have 4 or 3 parameters")

    # convert to .NET types
    _net_state = state.ptr
    _net_c = net_from_listlist(c, DT_REAL, "ALGLIB: parameter 'c' of 'xalglib.lsfitsetlc' must be real matrix")
    _net_ct = net_from_list(ct, DT_INT, "ALGLIB: parameter 'ct' of 'xalglib.lsfitsetlc' must be int vector")
    _net_k = k
    try:

        # call function
        _net_alglib.lsfitsetlc(_net_state, _net_c, _net_ct, _net_k)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return



def lsfitfit_f(state, func, rep = None, param = None):
    _net_c  = state.ptr.c
    _py_c = create_real_vector(_net_c.GetLength(0))
    _net_x  = state.ptr.x
    _py_x = create_real_vector(_net_x.GetLength(0))
    while True:
        try:
            result = _net_alglib.lsfititeration(state.ptr)
        except _net_alglib.alglibexception as e:
            raise RuntimeError(e.msg)
        if not result:
            break
        if state.ptr.needf:
            copy_net_to_list(_net_c, _py_c, DT_REAL)
            copy_net_to_list(_net_x, _py_x, DT_REAL)
            fvalue = func(_py_c, _py_x, param)
            state.ptr.f = fvalue
            continue
        if state.ptr.xupdated:
            if not (rep is None):
                copy_net_to_list(_net_c, _py_c, DT_REAL)
                rep(_py_c, state.ptr.f, param)
            continue
        raise RuntimeError("ALGLIB: error in 'lsfitfit' (some derivatives were not provided?)")
    return


def lsfitfit_fg(state, func, grad, rep = None, param = None):
    _net_c  = state.ptr.c
    _py_c = create_real_vector(_net_c.GetLength(0))
    _net_x  = state.ptr.x
    _py_x = create_real_vector(_net_x.GetLength(0))
    _net_g  = state.ptr.g
    _py_g = create_real_vector(_net_g.GetLength(0))
    while True:
        try:
            result = _net_alglib.lsfititeration(state.ptr)
        except _net_alglib.alglibexception as e:
            raise RuntimeError(e.msg)
        if not result:
            break
        if state.ptr.needf:
            copy_net_to_list(_net_c, _py_c, DT_REAL)
            copy_net_to_list(_net_x, _py_x, DT_REAL)
            fvalue = func(_py_c, _py_x, param)
            state.ptr.f = fvalue
            continue
        if state.ptr.needfg:
            copy_net_to_list(_net_c, _py_c, DT_REAL)
            copy_net_to_list(_net_x, _py_x, DT_REAL)
            fvalue = grad(_py_c, _py_x, _py_g, param)
            state.ptr.f = fvalue
            copy_list_to_net(_py_g, _net_g, DT_REAL)
            continue
        if state.ptr.xupdated:
            if not (rep is None):
                copy_net_to_list(_net_c, _py_c, DT_REAL)
                rep(_py_c, state.ptr.f, param)
            continue
        raise RuntimeError("ALGLIB: error in 'lsfitfit' (some derivatives were not provided?)")
    return


def lsfitfit_fgh(state, func, grad, hess, rep = None, param = None):
    _net_c  = state.ptr.c
    _py_c = create_real_vector(_net_c.GetLength(0))
    _net_x  = state.ptr.x
    _py_x = create_real_vector(_net_x.GetLength(0))
    _net_g  = state.ptr.g
    _py_g = create_real_vector(_net_g.GetLength(0))
    _net_h  = state.ptr.h
    _py_h = create_real_matrix(_net_h.GetLength(0),_net_h.GetLength(1))
    while True:
        try:
            result = _net_alglib.lsfititeration(state.ptr)
        except _net_alglib.alglibexception as e:
            raise RuntimeError(e.msg)
        if not result:
            break
        if state.ptr.needf:
            copy_net_to_list(_net_c, _py_c, DT_REAL)
            copy_net_to_list(_net_x, _py_x, DT_REAL)
            fvalue = func(_py_c, _py_x, param)
            state.ptr.f = fvalue
            continue
        if state.ptr.needfg:
            copy_net_to_list(_net_c, _py_c, DT_REAL)
            copy_net_to_list(_net_x, _py_x, DT_REAL)
            fvalue = grad(_py_c, _py_x, _py_g, param)
            state.ptr.f = fvalue
            copy_list_to_net(_py_g, _net_g, DT_REAL)
            continue
        if state.ptr.needfgh:
            copy_net_to_list(_net_c, _py_c, DT_REAL)
            copy_net_to_list(_net_x, _py_x, DT_REAL)
            fvalue = hess(_py_c, _py_x, _py_g, _py_h, param)
            state.ptr.f = fvalue
            copy_list_to_net(_py_g, _net_g, DT_REAL)
            copy_listlist_to_net(_py_h, _net_h, DT_REAL)
            continue
        if state.ptr.xupdated:
            if not (rep is None):
                copy_net_to_list(_net_c, _py_c, DT_REAL)
                rep(_py_c, state.ptr.f, param)
            continue
        raise RuntimeError("ALGLIB: error in 'lsfitfit' (some derivatives were not provided?)")
    return


def lsfitresults(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_info, _net_c, _net_rep = _net_alglib.lsfitresults(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    info = _net_info
    c = list_from_net(_net_c, DT_REAL)
    rep = lsfitreport_from_net(_net_rep)

    # return
    return (info, c, rep)

def lsfitsetgradientcheck(*functionargs):
    # unpack inputs
    state, teststep = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_teststep = teststep
    try:

        # call function
        _net_alglib.lsfitsetgradientcheck(_net_state, _net_teststep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def nsfitspheremcc(*functionargs):
    # unpack inputs
    xy, npoints, nx = functionargs
    friendly_form = False

    # convert to .NET types
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.nsfitspheremcc' must be real matrix")
    _net_npoints = npoints
    _net_nx = nx
    try:

        # call function
        _net_cx, _net_rhi = _net_alglib.nsfitspheremcc(_net_xy, _net_npoints, _net_nx)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    cx = list_from_net(_net_cx, DT_REAL)
    rhi = _net_rhi

    # return
    return (cx, rhi)

def nsfitspheremic(*functionargs):
    # unpack inputs
    xy, npoints, nx = functionargs
    friendly_form = False

    # convert to .NET types
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.nsfitspheremic' must be real matrix")
    _net_npoints = npoints
    _net_nx = nx
    try:

        # call function
        _net_cx, _net_rlo = _net_alglib.nsfitspheremic(_net_xy, _net_npoints, _net_nx)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    cx = list_from_net(_net_cx, DT_REAL)
    rlo = _net_rlo

    # return
    return (cx, rlo)

def nsfitspheremzc(*functionargs):
    # unpack inputs
    xy, npoints, nx = functionargs
    friendly_form = False

    # convert to .NET types
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.nsfitspheremzc' must be real matrix")
    _net_npoints = npoints
    _net_nx = nx
    try:

        # call function
        _net_cx, _net_rlo, _net_rhi = _net_alglib.nsfitspheremzc(_net_xy, _net_npoints, _net_nx)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    cx = list_from_net(_net_cx, DT_REAL)
    rlo = _net_rlo
    rhi = _net_rhi

    # return
    return (cx, rlo, rhi)

def nsfitspherex(*functionargs):
    # unpack inputs
    xy, npoints, nx, problemtype, epsx, aulits, penalty = functionargs
    friendly_form = False

    # convert to .NET types
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.nsfitspherex' must be real matrix")
    _net_npoints = npoints
    _net_nx = nx
    _net_problemtype = problemtype
    _net_epsx = epsx
    _net_aulits = aulits
    _net_penalty = penalty
    try:

        # call function
        _net_cx, _net_rlo, _net_rhi = _net_alglib.nsfitspherex(_net_xy, _net_npoints, _net_nx, _net_problemtype, _net_epsx, _net_aulits, _net_penalty)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    cx = list_from_net(_net_cx, DT_REAL)
    rlo = _net_rlo
    rhi = _net_rhi

    # return
    return (cx, rlo, rhi)



class spline2dinterpolant(object):
    def __init__(self,ptr):
        self.ptr = ptr
def spline2dcalc(*functionargs):
    # unpack inputs
    c, x, y = functionargs
    friendly_form = False

    # convert to .NET types
    _net_c = c.ptr
    _net_x = x
    _net_y = y
    try:

        # call function
        _net_result = _net_alglib.spline2dcalc(_net_c, _net_x, _net_y)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def spline2ddiff(*functionargs):
    # unpack inputs
    c, x, y = functionargs
    friendly_form = False

    # convert to .NET types
    _net_c = c.ptr
    _net_x = x
    _net_y = y
    try:

        # call function
        _net_f, _net_fx, _net_fy, _net_fxy = _net_alglib.spline2ddiff(_net_c, _net_x, _net_y)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    f = _net_f
    fx = _net_fx
    fy = _net_fy
    fxy = _net_fxy

    # return
    return (f, fx, fy, fxy)

def spline2dlintransxy(*functionargs):
    # unpack inputs
    c, ax, bx, ay, by = functionargs
    friendly_form = False

    # convert to .NET types
    _net_c = c.ptr
    _net_ax = ax
    _net_bx = bx
    _net_ay = ay
    _net_by = by
    try:

        # call function
        _net_alglib.spline2dlintransxy(_net_c, _net_ax, _net_bx, _net_ay, _net_by)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def spline2dlintransf(*functionargs):
    # unpack inputs
    c, a, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_c = c.ptr
    _net_a = a
    _net_b = b
    try:

        # call function
        _net_alglib.spline2dlintransf(_net_c, _net_a, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def spline2dcopy(*functionargs):
    # unpack inputs
    c,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_c = c.ptr
    try:

        # call function
        _net_cc = _net_alglib.spline2dcopy(_net_c)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    cc = spline2dinterpolant(_net_cc)

    # return
    return cc

def spline2dresamplebicubic(*functionargs):
    # unpack inputs
    a, oldheight, oldwidth, newheight, newwidth = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.spline2dresamplebicubic' must be real matrix")
    _net_oldheight = oldheight
    _net_oldwidth = oldwidth
    _net_newheight = newheight
    _net_newwidth = newwidth
    try:

        # call function
        _net_b = _net_alglib.spline2dresamplebicubic(_net_a, _net_oldheight, _net_oldwidth, _net_newheight, _net_newwidth)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = listlist_from_net(_net_b, DT_REAL)

    # return
    return b

def spline2dresamplebilinear(*functionargs):
    # unpack inputs
    a, oldheight, oldwidth, newheight, newwidth = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.spline2dresamplebilinear' must be real matrix")
    _net_oldheight = oldheight
    _net_oldwidth = oldwidth
    _net_newheight = newheight
    _net_newwidth = newwidth
    try:

        # call function
        _net_b = _net_alglib.spline2dresamplebilinear(_net_a, _net_oldheight, _net_oldwidth, _net_newheight, _net_newwidth)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = listlist_from_net(_net_b, DT_REAL)

    # return
    return b

def spline2dbuildbilinearv(*functionargs):
    # unpack inputs
    x, n, y, m, f, d = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.spline2dbuildbilinearv' must be real vector")
    _net_n = n
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.spline2dbuildbilinearv' must be real vector")
    _net_m = m
    _net_f = net_from_list(f, DT_REAL, "ALGLIB: parameter 'f' of 'xalglib.spline2dbuildbilinearv' must be real vector")
    _net_d = d
    try:

        # call function
        _net_c = _net_alglib.spline2dbuildbilinearv(_net_x, _net_n, _net_y, _net_m, _net_f, _net_d)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = spline2dinterpolant(_net_c)

    # return
    return c

def spline2dbuildbicubicv(*functionargs):
    # unpack inputs
    x, n, y, m, f, d = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.spline2dbuildbicubicv' must be real vector")
    _net_n = n
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.spline2dbuildbicubicv' must be real vector")
    _net_m = m
    _net_f = net_from_list(f, DT_REAL, "ALGLIB: parameter 'f' of 'xalglib.spline2dbuildbicubicv' must be real vector")
    _net_d = d
    try:

        # call function
        _net_c = _net_alglib.spline2dbuildbicubicv(_net_x, _net_n, _net_y, _net_m, _net_f, _net_d)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = spline2dinterpolant(_net_c)

    # return
    return c

def spline2dcalcvbuf(*functionargs):
    # unpack inputs
    c, x, y, f = functionargs
    friendly_form = False

    # convert to .NET types
    _net_c = c.ptr
    _net_x = x
    _net_y = y
    _net_f = net_from_list(f, DT_REAL, "ALGLIB: parameter 'f' of 'xalglib.spline2dcalcvbuf' must be real vector")
    try:

        # call function
        _net_f = _net_alglib.spline2dcalcvbuf(_net_c, _net_x, _net_y, _net_f)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    f = list_from_net(_net_f, DT_REAL)

    # return
    return f

def spline2dcalcv(*functionargs):
    # unpack inputs
    c, x, y = functionargs
    friendly_form = False

    # convert to .NET types
    _net_c = c.ptr
    _net_x = x
    _net_y = y
    try:

        # call function
        _net_f = _net_alglib.spline2dcalcv(_net_c, _net_x, _net_y)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    f = list_from_net(_net_f, DT_REAL)

    # return
    return f

def spline2dunpackv(*functionargs):
    # unpack inputs
    c,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_c = c.ptr
    try:

        # call function
        _net_m, _net_n, _net_d, _net_tbl = _net_alglib.spline2dunpackv(_net_c)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    m = _net_m
    n = _net_n
    d = _net_d
    tbl = listlist_from_net(_net_tbl, DT_REAL)

    # return
    return (m, n, d, tbl)

def spline2dbuildbilinear(*functionargs):
    # unpack inputs
    x, y, f, m, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.spline2dbuildbilinear' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.spline2dbuildbilinear' must be real vector")
    _net_f = net_from_listlist(f, DT_REAL, "ALGLIB: parameter 'f' of 'xalglib.spline2dbuildbilinear' must be real matrix")
    _net_m = m
    _net_n = n
    try:

        # call function
        _net_c = _net_alglib.spline2dbuildbilinear(_net_x, _net_y, _net_f, _net_m, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = spline2dinterpolant(_net_c)

    # return
    return c

def spline2dbuildbicubic(*functionargs):
    # unpack inputs
    x, y, f, m, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.spline2dbuildbicubic' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.spline2dbuildbicubic' must be real vector")
    _net_f = net_from_listlist(f, DT_REAL, "ALGLIB: parameter 'f' of 'xalglib.spline2dbuildbicubic' must be real matrix")
    _net_m = m
    _net_n = n
    try:

        # call function
        _net_c = _net_alglib.spline2dbuildbicubic(_net_x, _net_y, _net_f, _net_m, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = spline2dinterpolant(_net_c)

    # return
    return c

def spline2dunpack(*functionargs):
    # unpack inputs
    c,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_c = c.ptr
    try:

        # call function
        _net_m, _net_n, _net_tbl = _net_alglib.spline2dunpack(_net_c)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    m = _net_m
    n = _net_n
    tbl = listlist_from_net(_net_tbl, DT_REAL)

    # return
    return (m, n, tbl)



class rbfcalcbuffer(object):
    def __init__(self,ptr):
        self.ptr = ptr


class rbfmodel(object):
    def __init__(self,ptr):
        self.ptr = ptr


class rbfreport(object):
    def __init__(self):
        self.rmserror = 0
        self.maxerror = 0
        self.arows = 0
        self.acols = 0
        self.annz = 0
        self.iterationscount = 0
        self.nmv = 0
        self.terminationtype = 0


def net_from_rbfreport(x,v):
    x.rmserror = float(v.rmserror)
    x.maxerror = float(v.maxerror)
    x.arows = int(v.arows)
    x.acols = int(v.acols)
    x.annz = int(v.annz)
    x.iterationscount = int(v.iterationscount)
    x.nmv = int(v.nmv)
    x.terminationtype = int(v.terminationtype)
    return




def rbfreport_from_net(x):
    r = rbfreport()
    r.rmserror = x.rmserror
    r.maxerror = x.maxerror
    r.arows = x.arows
    r.acols = x.acols
    r.annz = x.annz
    r.iterationscount = x.iterationscount
    r.nmv = x.nmv
    r.terminationtype = x.terminationtype
    return r


def rbfserialize(obj):
    try:
        return _net_alglib.rbfserialize(obj.ptr)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

def rbfunserialize(s_in):
    try:
        return rbfmodel(_net_alglib.rbfunserialize(s_in))
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)
def rbfcreate(*functionargs):
    # unpack inputs
    nx, ny = functionargs
    friendly_form = False

    # convert to .NET types
    _net_nx = nx
    _net_ny = ny
    try:

        # call function
        _net_s = _net_alglib.rbfcreate(_net_nx, _net_ny)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    s = rbfmodel(_net_s)

    # return
    return s

def rbfcreatecalcbuffer(*functionargs):
    # unpack inputs
    s,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    try:

        # call function
        _net_buf = _net_alglib.rbfcreatecalcbuffer(_net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    buf = rbfcalcbuffer(_net_buf)

    # return
    return buf

def rbfsetpoints(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        s, xy, n = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        s, xy = functionargs
        n = check_equality_and_get([safe_rows("'rbfsetpoints': incorrect parameters",xy)],"Error while calling 'rbfsetpoints': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'rbfsetpoints': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_s = s.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.rbfsetpoints' must be real matrix")
    _net_n = n
    try:

        # call function
        _net_alglib.rbfsetpoints(_net_s, _net_xy, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def rbfsetpointsandscales(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        r, xy, n, s = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        r, xy, s = functionargs
        n = check_equality_and_get([safe_rows("'rbfsetpointsandscales': incorrect parameters",xy)],"Error while calling 'rbfsetpointsandscales': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'rbfsetpointsandscales': function must have 4 or 3 parameters")

    # convert to .NET types
    _net_r = r.ptr
    _net_xy = net_from_listlist(xy, DT_REAL, "ALGLIB: parameter 'xy' of 'xalglib.rbfsetpointsandscales' must be real matrix")
    _net_n = n
    _net_s = net_from_list(s, DT_REAL, "ALGLIB: parameter 's' of 'xalglib.rbfsetpointsandscales' must be real vector")
    try:

        # call function
        _net_alglib.rbfsetpointsandscales(_net_r, _net_xy, _net_n, _net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def rbfsetalgoqnn(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        s, q, z = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        s,  = functionargs
        q = check_equality_and_get([1.0],"Error while calling 'rbfsetalgoqnn': looks like one of arguments has wrong size")
        z = check_equality_and_get([5.0],"Error while calling 'rbfsetalgoqnn': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'rbfsetalgoqnn': function must have 3 or 1 parameters")

    # convert to .NET types
    _net_s = s.ptr
    _net_q = q
    _net_z = z
    try:

        # call function
        _net_alglib.rbfsetalgoqnn(_net_s, _net_q, _net_z)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def rbfsetalgomultilayer(*functionargs):
    # unpack inputs
    if len(functionargs)==4:
        # full-form call
        s, rbase, nlayers, lambdav = functionargs
        friendly_form = False
    elif len(functionargs)==3:
        # short-form call
        s, rbase, nlayers = functionargs
        lambdav = check_equality_and_get([0.01],"Error while calling 'rbfsetalgomultilayer': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'rbfsetalgomultilayer': function must have 4 or 3 parameters")

    # convert to .NET types
    _net_s = s.ptr
    _net_rbase = rbase
    _net_nlayers = nlayers
    _net_lambdav = lambdav
    try:

        # call function
        _net_alglib.rbfsetalgomultilayer(_net_s, _net_rbase, _net_nlayers, _net_lambdav)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def rbfsetalgohierarchical(*functionargs):
    # unpack inputs
    s, rbase, nlayers, lambdans = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_rbase = rbase
    _net_nlayers = nlayers
    _net_lambdans = lambdans
    try:

        # call function
        _net_alglib.rbfsetalgohierarchical(_net_s, _net_rbase, _net_nlayers, _net_lambdans)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def rbfsetlinterm(*functionargs):
    # unpack inputs
    s,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    try:

        # call function
        _net_alglib.rbfsetlinterm(_net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def rbfsetconstterm(*functionargs):
    # unpack inputs
    s,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    try:

        # call function
        _net_alglib.rbfsetconstterm(_net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def rbfsetzeroterm(*functionargs):
    # unpack inputs
    s,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    try:

        # call function
        _net_alglib.rbfsetzeroterm(_net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def rbfsetv2bf(*functionargs):
    # unpack inputs
    s, bf = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_bf = bf
    try:

        # call function
        _net_alglib.rbfsetv2bf(_net_s, _net_bf)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def rbfsetv2its(*functionargs):
    # unpack inputs
    s, maxits = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_maxits = maxits
    try:

        # call function
        _net_alglib.rbfsetv2its(_net_s, _net_maxits)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def rbfsetv2supportr(*functionargs):
    # unpack inputs
    s, r = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_r = r
    try:

        # call function
        _net_alglib.rbfsetv2supportr(_net_s, _net_r)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def rbfbuildmodel(*functionargs):
    # unpack inputs
    s,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    try:

        # call function
        _net_rep = _net_alglib.rbfbuildmodel(_net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    rep = rbfreport_from_net(_net_rep)

    # return
    return rep

def rbfcalc1(*functionargs):
    # unpack inputs
    s, x0 = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_x0 = x0
    try:

        # call function
        _net_result = _net_alglib.rbfcalc1(_net_s, _net_x0)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def rbfcalc2(*functionargs):
    # unpack inputs
    s, x0, x1 = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_x0 = x0
    _net_x1 = x1
    try:

        # call function
        _net_result = _net_alglib.rbfcalc2(_net_s, _net_x0, _net_x1)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def rbfcalc3(*functionargs):
    # unpack inputs
    s, x0, x1, x2 = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_x0 = x0
    _net_x1 = x1
    _net_x2 = x2
    try:

        # call function
        _net_result = _net_alglib.rbfcalc3(_net_s, _net_x0, _net_x1, _net_x2)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def rbfcalc(*functionargs):
    # unpack inputs
    s, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.rbfcalc' must be real vector")
    try:

        # call function
        _net_y = _net_alglib.rbfcalc(_net_s, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    y = list_from_net(_net_y, DT_REAL)

    # return
    return y

def rbfcalcbuf(*functionargs):
    # unpack inputs
    s, x, y = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.rbfcalcbuf' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.rbfcalcbuf' must be real vector")
    try:

        # call function
        _net_y = _net_alglib.rbfcalcbuf(_net_s, _net_x, _net_y)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    y = list_from_net(_net_y, DT_REAL)

    # return
    return y

def rbftscalcbuf(*functionargs):
    # unpack inputs
    s, buf, x, y = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_buf = buf.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.rbftscalcbuf' must be real vector")
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.rbftscalcbuf' must be real vector")
    try:

        # call function
        _net_y = _net_alglib.rbftscalcbuf(_net_s, _net_buf, _net_x, _net_y)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    y = list_from_net(_net_y, DT_REAL)

    # return
    return y

def rbfgridcalc2(*functionargs):
    # unpack inputs
    s, x0, n0, x1, n1 = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_x0 = net_from_list(x0, DT_REAL, "ALGLIB: parameter 'x0' of 'xalglib.rbfgridcalc2' must be real vector")
    _net_n0 = n0
    _net_x1 = net_from_list(x1, DT_REAL, "ALGLIB: parameter 'x1' of 'xalglib.rbfgridcalc2' must be real vector")
    _net_n1 = n1
    try:

        # call function
        _net_y = _net_alglib.rbfgridcalc2(_net_s, _net_x0, _net_n0, _net_x1, _net_n1)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    y = listlist_from_net(_net_y, DT_REAL)

    # return
    return y

def rbfgridcalc2v(*functionargs):
    # unpack inputs
    s, x0, n0, x1, n1 = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_x0 = net_from_list(x0, DT_REAL, "ALGLIB: parameter 'x0' of 'xalglib.rbfgridcalc2v' must be real vector")
    _net_n0 = n0
    _net_x1 = net_from_list(x1, DT_REAL, "ALGLIB: parameter 'x1' of 'xalglib.rbfgridcalc2v' must be real vector")
    _net_n1 = n1
    try:

        # call function
        _net_y = _net_alglib.rbfgridcalc2v(_net_s, _net_x0, _net_n0, _net_x1, _net_n1)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    y = list_from_net(_net_y, DT_REAL)

    # return
    return y

def smp_rbfgridcalc2v(*functionargs):
    # unpack inputs
    s, x0, n0, x1, n1 = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_x0 = net_from_list(x0, DT_REAL, "ALGLIB: parameter 'x0' of 'xalglib.smp_rbfgridcalc2v' must be real vector")
    _net_n0 = n0
    _net_x1 = net_from_list(x1, DT_REAL, "ALGLIB: parameter 'x1' of 'xalglib.smp_rbfgridcalc2v' must be real vector")
    _net_n1 = n1
    try:

        # call function
        _net_y = _net_alglib.smp_rbfgridcalc2v(_net_s, _net_x0, _net_n0, _net_x1, _net_n1)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    y = list_from_net(_net_y, DT_REAL)

    # return
    return y

def rbfgridcalc2vsubset(*functionargs):
    # unpack inputs
    s, x0, n0, x1, n1, flagy = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_x0 = net_from_list(x0, DT_REAL, "ALGLIB: parameter 'x0' of 'xalglib.rbfgridcalc2vsubset' must be real vector")
    _net_n0 = n0
    _net_x1 = net_from_list(x1, DT_REAL, "ALGLIB: parameter 'x1' of 'xalglib.rbfgridcalc2vsubset' must be real vector")
    _net_n1 = n1
    _net_flagy = net_from_list(flagy, DT_BOOL, "ALGLIB: parameter 'flagy' of 'xalglib.rbfgridcalc2vsubset' must be bool vector")
    try:

        # call function
        _net_y = _net_alglib.rbfgridcalc2vsubset(_net_s, _net_x0, _net_n0, _net_x1, _net_n1, _net_flagy)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    y = list_from_net(_net_y, DT_REAL)

    # return
    return y

def smp_rbfgridcalc2vsubset(*functionargs):
    # unpack inputs
    s, x0, n0, x1, n1, flagy = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_x0 = net_from_list(x0, DT_REAL, "ALGLIB: parameter 'x0' of 'xalglib.smp_rbfgridcalc2vsubset' must be real vector")
    _net_n0 = n0
    _net_x1 = net_from_list(x1, DT_REAL, "ALGLIB: parameter 'x1' of 'xalglib.smp_rbfgridcalc2vsubset' must be real vector")
    _net_n1 = n1
    _net_flagy = net_from_list(flagy, DT_BOOL, "ALGLIB: parameter 'flagy' of 'xalglib.smp_rbfgridcalc2vsubset' must be bool vector")
    try:

        # call function
        _net_y = _net_alglib.smp_rbfgridcalc2vsubset(_net_s, _net_x0, _net_n0, _net_x1, _net_n1, _net_flagy)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    y = list_from_net(_net_y, DT_REAL)

    # return
    return y

def rbfgridcalc3v(*functionargs):
    # unpack inputs
    s, x0, n0, x1, n1, x2, n2 = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_x0 = net_from_list(x0, DT_REAL, "ALGLIB: parameter 'x0' of 'xalglib.rbfgridcalc3v' must be real vector")
    _net_n0 = n0
    _net_x1 = net_from_list(x1, DT_REAL, "ALGLIB: parameter 'x1' of 'xalglib.rbfgridcalc3v' must be real vector")
    _net_n1 = n1
    _net_x2 = net_from_list(x2, DT_REAL, "ALGLIB: parameter 'x2' of 'xalglib.rbfgridcalc3v' must be real vector")
    _net_n2 = n2
    try:

        # call function
        _net_y = _net_alglib.rbfgridcalc3v(_net_s, _net_x0, _net_n0, _net_x1, _net_n1, _net_x2, _net_n2)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    y = list_from_net(_net_y, DT_REAL)

    # return
    return y

def smp_rbfgridcalc3v(*functionargs):
    # unpack inputs
    s, x0, n0, x1, n1, x2, n2 = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_x0 = net_from_list(x0, DT_REAL, "ALGLIB: parameter 'x0' of 'xalglib.smp_rbfgridcalc3v' must be real vector")
    _net_n0 = n0
    _net_x1 = net_from_list(x1, DT_REAL, "ALGLIB: parameter 'x1' of 'xalglib.smp_rbfgridcalc3v' must be real vector")
    _net_n1 = n1
    _net_x2 = net_from_list(x2, DT_REAL, "ALGLIB: parameter 'x2' of 'xalglib.smp_rbfgridcalc3v' must be real vector")
    _net_n2 = n2
    try:

        # call function
        _net_y = _net_alglib.smp_rbfgridcalc3v(_net_s, _net_x0, _net_n0, _net_x1, _net_n1, _net_x2, _net_n2)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    y = list_from_net(_net_y, DT_REAL)

    # return
    return y

def rbfgridcalc3vsubset(*functionargs):
    # unpack inputs
    s, x0, n0, x1, n1, x2, n2, flagy = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_x0 = net_from_list(x0, DT_REAL, "ALGLIB: parameter 'x0' of 'xalglib.rbfgridcalc3vsubset' must be real vector")
    _net_n0 = n0
    _net_x1 = net_from_list(x1, DT_REAL, "ALGLIB: parameter 'x1' of 'xalglib.rbfgridcalc3vsubset' must be real vector")
    _net_n1 = n1
    _net_x2 = net_from_list(x2, DT_REAL, "ALGLIB: parameter 'x2' of 'xalglib.rbfgridcalc3vsubset' must be real vector")
    _net_n2 = n2
    _net_flagy = net_from_list(flagy, DT_BOOL, "ALGLIB: parameter 'flagy' of 'xalglib.rbfgridcalc3vsubset' must be bool vector")
    try:

        # call function
        _net_y = _net_alglib.rbfgridcalc3vsubset(_net_s, _net_x0, _net_n0, _net_x1, _net_n1, _net_x2, _net_n2, _net_flagy)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    y = list_from_net(_net_y, DT_REAL)

    # return
    return y

def smp_rbfgridcalc3vsubset(*functionargs):
    # unpack inputs
    s, x0, n0, x1, n1, x2, n2, flagy = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    _net_x0 = net_from_list(x0, DT_REAL, "ALGLIB: parameter 'x0' of 'xalglib.smp_rbfgridcalc3vsubset' must be real vector")
    _net_n0 = n0
    _net_x1 = net_from_list(x1, DT_REAL, "ALGLIB: parameter 'x1' of 'xalglib.smp_rbfgridcalc3vsubset' must be real vector")
    _net_n1 = n1
    _net_x2 = net_from_list(x2, DT_REAL, "ALGLIB: parameter 'x2' of 'xalglib.smp_rbfgridcalc3vsubset' must be real vector")
    _net_n2 = n2
    _net_flagy = net_from_list(flagy, DT_BOOL, "ALGLIB: parameter 'flagy' of 'xalglib.smp_rbfgridcalc3vsubset' must be bool vector")
    try:

        # call function
        _net_y = _net_alglib.smp_rbfgridcalc3vsubset(_net_s, _net_x0, _net_n0, _net_x1, _net_n1, _net_x2, _net_n2, _net_flagy)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    y = list_from_net(_net_y, DT_REAL)

    # return
    return y

def rbfunpack(*functionargs):
    # unpack inputs
    s,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    try:

        # call function
        _net_nx, _net_ny, _net_xwr, _net_nc, _net_v, _net_modelversion = _net_alglib.rbfunpack(_net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    nx = _net_nx
    ny = _net_ny
    xwr = listlist_from_net(_net_xwr, DT_REAL)
    nc = _net_nc
    v = listlist_from_net(_net_v, DT_REAL)
    modelversion = _net_modelversion

    # return
    return (nx, ny, xwr, nc, v, modelversion)

def rbfgetmodelversion(*functionargs):
    # unpack inputs
    s,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_s = s.ptr
    try:

        # call function
        _net_result = _net_alglib.rbfgetmodelversion(_net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def ellipticintegralk(*functionargs):
    # unpack inputs
    m,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    try:

        # call function
        _net_result = _net_alglib.ellipticintegralk(_net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def ellipticintegralkhighprecision(*functionargs):
    # unpack inputs
    m1,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m1 = m1
    try:

        # call function
        _net_result = _net_alglib.ellipticintegralkhighprecision(_net_m1)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def incompleteellipticintegralk(*functionargs):
    # unpack inputs
    phi, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_phi = phi
    _net_m = m
    try:

        # call function
        _net_result = _net_alglib.incompleteellipticintegralk(_net_phi, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def ellipticintegrale(*functionargs):
    # unpack inputs
    m,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_m = m
    try:

        # call function
        _net_result = _net_alglib.ellipticintegrale(_net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def incompleteellipticintegrale(*functionargs):
    # unpack inputs
    phi, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_phi = phi
    _net_m = m
    try:

        # call function
        _net_result = _net_alglib.incompleteellipticintegrale(_net_phi, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def hermitecalculate(*functionargs):
    # unpack inputs
    n, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.hermitecalculate(_net_n, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def hermitesum(*functionargs):
    # unpack inputs
    c, n, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_c = net_from_list(c, DT_REAL, "ALGLIB: parameter 'c' of 'xalglib.hermitesum' must be real vector")
    _net_n = n
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.hermitesum(_net_c, _net_n, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def hermitecoefficients(*functionargs):
    # unpack inputs
    n,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    try:

        # call function
        _net_c = _net_alglib.hermitecoefficients(_net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = list_from_net(_net_c, DT_REAL)

    # return
    return c

def dawsonintegral(*functionargs):
    # unpack inputs
    x,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.dawsonintegral(_net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def sinecosineintegrals(*functionargs):
    # unpack inputs
    x,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = x
    try:

        # call function
        _net_si, _net_ci = _net_alglib.sinecosineintegrals(_net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    si = _net_si
    ci = _net_ci

    # return
    return (si, ci)

def hyperbolicsinecosineintegrals(*functionargs):
    # unpack inputs
    x,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = x
    try:

        # call function
        _net_shi, _net_chi = _net_alglib.hyperbolicsinecosineintegrals(_net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    shi = _net_shi
    chi = _net_chi

    # return
    return (shi, chi)

def poissondistribution(*functionargs):
    # unpack inputs
    k, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_k = k
    _net_m = m
    try:

        # call function
        _net_result = _net_alglib.poissondistribution(_net_k, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def poissoncdistribution(*functionargs):
    # unpack inputs
    k, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_k = k
    _net_m = m
    try:

        # call function
        _net_result = _net_alglib.poissoncdistribution(_net_k, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def invpoissondistribution(*functionargs):
    # unpack inputs
    k, y = functionargs
    friendly_form = False

    # convert to .NET types
    _net_k = k
    _net_y = y
    try:

        # call function
        _net_result = _net_alglib.invpoissondistribution(_net_k, _net_y)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def besselj0(*functionargs):
    # unpack inputs
    x,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.besselj0(_net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def besselj1(*functionargs):
    # unpack inputs
    x,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.besselj1(_net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def besseljn(*functionargs):
    # unpack inputs
    n, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.besseljn(_net_n, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def bessely0(*functionargs):
    # unpack inputs
    x,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.bessely0(_net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def bessely1(*functionargs):
    # unpack inputs
    x,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.bessely1(_net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def besselyn(*functionargs):
    # unpack inputs
    n, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.besselyn(_net_n, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def besseli0(*functionargs):
    # unpack inputs
    x,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.besseli0(_net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def besseli1(*functionargs):
    # unpack inputs
    x,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.besseli1(_net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def besselk0(*functionargs):
    # unpack inputs
    x,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.besselk0(_net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def besselk1(*functionargs):
    # unpack inputs
    x,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.besselk1(_net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def besselkn(*functionargs):
    # unpack inputs
    nn, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_nn = nn
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.besselkn(_net_nn, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def incompletebeta(*functionargs):
    # unpack inputs
    a, b, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = a
    _net_b = b
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.incompletebeta(_net_a, _net_b, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def invincompletebeta(*functionargs):
    # unpack inputs
    a, b, y = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = a
    _net_b = b
    _net_y = y
    try:

        # call function
        _net_result = _net_alglib.invincompletebeta(_net_a, _net_b, _net_y)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def fdistribution(*functionargs):
    # unpack inputs
    a, b, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = a
    _net_b = b
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.fdistribution(_net_a, _net_b, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def fcdistribution(*functionargs):
    # unpack inputs
    a, b, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = a
    _net_b = b
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.fcdistribution(_net_a, _net_b, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def invfdistribution(*functionargs):
    # unpack inputs
    a, b, y = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = a
    _net_b = b
    _net_y = y
    try:

        # call function
        _net_result = _net_alglib.invfdistribution(_net_a, _net_b, _net_y)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def fresnelintegral(*functionargs):
    # unpack inputs
    x, c, s = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = x
    _net_c = c
    _net_s = s
    try:

        # call function
        _net_c, _net_s = _net_alglib.fresnelintegral(_net_x, _net_c, _net_s)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = _net_c
    s = _net_s

    # return
    return (c, s)

def jacobianellipticfunctions(*functionargs):
    # unpack inputs
    u, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_u = u
    _net_m = m
    try:

        # call function
        _net_sn, _net_cn, _net_dn, _net_ph = _net_alglib.jacobianellipticfunctions(_net_u, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    sn = _net_sn
    cn = _net_cn
    dn = _net_dn
    ph = _net_ph

    # return
    return (sn, cn, dn, ph)

def psi(*functionargs):
    # unpack inputs
    x,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.psi(_net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def exponentialintegralei(*functionargs):
    # unpack inputs
    x,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.exponentialintegralei(_net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def exponentialintegralen(*functionargs):
    # unpack inputs
    x, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = x
    _net_n = n
    try:

        # call function
        _net_result = _net_alglib.exponentialintegralen(_net_x, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def laguerrecalculate(*functionargs):
    # unpack inputs
    n, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.laguerrecalculate(_net_n, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def laguerresum(*functionargs):
    # unpack inputs
    c, n, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_c = net_from_list(c, DT_REAL, "ALGLIB: parameter 'c' of 'xalglib.laguerresum' must be real vector")
    _net_n = n
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.laguerresum(_net_c, _net_n, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def laguerrecoefficients(*functionargs):
    # unpack inputs
    n,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    try:

        # call function
        _net_c = _net_alglib.laguerrecoefficients(_net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = list_from_net(_net_c, DT_REAL)

    # return
    return c

def chisquaredistribution(*functionargs):
    # unpack inputs
    v, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_v = v
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.chisquaredistribution(_net_v, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def chisquarecdistribution(*functionargs):
    # unpack inputs
    v, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_v = v
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.chisquarecdistribution(_net_v, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def invchisquaredistribution(*functionargs):
    # unpack inputs
    v, y = functionargs
    friendly_form = False

    # convert to .NET types
    _net_v = v
    _net_y = y
    try:

        # call function
        _net_result = _net_alglib.invchisquaredistribution(_net_v, _net_y)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def legendrecalculate(*functionargs):
    # unpack inputs
    n, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.legendrecalculate(_net_n, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def legendresum(*functionargs):
    # unpack inputs
    c, n, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_c = net_from_list(c, DT_REAL, "ALGLIB: parameter 'c' of 'xalglib.legendresum' must be real vector")
    _net_n = n
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.legendresum(_net_c, _net_n, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def legendrecoefficients(*functionargs):
    # unpack inputs
    n,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    try:

        # call function
        _net_c = _net_alglib.legendrecoefficients(_net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = list_from_net(_net_c, DT_REAL)

    # return
    return c

def beta(*functionargs):
    # unpack inputs
    a, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = a
    _net_b = b
    try:

        # call function
        _net_result = _net_alglib.beta(_net_a, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def chebyshevcalculate(*functionargs):
    # unpack inputs
    r, n, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_r = r
    _net_n = n
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.chebyshevcalculate(_net_r, _net_n, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def chebyshevsum(*functionargs):
    # unpack inputs
    c, r, n, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_c = net_from_list(c, DT_REAL, "ALGLIB: parameter 'c' of 'xalglib.chebyshevsum' must be real vector")
    _net_r = r
    _net_n = n
    _net_x = x
    try:

        # call function
        _net_result = _net_alglib.chebyshevsum(_net_c, _net_r, _net_n, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def chebyshevcoefficients(*functionargs):
    # unpack inputs
    n,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    try:

        # call function
        _net_c = _net_alglib.chebyshevcoefficients(_net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    c = list_from_net(_net_c, DT_REAL)

    # return
    return c

def fromchebyshev(*functionargs):
    # unpack inputs
    a, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_list(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.fromchebyshev' must be real vector")
    _net_n = n
    try:

        # call function
        _net_b = _net_alglib.fromchebyshev(_net_a, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    b = list_from_net(_net_b, DT_REAL)

    # return
    return b

def studenttdistribution(*functionargs):
    # unpack inputs
    k, t = functionargs
    friendly_form = False

    # convert to .NET types
    _net_k = k
    _net_t = t
    try:

        # call function
        _net_result = _net_alglib.studenttdistribution(_net_k, _net_t)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def invstudenttdistribution(*functionargs):
    # unpack inputs
    k, p = functionargs
    friendly_form = False

    # convert to .NET types
    _net_k = k
    _net_p = p
    try:

        # call function
        _net_result = _net_alglib.invstudenttdistribution(_net_k, _net_p)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def binomialdistribution(*functionargs):
    # unpack inputs
    k, n, p = functionargs
    friendly_form = False

    # convert to .NET types
    _net_k = k
    _net_n = n
    _net_p = p
    try:

        # call function
        _net_result = _net_alglib.binomialdistribution(_net_k, _net_n, _net_p)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def binomialcdistribution(*functionargs):
    # unpack inputs
    k, n, p = functionargs
    friendly_form = False

    # convert to .NET types
    _net_k = k
    _net_n = n
    _net_p = p
    try:

        # call function
        _net_result = _net_alglib.binomialcdistribution(_net_k, _net_n, _net_p)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def invbinomialdistribution(*functionargs):
    # unpack inputs
    k, n, y = functionargs
    friendly_form = False

    # convert to .NET types
    _net_k = k
    _net_n = n
    _net_y = y
    try:

        # call function
        _net_result = _net_alglib.invbinomialdistribution(_net_k, _net_n, _net_y)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def airy(*functionargs):
    # unpack inputs
    x,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = x
    try:

        # call function
        _net_ai, _net_aip, _net_bi, _net_bip = _net_alglib.airy(_net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    ai = _net_ai
    aip = _net_aip
    bi = _net_bi
    bip = _net_bip

    # return
    return (ai, aip, bi, bip)

def wilcoxonsignedranktest(*functionargs):
    # unpack inputs
    x, n, e = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.wilcoxonsignedranktest' must be real vector")
    _net_n = n
    _net_e = e
    try:

        # call function
        _net_bothtails, _net_lefttail, _net_righttail = _net_alglib.wilcoxonsignedranktest(_net_x, _net_n, _net_e)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    bothtails = _net_bothtails
    lefttail = _net_lefttail
    righttail = _net_righttail

    # return
    return (bothtails, lefttail, righttail)

def onesamplesigntest(*functionargs):
    # unpack inputs
    x, n, median = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.onesamplesigntest' must be real vector")
    _net_n = n
    _net_median = median
    try:

        # call function
        _net_bothtails, _net_lefttail, _net_righttail = _net_alglib.onesamplesigntest(_net_x, _net_n, _net_median)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    bothtails = _net_bothtails
    lefttail = _net_lefttail
    righttail = _net_righttail

    # return
    return (bothtails, lefttail, righttail)

def pearsoncorrelationsignificance(*functionargs):
    # unpack inputs
    r, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_r = r
    _net_n = n
    try:

        # call function
        _net_bothtails, _net_lefttail, _net_righttail = _net_alglib.pearsoncorrelationsignificance(_net_r, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    bothtails = _net_bothtails
    lefttail = _net_lefttail
    righttail = _net_righttail

    # return
    return (bothtails, lefttail, righttail)

def spearmanrankcorrelationsignificance(*functionargs):
    # unpack inputs
    r, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_r = r
    _net_n = n
    try:

        # call function
        _net_bothtails, _net_lefttail, _net_righttail = _net_alglib.spearmanrankcorrelationsignificance(_net_r, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    bothtails = _net_bothtails
    lefttail = _net_lefttail
    righttail = _net_righttail

    # return
    return (bothtails, lefttail, righttail)

def studentttest1(*functionargs):
    # unpack inputs
    x, n, mean = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.studentttest1' must be real vector")
    _net_n = n
    _net_mean = mean
    try:

        # call function
        _net_bothtails, _net_lefttail, _net_righttail = _net_alglib.studentttest1(_net_x, _net_n, _net_mean)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    bothtails = _net_bothtails
    lefttail = _net_lefttail
    righttail = _net_righttail

    # return
    return (bothtails, lefttail, righttail)

def studentttest2(*functionargs):
    # unpack inputs
    x, n, y, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.studentttest2' must be real vector")
    _net_n = n
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.studentttest2' must be real vector")
    _net_m = m
    try:

        # call function
        _net_bothtails, _net_lefttail, _net_righttail = _net_alglib.studentttest2(_net_x, _net_n, _net_y, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    bothtails = _net_bothtails
    lefttail = _net_lefttail
    righttail = _net_righttail

    # return
    return (bothtails, lefttail, righttail)

def unequalvariancettest(*functionargs):
    # unpack inputs
    x, n, y, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.unequalvariancettest' must be real vector")
    _net_n = n
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.unequalvariancettest' must be real vector")
    _net_m = m
    try:

        # call function
        _net_bothtails, _net_lefttail, _net_righttail = _net_alglib.unequalvariancettest(_net_x, _net_n, _net_y, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    bothtails = _net_bothtails
    lefttail = _net_lefttail
    righttail = _net_righttail

    # return
    return (bothtails, lefttail, righttail)

def mannwhitneyutest(*functionargs):
    # unpack inputs
    x, n, y, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.mannwhitneyutest' must be real vector")
    _net_n = n
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.mannwhitneyutest' must be real vector")
    _net_m = m
    try:

        # call function
        _net_bothtails, _net_lefttail, _net_righttail = _net_alglib.mannwhitneyutest(_net_x, _net_n, _net_y, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    bothtails = _net_bothtails
    lefttail = _net_lefttail
    righttail = _net_righttail

    # return
    return (bothtails, lefttail, righttail)

def jarqueberatest(*functionargs):
    # unpack inputs
    x, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.jarqueberatest' must be real vector")
    _net_n = n
    try:

        # call function
        _net_p = _net_alglib.jarqueberatest(_net_x, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    p = _net_p

    # return
    return p

def ftest(*functionargs):
    # unpack inputs
    x, n, y, m = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.ftest' must be real vector")
    _net_n = n
    _net_y = net_from_list(y, DT_REAL, "ALGLIB: parameter 'y' of 'xalglib.ftest' must be real vector")
    _net_m = m
    try:

        # call function
        _net_bothtails, _net_lefttail, _net_righttail = _net_alglib.ftest(_net_x, _net_n, _net_y, _net_m)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    bothtails = _net_bothtails
    lefttail = _net_lefttail
    righttail = _net_righttail

    # return
    return (bothtails, lefttail, righttail)

def onesamplevariancetest(*functionargs):
    # unpack inputs
    x, n, variance = functionargs
    friendly_form = False

    # convert to .NET types
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.onesamplevariancetest' must be real vector")
    _net_n = n
    _net_variance = variance
    try:

        # call function
        _net_bothtails, _net_lefttail, _net_righttail = _net_alglib.onesamplevariancetest(_net_x, _net_n, _net_variance)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    bothtails = _net_bothtails
    lefttail = _net_lefttail
    righttail = _net_righttail

    # return
    return (bothtails, lefttail, righttail)

def rmatrixschur(*functionargs):
    # unpack inputs
    a, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixschur' must be real matrix")
    _net_n = n
    try:

        # call function
        _net_result, _net_a, _net_s = _net_alglib.rmatrixschur(_net_a, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result
    a = listlist_from_net(_net_a, DT_REAL)
    s = listlist_from_net(_net_s, DT_REAL)

    # return
    return (result, a, s)

def smatrixgevd(*functionargs):
    # unpack inputs
    a, n, isuppera, b, isupperb, zneeded, problemtype = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smatrixgevd' must be real matrix")
    _net_n = n
    _net_isuppera = isuppera
    _net_b = net_from_listlist(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.smatrixgevd' must be real matrix")
    _net_isupperb = isupperb
    _net_zneeded = zneeded
    _net_problemtype = problemtype
    try:

        # call function
        _net_result, _net_d, _net_z = _net_alglib.smatrixgevd(_net_a, _net_n, _net_isuppera, _net_b, _net_isupperb, _net_zneeded, _net_problemtype)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result
    d = list_from_net(_net_d, DT_REAL)
    z = listlist_from_net(_net_z, DT_REAL)

    # return
    return (result, d, z)

def smatrixgevdreduce(*functionargs):
    # unpack inputs
    a, n, isuppera, b, isupperb, problemtype = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.smatrixgevdreduce' must be real matrix")
    _net_n = n
    _net_isuppera = isuppera
    _net_b = net_from_listlist(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.smatrixgevdreduce' must be real matrix")
    _net_isupperb = isupperb
    _net_problemtype = problemtype
    try:

        # call function
        _net_result, _net_a, _net_r, _net_isupperr = _net_alglib.smatrixgevdreduce(_net_a, _net_n, _net_isuppera, _net_b, _net_isupperb, _net_problemtype)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result
    a = listlist_from_net(_net_a, DT_REAL)
    r = listlist_from_net(_net_r, DT_REAL)
    isupperr = _net_isupperr

    # return
    return (result, a, r, isupperr)

def rmatrixinvupdatesimple(*functionargs):
    # unpack inputs
    inva, n, updrow, updcolumn, updval = functionargs
    friendly_form = False

    # convert to .NET types
    _net_inva = net_from_listlist(inva, DT_REAL, "ALGLIB: parameter 'inva' of 'xalglib.rmatrixinvupdatesimple' must be real matrix")
    _net_n = n
    _net_updrow = updrow
    _net_updcolumn = updcolumn
    _net_updval = updval
    try:

        # call function
        _net_inva = _net_alglib.rmatrixinvupdatesimple(_net_inva, _net_n, _net_updrow, _net_updcolumn, _net_updval)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    inva = listlist_from_net(_net_inva, DT_REAL)

    # return
    return inva

def rmatrixinvupdaterow(*functionargs):
    # unpack inputs
    inva, n, updrow, v = functionargs
    friendly_form = False

    # convert to .NET types
    _net_inva = net_from_listlist(inva, DT_REAL, "ALGLIB: parameter 'inva' of 'xalglib.rmatrixinvupdaterow' must be real matrix")
    _net_n = n
    _net_updrow = updrow
    _net_v = net_from_list(v, DT_REAL, "ALGLIB: parameter 'v' of 'xalglib.rmatrixinvupdaterow' must be real vector")
    try:

        # call function
        _net_inva = _net_alglib.rmatrixinvupdaterow(_net_inva, _net_n, _net_updrow, _net_v)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    inva = listlist_from_net(_net_inva, DT_REAL)

    # return
    return inva

def rmatrixinvupdatecolumn(*functionargs):
    # unpack inputs
    inva, n, updcolumn, u = functionargs
    friendly_form = False

    # convert to .NET types
    _net_inva = net_from_listlist(inva, DT_REAL, "ALGLIB: parameter 'inva' of 'xalglib.rmatrixinvupdatecolumn' must be real matrix")
    _net_n = n
    _net_updcolumn = updcolumn
    _net_u = net_from_list(u, DT_REAL, "ALGLIB: parameter 'u' of 'xalglib.rmatrixinvupdatecolumn' must be real vector")
    try:

        # call function
        _net_inva = _net_alglib.rmatrixinvupdatecolumn(_net_inva, _net_n, _net_updcolumn, _net_u)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    inva = listlist_from_net(_net_inva, DT_REAL)

    # return
    return inva

def rmatrixinvupdateuv(*functionargs):
    # unpack inputs
    inva, n, u, v = functionargs
    friendly_form = False

    # convert to .NET types
    _net_inva = net_from_listlist(inva, DT_REAL, "ALGLIB: parameter 'inva' of 'xalglib.rmatrixinvupdateuv' must be real matrix")
    _net_n = n
    _net_u = net_from_list(u, DT_REAL, "ALGLIB: parameter 'u' of 'xalglib.rmatrixinvupdateuv' must be real vector")
    _net_v = net_from_list(v, DT_REAL, "ALGLIB: parameter 'v' of 'xalglib.rmatrixinvupdateuv' must be real vector")
    try:

        # call function
        _net_inva = _net_alglib.rmatrixinvupdateuv(_net_inva, _net_n, _net_u, _net_v)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    inva = listlist_from_net(_net_inva, DT_REAL)

    # return
    return inva

def rmatrixludet(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        a, pivots, n = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        a, pivots = functionargs
        n = check_equality_and_get([safe_rows("'rmatrixludet': incorrect parameters",a), safe_cols("'rmatrixludet': incorrect parameters",a), safe_len("'rmatrixludet': incorrect parameters",pivots)],"Error while calling 'rmatrixludet': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'rmatrixludet': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixludet' must be real matrix")
    _net_pivots = net_from_list(pivots, DT_INT, "ALGLIB: parameter 'pivots' of 'xalglib.rmatrixludet' must be int vector")
    _net_n = n
    try:

        # call function
        _net_result = _net_alglib.rmatrixludet(_net_a, _net_pivots, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def rmatrixdet(*functionargs):
    # unpack inputs
    if len(functionargs)==2:
        # full-form call
        a, n = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        a,  = functionargs
        n = check_equality_and_get([safe_rows("'rmatrixdet': incorrect parameters",a), safe_cols("'rmatrixdet': incorrect parameters",a)],"Error while calling 'rmatrixdet': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'rmatrixdet': function must have 2 or 1 parameters")

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.rmatrixdet' must be real matrix")
    _net_n = n
    try:

        # call function
        _net_result = _net_alglib.rmatrixdet(_net_a, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def cmatrixludet(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        a, pivots, n = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        a, pivots = functionargs
        n = check_equality_and_get([safe_rows("'cmatrixludet': incorrect parameters",a), safe_cols("'cmatrixludet': incorrect parameters",a), safe_len("'cmatrixludet': incorrect parameters",pivots)],"Error while calling 'cmatrixludet': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'cmatrixludet': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.cmatrixludet' must be complex matrix")
    _net_pivots = net_from_list(pivots, DT_INT, "ALGLIB: parameter 'pivots' of 'xalglib.cmatrixludet' must be int vector")
    _net_n = n
    try:

        # call function
        _net_result = _net_alglib.cmatrixludet(_net_a, _net_pivots, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = complex(_net_result.x,_net_result.y)

    # return
    return result

def cmatrixdet(*functionargs):
    # unpack inputs
    if len(functionargs)==2:
        # full-form call
        a, n = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        a,  = functionargs
        n = check_equality_and_get([safe_rows("'cmatrixdet': incorrect parameters",a), safe_cols("'cmatrixdet': incorrect parameters",a)],"Error while calling 'cmatrixdet': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'cmatrixdet': function must have 2 or 1 parameters")

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_COMPLEX, "ALGLIB: parameter 'a' of 'xalglib.cmatrixdet' must be complex matrix")
    _net_n = n
    try:

        # call function
        _net_result = _net_alglib.cmatrixdet(_net_a, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = complex(_net_result.x,_net_result.y)

    # return
    return result

def spdmatrixcholeskydet(*functionargs):
    # unpack inputs
    if len(functionargs)==2:
        # full-form call
        a, n = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        a,  = functionargs
        n = check_equality_and_get([safe_rows("'spdmatrixcholeskydet': incorrect parameters",a), safe_cols("'spdmatrixcholeskydet': incorrect parameters",a)],"Error while calling 'spdmatrixcholeskydet': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'spdmatrixcholeskydet': function must have 2 or 1 parameters")

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.spdmatrixcholeskydet' must be real matrix")
    _net_n = n
    try:

        # call function
        _net_result = _net_alglib.spdmatrixcholeskydet(_net_a, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result

def spdmatrixdet(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        a, n, isupper = functionargs
        friendly_form = False
    elif len(functionargs)==1:
        # short-form call
        a,  = functionargs
        n = check_equality_and_get([safe_rows("'spdmatrixdet': incorrect parameters",a), safe_cols("'spdmatrixdet': incorrect parameters",a)],"Error while calling 'spdmatrixdet': looks like one of arguments has wrong size")
        isupper = check_equality_and_get([False],"Error while calling 'spdmatrixdet': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'spdmatrixdet': function must have 3 or 1 parameters")

    # convert to .NET types
    _net_a = net_from_listlist(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.spdmatrixdet' must be real matrix")
    if friendly_form and (not _net_alglib.ap.issymmetric(_net_a)):
        raise ValueError("ALGLIB: parameter 'a' of 'xalglib.spdmatrixdet' must be symmetric matrix")
    _net_n = n
    _net_isupper = isupper
    try:

        # call function
        _net_result = _net_alglib.spdmatrixdet(_net_a, _net_n, _net_isupper)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    result = _net_result

    # return
    return result



class polynomialsolverreport(object):
    def __init__(self):
        self.maxerr = 0


def net_from_polynomialsolverreport(x,v):
    x.maxerr = float(v.maxerr)
    return




def polynomialsolverreport_from_net(x):
    r = polynomialsolverreport()
    r.maxerr = x.maxerr
    return r


def polynomialsolve(*functionargs):
    # unpack inputs
    a, n = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = net_from_list(a, DT_REAL, "ALGLIB: parameter 'a' of 'xalglib.polynomialsolve' must be real vector")
    _net_n = n
    try:

        # call function
        _net_x, _net_rep = _net_alglib.polynomialsolve(_net_a, _net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = list_from_net(_net_x, DT_COMPLEX)
    rep = polynomialsolverreport_from_net(_net_rep)

    # return
    return (x, rep)



class nleqstate(object):
    def __init__(self,ptr):
        self.ptr = ptr


class nleqreport(object):
    def __init__(self):
        self.iterationscount = 0
        self.nfunc = 0
        self.njac = 0
        self.terminationtype = 0


def net_from_nleqreport(x,v):
    x.iterationscount = int(v.iterationscount)
    x.nfunc = int(v.nfunc)
    x.njac = int(v.njac)
    x.terminationtype = int(v.terminationtype)
    return




def nleqreport_from_net(x):
    r = nleqreport()
    r.iterationscount = x.iterationscount
    r.nfunc = x.nfunc
    r.njac = x.njac
    r.terminationtype = x.terminationtype
    return r


def nleqcreatelm(*functionargs):
    # unpack inputs
    if len(functionargs)==3:
        # full-form call
        n, m, x = functionargs
        friendly_form = False
    elif len(functionargs)==2:
        # short-form call
        m, x = functionargs
        n = check_equality_and_get([safe_len("'nleqcreatelm': incorrect parameters",x)],"Error while calling 'nleqcreatelm': looks like one of arguments has wrong size")
        friendly_form = True
    else:
        raise RuntimeError("Error while calling 'nleqcreatelm': function must have 3 or 2 parameters")

    # convert to .NET types
    _net_n = n
    _net_m = m
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.nleqcreatelm' must be real vector")
    try:

        # call function
        _net_state = _net_alglib.nleqcreatelm(_net_n, _net_m, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = nleqstate(_net_state)

    # return
    return state

def nleqsetcond(*functionargs):
    # unpack inputs
    state, epsf, maxits = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_epsf = epsf
    _net_maxits = maxits
    try:

        # call function
        _net_alglib.nleqsetcond(_net_state, _net_epsf, _net_maxits)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def nleqsetxrep(*functionargs):
    # unpack inputs
    state, needxrep = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_needxrep = needxrep
    try:

        # call function
        _net_alglib.nleqsetxrep(_net_state, _net_needxrep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def nleqsetstpmax(*functionargs):
    # unpack inputs
    state, stpmax = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_stpmax = stpmax
    try:

        # call function
        _net_alglib.nleqsetstpmax(_net_state, _net_stpmax)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return



def nleqsolve_fj(state, func, jac, rep = None, param = None):
    _net_x  = state.ptr.x
    _py_x = create_real_vector(_net_x.GetLength(0))
    _net_fi  = state.ptr.fi
    _py_fi = create_real_vector(_net_fi.GetLength(0))
    _net_j  = state.ptr.j
    _py_j = create_real_matrix(_net_j.GetLength(0),_net_j.GetLength(1))
    while True:
        try:
            result = _net_alglib.nleqiteration(state.ptr)
        except _net_alglib.alglibexception as e:
            raise RuntimeError(e.msg)
        if not result:
            break
        if state.ptr.needf:
            copy_net_to_list(_net_x, _py_x, DT_REAL)

            fvalue = func(_py_x, param)
            state.ptr.f = fvalue
            continue
        if state.ptr.needfij:
            copy_net_to_list(_net_x, _py_x, DT_REAL)

            jac(_py_x, _py_fi, _py_j, param)
            copy_list_to_net(_py_fi, _net_fi, DT_REAL)
            copy_listlist_to_net(_py_j, _net_j, DT_REAL)
            continue
        if state.ptr.xupdated:
            if not (rep is None):
                copy_net_to_list(_net_x, _py_x, DT_REAL)
                rep(_py_x, state.ptr.f, param)
            continue
        raise RuntimeError("ALGLIB: error in 'nleqsolve' (some derivatives were not provided?)")
    return


def nleqresults(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_x, _net_rep = _net_alglib.nleqresults(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = list_from_net(_net_x, DT_REAL)
    rep = nleqreport_from_net(_net_rep)

    # return
    return (x, rep)

def nleqresultsbuf(*functionargs):
    # unpack inputs
    state, x, rep = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.nleqresultsbuf' must be real vector")
    _net_rep = _net_alglib.nleqreport()
    net_from_nleqreport(_net_rep, rep)
    try:

        # call function
        _net_x, _net_rep = _net_alglib.nleqresultsbuf(_net_state, _net_x, _net_rep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = list_from_net(_net_x, DT_REAL)
    rep = nleqreport_from_net(_net_rep)

    # return
    return (x, rep)

def nleqrestartfrom(*functionargs):
    # unpack inputs
    state, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.nleqrestartfrom' must be real vector")
    try:

        # call function
        _net_alglib.nleqrestartfrom(_net_state, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return



class sparsesolverreport(object):
    def __init__(self):
        self.terminationtype = 0


def net_from_sparsesolverreport(x,v):
    x.terminationtype = int(v.terminationtype)
    return




def sparsesolverreport_from_net(x):
    r = sparsesolverreport()
    r.terminationtype = x.terminationtype
    return r


def sparsesolvesks(*functionargs):
    # unpack inputs
    a, n, isupper, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = a.ptr
    _net_n = n
    _net_isupper = isupper
    _net_b = net_from_list(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.sparsesolvesks' must be real vector")
    try:

        # call function
        _net_rep, _net_x = _net_alglib.sparsesolvesks(_net_a, _net_n, _net_isupper, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    rep = sparsesolverreport_from_net(_net_rep)
    x = list_from_net(_net_x, DT_REAL)

    # return
    return (rep, x)

def sparsecholeskysolvesks(*functionargs):
    # unpack inputs
    a, n, isupper, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_a = a.ptr
    _net_n = n
    _net_isupper = isupper
    _net_b = net_from_list(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.sparsecholeskysolvesks' must be real vector")
    try:

        # call function
        _net_rep, _net_x = _net_alglib.sparsecholeskysolvesks(_net_a, _net_n, _net_isupper, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    rep = sparsesolverreport_from_net(_net_rep)
    x = list_from_net(_net_x, DT_REAL)

    # return
    return (rep, x)



class lincgstate(object):
    def __init__(self,ptr):
        self.ptr = ptr


class lincgreport(object):
    def __init__(self):
        self.iterationscount = 0
        self.nmv = 0
        self.terminationtype = 0
        self.r2 = 0


def net_from_lincgreport(x,v):
    x.iterationscount = int(v.iterationscount)
    x.nmv = int(v.nmv)
    x.terminationtype = int(v.terminationtype)
    x.r2 = float(v.r2)
    return




def lincgreport_from_net(x):
    r = lincgreport()
    r.iterationscount = x.iterationscount
    r.nmv = x.nmv
    r.terminationtype = x.terminationtype
    r.r2 = x.r2
    return r


def lincgcreate(*functionargs):
    # unpack inputs
    n,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_n = n
    try:

        # call function
        _net_state = _net_alglib.lincgcreate(_net_n)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    state = lincgstate(_net_state)

    # return
    return state

def lincgsetstartingpoint(*functionargs):
    # unpack inputs
    state, x = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_x = net_from_list(x, DT_REAL, "ALGLIB: parameter 'x' of 'xalglib.lincgsetstartingpoint' must be real vector")
    try:

        # call function
        _net_alglib.lincgsetstartingpoint(_net_state, _net_x)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def lincgsetprecunit(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_alglib.lincgsetprecunit(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def lincgsetprecdiag(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_alglib.lincgsetprecdiag(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def lincgsetcond(*functionargs):
    # unpack inputs
    state, epsf, maxits = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_epsf = epsf
    _net_maxits = maxits
    try:

        # call function
        _net_alglib.lincgsetcond(_net_state, _net_epsf, _net_maxits)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def lincgsolvesparse(*functionargs):
    # unpack inputs
    state, a, isupper, b = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_a = a.ptr
    _net_isupper = isupper
    _net_b = net_from_list(b, DT_REAL, "ALGLIB: parameter 'b' of 'xalglib.lincgsolvesparse' must be real vector")
    try:

        # call function
        _net_alglib.lincgsolvesparse(_net_state, _net_a, _net_isupper, _net_b)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def lincgresults(*functionargs):
    # unpack inputs
    state,  = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    try:

        # call function
        _net_x, _net_rep = _net_alglib.lincgresults(_net_state)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types
    x = list_from_net(_net_x, DT_REAL)
    rep = lincgreport_from_net(_net_rep)

    # return
    return (x, rep)

def lincgsetrestartfreq(*functionargs):
    # unpack inputs
    state, srf = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_srf = srf
    try:

        # call function
        _net_alglib.lincgsetrestartfreq(_net_state, _net_srf)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def lincgsetrupdatefreq(*functionargs):
    # unpack inputs
    state, freq = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_freq = freq
    try:

        # call function
        _net_alglib.lincgsetrupdatefreq(_net_state, _net_freq)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

def lincgsetxrep(*functionargs):
    # unpack inputs
    state, needxrep = functionargs
    friendly_form = False

    # convert to .NET types
    _net_state = state.ptr
    _net_needxrep = needxrep
    try:

        # call function
        _net_alglib.lincgsetxrep(_net_state, _net_needxrep)
    except _net_alglib.alglibexception as e:
        raise RuntimeError(e.msg)

    # convert from .NET types

    # return
    return

