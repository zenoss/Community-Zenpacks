###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2008-2009 Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

from pysamba.library import *

library.ConnectAndQuery.restype = WERROR
library.IEnumWbemClassObject_SmartNext.restype = WERROR
class com_context(Structure): pass
class IEnumWbemClassObject(Structure): pass

from pysamba.wbem.wbem import *
from twisted.internet import defer
from pysamba.talloc import *
from pysamba.rpc.credentials import *
from pysamba.twisted.callback import Callback, WMIFailure


import Globals
from Products.ZenUtils.Driver import drive

import logging
logging.basicConfig()
log = logging.getLogger('zen.pysamba')

WBEM_S_TIMEDOUT = 0x40004L

WERR_BADFUNC = 1

# struct dcom_client_context *dcom_client_init(struct com_context *ctx,
#         struct cli_credentials *credentials)
library.dcom_client_init.restype = c_void_p
library.dcom_client_init.argtypes = [POINTER(com_context), c_void_p]

class _WbemObject:
    def __getattr__(self, name):
        try:
            return self.__dict__[name.lower()]
        except Exception, ex:
            raise AttributeError(name)

WbemQualifier._fields_ = [
        ('name', CIMSTRING),
        ('flavors', uint8_t),
        ('cimtype', uint32_t),
        ('value', CIMVAR),
        ]

def convertArray(arr):
    if not arr:
        return None
    result = []
    arr = arr.contents
    for i in range(arr.count):
        result.append(arr.item[i])
    return result

def convert(v, typeval):
    if typeval == CIM_SINT8: return v.v_sint8
    if typeval == CIM_UINT8: return v.v_uint8
    if typeval == CIM_SINT16: return v.v_sint16
    if typeval == CIM_UINT16: return v.v_uint16
    if typeval == CIM_SINT32: return v.v_sint32
    if typeval == CIM_UINT32: return v.v_uint32
    if typeval == CIM_SINT64: return v.v_sint64
    if typeval == CIM_UINT64: return v.v_sint64
    if typeval == CIM_REAL32: return float(v.v_uint32)
    if typeval == CIM_REAL64: return float(v.v_uint64)
    if typeval == CIM_BOOLEAN: return bool(v.v_boolean)
    if typeval in (CIM_STRING, CIM_DATETIME, CIM_REFERENCE):
        return v.v_string
    if typeval == CIM_CHAR16:
        return v.v_string.decode('utf16')
    if typeval == CIM_OBJECT:
        return wbemInstanceToPython(v.v_object)
    if typeval == CIM_ARR_SINT8: return convertArray(v.a_sint8)
    if typeval == CIM_ARR_UINT8: return convertArray(v.a_uint8)
    if typeval == CIM_ARR_SINT16: return convertArray(v.a_sint16)
    if typeval == CIM_ARR_UINT16: return convertArray(v.a_uint16)
    if typeval == CIM_ARR_SINT32: return convertArray(v.a_sint32)
    if typeval == CIM_ARR_UINT32: return convertArray(v.a_uint32)
    if typeval == CIM_ARR_SINT64: return convertArray(v.a_sint64)
    if typeval == CIM_ARR_UINT64: return convertArray(v.a_uint64)
    if typeval == CIM_ARR_REAL32: return convertArray(v.a_real32)
    if typeval == CIM_ARR_REAL64: return convertArray(v.a_real64)
    if typeval == CIM_ARR_BOOLEAN: return convertArray(v.a_boolean)
    if typeval == CIM_ARR_STRING: return convertArray(v.a_string)
    if typeval == CIM_ARR_DATETIME:
        return convertArray(v.contents.a_datetime)
    if typeval == CIM_ARR_REFERENCE:
        return convertArray(v.contents.a_reference)
    return "Unsupported"

def wbemInstanceToPython(obj):
    klass = obj.contents.obj_class.contents
    inst = obj.contents.instance.contents
    result = _WbemObject()
    result._class_name = klass.__CLASS
    for j in range(klass.__PROPERTY_COUNT):
        prop = klass.properties[j]
        value = convert(inst.data[j], prop.desc.contents.cimtype & CIM_TYPEMASK)
        if prop.name:
            setattr(result, prop.name.lower(), value)
    return result


def wbemInstanceWithQualifiersToPython(obj):
    klass = obj.contents.obj_class.contents
    inst = obj.contents.instance.contents
    result = _WbemObject()
    kb = []
    result._class_name = klass.__CLASS
    for j in range(klass.__PROPERTY_COUNT):
        vindex = True
        values = None
        prop = klass.properties[j]
        value = convert(inst.data[j], prop.desc.contents.cimtype & CIM_TYPEMASK)
        for q in range(prop.desc.contents.qualifiers.count):
            qualifier = prop.desc.contents.qualifiers.item[q].contents
            qname = qualifier.name
            qvalue = convert(qualifier.value, qualifier.cimtype)
            if qname == 'key' and qvalue == True:
                kb.append("%s=%s"%(prop.name,
                            type(value) is str and '"%s"'%value or value))
            elif qname == 'ValueMap':
                try:
                    if type(value) is list:
                        vindex = [qvalue.index(str(v)) for v in value]
                    else:
                        vindex = qvalue.index(str(value))
                except: vindex = False
            elif qname == 'Values':
                values = qvalue
        if values and vindex:
            if type(vindex) is not int: vindex = value
            if type(value) is list:
                value = [values[v] for v in vindex]
            else:
                value = values[vindex]
        if prop.name:
            setattr(result, prop.name.lower(), value)
    result.__path = "%s:%s.%s"%(obj.contents.__NAMESPACE.replace("\\", '/'),
                                                    klass.__CLASS, ",".join(kb))
    return result

