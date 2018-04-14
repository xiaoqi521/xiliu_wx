# -*- coding: utf-8 -*-
import yaml
import coreapi
from urllib import parse

from django.contrib.admindocs.utils import trim_docstring

from rest_framework import schemas


class OuchSchemaGenerator(schemas.SchemaGenerator):

    def get_des(self, docstring):
        split_lines = trim_docstring(docstring).split('\n')

        cut_off = None
        for index in range(len(split_lines) - 1, -1, -1):
            line = split_lines[index]
            line = line.strip()
            if line == '---':
                cut_off = index
                break
        if cut_off is not None:
            split_lines = split_lines[0:cut_off]

        return "\n".join(split_lines)

    def strip_yaml_from_docstring(self, docstring):
        split_lines = trim_docstring(docstring).split('\n')

        cut_off = None
        for index in range(len(split_lines) - 1, -1, -1):
            line = split_lines[index]
            line = line.strip()
            if line == '---':
                cut_off = index
                break
        if cut_off is not None:
            split_lines = split_lines[cut_off:]

        return "\n".join(split_lines)

    def get_link(self, path, method, view):
        method_name = getattr(view, 'action', method.lower())

        fields = self.get_path_fields(path, method, view)
        yaml_doc = None

        func = getattr(view, method_name, None) if method_name else None
        if not func:
            func = view

        if func and func.__doc__:
            try:
                yaml_doc = yaml.load(self.strip_yaml_from_docstring(func.__doc__))
            except:
                yaml_doc = None

        if yaml_doc and isinstance(yaml_doc, dict):
            desc = self.get_des(func.__doc__)
            # ret = yaml_doc.get('ret', '')
            # err = yaml_doc.get('err', '')
            # _method_desc = desc + '<br>' + 'return: ' + ret + '<br>' + 'error: ' + err
            _method_desc = desc
            params = yaml_doc.get('parameters', [])
            for i in params:
                _name = i.get('name')
                _desc = i.get('description')
                _required = i.get('required', True)
                _type = i.get('type', 'string')
                _location = i.get('paramType', 'form')
                field = coreapi.Field(
                    name=_name,
                    location=_location,
                    required=_required,
                    description=_desc,
                    type=_type
                )
                fields.append(field)
        else:
            _method_desc = func.__doc__ if func and func.__doc__ else ''
            fields += self.get_serializer_fields(path, method, view)
        fields += self.get_pagination_fields(path, method, view)
        fields += self.get_filter_fields(path, method, view)

        if fields and any([field.location in ('form', 'body') for field in fields]):
            encoding = self.get_encoding(path, method, view)
        else:
            encoding = None

        if self.url and path.startswith('/'):
            path = path[1:]

        return coreapi.Link(
            url=parse.urljoin(self.url, path),
            action=method.lower(),
            encoding=encoding,
            fields=fields,
            description=_method_desc
        )
