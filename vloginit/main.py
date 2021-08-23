#
# Project       : Verilog/System Verilog module template generator
# Author        : Shekhalev Denis (des00), Borshch Vladislav
# Contact       : diod2003@list.ru, borchsh.vn@gmail.com
# Licence       : free for use
#
# Workfile      : main.py
# Description   : generator module itself


'''
Verilog/SystemVerilog modules template generator

Usage:
    vloginit index_file.dat
    vloginit -sv index_file.dat
'''

import string
import sys
from . import vlog

param_dict = {}

inc_list    = []
param_list  = []
lparam_list = []
port_list   = []

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def error(msg):
    string = 'ERROR : ' + msg
    sys.stderr.write(string)
    sys.exit(100)

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def GetSymbol (symbol) :
    '''
    function to check data for validity
    '''
    new_symbol = symbol.strip()
    if len(new_symbol.split(' ')) != 1 :
        s = "wrong symbol \"" + str(new_symbol) + "\""
        error(s)
    return new_symbol

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def AssignNotDeclaratedParameter (width, local):
    if len(width) == 0:
        return
    if width.isdigit():
        return
    if width in param_dict:
        return
    name, value, width, ptype, array, tab = width, '1', '', 'int', '1', 0 # untyped parameter
    if local == 1:
        lparam_list.append ([name, value, width, ptype, array, tab])
    else:
        param_list.append ([name, value, width, ptype, array, tab])
    param_dict[name] = 1

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def ParseFile (filelist):
    '''
    function to parse input file
    %file_name              - module name
    $<name> # <value>       - parameter
    ?<name> # <value>       - localparameter
    @<direction>#<name>#<width>#<ptype> - port
    '''
    mname = 'veriloginit'

    pre_token_param = 0;

    for file_list_item in filelist:
        elem  = file_list_item.strip()
        try:
            token = elem[0]
        except IndexError :
            token = ''
        # module name
        if token == '%' :
            tmp     = elem[1:].split(' ')   # divide by ' ' symbol
            mname   = GetSymbol(tmp[0])
        # include file
        elif token == '`' :
            tmp     = elem[1:].split(' ')   # divide by ' ' symbol
            iname   = GetSymbol(tmp[0])
            inc_list.append(iname)
        # param
        elif token == '$' or token == '?':
            tmp  = elem[1:].split('#')       # divide by '#' symbol
            name = GetSymbol(tmp[0])
            # get value
            try:
                value = tmp[1].strip()
            except IndexError:
                value = '1'
            # cross reference parameter if value is used
            if token == '$':
                AssignNotDeclaratedParameter(value, 0) # parameter
            else:
                AssignNotDeclaratedParameter(value, 1) # localparam
            # get ptype
            try:
                ptype = tmp[2].strip()
            except IndexError:
                ptype = 'int'
            # get width
            try:
                width = tmp[3].strip()
            except IndexError:
                width = '1'
            # get array width
            try:
                array = tmp[4].strip()
            except IndexError:
                array = '1'
            # cross reference parameter if width is used
            if token == '$':
                AssignNotDeclaratedParameter(width, 0) # parameter
            else:
                AssignNotDeclaratedParameter(width, 1) # localparam
            # update list & common dictionary
            if name not in param_dict:
                if token == '$':
                    param_list.append  ([name, value, width, ptype, array, 0])
                else:
                    lparam_list.append ([name, value, width, ptype, array, 0])
                param_dict[name] = 1
                pre_token_param  = 1;
            else:
                error ('parameter ' + name + ' already declarated')
        # port
        elif token == '@':
            tmp = elem[1:].split('#')
            direct = GetSymbol(tmp[0])
            name   = GetSymbol(tmp[1])
            # get width
            try:
                width = tmp[2].strip()
            except IndexError :
                width = '1' # bit default
            # cross reference parameter
            AssignNotDeclaratedParameter(width, 0) # only global parameters
            # get ptype
            try:
                ptype = tmp[3].strip()
            except IndexError:
                ptype = 'L' # logic default
            # get array width
            try:
                array = tmp[4].strip()
            except IndexError:
                array = '1'
            # update list
            port_list.append ([name, direct, width, ptype, array, 0])
            pre_token_param = 0;
        # comment
        elif token == '*':
            if pre_token_param:
                param_list[len(param_list)-1][5] = '*' + elem[1:]
            else:
                port_list[len(port_list)-1][5] = '*' + elem[1:]
        elif token == '/':
            pass
        elif token != '' :
            error('unrecognized token ' + token)

    return mname

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def CreateTemplateV (filename):
    '''
    function to generate module template in pure verilog
    '''
    # read file
    f = open(filename,"r")
    lines = f.readlines()
    f.close()
    # parse file
    mname = ParseFile(lines)
    # prepare parameters
    _param_list     = vlog.ParseParams( param_list)
    _lparam_list    = vlog.ParseParams(lparam_list)
    _port_list      = vlog.ParsePorts ( port_list )
    # generate inlclude files
    header_info     = vlog.PrintIncludeFiles(inc_list)
    # generate module
    context  = vlog.PrintModuleInstanceCode(mname, _param_list, _port_list);
    context += vlog.PrintModuleDeclarationCode(mname, _param_list, _lparam_list, _port_list, False);
    # addittion fields
    args = {}
    args['header_info'] = header_info
    args['inst_info']   = ''
    args['signal']      = ''
    args['process']     = ''
    #
    context = context % args
    # write to file
    filename = mname + '.v'
    f = open(filename, "w")
    f.writelines(context.expandtabs(2))
    f.close()

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def CreateTemplateSV (filename):
    '''
    function to generate module template in system verilog
    '''
    # read file
    f = open(filename,"r")
    lines = f.readlines()
    f.close()
    # parse file
    mname = ParseFile(lines)
    # prepare parameters
    _param_list     = vlog.ParseParams( param_list)
    _lparam_list    = vlog.ParseParams(lparam_list)
    _port_list      = vlog.ParsePorts ( port_list )
    # generate inlclude files
    header_info     = vlog.PrintIncludeFiles(inc_list)
    # generate module
    context  = vlog.PrintModuleInstanceCode(mname, _param_list, _port_list);
    context += vlog.PrintModuleDeclarationCode(mname, _param_list, _lparam_list, _port_list, True);
    # addittion fields
    args = {}
    args['header_info'] = header_info
    args['inst_info']   = ''
    args['signal']      = ''
    args['process']     = ''
    #
    context = context % args
    # write to file
    filename = mname + '.sv'
    f = open(filename, "w")
    f.writelines(context.expandtabs(2))
    f.close()

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def vloginit(args):
    if len(args) != 1 and len(args) != 2 :
        print(__doc__)
        sys.exit(100)
    elif len(args) == 1 and sys.argv[1] == '-sv' :
        print(__doc__)
        sys.exit(100)
    elif len(args) == 2 and sys.argv[1] != '-sv' :
        print(__doc__)
        sys.exit(100)
    else:
        try:
            if len(args) == 1:
                CreateTemplateV(sys.argv[1])
            else :
                CreateTemplateSV(sys.argv[2])
        except IOError:
            error("ERROR: Invalid filename;")

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def main():
    """Entry point used by the executable"""
    vloginit(sys.argv[1:])
