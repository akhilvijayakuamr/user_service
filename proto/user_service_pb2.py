# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: user_service.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12user_service.proto\x12\x0cuser_service\"Y\n\x11\x43reateUserRequest\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x10\n\x08username\x18\x02 \x01(\t\x12\x11\n\tfull_name\x18\x03 \x01(\t\x12\x10\n\x08password\x18\x04 \x01(\t\"4\n\x12\x43reateUserResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\r\n\x05\x65rror\x18\x02 \x01(\t\".\n\x10VerifyOtpRequest\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x0b\n\x03otp\x18\x02 \x01(\t\"3\n\x11VerifyOtpResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\r\n\x05\x65rror\x18\x02 \x01(\t\"!\n\x10ResendOtpRequest\x12\r\n\x05\x65mail\x18\x01 \x01(\t\"3\n\x11ResendOtpResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\r\n\x05\x65rror\x18\x02 \x01(\t\"E\n\x10LoginUserRequest\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\x12\x10\n\x08provider\x18\x03 \x01(\t\"H\n\rLoginResponse\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05\x65mail\x18\x02 \x01(\t\x12\x0b\n\x03jwt\x18\x03 \x01(\t\x12\x0f\n\x07message\x18\x04 \x01(\t\"4\n\x11LoginAdminRequest\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"2\n\x12LoginAdminResponse\x12\x0b\n\x03jwt\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\"Y\n\x04User\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x10\n\x08username\x18\x02 \x01(\t\x12\x11\n\tfull_name\x18\x03 \x01(\t\x12\r\n\x05\x65mail\x18\x04 \x01(\t\x12\x11\n\tis_active\x18\x05 \x01(\x08\"\x11\n\x0fUserListRequest\"5\n\x10UserListResponse\x12!\n\x05users\x18\x01 \x03(\x0b\x32\x12.user_service.User2\xe0\x03\n\x0bUserService\x12O\n\nCreateUser\x12\x1f.user_service.CreateUserRequest\x1a .user_service.CreateUserResponse\x12L\n\tVerifyOtp\x12\x1e.user_service.VerifyOtpRequest\x1a\x1f.user_service.VerifyOtpResponse\x12H\n\tLoginUser\x12\x1e.user_service.LoginUserRequest\x1a\x1b.user_service.LoginResponse\x12O\n\nLoginAdmin\x12\x1f.user_service.LoginAdminRequest\x1a .user_service.LoginAdminResponse\x12L\n\tResendOtp\x12\x1e.user_service.ResendOtpRequest\x1a\x1f.user_service.ResendOtpResponse\x12I\n\x08UserList\x12\x1d.user_service.UserListRequest\x1a\x1e.user_service.UserListResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'user_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_CREATEUSERREQUEST']._serialized_start=36
  _globals['_CREATEUSERREQUEST']._serialized_end=125
  _globals['_CREATEUSERRESPONSE']._serialized_start=127
  _globals['_CREATEUSERRESPONSE']._serialized_end=179
  _globals['_VERIFYOTPREQUEST']._serialized_start=181
  _globals['_VERIFYOTPREQUEST']._serialized_end=227
  _globals['_VERIFYOTPRESPONSE']._serialized_start=229
  _globals['_VERIFYOTPRESPONSE']._serialized_end=280
  _globals['_RESENDOTPREQUEST']._serialized_start=282
  _globals['_RESENDOTPREQUEST']._serialized_end=315
  _globals['_RESENDOTPRESPONSE']._serialized_start=317
  _globals['_RESENDOTPRESPONSE']._serialized_end=368
  _globals['_LOGINUSERREQUEST']._serialized_start=370
  _globals['_LOGINUSERREQUEST']._serialized_end=439
  _globals['_LOGINRESPONSE']._serialized_start=441
  _globals['_LOGINRESPONSE']._serialized_end=513
  _globals['_LOGINADMINREQUEST']._serialized_start=515
  _globals['_LOGINADMINREQUEST']._serialized_end=567
  _globals['_LOGINADMINRESPONSE']._serialized_start=569
  _globals['_LOGINADMINRESPONSE']._serialized_end=619
  _globals['_USER']._serialized_start=621
  _globals['_USER']._serialized_end=710
  _globals['_USERLISTREQUEST']._serialized_start=712
  _globals['_USERLISTREQUEST']._serialized_end=729
  _globals['_USERLISTRESPONSE']._serialized_start=731
  _globals['_USERLISTRESPONSE']._serialized_end=784
  _globals['_USERSERVICE']._serialized_start=787
  _globals['_USERSERVICE']._serialized_end=1267
# @@protoc_insertion_point(module_scope)
