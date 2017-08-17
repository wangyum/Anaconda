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

def create_tree_variable(tree_handle, tree_config, params, name=None):
  r"""Creates a tree  model and returns a handle to it.

  Args:
    tree_handle: A `Tensor` of type `resource`.
      handle to the tree resource to be created.
    tree_config: A `Tensor` of type `string`. Serialized proto of the tree.
    params: A `string`. A serialized TensorForestParams proto.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  result = _op_def_lib.apply_op("CreateTreeVariable", tree_handle=tree_handle,
                                tree_config=tree_config, params=params,
                                name=name)
  return result


_ops.RegisterShape("CreateTreeVariable")(None)

def decision_tree_resource_handle_op(container=None, shared_name=None,
                                     name=None):
  r"""Creates a handle to a DecisionTreeResource

  Args:
    container: An optional `string`. Defaults to `""`.
    shared_name: An optional `string`. Defaults to `""`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `resource`.
  """
  result = _op_def_lib.apply_op("DecisionTreeResourceHandleOp",
                                container=container, shared_name=shared_name,
                                name=name)
  return result


_ops.RegisterShape("DecisionTreeResourceHandleOp")(None)

def feature_usage_counts(tree_handle, params, name=None):
  r"""Outputs the number of times each feature was used in a split.

  Args:
    tree_handle: A `Tensor` of type `resource`. The handle to the tree.
    params: A `string`. A serialized TensorForestParams proto.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `int32`.
    `feature_counts[i]` is the number of times feature i was used
    in a split.
  """
  result = _op_def_lib.apply_op("FeatureUsageCounts", tree_handle=tree_handle,
                                params=params, name=name)
  return result


_ops.RegisterShape("FeatureUsageCounts")(None)

def traverse_tree_v4(tree_handle, input_data, sparse_input_indices,
                     sparse_input_values, sparse_input_shape, input_spec,
                     params, name=None):
  r"""Outputs the leaf ids for the given input data.

  Args:
    tree_handle: A `Tensor` of type `resource`. The handle to the tree.
    input_data: A `Tensor` of type `float32`.
      The training batch's features as a 2-d tensor; `input_data[i][j]`
      gives the j-th feature of the i-th input.
    sparse_input_indices: A `Tensor` of type `int64`.
      The indices tensor from the SparseTensor input.
    sparse_input_values: A `Tensor` of type `float32`.
      The values tensor from the SparseTensor input.
    sparse_input_shape: A `Tensor` of type `int64`.
      The shape tensor from the SparseTensor input.
    input_spec: A `string`.
    params: A `string`. A serialized TensorForestParams proto.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `int32`. `leaf_ids[i]` is the leaf id for input i.
  """
  result = _op_def_lib.apply_op("TraverseTreeV4", tree_handle=tree_handle,
                                input_data=input_data,
                                sparse_input_indices=sparse_input_indices,
                                sparse_input_values=sparse_input_values,
                                sparse_input_shape=sparse_input_shape,
                                input_spec=input_spec, params=params,
                                name=name)
  return result


_ops.RegisterShape("TraverseTreeV4")(None)

def tree_deserialize(tree_handle, tree_config, params, name=None):
  r"""Deserializes a serialized tree config and replaces current tree.

  Args:
    tree_handle: A `Tensor` of type `resource`. The handle to the tree .
    tree_config: A `Tensor` of type `string`. Serialized proto of the .
    params: A `string`. A serialized TensorForestParams proto.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  result = _op_def_lib.apply_op("TreeDeserialize", tree_handle=tree_handle,
                                tree_config=tree_config, params=params,
                                name=name)
  return result


_ops.RegisterShape("TreeDeserialize")(None)

def tree_is_initialized_op(tree_handle, name=None):
  r"""Checks whether a tree has been initialized.

  Args:
    tree_handle: A `Tensor` of type `resource`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `bool`.
  """
  result = _op_def_lib.apply_op("TreeIsInitializedOp",
                                tree_handle=tree_handle, name=name)
  return result


_ops.RegisterShape("TreeIsInitializedOp")(None)

