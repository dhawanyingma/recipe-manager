from datetime import datetime, timezone
from app.db import db

class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(300), nullable= False)
    ingredients = db.Column(db.Text, nullable = True)
    instructions = db.Column(db.Text, nullable = True)
    tags = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default = datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default = datetime.utcnow, onupdate = datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Recipe {self.name}>"
    
