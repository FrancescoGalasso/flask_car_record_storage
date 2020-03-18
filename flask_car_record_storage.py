from app import app_flask_car_record_storage, db
from app.models import User

# Uselfull using cmd *flask shell* for debug testing
@app_flask_car_record_storage.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

# usefull for the cmd *python flask_file_server.py*
app_flask_car_record_storage.run(host="0.0.0.0", port=5000)