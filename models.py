"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMG_URL = "https://tinyurl.com/demo-cupcake"

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class Cupcake(db.Model):
    """Cupcake"""

    __tablename__ = "cupcake"

    id = db.Column(
        db.Integer(),
        primary_key=True,
        autoincrement=True,
    )

    flavor = db.Column(
        db.String(50),
        nullable=False,
    )

    size = db.Column(
        db.String(50),
        nullable=False,
    )

    rating = db.Column(
        db.Integer(),
        nullable=False,
    )

    image = db.Column(
        db.VARCHAR(),
        nullable=False,
        default=DEFAULT_IMG_URL,
    )

    def serialize(self):
        """Serialize a cupcake SQLAlchemy obj to dictionary."""

        return {
            "id": self.id,
            "flavor": self.flavor,
            "size": self.size,
            "rating": self.rating,
            "image": self.image,
        }

    def __repr__(self):
        return f"<cupcake {self.id} flavor={self.flavor} size={self.size} rating={self.rating} image={self.image}>"