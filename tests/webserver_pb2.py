#!/usr/bin/python2.4
# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import service
from google.protobuf import service_reflection
from google.protobuf import descriptor_pb2


_REQUEST_METHOD = descriptor.EnumDescriptor(
  name='Method',
  full_name='webserver.Request.Method',
  filename='Method',
  values=[
    descriptor.EnumValueDescriptor(
      name='POST', index=0, number=0,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='GET', index=1, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='PUT', index=2, number=2,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='DELETE', index=3, number=3,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='HEAD', index=4, number=4,
      options=None,
      type=None),
  ],
  options=None,
)


_REQUEST = descriptor.Descriptor(
  name='Request',
  full_name='webserver.Request',
  filename='webserver.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='ip', full_name='webserver.Request.ip', index=0,
      number=2, type=5, cpp_type=1, label=1,
      default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='method', full_name='webserver.Request.method', index=1,
      number=3, type=14, cpp_type=8, label=1,
      default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='responseGiven', full_name='webserver.Request.responseGiven', index=2,
      number=4, type=5, cpp_type=1, label=1,
      default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='header', full_name='webserver.Request.header', index=3,
      number=5, type=11, cpp_type=10, label=3,
      default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='uri', full_name='webserver.Request.uri', index=4,
      number=6, type=9, cpp_type=9, label=1,
      default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
    _REQUEST_METHOD,
  ],
  options=None)


_HEADER = descriptor.Descriptor(
  name='Header',
  full_name='webserver.Header',
  filename='webserver.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='key', full_name='webserver.Header.key', index=0,
      number=1, type=9, cpp_type=9, label=2,
      default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='value', full_name='webserver.Header.value', index=1,
      number=2, type=9, cpp_type=9, label=2,
      default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_REQUEST.fields_by_name['method'].enum_type = _REQUEST_METHOD
_REQUEST.fields_by_name['header'].message_type = _HEADER

class Request(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _REQUEST

class Header(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _HEADER