def tree_predictions_v4(tree_handle, input_data, sparse_input_indices,
                        sparse_input_values, sparse_input_shape, input_spec,
                        params, name=None):
  r"""Outputs the predictions for the given input data.

  Args:
    tree_handle: A `Tensor` of type `resource`. The handle to the tree.
    input_data: A `Tensor` of type `float32`.
      The training batch's features as a 2-d tensor; `input_data[i][j]`
      gives the j-th feature of the i-th input.
    sparse_input_indices: A `Tensor` of type `int64`.
      The indices tensor from the SparseTensor input.
    sparse_input_values: A `Tensor` of type `float32`.
      The values tensor from the SparseTensor input.
    sparse_input_shape: A `Tensor` of type `int64`.
      The shape tensor from the SparseTensor input.
    input_spec: A `string`.
    params: A `string`. A serialized TensorForestParams proto.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `float32`.
    `predictions[i][j]` is the probability that input i is class j.
  """
  result = _op_def_lib.apply_op("TreePredictionsV4", tree_handle=tree_handle,
                                input_data=input_data,
                                sparse_input_indices=sparse_input_indices,
                                sparse_input_values=sparse_input_values,
                                sparse_input_shape=sparse_input_shape,
                                input_spec=input_spec, params=params,
                                name=name)
  return result


_ops.RegisterShape("TreePredictionsV4")(None)

def tree_serialize(tree_handle, name=None):
  r"""Serializes the tree  to a proto.

  Args:
    tree_handle: A `Tensor` of type `resource`. The handle to the tree.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `string`. Serialized proto of the tree.
  """
  result = _op_def_lib.apply_op("TreeSerialize", tree_handle=tree_handle,
                                name=name)
  return result


_ops.RegisterShape("TreeSerialize")(None)

def tree_size(tree_handle, name=None):
  r"""Outputs the size of the tree, including leaves.

  Args:
    tree_handle: A `Tensor` of type `resource`. The handle to the tree.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `int32`. Size scalar.
  """
  result = _op_def_lib.apply_op("TreeSize", tree_handle=tree_handle,
                                name=name)
  return result


_ops.RegisterShape("TreeSize")(None)

