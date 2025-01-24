Logs
============

Counter
-----------------

DoubleClick
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.logs.counter.double_click.DoubleClick.filter

.. autofunction:: src.logs.counter.double_click.DoubleClick._clean_old_entries

RobotsCrawlers
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.logs.counter.robots_crawlers.RobotsCrawlers._download_robots_list

.. autofunction:: src.logs.counter.robots_crawlers.RobotsCrawlers.filter

StatusCode
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.logs.counter.status_code.StatusCode.filter

Filter
-----------------

AccessBitstream
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.logs.filter.access_bitstream.AccessBitstream.filter

AccessResourceBitstream
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.logs.filter.access_resource_bitstream.AccessResourceBitstream.filter

AccessResource
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.logs.filter.access_resource.AccessResource.filter

IFilter
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.logs.filter.filter_interface.IFilter.filter

SearchResource
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.logs.filter.search_resource.SearchResource.filter

WebResource
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.logs.filter.web_resource.WebResource.filter

WithIPv6Address
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.logs.filter.with_ipv6address.WithIPv6Address.filter

WithoutIpAddress
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.logs.filter.without_ipaddress.WithoutIpAddress.filter

Forwarder
-----------------

IForwarder
~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: src.logs.forwarder.forwarder_interface.IForwarder.forward

LokiForwarder
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.logs.forwarder.loki_forwarder.LokiForwarder.forward

.. autofunction:: src.logs.forwarder.loki_forwarder.LokiForwarder.forward_batch

.. autofunction:: src.logs.forwarder.loki_forwarder.LokiForwarder.close

.. autofunction:: src.logs.forwarder.loki_forwarder.LokiForwarder._set_log_tags

.. autofunction:: src.logs.forwarder.loki_forwarder.LokiForwarder._ensure_loki_url

.. autofunction:: src.logs.forwarder.loki_forwarder.LokiForwarder._set_timestamp

Transformer
-----------

AddBitstreamResourceIdLabel
~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.logs.transformer.add_bitstream_resource_id_label.AddBitstreamResourceIdLabel.transform

AddDefaultIpAddress
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.logs.transformer.add_default_ipaddress.AddDefaultIpAddress.transform

AddLabel
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.logs.transformer.add_label.AddLabel.transform

AddLogMetadata
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.logs.transformer.add_log_metadata.AddLogMetadata.get_metadata

.. autofunction:: src.logs.transformer.add_log_metadata.AddLogMetadata.transform

AddResourceIdLabel
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.logs.transformer.add_resource_id_label.AddResourceIdLabel.transform

AddTimestamp
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.logs.transformer.add_timestamp.AddTimestamp.transform

RemoveIPv6Address
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.logs.transformer.remove_ipv6address.RemoveIPv6Address.transform

ToJSON
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.logs.transformer.to_json.ToJSON.transform

ITransformer
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.logs.transformer.transformer_interface.ITransformer

Utils
-----------

Date Converter
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.logs.utils.date_converter.to_iso_format

.. autofunction:: src.logs.utils.date_converter.to_timestamp

.. autofunction:: src.logs.utils.date_converter.to_nanoseconds

Main
-----------

Main
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: src.logs.main.process_log

.. autofunction:: src.logs.main.process_logs_for_day

.. autofunction:: src.logs.main.update_yearly_stats

.. autofunction:: src.logs.main.process_month

.. autofunction:: src.logs.main.main
