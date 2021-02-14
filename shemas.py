from urllib.parse import urlparse

from marshmallow import Schema, fields, ValidationError, validates


class NewLinkRequestSchema(Schema):
    url = fields.Url(required=True, relative=False, schemes=["http", "https"])

    @validates("url")
    def validate_cycle(self, url):
        if not self.context.get("app_host"):
            return
        parts = urlparse(url)
        if parts.hostname == self.context["app_host"]:
            raise ValidationError("Cannot store URL to own host.")
