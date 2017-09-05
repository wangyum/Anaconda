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

def decode_audio(contents, file_format, samples_per_second, channel_count,
                 name=None):
  r"""Processes the contents of an audio file into a tensor using FFmpeg to decode

  the file.

  One row of the tensor is created for each channel in the audio file. Each
  channel contains audio samples starting at the beginning of the audio and
  having `1/samples_per_second` time between them. If the `channel_count` is
  different from the contents of the file, channels will be merged or created.

  Args:
    contents: A `Tensor` of type `string`. The binary audio file contents.
    file_format: A `string`.
      A string describing the audio file format. This can be "wav" or
      "mp3".
    samples_per_second: An `int`.
      The number of samples per second that the audio should have.
    channel_count: An `int`. The number of channels of audio to read.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `float32`.
    A rank 2 tensor containing all tracks of the audio. Dimension 0
    is time and dimension 1 is the channel. If ffmpeg fails to decode the audio
    then an empty tensor will be returned.
  """
  result = _op_def_lib.apply_op("DecodeAudio", contents=contents,
                                file_format=file_format,
                                samples_per_second=samples_per_second,
                                channel_count=channel_count, name=name)
  return result


def _InitOpDefLibrary(op_list_proto_bytes):
  op_list = _op_def_pb2.OpList()
  op_list.ParseFromString(op_list_proto_bytes)
  _op_def_registry.register_op_list(op_list)
  op_def_lib = _op_def_library.OpDefLibrary()
  op_def_lib.add_op_list(op_list)
  return op_def_lib


# op {
#   name: "DecodeAudio"
#   input_arg {
#     name: "contents"
#     type: DT_STRING
#   }
#   output_arg {
#     name: "sampled_audio"
#     type: DT_FLOAT
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
#     name: "channel_count"
#     type: "int"
#   }
# }
_op_def_lib = _InitOpDefLibrary(b"\nv\n\013DecodeAudio\022\014\n\010contents\030\007\032\021\n\rsampled_audio\030\001\"\025\n\013file_format\022\006string\"\031\n\022samples_per_second\022\003int\"\024\n\rchannel_count\022\003int")
