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

_generate_vocab_remapping_outputs = ["remapping", "num_present"]
_GenerateVocabRemappingOutput = _collections.namedtuple(
    "GenerateVocabRemapping", _generate_vocab_remapping_outputs)


def generate_vocab_remapping(new_vocab_file, old_vocab_file, new_vocab_offset,
                             num_new_vocab, name=None):
  r"""Given a path to new and old vocabulary files, returns a remapping Tensor of

  length `num_new_vocab`, where `remapping[i]` contains the row number in the old
  vocabulary that corresponds to row `i` in the new vocabulary (starting at line
  `new_vocab_offset` and up to `num_new_vocab` entities), or `-1` if entry `i`
  in the new vocabulary is not in the old vocabulary.  `num_vocab_offset` enables
  use in the partitioned variable case, and should generally be set through
  examining partitioning info.  The format of the files should be a text file,
  with each line containing a single entity within the vocabulary.

  For example, with `new_vocab_file` a text file containing each of the following
  elements on a single line: `[f0, f1, f2, f3]`, old_vocab_file = [f1, f0, f3],
  `num_new_vocab = 3, new_vocab_offset = 1`, the returned remapping would be
  `[0, -1, 2]`.

  The op also returns a count of how many entries in the new vocabulary
  were present in the old vocabulary, which is used to calculate the number of
  values to initialize in a weight matrix remapping

  This functionality can be used to remap both row vocabularies (typically,
  features) and column vocabularies (typically, classes) from TensorFlow
  checkpoints.  Note that the partitioning logic relies on contiguous vocabularies
  corresponding to div-partitioned variables.  Moreover, the underlying remapping
  uses an IndexTable (as opposed to an inexact CuckooTable), so client code should
  use the corresponding index_table_from_file() as the FeatureColumn framework
  does (as opposed to tf.feature_to_id(), which uses a CuckooTable).

  Args:
    new_vocab_file: A `Tensor` of type `string`. Path to the new vocab file.
    old_vocab_file: A `Tensor` of type `string`. Path to the old vocab file.
    new_vocab_offset: An `int` that is `>= 0`.
      How many entries into the new vocab file to start reading.
    num_new_vocab: An `int` that is `>= 0`.
      Number of entries in the new vocab file to remap.
    name: A name for the operation (optional).

  Returns:
    A tuple of `Tensor` objects (remapping, num_present).

    remapping: A `Tensor` of type `int64`. A Tensor of length num_new_vocab where the element at index i
      is equal to the old ID that maps to the new ID i.  This element is -1 for any
      new ID that is not found in the old vocabulary.
    num_present: A `Tensor` of type `int32`. Number of new vocab entries found in old vocab.
  """
  result = _op_def_lib.apply_op("GenerateVocabRemapping",
                                new_vocab_file=new_vocab_file,
                                old_vocab_file=old_vocab_file,
                                new_vocab_offset=new_vocab_offset,
                                num_new_vocab=num_new_vocab, name=name)
  return _GenerateVocabRemappingOutput._make(result)


_ops.RegisterShape("GenerateVocabRemapping")(None)

