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

def create_quantile_accumulator(quantile_accumulator_handle, stamp_token,
                                epsilon, num_quantiles, container=None,
                                shared_name=None, max_elements=None,
                                name=None):
  r"""Creates a stateful accumulator for quantile summaries.

  Args:
    quantile_accumulator_handle: A `Tensor` of type `resource`.
      The handle to the accumulator.
    stamp_token: A `Tensor` of type `int64`.
      Token to use as the initial value of the resource stamp.
    epsilon: A `float`. Error bound on the quantile summary.
    num_quantiles: An `int`. Number of buckets that we create from the data.
    container: An optional `string`. Defaults to `""`.
    shared_name: An optional `string`. Defaults to `""`.
    max_elements: An optional `int`. Defaults to `1099511627776`.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  result = _op_def_lib.apply_op("CreateQuantileAccumulator",
                                quantile_accumulator_handle=quantile_accumulator_handle,
                                stamp_token=stamp_token, epsilon=epsilon,
                                num_quantiles=num_quantiles,
                                container=container, shared_name=shared_name,
                                max_elements=max_elements, name=name)
  return result


_ops.RegisterShape("CreateQuantileAccumulator")(None)

_make_quantile_summaries_outputs = ["dense_summaries", "sparse_summaries"]
_MakeQuantileSummariesOutput = _collections.namedtuple(
    "MakeQuantileSummaries", _make_quantile_summaries_outputs)


def make_quantile_summaries(dense_float_features,
                            sparse_float_feature_indices,
                            sparse_float_feature_values,
                            sparse_float_feature_shapes, example_weights,
                            epsilon, name=None):
  r"""Creates a summary for the given features.

  Args:
    dense_float_features: A list of `Tensor` objects with type `float32`.
      A list of vectors which contains dense values.
    sparse_float_feature_indices: A list of `Tensor` objects with type `int64`.
      List of rank 2 tensors containing the sparse float
      feature indices.
    sparse_float_feature_values: A list with the same length as `sparse_float_feature_indices` of `Tensor` objects with type `float32`.
      List of rank 1 tensors containing the sparse float
      feature values.
    sparse_float_feature_shapes: A list with the same length as `sparse_float_feature_indices` of `Tensor` objects with type `int64`.
      List of rank 1 tensors containing the shape of the
      float feature.
    example_weights: A `Tensor` of type `float32`.
      Rank 2 (N, 1) tensor of per-example weights. Should match
      dense and sparse features shape.
    epsilon: A `float`. Error bound on the computed summary.
    name: A name for the operation (optional).

  Returns:
    A tuple of `Tensor` objects (dense_summaries, sparse_summaries).

    dense_summaries: A list with the same length as `dense_float_features` of `Tensor` objects with type `string`. A list of serialized QuantileSummaryState for dense columns.
    sparse_summaries: A list with the same length as `sparse_float_feature_indices` of `Tensor` objects with type `string`. A list of serialized QuantileSummaryState for sparse columns.
  """
  result = _op_def_lib.apply_op("MakeQuantileSummaries",
                                dense_float_features=dense_float_features,
                                sparse_float_feature_indices=sparse_float_feature_indices,
                                sparse_float_feature_values=sparse_float_feature_values,
                                sparse_float_feature_shapes=sparse_float_feature_shapes,
                                example_weights=example_weights,
                                epsilon=epsilon, name=name)
  return _MakeQuantileSummariesOutput._make(result)


_ops.RegisterShape("MakeQuantileSummaries")(None)

def quantile_accumulator_add_summaries(quantile_accumulator_handles,
                                       stamp_token, summaries, name=None):
  r"""Adds each quantile summary to its stream.

  Args:
    quantile_accumulator_handles: A list of at least 1 `Tensor` objects with type `resource`.
      The handles to the quantile stream resources.
    stamp_token: A `Tensor` of type `int64`.
      Stamp token to validate the Read/Write operation.
    summaries: A list with the same length as `quantile_accumulator_handles` of `Tensor` objects with type `string`.
      A list of serialized QuantileSummaryState.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  result = _op_def_lib.apply_op("QuantileAccumulatorAddSummaries",
                                quantile_accumulator_handles=quantile_accumulator_handles,
                                stamp_token=stamp_token, summaries=summaries,
                                name=name)
  return result


