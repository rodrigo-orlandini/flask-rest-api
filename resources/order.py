from collections import Counter
from flask import request
from flask_restful import Resource
from stripe import error

from libs.strings import gettext
from schemas.order import OrderSchema
from models.item import ItemModel
from models.order import OrderModel, ItemsInOrder

order_schema = OrderSchema()
#multiple_order_schema = OrderSchema(many=True)

class Order(Resource):
    @classmethod
    def get(cls):
        return order_schema.dump(OrderModel.find_all(), many=True), 200

    @classmethod
    def post(cls):
        data = request.get_json()
        items = []
        item_id_quantities = Counter(data["item_ids"])

        for _id, count in item_id_quantities.most_common():
            item = ItemModel.find_by_id(_id)
            if not item:
                return {"message", gettext("order_item_id_not_found").format(_id)}, 404

            items.append(ItemsInOrder(item_id=_id, quantity=count))

        order = OrderModel(items=items, status="pending")
        order.save_to_db()

        try:
            order.set_status("failed")
            order.charge_with_stripe(data["token"])
            order.set_status("complete")
            return order_schema.dump(order), 200

        except error.CardError as e:
            return e.json_body, e.http_status

        except error.RateLimitError as e:
            return e.json_body, e.http_status

        except error.InvalidRequestError as e:
            return e.json_body, e.http_status

        except error.AuthenticationError as e:
            return e.json_body, e.http_status

        except error.APIConnectionError as e:
            return e.json_body, e.http_status

        except error.StripeError as e:
            return e.json_body, e.http_status

        except Exception as e:
            print(e)
            return {"message": gettext("order_error")}, 500
