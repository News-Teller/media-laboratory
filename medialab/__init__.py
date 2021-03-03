from .database import Database
from .utils import generate_uid

# Direclty instantiate the database so it can be imported and used right away
# Database URI can be set using environment variables
db = Database()