_ops.RegisterShape("QuantileAccumulatorAddSummaries")(None)

def quantile_accumulator_deserialize(quantile_accumulator_handle, stamp_token,
                                     stream_state, are_buckets_ready, buckets,
                                     name=None):
  r"""Serializes the state of the given resource.

  Args:
    quantile_accumulator_handle: A `Tensor` of type `resource`.
      The handle to the accumulator.
    stamp_token: A `Tensor` of type `int64`.
      Stamp token for Read/Write operations.
      Any operation with a mismatching token will be dropped.
    stream_state: A `Tensor` of type `string`.
      A serialized QuantileStreamState.
    are_buckets_ready: A `Tensor` of type `bool`.
      Whether the buckets are ready or not.
    buckets: A `Tensor` of type `float32`.
      Output quantile summary representing boundaries with "num_quantile"
      elements.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  result = _op_def_lib.apply_op("QuantileAccumulatorDeserialize",
                                quantile_accumulator_handle=quantile_accumulator_handle,
                                stamp_token=stamp_token,
                                stream_state=stream_state,
                                are_buckets_ready=are_buckets_ready,
                                buckets=buckets, name=name)
  return result


_ops.RegisterShape("QuantileAccumulatorDeserialize")(None)

def quantile_accumulator_flush(quantile_accumulator_handle, stamp_token,
                               next_stamp_token, name=None):
  r"""Resets quantile summary streams for each column with a new token.

  Args:
    quantile_accumulator_handle: A `Tensor` of type `resource`.
      The handle to the accumulator.
    stamp_token: A `Tensor` of type `int64`.
      Stamp token for Read/Write operations.
      Any operation with a mismatching token will be dropped.
    next_stamp_token: A `Tensor` of type `int64`.
      Stamp token to be used for the next iteration.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  result = _op_def_lib.apply_op("QuantileAccumulatorFlush",
                                quantile_accumulator_handle=quantile_accumulator_handle,
                                stamp_token=stamp_token,
                                next_stamp_token=next_stamp_token, name=name)
  return result


_ops.RegisterShape("QuantileAccumulatorFlush")(None)

_quantile_accumulator_get_buckets_outputs = ["are_buckets_ready", "buckets"]
_QuantileAccumulatorGetBucketsOutput = _collections.namedtuple(
    "QuantileAccumulatorGetBuckets",
    _quantile_accumulator_get_buckets_outputs)


def quantile_accumulator_get_buckets(quantile_accumulator_handles,
                                     stamp_token, name=None):
  r"""Returns quantile buckets created during previous flush of the accumulator.

  Args:
    quantile_accumulator_handles: A list of at least 1 `Tensor` objects with type `resource`.
      The handles to the quantile stream resources.
    stamp_token: A `Tensor` of type `int64`.
      Stamp token to validate the Read/Write operation.
    name: A name for the operation (optional).

  Returns:
    A tuple of `Tensor` objects (are_buckets_ready, buckets).

    are_buckets_ready: A list with the same length as `quantile_accumulator_handles` of `Tensor` objects with type `bool`. Whether the buckets are ready or not.
    buckets: A list with the same length as `quantile_accumulator_handles` of `Tensor` objects with type `float32`. Output quantile summary representing boundaries with "num_quantile"
      elements.
  """
  result = _op_def_lib.apply_op("QuantileAccumulatorGetBuckets",
                                quantile_accumulator_handles=quantile_accumulator_handles,
                                stamp_token=stamp_token, name=name)
  return _QuantileAccumulatorGetBucketsOutput._make(result)


