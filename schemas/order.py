from marsh import marshmallow
from models.order import OrderModel

class OrderSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderModel
        load_only = ("token",)
        dump_only = ("id", "status",)
        include_fk = True