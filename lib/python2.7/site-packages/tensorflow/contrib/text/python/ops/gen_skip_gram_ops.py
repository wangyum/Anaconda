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

_skip_gram_generate_candidates_outputs = ["tokens", "labels"]
_SkipGramGenerateCandidatesOutput = _collections.namedtuple(
    "SkipGramGenerateCandidates", _skip_gram_generate_candidates_outputs)


def skip_gram_generate_candidates(input_tensor, min_skips, max_skips, start,
                                  limit, emit_self_as_target, seed=None,
                                  seed2=None, name=None):
  r"""Generates skip-gram token and label paired Tensors from the input tensor.

  See docs for the public-facing skip_gram_sample() Python op for more details.

  Args:
    input_tensor: A `Tensor`.
    min_skips: A `Tensor` of type `int32`.
    max_skips: A `Tensor` of type `int32`.
    start: A `Tensor` of type `int32`.
    limit: A `Tensor` of type `int32`.
    emit_self_as_target: A `Tensor` of type `bool`.
    seed: An optional `int`. Defaults to `0`.
    seed2: An optional `int`. Defaults to `0`.
    name: A name for the operation (optional).

  Returns:
    A tuple of `Tensor` objects (tokens, labels).

    tokens: A `Tensor`. Has the same type as `input_tensor`.
    labels: A `Tensor`. Has the same type as `input_tensor`.
  """
  result = _op_def_lib.apply_op("SkipGramGenerateCandidates",
                                input_tensor=input_tensor,
                                min_skips=min_skips, max_skips=max_skips,
                                start=start, limit=limit,
                                emit_self_as_target=emit_self_as_target,
                                seed=seed, seed2=seed2, name=name)
  return _SkipGramGenerateCandidatesOutput._make(result)


_ops.RegisterShape("SkipGramGenerateCandidates")(None)
def _InitOpDefLibrary(op_list_proto_bytes):
  op_list = _op_def_pb2.OpList()
  op_list.ParseFromString(op_list_proto_bytes)
  _op_def_registry.register_op_list(op_list)
  op_def_lib = _op_def_library.OpDefLibrary()
  op_def_lib.add_op_list(op_list)
  return op_def_lib


# op {
#   name: "SkipGramGenerateCandidates"
#   input_arg {
#     name: "input_tensor"
#     type_attr: "T"
#   }
#   input_arg {
#     name: "min_skips"
#     type: DT_INT32
#   }
#   input_arg {
#     name: "max_skips"
#     type: DT_INT32
#   }
#   input_arg {
#     name: "start"
#     type: DT_INT32
#   }
#   input_arg {
#     name: "limit"
#     type: DT_INT32
#   }
#   input_arg {
#     name: "emit_self_as_target"
#     type: DT_BOOL
#   }
#   output_arg {
#     name: "tokens"
#     type_attr: "T"
#   }
#   output_arg {
#     name: "labels"
#     type_attr: "T"
#   }
#   attr {
#     name: "T"
#     type: "type"
#   }
#   attr {
#     name: "seed"
#     type: "int"
#     default_value {
#       i: 0
#     }
#   }
#   attr {
#     name: "seed2"
#     type: "int"
#     default_value {
#       i: 0
#     }
#   }
#   is_stateful: true
# }
_op_def_lib = _InitOpDefLibrary(b"\n\307\001\n\032SkipGramGenerateCandidates\022\021\n\014input_tensor\"\001T\022\r\n\tmin_skips\030\003\022\r\n\tmax_skips\030\003\022\t\n\005start\030\003\022\t\n\005limit\030\003\022\027\n\023emit_self_as_target\030\n\032\013\n\006tokens\"\001T\032\013\n\006labels\"\001T\"\t\n\001T\022\004type\"\017\n\004seed\022\003int\032\002\030\000\"\020\n\005seed2\022\003int\032\002\030\000\210\001\001")
