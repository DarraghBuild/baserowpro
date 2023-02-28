from baserow.contrib.builder.elements.models import HeadingElement, ParagraphElement
from baserow.contrib.builder.elements.registries import ElementType


class HeadingElementType(ElementType):
    type = "heading"
    model_class = HeadingElement

    def get_config_serializer_class(self):
        from baserow.contrib.builder.api.elements.element_type_serializers import (
            HeadingElementConfigSerializer,
        )

        return HeadingElementConfigSerializer

    def get_sample_params(self):
        return {"config": {"value": "Corporis perspiciatis"}}


class ParagraphElementType(ElementType):
    type = "paragraph"
    model_class = ParagraphElement

    def get_config_serializer_class(self):
        from baserow.contrib.builder.api.elements.element_type_serializers import (
            ParagraphElementConfigSerializer,
        )

        return ParagraphElementConfigSerializer

    def get_sample_params(self):
        return {
            "config": {
                "content": "Suscipit maxime eos ea vel commodi dolore. "
                "Eum dicta sit rerum animi. Sint sapiente eum cupiditate nobis vel. "
                "Maxime qui nam consequatur. "
                "Asperiores corporis perspiciatis nam harum veritatis. "
                "Impedit qui maxime aut illo quod ea molestias."
            }
        }
