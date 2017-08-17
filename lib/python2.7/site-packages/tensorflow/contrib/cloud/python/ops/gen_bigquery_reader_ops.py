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

def big_query_reader(project_id, dataset_id, table_id, columns,
                     timestamp_millis, container=None, shared_name=None,
                     test_end_point=None, name=None):
  r"""A Reader that outputs rows from a BigQuery table as tensorflow Examples.

  Args:
    project_id: A `string`. GCP project ID.
    dataset_id: A `string`. BigQuery Dataset ID.
    table_id: A `string`. Table to read.
    columns: A list of `strings`.
      List of columns to read. Leave empty to read all columns.
    timestamp_millis: An `int`.
      Table snapshot timestamp in millis since epoch. Relative
      (negative or zero) snapshot times are not allowed. For more details, see
      'Table Decorators' in BigQuery docs.
    container: An optional `string`. Defaults to `""`.
      If non-empty, this reader is placed in the given container.
      Otherwise, a default container is used.
    shared_name: An optional `string`. Defaults to `""`.
      If non-empty, this reader is named in the given bucket
      with this shared_name. Otherwise, the node name is used instead.
    test_end_point: An optional `string`. Defaults to `""`.
      Do not use. For testing purposes only.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type mutable `string`. The handle to reference the Reader.
  """
  result = _op_def_lib.apply_op("BigQueryReader", project_id=project_id,
                                dataset_id=dataset_id, table_id=table_id,
                                columns=columns,
                                timestamp_millis=timestamp_millis,
                                container=container, shared_name=shared_name,
                                test_end_point=test_end_point, name=name)
  return result



def generate_big_query_reader_partitions(project_id, dataset_id, table_id,
                                         columns, timestamp_millis,
                                         num_partitions, test_end_point=None,
                                         name=None):
  r"""Generates serialized partition messages suitable for batch reads.

  This op should not be used directly by clients. Instead, the
  bigquery_reader_ops.py file defines a clean interface to the reader.

  Args:
    project_id: A `string`. GCP project ID.
    dataset_id: A `string`. BigQuery Dataset ID.
    table_id: A `string`. Table to read.
    columns: A list of `strings`.
      List of columns to read. Leave empty to read all columns.
    timestamp_millis: An `int`.
      Table snapshot timestamp in millis since epoch. Relative
      (negative or zero) snapshot times are not allowed. For more details, see
      'Table Decorators' in BigQuery docs.
    num_partitions: An `int`. Number of partitions to split the table into.
    test_end_point: An optional `string`. Defaults to `""`.
      Do not use. For testing purposes only.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `string`. Serialized table partitions.
  """
  result = _op_def_lib.apply_op("GenerateBigQueryReaderPartitions",
                                project_id=project_id, dataset_id=dataset_id,
                                table_id=table_id, columns=columns,
                                timestamp_millis=timestamp_millis,
                                num_partitions=num_partitions,
                                test_end_point=test_end_point, name=name)
  return result


def _InitOpDefLibrary(op_list_proto_bytes):
  op_list = _op_def_pb2.OpList()
  op_list.ParseFromString(op_list_proto_bytes)
  _op_def_registry.register_op_list(op_list)
  op_def_lib = _op_def_library.OpDefLibrary()
  op_def_lib.add_op_list(op_list)
  return op_def_lib


# op {
#   name: "BigQueryReader"
#   output_arg {
#     name: "reader_handle"
#     type: DT_STRING
#     is_ref: true
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
#     name: "project_id"
#     type: "string"
#   }
#   attr {
#     name: "dataset_id"
#     type: "string"
#   }
#   attr {
#     name: "table_id"
#     type: "string"
#   }
#   attr {
#     name: "columns"
#     type: "list(string)"
#   }
#   attr {
#     name: "timestamp_millis"
#     type: "int"
#   }
#   attr {
#     name: "test_end_point"
#     type: "string"
#     default_value {
#       s: ""
#     }
#   }
#   is_stateful: true
# }
# op {
#   name: "GenerateBigQueryReaderPartitions"
#   output_arg {
#     name: "partitions"
#     type: DT_STRING
#   }
#   attr {
#     name: "project_id"
#     type: "string"
#   }
#   attr {
#     name: "dataset_id"
#     type: "string"
#   }
#   attr {
#     name: "table_id"
#     type: "string"
#   }
#   attr {
#     name: "columns"
#     type: "list(string)"
#   }
#   attr {
#     name: "timestamp_millis"
#     type: "int"
#   }
#   attr {
#     name: "num_partitions"
#     type: "int"
#   }
#   attr {
#     name: "test_end_point"
#     type: "string"
#     default_value {
#       s: ""
#     }
#   }
# }
_op_def_lib = _InitOpDefLibrary(b"\n\355\001\n\016BigQueryReader\032\024\n\rreader_handle\030\007\200\001\001\"\027\n\tcontainer\022\006string\032\002\022\000\"\031\n\013shared_name\022\006string\032\002\022\000\"\024\n\nproject_id\022\006string\"\024\n\ndataset_id\022\006string\"\022\n\010table_id\022\006string\"\027\n\007columns\022\014list(string)\"\027\n\020timestamp_millis\022\003int\"\034\n\016test_end_point\022\006string\032\002\022\000\210\001\001\n\331\001\n GenerateBigQueryReaderPartitions\032\016\n\npartitions\030\007\"\024\n\nproject_id\022\006string\"\024\n\ndataset_id\022\006string\"\022\n\010table_id\022\006string\"\027\n\007columns\022\014list(string)\"\027\n\020timestamp_millis\022\003int\"\025\n\016num_partitions\022\003int\"\034\n\016test_end_point\022\006string\032\002\022\000")
