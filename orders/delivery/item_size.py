from pydantic import NonNegativeFloat, BaseModel


class ItemSizes(BaseModel):
    """
    Размеры посылки в метрах.
    Пример: 0.45

    Source: https://yandex.ru/support2/delivery-profile/ru/api/express/openapi/IntegrationV2OfferCalculate#item

    """
    height: NonNegativeFloat
    length: NonNegativeFloat
    width: NonNegativeFloat


a = ItemSizes(height=1, length=2.5, width=3)

print(a)
