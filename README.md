# Templates generator: make Verilog/SystemVerilog module template by parameters and ports list

## Usage
Verilog-style generation:

`python veriloginit.py somefile.dat`

SystemVerilog-style generation: 

`python veriloginit.py -sv somefile.dat`

### Mnemonics list

```
module name     : %file_name
include file    : `<name>
parameter       : $<name> # <value> # <param_type> # <width> # <array width>
localparam      : ?<name> # <value> # <param_type> # <width> # <array width>
port            : @<direction> # <name> # <width> # <port_type> # <array width>
comment list    : "/", "//"
comment RTL     : "*"
```

### Ports description mnemonics
```
<width>         default `1`. Number's or parameter name - both is possible. If there is no previously defined parameter - this parameter will defined.
<port type>     default `logic`. Define required mnemonic, in case it necesary
<array width>   Number or parameter's name - both is possible. Only 1-D arrays. TODO: N-D arrays support
<direction>     = [ i   : input             ,
                    o   : output            ,
                    io  : inout
                  ]

<port_type>     = [ w/W       : wire        ,
                    l/L       : logic       ,
                    b/B       : bit         ,
                    r/R       : reg         ,
                    ws/Ws     : wire signed ,
                    ls/Ls     : logic signed,
                    bs/Bs     : bit signed  ,
                    rs/Rs     : reg signed  ,
                    i/I       : int         ,
                    user_type
                  ]

<param_type>    = [ l/L       : logic       ,
                    b/B       : bit         ,
                    r/R       : reg         ,
                    i/I       : int         ,
                    u/U       : untyped     ,
                    user_type
                  ]
```

### Parameters/local parameters mnemonics
```
    <value>         default "1". Number's or parameter name - both is possible. If there is no previously defined parameter - this parameter will defined.
    <param type>    default "int". Define required mnemonic, in case it necesary
    <width>         default "1". Number's or parameter name - both is possible. If there is no previously defined parameter - this parameter will defined.
    <array width>   Number or parameter's name - both is possible. Only 1-D arrays. TODO: N-D arrays support
```

### Comments mnemonics
```
comment list:
    String started with '/'. Exclude this string from vloginit parsing

comment RTL:
    String started with "//". Translated into RTL comment line.
```

In case using only default values for all fields possible to leave it blank. But separation symbol '#' must be inserted

### Examples

Input and results files are accessible `./examples`
