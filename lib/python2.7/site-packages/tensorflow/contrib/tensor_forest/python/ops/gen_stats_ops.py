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

def create_fertile_stats_variable(stats_handle, stats_config, params,
                                  name=None):
  r"""Creates a stats model and returns a handle to it.

  Args:
    stats_handle: A `Tensor` of type `resource`.
      handle to the stats resource to be created.
    stats_config: A `Tensor` of type `string`. Serialized proto of the stats.
    params: A `string`. A serialized TensorForestParams proto.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  result = _op_def_lib.apply_op("CreateFertileStatsVariable",
                                stats_handle=stats_handle,
                                stats_config=stats_config, params=params,
                                name=name)
  return result


_ops.RegisterShape("CreateFertileStatsVariable")(None)

def fertile_stats_deserialize(stats_handle, stats_config, params, name=None):
  r"""Deserializes a serialized stats config and replaces current stats.

  Args:
    stats_handle: A `Tensor` of type `resource`. The handle to the stats.
    stats_config: A `Tensor` of type `string`. Serialized proto of the stats.
    params: A `string`. A serialized TensorForestParams proto.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  result = _op_def_lib.apply_op("FertileStatsDeserialize",
                                stats_handle=stats_handle,
                                stats_config=stats_config, params=params,
                                name=name)
  return result


_ops.RegisterShape("FertileStatsDeserialize")(None)

def fertile_stats_is_initialized_op(stats_handle, name=None):
  r"""Checks whether a stats has been initialized.

  Args:
    stats_handle: A `Tensor` of type `resource`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `bool`.
  """
  result = _op_def_lib.apply_op("FertileStatsIsInitializedOp",
                                stats_handle=stats_handle, name=name)
  return result


_ops.RegisterShape("FertileStatsIsInitializedOp")(None)

def fertile_stats_resource_handle_op(container=None, shared_name=None,
                                     name=None):
  r"""Creates a handle to a FertileStatsResource

  Args:
    container: An optional `string`. Defaults to `""`.
    shared_name: An optional `string`. Defaults to `""`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `resource`.
  """
  result = _op_def_lib.apply_op("FertileStatsResourceHandleOp",
                                container=container, shared_name=shared_name,
                                name=name)
  return result


_ops.RegisterShape("FertileStatsResourceHandleOp")(None)

def fertile_stats_serialize(stats_handle, params, name=None):
  r"""Serializes the stats to a proto.

  Args:
    stats_handle: A `Tensor` of type `resource`. The handle to the stats.
    params: A `string`. A serialized TensorForestParams proto.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `string`. Serialized proto of the stats.
  """
  result = _op_def_lib.apply_op("FertileStatsSerialize",
                                stats_handle=stats_handle, params=params,
                                name=name)
  return result


_ops.RegisterShape("FertileStatsSerialize")(None)

def finalize_tree(tree_handle, stats_handle, params, name=None):
  r"""Puts the Leaf models inside the tree into their final form.

  If drop_final_class is true, the per-class probability prediction of the
  last class is not stored in the leaf models.

  Args:
    tree_handle: A `Tensor` of type `resource`. The handle to the tree.
    stats_handle: A `Tensor` of type `resource`. The handle to the stats.
    params: A `string`. A serialized TensorForestParams proto.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  result = _op_def_lib.apply_op("FinalizeTree", tree_handle=tree_handle,
                                stats_handle=stats_handle, params=params,
                                name=name)
  return result


_ops.RegisterShape("FinalizeTree")(None)

def grow_tree_v4(tree_handle, stats_handle, finshed_nodes, params, name=None):
  r"""Grows the tree for finished nodes and allocates waiting nodes.

  Args:
    tree_handle: A `Tensor` of type `resource`. The handle to the tree.
    stats_handle: A `Tensor` of type `resource`. The handle to the stats.
    finshed_nodes: A `Tensor` of type `int32`.
      A 1-d Tensor of finished node ids from ProcessInput.
    params: A `string`. A serialized TensorForestParams proto.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  result = _op_def_lib.apply_op("GrowTreeV4", tree_handle=tree_handle,
                                stats_handle=stats_handle,
                                finshed_nodes=finshed_nodes, params=params,
                                name=name)
  return result


