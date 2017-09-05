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

def batch_dataset(input_dataset, batch_size, output_types, output_shapes,
                  name=None):
  r"""Creates a dataset that batches `batch_size` elements from `input_dataset`.

  Args:
    input_dataset: A `Tensor` of type `resource`.
    batch_size: A `Tensor` of type `int64`.
      A scalar representing the number of elements to accumulate in a
      batch.
    output_types: A list of `tf.DTypes` that has length `>= 1`.
    output_shapes: A list of shapes (each a `tf.TensorShape` or list of `ints`) that has length `>= 1`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `resource`.
  """
  result = _op_def_lib.apply_op("BatchDataset", input_dataset=input_dataset,
                                batch_size=batch_size,
                                output_types=output_types,
                                output_shapes=output_shapes, name=name)
  return result



def cache_dataset(input_dataset, filename, output_types, output_shapes,
                  name=None):
  r"""Creates a dataset that caches elements from `input_dataset`.

  A CacheDataset will iterate over the input_dataset, and store tensors. If the
  cache already exists, the cache will be used. If the cache is inappropriate
  (e.g. cannot be opened, contains tensors of the wrong shape / size), an error
  will the returned when used.

  Args:
    input_dataset: A `Tensor` of type `resource`.
    filename: A `Tensor` of type `string`.
      A path on the filesystem where we should cache the dataset. Note: this
      will be a directory.
    output_types: A list of `tf.DTypes` that has length `>= 1`.
    output_shapes: A list of shapes (each a `tf.TensorShape` or list of `ints`) that has length `>= 1`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `resource`.
  """
  result = _op_def_lib.apply_op("CacheDataset", input_dataset=input_dataset,
                                filename=filename, output_types=output_types,
                                output_shapes=output_shapes, name=name)
  return result



def concatenate_dataset(input_dataset, another_dataset, output_types,
                        output_shapes, name=None):
  r"""Creates a dataset that concatenates `input_dataset` with `another_dataset`.

  Args:
    input_dataset: A `Tensor` of type `resource`.
    another_dataset: A `Tensor` of type `resource`.
    output_types: A list of `tf.DTypes` that has length `>= 1`.
    output_shapes: A list of shapes (each a `tf.TensorShape` or list of `ints`) that has length `>= 1`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `resource`.
  """
  result = _op_def_lib.apply_op("ConcatenateDataset",
                                input_dataset=input_dataset,
                                another_dataset=another_dataset,
                                output_types=output_types,
                                output_shapes=output_shapes, name=name)
  return result



def dense_to_sparse_batch_dataset(input_dataset, batch_size, row_shape,
                                  output_types, output_shapes, name=None):
  r"""Creates a dataset that yields a SparseTensor for each element of the input.

  Args:
    input_dataset: A `Tensor` of type `resource`.
      A handle to an input dataset. Must have a single component.
    batch_size: A `Tensor` of type `int64`.
      A scalar representing the number of elements to accumulate in a
      batch.
    row_shape: A `Tensor` of type `int64`.
      A vector representing the dense shape of each row in the produced
      SparseTensor.
    output_types: A list of `tf.DTypes` that has length `>= 1`.
    output_shapes: A list of shapes (each a `tf.TensorShape` or list of `ints`) that has length `>= 1`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `resource`.
  """
  result = _op_def_lib.apply_op("DenseToSparseBatchDataset",
                                input_dataset=input_dataset,
                                batch_size=batch_size, row_shape=row_shape,
                                output_types=output_types,
                                output_shapes=output_shapes, name=name)
  return result



def filter_dataset(input_dataset, other_arguments, predicate, output_types,
                   output_shapes, name=None):
  r"""Creates a dataset containing elements of `input_dataset` matching `predicate`.

  The `predicate` function must return a scalar boolean and accept the
  following arguments:

  * One tensor for each component of an element of `input_dataset`.
  * One tensor for each value in `other_arguments`.

  Args:
    input_dataset: A `Tensor` of type `resource`.
    other_arguments: A list of `Tensor` objects.
      A list of tensors, typically values that were captured when
      building a closure for `predicate`.
    predicate: A function decorated with @Defun.
      A function returning a scalar boolean.
    output_types: A list of `tf.DTypes` that has length `>= 1`.
    output_shapes: A list of shapes (each a `tf.TensorShape` or list of `ints`) that has length `>= 1`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `resource`.
  """
  result = _op_def_lib.apply_op("FilterDataset", input_dataset=input_dataset,
                                other_arguments=other_arguments,
                                predicate=predicate,
                                output_types=output_types,
                                output_shapes=output_shapes, name=name)
  return result



def fixed_length_record_dataset(filenames, header_bytes, record_bytes,
                                footer_bytes, name=None):
  r"""Creates a dataset that emits the records from one or more binary files.

  Args:
    filenames: A `Tensor` of type `string`.
      A scalar or a vector containing the name(s) of the file(s) to be
      read.
    header_bytes: A `Tensor` of type `int64`.
      A scalar representing the number of bytes to skip at the
      beginning of a file.
    record_bytes: A `Tensor` of type `int64`.
      A scalar representing the number of bytes in each record.
    footer_bytes: A `Tensor` of type `int64`.
      A scalar representing the number of bytes to skip at the end
      of a file.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `resource`.
  """
  result = _op_def_lib.apply_op("FixedLengthRecordDataset",
                                filenames=filenames,
                                header_bytes=header_bytes,
                                record_bytes=record_bytes,
                                footer_bytes=footer_bytes, name=name)
  return result



def flat_map_dataset(input_dataset, other_arguments, f, output_types,
                     output_shapes, name=None):
  r"""Creates a dataset that applies `f` to the outputs of `input_dataset`.

  Unlike MapDataset, the `f` in FlatMapDataset is expected to return a
  Dataset resource, and FlatMapDataset will flatten successive results
  into a single Dataset.

  Args:
    input_dataset: A `Tensor` of type `resource`.
    other_arguments: A list of `Tensor` objects.
    f: A function decorated with @Defun.
      A function mapping elements of `input_dataset`, concatenated with
      `other_arguments`, to a Dataset resource that contains elements matching
      `output_types` and `output_shapes`.
    output_types: A list of `tf.DTypes` that has length `>= 1`.
    output_shapes: A list of shapes (each a `tf.TensorShape` or list of `ints`) that has length `>= 1`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `resource`.
  """
  result = _op_def_lib.apply_op("FlatMapDataset", input_dataset=input_dataset,
                                other_arguments=other_arguments, f=f,
                                output_types=output_types,
                                output_shapes=output_shapes, name=name)
  return result



