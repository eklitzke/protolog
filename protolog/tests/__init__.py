import os
import protolog
#import person_pb2 as person_proto
import person_proto
import tempfile
from testify import *

class DecoderTests(TestCase):

    @staticmethod
    def load_file(name):
        # XXX: assumes you're in an appropriate directory
        return open(os.path.join('data', name), 'rb')
        return 
        self.decoder = protolog.ProtoDecoder(f)

    def test_null(self):
        self.decoder = protolog.ProtoDecoder(self.load_file('null.dat'))
        assert_equal(list(self.decoder), [])

    def test_urandom(self):
        self.decoder = protolog.ProtoDecoder(self.load_file('urandom.dat'))
        assert_equal(list(self.decoder), [])

    def check_persons(self):
        """a helper for test_persons &c."""
        people = list(self.decoder)
        assert_equal(len(people), 2)
        assert all(isinstance(p, person_proto.Person) for p in people)
        assert_equal(people[0].name, 'George Washington')
        assert_equal(people[0].birth_year, 1732)
        assert_equal(people[1].name, 'Abraham Lincoln')
        assert_equal(people[1].birth_year, 1809)

    def test_persons(self):
        self.decoder = protolog.ProtocolBufferDecoder(self.load_file('persons.dat'), person_proto.Person)
        self.check_persons()

    def test_persons_with_corruption(self):
        """This is like test_persons, but the file has an extra null byte
        between the two records. The null byte should be skipped over.
        """
        self.decoder = protolog.ProtocolBufferDecoder(self.load_file('extra_middle_byte.dat'), person_proto.Person)
        self.check_persons()

    def test_persons_with_corruption_dos(self):
        """This data file consists of three records, and the middle record has
        its final null byte removed (so the record is corrupted, and cannot be
        recovered)
        """
        self.decoder = protolog.ProtocolBufferDecoder(self.load_file('corrupt.dat'), person_proto.Person)
        self.check_persons()

class EncoderTests(TestCase):

    def test_persons(self):
        washington = person_proto.Person(name='George Washington', birth_year=1732)
        lincoln = person_proto.Person(name='Abraham Lincoln', birth_year=1809)

        with tempfile.TemporaryFile() as temp_file:
            logger = protolog.ProtocolBufferLogger(temp_file)
            logger.append(washington)
            logger.append(lincoln)

            # sanity check the length
            assert_equal(temp_file.tell(), 60)

    def test_context_manager(self):
        """Test using the encoder as a context manager... this is kind of a lame test."""
        with tempfile.TemporaryFile() as temp_file:
            assert_equal(temp_file.closed, False)
            with protolog.ProtocolBufferLogger(temp_file) as logger:
                pass
            assert_equal(temp_file.closed, True)

if __name__ == '__main__':

    def doit(fname, name, birth_year):
        f = open(fname, 'wb')
        p = person_proto.Person(name=name, birth_year=birth_year)
        logger = protolog.ProtocolBufferLogger(f)
        logger.append(p)

    #doit('a', 'George Washington', 1732)
    #doit('b', 'Thomas Jefferson', 1743)
    #doit('c', 'Abraham Lincoln', 1809)

    #run()
