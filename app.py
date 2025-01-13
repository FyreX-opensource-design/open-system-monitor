from flask import Flask, render_template
import psutil
import time, random, threading
from turbo_flask import Turbo
from util import CPUutil

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
turbo = Turbo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.before_request
def before_request():
    thread = threading.Thread(target=update_load, daemon=True)
    thread.start()

def update_load():
    with app.app_context():
        while True:
            try:
                time.sleep(1)
                turbo.push(turbo.replace(render_template('loadavg.html'), 'load'))
            except Exception as e:
                print(f"Error in update_load: {e}")
                break

@app.context_processor
def inject_load():
    load = [str(psutil.cpu_percent(interval=1)) + " %", str(CPUutil.CPUThreadLoad()) + " %", str(round(psutil.virtual_memory().used / 1024 / 1024 / 1024, 1)) + " GB", str(round(psutil.virtual_memory().free / 1024 / 1024 / 1024, 1)) + " GB", str(psutil.cpu_percent(interval=None, percpu=True)[1]) + " " + str(psutil.cpu_percent(interval=None, percpu=True)[2])]
    return {'loadCPU': load[0], 'loadRAM_used': load[1], 'loadRAM_free': load[2]}
if __name__ == '__main__':
    app.run()