def group_by_window_dataset(input_dataset, key_func_other_arguments,
                            reduce_func_other_arguments, window_size,
                            key_func, reduce_func, output_types,
                            output_shapes, name=None):
  r"""Creates a dataset that computes a windowed group-by on `input_dataset`.

  // TODO(mrry): Support non-int64 keys.

  Args:
    input_dataset: A `Tensor` of type `resource`.
    key_func_other_arguments: A list of `Tensor` objects.
    reduce_func_other_arguments: A list of `Tensor` objects.
    window_size: A `Tensor` of type `int64`.
    key_func: A function decorated with @Defun.
      A function mapping an element of `input_dataset`, concatenated
      with `key_func_other_arguments` to a scalar value of type DT_INT64.
    reduce_func: A function decorated with @Defun.
    output_types: A list of `tf.DTypes` that has length `>= 1`.
    output_shapes: A list of shapes (each a `tf.TensorShape` or list of `ints`) that has length `>= 1`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `resource`.
  """
  result = _op_def_lib.apply_op("GroupByWindowDataset",
                                input_dataset=input_dataset,
                                key_func_other_arguments=key_func_other_arguments,
                                reduce_func_other_arguments=reduce_func_other_arguments,
                                window_size=window_size, key_func=key_func,
                                reduce_func=reduce_func,
                                output_types=output_types,
                                output_shapes=output_shapes, name=name)
  return result



def ignore_errors_dataset(input_dataset, output_types, output_shapes,
                          name=None):
  r"""Creates a dataset that contains the elements of `input_dataset` ignoring errors.

  Args:
    input_dataset: A `Tensor` of type `resource`.
    output_types: A list of `tf.DTypes` that has length `>= 1`.
    output_shapes: A list of shapes (each a `tf.TensorShape` or list of `ints`) that has length `>= 1`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `resource`.
  """
  result = _op_def_lib.apply_op("IgnoreErrorsDataset",
                                input_dataset=input_dataset,
                                output_types=output_types,
                                output_shapes=output_shapes, name=name)
  return result



def interleave_dataset(input_dataset, other_arguments, cycle_length,
                       block_length, f, output_types, output_shapes,
                       name=None):
  r"""Creates a dataset that applies `f` to the outputs of `input_dataset`.

  Unlike MapDataset, the `f` in InterleaveDataset is expected to return
  a Dataset resource, and InterleaveDataset will flatten successive
  results into a single Dataset. Unlike FlatMapDataset,
  InterleaveDataset will interleave sequences of up to `block_length`
  consecutive elements from `cycle_length` input elements.

  Args:
    input_dataset: A `Tensor` of type `resource`.
    other_arguments: A list of `Tensor` objects.
    cycle_length: A `Tensor` of type `int64`.
    block_length: A `Tensor` of type `int64`.
    f: A function decorated with @Defun.
      A function mapping elements of `input_dataset`, concatenated with
      `other_arguments`, to a Dataset resource that contains elements matching
      `output_types` and `output_shapes`.
    output_types: A list of `tf.DTypes` that has length `>= 1`.
    output_shapes: A list of shapes (each a `tf.TensorShape` or list of `ints`) that has length `>= 1`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `resource`.
  """
  result = _op_def_lib.apply_op("InterleaveDataset",
                                input_dataset=input_dataset,
                                other_arguments=other_arguments,
                                cycle_length=cycle_length,
                                block_length=block_length, f=f,
                                output_types=output_types,
                                output_shapes=output_shapes, name=name)
  return result



def iterator(shared_name, container, output_types, output_shapes, name=None):
  r"""A container for an iterator resource.

  Args:
    shared_name: A `string`.
    container: A `string`.
    output_types: A list of `tf.DTypes` that has length `>= 1`.
    output_shapes: A list of shapes (each a `tf.TensorShape` or list of `ints`) that has length `>= 1`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `resource`.
    A handle to the iterator that can be passed to a "MakeIterator"
    or "IteratorGetNext" op.
  """
  result = _op_def_lib.apply_op("Iterator", shared_name=shared_name,
                                container=container,
                                output_types=output_types,
                                output_shapes=output_shapes, name=name)
  return result



def iterator_dispose(iterator, name=None):
  r"""Releases any resources used by the given iterator.

  Args:
    iterator: A `Tensor` of type `resource`.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  result = _op_def_lib.apply_op("IteratorDispose", iterator=iterator,
                                name=name)
  return result



def iterator_from_string_handle(string_handle, name=None):
  r"""Converts the given string representing a handle to an iterator to a resource.

  Args:
    string_handle: A `Tensor` of type `string`.
      A string representation of the given handle.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `resource`. A handle to an iterator resource.
  """
  result = _op_def_lib.apply_op("IteratorFromStringHandle",
                                string_handle=string_handle, name=name)
  return result



def iterator_get_next(iterator, output_types, output_shapes, name=None):
  r"""Gets the next output from the given iterator.

  Args:
    iterator: A `Tensor` of type `resource`.
    output_types: A list of `tf.DTypes` that has length `>= 1`.
    output_shapes: A list of shapes (each a `tf.TensorShape` or list of `ints`) that has length `>= 1`.
    name: A name for the operation (optional).

  Returns:
    A list of `Tensor` objects of type `output_types`.
  """
  result = _op_def_lib.apply_op("IteratorGetNext", iterator=iterator,
                                output_types=output_types,
                                output_shapes=output_shapes, name=name)
  return result



def iterator_to_string_handle(resource_handle, name=None):
  r"""Converts the given `resource_handle` representing an iterator to a string.

  Args:
    resource_handle: A `Tensor` of type `resource`.
      A handle to an iterator resource.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `string`. A string representation of the given handle.
  """
  result = _op_def_lib.apply_op("IteratorToStringHandle",
                                resource_handle=resource_handle, name=name)
  return result



def make_iterator(dataset, iterator, name=None):
  r"""Makes a new iterator from the given `dataset` and stores it in `iterator`.

  This operation may be executed multiple times. Each execution will reset the
  iterator in `iterator` to the first element of `dataset`.

  Args:
    dataset: A `Tensor` of type `resource`.
    iterator: A `Tensor` of type `resource`.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  result = _op_def_lib.apply_op("MakeIterator", dataset=dataset,
                                iterator=iterator, name=name)
  return result



