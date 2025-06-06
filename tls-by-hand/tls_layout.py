# RFC 2246 – Record §6.2.1, Handshake §7.4, ClientHello §7.4.1.2
from ctypes import *

class TLSRecHdr(BigEndianStructure):
    _pack_ = 1
    _fields_ = [('type',c_uint8),('ver',c_uint16),('ln',c_uint16)]

class HSHdr(BigEndianStructure):
    _pack_ = 1
    _fields_ = [('msg',c_uint8),('ln',c_uint32)]      # ln é uint24; usamos 32-bits

class ChFixed(BigEndianStructure):
    _pack_ = 1
    _fields_=[('ver',c_uint16),('rand',c_uint8*32),('sid_len',c_uint8)]

sizeof_rec = sizeof(TLSRecHdr)
sizeof_hs  = sizeof(HSHdr)
sizeof_chf = sizeof(ChFixed)
