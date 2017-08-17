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

def configure_distributed_tpu(embedding_config=None, name=None):
  r"""An op that sets up the centralized structures for a distributed TPU

  system.

  Args:
    embedding_config: An optional `string`. Defaults to `""`. Internal use.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `int32`.
    A two-dimensional array. For each host (the outer
    dimension) the array lists the global ids of the TPUs on that host.
  """
  result = _op_def_lib.apply_op("ConfigureDistributedTPU",
                                embedding_config=embedding_config, name=name)
  return result


_ops.RegisterShape("ConfigureDistributedTPU")(None)

def cross_replica_sum(input, name=None):
  r"""An Op to sum inputs across replicated TPU instances. Each

  instance supplies its own input, and the output of each is the sum of
  all the inputs.

  Args:
    input: A `Tensor`. Must be one of the following types: `float32`.
      The local input to the sum.
    name: A name for the operation (optional).

  Returns:
    A `Tensor`. Has the same type as `input`.
    The sum of all the distributed inputs.
  """
  result = _op_def_lib.apply_op("CrossReplicaSum", input=input, name=name)
  return result


_ops.RegisterShape("CrossReplicaSum")(None)

def infeed_dequeue(dtype, shape, name=None):
  r"""A placeholder op for a value that will be fed into the computation.

  Args:
    dtype: A `tf.DType`. The type of elements in the tensor.
    shape: A `tf.TensorShape` or list of `ints`. The shape of the tensor.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `dtype`.
    A tensor that will be provided using the infeed mechanism.
  """
  result = _op_def_lib.apply_op("InfeedDequeue", dtype=dtype, shape=shape,
                                name=name)
  return result


_ops.RegisterShape("InfeedDequeue")(None)

def infeed_dequeue_tuple(dtypes, shapes, name=None):
  r"""A placeholder op for multiple values that will be fed into the computation

  simultaneously as an XLA tuple.

  Args:
    dtypes: A list of `tf.DTypes` that has length `>= 1`.
      The element types of each element in `outputs`.
    shapes: A list of shapes (each a `tf.TensorShape` or list of `ints`).
      The shapes of each tensor in `outputs`.
    name: A name for the operation (optional).

  Returns:
    A list of `Tensor` objects of type `dtypes`.
    A list of tensors that will be provided using the infeed mechanism.
  """
  result = _op_def_lib.apply_op("InfeedDequeueTuple", dtypes=dtypes,
                                shapes=shapes, name=name)
  return result


_ops.RegisterShape("InfeedDequeueTuple")(None)

def infeed_enqueue(input, shape=None, device_ordinal=None, name=None):
  r"""An op which feeds a single Tensor value into the computation.

  Args:
    input: A `Tensor`.
      A tensor that will be provided using the infeed mechanism.
    shape: An optional `tf.TensorShape` or list of `ints`. Defaults to `[]`.
      The shape of the tensor.
    device_ordinal: An optional `int`. Defaults to `-1`.
      The TPU device to use. This should be -1 when the Op
      is running on a TPU device, and >= 0 when the Op is running on the CPU
      device.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  result = _op_def_lib.apply_op("InfeedEnqueue", input=input, shape=shape,
                                device_ordinal=device_ordinal, name=name)
  return result


_ops.RegisterShape("InfeedEnqueue")(None)

def infeed_enqueue_tuple(inputs, shapes, device_ordinal=None, name=None):
  r"""An op which feeds multiple Tensor values into the computation as an XLA tuple.

  Args:
    inputs: A list of `Tensor` objects.
      A list of tensors that will be provided using the infeed mechanism.
    shapes: A list of shapes (each a `tf.TensorShape` or list of `ints`).
      The shapes of each tensor in `inputs`.
    device_ordinal: An optional `int`. Defaults to `-1`.
      The TPU device to use. This should be -1 when the Op
      is running on a TPU device, and >= 0 when the Op is running on the CPU
      device.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  result = _op_def_lib.apply_op("InfeedEnqueueTuple", inputs=inputs,
                                shapes=shapes, device_ordinal=device_ordinal,
                                name=name)
  return result