_ops.RegisterShape("QuantileAccumulatorGetBuckets")(None)

def quantile_accumulator_is_initialized(quantile_accumulator_handle,
                                        name=None):
  r"""Checks whether a quantile accumulator has been initialized.

  Args:
    quantile_accumulator_handle: A `Tensor` of type `resource`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `bool`.
  """
  result = _op_def_lib.apply_op("QuantileAccumulatorIsInitialized",
                                quantile_accumulator_handle=quantile_accumulator_handle,
                                name=name)
  return result


_ops.RegisterShape("QuantileAccumulatorIsInitialized")(None)

_quantile_accumulator_serialize_outputs = ["stamp_token", "stream_state",
                                          "are_buckets_ready", "buckets"]
_QuantileAccumulatorSerializeOutput = _collections.namedtuple(
    "QuantileAccumulatorSerialize", _quantile_accumulator_serialize_outputs)


def quantile_accumulator_serialize(quantile_accumulator_handle, name=None):
  r"""Serializes the state of the given resource.

  Args:
    quantile_accumulator_handle: A `Tensor` of type `resource`.
      The handle to the accumulator.
    name: A name for the operation (optional).

  Returns:
    A tuple of `Tensor` objects (stamp_token, stream_state, are_buckets_ready, buckets).

    stamp_token: A `Tensor` of type `int64`. Stamp token for Read/Write operations.
      Any operation with a mismatching token will be dropped.
    stream_state: A `Tensor` of type `string`. A serialized QuantileStreamState.
    are_buckets_ready: A `Tensor` of type `bool`. Whether the buckets are ready or not.
    buckets: A `Tensor` of type `float32`. Output quantile buckets representing boundaries with "num_quantile"
      elements.
  """
  result = _op_def_lib.apply_op("QuantileAccumulatorSerialize",
                                quantile_accumulator_handle=quantile_accumulator_handle,
                                name=name)
  return _QuantileAccumulatorSerializeOutput._make(result)


_ops.RegisterShape("QuantileAccumulatorSerialize")(None)

_quantile_buckets_outputs = ["dense_buckets", "sparse_buckets"]
_QuantileBucketsOutput = _collections.namedtuple(
    "QuantileBuckets", _quantile_buckets_outputs)


def quantile_buckets(dense_float_features, sparse_float_feature_indices,
                     sparse_float_feature_values, sparse_float_feature_shapes,
                     example_weights, dense_config, sparse_config, name=None):
  r"""Computes quantile buckets for a given list of dense and sparse features with

  given example weights.

  Args:
    dense_float_features: A list of `Tensor` objects with type `float32`.
      A list of vectors which contains dense values.
    sparse_float_feature_indices: A list of `Tensor` objects with type `int64`.
      List of rank 2 tensors containing the sparse float
      feature indices.
    sparse_float_feature_values: A list with the same length as `sparse_float_feature_indices` of `Tensor` objects with type `float32`.
      List of rank 1 tensors containing the sparse float
      feature values.
    sparse_float_feature_shapes: A list with the same length as `sparse_float_feature_indices` of `Tensor` objects with type `int64`.
      List of rank 1 tensors containing the shape of the
      float feature.
    example_weights: A `Tensor` of type `float32`.
      Rank 1 tensor containing the example weight tensor.
    dense_config: A list of `strings`.
      Config for computing buckets for dense values.
      Each entry is QuantileConfig proto.
    sparse_config: A list of `strings`.
      Config for computing buckets for sparse feature values.
      Each entry is QuantileConfig proto.
    name: A name for the operation (optional).

  Returns:
    A tuple of `Tensor` objects (dense_buckets, sparse_buckets).

    dense_buckets: A list with the same length as `dense_float_features` of `Tensor` objects with type `float32`. Output quantile summary for each dense float tensor
      representing boundaries each with "num_quantile" elements.
    sparse_buckets: A list with the same length as `sparse_float_feature_indices` of `Tensor` objects with type `float32`. Output quantile summary for each sparse float value tensor
      representing boundaries each with "num_quantile" elements.
  """
  result = _op_def_lib.apply_op("QuantileBuckets",
                                dense_float_features=dense_float_features,
                                sparse_float_feature_indices=sparse_float_feature_indices,
                                sparse_float_feature_values=sparse_float_feature_values,
                                sparse_float_feature_shapes=sparse_float_feature_shapes,
                                example_weights=example_weights,
                                dense_config=dense_config,
                                sparse_config=sparse_config, name=name)
  return _QuantileBucketsOutput._make(result)


