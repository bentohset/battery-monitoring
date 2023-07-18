from app.extensions import db

class Battery(db.Model):
    __tablename__ = "batteries"

    id = db.Column(db.Integer, primary_key=True)
    shelf_id = db.Column(db.Integer)
    container_id = db.Column(db.Integer)

    def __init__(self, shelf_id:int, container_id:int):
        self.shelf_id = shelf_id
        self.container_id = container_id