# -*- coding: utf-8 -*-

from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas

from libs.api_tools.ouch_schema_generator import OuchSchemaGenerator


@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    generator = OuchSchemaGenerator()
    return response.Response(generator.get_schema(request=request))
