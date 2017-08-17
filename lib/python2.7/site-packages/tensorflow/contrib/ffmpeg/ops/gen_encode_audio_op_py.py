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

def encode_audio(sampled_audio, file_format, samples_per_second,
                 bits_per_second=None, name=None):
  r"""Processes a `Tensor` containing sampled audio with the number of channels

  and length of the audio specified by the dimensions of the `Tensor`. The
  audio is converted into a string that, when saved to disk, will be equivalent
  to the audio in the specified audio format.

  The input audio has one row of the tensor for each channel in the audio file.
  Each channel contains audio samples starting at the beginning of the audio and
  having `1/samples_per_second` time between them. The output file will contain
  all of the audio channels contained in the tensor.

  Args:
    sampled_audio: A `Tensor` of type `float32`.
      A rank 2 tensor containing all tracks of the audio. Dimension 0
      is time and dimension 1 is the channel.
    file_format: A `string`.
      A string describing the audio file format. This must be "wav".
    samples_per_second: An `int`.
      The number of samples per second that the audio should have.
    bits_per_second: An optional `int`. Defaults to `192000`.
      The approximate bitrate of the encoded audio file. This is
      ignored by the "wav" file format.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `string`. The binary audio file contents.
  """
  result = _op_def_lib.apply_op("EncodeAudio", sampled_audio=sampled_audio,
                                file_format=file_format,
                                samples_per_second=samples_per_second,
                                bits_per_second=bits_per_second, name=name)
  return result


def _InitOpDefLibrary(op_list_proto_bytes):
  op_list = _op_def_pb2.OpList()
  op_list.ParseFromString(op_list_proto_bytes)
  _op_def_registry.register_op_list(op_list)
  op_def_lib = _op_def_library.OpDefLibrary()
  op_def_lib.add_op_list(op_list)
  return op_def_lib


# op {
#   name: "EncodeAudio"
#   input_arg {
#     name: "sampled_audio"
#     type: DT_FLOAT
#   }
#   output_arg {
#     name: "contents"
#     type: DT_STRING
#   }
#   attr {
#     name: "file_format"
#     type: "string"
#   }
#   attr {
#     name: "samples_per_second"
#     type: "int"
#   }
#   attr {
#     name: "bits_per_second"
#     type: "int"
#     default_value {
#       i: 192000
#     }
#   }
# }
_op_def_lib = _InitOpDefLibrary(b"\n~\n\013EncodeAudio\022\021\n\rsampled_audio\030\001\032\014\n\010contents\030\007\"\025\n\013file_format\022\006string\"\031\n\022samples_per_second\022\003int\"\034\n\017bits_per_second\022\003int\032\004\030\200\334\013")
