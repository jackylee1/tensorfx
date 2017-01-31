# Copyright 2016 TensorLab. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing permissions and limitations under
# the License.

# _dataset.py
# Implementation of DataSet and DataSource classes.


class DataSet(object):
  """A class representing data to be used within a job.

  A DataSet contains one or more DataSource instances, each associated with a name.
  """
  def __init__(self, datasources, schema, metadata=None, features=None):
    """Initializes a DataSet with the specified DataSource instances.

    Arguments:
      datasources: a set of named DataSource instances.
      schema: the description of the source data.
      metadata: additional per-field information associated with the data.
      features: the optional description of the transformed data.
    """
    self._datasources = datasources
    self._schema = schema
    self._metadata = metadata
    self._features = features

  @classmethod
  def create(cls, schema, *args, **kwargs):
    """Creates a DataSet with the specified DataSource instances.

    Arguments:
      schema: the description of the source data.
      args: A list of named DataSource instances.
      kwargs: optional information, such as metadata and features.
    Returns:
      A DataSet containing the specified DataSource instances.
    Raises:
      ValueError if the list of DataSources is empty, or not a homogeneous set of instances.
    """
    if not len(args):
      raise ValueError('One or more DataSource instances must be specified.')
    if not isinstance(args[0], DataSource) or \
       not all(map(lambda ds: type(ds) == type(args[0]), args)):
      raise ValueError('All the listed DataSource instances must be of the same type.')

    datasources = dict(map(lambda ds: (ds.name, ds), args))
    return cls(datasources, schema, kwargs.get('metadata', None), kwargs.get('features', None))

  def __getattr__(self, attr):
    """Retrieves a named DataSource within the DataSet.

    Arguments:
      attr: the name of the DataSource to retrieve.
    Returns:
      The DataSource if there is one with the specified name.
    Raises:
      AttributeError if no such DataSource exists.
    """
    datasource = self._datasources.get(attr, None)
    if datasource is None:
      raise AttributeError
    return datasource

  def __getitem__(self, index):
    """Retrieves a named DataSource within the DataSet.

    Arguments:
      index: the name of the DataSource to retrieve.
    Returns:
      The DataSource if there is one with the specified name; None otherwise.
    """
    return self._datasources.get(index, None)

  @property
  def schema(self):
    """Retrives the schema associated with the DataSet.
    """
    return self._schema

  @property
  def metadata(self):
    """Retrives the metadata associated with the DataSet.
    """
    return self._metadata

  @property
  def features(self):
    """Retrives the features defined with the DataSet.
    """
    return self._features


class DataSource(object):
  """A base class representing data that can be read for use in a job.
  """
  def __init__(self, name):
    """Initializes an instance of a DataSource.

    Arguments:
      name: the name of the DataSource.
    """
    self._name = name

  @property
  def name(self):
    """Retrieves the name of the DataSource.
    """
    return self._name
