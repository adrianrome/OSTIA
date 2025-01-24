Metadata
============
Filter
-----------------

IFilter
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.metadata.filter.filter_interface.IFilter.filter

RecordDeleted
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.metadata.filter.record_deleted.RecordDeleted.filter

Forwarder
-----------------

FileSystemForwarder
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.metadata.forwarder.filesystem_forwarder.FileSystemForwarder.forward

.. autofunction:: src.metadata.forwarder.filesystem_forwarder.FileSystemForwarder._get_subfolder

IForwarder
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.metadata.forwarder.forwarder_interface.IForwarder.forward

MongoDbForwarder
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.metadata.forwarder.mongodb_forwarder.MongoDbForwarder.forward

.. autofunction:: src.metadata.forwarder.mongodb_forwarder.MongoDbForwarder.close

.. autofunction:: src.metadata.forwarder.mongodb_forwarder.MongoDbForwarder._preprocess_metadata

.. autofunction:: src.metadata.forwarder.mongodb_forwarder.MongoDbForwarder._get_mongodb_credentials

.. autofunction:: src.metadata.forwarder.mongodb_forwarder.MongoDbForwarder._get_mongodb_collection

.. autofunction:: src.metadata.forwarder.mongodb_forwarder.MongoDbForwarder.count_documents

.. autofunction:: src.metadata.forwarder.mongodb_forwarder.MongoDbForwarder.get_metadata_by_id

OAI-PMH
-----------------

OAIClient
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.metadata.oaipmh.oaiclient.OAIClient.__init__

.. autofunction:: src.metadata.oaipmh.oaiclient.OAIClient.get_records

Parser
-----------------

DimParser
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.metadata.parser.dim_parser.DimParser.parse

IParser
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.metadata.parser.parser_interface.IParser.parse

Utils
-----------

Get Resource Id
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.metadata.utils.get_resource_id.get_resource_id

Main
-----------

Main
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.metadata.main.process_metadata_batch

.. autofunction:: src.metadata.main.get_metadata

.. autofunction:: src.metadata.main.process_metadata

.. autofunction:: src.metadata.main.main
