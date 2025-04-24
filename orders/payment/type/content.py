from datetime import datetime

from orders.models import OrderItem


class Content:
    def __init__(self, order_id: int):
        self.order_id = order_id
        self.total_amount_order = None


    def __create_list_position(self) -> list[dict]:
        ''' формируем dict по каждой позиции и кладем в list'''
        order_items = OrderItem.objects.filter(order=self.order_id)
        positions = []
        for i, v in enumerate(order_items):
            new_dict = {
                "positionName": f'{v.product.material} {v.product.length}x{v.product.width} м',
                "unitCode": "шт.",
                "ndsKind": "without_nds",
                "price": float(v.product.price / v.product.quantity),
                "quantity": v.product.quantity,
                "totalAmount": v.price_per_item,
                "totalNds": 0
            }
            self.total_amount_order += v.price_per_item
            positions.append(new_dict)
        return positions


    def items_content(self, name_document:str) -> dict[str:str]:
        '''
        name_document or 'Invoice' or 'Act'
        '''
        return {
            name_document: {
                "number": str(self.order_id),
                "Positions": self.__create_list_position(),
                "date": str(datetime.now().date()),
                "totalAmount": self.total_amount_order,
                "totalNds": "0",
                # "basedOn": "Основание платежа",
                # "comment": "Комментарий к платежу",
            }

        }

    '''
    Контент для инвойса
        "Content": {
                    "Invoice": {
                        "number": str(self.order_id),
                        "Positions": self.create_list_position(),
                        "date": str(datetime.now().date()),
                        "totalAmount": self.total_amount_order,
                        "totalNds": "0",
                        # "basedOn": "Основание платежа",
                        # "comment": "Комментарий к платежу",
                    }
                }
    '''
    '''
    Контент для акта
       "Content": {
                    "Act": {
                        "number": self.order_id,
                        "Positions": self.create_list_position()
                        "date": str(datetime.now().date()),
                        "totalAmount": super().total_amount_order,
                        "totalNds": "0",
                        # "comment": "Комментарий",
                        # "basedOn": "Основание платежа", !!! оферта сайта
                    }
                },
    '''
