"""
Provides formatting tools for the list of json objects.
"""
from abc import ABC, abstractmethod
import json


class AbstractFormatter(ABC):
    """
    An abstract data formatter.
    """

    def __init__(self, key_name: str) -> None:
        super().__init__()
        self._key_name = key_name

    @abstractmethod
    def format(self, json_list: list) -> dict[str, list]:
        """
        Formats incoming data.
        """
        return NotImplemented


class JsonFormatter(AbstractFormatter):
    """
    JSON data formatter.
    """

    def format(self, json_list: list) -> dict[str, list]:
        """
        Just returns json data by the provided key name.
        """

        return {
            f"{self._key_name}": json_list
        }


class SQLFormatter(AbstractFormatter):
    """
    SQL data formatter.
    """

    def format(self, json_list: list) -> dict[str, list]:
        """
        For every element in the list returns INSERT SQL QUERY.
        The name of the table is equal to provided key name and the values matched the
        parameters from the JSON object.
        """
        return list(map(self.__make_sql_statement, json_list))

    def __make_sql_statement(self, element: object) -> str:
        keys = ",".join(element.keys())
        values = ",".join(
            map(self.__parse_value, element.values()))
        return f"INSERT INTO {self._key_name} ({keys}) VALUES({values});"

    def __parse_value(self, value) -> str:
        if isinstance(value, int | float):
            return str(value)

        if isinstance(value, str):
            return f"'{value}'"

        return f"'{json.dumps(value)}'"
