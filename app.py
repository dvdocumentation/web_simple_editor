from flask import Flask, render_template_string, request, render_template_string, session, copy_current_request_context,   redirect,send_from_directory
from flask_session import Session
import json
from flask_socketio import SocketIO,  disconnect
import pathlib
import os

from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'

from uiweb import Simple
#from simpleweb import Simple

async_mode = 'threading'
fapp = Flask(__name__,template_folder='templates',static_url_path='',  static_folder='static')

SESSION_TYPE= 'filesystem'

fapp.config['SECRET_KEY'] = 'secret!'
fapp.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
fapp.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
fapp.config['SESSION_TYPE'] = 'filesystem'

Session(fapp)

socket_ = SocketIO(fapp,async_mode=async_mode, async_handlers=True)

sid = None

PATH_TO_SETTINGS = 'web_settings.json'
PYTHONPATH=str(pathlib.Path(__file__).parent.absolute())

connected=[]
connected_agent=[]

def get_current_connection(sid):
    l = list(filter(lambda x: x[1] == sid, connected))

    for user in l:
        return user

SW = None
# WebSocket events

@socket_.on('connect')
def connect_test_message(message):
    global connected_agent
    
    sid = request.sid
    connected_agent.append((socket_, sid))

     


@socket_.on('agent_message')
def agent_test_message(message):
    global connected_agent

    mode = message.get("mode")
    uid = message.get("uid")

    if mode=='request_handlers':
        handlers_list = {}
        handlers_list["main_pyhandlers_file"] = ""

        os.makedirs(PYTHONPATH+os.sep+fapp.config['UPLOAD_FOLDER'],exist_ok=True)
        filename = uid+".ui"
        full_path = PYTHONPATH+os.sep+os.path.join(fapp.config['UPLOAD_FOLDER'])+os.sep+filename

        configuration={}
        if os.path.isfile(full_path): 
            with open(full_path, "r",encoding="utf-8") as file:
                configuration = json.load(file) 


            if configuration['ClientConfiguration'].get("host_uid") == uid:
                if "PyFiles" in configuration['ClientConfiguration']:
                    for h in configuration['ClientConfiguration']['PyFiles']:
                        handlers_list[h.get("PyFileKey")] = ""    

        
                socket_.emit('server_message', json.dumps(handlers_list));    
    
    elif mode =='update_data':
        jdata = json.loads(message.get("data"))

        os.makedirs(PYTHONPATH+os.sep+fapp.config['UPLOAD_FOLDER'],exist_ok=True)
        filename = uid+".ui"
        full_path = PYTHONPATH+os.sep+os.path.join(fapp.config['UPLOAD_FOLDER'])+os.sep+filename

        configuration={}
        if os.path.isfile(full_path): 
            with open(full_path, "r",encoding="utf-8") as file:
                configuration = json.load(file) 

            #if "PyFiles" in  configuration['ClientConfiguration']:
            #   configuration['ClientConfiguration'].pop("PyFiles",None)   

            for key, value in jdata.items(): 
                if key == "main_pyhandlers_file":
                    if len(str(value))>0:
                        configuration['ClientConfiguration']["PyHandlers"] = value
                else:
                    if len(str(value))>0:
                        if not "PyFiles" in  configuration['ClientConfiguration']:
                            configuration['ClientConfiguration']["PyFiles"] = []
                        str_file = next((item for item in configuration['ClientConfiguration']["PyFiles"] if item["PyFileKey"] == key), None)
                        if str_file==None:
                            configuration['ClientConfiguration']["PyFiles"].append({"PyFileKey":key,"PyFileData":value})    
                        else:
                            configuration['ClientConfiguration']["PyFiles"][configuration['ClientConfiguration']["PyFiles"].index(str_file)] = {"PyFileKey":key,"PyFileData":value} 
                            

            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(configuration, f, ensure_ascii=False, indent=4)

@socket_.on('connect_event', namespace='/simpleweb')
def test_message(message):
    global SW
    global connected
    if not SW==None:
        sid = request.sid
        session['sid']=sid
        session['SW']=SW
        session['SW'].set_sid(sid)

        connected.append((socket_, sid, SW))

        
        user = get_current_connection(request.sid)
        if user!=None:
            user[2].on_launch({"sid":sid}) 

        

    session['receive_count'] = session.get('receive_count', 0) + 1
 
@socket_.on('run_process', namespace='/simpleweb')
def run_process(message):
    user = get_current_connection(request.sid)
    user[2].run_process(message)

@socket_.on('input_event', namespace='/simpleweb')
def input_event(message):
    user = get_current_connection(request.sid)
    if user!=None:
        user[2].input_event(message) 
@socket_.on('cookie_event', namespace='/simpleweb')
def cookie_event(message):
    user = get_current_connection(request.sid)
    if user!=None:
        user[2].hashMap["_cookies"] =message.get('value')     

@socket_.on('js_result', namespace='/simpleweb')
def js_result(message):
    user = get_current_connection(request.sid)
    user[2].js_result(message)     

@socket_.on('close_maintab', namespace='/simpleweb')
def close_maintab(message):
    user = get_current_connection(request.sid)
    user[2].close_maintab(message)   

@socket_.on('select_tab', namespace='/simpleweb')
def select_tab(message):
    user = get_current_connection(request.sid)
    user[2].select_tab(message) 