def deferred(ctx):
    cback = Callback()
    ctx.contents.async.fn = cback.callback
    return cback.deferred

wbemTimeoutInfinite = -1

class QueryResult(object):

    def __init__(self, deviceId, ctx, pEnum):
        self._deviceId = deviceId
        self.ctx = ctx
        talloc_increase_ref_count(self.ctx)
        self.pEnum = pEnum

    def close(self):
        if self.ctx:
            talloc_free(self.ctx)
        self.ctx = None

    def __del__(self):
        self.close()


    def fetchSome(self, timeoutMs=wbemTimeoutInfinite, chunkSize=10,
                                                        includeQualifiers=False):
        assert self.pEnum
        def inner(driver):
            count = uint32_t()
            objs = (POINTER(WbemClassObject)*chunkSize)()

            ctx = library.IEnumWbemClassObject_SmartNext_send(
                self.pEnum, None, timeoutMs, chunkSize
                )
            yield deferred(ctx); driver.next()

            result = library.IEnumWbemClassObject_SmartNext_recv(
                ctx, self.ctx, objs, byref(count)
                )

            WERR_CHECK(result, self._deviceId, "Retrieve result data.")

            result = []
            if includeQualifiers:
                for i in range(count.value):
                    result.append(wbemInstanceWithQualifiersToPython(objs[i]))
                    talloc_free(objs[i])
            else:
                for i in range(count.value):
                    result.append(wbemInstanceToPython(objs[i]))
                    talloc_free(objs[i])
            driver.finish(result)
        return drive(inner)


class Query(object):
    def __init__(self):
        self.ctx = POINTER(com_context)()
        self.pWS = POINTER(IWbemServices)()
        self._deviceId = None

    def connect(self, eventContext, deviceId, hostname, creds, namespace="root\\cimv2"):
        self._deviceId = deviceId
        library.com_init_ctx.restype = WERROR
        library.com_init_ctx(byref(self.ctx), eventContext)
        cred = library.cli_credentials_init(self.ctx)
        library.cli_credentials_set_conf(cred)
        library.cli_credentials_parse_string(cred, creds, CRED_SPECIFIED)
        library.dcom_client_init(self.ctx, cred)

        def inner(driver):
            flags = uint32_t()
            flags.value = 0
            ctx = library.WBEM_ConnectServer_send(
                          self.ctx,     # com_ctx
                          None,         # parent_ctx
                          hostname,     # server
                          namespace,    # namespace
                          None,         # username
                          None,         # password
                          None,         # locale
                          flags.value,  # flags
                          None,         # authority 
                          None)         # wbem_ctx 
            yield deferred(ctx); driver.next()
            result = library.WBEM_ConnectServer_recv(ctx, None, byref(self.pWS))
            WERR_CHECK(result, self._deviceId, "Connect")
            driver.finish(None)
        return drive(inner)

    def query(self, query):
        assert self.pWS
        def inner(driver):
            qctx = None
            try:
                qctx = library.IWbemServices_ExecQuery_send_f(
                    self.pWS,
                    self.ctx,
                    "WQL", 
                    query, 
                    WBEM_FLAG_RETURN_IMMEDIATELY | WBEM_FLAG_ENSURE_LOCATABLE, 
                    None)
                yield deferred(qctx); driver.next()
                pEnum = POINTER(IEnumWbemClassObject)()
                result = library.IWbemServices_ExecQuery_recv(qctx,
                                                              byref(pEnum))
                WERR_CHECK(result, self._deviceId, "ExecQuery")
                ctx = library.IEnumWbemClassObject_Reset_send_f(pEnum, self.ctx)
                yield deferred(ctx); driver.next()
                result = library.IEnumWbemClassObject_Reset_recv(ctx);
                WERR_CHECK(result, self._deviceId, "Reset result of WMI query.");
                driver.finish(QueryResult(self._deviceId, self.ctx, pEnum))
            except Exception, ex:
                log.exception(ex)
                raise
        return drive(inner)

    def notificationQuery(self, query):
        assert self.pWS
        def inner(driver):
            qctx = None
            pEnum = None
            try:
                qctx = library.IWbemServices_ExecNotificationQuery_send_f(
                    self.pWS,
                    self.ctx,
                    "WQL", 
                    query, 
                    WBEM_FLAG_RETURN_IMMEDIATELY | WBEM_FLAG_FORWARD_ONLY, 
                    None)
                yield deferred(qctx); driver.next()
                pEnum = POINTER(IEnumWbemClassObject)()

                result = library.IWbemServices_ExecNotificationQuery_recv(
                    qctx, byref(pEnum))
                WERR_CHECK(result, self._deviceId, "ExecNotificationQuery")
                driver.finish(QueryResult(self._deviceId, self.ctx, pEnum))
            except Exception, ex:
                if pEnum:
                    c = library.IUnknown_Release_send_f(pEnum, self.ctx)
                    yield deferred(c); driver.next()
                    result = library.IUnknown_Release_recv(self.ctx)
                    WERR_CHECK(result, self._deviceId, "Release")
                log.exception(ex)
                raise
        return drive(inner)


    def __del__(self):
        self.close()

    def close(self):
        if self.ctx:
            talloc_free(self.ctx)
        self.ctx = None