def map_dataset(input_dataset, other_arguments, f, output_types,
                output_shapes, name=None):
  r"""Creates a dataset that applies `f` to the outputs of `input_dataset`.

  Args:
    input_dataset: A `Tensor` of type `resource`.
    other_arguments: A list of `Tensor` objects.
    f: A function decorated with @Defun.
    output_types: A list of `tf.DTypes` that has length `>= 1`.
    output_shapes: A list of shapes (each a `tf.TensorShape` or list of `ints`) that has length `>= 1`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `resource`.
  """
  result = _op_def_lib.apply_op("MapDataset", input_dataset=input_dataset,
                                other_arguments=other_arguments, f=f,
                                output_types=output_types,
                                output_shapes=output_shapes, name=name)
  return result



def one_shot_iterator(dataset_factory, output_types, output_shapes,
                      container=None, shared_name=None, name=None):
  r"""Makes a "one-shot" iterator that can be iterated only once.

  A one-shot iterator bundles the logic for defining the dataset and
  the state of the iterator in a single op, which allows simple input
  pipelines to be defined without an additional initialization
  ("MakeIterator") step.

  One-shot iterators have the following limitations:

  * They do not support parameterization: all logic for creating the underlying
    dataset must be bundled in the `dataset_factory` function.
  * They are not resettable. Once a one-shot iterator reaches the end of its
    underlying dataset, subsequent "IteratorGetNext" operations on that
    iterator will always produce an `OutOfRange` error.

  For greater flexibility, use "Iterator" and "MakeIterator" to define
  an iterator using an arbitrary subgraph, which may capture tensors
  (including fed values) as parameters, and which may be reset multiple
  times by rerunning "MakeIterator".

  Args:
    dataset_factory: A function decorated with @Defun.
      A function of type `() -> DT_RESOURCE`, where the returned
      DT_RESOURCE is a handle to a dataset.
    output_types: A list of `tf.DTypes` that has length `>= 1`.
    output_shapes: A list of shapes (each a `tf.TensorShape` or list of `ints`) that has length `>= 1`.
    container: An optional `string`. Defaults to `""`.
    shared_name: An optional `string`. Defaults to `""`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `resource`.
    A handle to the iterator that can be passed to an "IteratorGetNext"
    op.
  """
  result = _op_def_lib.apply_op("OneShotIterator",
                                dataset_factory=dataset_factory,
                                output_types=output_types,
                                output_shapes=output_shapes,
                                container=container, shared_name=shared_name,
                                name=name)
  return result



def padded_batch_dataset(input_dataset, batch_size, padded_shapes,
                         padding_values, output_shapes, name=None):
  r"""Creates a dataset that batches and pads `batch_size` elements from the input.

  Args:
    input_dataset: A `Tensor` of type `resource`.
    batch_size: A `Tensor` of type `int64`.
      A scalar representing the number of elements to accumulate in a
      batch.
    padded_shapes: A list of at least 1 `Tensor` objects with type `int64`.
      A list of int64 tensors representing the desired padded shapes
      of the corresponding output components. These shapes may be partially
      specified, using `-1` to indicate that a particular dimension should be
      padded to the maximum size of all batch elements.
    padding_values: A list of `Tensor` objects.
      A list of scalars containing the padding value to use for
      each of the outputs.
    output_shapes: A list of shapes (each a `tf.TensorShape` or list of `ints`) that has length `>= 1`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `resource`.
  """
  result = _op_def_lib.apply_op("PaddedBatchDataset",
                                input_dataset=input_dataset,
                                batch_size=batch_size,
                                padded_shapes=padded_shapes,
                                padding_values=padding_values,
                                output_shapes=output_shapes, name=name)
  return result



def parallel_map_dataset(input_dataset, other_arguments, num_threads,
                         output_buffer_size, f, output_types, output_shapes,
                         name=None):
  r"""Creates a dataset that applies `f` to the outputs of `input_dataset`.

  Unlike a "MapDataset", which applies `f` sequentially, this dataset uses
  up to `num_threads` threads to process elements from `input_dataset`
  in parallel.

  Args:
    input_dataset: A `Tensor` of type `resource`.
    other_arguments: A list of `Tensor` objects.
    num_threads: A `Tensor` of type `int32`.
      The number of threads to use to process elements from
      `input_dataset`.
    output_buffer_size: A `Tensor` of type `int64`.
      The maximum number of output elements to buffer in an
      iterator over this dataset.
    f: A function decorated with @Defun.
    output_types: A list of `tf.DTypes` that has length `>= 1`.
    output_shapes: A list of shapes (each a `tf.TensorShape` or list of `ints`) that has length `>= 1`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `resource`.
  """
  result = _op_def_lib.apply_op("ParallelMapDataset",
                                input_dataset=input_dataset,
                                other_arguments=other_arguments,
                                num_threads=num_threads,
                                output_buffer_size=output_buffer_size, f=f,
                                output_types=output_types,
                                output_shapes=output_shapes, name=name)
  return result



def range_dataset(start, stop, step, output_types, output_shapes, name=None):
  r"""Creates a dataset with a range of values. Corresponds to python's xrange.

  Args:
    start: A `Tensor` of type `int64`.
      corresponds to start in python's xrange().
    stop: A `Tensor` of type `int64`.
      corresponds to stop in python's xrange().
    step: A `Tensor` of type `int64`.
      corresponds to step in python's xrange().
    output_types: A list of `tf.DTypes` that has length `>= 1`.
    output_shapes: A list of shapes (each a `tf.TensorShape` or list of `ints`) that has length `>= 1`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `resource`.
  """
  result = _op_def_lib.apply_op("RangeDataset", start=start, stop=stop,
                                step=step, output_types=output_types,
                                output_shapes=output_shapes, name=name)
  return result



def repeat_dataset(input_dataset, count, output_types, output_shapes,
                   name=None):
  r"""Creates a dataset that emits the outputs of `input_dataset` `count` times.

  Args:
    input_dataset: A `Tensor` of type `resource`.
    count: A `Tensor` of type `int64`.
      A scalar representing the number of times that `input_dataset` should
      be repeated. A value of `-1` indicates that it should be repeated infinitely.
    output_types: A list of `tf.DTypes` that has length `>= 1`.
    output_shapes: A list of shapes (each a `tf.TensorShape` or list of `ints`) that has length `>= 1`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `resource`.
  """
  result = _op_def_lib.apply_op("RepeatDataset", input_dataset=input_dataset,
                                count=count, output_types=output_types,
                                output_shapes=output_shapes, name=name)
  return result



