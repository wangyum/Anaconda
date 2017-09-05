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

def add_trees_to_ensemble(tree_ensemble_handle, ensemble_to_add,
                          feature_column_usage_counts_handle,
                          feature_column_usage_counts_to_add,
                          feature_column_gains_handle,
                          feature_column_gains_to_add,
                          drop_out_tree_indices_weights, learning_rate,
                          name=None):
  r"""Synchronously adds a tree ensemble to a an existing tree ensemble variable.

  Args:
    tree_ensemble_handle: A `Tensor` of type `resource`.
      Handle to the ensemble variable.
    ensemble_to_add: A `Tensor` of type `string`.
      Serialized DecisionTreeConfig proto of the tree.
    feature_column_usage_counts_handle: A `Tensor` of type mutable `int64`.
      Handle to the feature column usage counts variable.
    feature_column_usage_counts_to_add: A `Tensor` of type `int64`.
      Rank 1 Tensor holding feature column usage counts to add.
    feature_column_gains_handle: A `Tensor` of type mutable `float32`.
      Handle to the feature column gains variable.
    feature_column_gains_to_add: A `Tensor` of type `float32`.
      Rank 1 Tensor holding feature column gains to add.
    drop_out_tree_indices_weights: A `Tensor` of type `float32`.
      Rank 2 Tensor containing dropped trees indices
      and original weights of those trees during prediction.
    learning_rate: A `Tensor` of type `float32`.
      The learning rate that the tuner found for this iteration.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  result = _op_def_lib.apply_op("AddTreesToEnsemble",
                                tree_ensemble_handle=tree_ensemble_handle,
                                ensemble_to_add=ensemble_to_add,
                                feature_column_usage_counts_handle=feature_column_usage_counts_handle,
                                feature_column_usage_counts_to_add=feature_column_usage_counts_to_add,
                                feature_column_gains_handle=feature_column_gains_handle,
                                feature_column_gains_to_add=feature_column_gains_to_add,
                                drop_out_tree_indices_weights=drop_out_tree_indices_weights,
                                learning_rate=learning_rate, name=name)
  return result


_ops.RegisterShape("AddTreesToEnsemble")(None)
def _InitOpDefLibrary(op_list_proto_bytes):
  op_list = _op_def_pb2.OpList()
  op_list.ParseFromString(op_list_proto_bytes)
  _op_def_registry.register_op_list(op_list)
  op_def_lib = _op_def_library.OpDefLibrary()
  op_def_lib.add_op_list(op_list)
  return op_def_lib


# op {
#   name: "AddTreesToEnsemble"
#   input_arg {
#     name: "tree_ensemble_handle"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "ensemble_to_add"
#     type: DT_STRING
#   }
#   input_arg {
#     name: "feature_column_usage_counts_handle"
#     type: DT_INT64
#     is_ref: true
#   }
#   input_arg {
#     name: "feature_column_usage_counts_to_add"
#     type: DT_INT64
#   }
#   input_arg {
#     name: "feature_column_gains_handle"
#     type: DT_FLOAT
#     is_ref: true
#   }
#   input_arg {
#     name: "feature_column_gains_to_add"
#     type: DT_FLOAT
#   }
#   input_arg {
#     name: "drop_out_tree_indices_weights"
#     type: DT_FLOAT
#   }
#   input_arg {
#     name: "learning_rate"
#     type: DT_FLOAT
#   }
#   is_stateful: true
# }
_op_def_lib = _InitOpDefLibrary(b"\n\224\002\n\022AddTreesToEnsemble\022\030\n\024tree_ensemble_handle\030\024\022\023\n\017ensemble_to_add\030\007\022)\n\"feature_column_usage_counts_handle\030\t\200\001\001\022&\n\"feature_column_usage_counts_to_add\030\t\022\"\n\033feature_column_gains_handle\030\001\200\001\001\022\037\n\033feature_column_gains_to_add\030\001\022!\n\035drop_out_tree_indices_weights\030\001\022\021\n\rlearning_rate\030\001\210\001\001")
