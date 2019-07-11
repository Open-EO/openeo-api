"""

DIY validation of openapi.json examples against their corresponding schema (PR#194).
Currently implemented as pytest based test suite due to lack of this
validation feature in speccy itself (see https://github.com/wework/speccy/issues/287)

"""

import json
from pathlib import Path

import _pytest
import jsonschema
import openapi_schema_to_json_schema
import pytest

_PROJECT_ROOT = Path(__file__).parent.parent


def get_api_spec() -> dict:
    with (_PROJECT_ROOT / 'openapi.json').open() as f:
        return json.load(f)


class OpenApiValidator:
    """
    Helper class to validate OpenApi specifications

    Implemented using combination of `jsonschema` and `openapi_schema_to_json_schema`
    due to current lack of a dedicated OpenApi validation module
    """

    class OpenApiResolver(jsonschema.RefResolver):
        """Custom resolver for OpenApi $ref references"""

        def resolve(self, ref):
            url, schema = super().resolve(ref)
            return url, openapi_schema_to_json_schema.to_json_schema(schema)

    def __init__(self, api_spec: dict, schema: dict, resolver_cls=OpenApiResolver):
        resolver = resolver_cls.from_schema(
            schema=openapi_schema_to_json_schema.to_json_schema(api_spec)
        )
        # OpenApi 3 is closest to JSON Schema Draft 4
        self.validator = jsonschema.Draft4Validator(
            schema=openapi_schema_to_json_schema.to_json_schema(schema),
            resolver=resolver
        )

    def validate(self, instance):
        return self.validator.validate(instance)


def pytest_generate_tests(metafunc: _pytest.python.Metafunc):
    """
    Pytest hook for custom test parametrization
    """
    if 'schema_with_example' in metafunc.fixturenames:

        def extract_schemas_with_example(d: dict, path: tuple = ()):
            """Extract all nodes in the spec that have an 'example' item."""
            for key, value in d.items():
                if isinstance(value, dict):
                    if 'example' in value:
                        yield path + (key,), value
                    else:
                        yield from extract_schemas_with_example(value, path + (key,))

        api_spec = get_api_spec()
        schemas = list(extract_schemas_with_example(api_spec))
        metafunc.parametrize(
            ['api_spec', 'path', 'schema_with_example'],
            [(api_spec, path, schema) for path, schema in schemas],
            ids=[':'.join(path) for path, schema in schemas]
        )


def test_schema_example(api_spec, path, schema_with_example):
    """
    Check whether examples included in the API schemas correspond with the schema.
    """
    if path[-1] == "properties":
        pytest.skip("This is probably not a schema example but an 'example' property")
    assert "type" in schema_with_example
    assert "example" in schema_with_example
    example = schema_with_example['example']
    OpenApiValidator(api_spec=api_spec, schema=schema_with_example).validate(example)
