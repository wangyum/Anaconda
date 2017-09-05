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

def create_stats_accumulator_scalar(stats_accumulator_handle, stamp_token,
                                    name=None):
  r"""Creates a scalar stats accumulator.

  Args:
    stats_accumulator_handle: A `Tensor` of type `resource`.
      handle to the stats accumulator.
    stamp_token: A `Tensor` of type `int64`.
      Token to use as the initial value of the resource stamp.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  result = _op_def_lib.apply_op("CreateStatsAccumulatorScalar",
                                stats_accumulator_handle=stats_accumulator_handle,
                                stamp_token=stamp_token, name=name)
  return result


_ops.RegisterShape("CreateStatsAccumulatorScalar")(None)

def create_stats_accumulator_tensor(stats_accumulator_handle, stamp_token,
                                    per_slot_gradient_shape,
                                    per_slot_hessian_shape, name=None):
  r"""Creates a tensor stats accumulator.

  Args:
    stats_accumulator_handle: A `Tensor` of type `resource`.
      handle to the tree ensemble resource to be created.
    stamp_token: A `Tensor` of type `int64`.
      Token to use as the initial value of the resource stamp.
    per_slot_gradient_shape: A `Tensor` of type `int64`.
      a vector that defines the shape of gradients.
    per_slot_hessian_shape: A `Tensor` of type `int64`.
      a vector that defines the shape of hessians.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  result = _op_def_lib.apply_op("CreateStatsAccumulatorTensor",
                                stats_accumulator_handle=stats_accumulator_handle,
                                stamp_token=stamp_token,
                                per_slot_gradient_shape=per_slot_gradient_shape,
                                per_slot_hessian_shape=per_slot_hessian_shape,
                                name=name)
  return result


_ops.RegisterShape("CreateStatsAccumulatorTensor")(None)

def stats_accumulator_scalar_add(stats_accumulator_handles, stamp_token,
                                 partition_ids, feature_ids, gradients,
                                 hessians, name=None):
  r"""Updates the scalar stats accumulator.

  Args:
    stats_accumulator_handles: A list of at least 1 `Tensor` objects with type `resource`.
      A list of handles to the stats accumulator.
    stamp_token: A `Tensor` of type `int64`.
      Stamp token for Read/Write operations.
      Any operation with a mismatching token will be dropped.
    partition_ids: A list with the same length as `stats_accumulator_handles` of `Tensor` objects with type `int32`.
      A list of vectors of partition_ids.
    feature_ids: A list with the same length as `stats_accumulator_handles` of `Tensor` objects with type `int64`.
      A list of vectors of feature_ids.
    gradients: A list with the same length as `stats_accumulator_handles` of `Tensor` objects with type `float32`.
      A list of vectors of gradients for each slot in
      <partition_id, feature_id>.
    hessians: A list with the same length as `stats_accumulator_handles` of `Tensor` objects with type `float32`.
      A list of vectors of hessians for each slot in
      <partition_id, feature_id>.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  result = _op_def_lib.apply_op("StatsAccumulatorScalarAdd",
                                stats_accumulator_handles=stats_accumulator_handles,
                                stamp_token=stamp_token,
                                partition_ids=partition_ids,
                                feature_ids=feature_ids, gradients=gradients,
                                hessians=hessians, name=name)
  return result


_ops.RegisterShape("StatsAccumulatorScalarAdd")(None)

def stats_accumulator_scalar_deserialize(stats_accumulator_handle,
                                         stamp_token, num_updates,
                                         partition_ids, feature_ids,
                                         gradients, hessians, name=None):
  r"""Resets the scalar stats accumulator with the serialized state.

  Args:
    stats_accumulator_handle: A `Tensor` of type `resource`.
      handle to the stats accumulator.
    stamp_token: A `Tensor` of type `int64`.
      Stamp token for Read/Write operations.
      Any operation with a mismatching token will be dropped.
    num_updates: A `Tensor` of type `int64`.
      Number of times stats were added to this accumulator since last
      flush.
    partition_ids: A `Tensor` of type `int32`. A vector of partition_ids.
    feature_ids: A `Tensor` of type `int64`. A vector of feature_ids.
    gradients: A `Tensor` of type `float32`.
      A vector of gradients for each slot in <partition_id, feature_id>.
    hessians: A `Tensor` of type `float32`.
      A vector of hessians for each slot in <partition_id, feature_id>.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  result = _op_def_lib.apply_op("StatsAccumulatorScalarDeserialize",
                                stats_accumulator_handle=stats_accumulator_handle,
                                stamp_token=stamp_token,
                                num_updates=num_updates,
                                partition_ids=partition_ids,
                                feature_ids=feature_ids, gradients=gradients,
                                hessians=hessians, name=name)
  return result