_ops.RegisterShape("GrowTreeV4")(None)

def process_input_v4(tree_handle, stats_handle, input_data,
                     sparse_input_indices, sparse_input_values,
                     sparse_input_shape, input_labels, input_weights,
                     leaf_ids, random_seed, input_spec, params, name=None):
  r"""Add labels to stats after traversing the tree for each example.

  Outputs node ids that are finished.

  Args:
    tree_handle: A `Tensor` of type `resource`. The handle to the tree.
    stats_handle: A `Tensor` of type `resource`. The handle to the stats.
    input_data: A `Tensor` of type `float32`.
      The training batch's features as a 2-d tensor; `input_data[i][j]`
      gives the j-th feature of the i-th input.
    sparse_input_indices: A `Tensor` of type `int64`.
      The indices tensor from the SparseTensor input.
    sparse_input_values: A `Tensor` of type `float32`.
      The values tensor from the SparseTensor input.
    sparse_input_shape: A `Tensor` of type `int64`.
      The shape tensor from the SparseTensor input.
    input_labels: A `Tensor` of type `float32`.
      The training batch's labels as a 1 or 2-d tensor.
      'input_labels[i][j]' gives the j-th label/target for the i-th input.
    input_weights: A `Tensor` of type `float32`.
      The training batch's eample weights as a 1-d tensor.
      'input_weights[i]' gives the weight for the i-th input.
    leaf_ids: A `Tensor` of type `int32`.
      `leaf_ids[i]` is the leaf id for input i.
    random_seed: An `int`.
    input_spec: A `string`.
    params: A `string`. A serialized TensorForestParams proto.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `int32`.
    A 1-d tensor of node ids that have finished and are ready to
    grow.
  """
  result = _op_def_lib.apply_op("ProcessInputV4", tree_handle=tree_handle,
                                stats_handle=stats_handle,
                                input_data=input_data,
                                sparse_input_indices=sparse_input_indices,
                                sparse_input_values=sparse_input_values,
                                sparse_input_shape=sparse_input_shape,
                                input_labels=input_labels,
                                input_weights=input_weights,
                                leaf_ids=leaf_ids, random_seed=random_seed,
                                input_spec=input_spec, params=params,
                                name=name)
  return result


_ops.RegisterShape("ProcessInputV4")(None)
def _InitOpDefLibrary(op_list_proto_bytes):
  op_list = _op_def_pb2.OpList()
  op_list.ParseFromString(op_list_proto_bytes)
  _op_def_registry.register_op_list(op_list)
  op_def_lib = _op_def_library.OpDefLibrary()
  op_def_lib.add_op_list(op_list)
  return op_def_lib


