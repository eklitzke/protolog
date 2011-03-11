import protolog

class ProtocolBufferLogger(protolog.ProtoLogger):

    def encode(self, pb):
        return super(ProtocolBufferLogger, self).encode(pb.SerializeToString())

# XXX: terrible class name
class ProtocolBufferDecoder(protolog.ProtoDecoder):
    """A protolog decoder that automatically unserializes protocol buffers"""

    def __init__(self, file_obj, pb_cls):
        def decode(s):
            pb = pb_cls()
            pb.ParseFromString(s)
            return pb
        super(ProtocolBufferDecoder, self).__init__(file_obj, decode)


__all__ = ['ProtocolBufferLogger', 'ProtocolBufferDecoder']