_ops.RegisterShape("StatsAccumulatorScalarDeserialize")(None)

_stats_accumulator_scalar_flush_outputs = ["num_updates",
                                          "output_partition_ids",
                                          "output_feature_ids",
                                          "output_gradients",
                                          "output_hessians"]
_StatsAccumulatorScalarFlushOutput = _collections.namedtuple(
    "StatsAccumulatorScalarFlush", _stats_accumulator_scalar_flush_outputs)


def stats_accumulator_scalar_flush(stats_accumulator_handle, stamp_token,
                                   next_stamp_token, name=None):
  r"""Flushes the scalar stats accumulator to output and resets the internal state.

  Args:
    stats_accumulator_handle: A `Tensor` of type `resource`.
      handle to the stats accumulator.
    stamp_token: A `Tensor` of type `int64`.
      Stamp token for Read/Write operations.
      Any operation with a mismatching token will be dropped.
    next_stamp_token: A `Tensor` of type `int64`.
      Stamp token for the next iteration.
    name: A name for the operation (optional).

  Returns:
    A tuple of `Tensor` objects (num_updates, output_partition_ids, output_feature_ids, output_gradients, output_hessians).

    num_updates: A `Tensor` of type `int64`. Number of times stats were added to this accumulator since last
          flush.
      output_partition_ids A vector of partition_ids for the slots.
    output_partition_ids: A `Tensor` of type `int32`.
    output_feature_ids: A `Tensor` of type `int64`. A vector of feature_ids for the slots.
    output_gradients: A `Tensor` of type `float32`. A vector of gradients, with a value for each slot
      in <output_partition_id, output_feature_id>.
    output_hessians: A `Tensor` of type `float32`. A vector of hessians, with a value for each slot
      in <output_partition_id, output_feature_id>.
  """
  result = _op_def_lib.apply_op("StatsAccumulatorScalarFlush",
                                stats_accumulator_handle=stats_accumulator_handle,
                                stamp_token=stamp_token,
                                next_stamp_token=next_stamp_token, name=name)
  return _StatsAccumulatorScalarFlushOutput._make(result)


_ops.RegisterShape("StatsAccumulatorScalarFlush")(None)

def stats_accumulator_scalar_is_initialized(stats_accumulator_handle,
                                            name=None):
  r"""Checks whether a stats accumulator has been initialized.

  Args:
    stats_accumulator_handle: A `Tensor` of type `resource`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `bool`.
  """
  result = _op_def_lib.apply_op("StatsAccumulatorScalarIsInitialized",
                                stats_accumulator_handle=stats_accumulator_handle,
                                name=name)
  return result


_ops.RegisterShape("StatsAccumulatorScalarIsInitialized")(None)

_stats_accumulator_scalar_make_summary_outputs = ["output_partition_ids",
                                                 "output_feature_ids",
                                                 "output_gradients",
                                                 "output_hessians"]
_StatsAccumulatorScalarMakeSummaryOutput = _collections.namedtuple(
    "StatsAccumulatorScalarMakeSummary",
    _stats_accumulator_scalar_make_summary_outputs)


def stats_accumulator_scalar_make_summary(partition_ids, feature_ids,
                                          gradients, hessians, name=None):
  r"""TODO: add doc.

  Args:
    partition_ids: A `Tensor` of type `int32`.
    feature_ids: A `Tensor` of type `int64`.
    gradients: A `Tensor` of type `float32`.
    hessians: A `Tensor` of type `float32`.
    name: A name for the operation (optional).

  Returns:
    A tuple of `Tensor` objects (output_partition_ids, output_feature_ids, output_gradients, output_hessians).

    output_partition_ids: A `Tensor` of type `int32`.
    output_feature_ids: A `Tensor` of type `int64`.
    output_gradients: A `Tensor` of type `float32`.
    output_hessians: A `Tensor` of type `float32`.
  """
  result = _op_def_lib.apply_op("StatsAccumulatorScalarMakeSummary",
                                partition_ids=partition_ids,
                                feature_ids=feature_ids, gradients=gradients,
                                hessians=hessians, name=name)
  return _StatsAccumulatorScalarMakeSummaryOutput._make(result)


_ops.RegisterShape("StatsAccumulatorScalarMakeSummary")(None)