def update_model_v4(tree_handle, leaf_ids, input_labels, input_weights,
                    params, name=None):
  r"""Updates the given leaves for each example with the new labels.

  Args:
    tree_handle: A `Tensor` of type `resource`. The handle to the tree.
    leaf_ids: A `Tensor` of type `int32`.
      `leaf_ids[i]` is the leaf id for input i.
    input_labels: A `Tensor` of type `float32`.
      The training batch's labels as a 1 or 2-d tensor.
      'input_labels[i][j]' gives the j-th label/target for the i-th input.
    input_weights: A `Tensor` of type `float32`.
      The training batch's eample weights as a 1-d tensor.
      'input_weights[i]' gives the weight for the i-th input.
    params: A `string`. A serialized TensorForestParams proto.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  result = _op_def_lib.apply_op("UpdateModelV4", tree_handle=tree_handle,
                                leaf_ids=leaf_ids, input_labels=input_labels,
                                input_weights=input_weights, params=params,
                                name=name)
  return result


_ops.RegisterShape("UpdateModelV4")(None)
def _InitOpDefLibrary(op_list_proto_bytes):
  op_list = _op_def_pb2.OpList()
  op_list.ParseFromString(op_list_proto_bytes)
  _op_def_registry.register_op_list(op_list)
  op_def_lib = _op_def_library.OpDefLibrary()
  op_def_lib.add_op_list(op_list)
  return op_def_lib


# op {
#   name: "CreateTreeVariable"
#   input_arg {
#     name: "tree_handle"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "tree_config"
#     type: DT_STRING
#   }
#   attr {
#     name: "params"
#     type: "string"
#   }
#   is_stateful: true
# }
# op {
#   name: "DecisionTreeResourceHandleOp"
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
#   name: "FeatureUsageCounts"
#   input_arg {
#     name: "tree_handle"
#     type: DT_RESOURCE
#   }
#   output_arg {
#     name: "feature_counts"
#     type: DT_INT32
#   }
#   attr {
#     name: "params"
#     type: "string"
#   }
#   is_stateful: true
# }
# op {
#   name: "TraverseTreeV4"
#   input_arg {
#     name: "tree_handle"
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
#   output_arg {
#     name: "leaf_ids"
#     type: DT_INT32
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
# op {
#   name: "TreeDeserialize"
#   input_arg {
#     name: "tree_handle"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "tree_config"
#     type: DT_STRING
#   }
#   attr {
#     name: "params"
#     type: "string"
#   }
#   is_stateful: true
# }
# op {
#   name: "TreeIsInitializedOp"
#   input_arg {
#     name: "tree_handle"
#     type: DT_RESOURCE
#   }
#   output_arg {
#     name: "is_initialized"
#     type: DT_BOOL
#   }
#   is_stateful: true
# }
# op {
#   name: "TreePredictionsV4"
#   input_arg {
#     name: "tree_handle"
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
#   output_arg {
#     name: "predictions"
#     type: DT_FLOAT
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
# op {
#   name: "TreeSerialize"
#   input_arg {
#     name: "tree_handle"
#     type: DT_RESOURCE
#   }
#   output_arg {
#     name: "tree_config"
#     type: DT_STRING
#   }
#   is_stateful: true
# }
# op {
#   name: "TreeSize"
#   input_arg {
#     name: "tree_handle"
#     type: DT_RESOURCE
#   }
#   output_arg {
#     name: "tree_size"
#     type: DT_INT32
#   }
#   is_stateful: true
# }
# op {
#   name: "UpdateModelV4"
#   input_arg {
#     name: "tree_handle"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "leaf_ids"
#     type: DT_INT32
#   }
#   input_arg {
#     name: "input_labels"
#     type: DT_FLOAT
#   }
#   input_arg {
#     name: "input_weights"
#     type: DT_FLOAT
#   }
#   attr {
#     name: "params"
#     type: "string"
#   }
#   is_stateful: true
# }
_op_def_lib = _InitOpDefLibrary(b"\nK\n\022CreateTreeVariable\022\017\n\013tree_handle\030\024\022\017\n\013tree_config\030\007\"\020\n\006params\022\006string\210\001\001\nc\n\034DecisionTreeResourceHandleOp\032\014\n\010resource\030\024\"\027\n\tcontainer\022\006string\032\002\022\000\"\031\n\013shared_name\022\006string\032\002\022\000\210\001\001\nN\n\022FeatureUsageCounts\022\017\n\013tree_handle\030\024\032\022\n\016feature_counts\030\003\"\020\n\006params\022\006string\210\001\001\n\265\001\n\016TraverseTreeV4\022\017\n\013tree_handle\030\024\022\016\n\ninput_data\030\001\022\030\n\024sparse_input_indices\030\t\022\027\n\023sparse_input_values\030\001\022\026\n\022sparse_input_shape\030\t\032\014\n\010leaf_ids\030\003\"\024\n\ninput_spec\022\006string\"\020\n\006params\022\006string\210\001\001\nH\n\017TreeDeserialize\022\017\n\013tree_handle\030\024\022\017\n\013tree_config\030\007\"\020\n\006params\022\006string\210\001\001\n=\n\023TreeIsInitializedOp\022\017\n\013tree_handle\030\024\032\022\n\016is_initialized\030\n\210\001\001\n\273\001\n\021TreePredictionsV4\022\017\n\013tree_handle\030\024\022\016\n\ninput_data\030\001\022\030\n\024sparse_input_indices\030\t\022\027\n\023sparse_input_values\030\001\022\026\n\022sparse_input_shape\030\t\032\017\n\013predictions\030\001\"\024\n\ninput_spec\022\006string\"\020\n\006params\022\006string\210\001\001\n4\n\rTreeSerialize\022\017\n\013tree_handle\030\024\032\017\n\013tree_config\030\007\210\001\001\n-\n\010TreeSize\022\017\n\013tree_handle\030\024\032\r\n\ttree_size\030\003\210\001\001\nh\n\rUpdateModelV4\022\017\n\013tree_handle\030\024\022\014\n\010leaf_ids\030\003\022\020\n\014input_labels\030\001\022\021\n\rinput_weights\030\001\"\020\n\006params\022\006string\210\001\001")
