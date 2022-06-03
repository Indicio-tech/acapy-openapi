from abc import ABC, abstractmethod
import re
from typing import Any
import yaml


class Visitor(ABC):
    @abstractmethod
    def visit(self, value: Any) -> Any:
        """Visit the value."""


class NullDescriptors(Visitor):
    def visit(self, value):
        if isinstance(value, dict):
            if "description" in value and value["description"] is None:
                value["description"] = ""
            return value
        return value

class MissingExternalDocUrls(Visitor):
    def visit(self, value):
        if isinstance(value, dict):
            if "externalDocs" in value and "url" not in value["externalDocs"]:
                value["externalDocs"]["url"] = "http://example.com/replace/me"
            return value
        return value


class FixRefs(Visitor):

    FIX_REF_RE = re.compile(r"#/definitions")

    def visit(self, value):
        if isinstance(value, dict):
            if "$ref" in value:
                value["$ref"] = self.FIX_REF_RE.sub("#/components/schemas", value["$ref"])
            return value
        return value


class FixContentTypes(Visitor):
    def visit(self, value):
        if isinstance(value, dict):
            if "*/*" in value:
                value["application/json"] = value["*/*"]
                del value["*/*"]
            return value
        return value


class OpenAPICleaner:

    def __init__(self, *visitors: Visitor):
        self.visitors = visitors

    def clean(self, value: Any):
        for visitor in self.visitors:
            value = visitor.visit(value)
        
        # Recurse
        if isinstance(value, dict):
            for child in value.values():
                self.clean(child)

        if isinstance(value, list):
            for item in value:
                self.clean(item)

        return value


if __name__ == "__main__":
    with open(
        "/app/openapi.yml"
    ) as openapi_file:
        openapi = yaml.load(openapi_file, Loader=yaml.FullLoader)

    cleaner = OpenAPICleaner(
        NullDescriptors(),
        MissingExternalDocUrls(),
        FixRefs(),
        FixContentTypes()
    )
    openapi = cleaner.clean(openapi)

    with open("/app/openapi.yml", "w") as openapi_file:
        yaml.dump(openapi, openapi_file, sort_keys=False)