def stats_accumulator_scalar_resource_handle_op(container=None,
                                                shared_name=None, name=None):
  r"""Creates a handle to a StatsAccumulatorScalarResource

  Args:
    container: An optional `string`. Defaults to `""`.
    shared_name: An optional `string`. Defaults to `""`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `resource`.
  """
  result = _op_def_lib.apply_op("StatsAccumulatorScalarResourceHandleOp",
                                container=container, shared_name=shared_name,
                                name=name)
  return result


_ops.RegisterShape("StatsAccumulatorScalarResourceHandleOp")(None)

_stats_accumulator_scalar_serialize_outputs = ["stamp_token", "num_updates",
                                              "output_partition_ids",
                                              "output_feature_ids",
                                              "output_gradients",
                                              "output_hessians"]
_StatsAccumulatorScalarSerializeOutput = _collections.namedtuple(
    "StatsAccumulatorScalarSerialize",
    _stats_accumulator_scalar_serialize_outputs)


def stats_accumulator_scalar_serialize(stats_accumulator_handle, name=None):
  r"""Serializes the scalar stats accumulator state.

  Args:
    stats_accumulator_handle: A `Tensor` of type `resource`.
      handle to the stats accumulator.
    name: A name for the operation (optional).

  Returns:
    A tuple of `Tensor` objects (stamp_token, num_updates, output_partition_ids, output_feature_ids, output_gradients, output_hessians).

    stamp_token: A `Tensor` of type `int64`. The current stamp token for the resource.
    num_updates: A `Tensor` of type `int64`. Number of times stats were added to this accumulator since last
          flush.
      output_partition_ids A vector of partition_ids for the slots.
    output_partition_ids: A `Tensor` of type `int32`.
    output_feature_ids: A `Tensor` of type `int64`. A vector of feature_ids for the slots.
    output_gradients: A `Tensor` of type `float32`. A vector of gradients, with a value for each slot
      in <output_partition_id, output_feature_id>.
    output_hessians: A `Tensor` of type `float32`. A vector of hessians, with a value for each slot
      in <output_partition_id, output_feature_id>.
  """
  result = _op_def_lib.apply_op("StatsAccumulatorScalarSerialize",
                                stats_accumulator_handle=stats_accumulator_handle,
                                name=name)
  return _StatsAccumulatorScalarSerializeOutput._make(result)


_ops.RegisterShape("StatsAccumulatorScalarSerialize")(None)

def stats_accumulator_tensor_add(stats_accumulator_handles, stamp_token,
                                 partition_ids, feature_ids, gradients,
                                 hessians, name=None):
  r"""Updates the tensor stats accumulator.

  Args:
    stats_accumulator_handles: A list of at least 1 `Tensor` objects with type `resource`.
      A list of handles to the stats accumulator.
    stamp_token: A `Tensor` of type `int64`.
      Stamp token for Read/Write operations.
      Any operation with a mismatching token will be dropped.
    partition_ids: A list with the same length as `stats_accumulator_handles` of `Tensor` objects with type `int32`.
      A list of vectors of partition_ids.
    feature_ids: A list with the same length as `stats_accumulator_handles` of `Tensor` objects with type `int64`.
      A list of vectors of feature_ids.
    gradients: A list with the same length as `stats_accumulator_handles` of `Tensor` objects with type `float32`.
      A list of vectors of gradients for each slot in
      <partition_id, feature_id>.
    hessians: A list with the same length as `stats_accumulator_handles` of `Tensor` objects with type `float32`.
      A list of vectors of hessians for each slot in
      <partition_id, feature_id>.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  result = _op_def_lib.apply_op("StatsAccumulatorTensorAdd",
                                stats_accumulator_handles=stats_accumulator_handles,
                                stamp_token=stamp_token,
                                partition_ids=partition_ids,
                                feature_ids=feature_ids, gradients=gradients,
                                hessians=hessians, name=name)
  return result


_ops.RegisterShape("StatsAccumulatorTensorAdd")(None)

def stats_accumulator_tensor_deserialize(stats_accumulator_handle,
                                         stamp_token, num_updates,
                                         partition_ids, feature_ids,
                                         gradients, hessians, name=None):
  r"""Resets the tensor stats accumulator with the serialized state.

  Args:
    stats_accumulator_handle: A `Tensor` of type `resource`.
      handle to the tree ensemble resource to be created.
    stamp_token: A `Tensor` of type `int64`.
      Stamp token for Read/Write operations.
      Any operation with a mismatching token will be dropped.
    num_updates: A `Tensor` of type `int64`.
      Number of times stats were added to this accumulator since last
      flush.
    partition_ids: A `Tensor` of type `int32`. A vector of partition_ids.
    feature_ids: A `Tensor` of type `int64`. A vector of feature_ids.
    gradients: A `Tensor` of type `float32`.
      A vector of gradients for each slot in <partition_id, feature_id>.
    hessians: A `Tensor` of type `float32`.
      A vector of hessians for each slot in <partition_id, feature_id>.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  result = _op_def_lib.apply_op("StatsAccumulatorTensorDeserialize",
                                stats_accumulator_handle=stats_accumulator_handle,
                                stamp_token=stamp_token,
                                num_updates=num_updates,
                                partition_ids=partition_ids,
                                feature_ids=feature_ids, gradients=gradients,
                                hessians=hessians, name=name)
  return result