_ops.RegisterShape("InfeedEnqueueTuple")(None)

def outfeed_dequeue(dtype, shape, device_ordinal=None, name=None):
  r"""Retrieves a single tensor from the computation outfeed.  This operation will

  block indefinitely until data is available.

  Args:
    dtype: A `tf.DType`. The type of elements in the tensor.
    shape: A `tf.TensorShape` or list of `ints`. The shape of the tensor.
    device_ordinal: An optional `int`. Defaults to `-1`.
      The TPU device to use. This should be -1 when the Op
      is running on a TPU device, and >= 0 when the Op is running on the CPU
      device.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `dtype`.
    A tensor that will be read from the device outfeed.
  """
  result = _op_def_lib.apply_op("OutfeedDequeue", dtype=dtype, shape=shape,
                                device_ordinal=device_ordinal, name=name)
  return result


_ops.RegisterShape("OutfeedDequeue")(None)

def outfeed_dequeue_tuple(dtypes, shapes, device_ordinal=None, name=None):
  r"""Retrieve multiple values that will be emitted by the computation as an XLA

  tuple.  This operations will block indefinitely until data is available.
  Output `i` corresponds to XLA tuple element `i`.

  Args:
    dtypes: A list of `tf.DTypes` that has length `>= 1`.
      The element types of each element in `outputs`.
    shapes: A list of shapes (each a `tf.TensorShape` or list of `ints`).
      The shapes of each tensor in `outputs`.
    device_ordinal: An optional `int`. Defaults to `-1`.
      The TPU device to use. This should be -1 when the Op
      is running on a TPU device, and >= 0 when the Op is running on the CPU
      device.
    name: A name for the operation (optional).

  Returns:
    A list of `Tensor` objects of type `dtypes`.
    A list of tensors that will be read from the outfeed.
  """
  result = _op_def_lib.apply_op("OutfeedDequeueTuple", dtypes=dtypes,
                                shapes=shapes, device_ordinal=device_ordinal,
                                name=name)
  return result


_ops.RegisterShape("OutfeedDequeueTuple")(None)

def outfeed_enqueue(input, name=None):
  r"""An op which emits a single Tensor value from an XLA computation.

  Args:
    input: A `Tensor`. A tensor that will be inserted into the outfeed queue.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  result = _op_def_lib.apply_op("OutfeedEnqueue", input=input, name=name)
  return result


_ops.RegisterShape("OutfeedEnqueue")(None)

def outfeed_enqueue_tuple(inputs, name=None):
  r"""An op which emits multiple Tensor values from an XLA computation.

  Args:
    inputs: A list of `Tensor` objects.
      A list of tensors that will be inserted into the outfeed queue as an
      XLA tuple.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  result = _op_def_lib.apply_op("OutfeedEnqueueTuple", inputs=inputs,
                                name=name)
  return result


_ops.RegisterShape("OutfeedEnqueueTuple")(None)

