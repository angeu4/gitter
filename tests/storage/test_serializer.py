from gitter.storage.serializer import serialize_dict, deserialize_dict


def test_serializer_roundtrip():
    data = {"b": 2, "a": 1}

    serialized = serialize_dict(data)
    deserialized = deserialize_dict(serialized)

    assert deserialized == data


def test_serializer_deterministic_order():
    data1 = {"a": 1, "b": 2}
    data2 = {"b": 2, "a": 1}

    assert serialize_dict(data1) == serialize_dict(data2)