_ops.RegisterShape("StatsAccumulatorTensorDeserialize")(None)

_stats_accumulator_tensor_flush_outputs = ["num_updates",
                                          "output_partition_ids",
                                          "output_feature_ids",
                                          "output_gradients",
                                          "output_hessians"]
_StatsAccumulatorTensorFlushOutput = _collections.namedtuple(
    "StatsAccumulatorTensorFlush", _stats_accumulator_tensor_flush_outputs)


def stats_accumulator_tensor_flush(stats_accumulator_handle, stamp_token,
                                   next_stamp_token, name=None):
  r"""Flushes the stats accumulator to output and resets the internal state.

  Args:
    stats_accumulator_handle: A `Tensor` of type `resource`.
      handle to the tree ensemble resource to be created.
    stamp_token: A `Tensor` of type `int64`.
      Stamp token for Read/Write operations.
      Any operation with a mismatching token will be dropped.
    next_stamp_token: A `Tensor` of type `int64`.
      Stamp token to be used for the next iteration.
    name: A name for the operation (optional).

  Returns:
    A tuple of `Tensor` objects (num_updates, output_partition_ids, output_feature_ids, output_gradients, output_hessians).

    num_updates: A `Tensor` of type `int64`. Number of times stats were added to this accumulator since last
      flush.
    output_partition_ids: A `Tensor` of type `int32`. A vector of partition_ids for the slots.
    output_feature_ids: A `Tensor` of type `int64`. A vector of feature_ids for the slots.
    output_gradients: A `Tensor` of type `float32`. A tensor of gradients, first dimension matches slots
      in <partition_id, feature_id>.
    output_hessians: A `Tensor` of type `float32`. A tensor of hessians, first dimension matches slots
      in <partition_id, feature_id>.
  """
  result = _op_def_lib.apply_op("StatsAccumulatorTensorFlush",
                                stats_accumulator_handle=stats_accumulator_handle,
                                stamp_token=stamp_token,
                                next_stamp_token=next_stamp_token, name=name)
  return _StatsAccumulatorTensorFlushOutput._make(result)


_ops.RegisterShape("StatsAccumulatorTensorFlush")(None)

def stats_accumulator_tensor_is_initialized(stats_accumulator_handle,
                                            name=None):
  r"""Checks whether a tensor stats accumulator has been initialized.

  Args:
    stats_accumulator_handle: A `Tensor` of type `resource`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `bool`.
  """
  result = _op_def_lib.apply_op("StatsAccumulatorTensorIsInitialized",
                                stats_accumulator_handle=stats_accumulator_handle,
                                name=name)
  return result


_ops.RegisterShape("StatsAccumulatorTensorIsInitialized")(None)

_stats_accumulator_tensor_make_summary_outputs = ["output_partition_ids",
                                                 "output_feature_ids",
                                                 "output_gradients",
                                                 "output_hessians"]
_StatsAccumulatorTensorMakeSummaryOutput = _collections.namedtuple(
    "StatsAccumulatorTensorMakeSummary",
    _stats_accumulator_tensor_make_summary_outputs)