def shuffle_dataset(input_dataset, buffer_size, seed, seed2, output_types,
                    output_shapes, name=None):
  r"""Creates a dataset that shuffles elements from `input_dataset` pseudorandomly.

  Args:
    input_dataset: A `Tensor` of type `resource`.
    buffer_size: A `Tensor` of type `int64`.
      The number of output elements to buffer in an iterator over
      this dataset. Compare with the `min_after_dequeue` attr when creating a
      `RandomShuffleQueue`.
    seed: A `Tensor` of type `int64`.
      A scalar seed for the random number generator. If either seed or
      seed2 is set to be non-zero, the random number generator is seeded
      by the given seed.  Otherwise, a random seed is used.
    seed2: A `Tensor` of type `int64`.
      A second scalar seed to avoid seed collision.
    output_types: A list of `tf.DTypes` that has length `>= 1`.
    output_shapes: A list of shapes (each a `tf.TensorShape` or list of `ints`) that has length `>= 1`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `resource`.
  """
  result = _op_def_lib.apply_op("ShuffleDataset", input_dataset=input_dataset,
                                buffer_size=buffer_size, seed=seed,
                                seed2=seed2, output_types=output_types,
                                output_shapes=output_shapes, name=name)
  return result



def skip_dataset(input_dataset, count, output_types, output_shapes,
                 name=None):
  r"""Creates a dataset that skips `count` elements from the `input_dataset`.

  Args:
    input_dataset: A `Tensor` of type `resource`.
    count: A `Tensor` of type `int64`.
      A scalar representing the number of elements from the `input_dataset`
      that should be skipped.  If count is -1, skips everything.
    output_types: A list of `tf.DTypes` that has length `>= 1`.
    output_shapes: A list of shapes (each a `tf.TensorShape` or list of `ints`) that has length `>= 1`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `resource`.
  """
  result = _op_def_lib.apply_op("SkipDataset", input_dataset=input_dataset,
                                count=count, output_types=output_types,
                                output_shapes=output_shapes, name=name)
  return result



def sparse_tensor_slice_dataset(indices, values, dense_shape, name=None):
  r"""Creates a dataset that splits a SparseTensor into elements row-wise.

  Args:
    indices: A `Tensor` of type `int64`.
    values: A `Tensor`.
    dense_shape: A `Tensor` of type `int64`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `resource`.
  """
  result = _op_def_lib.apply_op("SparseTensorSliceDataset", indices=indices,
                                values=values, dense_shape=dense_shape,
                                name=name)
  return result



def tf_record_dataset(filenames, compression_type, name=None):
  r"""Creates a dataset that emits the records from one or more TFRecord files.

  Args:
    filenames: A `Tensor` of type `string`.
      A scalar or vector containing the name(s) of the file(s) to be
      read.
    compression_type: A `Tensor` of type `string`.
      A scalar containing either (i) the empty string (no
      compression), (ii) "ZLIB", or (iii) "GZIP".
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `resource`.
  """
  result = _op_def_lib.apply_op("TFRecordDataset", filenames=filenames,
                                compression_type=compression_type, name=name)
  return result



def take_dataset(input_dataset, count, output_types, output_shapes,
                 name=None):
  r"""Creates a dataset that contains `count` elements from the `input_dataset`.

  Args:
    input_dataset: A `Tensor` of type `resource`.
    count: A `Tensor` of type `int64`.
      A scalar representing the number of elements from the `input_dataset`
      that should be taken. A value of `-1` indicates that all of `input_dataset`
      is taken.
    output_types: A list of `tf.DTypes` that has length `>= 1`.
    output_shapes: A list of shapes (each a `tf.TensorShape` or list of `ints`) that has length `>= 1`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `resource`.
  """
  result = _op_def_lib.apply_op("TakeDataset", input_dataset=input_dataset,
                                count=count, output_types=output_types,
                                output_shapes=output_shapes, name=name)
  return result



def tensor_dataset(components, output_shapes, name=None):
  r"""Creates a dataset that emits `components` as a tuple of tensors once.

  Args:
    components: A list of `Tensor` objects.
    output_shapes: A list of shapes (each a `tf.TensorShape` or list of `ints`) that has length `>= 1`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `resource`.
  """
  result = _op_def_lib.apply_op("TensorDataset", components=components,
                                output_shapes=output_shapes, name=name)
  return result



def tensor_slice_dataset(components, output_shapes, name=None):
  r"""Creates a dataset that emits each dim-0 slice of `components` once.

  Args:
    components: A list of `Tensor` objects.
    output_shapes: A list of shapes (each a `tf.TensorShape` or list of `ints`) that has length `>= 1`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `resource`.
  """
  result = _op_def_lib.apply_op("TensorSliceDataset", components=components,
                                output_shapes=output_shapes, name=name)
  return result



def text_line_dataset(filenames, compression_type, name=None):
  r"""Creates a dataset that emits the lines of one or more text files.

  Args:
    filenames: A `Tensor` of type `string`.
      A scalar or a vector containing the name(s) of the file(s) to be
      read.
    compression_type: A `Tensor` of type `string`.
      A scalar containing either (i) the empty string (no
      compression), (ii) "ZLIB", or (iii) "GZIP".
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `resource`.
  """
  result = _op_def_lib.apply_op("TextLineDataset", filenames=filenames,
                                compression_type=compression_type, name=name)
  return result



def zip_dataset(input_datasets, output_types, output_shapes, name=None):
  r"""Creates a dataset that zips together `input_datasets`.

  Args:
    input_datasets: A list of at least 1 `Tensor` objects with type `resource`.
    output_types: A list of `tf.DTypes` that has length `>= 1`.
    output_shapes: A list of shapes (each a `tf.TensorShape` or list of `ints`) that has length `>= 1`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `resource`.
  """
  result = _op_def_lib.apply_op("ZipDataset", input_datasets=input_datasets,
                                output_types=output_types,
                                output_shapes=output_shapes, name=name)
  return result


def _InitOpDefLibrary(op_list_proto_bytes):
  op_list = _op_def_pb2.OpList()
  op_list.ParseFromString(op_list_proto_bytes)
  _op_def_registry.register_op_list(op_list)
  op_def_lib = _op_def_library.OpDefLibrary()
  op_def_lib.add_op_list(op_list)
  return op_def_lib


