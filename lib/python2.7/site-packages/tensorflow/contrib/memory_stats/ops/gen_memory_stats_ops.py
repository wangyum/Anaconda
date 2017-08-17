"""Python wrappers around TensorFlow ops.

This file is MACHINE GENERATED! Do not edit.
"""

import collections as _collections

from tensorflow.core.framework import op_def_pb2 as _op_def_pb2

# Needed to trigger the call to _set_call_cpp_shape_fn.
from tensorflow.python.framework import common_shapes as _common_shapes

from tensorflow.python.framework import op_def_registry as _op_def_registry
from tensorflow.python.framework import ops as _ops
from tensorflow.python.framework import op_def_library as _op_def_library

def bytes_limit(name=None):
  r"""TODO: add doc.

  Args:
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `int64`.
  """
  result = _op_def_lib.apply_op("BytesLimit", name=name)
  return result


_ops.RegisterShape("BytesLimit")(None)

def max_bytes_in_use(name=None):
  r"""TODO: add doc.

  Args:
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `int64`.
  """
  result = _op_def_lib.apply_op("MaxBytesInUse", name=name)
  return result


_ops.RegisterShape("MaxBytesInUse")(None)
def _InitOpDefLibrary(op_list_proto_bytes):
  op_list = _op_def_pb2.OpList()
  op_list.ParseFromString(op_list_proto_bytes)
  _op_def_registry.register_op_list(op_list)
  op_def_lib = _op_def_library.OpDefLibrary()
  op_def_lib.add_op_list(op_list)
  return op_def_lib


# op {
#   name: "BytesLimit"
#   output_arg {
#     name: "out"
#     type: DT_INT64
#   }
#   is_stateful: true
# }
# op {
#   name: "MaxBytesInUse"
#   output_arg {
#     name: "out"
#     type: DT_INT64
#   }
#   is_stateful: true
# }
_op_def_lib = _InitOpDefLibrary(b"\n\030\n\nBytesLimit\032\007\n\003out\030\t\210\001\001\n\033\n\rMaxBytesInUse\032\007\n\003out\030\t\210\001\001")
