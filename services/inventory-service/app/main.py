from app import create_app
from app.consumers.manager import start_consumers_in_thread
import os

app = create_app()

# Start consumers in a separate thread/process if not in migrated/cli mode
# In a real heavy production env, consumers might be separate worker processes
if os.environ.get("WERKZEUG_RUN_MAIN") != "true": # Prevent double start in dev reload
    start_consumers_in_thread(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