def stats_accumulator_tensor_make_summary(partition_ids, feature_ids,
                                          gradients, hessians, name=None):
  r"""Summarizes the stats by summing the <gradients, hessians> that are for the same

  <partition_id, feature_id>.

  Args:
    partition_ids: A `Tensor` of type `int32`. A vector of partition_ids.
    feature_ids: A `Tensor` of type `int64`. A vector of feature_ids.
    gradients: A `Tensor` of type `float32`.
      A vector of gradients for each slot in <partition_id, feature_id>.
    hessians: A `Tensor` of type `float32`.
      A vector of hessians for each slot in <partition_id, feature_id>.
    name: A name for the operation (optional).

  Returns:
    A tuple of `Tensor` objects (output_partition_ids, output_feature_ids, output_gradients, output_hessians).

    output_partition_ids: A `Tensor` of type `int32`. A vector of partition_ids for the slots.
    output_feature_ids: A `Tensor` of type `int64`. A vector of feature_ids for the slots.
    output_gradients: A `Tensor` of type `float32`. A tensor of gradients, first dimension matches slots
      in <partition_id, feature_id>.
    output_hessians: A `Tensor` of type `float32`. A tensor of hessians, first dimension matches slots
      in <partition_id, feature_id>.
  """
  result = _op_def_lib.apply_op("StatsAccumulatorTensorMakeSummary",
                                partition_ids=partition_ids,
                                feature_ids=feature_ids, gradients=gradients,
                                hessians=hessians, name=name)
  return _StatsAccumulatorTensorMakeSummaryOutput._make(result)


_ops.RegisterShape("StatsAccumulatorTensorMakeSummary")(None)

def stats_accumulator_tensor_resource_handle_op(container=None,
                                                shared_name=None, name=None):
  r"""Creates a handle to a StatsAccumulatorTensorResource

  Args:
    container: An optional `string`. Defaults to `""`.
    shared_name: An optional `string`. Defaults to `""`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `resource`.
  """
  result = _op_def_lib.apply_op("StatsAccumulatorTensorResourceHandleOp",
                                container=container, shared_name=shared_name,
                                name=name)
  return result


_ops.RegisterShape("StatsAccumulatorTensorResourceHandleOp")(None)

_stats_accumulator_tensor_serialize_outputs = ["stamp_token", "num_updates",
                                              "output_partition_ids",
                                              "output_feature_ids",
                                              "output_gradients",
                                              "output_hessians"]
_StatsAccumulatorTensorSerializeOutput = _collections.namedtuple(
    "StatsAccumulatorTensorSerialize",
    _stats_accumulator_tensor_serialize_outputs)


def stats_accumulator_tensor_serialize(stats_accumulator_handle, name=None):
  r"""Serializes the scalar stats accumulator state.

  Args:
    stats_accumulator_handle: A `Tensor` of type `resource`.
      handle to the tree ensemble resource to be created.
    name: A name for the operation (optional).

  Returns:
    A tuple of `Tensor` objects (stamp_token, num_updates, output_partition_ids, output_feature_ids, output_gradients, output_hessians).

    stamp_token: A `Tensor` of type `int64`. Stamp token for Read/Write operations.
      Any operation with a mismatching token will be dropped.
    num_updates: A `Tensor` of type `int64`. Number of times stats were added to this accumulator since last
      flush.
    output_partition_ids: A `Tensor` of type `int32`. A vector of partition_ids for the slots.
    output_feature_ids: A `Tensor` of type `int64`. A vector of feature_ids for the slots.
    output_gradients: A `Tensor` of type `float32`. A tensor of gradients, first dimension matches slots
      in <partition_id, feature_id>.
    output_hessians: A `Tensor` of type `float32`. A tensor of hessians, first dimension matches slots
      in <partition_id, feature_id>.
  """
  result = _op_def_lib.apply_op("StatsAccumulatorTensorSerialize",
                                stats_accumulator_handle=stats_accumulator_handle,
                                name=name)
  return _StatsAccumulatorTensorSerializeOutput._make(result)


_ops.RegisterShape("StatsAccumulatorTensorSerialize")(None)
def _InitOpDefLibrary(op_list_proto_bytes):
  op_list = _op_def_pb2.OpList()
  op_list.ParseFromString(op_list_proto_bytes)
  _op_def_registry.register_op_list(op_list)
  op_def_lib = _op_def_library.OpDefLibrary()
  op_def_lib.add_op_list(op_list)
  return op_def_lib