_ops.RegisterShape("QuantileBuckets")(None)

def quantile_stream_resource_handle_op(container=None, shared_name=None,
                                       name=None):
  r"""Creates a handle to a QuantileStreamResource

  Args:
    container: An optional `string`. Defaults to `""`.
    shared_name: An optional `string`. Defaults to `""`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `resource`.
  """
  result = _op_def_lib.apply_op("QuantileStreamResourceHandleOp",
                                container=container, shared_name=shared_name,
                                name=name)
  return result


_ops.RegisterShape("QuantileStreamResourceHandleOp")(None)

_quantiles_outputs = ["dense_quantiles", "sparse_quantiles"]
_QuantilesOutput = _collections.namedtuple(
    "Quantiles", _quantiles_outputs)


def quantiles(dense_values, sparse_values, dense_buckets, sparse_buckets,
              name=None):
  r"""Computes quantile for each a given list of dense and sparse feature values using

  the given buckets.

  Args:
    dense_values: A list of `Tensor` objects with type `float32`.
      List of rank 1 tensors containing the dense values.
    sparse_values: A list of `Tensor` objects with type `float32`.
      List of rank 1 tensors containing the sparse feature values.
    dense_buckets: A list with the same length as `dense_values` of `Tensor` objects with type `float32`.
      Quantile summary for each of the dense float tensor.
    sparse_buckets: A list with the same length as `sparse_values` of `Tensor` objects with type `float32`.
      Quantile summary for each of the sparse feature float tensor.
    name: A name for the operation (optional).

  Returns:
    A tuple of `Tensor` objects (dense_quantiles, sparse_quantiles).

    dense_quantiles: A list with the same length as `dense_values` of `Tensor` objects with type `int32`. Rank 1 tensors representing associated quantiles for each of
      dense float tensors.
    sparse_quantiles: A list with the same length as `sparse_values` of `Tensor` objects with type `int32`. Rank 1 tensors representing associated quantiles for each of
      the sparse feature tensors.
  """
  result = _op_def_lib.apply_op("Quantiles", dense_values=dense_values,
                                sparse_values=sparse_values,
                                dense_buckets=dense_buckets,
                                sparse_buckets=sparse_buckets, name=name)
  return _QuantilesOutput._make(result)


_ops.RegisterShape("Quantiles")(None)
def _InitOpDefLibrary(op_list_proto_bytes):
  op_list = _op_def_pb2.OpList()
  op_list.ParseFromString(op_list_proto_bytes)
  _op_def_registry.register_op_list(op_list)
  op_def_lib = _op_def_library.OpDefLibrary()
  op_def_lib.add_op_list(op_list)
  return op_def_lib


