class SecondSide:
    '''
    Реквизиты плательщика
    '''

    def __init__(self, payer):  # плательщик
        self.accountId: str = f'{payer.organisation_payer.bank_account}/{payer.organisation_payer.bik_bank}'
        self.legalAddress: str = payer.organisation_payer.address  # адрес "197183, г. Санкт-Петербург, ул. Сестрорецкая, д. 8",
        self.kpp: str = payer.organisation_payer.kpp  # КПП"668101001",
        self.bankName: str = payer.organisation_payer.bank_name  # Наименование банка"ООО \"БАНК ТОЧКА\"",
        self.bankCorrAccount: str = payer.organisation_payer.bankCorrAccount  # Кор.счет банка"30101810745374525104",
        self.taxCode: str = payer.organisation_payer.inn  # ИНН "660000000000",
        self.type: str = 'ip' if len(
            payer.organisation_payer.inn) == 12 else 'company'  # Тип компании или ИП или компания"company",
        self.secondSideName: str = payer.organisation_payer.name_full  # Наименование компании "ООО \"ГОС-АЛЬЯНС\""