def load_and_remap_matrix(ckpt_path, old_tensor_name, row_remapping,
                          col_remapping, initializing_values, num_rows,
                          num_cols, max_rows_in_memory=None, name=None):
  r"""Loads a 2-D (matrix) `Tensor` with name `old_tensor_name` from the checkpoint

  at `ckpt_path` and potentially reorders its rows and columns using the
  specified remappings.

  Most users should use one of the wrapper initializers (such as
  `tf.contrib.framework.load_and_remap_matrix_initializer`) instead of this
  function directly.

  The remappings are 1-D tensors with the following properties:

  * `row_remapping` must have exactly `num_rows` entries. Row `i` of the output
    matrix will be initialized from the row corresponding to index
    `row_remapping[i]` in the old `Tensor` from the checkpoint.
  * `col_remapping` must have either 0 entries (indicating that no column
    reordering is needed) or `num_cols` entries. If specified, column `j` of the
    output matrix will be initialized from the column corresponding to index
    `col_remapping[j]` in the old `Tensor` from the checkpoint.
  * A value of -1 in either of the remappings signifies a "missing" entry. In that
    case, values from the `initializing_values` tensor will be used to fill that
    missing row or column. If `row_remapping` has `r` missing entries and
    `col_remapping` has `c` missing entries, then the following condition must be
    true:

  `(r * num_cols) + (c * num_rows) - (r * c) == len(initializing_values)`

  The remapping tensors can be generated using the GenerateVocabRemapping op.

  As an example, with row_remapping = [1, 0, -1], col_remapping = [0, 2, -1],
  initializing_values = [0.5, -0.5, 0.25, -0.25, 42], and w(i, j) representing
  the value from row i, column j of the old tensor in the checkpoint, the output
  matrix will look like the following:

  [[w(1, 0),  w(1, 2),  0.5],
   [w(0, 0),  w(0, 2), -0.5],
   [0.25,    -0.25,      42]]

  Args:
    ckpt_path: A `Tensor` of type `string`.
      Path to the TensorFlow checkpoint (version 2, `TensorBundle`) from
      which the old matrix `Tensor` will be loaded.
    old_tensor_name: A `Tensor` of type `string`.
      Name of the 2-D `Tensor` to load from checkpoint.
    row_remapping: A `Tensor` of type `int64`.
      An int `Tensor` of row remappings (generally created by
      `generate_vocab_remapping`).  Even if no row remapping is needed, this must
      still be an index-valued Tensor (e.g. [0, 1, 2, ...]), or a shifted
      index-valued `Tensor` (e.g. [8, 9, 10, ...], for partitioned `Variables`).
    col_remapping: A `Tensor` of type `int64`.
      An int `Tensor` of column remappings (generally created by
      `generate_vocab_remapping`).  May be a size-0 `Tensor` if only row remapping
      is to be done (e.g. column ordering is the same).
    initializing_values: A `Tensor` of type `float32`.
      A float `Tensor` containing  values to fill in for cells
      in the output matrix that are not loaded from the checkpoint. Length must be
      exactly the same as the number of missing / new cells.
    num_rows: An `int` that is `>= 0`.
      Number of rows (length of the 1st dimension) in the output matrix.
    num_cols: An `int` that is `>= 1`.
      Number of columns (length of the 2nd dimension) in the output matrix.
    max_rows_in_memory: An optional `int`. Defaults to `-1`.
      The maximum number of rows to load from the checkpoint at
      once. If less than or equal to 0, the entire matrix will be loaded into
      memory. Setting this arg trades increased disk reads for lower memory usage.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `float32`.
    Output matrix containing existing values loaded from the
    checkpoint, and with any missing values filled in from initializing_values.
  """
  result = _op_def_lib.apply_op("LoadAndRemapMatrix", ckpt_path=ckpt_path,
                                old_tensor_name=old_tensor_name,
                                row_remapping=row_remapping,
                                col_remapping=col_remapping,
                                initializing_values=initializing_values,
                                num_rows=num_rows, num_cols=num_cols,
                                max_rows_in_memory=max_rows_in_memory,
                                name=name)
  return result


_ops.RegisterShape("LoadAndRemapMatrix")(None)
def _InitOpDefLibrary(op_list_proto_bytes):
  op_list = _op_def_pb2.OpList()
  op_list.ParseFromString(op_list_proto_bytes)
  _op_def_registry.register_op_list(op_list)
  op_def_lib = _op_def_library.OpDefLibrary()
  op_def_lib.add_op_list(op_list)
  return op_def_lib


# op {
#   name: "GenerateVocabRemapping"
#   input_arg {
#     name: "new_vocab_file"
#     type: DT_STRING
#   }
#   input_arg {
#     name: "old_vocab_file"
#     type: DT_STRING
#   }
#   output_arg {
#     name: "remapping"
#     type: DT_INT64
#   }
#   output_arg {
#     name: "num_present"
#     type: DT_INT32
#   }
#   attr {
#     name: "new_vocab_offset"
#     type: "int"
#     has_minimum: true
#   }
#   attr {
#     name: "num_new_vocab"
#     type: "int"
#     has_minimum: true
#   }
# }
# op {
#   name: "LoadAndRemapMatrix"
#   input_arg {
#     name: "ckpt_path"
#     type: DT_STRING
#   }
#   input_arg {
#     name: "old_tensor_name"
#     type: DT_STRING
#   }
#   input_arg {
#     name: "row_remapping"
#     type: DT_INT64
#   }
#   input_arg {
#     name: "col_remapping"
#     type: DT_INT64
#   }
#   input_arg {
#     name: "initializing_values"
#     type: DT_FLOAT
#   }
#   output_arg {
#     name: "output_matrix"
#     type: DT_FLOAT
#   }
#   attr {
#     name: "num_rows"
#     type: "int"
#     has_minimum: true
#   }
#   attr {
#     name: "num_cols"
#     type: "int"
#     has_minimum: true
#     minimum: 1
#   }
#   attr {
#     name: "max_rows_in_memory"
#     type: "int"
#     default_value {
#       i: -1
#     }
#   }
#   is_stateful: true
# }
_op_def_lib = _InitOpDefLibrary(b"\n\223\001\n\026GenerateVocabRemapping\022\022\n\016new_vocab_file\030\007\022\022\n\016old_vocab_file\030\007\032\r\n\tremapping\030\t\032\017\n\013num_present\030\003\"\031\n\020new_vocab_offset\022\003int(\001\"\026\n\rnum_new_vocab\022\003int(\001\n\335\001\n\022LoadAndRemapMatrix\022\r\n\tckpt_path\030\007\022\023\n\017old_tensor_name\030\007\022\021\n\rrow_remapping\030\t\022\021\n\rcol_remapping\030\t\022\027\n\023initializing_values\030\001\032\021\n\routput_matrix\030\001\"\021\n\010num_rows\022\003int(\001\"\023\n\010num_cols\022\003int(\0010\001\"&\n\022max_rows_in_memory\022\003int\032\013\030\377\377\377\377\377\377\377\377\377\001\210\001\001")