# op {
#   name: "CreateStatsAccumulatorScalar"
#   input_arg {
#     name: "stats_accumulator_handle"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "stamp_token"
#     type: DT_INT64
#   }
#   is_stateful: true
# }
# op {
#   name: "CreateStatsAccumulatorTensor"
#   input_arg {
#     name: "stats_accumulator_handle"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "stamp_token"
#     type: DT_INT64
#   }
#   input_arg {
#     name: "per_slot_gradient_shape"
#     type: DT_INT64
#   }
#   input_arg {
#     name: "per_slot_hessian_shape"
#     type: DT_INT64
#   }
#   is_stateful: true
# }
# op {
#   name: "StatsAccumulatorScalarAdd"
#   input_arg {
#     name: "stats_accumulator_handles"
#     type: DT_RESOURCE
#     number_attr: "num_resource_handles"
#   }
#   input_arg {
#     name: "stamp_token"
#     type: DT_INT64
#   }
#   input_arg {
#     name: "partition_ids"
#     type: DT_INT32
#     number_attr: "num_resource_handles"
#   }
#   input_arg {
#     name: "feature_ids"
#     type: DT_INT64
#     number_attr: "num_resource_handles"
#   }
#   input_arg {
#     name: "gradients"
#     type: DT_FLOAT
#     number_attr: "num_resource_handles"
#   }
#   input_arg {
#     name: "hessians"
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
#   name: "StatsAccumulatorScalarDeserialize"
#   input_arg {
#     name: "stats_accumulator_handle"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "stamp_token"
#     type: DT_INT64
#   }
#   input_arg {
#     name: "num_updates"
#     type: DT_INT64
#   }
#   input_arg {
#     name: "partition_ids"
#     type: DT_INT32
#   }
#   input_arg {
#     name: "feature_ids"
#     type: DT_INT64
#   }
#   input_arg {
#     name: "gradients"
#     type: DT_FLOAT
#   }
#   input_arg {
#     name: "hessians"
#     type: DT_FLOAT
#   }
#   is_stateful: true
# }
# op {
#   name: "StatsAccumulatorScalarFlush"
#   input_arg {
#     name: "stats_accumulator_handle"
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
#   output_arg {
#     name: "num_updates"
#     type: DT_INT64
#   }
#   output_arg {
#     name: "output_partition_ids"
#     type: DT_INT32
#   }
#   output_arg {
#     name: "output_feature_ids"
#     type: DT_INT64
#   }
#   output_arg {
#     name: "output_gradients"
#     type: DT_FLOAT
#   }
#   output_arg {
#     name: "output_hessians"
#     type: DT_FLOAT
#   }
#   is_stateful: true
# }
# op {
#   name: "StatsAccumulatorScalarIsInitialized"
#   input_arg {
#     name: "stats_accumulator_handle"
#     type: DT_RESOURCE
#   }
#   output_arg {
#     name: "is_initialized"
#     type: DT_BOOL
#   }
#   is_stateful: true
# }
# op {
#   name: "StatsAccumulatorScalarMakeSummary"
#   input_arg {
#     name: "partition_ids"
#     type: DT_INT32
#   }
#   input_arg {
#     name: "feature_ids"
#     type: DT_INT64
#   }
#   input_arg {
#     name: "gradients"
#     type: DT_FLOAT
#   }
#   input_arg {
#     name: "hessians"
#     type: DT_FLOAT
#   }
#   output_arg {
#     name: "output_partition_ids"
#     type: DT_INT32
#   }
#   output_arg {
#     name: "output_feature_ids"
#     type: DT_INT64
#   }
#   output_arg {
#     name: "output_gradients"
#     type: DT_FLOAT
#   }
#   output_arg {
#     name: "output_hessians"
#     type: DT_FLOAT
#   }
# }
# op {
#   name: "StatsAccumulatorScalarResourceHandleOp"
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
#   name: "StatsAccumulatorScalarSerialize"
#   input_arg {
#     name: "stats_accumulator_handle"
#     type: DT_RESOURCE
#   }
#   output_arg {
#     name: "stamp_token"
#     type: DT_INT64
#   }
#   output_arg {
#     name: "num_updates"
#     type: DT_INT64
#   }
#   output_arg {
#     name: "output_partition_ids"
#     type: DT_INT32
#   }
#   output_arg {
#     name: "output_feature_ids"
#     type: DT_INT64
#   }
#   output_arg {
#     name: "output_gradients"
#     type: DT_FLOAT
#   }
#   output_arg {
#     name: "output_hessians"
#     type: DT_FLOAT
#   }
#   is_stateful: true
# }
# op {
#   name: "StatsAccumulatorTensorAdd"
#   input_arg {
#     name: "stats_accumulator_handles"
#     type: DT_RESOURCE
#     number_attr: "num_resource_handles"
#   }
#   input_arg {
#     name: "stamp_token"
#     type: DT_INT64
#   }
#   input_arg {
#     name: "partition_ids"
#     type: DT_INT32
#     number_attr: "num_resource_handles"
#   }
#   input_arg {
#     name: "feature_ids"
#     type: DT_INT64
#     number_attr: "num_resource_handles"
#   }
#   input_arg {
#     name: "gradients"
#     type: DT_FLOAT
#     number_attr: "num_resource_handles"
#   }
#   input_arg {
#     name: "hessians"
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
#   name: "StatsAccumulatorTensorDeserialize"
#   input_arg {
#     name: "stats_accumulator_handle"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "stamp_token"
#     type: DT_INT64
#   }
#   input_arg {
#     name: "num_updates"
#     type: DT_INT64
#   }
#   input_arg {
#     name: "partition_ids"
#     type: DT_INT32
#   }
#   input_arg {
#     name: "feature_ids"
#     type: DT_INT64
#   }
#   input_arg {
#     name: "gradients"
#     type: DT_FLOAT
#   }
#   input_arg {
#     name: "hessians"
#     type: DT_FLOAT
#   }
#   is_stateful: true
# }
# op {
#   name: "StatsAccumulatorTensorFlush"
#   input_arg {
#     name: "stats_accumulator_handle"
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
#   output_arg {
#     name: "num_updates"
#     type: DT_INT64
#   }
#   output_arg {
#     name: "output_partition_ids"
#     type: DT_INT32
#   }
#   output_arg {
#     name: "output_feature_ids"
#     type: DT_INT64
#   }
#   output_arg {
#     name: "output_gradients"
#     type: DT_FLOAT
#   }
#   output_arg {
#     name: "output_hessians"
#     type: DT_FLOAT
#   }
#   is_stateful: true
# }
# op {
#   name: "StatsAccumulatorTensorIsInitialized"
#   input_arg {
#     name: "stats_accumulator_handle"
#     type: DT_RESOURCE
#   }
#   output_arg {
#     name: "is_initialized"
#     type: DT_BOOL
#   }
#   is_stateful: true
# }
# op {
#   name: "StatsAccumulatorTensorMakeSummary"
#   input_arg {
#     name: "partition_ids"
#     type: DT_INT32
#   }
#   input_arg {
#     name: "feature_ids"
#     type: DT_INT64
#   }
#   input_arg {
#     name: "gradients"
#     type: DT_FLOAT
#   }
#   input_arg {
#     name: "hessians"
#     type: DT_FLOAT
#   }
#   output_arg {
#     name: "output_partition_ids"
#     type: DT_INT32
#   }
#   output_arg {
#     name: "output_feature_ids"
#     type: DT_INT64
#   }
#   output_arg {
#     name: "output_gradients"
#     type: DT_FLOAT
#   }
#   output_arg {
#     name: "output_hessians"
#     type: DT_FLOAT
#   }
# }
# op {
#   name: "StatsAccumulatorTensorResourceHandleOp"
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
#   name: "StatsAccumulatorTensorSerialize"
#   input_arg {
#     name: "stats_accumulator_handle"
#     type: DT_RESOURCE
#   }
#   output_arg {
#     name: "stamp_token"
#     type: DT_INT64
#   }
#   output_arg {
#     name: "num_updates"
#     type: DT_INT64
#   }
#   output_arg {
#     name: "output_partition_ids"
#     type: DT_INT32
#   }
#   output_arg {
#     name: "output_feature_ids"
#     type: DT_INT64
#   }
#   output_arg {
#     name: "output_gradients"
#     type: DT_FLOAT
#   }
#   output_arg {
#     name: "output_hessians"
#     type: DT_FLOAT
#   }
#   is_stateful: true
# }
_op_def_lib = _InitOpDefLibrary(b"\nP\n\034CreateStatsAccumulatorScalar\022\034\n\030stats_accumulator_handle\030\024\022\017\n\013stamp_token\030\t\210\001\001\n\211\001\n\034CreateStatsAccumulatorTensor\022\034\n\030stats_accumulator_handle\030\024\022\017\n\013stamp_token\030\t\022\033\n\027per_slot_gradient_shape\030\t\022\032\n\026per_slot_hessian_shape\030\t\210\001\001\n\236\002\n\031StatsAccumulatorScalarAdd\0223\n\031stats_accumulator_handles\030\024*\024num_resource_handles\022\017\n\013stamp_token\030\t\022\'\n\rpartition_ids\030\003*\024num_resource_handles\022%\n\013feature_ids\030\t*\024num_resource_handles\022#\n\tgradients\030\001*\024num_resource_handles\022\"\n\010hessians\030\001*\024num_resource_handles\"\037\n\024num_resource_handles\022\003int(\0010\001\210\001\001\n\247\001\n!StatsAccumulatorScalarDeserialize\022\034\n\030stats_accumulator_handle\030\024\022\017\n\013stamp_token\030\t\022\017\n\013num_updates\030\t\022\021\n\rpartition_ids\030\003\022\017\n\013feature_ids\030\t\022\r\n\tgradients\030\001\022\014\n\010hessians\030\001\210\001\001\n\323\001\n\033StatsAccumulatorScalarFlush\022\034\n\030stats_accumulator_handle\030\024\022\017\n\013stamp_token\030\t\022\024\n\020next_stamp_token\030\t\032\017\n\013num_updates\030\t\032\030\n\024output_partition_ids\030\003\032\026\n\022output_feature_ids\030\t\032\024\n\020output_gradients\030\001\032\023\n\017output_hessians\030\001\210\001\001\nZ\n#StatsAccumulatorScalarIsInitialized\022\034\n\030stats_accumulator_handle\030\024\032\022\n\016is_initialized\030\n\210\001\001\n\301\001\n!StatsAccumulatorScalarMakeSummary\022\021\n\rpartition_ids\030\003\022\017\n\013feature_ids\030\t\022\r\n\tgradients\030\001\022\014\n\010hessians\030\001\032\030\n\024output_partition_ids\030\003\032\026\n\022output_feature_ids\030\t\032\024\n\020output_gradients\030\001\032\023\n\017output_hessians\030\001\nm\n&StatsAccumulatorScalarResourceHandleOp\032\014\n\010resource\030\024\"\027\n\tcontainer\022\006string\032\002\022\000\"\031\n\013shared_name\022\006string\032\002\022\000\210\001\001\n\301\001\n\037StatsAccumulatorScalarSerialize\022\034\n\030stats_accumulator_handle\030\024\032\017\n\013stamp_token\030\t\032\017\n\013num_updates\030\t\032\030\n\024output_partition_ids\030\003\032\026\n\022output_feature_ids\030\t\032\024\n\020output_gradients\030\001\032\023\n\017output_hessians\030\001\210\001\001\n\236\002\n\031StatsAccumulatorTensorAdd\0223\n\031stats_accumulator_handles\030\024*\024num_resource_handles\022\017\n\013stamp_token\030\t\022\'\n\rpartition_ids\030\003*\024num_resource_handles\022%\n\013feature_ids\030\t*\024num_resource_handles\022#\n\tgradients\030\001*\024num_resource_handles\022\"\n\010hessians\030\001*\024num_resource_handles\"\037\n\024num_resource_handles\022\003int(\0010\001\210\001\001\n\247\001\n!StatsAccumulatorTensorDeserialize\022\034\n\030stats_accumulator_handle\030\024\022\017\n\013stamp_token\030\t\022\017\n\013num_updates\030\t\022\021\n\rpartition_ids\030\003\022\017\n\013feature_ids\030\t\022\r\n\tgradients\030\001\022\014\n\010hessians\030\001\210\001\001\n\323\001\n\033StatsAccumulatorTensorFlush\022\034\n\030stats_accumulator_handle\030\024\022\017\n\013stamp_token\030\t\022\024\n\020next_stamp_token\030\t\032\017\n\013num_updates\030\t\032\030\n\024output_partition_ids\030\003\032\026\n\022output_feature_ids\030\t\032\024\n\020output_gradients\030\001\032\023\n\017output_hessians\030\001\210\001\001\nZ\n#StatsAccumulatorTensorIsInitialized\022\034\n\030stats_accumulator_handle\030\024\032\022\n\016is_initialized\030\n\210\001\001\n\301\001\n!StatsAccumulatorTensorMakeSummary\022\021\n\rpartition_ids\030\003\022\017\n\013feature_ids\030\t\022\r\n\tgradients\030\001\022\014\n\010hessians\030\001\032\030\n\024output_partition_ids\030\003\032\026\n\022output_feature_ids\030\t\032\024\n\020output_gradients\030\001\032\023\n\017output_hessians\030\001\nm\n&StatsAccumulatorTensorResourceHandleOp\032\014\n\010resource\030\024\"\027\n\tcontainer\022\006string\032\002\022\000\"\031\n\013shared_name\022\006string\032\002\022\000\210\001\001\n\301\001\n\037StatsAccumulatorTensorSerialize\022\034\n\030stats_accumulator_handle\030\024\032\017\n\013stamp_token\030\t\032\017\n\013num_updates\030\t\032\030\n\024output_partition_ids\030\003\032\026\n\022output_feature_ids\030\t\032\024\n\020output_gradients\030\001\032\023\n\017output_hessians\030\001\210\001\001")
