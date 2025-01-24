import pytest
from metadata.filter.record_deleted import RecordDeleted

def test_record_deleted_with_empty_record():

    record = {
        'header': {}
    }
    assert RecordDeleted.filter(record) == False
