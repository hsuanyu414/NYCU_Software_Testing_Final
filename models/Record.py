class Record:
    def __init__(self, user_id=None, record_id=None, date=None, item=None, cost=None, category=None, comment=None, create_date=None):
        self.user_id = user_id
        self.record_id = record_id
        self.date = date
        self.item = item
        self.cost = cost
        self.category = category
        self.comment = comment
        self.create_date = create_date

    def __str__(self):
        return f"[record_id: {self.record_id}\n date: {self.date}\n item: {self.item}\n cost: {self.cost}\n category: {self.category}\n comment: {self.comment}\n create_date: {self.create_date}]\n\n"