#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

import codec
from cStringIO import StringIO
from spec import load, pythonize
from codec import EOF

class Frame:

  METHOD = "frame_method"
  HEADER = "frame_header"
  BODY = "frame_body"
  OOB_METHOD = "frame_oob_method"
  OOB_HEADER = "frame_oob_header"
  OOB_BODY = "frame_oob_body"
  TRACE = "frame_trace"
  HEARTBEAT = "frame_heartbeat"

  DECODERS = {}

  def __init__(self, channel, payload):
    self.channel = channel
    self.payload = payload

  def __str__(self):
    return "[%d] %s" % (self.channel, self.payload)

class Payload:

  class __metaclass__(type):

    def __new__(cls, name, bases, dict):
      for req in ("encode", "decode", "type"):
        if not dict.has_key(req):
          raise TypeError("%s must define %s" % (name, req))
      dict["decode"] = staticmethod(dict["decode"])
      t = type.__new__(cls, name, bases, dict)
      if t.type != None:
        Frame.DECODERS[t.type] = t
      return t

  type = None

  def encode(self, enc): abstract

  def decode(spec, dec): abstract

class Method(Payload):

  type = Frame.METHOD

  def __init__(self, method, *args):
    if len(args) != len(method.fields):
      argspec = ["%s: %s" % (pythonize(f.name), f.type)
                 for f in method.fields]
      raise TypeError("%s.%s expecting (%s), got %s" %
                      (pythonize(method.klass.name),
                       pythonize(method.name), ", ".join(argspec), args))
    self.method = method
    self.args = args

  def encode(self, enc):
    buf = StringIO()
    c = codec.Codec(buf)
    c.encode_short(self.method.klass.id)
    c.encode_short(self.method.id)
    for field, arg in zip(self.method.fields, self.args):
      c.encode(field.type, arg)
    c.flush()
    enc.encode_longstr(buf.getvalue())

  def decode(spec, dec):
    enc = dec.decode_longstr()
    c = codec.Codec(StringIO(enc))
    klass = spec.classes.byid[c.decode_short()]
    meth = klass.methods.byid[c.decode_short()]
    args = tuple([c.decode(f.type) for f in meth.fields])
    return Method(meth, *args)

  def __str__(self):
    return "%s %s" % (self.method, ", ".join([str(a) for a in self.args]))

class Header(Payload):

  type = Frame.HEADER

  def __init__(self, klass, weight, size, **properties):
    self.klass = klass
    self.weight = weight
    self.size = size
    self.properties = properties

  def __getitem__(self, name):
    return self.properties[name]

  def __setitem__(self, name, value):
    self.properties[name] = value

  def __delitem__(self, name):
    del self.properties[name]

  def encode(self, enc):
    buf = StringIO()
    c = codec.Codec(buf)
    c.encode_short(self.klass.id)
    c.encode_short(self.weight)
    c.encode_longlong(self.size)

    # property flags
    nprops = len(self.klass.fields)
    flags = 0
    for i in range(nprops):
      f = self.klass.fields.items[i]
      flags <<= 1
      if self.properties.get(f.name) != None:
        flags |= 1
      # the last bit indicates more flags
      if i > 0 and (i % 15) == 0:
        flags <<= 1
        if nprops > (i + 1):
          flags |= 1
          c.encode_short(flags)
          flags = 0
    flags <<= ((16 - (nprops % 15)) % 16)
    c.encode_short(flags)

    # properties
    for f in self.klass.fields:
      v = self.properties.get(f.name)
      if v != None:
        c.encode(f.type, v)
    c.flush()
    enc.encode_longstr(buf.getvalue())

  def decode(spec, dec):
    c = codec.Codec(StringIO(dec.decode_longstr()))
    klass = spec.classes.byid[c.decode_short()]
    weight = c.decode_short()
    size = c.decode_longlong()

    # property flags
    bits = []
    while True:
      flags = c.decode_short()
      for i in range(15, 0, -1):
        if flags >> i & 0x1 != 0:
          bits.append(True)
        else:
          bits.append(False)
      if flags & 0x1 == 0:
        break

    # properties
    properties = {}
    for b, f in zip(bits, klass.fields):
      if b:
        # Note: decode returns a unicode u'' string but only
        # plain '' strings can be used as keywords so we need to
        # stringify the names.
        properties[str(f.name)] = c.decode(f.type)
    return Header(klass, weight, size, **properties)

  def __str__(self):
    return "%s %s %s %s" % (self.klass, self.weight, self.size,
                            self.properties)

class Body(Payload):

  type = Frame.BODY

  def __init__(self, content):
    self.content = content

  def encode(self, enc):
    enc.encode_longstr(self.content)

  def decode(spec, dec):
    return Body(dec.decode_longstr())

  def __str__(self):
    return "Body(%r)" % self.content

class Heartbeat(Payload):
  type = Frame.HEARTBEAT
  def __str__(self):
    return "Heartbeat()"

  def encode(self, enc):
    enc.encode_long(0)

  def decode(spec, dec):
    dec.decode_long()
    return Heartbeat()
