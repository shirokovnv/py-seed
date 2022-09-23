"""
Provides formatting tools for the list of json objects.
"""

import json
from abc import ABC, abstractmethod


class AbstractFormatter(ABC):
    """
    An abstract data formatter.
    """

    def __init__(self, schema_title: str) -> None:
        """
        Construct the formatter.

        Args:
            schema_title: Just the name of the schema.
        """
        super().__init__()
        self._schema_title = schema_title

    @abstractmethod
    def format(self, json_data: list[dict[str, object]]) -> list[str] | dict[str, object]:
        """
        Format incoming data.

        Args:
            json_data: The data you need to format.
        """
        return NotImplemented


class JsonFormatter(AbstractFormatter):
    """
    JSON data formatter.
    """

    def format(self, json_data: list[dict[str, object]]) -> dict[str, object]:
        """
        Format json data.

        Args:
            json_data: The data you need to format.

        Returns:
            key-value pair, where key is `schema title` and value is `json_data`
        """
        return {'{0}'.format(self._schema_title): json_data}


class SQLFormatter(AbstractFormatter):
    """
    SQL data formatter.
    """

    def format(self, json_data: list[dict[str, object]]) -> list[str]:
        """
        For every element in the list returns INSERT SQL QUERY.

        Args:
            json_data: The data you need to format.

        Returns:
            A list of insert SQL statements.
        """
        return list(map(self._make_sql_statement, json_data))

    def _make_sql_statement(self, json_element: dict[str, object]) -> str:
        json_keys = ','.join(json_element.keys())
        json_values = ','.join(
            map(self._parse_json_value, json_element.values())
        )
        return 'INSERT INTO {0} ({1}) VALUES({2});'.format(
            self._schema_title, json_keys, json_values
        )

    def _parse_json_value(self, json_value: object) -> str:
        if isinstance(json_value, int | float):
            return str(json_value)

        if isinstance(json_value, str):
            return "'{0}'".format(json_value)

        return "'{0}'".format(json.dumps(json_value))
