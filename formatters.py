"""
Provides formatting tools for the list of json objects.
"""

from abc import ABC, abstractmethod
from typing import Any


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
    def format(self, json_data: list[dict[str, object]]) -> str | list[str] | dict[str, object]:
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


class XMLFormatter(AbstractFormatter):
    """
    XML data formatter.
    """

    def format(self, json_data: list[dict[str, object]]) -> str:
        """
        Convert json object to XML string.

        Args:
            json_data: The data you need to format.

        Returns:
            XML SOAP response
        """
        capitalized_title = self._schema_title[0].upper() + self._schema_title[1:]

        return """<?xml version=\"1.0\" encoding=\"utf-8\"?>
            <soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\">
                <soap:Body>
                    <{0}>
                        {1}
                    </{0}>
                </soap:Body>
            </soap:Envelope>""".format(capitalized_title, self._json_to_xml(json_data))

    def _json_to_xml(self, json_object: Any) -> str:
        result_list = []

        json_object_type = type(json_object)

        if json_object_type is list:
            for sub_element in json_object:
                result_list.append(self._json_to_xml(sub_element))

            return ''.join(result_list)

        if json_object_type is dict:
            result_list.append('<Item>\r\t')
            for tag_name in json_object:
                sub_object = json_object[tag_name]
                result_list.append('<{0}>'.format(tag_name[0].upper() + tag_name[1:]))
                result_list.append(self._json_to_xml(sub_object))
                result_list.append('</{0}>'.format(tag_name[0].upper() + tag_name[1:]))

            result_list.append('</Item>')

            return ''.join(result_list)

        return '{0}'.format(json_object)
