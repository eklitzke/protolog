"""protolog

Encoding system to log protocol buffer messages to a stream with a checksum and message size header.

See http://code.google.com/p/protobuf/ for more information about protocol buffers.

Log format: RECORD*
RECORD := HEADER + BODY + NULL 
NULL := 1 Byte / NULL
HEADER := BODY-LENGTH CRC
BODY-LENGTH := 4 bytes / 32 bit unsigned integer
CRC := 4 bytes / 32 bit signed integer (see binascii.crc32)
BODY := protocol buffer message, serialized

Each log line is a protocol buffer message.  The caller is responsible for
keeping message types in a stream homogoneous --- no type information is
written to the log.
"""

from binascii import *
from struct import pack, calcsize, unpack
from StringIO import StringIO

LOG_HEADER_FORMAT = 'Ii' 
LOG_HEADER_SIZE = calcsize(LOG_HEADER_FORMAT)
NULL = chr(0)

def dumps(messages):
    """dump messages to a string of bytes"""
    blobs = []
    for message in messages:
        serialized_message = message.SerializeToString()
        length = len(serialized_message) 
        crc = crc32(serialized_message)
        header = pack(LOG_HEADER_FORMAT, length, crc)
        blobs.append(header + serialized_message + NULL)
    return ''.join(blobs)

def dump(message, output_stream):
    """dump a message to a stream"""
    output_stream.write(dumps(message))

def load(message_class, input_stream):
    """load messages from a stream"""
    while True:
        header = input_stream.read(LOG_HEADER_SIZE)
        if len(header) < LOG_HEADER_SIZE:
            # Then we must be at EOF
            return
        length, expected_crc = unpack(LOG_HEADER_FORMAT, header)
        serialized_message = input_stream.read(length)

        # Make sure the crc matches:
        result_crc = crc32(serialized_message)
        if result_crc != expected_crc:
            continue
        else:
            message = message_class()
            message.MergeFromString(serialized_message)
            yield message

        # Advance past the next null
        while True:
            next_char = input_stream.read(1)
            if not next_char:
                return
            if next_char != NULL:
                continue
        
def loads(message_class, serialized_string):
    """load messages from a byte string"""
    return load(message_class, StringIO(serialized_string))
