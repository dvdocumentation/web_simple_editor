
from threading import Event, Thread
import threading


import PySimpleGUI as sg
import json
import base64
from easysettings import EasySettings

import socketio

sio = socketio.Client()

main_uid = ''
main_url = ''

handlers_dict = {}
window = None

class CodeUpdateThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        while not self.stopped.wait(1):
            
            for key,value in handlers_dict.items():
                 if value!="" and value!=None:
                     filename = value[0]
                     with open(filename, 'r',encoding='utf-8') as file:
                        data = file.read()
                        base64file  = base64.b64encode(data.encode('utf-8')).decode('utf-8') 

                        if base64file!=value[1]:
                            handlers_dict[key] = (value[0], base64file, value[1])
                            #value[1] = base64file
                            output_handlers_dict = {}

                            output_handlers_dict[key] = base64file

                            sio.emit('agent_message', {'mode': 'update_data', 'uid': main_uid, "data":json.dumps(output_handlers_dict)}) 
                            
                            #for lkey,lvalue in handlers_dict.items():
                            #    if lvalue!="" and lvalue!=None:
                            #        output_handlers_dict[lkey] = lvalue[1]

                            #if len(output_handlers_dict)>0:
                            #    sio.emit('agent_message', {'mode': 'update_data', 'uid': main_uid, "data":json.dumps(output_handlers_dict)}) 



@sio.event
def connect():
    print('connection established')
    #sio.emit('agent_message', {'mode': 'request_handlers', 'uid': test_uid})

@sio.event
def server_message(data):
    global handlers_dict

    
    handlers = json.loads(data)
    for key in handlers.keys():
        if not key in handlers_dict:
            handlers_dict[key] = ""

    for key in list(handlers_dict.keys()):  
        if not key in handlers:
            handlers_dict.pop(key,None)

    load_pyfiles()


    

@sio.event
def disconnect():
    print('disconnected from server')

def sio_main():
    sio.connect(main_url)
    sio.wait()

#settings object
settings_global = EasySettings("uiconfigfile.conf") 

main_uid = settings_global.get("uid")
main_url = settings_global.get("url")

current_uid = None

def load_pyfiles():
    global data_pyfiles
    global data_pyfilenames
    global current_uid
    
    data_pyfiles=[['','','']]
    pyfiles_settings = []
    data_pyfiles_table=[['','']]

    configuration_json = {'ClientConfiguration':{}}

    
    for key,value in handlers_dict.items():
        if value=="":
            data_pyfiles.append([key,"...",""])
            pyfiles_settings.append({"alias":key,"filename":""})
            data_pyfiles_table.append([key,"..."])
        else:    
            data_pyfiles.append([key,value[0],value[1]])
            pyfiles_settings.append({"alias":key,"filename":value[0]})
            data_pyfiles_table.append([key,value[0]])

    #settings_global.set("handlers_list"+current_uid, json.dumps(pyfiles_settings))
    settings_global.save()

    v = data_pyfiles_table[1:][:]
    try:
        window['pyfiles_table'].update(values=v)   
    except:
        pass    

def update_data():
    output_handlers_dict = {}
    for lkey,lvalue in handlers_dict.items():
        if lvalue!="" and lvalue!=None:
            output_handlers_dict[lkey] = lvalue[1]

    if len(output_handlers_dict)>0:
        sio.emit('agent_message', {'mode': 'update_data', 'uid': main_uid, "data":json.dumps(output_handlers_dict)})  


def load_settings(current_uid):
    data_pyfilenames=[]
    if not current_uid==None:


        handlers_filename =  settings_global.get("handlers_filename"+current_uid)
        if not handlers_filename == None:
            window['conf_file_python'].update(handlers_filename)

        shandlers_list = settings_global.get("handlers_list"+current_uid)
        if not shandlers_list==None:
            try:
                if len(shandlers_list)>0:
                    jhandlers_list = json.loads(shandlers_list)
                    
                    for elem in jhandlers_list:
                            data_pyfilenames.append({"key":elem['alias'],"filename":elem['filename']})

                    load_pyfiles()

            except Exception:
                    print("Error reading settings...")

tab_layout_pyfiles=[[sg.Text("URL",size=35),sg.Input(do_not_clear=True, key='url',enable_events=True,expand_x=True,default_text=main_url)],
                    [sg.Text("После ввода URL перезапустите приложение",size=35)],
                    [sg.Text("host uid",size=35),sg.Input(do_not_clear=True, key='host_uid',enable_events=True,expand_x=True,default_text=main_uid)],
   
        [sg.Button('Connect',key='add_pyfiles')],[sg.Table(values=[['','']],headings=['Имя','Путь'],key='pyfiles_table',enable_events=True,expand_x=True,auto_size_columns=True,select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                    bind_return_key=True)]]


if __name__ == "__main__":

    #_thread = threading.Thread(target=sio_main, args=(operation,json_str,self.current_tab_id,handler.get('postExecute','')))
    if main_url!="":
        _thread = threading.Thread(target=sio_main)
        _thread.start() 

    #sg.theme('DarkAmber')    # Keep things interesting for your users


    window = sg.Window('Simple Constructor Agent', tab_layout_pyfiles,                  
                    resizable=True)
    window.finalize()

    stopFlag = Event()
    thread = CodeUpdateThread(stopFlag)
    thread.start()

        # ------ Event Loop ------
    while True:
        event, values = window.read()
        #print(event, values)
        if event == sg.WIN_CLOSED:
            break
        if event == 'pyfiles_table':
            #print(event)
            if len(values['pyfiles_table'])>0:
                row_clicked =  values['pyfiles_table'][0]+1
                key = data_pyfiles[row_clicked][0]

                rlayout = [
        
                [sg.Text('Ключ', size =(15, 1)), sg.Text(key, size =(15, 1))],
                [sg.Text('Файл', size =(15, 1)), sg.Input(key='pyfiles_file'), sg.FileBrowse(file_types=[("Python files (*.py)", "*.py")])],
            
                [sg.Ok(), sg.Cancel()]
                ]
        
                rwindow = sg.Window("Добавление файла", rlayout)
                revent, rvalues = rwindow.read()
                rwindow.close()  

                if revent=='Ok':
                     data=''
                     with open(rvalues['pyfiles_file'], 'r',encoding='utf-8') as file:
                        data = file.read()
                        base64file  = base64.b64encode(data.encode('utf-8')).decode('utf-8')   

                        handlers_dict[key] = (rvalues['pyfiles_file'],base64file)

                     #data_pyfilenames.append({"key":rvalues['pyfiles_key'],"filename":rvalues['pyfiles_file']})
                     #configuration_json['ClientConfiguration']['PyFiles'].append({"PyFileKey":rvalues['pyfiles_key'],"PyFileData":base64file})
                     load_pyfiles() 
                     update_data()

        if event == 'add_pyfiles':
             sio.emit('agent_message', {'mode': 'request_handlers', 'uid': main_uid})
        if event == 'url':
            main_url = values['url']
            settings_global.set("url", main_url)
            settings_global.save()
        if event == 'host_uid':
            main_uid = values['host_uid']
            settings_global.set("uid", main_uid)
            settings_global.save()    

   

            

    sio.disconnect()
    window.close()            
    