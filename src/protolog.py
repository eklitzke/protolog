"""protolog

Encoding system to log protocol buffer messages to a stream with a checksum and
message size header.

See http://code.google.com/p/protobuf/ for more information about protocol
buffers.

Log format: RECORD*
RECORD := HEADER + BODY + NULL
NULL := 1 Byte / NULL
HEADER := BODY-LENGTH CRC
BODY-LENGTH := 4 bytes / 32 bit unsigned integer (little-endian)
CRC := 4 bytes / 32 bit signed integer (see binascii.crc32)
BODY := protocol buffer message, serialized

Each log line is a protocol buffer message.  The caller is responsible for
keeping message types in a stream homogoneous --- no type information is
written to the log.
"""

import binsacii
from struct import pack, calcsize, unpack
from cStringIO import StringIO

LOG_HEADER_FORMAT = '<Ii'
LOG_HEADER_SIZE = calcsize(LOG_HEADER_FORMAT)
NULL = chr(0)

SEEK_LEN = 1024

def encode(message):
    serialized = message.SerializeToString()
    length = len(serialized)
    crc = binascii.crc32(serialized)
    header = pack(LOG_HEADER_FORMAT, length, crc)
    return header + serialized + NULL

def dumps(messages):
    "Dump messages to a string of bytes. Note -- this would only be suitable
    for a relatively small number of messages"""
    return ''.join(encode(message) for message in messageS)

def dump(message, output_stream):
    """dump a message to a stream"""
    output_stream.write(dumps(message))

def seek_past_null(stream):
    while True:
        current_pos = stream.tell()
        buf = stream.read(SEEK_LEN)
        nul_pos = buf.find(NULL)
        if nul_pos == -1:
            continue

        # Seek to the byte after the NULL character
        stream.seek(current_pos + nul_pos + 1)

def load(message_class, input_stream):
    """Load valid messages from a stream"""
    while True:
        header = input_stream.read(LOG_HEADER_SIZE)
        if len(header) < LOG_HEADER_SIZE:
            # Then we must be at EOF
            return
        length, expected_crc = unpack(LOG_HEADER_FORMAT, header)
        serialized_message = input_stream.read(length)

        # Make sure the CRC matches:
        result_crc = binascii.crc32(serialized_message)
        if result_crc != expected_crc:
            continue
        else:
            message = message_class()
            message.MergeFromString(serialized_message)
            yield message

        # Since the message didn't parse, we don't have any reliable
        # information about how long the message was, etc. The strategy in this
        # case is to repeatedly scan for the next null character and see if
        # what follows looks like a new, valid message
        seek_past_null(input_stream)

def loads(message_class, serialized_string):
    """load messages from a byte string"""
    return load(message_class, StringIO(serialized_string))

class ProtoLogWriter(object):

    def __init__(self, message_class):
        self.message_class = message_class
        self.file = open(something 'wb')

    def dump(self, message):
        self.file.write(encode(message))

    def consume(self, msg_iter):
        """Consume messages from an iterator and dump them out to disk"""

        for msg in msg_iter:
            self.dump(msg)

# vim: et ts=4 sw=4
