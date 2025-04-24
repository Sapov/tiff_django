#
#
# class Invoice:
#     '''Содержание ордера'''
#     Positions: list[dict]
#     date:str
#     totalAmount: int
#     number: str
#
#
#
# {
#                         "Positions": self.__create_list_position(),
#                         "date": str(datetime.now().date()),
#                         "totalAmount": self.total_amount_order,
#                         "totalNds": "0",
#                         "number": str(self.order_id),
#                         # "basedOn": "Основание платежа",
#                         # "comment": "Комментарий к платежу",
#                     }
#
# "Positions": [
#                             {
#                                 "positionName": "Название товара или услуги",
#                                 "unitCode": "шт.",
#                                 "ndsKind": "nds_0",
#                                 "price": "12345.00",
#                                 "quantity": "12345",
#                                 "totalAmount": "12345",
#                                 "totalNds": "1"
#                             }