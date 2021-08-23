#
# Project       : Verilog/System Verilog code generate functions and templates
# Author        : Shekhalev Denis (des00), Borshch Vladislav
# Contact       : diod2003@list.ru, borchsh.vn@gmail.com
# Licence       : free for use
#
# Workfile      : vlog.py
# Description   : module with verilog code generate functions
'''
module with verilog/system verilog code generate functions
'''

comment = '''\t//------------------------------------------------------------------------------------------------------
\t//
\t//------------------------------------------------------------------------------------------------------
'''
#
# port list     : {name, direction, width, ptype, tab }
# param list    : {name, value    , width, ptype, tab }
# lparam list   : {name, value    , width, ptype }
# signal list   : {name, width, ptype }
# include list  : {filename}
port_list   = []
param_list  = []
lparam_list = []
signal_list = []
inc_list    = []

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def clogb2 (num):
    '''
    function to get amount of bits for representation [0..num-1] value range
    '''
    if num < 0 :
        return 0
    elif num <= 1:
        return 1
    else:
        res = 1
        while num > 2**res:
            res += 1
        return res

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def clogb2_p1 (num):
    '''
    function to get_amount of bits for representation [1..num] value range
    '''
    if num < 1 :
        return 0
    else:
        return clogb2(num + 1)

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def GetPortDir (direct):
    '''
    function to get port direction
    '''
    pattern = {
        'I' : 'input',
        'O' : 'output',
        'IO': 'inout'
        }
    try:
        direct = pattern[direct.upper()]
    except KeyError:
        print('port direction error')
    return direct

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def GetNibleWidth (num):
    '''
    function to get amount of valid nible in the world
    '''
    if num <= 0:
        return 0
    else:
        nible = 1
        while num > 4 :
            num   -= 4
            nible += 1
        return nible

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def GetByteWidth (num):
    '''
    function to get amount of valid bytes in the world
    '''
    if num <= 0:
        return 0
    else:
        byte = 1
        while num > 8 :
            num   -= 8
            byte  += 1
        return byte

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def GetWidth (width):
    '''
    function to get width of port
    '''
    if len(width) == 0:
        return '' # null string
    if width.isdigit():
        iwidth = int(width)
        if iwidth in [0,1]: # single bit or user type
            width = '' # null string
        else:
            width = '[' + str(iwidth-1) + ':0]'  # bit vector
    else :
        width = '['+ str(width)+'-1:0]' # parameter vector

    return width

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def GetAWidth (width):
    '''
    function to get width of array
    '''
    if len(width) == 0:
        return '' # null string
    if width.isdigit():
        iwidth = int(width)
        if iwidth in [0,1]: # single bit or user type
            width = '' # null string
        else:
            width = '['+ str(iwidth) + ']'  # bit vector
    else:
        width = '[' + str(width) + ']' # parameter vector

    return width

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def GetType (ptype):
    '''
    function to get port type
    '''
    _ptype = ptype.upper();
    # common types
    if     _ptype in ['W'] : ptype = 'wire'
    elif   _ptype in ['L'] : ptype = 'logic'
    elif   _ptype in ['B'] : ptype = 'bit'
    elif   _ptype in ['R'] : ptype = 'reg'
    elif   _ptype in ['I'] : ptype = 'int'
    elif   _ptype in ['S'] : ptype = 'string'
    # signed types
    if     _ptype in ['WS'] : ptype = 'wire signed'
    elif   _ptype in ['LS'] : ptype = 'logic signed'
    elif   _ptype in ['BS'] : ptype = 'bit signed'
    elif   _ptype in ['RS'] : ptype = 'reg signed'
    # other types
    elif    len(ptype) != 0 : pass              # user defined type
    else                    : ptype = 'logic'   # default
    return ptype

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def GetParamType (ptype):
    '''
    function to get parameter type
    '''
    _ptype = ptype.upper();
    # common types
    if     _ptype in ['L'] : ptype = 'logic'
    elif   _ptype in ['B'] : ptype = 'bit'
    elif   _ptype in ['R'] : ptype = 'reg'
    elif   _ptype in ['I'] : ptype = 'int'
    elif   _ptype in ['S'] : ptype = 'string'
    # signed types
    if     _ptype in ['WS'] : ptype = 'wire signed'
    elif   _ptype in ['LS'] : ptype = 'logic signed'
    elif   _ptype in ['BS'] : ptype = 'bit signed'
    elif   _ptype in ['RS'] : ptype = 'reg signed'
    # other types
    elif   _ptype in ['U'] : ptype = '' # untyped
    else                   : pass       # user defined type
    return ptype

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def ParseSignals (list):
    '''
    funtion to parse signal list in format {name, width, ptype }
    '''
    this_list = []
    # find max length
    max_name_length     = 0
    max_width_length    = 0
    max_type_length     = 0
    for elem in list:
        try:
            name, width, ptype = elem[0], elem[1], elem[2]
        except IndexError:
            print('parse signal list error')
            return this_list
        # decode
        width  = GetWidth   (width)
        ptype  = GetType    (ptype)
        # max for align
        max_name_length     = max(max_name_length,  len(name) )
        max_width_length    = max(max_width_length, len(width))
        max_type_length     = max(max_type_length,  len(ptype))
        #
        this_list.append([name, width, ptype])
    # align
    for elem in this_list :
        name, width, ptype = elem[0], elem[1], elem[2]
        # rigth aligh
        name    = name  + ' '*(max_name_length - len(name))
        ptype   = ptype + ' '*(max_type_length - len(ptype))
        # left align
        width   = ' '*(max_width_length - len(width)) + width
        #
        elem[0], elem[1], elem[2] = name, width, ptype
    #
    return this_list

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def ParsePorts (list):
    '''
    function to parse port list in format {name, direction, width, ptype, awidth}
    '''
    this_list = []
    # find max length
    max_direct_length   = 0
    max_name_length     = 0
    max_width_length    = 0
    max_type_length     = 0
    max_awidth_length   = 0

    for elem in list:
        try:
            name, direct, width, ptype, awidth, tab = elem[0], elem[1], elem[2], elem[3], elem[4], elem[5]
        except :
            print('parse port list error')
            return this_list
        # decode
        direct = GetPortDir (direct)
        width  = GetWidth   (width)
        ptype  = GetType    (ptype)
        awidth = GetAWidth  (awidth)
        # max for align
        max_direct_length   = max(max_direct_length, len(direct))
        max_name_length     = max(max_name_length,   len(name) )
        max_width_length    = max(max_width_length,  len(width))
        max_type_length     = max(max_type_length,   len(ptype))
        max_awidth_length   = max(max_awidth_length, len(awidth))
        #
        this_list.append([name, direct, width, ptype, awidth, tab])
    #
    for elem in this_list :
        name, direct, width, ptype, awidth = elem[0], elem[1], elem[2], elem[3], elem[4]
        # rigth aligh
        direct  = direct + ' '*(max_direct_length - len(direct))
        name    = name  + ' '*(max_name_length - len(name))
        ptype   = ptype + ' '*(max_type_length - len(ptype))
        # left align
        width   = ' '*(max_width_length - len(width)) + width
        awidth  = ' '*(max_awidth_length - len(awidth)) + awidth;
        #
        elem[0], elem[1], elem[2], elem[3], elem[4] = name, direct, width, ptype, awidth
    return this_list

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def ParseParams (list):
    '''
    function to parse param list in format {name, value    , width, ptype }
    '''
    this_list = []
    # find max length
    max_name_length     = 0
    max_value_length    = 0
    max_width_length    = 0
    max_type_length     = 0
    max_awidth_length   = 0
    for elem in list:
        try:
            name, value, width, ptype, awidth, tab = elem[0], elem[1], elem[2], elem[3], elem[4], elem[5]
        except :
            print('parse parameter list error')
            return this_list
        # decode
        value  = str(value)
        # Replace empty parameter by predefined string
        if not value:
            value = "\"ext\""
        width  = GetWidth       (width)
        ptype  = GetParamType   (ptype)
        awidth = GetAWidth      (awidth)
        # max for align
        max_name_length     = max(max_name_length,   len(name) )
        max_value_length    = max(max_value_length,  len(value))
        max_width_length    = max(max_width_length,  len(width))
        max_type_length     = max(max_type_length,   len(ptype))
        max_awidth_length   = max(max_awidth_length, len(awidth))
        #
        this_list.append([name, value, width, ptype, awidth, tab])
    # align
    for elem in this_list :
        name, value, width, ptype, awidth = elem[0], elem[1], elem[2], elem[3], elem[4]
        #
        # rigth aligh
        name    = name  + ' '*(max_name_length - len(name))
        ptype   = ptype + ' '*(max_type_length - len(ptype))
        # left align
        width   = ' '*(max_width_length - len(width)) + width
        awidth  = ' '*(max_awidth_length - len(awidth)) + awidth
        value   = ' '*(max_value_length - len(value)) + value
        #
        elem[0], elem[1], elem[2], elem[3], elem[4] = name, value, width, ptype, awidth
    return this_list

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def PrintIncludeFiles (list):
    '''
    function to prin include files
    '''
    context = ''
    for elem in list :
        context += '`include "' + elem + '"\n'
    return context

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def PrintPortMap (list):
    '''
    function to print declaration of port names in verilog module
    '''
    if len(list) == 0 :
        return ''
    #
    context = '(\n'
    for elem in list:
        name, tab = elem[0], elem[5]
        context += '\t' + name + ' ,\n'
        if tab:
            if tab[0] == '*':
                context += '\t//' + tab[1:] + '\n'
    # cut off last symbol ',\n'
    context = context[:-2] + '\n);\n'
    return context

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def PrintPortMapSV (list):
    '''
    function to print declaration of port names in system verilog module
    '''
    if len(list) == 0 :
        return ''
    #
    context = '(\n'
    for elem in list:
        name, direct, width, ptype, awidth, tab = elem[0], elem[1], elem[2], elem[3], elem[4], elem[5]
        
        if len(width) == 0:
            context += '\t' + direct + ' ' + ptype + ' '
        else:
            context += '\t' + direct + ' ' + ptype + ' ' + width + ' '

        if len(awidth) == 0:
            context += name + ' ,\n';
        else:
            context += name + ' ' + awidth +' ,\n';

        if tab:
            if tab[0] == '*':
                context += '\t//' + tab[1:] + '\n'
    # cut off last symbol ',\n'
    context = context[:-2] + '\n);\n'
    return context

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def PrintPortList (list):
    '''
    function to print declaration of port types in verilog module
    '''
    if len(list) == 0:
        return ''
    #
    context = ''
    for elem in list:
        name, direct, width, ptype, awidth, tab = elem[0], elem[1], elem[2], elem[3], elem[4], elem[5]

        if len(width) == 0:
            context += '\t' + direct + ' ' + ptype + ' '
        else:
            context += '\t' + direct + ' ' + ptype + ' ' + width + ' '

        if len(awidth) == 0:
            context += name + ' ;\n';
        else:
            context += name + ' ' + awidth +' ;\n';

        if tab:
            if tab[0] == '*':
                context += '\t//' + tab[1:] + '\n'
    #
    return context

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def PrintPortDeclaration (mname, list):
    '''
    function to print declaration of signals to connect module ports at module instance
    '''
    if len(list) == 0:
        return ''
    #
    context = ''
    for elem in list:
        name, direct, width, ptype, awidth, tab = elem[0], elem[1], elem[2], elem[3], elem[4], elem[5]
        pin_name = mname + '__' + name

        if len(width) == 0:
            context += '\t' + ptype + ' '
        else:
            context += '\t' + ptype + ' ' + width + ' '

        if len(awidth) == 0:
            context += pin_name + ' ;\n'
        else:
            context += pin_name + ' ' + awidth + ' ;\n'
    #
    return context

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def PrintPortInstance (mname, list):
    '''
    function to print port map in verilog module instance
    '''
    if len(list) == 0:
        return ''
    #
    context = '\t(\n'
    for elem in list:
        name, tab = elem[0], elem[5]
        pin_name = mname + '__' + name
        context += '\t\t.' + name + ' (' + pin_name +'      )' + ' ,\n'
    # cut off last symbol ',\n'
    context = context[:-2] + '\n\t);\n'
    return context

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def PrintPortAssign (mname, list):
    '''
    function to print assigns of input signals to connect module ports at module instance
    '''
    if len(list) == 0:
        return ''
    #
    # first time lets truncate ' ' symbols in left of input port name
    #
    names = []
    max_name_length = 0;

    for elem in list:
        name, direct = elem[0], elem[1]
        if direct[0] == 'i':
            names.append(name)
            name_length = len(name.rstrip())
            if name_length > max_name_length :
                max_name_length = name_length
    # write input signals assign
    context = ''
    for name in names:
        pin_name = mname + '__' + name[:max_name_length]
        context += '\tassign ' + pin_name + ' = \'0' + ';\n'
    #
    return context

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def PrintParamMap(list) :
    '''
    functions to print parameters declaration in verilog module
    '''
    if len(list) == 0:
        return ''
    #
    context = '#(\n'
    for elem in list:
        name, value, width, ptype, awidth, tab = elem[0], elem[1], elem[2], elem[3], elem[4], elem[5]

        if len(width) == 0:
            context += '\tparameter ' + ptype + ' ' + name
        else:
            context += '\tparameter ' + ptype + ' ' + width + ' ' + name

        if len(awidth) == 0:
            context += ' = ' + value + ' ,\n'
        else:
            context += ' ' + awidth + ' = ' + value + ' ,\n'

        if tab:
            if tab[0] == '*':
                context += '\t//' + tab[1:] + '\n'
    # cut off last symbol ',\n'
    context = context[:-2] + '\n)\n'
    return context

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def PrintParamDeclaration (mname, list):
    '''
    functions to print parameters declaration at verilog module instance
    '''
    if len(list) == 0:
        return ''
    #
    context = ''
    for elem in list :
        name, value, width, ptype, awidth, tab = elem[0], elem[1], elem[2], elem[3], elem[4], elem[5]

        if len(width) == 0:
            context += '\tparameter ' + ptype + ' ' + name + ' '
        else:
            context += '\tparameter ' + ptype + ' ' + width + ' ' + name + ' '

        if len(awidth) == 0:
            context += '= ' + value + ';\n'
        else:
            context += awidth + ' = ' + value + ';\n'

    return context

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def PrintParamInstance  (list):
    '''
    functions to print parameters map assign at verilog module instance
    '''
    if len(list) == 0:
        return ''
    #
    context = '\t#(\n'
    for elem in list:
        name, value, tab = elem[0], elem[0], elem[5]
        context += '\t\t. ' + name + '    (' + str(value) +'      )' + ' ,\n'
    # cut off last symbol ',\n'
    context = context[:-2] + '\n\t)\n'
    return context

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def PrintLocalParamMap (list):
    '''
    function to print localparams for verilog module
    '''
    context = ''
    for elem in list:
        name, value, width, ptype, awidth = elem[0], elem[1], elem[2], elem[3], elem[4]

        if len(width) == 0:
            context += '\tlocalparam ' + ptype + ' ' + name
        else:
            context += '\tlocalparam ' + ptype + ' ' + width + ' ' + name

        if len(awidth) == 0:
            context += ' = ' + value + ';\n'
        else:
            context += ' ' + awidth + ' = ' + value + ';\n'
    #
    return context

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def PrintSignals (list):
    '''
    function to print any other signals declaration field
    '''
    context = ''
    for elem in list :
        name, width, ptype = elem[0], elem[1], elem[2]
        context += '\t' + ptype + ' ' + width + ' ' + name + ';\n'
    return context

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def PrintModuleInstanceCode (mname, param_list, port_list):
    '''
    function to print module instantce
    '''
    # start
    context = '/*\n'
    # null
    context += '\n'
    # insert addidition info label
    context += '%(inst_info)s\n'
    # null
    context += '\n'
    # param declaration
    context += PrintParamDeclaration(mname, param_list)
    # null
    context += '\n\n\n'
    # port declaration
    context += PrintPortDeclaration(mname, port_list)
    # null
    context += '\n\n\n'
    # module name
    context += '\t' + mname + '\n'
    # parameter of instance
    context += PrintParamInstance(param_list)
    # instance name
    context += '\t' + mname + '__\n'
    # port map
    context += PrintPortInstance(mname, port_list)
    # null
    context += '\n\n'
    # assigns to input
    context += PrintPortAssign(mname, port_list)
    # null
    context += '\n\n\n'
    # end
    context += '*/ \n'
    return context

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
def PrintModuleDeclarationCode (mname, param_list, lparam_list, port_list, sv_mode):
    '''
    function to print module declaration
    '''
    if sv_mode:
        print('Runned in SV mode...')
    else:
        print('Runned in V mode...')
    #
    context = ''
    # header info
    context = '\n%(header_info)s\n\n'
    # module name
    context += 'module ' + mname + '\n'
    # parameter map
    context += PrintParamMap(param_list);
    # port map
    if sv_mode:
        context += PrintPortMapSV(port_list);
    else:
        context += PrintPortMap(port_list);
    # null
    context += '\n' + comment + '\n'
    # localparam map
    context += PrintLocalParamMap(lparam_list)
    if len(lparam_list) != 0 :
        context += '\n' + comment + '\n'
    # port list
    if not sv_mode:
        context += PrintPortList(port_list);
    # local module signal declaration secton
    context += '\n' + comment + '\n'
    # insert module signal label
    context += '%(signal)s'
    # process module section
    context += '\n' + comment + '\n'
    context += '%(process)s\n'
    context += '\nendmodule\n'
    return context
