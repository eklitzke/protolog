from unittest import main, TestCase
from StringIO import StringIO
from google.protobuf.text_format import MessageToString
from webserver_pb2 import Request, Header

from protolog import dumps, loads

class WriteLog(TestCase):
    def test(self):
        file = StringIO('')
        request = Request()
        request.ip = 0
        request.responseGiven = 200
        request.uri = '/search'
        request.method = Request.POST
        parsed_requests = list(loads(Request, dumps([request])))
        assert parsed_requests
        for parsed_request in parsed_requests:
            assert request == parsed_request

if __name__ == "__main__":
    main()