# op {
#   name: "CreateFertileStatsVariable"
#   input_arg {
#     name: "stats_handle"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "stats_config"
#     type: DT_STRING
#   }
#   attr {
#     name: "params"
#     type: "string"
#   }
#   is_stateful: true
# }
# op {
#   name: "FertileStatsDeserialize"
#   input_arg {
#     name: "stats_handle"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "stats_config"
#     type: DT_STRING
#   }
#   attr {
#     name: "params"
#     type: "string"
#   }
#   is_stateful: true
# }
# op {
#   name: "FertileStatsIsInitializedOp"
#   input_arg {
#     name: "stats_handle"
#     type: DT_RESOURCE
#   }
#   output_arg {
#     name: "is_initialized"
#     type: DT_BOOL
#   }
#   is_stateful: true
# }
# op {
#   name: "FertileStatsResourceHandleOp"
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
#   name: "FertileStatsSerialize"
#   input_arg {
#     name: "stats_handle"
#     type: DT_RESOURCE
#   }
#   output_arg {
#     name: "stats_config"
#     type: DT_STRING
#   }
#   attr {
#     name: "params"
#     type: "string"
#   }
#   is_stateful: true
# }
# op {
#   name: "FinalizeTree"
#   input_arg {
#     name: "tree_handle"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "stats_handle"
#     type: DT_RESOURCE
#   }
#   attr {
#     name: "params"
#     type: "string"
#   }
#   is_stateful: true
# }
# op {
#   name: "GrowTreeV4"
#   input_arg {
#     name: "tree_handle"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "stats_handle"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "finshed_nodes"
#     type: DT_INT32
#   }
#   attr {
#     name: "params"
#     type: "string"
#   }
#   is_stateful: true
# }
# op {
#   name: "ProcessInputV4"
#   input_arg {
#     name: "tree_handle"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "stats_handle"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "input_data"
#     type: DT_FLOAT
#   }
#   input_arg {
#     name: "sparse_input_indices"
#     type: DT_INT64
#   }
#   input_arg {
#     name: "sparse_input_values"
#     type: DT_FLOAT
#   }
#   input_arg {
#     name: "sparse_input_shape"
#     type: DT_INT64
#   }
#   input_arg {
#     name: "input_labels"
#     type: DT_FLOAT
#   }
#   input_arg {
#     name: "input_weights"
#     type: DT_FLOAT
#   }
#   input_arg {
#     name: "leaf_ids"
#     type: DT_INT32
#   }
#   output_arg {
#     name: "finished_nodes"
#     type: DT_INT32
#   }
#   attr {
#     name: "random_seed"
#     type: "int"
#   }
#   attr {
#     name: "input_spec"
#     type: "string"
#   }
#   attr {
#     name: "params"
#     type: "string"
#   }
#   is_stateful: true
# }
_op_def_lib = _InitOpDefLibrary(b"\nU\n\032CreateFertileStatsVariable\022\020\n\014stats_handle\030\024\022\020\n\014stats_config\030\007\"\020\n\006params\022\006string\210\001\001\nR\n\027FertileStatsDeserialize\022\020\n\014stats_handle\030\024\022\020\n\014stats_config\030\007\"\020\n\006params\022\006string\210\001\001\nF\n\033FertileStatsIsInitializedOp\022\020\n\014stats_handle\030\024\032\022\n\016is_initialized\030\n\210\001\001\nc\n\034FertileStatsResourceHandleOp\032\014\n\010resource\030\024\"\027\n\tcontainer\022\006string\032\002\022\000\"\031\n\013shared_name\022\006string\032\002\022\000\210\001\001\nP\n\025FertileStatsSerialize\022\020\n\014stats_handle\030\024\032\020\n\014stats_config\030\007\"\020\n\006params\022\006string\210\001\001\nF\n\014FinalizeTree\022\017\n\013tree_handle\030\024\022\020\n\014stats_handle\030\024\"\020\n\006params\022\006string\210\001\001\nW\n\nGrowTreeV4\022\017\n\013tree_handle\030\024\022\020\n\014stats_handle\030\024\022\021\n\rfinshed_nodes\030\003\"\020\n\006params\022\006string\210\001\001\n\224\002\n\016ProcessInputV4\022\017\n\013tree_handle\030\024\022\020\n\014stats_handle\030\024\022\016\n\ninput_data\030\001\022\030\n\024sparse_input_indices\030\t\022\027\n\023sparse_input_values\030\001\022\026\n\022sparse_input_shape\030\t\022\020\n\014input_labels\030\001\022\021\n\rinput_weights\030\001\022\014\n\010leaf_ids\030\003\032\022\n\016finished_nodes\030\003\"\022\n\013random_seed\022\003int\"\024\n\ninput_spec\022\006string\"\020\n\006params\022\006string\210\001\001")