# op {
#   name: "CreateQuantileAccumulator"
#   input_arg {
#     name: "quantile_accumulator_handle"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "stamp_token"
#     type: DT_INT64
#   }
#   attr {
#     name: "container"
#     type: "string"
#     default_value {
#       s: ""
#     }
#   }
#   attr {
#     name: "shared_name"
#     type: "string"
#     default_value {
#       s: ""
#     }
#   }
#   attr {
#     name: "max_elements"
#     type: "int"
#     default_value {
#       i: 1099511627776
#     }
#   }
#   attr {
#     name: "epsilon"
#     type: "float"
#   }
#   attr {
#     name: "num_quantiles"
#     type: "int"
#   }
#   is_stateful: true
# }
# op {
#   name: "MakeQuantileSummaries"
#   input_arg {
#     name: "dense_float_features"
#     type: DT_FLOAT
#     number_attr: "num_dense_features"
#   }
#   input_arg {
#     name: "sparse_float_feature_indices"
#     type: DT_INT64
#     number_attr: "num_sparse_features"
#   }
#   input_arg {
#     name: "sparse_float_feature_values"
#     type: DT_FLOAT
#     number_attr: "num_sparse_features"
#   }
#   input_arg {
#     name: "sparse_float_feature_shapes"
#     type: DT_INT64
#     number_attr: "num_sparse_features"
#   }
#   input_arg {
#     name: "example_weights"
#     type: DT_FLOAT
#   }
#   output_arg {
#     name: "dense_summaries"
#     type: DT_STRING
#     number_attr: "num_dense_features"
#   }
#   output_arg {
#     name: "sparse_summaries"
#     type: DT_STRING
#     number_attr: "num_sparse_features"
#   }
#   attr {
#     name: "num_dense_features"
#     type: "int"
#     has_minimum: true
#   }
#   attr {
#     name: "num_sparse_features"
#     type: "int"
#     has_minimum: true
#   }
#   attr {
#     name: "epsilon"
#     type: "float"
#   }
# }
# op {
#   name: "QuantileAccumulatorAddSummaries"
#   input_arg {
#     name: "quantile_accumulator_handles"
#     type: DT_RESOURCE
#     number_attr: "num_resource_handles"
#   }
#   input_arg {
#     name: "stamp_token"
#     type: DT_INT64
#   }
#   input_arg {
#     name: "summaries"
#     type: DT_STRING
#     number_attr: "num_resource_handles"
#   }
#   attr {
#     name: "num_resource_handles"
#     type: "int"
#     has_minimum: true
#     minimum: 1
#   }
#   is_stateful: true
# }
# op {
#   name: "QuantileAccumulatorDeserialize"
#   input_arg {
#     name: "quantile_accumulator_handle"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "stamp_token"
#     type: DT_INT64
#   }
#   input_arg {
#     name: "stream_state"
#     type: DT_STRING
#   }
#   input_arg {
#     name: "are_buckets_ready"
#     type: DT_BOOL
#   }
#   input_arg {
#     name: "buckets"
#     type: DT_FLOAT
#   }
#   is_stateful: true
# }
# op {
#   name: "QuantileAccumulatorFlush"
#   input_arg {
#     name: "quantile_accumulator_handle"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "stamp_token"
#     type: DT_INT64
#   }
#   input_arg {
#     name: "next_stamp_token"
#     type: DT_INT64
#   }
#   is_stateful: true
# }
# op {
#   name: "QuantileAccumulatorGetBuckets"
#   input_arg {
#     name: "quantile_accumulator_handles"
#     type: DT_RESOURCE
#     number_attr: "num_resource_handles"
#   }
#   input_arg {
#     name: "stamp_token"
#     type: DT_INT64
#   }
#   output_arg {
#     name: "are_buckets_ready"
#     type: DT_BOOL
#     number_attr: "num_resource_handles"
#   }
#   output_arg {
#     name: "buckets"
#     type: DT_FLOAT
#     number_attr: "num_resource_handles"
#   }
#   attr {
#     name: "num_resource_handles"
#     type: "int"
#     has_minimum: true
#     minimum: 1
#   }
#   is_stateful: true
# }
# op {
#   name: "QuantileAccumulatorIsInitialized"
#   input_arg {
#     name: "quantile_accumulator_handle"
#     type: DT_RESOURCE
#   }
#   output_arg {
#     name: "is_initialized"
#     type: DT_BOOL
#   }
#   is_stateful: true
# }
# op {
#   name: "QuantileAccumulatorSerialize"
#   input_arg {
#     name: "quantile_accumulator_handle"
#     type: DT_RESOURCE
#   }
#   output_arg {
#     name: "stamp_token"
#     type: DT_INT64
#   }
#   output_arg {
#     name: "stream_state"
#     type: DT_STRING
#   }
#   output_arg {
#     name: "are_buckets_ready"
#     type: DT_BOOL
#   }
#   output_arg {
#     name: "buckets"
#     type: DT_FLOAT
#   }
#   is_stateful: true
# }
# op {
#   name: "QuantileBuckets"
#   input_arg {
#     name: "dense_float_features"
#     type: DT_FLOAT
#     number_attr: "num_dense_features"
#   }
#   input_arg {
#     name: "sparse_float_feature_indices"
#     type: DT_INT64
#     number_attr: "num_sparse_features"
#   }
#   input_arg {
#     name: "sparse_float_feature_values"
#     type: DT_FLOAT
#     number_attr: "num_sparse_features"
#   }
#   input_arg {
#     name: "sparse_float_feature_shapes"
#     type: DT_INT64
#     number_attr: "num_sparse_features"
#   }
#   input_arg {
#     name: "example_weights"
#     type: DT_FLOAT
#   }
#   output_arg {
#     name: "dense_buckets"
#     type: DT_FLOAT
#     number_attr: "num_dense_features"
#   }
#   output_arg {
#     name: "sparse_buckets"
#     type: DT_FLOAT
#     number_attr: "num_sparse_features"
#   }
#   attr {
#     name: "num_dense_features"
#     type: "int"
#     has_minimum: true
#   }
#   attr {
#     name: "num_sparse_features"
#     type: "int"
#     has_minimum: true
#   }
#   attr {
#     name: "dense_config"
#     type: "list(string)"
#   }
#   attr {
#     name: "sparse_config"
#     type: "list(string)"
#   }
# }
# op {
#   name: "QuantileStreamResourceHandleOp"
#   output_arg {
#     name: "resource"
#     type: DT_RESOURCE
#   }
#   attr {
#     name: "container"
#     type: "string"
#     default_value {
#       s: ""
#     }
#   }
#   attr {
#     name: "shared_name"
#     type: "string"
#     default_value {
#       s: ""
#     }
#   }
#   is_stateful: true
# }
# op {
#   name: "Quantiles"
#   input_arg {
#     name: "dense_values"
#     type: DT_FLOAT
#     number_attr: "num_dense_features"
#   }
#   input_arg {
#     name: "sparse_values"
#     type: DT_FLOAT
#     number_attr: "num_sparse_features"
#   }
#   input_arg {
#     name: "dense_buckets"
#     type: DT_FLOAT
#     number_attr: "num_dense_features"
#   }
#   input_arg {
#     name: "sparse_buckets"
#     type: DT_FLOAT
#     number_attr: "num_sparse_features"
#   }
#   output_arg {
#     name: "dense_quantiles"
#     type: DT_INT32
#     number_attr: "num_dense_features"
#   }
#   output_arg {
#     name: "sparse_quantiles"
#     type: DT_INT32
#     number_attr: "num_sparse_features"
#   }
#   attr {
#     name: "num_dense_features"
#     type: "int"
#     has_minimum: true
#   }
#   attr {
#     name: "num_sparse_features"
#     type: "int"
#     has_minimum: true
#   }
# }
_op_def_lib = _InitOpDefLibrary(b"\n\312\001\n\031CreateQuantileAccumulator\022\037\n\033quantile_accumulator_handle\030\024\022\017\n\013stamp_token\030\t\"\027\n\tcontainer\022\006string\032\002\022\000\"\031\n\013shared_name\022\006string\032\002\022\000\"\034\n\014max_elements\022\003int\032\007\030\200\200\200\200\200 \"\020\n\007epsilon\022\005float\"\024\n\rnum_quantiles\022\003int\210\001\001\n\236\003\n\025MakeQuantileSummaries\022,\n\024dense_float_features\030\001*\022num_dense_features\0225\n\034sparse_float_feature_indices\030\t*\023num_sparse_features\0224\n\033sparse_float_feature_values\030\001*\023num_sparse_features\0224\n\033sparse_float_feature_shapes\030\t*\023num_sparse_features\022\023\n\017example_weights\030\001\032\'\n\017dense_summaries\030\007*\022num_dense_features\032)\n\020sparse_summaries\030\007*\023num_sparse_features\"\033\n\022num_dense_features\022\003int(\001\"\034\n\023num_sparse_features\022\003int(\001\"\020\n\007epsilon\022\005float\n\263\001\n\037QuantileAccumulatorAddSummaries\0226\n\034quantile_accumulator_handles\030\024*\024num_resource_handles\022\017\n\013stamp_token\030\t\022#\n\tsummaries\030\007*\024num_resource_handles\"\037\n\024num_resource_handles\022\003int(\0010\001\210\001\001\n\213\001\n\036QuantileAccumulatorDeserialize\022\037\n\033quantile_accumulator_handle\030\024\022\017\n\013stamp_token\030\t\022\020\n\014stream_state\030\007\022\025\n\021are_buckets_ready\030\n\022\013\n\007buckets\030\001\210\001\001\ne\n\030QuantileAccumulatorFlush\022\037\n\033quantile_accumulator_handle\030\024\022\017\n\013stamp_token\030\t\022\024\n\020next_stamp_token\030\t\210\001\001\n\334\001\n\035QuantileAccumulatorGetBuckets\0226\n\034quantile_accumulator_handles\030\024*\024num_resource_handles\022\017\n\013stamp_token\030\t\032+\n\021are_buckets_ready\030\n*\024num_resource_handles\032!\n\007buckets\030\001*\024num_resource_handles\"\037\n\024num_resource_handles\022\003int(\0010\001\210\001\001\nZ\n QuantileAccumulatorIsInitialized\022\037\n\033quantile_accumulator_handle\030\024\032\022\n\016is_initialized\030\n\210\001\001\n\211\001\n\034QuantileAccumulatorSerialize\022\037\n\033quantile_accumulator_handle\030\024\032\017\n\013stamp_token\030\t\032\020\n\014stream_state\030\007\032\025\n\021are_buckets_ready\030\n\032\013\n\007buckets\030\001\210\001\001\n\277\003\n\017QuantileBuckets\022,\n\024dense_float_features\030\001*\022num_dense_features\0225\n\034sparse_float_feature_indices\030\t*\023num_sparse_features\0224\n\033sparse_float_feature_values\030\001*\023num_sparse_features\0224\n\033sparse_float_feature_shapes\030\t*\023num_sparse_features\022\023\n\017example_weights\030\001\032%\n\rdense_buckets\030\001*\022num_dense_features\032\'\n\016sparse_buckets\030\001*\023num_sparse_features\"\033\n\022num_dense_features\022\003int(\001\"\034\n\023num_sparse_features\022\003int(\001\"\034\n\014dense_config\022\014list(string)\"\035\n\rsparse_config\022\014list(string)\ne\n\036QuantileStreamResourceHandleOp\032\014\n\010resource\030\024\"\027\n\tcontainer\022\006string\032\002\022\000\"\031\n\013shared_name\022\006string\032\002\022\000\210\001\001\n\270\002\n\tQuantiles\022$\n\014dense_values\030\001*\022num_dense_features\022&\n\rsparse_values\030\001*\023num_sparse_features\022%\n\rdense_buckets\030\001*\022num_dense_features\022\'\n\016sparse_buckets\030\001*\023num_sparse_features\032\'\n\017dense_quantiles\030\003*\022num_dense_features\032)\n\020sparse_quantiles\030\003*\023num_sparse_features\"\033\n\022num_dense_features\022\003int(\001\"\034\n\023num_sparse_features\022\003int(\001")