# op {
#   name: "BatchDataset"
#   input_arg {
#     name: "input_dataset"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "batch_size"
#     type: DT_INT64
#   }
#   output_arg {
#     name: "handle"
#     type: DT_RESOURCE
#   }
#   attr {
#     name: "output_types"
#     type: "list(type)"
#     has_minimum: true
#     minimum: 1
#   }
#   attr {
#     name: "output_shapes"
#     type: "list(shape)"
#     has_minimum: true
#     minimum: 1
#   }
#   is_stateful: true
# }
# op {
#   name: "CacheDataset"
#   input_arg {
#     name: "input_dataset"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "filename"
#     type: DT_STRING
#   }
#   output_arg {
#     name: "handle"
#     type: DT_RESOURCE
#   }
#   attr {
#     name: "output_types"
#     type: "list(type)"
#     has_minimum: true
#     minimum: 1
#   }
#   attr {
#     name: "output_shapes"
#     type: "list(shape)"
#     has_minimum: true
#     minimum: 1
#   }
#   is_stateful: true
# }
# op {
#   name: "ConcatenateDataset"
#   input_arg {
#     name: "input_dataset"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "another_dataset"
#     type: DT_RESOURCE
#   }
#   output_arg {
#     name: "handle"
#     type: DT_RESOURCE
#   }
#   attr {
#     name: "output_types"
#     type: "list(type)"
#     has_minimum: true
#     minimum: 1
#   }
#   attr {
#     name: "output_shapes"
#     type: "list(shape)"
#     has_minimum: true
#     minimum: 1
#   }
#   is_stateful: true
# }
# op {
#   name: "DenseToSparseBatchDataset"
#   input_arg {
#     name: "input_dataset"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "batch_size"
#     type: DT_INT64
#   }
#   input_arg {
#     name: "row_shape"
#     type: DT_INT64
#   }
#   output_arg {
#     name: "handle"
#     type: DT_RESOURCE
#   }
#   attr {
#     name: "output_types"
#     type: "list(type)"
#     has_minimum: true
#     minimum: 1
#   }
#   attr {
#     name: "output_shapes"
#     type: "list(shape)"
#     has_minimum: true
#     minimum: 1
#   }
#   is_stateful: true
# }
# op {
#   name: "FilterDataset"
#   input_arg {
#     name: "input_dataset"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "other_arguments"
#     type_list_attr: "Targuments"
#   }
#   output_arg {
#     name: "handle"
#     type: DT_RESOURCE
#   }
#   attr {
#     name: "predicate"
#     type: "func"
#   }
#   attr {
#     name: "Targuments"
#     type: "list(type)"
#     has_minimum: true
#   }
#   attr {
#     name: "output_types"
#     type: "list(type)"
#     has_minimum: true
#     minimum: 1
#   }
#   attr {
#     name: "output_shapes"
#     type: "list(shape)"
#     has_minimum: true
#     minimum: 1
#   }
#   is_stateful: true
# }
# op {
#   name: "FixedLengthRecordDataset"
#   input_arg {
#     name: "filenames"
#     type: DT_STRING
#   }
#   input_arg {
#     name: "header_bytes"
#     type: DT_INT64
#   }
#   input_arg {
#     name: "record_bytes"
#     type: DT_INT64
#   }
#   input_arg {
#     name: "footer_bytes"
#     type: DT_INT64
#   }
#   output_arg {
#     name: "handle"
#     type: DT_RESOURCE
#   }
#   is_stateful: true
# }
# op {
#   name: "FlatMapDataset"
#   input_arg {
#     name: "input_dataset"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "other_arguments"
#     type_list_attr: "Targuments"
#   }
#   output_arg {
#     name: "handle"
#     type: DT_RESOURCE
#   }
#   attr {
#     name: "f"
#     type: "func"
#   }
#   attr {
#     name: "Targuments"
#     type: "list(type)"
#     has_minimum: true
#   }
#   attr {
#     name: "output_types"
#     type: "list(type)"
#     has_minimum: true
#     minimum: 1
#   }
#   attr {
#     name: "output_shapes"
#     type: "list(shape)"
#     has_minimum: true
#     minimum: 1
#   }
#   is_stateful: true
# }
# op {
#   name: "GroupByWindowDataset"
#   input_arg {
#     name: "input_dataset"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "key_func_other_arguments"
#     type_list_attr: "Tkey_func_other_arguments"
#   }
#   input_arg {
#     name: "reduce_func_other_arguments"
#     type_list_attr: "Treduce_func_other_arguments"
#   }
#   input_arg {
#     name: "window_size"
#     type: DT_INT64
#   }
#   output_arg {
#     name: "handle"
#     type: DT_RESOURCE
#   }
#   attr {
#     name: "key_func"
#     type: "func"
#   }
#   attr {
#     name: "reduce_func"
#     type: "func"
#   }
#   attr {
#     name: "Tkey_func_other_arguments"
#     type: "list(type)"
#     has_minimum: true
#   }
#   attr {
#     name: "Treduce_func_other_arguments"
#     type: "list(type)"
#     has_minimum: true
#   }
#   attr {
#     name: "output_types"
#     type: "list(type)"
#     has_minimum: true
#     minimum: 1
#   }
#   attr {
#     name: "output_shapes"
#     type: "list(shape)"
#     has_minimum: true
#     minimum: 1
#   }
#   is_stateful: true
# }
# op {
#   name: "IgnoreErrorsDataset"
#   input_arg {
#     name: "input_dataset"
#     type: DT_RESOURCE
#   }
#   output_arg {
#     name: "handle"
#     type: DT_RESOURCE
#   }
#   attr {
#     name: "output_types"
#     type: "list(type)"
#     has_minimum: true
#     minimum: 1
#   }
#   attr {
#     name: "output_shapes"
#     type: "list(shape)"
#     has_minimum: true
#     minimum: 1
#   }
#   is_stateful: true
# }
# op {
#   name: "InterleaveDataset"
#   input_arg {
#     name: "input_dataset"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "other_arguments"
#     type_list_attr: "Targuments"
#   }
#   input_arg {
#     name: "cycle_length"
#     type: DT_INT64
#   }
#   input_arg {
#     name: "block_length"
#     type: DT_INT64
#   }
#   output_arg {
#     name: "handle"
#     type: DT_RESOURCE
#   }
#   attr {
#     name: "f"
#     type: "func"
#   }
#   attr {
#     name: "Targuments"
#     type: "list(type)"
#     has_minimum: true
#   }
#   attr {
#     name: "output_types"
#     type: "list(type)"
#     has_minimum: true
#     minimum: 1
#   }
#   attr {
#     name: "output_shapes"
#     type: "list(shape)"
#     has_minimum: true
#     minimum: 1
#   }
#   is_stateful: true
# }
# op {
#   name: "Iterator"
#   output_arg {
#     name: "handle"
#     type: DT_RESOURCE
#   }
#   attr {
#     name: "shared_name"
#     type: "string"
#   }
#   attr {
#     name: "container"
#     type: "string"
#   }
#   attr {
#     name: "output_types"
#     type: "list(type)"
#     has_minimum: true
#     minimum: 1
#   }
#   attr {
#     name: "output_shapes"
#     type: "list(shape)"
#     has_minimum: true
#     minimum: 1
#   }
#   is_stateful: true
# }
# op {
#   name: "IteratorDispose"
#   input_arg {
#     name: "iterator"
#     type: DT_RESOURCE
#   }
#   is_stateful: true
# }
# op {
#   name: "IteratorFromStringHandle"
#   input_arg {
#     name: "string_handle"
#     type: DT_STRING
#   }
#   output_arg {
#     name: "resource_handle"
#     type: DT_RESOURCE
#   }
#   is_stateful: true
# }
# op {
#   name: "IteratorGetNext"
#   input_arg {
#     name: "iterator"
#     type: DT_RESOURCE
#   }
#   output_arg {
#     name: "components"
#     type_list_attr: "output_types"
#   }
#   attr {
#     name: "output_types"
#     type: "list(type)"
#     has_minimum: true
#     minimum: 1
#   }
#   attr {
#     name: "output_shapes"
#     type: "list(shape)"
#     has_minimum: true
#     minimum: 1
#   }
#   is_stateful: true
# }
# op {
#   name: "IteratorToStringHandle"
#   input_arg {
#     name: "resource_handle"
#     type: DT_RESOURCE
#   }
#   output_arg {
#     name: "string_handle"
#     type: DT_STRING
#   }
#   is_stateful: true
# }
# op {
#   name: "MakeIterator"
#   input_arg {
#     name: "dataset"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "iterator"
#     type: DT_RESOURCE
#   }
#   is_stateful: true
# }
# op {
#   name: "MapDataset"
#   input_arg {
#     name: "input_dataset"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "other_arguments"
#     type_list_attr: "Targuments"
#   }
#   output_arg {
#     name: "handle"
#     type: DT_RESOURCE
#   }
#   attr {
#     name: "f"
#     type: "func"
#   }
#   attr {
#     name: "Targuments"
#     type: "list(type)"
#     has_minimum: true
#   }
#   attr {
#     name: "output_types"
#     type: "list(type)"
#     has_minimum: true
#     minimum: 1
#   }
#   attr {
#     name: "output_shapes"
#     type: "list(shape)"
#     has_minimum: true
#     minimum: 1
#   }
#   is_stateful: true
# }
# op {
#   name: "OneShotIterator"
#   output_arg {
#     name: "handle"
#     type: DT_RESOURCE
#   }
#   attr {
#     name: "dataset_factory"
#     type: "func"
#   }
#   attr {
#     name: "output_types"
#     type: "list(type)"
#     has_minimum: true
#     minimum: 1
#   }
#   attr {
#     name: "output_shapes"
#     type: "list(shape)"
#     has_minimum: true
#     minimum: 1
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
#   name: "PaddedBatchDataset"
#   input_arg {
#     name: "input_dataset"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "batch_size"
#     type: DT_INT64
#   }
#   input_arg {
#     name: "padded_shapes"
#     type: DT_INT64
#     number_attr: "N"
#   }
#   input_arg {
#     name: "padding_values"
#     type_list_attr: "Toutput_types"
#   }
#   output_arg {
#     name: "handle"
#     type: DT_RESOURCE
#   }
#   attr {
#     name: "Toutput_types"
#     type: "list(type)"
#     has_minimum: true
#     minimum: 1
#   }
#   attr {
#     name: "output_shapes"
#     type: "list(shape)"
#     has_minimum: true
#     minimum: 1
#   }
#   attr {
#     name: "N"
#     type: "int"
#     has_minimum: true
#     minimum: 1
#   }
#   is_stateful: true
# }
# op {
#   name: "ParallelMapDataset"
#   input_arg {
#     name: "input_dataset"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "other_arguments"
#     type_list_attr: "Targuments"
#   }
#   input_arg {
#     name: "num_threads"
#     type: DT_INT32
#   }
#   input_arg {
#     name: "output_buffer_size"
#     type: DT_INT64
#   }
#   output_arg {
#     name: "handle"
#     type: DT_RESOURCE
#   }
#   attr {
#     name: "f"
#     type: "func"
#   }
#   attr {
#     name: "Targuments"
#     type: "list(type)"
#     has_minimum: true
#   }
#   attr {
#     name: "output_types"
#     type: "list(type)"
#     has_minimum: true
#     minimum: 1
#   }
#   attr {
#     name: "output_shapes"
#     type: "list(shape)"
#     has_minimum: true
#     minimum: 1
#   }
#   is_stateful: true
# }
# op {
#   name: "RangeDataset"
#   input_arg {
#     name: "start"
#     type: DT_INT64
#   }
#   input_arg {
#     name: "stop"
#     type: DT_INT64
#   }
#   input_arg {
#     name: "step"
#     type: DT_INT64
#   }
#   output_arg {
#     name: "handle"
#     type: DT_RESOURCE
#   }
#   attr {
#     name: "output_types"
#     type: "list(type)"
#     has_minimum: true
#     minimum: 1
#   }
#   attr {
#     name: "output_shapes"
#     type: "list(shape)"
#     has_minimum: true
#     minimum: 1
#   }
#   is_stateful: true
# }
# op {
#   name: "RepeatDataset"
#   input_arg {
#     name: "input_dataset"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "count"
#     type: DT_INT64
#   }
#   output_arg {
#     name: "handle"
#     type: DT_RESOURCE
#   }
#   attr {
#     name: "output_types"
#     type: "list(type)"
#     has_minimum: true
#     minimum: 1
#   }
#   attr {
#     name: "output_shapes"
#     type: "list(shape)"
#     has_minimum: true
#     minimum: 1
#   }
#   is_stateful: true
# }
# op {
#   name: "ShuffleDataset"
#   input_arg {
#     name: "input_dataset"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "buffer_size"
#     type: DT_INT64
#   }
#   input_arg {
#     name: "seed"
#     type: DT_INT64
#   }
#   input_arg {
#     name: "seed2"
#     type: DT_INT64
#   }
#   output_arg {
#     name: "handle"
#     type: DT_RESOURCE
#   }
#   attr {
#     name: "output_types"
#     type: "list(type)"
#     has_minimum: true
#     minimum: 1
#   }
#   attr {
#     name: "output_shapes"
#     type: "list(shape)"
#     has_minimum: true
#     minimum: 1
#   }
#   is_stateful: true
# }
# op {
#   name: "SkipDataset"
#   input_arg {
#     name: "input_dataset"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "count"
#     type: DT_INT64
#   }
#   output_arg {
#     name: "handle"
#     type: DT_RESOURCE
#   }
#   attr {
#     name: "output_types"
#     type: "list(type)"
#     has_minimum: true
#     minimum: 1
#   }
#   attr {
#     name: "output_shapes"
#     type: "list(shape)"
#     has_minimum: true
#     minimum: 1
#   }
#   is_stateful: true
# }
# op {
#   name: "SparseTensorSliceDataset"
#   input_arg {
#     name: "indices"
#     type: DT_INT64
#   }
#   input_arg {
#     name: "values"
#     type_attr: "Tvalues"
#   }
#   input_arg {
#     name: "dense_shape"
#     type: DT_INT64
#   }
#   output_arg {
#     name: "handle"
#     type: DT_RESOURCE
#   }
#   attr {
#     name: "Tvalues"
#     type: "type"
#   }
#   is_stateful: true
# }
# op {
#   name: "TFRecordDataset"
#   input_arg {
#     name: "filenames"
#     type: DT_STRING
#   }
#   input_arg {
#     name: "compression_type"
#     type: DT_STRING
#   }
#   output_arg {
#     name: "handle"
#     type: DT_RESOURCE
#   }
#   is_stateful: true
# }
# op {
#   name: "TakeDataset"
#   input_arg {
#     name: "input_dataset"
#     type: DT_RESOURCE
#   }
#   input_arg {
#     name: "count"
#     type: DT_INT64
#   }
#   output_arg {
#     name: "handle"
#     type: DT_RESOURCE
#   }
#   attr {
#     name: "output_types"
#     type: "list(type)"
#     has_minimum: true
#     minimum: 1
#   }
#   attr {
#     name: "output_shapes"
#     type: "list(shape)"
#     has_minimum: true
#     minimum: 1
#   }
#   is_stateful: true
# }
# op {
#   name: "TensorDataset"
#   input_arg {
#     name: "components"
#     type_list_attr: "Toutput_types"
#   }
#   output_arg {
#     name: "handle"
#     type: DT_RESOURCE
#   }
#   attr {
#     name: "Toutput_types"
#     type: "list(type)"
#     has_minimum: true
#     minimum: 1
#   }
#   attr {
#     name: "output_shapes"
#     type: "list(shape)"
#     has_minimum: true
#     minimum: 1
#   }
#   is_stateful: true
# }
# op {
#   name: "TensorSliceDataset"
#   input_arg {
#     name: "components"
#     type_list_attr: "Toutput_types"
#   }
#   output_arg {
#     name: "handle"
#     type: DT_RESOURCE
#   }
#   attr {
#     name: "Toutput_types"
#     type: "list(type)"
#     has_minimum: true
#     minimum: 1
#   }
#   attr {
#     name: "output_shapes"
#     type: "list(shape)"
#     has_minimum: true
#     minimum: 1
#   }
#   is_stateful: true
# }
# op {
#   name: "TextLineDataset"
#   input_arg {
#     name: "filenames"
#     type: DT_STRING
#   }
#   input_arg {
#     name: "compression_type"
#     type: DT_STRING
#   }
#   output_arg {
#     name: "handle"
#     type: DT_RESOURCE
#   }
#   is_stateful: true
# }
# op {
#   name: "ZipDataset"
#   input_arg {
#     name: "input_datasets"
#     type: DT_RESOURCE
#     number_attr: "N"
#   }
#   output_arg {
#     name: "handle"
#     type: DT_RESOURCE
#   }
#   attr {
#     name: "output_types"
#     type: "list(type)"
#     has_minimum: true
#     minimum: 1
#   }
#   attr {
#     name: "output_shapes"
#     type: "list(shape)"
#     has_minimum: true
#     minimum: 1
#   }
#   attr {
#     name: "N"
#     type: "int"
#     has_minimum: true
#     minimum: 1
#   }
#   is_stateful: true
# }
_op_def_lib = _InitOpDefLibrary(b"\n\202\001\n\014BatchDataset\022\021\n\rinput_dataset\030\024\022\016\n\nbatch_size\030\t\032\n\n\006handle\030\024\"\036\n\014output_types\022\nlist(type)(\0010\001\" \n\routput_shapes\022\013list(shape)(\0010\001\210\001\001\n\200\001\n\014CacheDataset\022\021\n\rinput_dataset\030\024\022\014\n\010filename\030\007\032\n\n\006handle\030\024\"\036\n\014output_types\022\nlist(type)(\0010\001\" \n\routput_shapes\022\013list(shape)(\0010\001\210\001\001\n\215\001\n\022ConcatenateDataset\022\021\n\rinput_dataset\030\024\022\023\n\017another_dataset\030\024\032\n\n\006handle\030\024\"\036\n\014output_types\022\nlist(type)(\0010\001\" \n\routput_shapes\022\013list(shape)(\0010\001\210\001\001\n\236\001\n\031DenseToSparseBatchDataset\022\021\n\rinput_dataset\030\024\022\016\n\nbatch_size\030\t\022\r\n\trow_shape\030\t\032\n\n\006handle\030\024\"\036\n\014output_types\022\nlist(type)(\0010\001\" \n\routput_shapes\022\013list(shape)(\0010\001\210\001\001\n\301\001\n\rFilterDataset\022\021\n\rinput_dataset\030\024\022\035\n\017other_arguments2\nTarguments\032\n\n\006handle\030\024\"\021\n\tpredicate\022\004func\"\032\n\nTarguments\022\nlist(type)(\001\"\036\n\014output_types\022\nlist(type)(\0010\001\" \n\routput_shapes\022\013list(shape)(\0010\001\210\001\001\nn\n\030FixedLengthRecordDataset\022\r\n\tfilenames\030\007\022\020\n\014header_bytes\030\t\022\020\n\014record_bytes\030\t\022\020\n\014footer_bytes\030\t\032\n\n\006handle\030\024\210\001\001\n\272\001\n\016FlatMapDataset\022\021\n\rinput_dataset\030\024\022\035\n\017other_arguments2\nTarguments\032\n\n\006handle\030\024\"\t\n\001f\022\004func\"\032\n\nTarguments\022\nlist(type)(\001\"\036\n\014output_types\022\nlist(type)(\0010\001\" \n\routput_shapes\022\013list(shape)(\0010\001\210\001\001\n\377\002\n\024GroupByWindowDataset\022\021\n\rinput_dataset\030\024\0225\n\030key_func_other_arguments2\031Tkey_func_other_arguments\022;\n\033reduce_func_other_arguments2\034Treduce_func_other_arguments\022\017\n\013window_size\030\t\032\n\n\006handle\030\024\"\020\n\010key_func\022\004func\"\023\n\013reduce_func\022\004func\")\n\031Tkey_func_other_arguments\022\nlist(type)(\001\",\n\034Treduce_func_other_arguments\022\nlist(type)(\001\"\036\n\014output_types\022\nlist(type)(\0010\001\" \n\routput_shapes\022\013list(shape)(\0010\001\210\001\001\ny\n\023IgnoreErrorsDataset\022\021\n\rinput_dataset\030\024\032\n\n\006handle\030\024\"\036\n\014output_types\022\nlist(type)(\0010\001\" \n\routput_shapes\022\013list(shape)(\0010\001\210\001\001\n\341\001\n\021InterleaveDataset\022\021\n\rinput_dataset\030\024\022\035\n\017other_arguments2\nTarguments\022\020\n\014cycle_length\030\t\022\020\n\014block_length\030\t\032\n\n\006handle\030\024\"\t\n\001f\022\004func\"\032\n\nTarguments\022\nlist(type)(\001\"\036\n\014output_types\022\nlist(type)(\0010\001\" \n\routput_shapes\022\013list(shape)(\0010\001\210\001\001\n\207\001\n\010Iterator\032\n\n\006handle\030\024\"\025\n\013shared_name\022\006string\"\023\n\tcontainer\022\006string\"\036\n\014output_types\022\nlist(type)(\0010\001\" \n\routput_shapes\022\013list(shape)(\0010\001\210\001\001\n\"\n\017IteratorDispose\022\014\n\010iterator\030\024\210\001\001\nE\n\030IteratorFromStringHandle\022\021\n\rstring_handle\030\007\032\023\n\017resource_handle\030\024\210\001\001\n\200\001\n\017IteratorGetNext\022\014\n\010iterator\030\024\032\032\n\ncomponents2\014output_types\"\036\n\014output_types\022\nlist(type)(\0010\001\" \n\routput_shapes\022\013list(shape)(\0010\001\210\001\001\nC\n\026IteratorToStringHandle\022\023\n\017resource_handle\030\024\032\021\n\rstring_handle\030\007\210\001\001\n,\n\014MakeIterator\022\013\n\007dataset\030\024\022\014\n\010iterator\030\024\210\001\001\n\266\001\n\nMapDataset\022\021\n\rinput_dataset\030\024\022\035\n\017other_arguments2\nTarguments\032\n\n\006handle\030\024\"\t\n\001f\022\004func\"\032\n\nTarguments\022\nlist(type)(\001\"\036\n\014output_types\022\nlist(type)(\0010\001\" \n\routput_shapes\022\013list(shape)(\0010\001\210\001\001\n\257\001\n\017OneShotIterator\032\n\n\006handle\030\024\"\027\n\017dataset_factory\022\004func\"\036\n\014output_types\022\nlist(type)(\0010\001\" \n\routput_shapes\022\013list(shape)(\0010\001\"\027\n\tcontainer\022\006string\032\002\022\000\"\031\n\013shared_name\022\006string\032\002\022\000\210\001\001\n\316\001\n\022PaddedBatchDataset\022\021\n\rinput_dataset\030\024\022\016\n\nbatch_size\030\t\022\024\n\rpadded_shapes\030\t*\001N\022\037\n\016padding_values2\rToutput_types\032\n\n\006handle\030\024\"\037\n\rToutput_types\022\nlist(type)(\0010\001\" \n\routput_shapes\022\013list(shape)(\0010\001\"\014\n\001N\022\003int(\0010\001\210\001\001\n\347\001\n\022ParallelMapDataset\022\021\n\rinput_dataset\030\024\022\035\n\017other_arguments2\nTarguments\022\017\n\013num_threads\030\003\022\026\n\022output_buffer_size\030\t\032\n\n\006handle\030\024\"\t\n\001f\022\004func\"\032\n\nTarguments\022\nlist(type)(\001\"\036\n\014output_types\022\nlist(type)(\0010\001\" \n\routput_shapes\022\013list(shape)(\0010\001\210\001\001\n~\n\014RangeDataset\022\t\n\005start\030\t\022\010\n\004stop\030\t\022\010\n\004step\030\t\032\n\n\006handle\030\024\"\036\n\014output_types\022\nlist(type)(\0010\001\" \n\routput_shapes\022\013list(shape)(\0010\001\210\001\001\n~\n\rRepeatDataset\022\021\n\rinput_dataset\030\024\022\t\n\005count\030\t\032\n\n\006handle\030\024\"\036\n\014output_types\022\nlist(type)(\0010\001\" \n\routput_shapes\022\013list(shape)(\0010\001\210\001\001\n\232\001\n\016ShuffleDataset\022\021\n\rinput_dataset\030\024\022\017\n\013buffer_size\030\t\022\010\n\004seed\030\t\022\t\n\005seed2\030\t\032\n\n\006handle\030\024\"\036\n\014output_types\022\nlist(type)(\0010\001\" \n\routput_shapes\022\013list(shape)(\0010\001\210\001\001\n|\n\013SkipDataset\022\021\n\rinput_dataset\030\024\022\t\n\005count\030\t\032\n\n\006handle\030\024\"\036\n\014output_types\022\nlist(type)(\0010\001\" \n\routput_shapes\022\013list(shape)(\0010\001\210\001\001\nk\n\030SparseTensorSliceDataset\022\013\n\007indices\030\t\022\021\n\006values\"\007Tvalues\022\017\n\013dense_shape\030\t\032\n\n\006handle\030\024\"\017\n\007Tvalues\022\004type\210\001\001\nE\n\017TFRecordDataset\022\r\n\tfilenames\030\007\022\024\n\020compression_type\030\007\032\n\n\006handle\030\024\210\001\001\n|\n\013TakeDataset\022\021\n\rinput_dataset\030\024\022\t\n\005count\030\t\032\n\n\006handle\030\024\"\036\n\014output_types\022\nlist(type)(\0010\001\" \n\routput_shapes\022\013list(shape)(\0010\001\210\001\001\n~\n\rTensorDataset\022\033\n\ncomponents2\rToutput_types\032\n\n\006handle\030\024\"\037\n\rToutput_types\022\nlist(type)(\0010\001\" \n\routput_shapes\022\013list(shape)(\0010\001\210\001\001\n\203\001\n\022TensorSliceDataset\022\033\n\ncomponents2\rToutput_types\032\n\n\006handle\030\024\"\037\n\rToutput_types\022\nlist(type)(\0010\001\" \n\routput_shapes\022\013list(shape)(\0010\001\210\001\001\nE\n\017TextLineDataset\022\r\n\tfilenames\030\007\022\024\n\020compression_type\030\007\032\n\n\006handle\030\024\210\001\001\n\202\001\n\nZipDataset\022\025\n\016input_datasets\030\024*\001N\032\n\n\006handle\030\024\"\036\n\014output_types\022\nlist(type)(\0010\001\" \n\routput_shapes\022\013list(shape)(\0010\001\"\014\n\001N\022\003int(\0010\001\210\001\001")
