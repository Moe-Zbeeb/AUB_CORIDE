from website.models import Carpool
from website.__intit__ import db
app.app_context()
carpools = Carpool.query.all()
print(carpools)