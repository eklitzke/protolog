from binascii import *
from struct import pack, calcsize, unpack
from StringIO import StringIO

LOG_HEADER_FORMAT = 'Ii' 
LOG_HEADER_SIZE = calcsize(LOG_HEADER_FORMAT)
NULL = chr(0)

def dumps(messages):
    blobs = []
    for message in messages:
        serialized_message = message.SerializeToString()
        length = len(serialized_message) 
        crc = crc32(serialized_message)
        header = pack(LOG_HEADER_FORMAT, length, crc)
        blobs.append(header + serialized_message + NULL)
    return ''.join(blobs)

def dump(message, output_stream):
    output_stream.write(dumps(message))

def load(message_class, input_stream):
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
    return load(message_class, StringIO(serialized_string))
