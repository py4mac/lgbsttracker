# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: common.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='common.proto',
  package='common',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0c\x63ommon.proto\x12\x06\x63ommon*\x82\x02\n\tErrorCode\x12\x12\n\x0eINTERNAL_ERROR\x10\x00\x12\x1b\n\x17TEMPORARILY_UNAVAILABLE\x10\x01\x12\x16\n\x12\x45NDPOINT_NOT_FOUND\x10\x02\x12\x15\n\x11PERMISSION_DENIED\x10\x03\x12\x1a\n\x16REQUEST_LIMIT_EXCEEDED\x10\x04\x12\x0f\n\x0b\x42\x41\x44_REQUEST\x10\x05\x12\x1b\n\x17INVALID_PARAMETER_VALUE\x10\x06\x12\x1b\n\x17RESOURCE_DOES_NOT_EXIST\x10\x07\x12\x11\n\rINVALID_STATE\x10\x08\x12\x1b\n\x17RESOURCE_ALREADY_EXISTS\x10\tb\x06proto3')
)

_ERRORCODE = _descriptor.EnumDescriptor(
  name='ErrorCode',
  full_name='common.ErrorCode',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='INTERNAL_ERROR', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TEMPORARILY_UNAVAILABLE', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ENDPOINT_NOT_FOUND', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PERMISSION_DENIED', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REQUEST_LIMIT_EXCEEDED', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BAD_REQUEST', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_PARAMETER_VALUE', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RESOURCE_DOES_NOT_EXIST', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_STATE', index=8, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RESOURCE_ALREADY_EXISTS', index=9, number=9,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=25,
  serialized_end=283,
)
_sym_db.RegisterEnumDescriptor(_ERRORCODE)

ErrorCode = enum_type_wrapper.EnumTypeWrapper(_ERRORCODE)
INTERNAL_ERROR = 0
TEMPORARILY_UNAVAILABLE = 1
ENDPOINT_NOT_FOUND = 2
PERMISSION_DENIED = 3
REQUEST_LIMIT_EXCEEDED = 4
BAD_REQUEST = 5
INVALID_PARAMETER_VALUE = 6
RESOURCE_DOES_NOT_EXIST = 7
INVALID_STATE = 8
RESOURCE_ALREADY_EXISTS = 9


DESCRIPTOR.enum_types_by_name['ErrorCode'] = _ERRORCODE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)


# @@protoc_insertion_point(module_scope)