def shutdown_distributed_tpu(name=None):
  r"""An op that shuts down a running distributed TPU system. The Op returns

  an error if no system is running.

  Args:
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  result = _op_def_lib.apply_op("ShutdownDistributedTPU", name=name)
  return result


_ops.RegisterShape("ShutdownDistributedTPU")(None)

def tpu_replicate(inputs, broadcast_inputs, variables, computation,
                  num_replicas, output_types, global_tpu_id=None, name=None):
  r"""Runs replicated computations on a distributed TPU system.

  Args:
    inputs: A list of `Tensor` objects.
      the inputs to 'computation', flattened, in replica-major order.
    broadcast_inputs: A list of `Tensor` objects.
      additional arguments to broadcast to all replicas. The
      broadcast inputs are appended to the per-replica inputs when calling
      computation.
    variables: A list of `Tensor` objects with type `resource`.
    computation: A function decorated with @Defun.
      a function containing the computation to run.
    num_replicas: An `int` that is `>= 1`.
      the number of replicas of the computation to run.
    output_types: A list of `tf.DTypes`.
      the types of the outputs of 'computation'.
    global_tpu_id: An optional list of `ints`. Defaults to `[]`.
      map from device to global tpu id.
    name: A name for the operation (optional).

  Returns:
    A list of `Tensor` objects of type `output_types`.
    the outputs of 'computation'.
  """
  result = _op_def_lib.apply_op("TPUReplicate", inputs=inputs,
                                broadcast_inputs=broadcast_inputs,
                                variables=variables, computation=computation,
                                num_replicas=num_replicas,
                                output_types=output_types,
                                global_tpu_id=global_tpu_id, name=name)
  return result


_ops.RegisterShape("TPUReplicate")(None)

def tpu_replicated_input(inputs, name=None):
  r"""Operator that connects N unreplicated inputs to an N-way replicated TPU computation.

  Args:
    inputs: A list of at least 1 `Tensor` objects with the same type.
    name: A name for the operation (optional).

  Returns:
    A `Tensor`. Has the same type as `inputs`.
  """
  result = _op_def_lib.apply_op("TPUReplicatedInput", inputs=inputs,
                                name=name)
  return result


_ops.RegisterShape("TPUReplicatedInput")(None)

def tpu_replicated_output(input, num_replicas, name=None):
  r"""Operator that connects the output of an N-way replicated TPU computation to N separate outputs.

  Args:
    input: A `Tensor`.
    num_replicas: An `int` that is `>= 1`.
    name: A name for the operation (optional).

  Returns:
    A list of `num_replicas` `Tensor` objects with the same type as `input`.
  """
  result = _op_def_lib.apply_op("TPUReplicatedOutput", input=input,
                                num_replicas=num_replicas, name=name)
  return result


_ops.RegisterShape("TPUReplicatedOutput")(None)
def _InitOpDefLibrary(op_list_proto_bytes):
  op_list = _op_def_pb2.OpList()
  op_list.ParseFromString(op_list_proto_bytes)
  _op_def_registry.register_op_list(op_list)
  op_def_lib = _op_def_library.OpDefLibrary()
  op_def_lib.add_op_list(op_list)
  return op_def_lib


# op {
#   name: "ConfigureDistributedTPU"
#   output_arg {
#     name: "global_tpu_array"
#     type: DT_INT32
#   }
#   attr {
#     name: "embedding_config"
#     type: "string"
#     default_value {
#       s: ""
#     }
#   }
#   is_stateful: true
# }
# op {
#   name: "CrossReplicaSum"
#   input_arg {
#     name: "input"
#     type_attr: "T"
#   }
#   output_arg {
#     name: "output"
#     type_attr: "T"
#   }
#   attr {
#     name: "T"
#     type: "type"
#     allowed_values {
#       list {
#         type: DT_FLOAT
#       }
#     }
#   }
# }
# op {
#   name: "InfeedDequeue"
#   output_arg {
#     name: "output"
#     type_attr: "dtype"
#   }
#   attr {
#     name: "dtype"
#     type: "type"
#   }
#   attr {
#     name: "shape"
#     type: "shape"
#   }
#   is_stateful: true
# }
# op {
#   name: "InfeedDequeueTuple"
#   output_arg {
#     name: "outputs"
#     type_list_attr: "dtypes"
#   }
#   attr {
#     name: "dtypes"
#     type: "list(type)"
#     has_minimum: true
#     minimum: 1
#   }
#   attr {
#     name: "shapes"
#     type: "list(shape)"
#   }
#   is_stateful: true
# }
# op {
#   name: "InfeedEnqueue"
#   input_arg {
#     name: "input"
#     type_attr: "dtype"
#   }
#   attr {
#     name: "dtype"
#     type: "type"
#   }
#   attr {
#     name: "shape"
#     type: "shape"
#     default_value {
#       shape {
#       }
#     }
#   }
#   attr {
#     name: "device_ordinal"
#     type: "int"
#     default_value {
#       i: -1
#     }
#   }
#   is_stateful: true
# }
# op {
#   name: "InfeedEnqueueTuple"
#   input_arg {
#     name: "inputs"
#     type_list_attr: "dtypes"
#   }
#   attr {
#     name: "dtypes"
#     type: "list(type)"
#     has_minimum: true
#     minimum: 1
#   }
#   attr {
#     name: "shapes"
#     type: "list(shape)"
#   }
#   attr {
#     name: "device_ordinal"
#     type: "int"
#     default_value {
#       i: -1
#     }
#   }
#   is_stateful: true
# }
# op {
#   name: "OutfeedDequeue"
#   output_arg {
#     name: "output"
#     type_attr: "dtype"
#   }
#   attr {
#     name: "dtype"
#     type: "type"
#   }
#   attr {
#     name: "shape"
#     type: "shape"
#   }
#   attr {
#     name: "device_ordinal"
#     type: "int"
#     default_value {
#       i: -1
#     }
#   }
#   is_stateful: true
# }
# op {
#   name: "OutfeedDequeueTuple"
#   output_arg {
#     name: "outputs"
#     type_list_attr: "dtypes"
#   }
#   attr {
#     name: "dtypes"
#     type: "list(type)"
#     has_minimum: true
#     minimum: 1
#   }
#   attr {
#     name: "shapes"
#     type: "list(shape)"
#   }
#   attr {
#     name: "device_ordinal"
#     type: "int"
#     default_value {
#       i: -1
#     }
#   }
#   is_stateful: true
# }
# op {
#   name: "OutfeedEnqueue"
#   input_arg {
#     name: "input"
#     type_attr: "dtype"
#   }
#   attr {
#     name: "dtype"
#     type: "type"
#   }
#   is_stateful: true
# }
# op {
#   name: "OutfeedEnqueueTuple"
#   input_arg {
#     name: "inputs"
#     type_list_attr: "dtypes"
#   }
#   attr {
#     name: "dtypes"
#     type: "list(type)"
#     has_minimum: true
#     minimum: 1
#   }
#   is_stateful: true
# }
# op {
#   name: "ShutdownDistributedTPU"
#   is_stateful: true
# }
# op {
#   name: "TPUReplicate"
#   input_arg {
#     name: "inputs"
#     type_list_attr: "Tinputs"
#   }
#   input_arg {
#     name: "broadcast_inputs"
#     type_list_attr: "Tbroadcast_inputs"
#   }
#   input_arg {
#     name: "variables"
#     type: DT_RESOURCE
#     number_attr: "NumVariables"
#   }
#   output_arg {
#     name: "outputs"
#     type_list_attr: "output_types"
#   }
#   attr {
#     name: "computation"
#     type: "func"
#   }
#   attr {
#     name: "num_replicas"
#     type: "int"
#     has_minimum: true
#     minimum: 1
#   }
#   attr {
#     name: "global_tpu_id"
#     type: "list(int)"
#     default_value {
#       list {
#       }
#     }
#   }
#   attr {
#     name: "Tinputs"
#     type: "list(type)"
#     has_minimum: true
#   }
#   attr {
#     name: "Tbroadcast_inputs"
#     type: "list(type)"
#     has_minimum: true
#   }
#   attr {
#     name: "NumVariables"
#     type: "int"
#     has_minimum: true
#   }
#   attr {
#     name: "output_types"
#     type: "list(type)"
#     has_minimum: true
#   }
#   is_stateful: true
# }
# op {
#   name: "TPUReplicatedInput"
#   input_arg {
#     name: "inputs"
#     type_attr: "T"
#     number_attr: "N"
#   }
#   output_arg {
#     name: "output"
#     type_attr: "T"
#   }
#   attr {
#     name: "N"
#     type: "int"
#     has_minimum: true
#     minimum: 1
#   }
#   attr {
#     name: "T"
#     type: "type"
#   }
# }
# op {
#   name: "TPUReplicatedOutput"
#   input_arg {
#     name: "input"
#     type_attr: "T"
#   }
#   output_arg {
#     name: "outputs"
#     type_attr: "T"
#     number_attr: "num_replicas"
#   }
#   attr {
#     name: "num_replicas"
#     type: "int"
#     has_minimum: true
#     minimum: 1
#   }
#   attr {
#     name: "T"
#     type: "type"
#   }
# }
_op_def_lib = _InitOpDefLibrary(b"\nR\n\027ConfigureDistributedTPU\032\024\n\020global_tpu_array\030\003\"\036\n\020embedding_config\022\006string\032\002\022\000\210\001\001\n<\n\017CrossReplicaSum\022\n\n\005input\"\001T\032\013\n\006output\"\001T\"\020\n\001T\022\004type:\005\n\0032\001\001\nB\n\rInfeedDequeue\032\017\n\006output\"\005dtype\"\r\n\005dtype\022\004type\"\016\n\005shape\022\005shape\210\001\001\n[\n\022InfeedDequeueTuple\032\021\n\007outputs2\006dtypes\"\030\n\006dtypes\022\nlist(type)(\0010\001\"\025\n\006shapes\022\013list(shape)\210\001\001\ni\n\rInfeedEnqueue\022\016\n\005input\"\005dtype\"\r\n\005dtype\022\004type\"\022\n\005shape\022\005shape\032\002:\000\"\"\n\016device_ordinal\022\003int\032\013\030\377\377\377\377\377\377\377\377\377\001\210\001\001\n~\n\022InfeedEnqueueTuple\022\020\n\006inputs2\006dtypes\"\030\n\006dtypes\022\nlist(type)(\0010\001\"\025\n\006shapes\022\013list(shape)\"\"\n\016device_ordinal\022\003int\032\013\030\377\377\377\377\377\377\377\377\377\001\210\001\001\ng\n\016OutfeedDequeue\032\017\n\006output\"\005dtype\"\r\n\005dtype\022\004type\"\016\n\005shape\022\005shape\"\"\n\016device_ordinal\022\003int\032\013\030\377\377\377\377\377\377\377\377\377\001\210\001\001\n\200\001\n\023OutfeedDequeueTuple\032\021\n\007outputs2\006dtypes\"\030\n\006dtypes\022\nlist(type)(\0010\001\"\025\n\006shapes\022\013list(shape)\"\"\n\016device_ordinal\022\003int\032\013\030\377\377\377\377\377\377\377\377\377\001\210\001\001\n2\n\016OutfeedEnqueue\022\016\n\005input\"\005dtype\"\r\n\005dtype\022\004type\210\001\001\nD\n\023OutfeedEnqueueTuple\022\020\n\006inputs2\006dtypes\"\030\n\006dtypes\022\nlist(type)(\0010\001\210\001\001\n\033\n\026ShutdownDistributedTPU\210\001\001\n\300\002\n\014TPUReplicate\022\021\n\006inputs2\007Tinputs\022%\n\020broadcast_inputs2\021Tbroadcast_inputs\022\033\n\tvariables\030\024*\014NumVariables\032\027\n\007outputs2\014output_types\"\023\n\013computation\022\004func\"\027\n\014num_replicas\022\003int(\0010\001\"\036\n\rglobal_tpu_id\022\tlist(int)\032\002\n\000\"\027\n\007Tinputs\022\nlist(type)(\001\"!\n\021Tbroadcast_inputs\022\nlist(type)(\001\"\025\n\014NumVariables\022\003int(\001\"\034\n\014output_types\022\nlist(type)(\001\210\001\001\nJ\n\022TPUReplicatedInput\022\016\n\006inputs\"\001T*\001N\032\013\n\006output\"\001T\"\014\n\001N\022\003int(\0010\001\"\t\n\001T\022\004type\na\n\023TPUReplicatedOutput\022\n\n\005input\"\001T\032\032\n\007outputs\"\001T*\014num_replicas\"\027\n\014num_replicas\022\003int(\0010\001\"\t\n\001T\022\004type")
