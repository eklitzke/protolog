"""
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

(this could be expanded by including a flags field, ala memcached?)
"""

import binascii
from struct import pack, calcsize, unpack
from cStringIO import StringIO

LOG_HEADER_FORMAT = '<II'
LOG_HEADER_SIZE = calcsize(LOG_HEADER_FORMAT)
NULL = chr(0)

SEEK_LEN = 1024


class DecodeError(ValueError):

    def __init__(self, init_pos):
        super(DecodeError, self).__init__()
        self.init_pos = init_pos

class DecodeErrorEOF(DecodeError): pass
class DecodeErrorMissingNull(DecodeError): pass
class DecodeErrorInvalidLength(DecodeError): pass

def compute_crc(msg):
    crc = binascii.crc32(msg)
    if crc < 0:
        crc += 1<<32 # zlib on 32 bit platforms treats the crc as signed
    return crc

class ProtoLogger(object):
    """A protologger, which writes raw byte streams out to a file object. You
    can also use this as a context manager if you want the file to be
    automatically closed.
    """

    def __init__(self, file_obj):
        self.file = file_obj

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.flush()
        self.file.close()
        return

    def encode(self, msg):
        if type(msg) is not str: # we really want a raw string here, not subclasses
            raise ValueError('message is not a binary string')
        length = len(msg)
        header = pack(LOG_HEADER_FORMAT, length, compute_crc(msg))
        return header + msg + NULL

    def append(self, msg):
        """Append a message to the log."""
        self.file.write(self.encode(msg))

class ProtoDecoder(object):

    MAX_MSG_LEN = 100<<20 # 100mb

    def __init__(self, file_obj, decoder=None):
        """Arguments:
            file_obj -- a file-like object to read from; should support seeking
                        and telling
            decoder  -- if not None, this is something to use to decode read messages
        """
        self.file = file_obj
        self.decoder = decoder or (lambda x: x)

    def get_message(self):
        init_pos = self.file.tell()
        hdr = self.file.read(LOG_HEADER_SIZE)
        if not hdr:
            # we're at the end of the file
            raise DecodeErrorEOF(init_pos)
        if len(hdr) < LOG_HEADER_SIZE:
            raise DecodeErrorEOF(init_pos)
        body_len, expected_crc = unpack(LOG_HEADER_FORMAT, hdr)
        if body_len > self.MAX_MSG_LEN:
            raise DecodeErrorInvalidLength(init_pos)


        read_length = body_len + 1 # to accomodate the null byte
        body = self.file.read(read_length)
        if len(body) < read_length:
            raise DecodeErrorEOF(init_pos)

        # check for the null byte first, because that's the cheapest check
        if body[-1] != NULL:
            raise DecodeErrorMissingNull(init_pos)

        # compare the seen vs. expected CRC
        # XXX: or do two reads to avoid a memory copy?
        pb_data = body[:-1]
        actual_crc = compute_crc(pb_data)

        if expected_crc != actual_crc:
            raise DecodeErrorCRC(init_pos)
        return pb_data

    def __iter__(self):
        """Return the messages as a stream."""
        while True:
            try:
                msg = self.get_message()
                yield self.decoder(msg)
            except DecodeErrorEOF:
                break
            except DecodeError, e:
                # this is really ghetto, and SLOW... much better would be to
                # mmap the file here, which would make searching for a null byte
                # signfiicantly faster (but less portable, might not work with
                # some fake file types, etc.)
                self.file.seek(e.init_pos + 1)
                continue

from protolog.pb import *
