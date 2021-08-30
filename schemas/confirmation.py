from marsh import marshmallow
from models.confirmation import ConfirmationModel

class ConfirmationSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = ConfirmationModel
        load_only = ("user",)
        dump_only = ("id", "expire_at", "confirmed")
        include_fk = True