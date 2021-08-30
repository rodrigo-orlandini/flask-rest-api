from marsh import marshmallow
from models.store import StoreModel
from models.item import ItemModel
from schemas.item import ItemSchema

class StoreSchema(marshmallow.SQLAlchemyAutoSchema):
    items = marshmallow.Nested(ItemSchema, many=True)

    class Meta:
        model = StoreModel
        dump_only: ("id",)
        load_instance = True
        include_fk = True