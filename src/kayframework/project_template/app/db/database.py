from sqlalchemy import create_engine
from .base import Base
from app.core.config import settings
import app.auth.models  # modelleri import et ki tablolar tanınsın

# SQLite database
engine = create_engine(settings.DATABASE_URL, echo=True)

# Tabloları oluşturma fonksiyonu
def create_tables():
    Base.metadata.create_all(engine)