@socket_.on('disconnect_request', namespace='/simpleweb')
def disconnect_request():
    global connected
    disconnected = list(filter(lambda x: x[0] == socket_, connected))

    for user in disconnected:
            connected.remove(user)
            print(f'{user[1]} left')
    @copy_current_request_context
    def can_disconnect():
        disconnected = list(filter(lambda x: x[0] == socket_, connected))

        for user in disconnected:
            connected.remove(user)
            print(f'{user[1]} left')

        disconnect()

#Flask events
@fapp.route('/setvalues/', methods=['POST'])
def jscommand(FUNCTION=None):
    session['SW'].set_values(request.json)
    
    return ""


@fapp.route('/setvaluespulse/', methods=['POST'])
def jscommandpulse(FUNCTION=None):
    session['SW'].set_values_pulse(request.json)
     
    return ""    

@fapp.route('/admin', methods=['GET'])
def adminpage():
    if not SW==None:
        
        path = pathlib.Path(PATH_TO_SETTINGS)
        if path.is_file():
            f = open(PATH_TO_SETTINGS)
            settings = json.load(f)
        else:
            settings={"url":"","user":"","password":""}

        return render_template_string(SW.get_admin_html(),settings = settings)


@fapp.route('/debug/<lsid>', methods=['POST'])
def debug(lsid):
    for c in connected:
        if c[1]==lsid:
            jdata = request.json
            c[2].debug(jdata)
            while not "next_"+lsid in c[2].hashMap:
                pass
            c[2].hashMap.pop("next_"+lsid,None)

            jtable = json.loads(c[2].hashMap["StackTable"])
            ex_hashMap = []
            for r in jtable["rows"]:
                ex_hashMap.append({"key":r.get("variable"),"value":r.get("value")})    
            jdata['hashmap'] = ex_hashMap
            jdata['stop'] =False
            jdata['ErrorMessage']=""
            jdata['Rows']=[]
            return json.dumps(jdata,ensure_ascii=False),200

            

      
    return "",200

@fapp.route('/uploader', methods = ['PUT', 'POST'])
def upload_file():
   SW.write_settings(request,PATH_TO_SETTINGS)

   return "ok",200



@fapp.route('/upload_file', methods = ['PUT', 'POST'])
def upload_file_ui():
   file = request.files['file'] 
   if file.filename == '':
            #'No selected file'
            return redirect(request.url)
   if file:
            filename = request.args.get('sid')+"_"+secure_filename(file.filename)
            os.makedirs(PYTHONPATH+os.sep+fapp.config['UPLOAD_FOLDER'],exist_ok=True)
            file.save(PYTHONPATH+os.sep+os.path.join(fapp.config['UPLOAD_FOLDER'], filename))

            user = get_current_connection(request.args.get('sid'))
            user[2].input_event({"data":"upload_file","filename":filename,"source":request.args.get('id')}) 
   

   return "ok",200 

@fapp.route('/download_file', methods = ['GET', 'POST'])
def download_file():
    os.makedirs(PYTHONPATH+os.sep+fapp.config['UPLOAD_FOLDER'],exist_ok=True)
    filename = request.args.get('filename')
   
    return send_from_directory(PYTHONPATH+os.sep+os.path.join(fapp.config['UPLOAD_FOLDER']), filename, as_attachment=True,download_name='')

@fapp.route('/get_conf', methods = ['GET'])
def get_conf():
    os.makedirs(PYTHONPATH+os.sep+fapp.config['UPLOAD_FOLDER'],exist_ok=True)
    filename = request.args.get('filename')
    full_path = PYTHONPATH+os.sep+os.path.join(fapp.config['UPLOAD_FOLDER'])+os.sep+filename
    
    return send_from_directory(PYTHONPATH+os.sep+os.path.join(fapp.config['UPLOAD_FOLDER']), filename, as_attachment=True)

@fapp.route('/get_conf_text', methods = ['GET'])
def get_conf_text():
    os.makedirs(PYTHONPATH+os.sep+fapp.config['UPLOAD_FOLDER'],exist_ok=True)
    filename = request.args.get('filename')
    full_path = PYTHONPATH+os.sep+os.path.join(fapp.config['UPLOAD_FOLDER'])+os.sep+filename

    jconfiguration={}
    with open(full_path, "r",encoding="utf-8") as file:
        jconfiguration = json.load(file)    

    return json.dumps(jconfiguration,ensure_ascii=False,indent=4, separators=(',', ': ')),200


@fapp.route('/static/<path:path>')
def static_file(path):
    return fapp.send_static_file(path)  
 
@fapp.route('/', methods=['GET', 'POST','PUT']) #main page initialization
def index():
    global SW

    SW = Simple(socket_,PYTHONPATH)
    
    SW.load_settings(PATH_TO_SETTINGS)
    
    SW.load_configuration('current_configuration.ui')
   
    res =SW.build_page()
     
    return render_template_string(res)
    
if __name__ == "__main__":
    global_data = {}
 
    #socket_.run(fapp, debug=False, host='0.0.0.0', port=1555,ssl_context=('server.crt', 'server.key'))
    socket_.run(fapp, debug=False, host='0.0.0.0', port=1555)
