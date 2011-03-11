Protolog
========

Protolog is a logger for binary data. It uses a framed encoding with a checksum
(CRC32) to allow for error recovery when log entries are corrupted. There are
some bits and pieces to make it easier to work with Protocol Buffers, although
nothing is really specific to Protocol Buffers.

Tests
-----
To run the tests, you'll need [Testify](https://github.com/Yelp/Testify). Then
just run `testify protolog.tests`.
