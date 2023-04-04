#===============================================================================
# led8x8icons.py
#
# Dictionary of LED 8x8 matrix icons as 64 bit values.
#
# Code snippet for computing value from bitmap:
#
#           BITMAP = [
#           [1, 1, 1, 1, 1, 1, 1, 1,],
#           [1, 1, 0, 0, 0, 0, 0, 1,],
#           [1, 0, 1, 0, 0, 0, 0, 1,],
#           [1, 0, 0, 1, 0, 0, 0, 1,],
#           [1, 0, 0, 0, 1, 0, 0, 1,],
#           [1, 0, 0, 0, 0, 1, 0, 1,],
#           [1, 0, 0, 0, 0, 0, 1, 1,],
#           [1, 0, 0, 0, 0, 0, 0, 1,],
#           ]
#           value = 0
#           for y,row in enumerate(BITMAP):
#               row_byte = 0
#               for x,bit in enumerate(row):
#                   row_byte += bit<<x    
#               value += row_byte<<(8*y)
#           print '0x'+format(value,'02x')
#
# Code snippet for setting individual LEDs on the display.
#
#        def set_raw64(value):
#            led8x8matrix.clear()
#            for y in xrange(8):
#                row_byte = value>>(8*y)
#                for x in xrange(8):
#                    pixel_bit = row_byte>>x&1 
#                    led8x8matrix.set_pixel(x,y,pixel_bit) 
#            led8x8mmatrix.write_display() 
#
# 2014-10-20
# Carter Nelson
#==============================================================================
LED8x8ICONS = {
#---------------------------------------------------------
# default
#---------------------------------------------------------
''                                  : 0x0000000000000000 ,    
#---------------------------------------------------------
# misc
#---------------------------------------------------------
'ALL_ON'                            : 0xffffffffffffffff ,
'ALL_OFF'                           : 0x0000000000000000 ,
'UNKNOWN'                           : 0x00004438006c6c00 ,
'BOTTOM_ROW'                        : 0xff00000000000000 ,
'TOP_ROW'                           : 0x00000000000000ff , 
'LEFT_COL'                          : 0x0101010101010101 ,
'RIGHT_COL'                         : 0x8080808080808080 ,
'BOX'                               : 0xff818181818181ff ,
'XBOX'                              : 0xffc3a59999a5c3ff ,
'§'                                 : 0x3c4299858599423c ,
#---------------------------------------------------------
# weather
#---------------------------------------------------------
'SUNNY'                             : 0x9142183dbc184289 ,
'RAIN'                              : 0x55aa55aa55aa55aa ,
'CLOUD'                             : 0x00007e818999710e ,
'SHOWERS'                           : 0x152a7e818191710e ,
'SNOW'                              : 0xa542a51818a542a5 ,
'STORM'                             : 0x0a04087e8191710e ,
#---------------------------------------------------------
# characters
#---------------------------------------------------------
' '          : 0x0000000000000000 ,
'!'          : 0x00180018183C3C18 ,
'"'          : 0x0000000000003636 ,
'#'          : 0x0036367F367F3636 ,
'$'          : 0x000C1F301E033E0C ,
'%'          : 0x0063660C18336300 ,
'&'          : 0x006E333B6E1C361C ,
'\''          : 0x0000000000030606 ,
'('          : 0x00180C0606060C18 ,
')'          : 0x00060C1818180C06 ,
'*'          : 0x0000663CFF3C6600 ,
'+'          : 0x00000C0C3F0C0C00 ,
','          : 0x060C0C0000000000 ,
'-'          : 0x000000003F000000 ,
'.'          : 0x000C0C0000000000 ,
'/'          : 0x000103060C183060 ,
'0'          : 0x003E676F7B73633E ,
'1'          : 0x003F0C0C0C0C0E0C ,
'2'          : 0x003F33061C30331E ,
'3'          : 0x001E33301C30331E ,
'4'          : 0x0078307F33363C38 ,
'5'          : 0x001E3330301F033F ,
'6'          : 0x001E33331F03061C ,
'7'          : 0x000C0C0C1830333F ,
'8'          : 0x001E33331E33331E ,
'9'          : 0x000E18303E33331E ,
':'          : 0x000C0C00000C0C00 ,
';'          : 0x060C0C00000C0C00 ,
'<'          : 0x00180C0603060C18 ,
'='          : 0x00003F00003F0000 ,
'>'          : 0x00060C1830180C06 ,
'?'          : 0x000C000C1830331E ,
'@'          : 0x001E037B7B7B633E ,
'A'          : 0x0033333F33331E0C ,
'B'          : 0x003F66663E66663F ,
'C'          : 0x003C66030303663C ,
'D'          : 0x001F36666666361F ,
'E'          : 0x007F46161E16467F ,
'F'          : 0x000F06161E16467F ,
'G'          : 0x007C66730303663C ,
'H'          : 0x003333333F333333 ,
'I'          : 0x001E0C0C0C0C0C1E ,
'J'          : 0x001E333330303078 ,
'K'          : 0x006766361E366667 ,
'L'          : 0x007F66460606060F ,
'M'          : 0x0063636B7F7F7763 ,
'N'          : 0x006363737B6F6763 ,
'O'          : 0x001C36636363361C ,
'P'          : 0x000F06063E66663F ,
'Q'          : 0x00381E3B3333331E ,
'R'          : 0x006766363E66663F ,
'S'          : 0x001E33380E07331E ,
'T'          : 0x001E0C0C0C0C2D3F ,
'U'          : 0x003F333333333333 ,
'V'          : 0x000C1E3333333333 ,
'W'          : 0x0063777F6B636363 ,
'X'          : 0x0063361C1C366363 ,
'Y'          : 0x001E0C0C1E333333 ,
'Z'          : 0x007F664C1831637F ,
'['          : 0x001E06060606061E ,
'\\'          : 0x00406030180C0603 ,
']'          : 0x001E18181818181E ,
'^'          : 0x0000000063361C08 ,
'_'          : 0xFF00000000000000 ,
'`'          : 0x0000000000180C0C ,
'a'          : 0x006E333E301E0000 ,
'b'          : 0x003B66663E060607 ,
'c'          : 0x001E3303331E0000 ,
'd'          : 0x006E33333e303038 ,
'e'          : 0x001E033f331E0000 ,
'f'          : 0x000F06060f06361C ,
'g'          : 0x1F303E33336E0000 ,
'h'          : 0x006766666E360607 ,
'i'          : 0x001E0C0C0C0E000C ,
'j'          : 0x1E33333030300030 ,
'k'          : 0x0067361E36660607 ,
'l'          : 0x001E0C0C0C0C0C0E ,
'm'          : 0x00636B7F7F330000 ,
'n'          : 0x00333333331F0000 ,
'o'          : 0x001E3333331E0000 ,
'p'          : 0x0F063E66663B0000 ,
'q'          : 0x78303E33336E0000 ,
'r'          : 0x000F06666E3B0000 ,
's'          : 0x001F301E033E0000 ,
't'          : 0x00182C0C0C3E0C08 ,
'u'          : 0x006E333333330000 ,
'v'          : 0x000C1E3333330000 ,
'w'          : 0x00367F7F6B630000 ,
'x'          : 0x0063361C36630000 ,
'y'          : 0x1F303E3333330000 ,
'z'          : 0x003F260C193F0000 ,
'{'          : 0x00380C0C070C0C38 ,
'|'          : 0x0018181800181818 ,
'}'          : 0x00070C0C380C0C07 ,
'~'          : 0x0000000000003B6E ,
}
