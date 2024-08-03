import json
import uuid

import requests



from pathlib import Path    

import os
import base64
from io import BytesIO
import copy

import requests
import qrcode
import socket
from jinja2 import Template

from app import session



SESSION_TYPE= 'filesystem'

session["filename"] = None
session["filename_base"] = None

session["processes_table_id"] = -1
session["screens_table_id"] = -1
session["elements_table_id"] = -1

session["current_element"] =None
session["parent_element"] = None
#parent_elelments_element = None

session["current_parent"] = (None,None)
session["current_parent_dict"] = {}

session["edit_handler_mode"] = -1
postExecute = ""
session["layouts_edit"] = False




WSPORT = "1555"
WS_URL = "WRITE_YOUR_ADDRESS_HERE"

locale_filename = "ru_locale.json"

session["host_uid"]=""


events_common = ["","onLaunch","onIntentBarcode","onBluetoothBarcode","onBackgroundCommand","onRecognitionListenerResult","onWEBMainTabSelected","onIntent","onWebServiceSyncCommand","onSQLDataChange","onSQLError","onCloseApp","WSIncomeMessage","onSimpleBusMessage","onSimpleBusResponse","onSimpleBusMessageDownload","onSimpleBusConfirmation","onWebEvent","onLaunchMenu","onInputMenu","onStartMenu","onServiceStarted","onHandlerError","onProcessClose","onPelicanInitialized","onPelicanInitError","onPelicanInitAction","onDirectWIFIMessage"]

events_screen = ["","onStart","onPostStart","onInput","onResultPositive","onResultNegative"]

session["opened_element_uid"] = None

main_menu_elements = ["","qr_settings","offline_exchange","documents","tasklist","product_log","store","save_settings","keyboard_test","ping_bt","update_configurations","Custom menu item"]

action_types = ["","run","runasync","runprogress"]
handler_types = ["","python","pythonargs","pythonbytes","online","http","sql","nosql","set","js","pythonscript","pelican"]

session["configuration"] = {"ClientConfiguration":{}}

session["processes_table"] = []

configuration_properties_list = ["ConfigurationName","ConfigurationFileName","ConfigurationVersion","ConfigurationDescription","agent","ForegroundService","StopForegroundServiceOnExit","BroadcastIntent","BroadcastVariable","FaceRecognitionURL","OnKeyboardMain","LaunchProcess","LaunchVar","MenuWebTemplate","Launch","HTMLHead","HTMLdocument_ready","PyGeneral","PelicanInit"]
configuration_settings_list = ["dictionaries","vendor","vendor_url","vendor_password","handler_split_mode","handler_url","handler_password"]

mediafile_layout = {
    "Name": "Новый экран",
    "type": "Operation",
    "Elements": [
        {
            "Value": "",
            "Variable": "",
            "type": "LinearLayout",
            "weight": "0",
            "height": "match_parent",
            "width": "match_parent",
            "orientation": "vertical",
            "Elements": [
                {
                    "type": "EditTextText",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Ключ|@key",
                    "Variable": "key",
                    "gravity_horizontal": "left"
                },
                {
                    "type": "file",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "@file",
                    "Variable": "file"
                }
            ],
            "BackgroundColor": "",
            "StrokeWidth": "",
            "Padding": ""
        }
    ],
    "Timer": False,
    "hideToolBarScreen": False,
    "noScroll": False,
    "handleKeyUp": False,
    "hideBottomBarScreen": False,
    "onlineOnStart": False,
    "onlineOnAfterStart": False,
    "onlineOnInput": False
}


handler_layout_lang = {
                        "Value": "",
                        "Variable": "",
                        "type": "LinearLayout",
                        "weight": "0",
                        "height": "match_parent",
                        "width": "match_parent",
                        "orientation": "vertical",
                        "Elements": [
                            {
                                "type": "EditTextText",
                                "height": "wrap_content",
                                "width": "match_parent",
                                "weight": "0",
                                "Value": "alias|@alias",
                                "Variable": "alias",
                                "gravity_horizontal": "left"
                            }
                            ,
                            {
                                "type": "SpinnerLayout",
                                "height": "wrap_content",
                                "width": "match_parent",
                                "weight": "0",
                                "Value": "Событие|@common_events",
                                "Variable": "event",
                                "gravity_horizontal": "left"
                            },
                            {
                                "type": "EditTextText",
                                "height": "wrap_content",
                                "width": "match_parent",
                                "weight": "0",
                                "Value": "listener|@listener",
                                "Variable": "listener",
                                "gravity_horizontal": "left"
                            }
                            ,
                            {
                                "type": "SpinnerLayout",
                                "height": "wrap_content",
                                "width": "match_parent",
                                "weight": "0",
                                "Value": "Действие|@action_types",
                                "Variable": "action",
                                "gravity_horizontal": "left"
                            }
                            ,
                            {
                                "type": "SpinnerLayout",
                                "height": "wrap_content",
                                "width": "match_parent",
                                "weight": "0",
                                "Value": "Тип обработчика|@handler_types",
                                "Variable": "type",
                                "gravity_horizontal": "left"
                            }
                            ,
                            {
                                "type": "TextView",
                                "height": "wrap_content",
                                "width": "match_parent",
                                "weight": "0",
                                "Value": "Метод",
                                "gravity_horizontal": "left"
                            },
                            {
                                "type": "#type_method",
                                "height": "wrap_content",
                                "width": "match_parent",
                                "weight": "0",
                                "Value": "@method",
                                "Variable": "method",
                                "gravity_horizontal": "left"
                            }
                            ,
                            {
                        "Value": "",
                        "Variable": "",
                        "type": "LinearLayout",
                        "weight": "0",
                        "height": "match_parent",
                        "width": "match_parent",
                        "orientation": "vertical",
                        "Elements": [
                            {
                                "type": "TextView",
                                "height": "wrap_content",
                                "width": "match_parent",
                                "weight": "0",
                                "Value": "Обработчик postExecute",
                                "Variable": "",
                                "gravity_horizontal": "center"
                            },

                            
                            
                            {
                                "type": "SpinnerLayout",
                                "height": "wrap_content",
                                "width": "match_parent",
                                "weight": "0",
                                "Value": "Действие|@action_types",
                                "Variable": "action_postExecute",
                                "gravity_horizontal": "left"
                            }
                            ,
                            {
                                "type": "SpinnerLayout",
                                "height": "wrap_content",
                                "width": "match_parent",
                                "weight": "0",
                                "Value": "Тип обработчика|@handler_types",
                                "Variable": "type_postExecute",
                                "gravity_horizontal": "left"
                            }
                            ,
                            {
                                "type": "TextView",
                                "height": "wrap_content",
                                "width": "match_parent",
                                "weight": "0",
                                "Value": "Метод",
                                "gravity_horizontal": "left"
                            },
                            {
                                "type": "#_PE",
                                "height": "wrap_content",
                                "width": "match_parent",
                                "weight": "0",
                                "Value": "@method_postExecute",
                                "Variable": "method_postExecute",
                                "gravity_horizontal": "left"
                            }

                        ]
                        ,
                        "BackgroundColor": "#f5bd8c",
                        "StrokeWidth": "2",
                        "Padding": ""
                        }
                        ],
                        "BackgroundColor": "",
                        "StrokeWidth": "",
                        "Padding": ""
        }

handler_layout_lang_screen = {
                        "Value": "",
                        "Variable": "",
                        "type": "LinearLayout",
                        "weight": "0",
                        "height": "match_parent",
                        "width": "match_parent",
                        "orientation": "vertical",
                        "Elements": [
                            
                            {
                                "type": "SpinnerLayout",
                                "height": "wrap_content",
                                "width": "match_parent",
                                "weight": "0",
                                "Value": "Событие|@common_events",
                                "Variable": "event",
                                "gravity_horizontal": "left"
                            },
                            {
                                "type": "html",
                                "height": "wrap_content",
                                "width": "match_parent",
                                "weight": "0",
                                "Value": "@listener",
                                "Variable": "listener",
                                "gravity_horizontal": "left"
                            }
                            ,
                            {
                                "type": "SpinnerLayout",
                                "height": "wrap_content",
                                "width": "match_parent",
                                "weight": "0",
                                "Value": "Действие|@action_types",
                                "Variable": "action",
                                "gravity_horizontal": "left"
                            }
                            ,
                            {
                                "type": "SpinnerLayout",
                                "height": "wrap_content",
                                "width": "match_parent",
                                "weight": "0",
                                "Value": "Тип обработчика|@handler_types",
                                "Variable": "type",
                                "gravity_horizontal": "left"
                            }
                            ,
                            {
                                "type": "TextView",
                                "height": "wrap_content",
                                "width": "match_parent",
                                "weight": "0",
                                "Value": "Метод",
                                "gravity_horizontal": "left"
                            },
                            {
                                "type": "#type_method",
                                "height": "wrap_content",
                                "width": "match_parent",
                                "weight": "0",
                                "Value": "@method",
                                "Variable": "method",
                                "gravity_horizontal": "left"
                            }
                            ,
                            {
                        "Value": "",
                        "Variable": "",
                        "type": "LinearLayout",
                        "weight": "0",
                        "height": "match_parent",
                        "width": "match_parent",
                        "orientation": "vertical",
                        "Elements": [
                            {
                                "type": "TextView",
                                "height": "wrap_content",
                                "width": "match_parent",
                                "weight": "0",
                                "Value": "Обработчик postExecute",
                                "Variable": "",
                                "gravity_horizontal": "center"
                            },

                            
                            
                            {
                                "type": "SpinnerLayout",
                                "height": "wrap_content",
                                "width": "match_parent",
                                "weight": "0",
                                "Value": "Действие|@action_types",
                                "Variable": "action_postExecute",
                                "gravity_horizontal": "left"
                            }
                            ,
                            {
                                "type": "SpinnerLayout",
                                "height": "wrap_content",
                                "width": "match_parent",
                                "weight": "0",
                                "Value": "Тип обработчика|@handler_types",
                                "Variable": "type_postExecute",
                                "gravity_horizontal": "left"
                            }
                            ,
                            {
                                "type": "TextView",
                                "height": "wrap_content",
                                "width": "match_parent",
                                "weight": "0",
                                "Value": "Метод",
                                "gravity_horizontal": "left"
                            },
                            {
                                "type": "#_PE",
                                "height": "wrap_content",
                                "width": "match_parent",
                                "weight": "0",
                                "Value": "@method_postExecute",
                                "Variable": "method_postExecute",
                                "gravity_horizontal": "left"
                            }

                        ]
                        ,
                        "BackgroundColor": "#f5bd8c",
                        "StrokeWidth": "2",
                        "Padding": ""
                        }
                        ],
                        "BackgroundColor": "",
                        "StrokeWidth": "",
                        "Padding": ""
        }



def get_text_from_github(url,token):

  # send a request
  if token=="" or token==None:
    r = requests.get(url, headers={'accept': 'application/vnd.github.v3.raw'})  
  else:    
    r = requests.get(url, headers={'accept': 'application/vnd.github.v3.raw','authorization': 'token {}'.format(token)})

  
  if r.status_code>200:
    return None
  else:
    return r.text

def remove_uid(d):
    if 'uid' in d:
        d.pop('uid')
    return d    

def remove_empty(d):
    for k in list(d.keys()):
        if d[k]=="" or d[k]==None or d[k]==False:
           d.pop(k) 
    return d        

def get_recognition_template(name):
    if 'RecognitionTemplates' in session["configuration"]['ClientConfiguration']:
        res = list(filter(lambda item: item['name'] == name, session["configuration"]['ClientConfiguration']['RecognitionTemplates']))
        if len(res)>0:
            return json.dumps(remove_empty(res[0]),ensure_ascii=False)
    return None

def get_style(name):
    if 'StyleTemplates' in session["configuration"]['ClientConfiguration']:
        res = list(filter(lambda item: item['name'] == name, session["configuration"]['ClientConfiguration']['StyleTemplates']))
        if len(res)>0:
            return remove_empty(res[0])
    return None

def get_operation_elemets(root):
    new_element = copy.deepcopy(root) 
    new_element = remove_uid(new_element)
    new_element = remove_empty(new_element)

    if 'RecognitionTemplate' in new_element:
        template = get_recognition_template(new_element.get('RecognitionTemplate'))
        if template!=None:
            new_element['VisionSettings'] = template

    if 'style_name' in new_element:
        template = get_style(new_element.get('style_name'))
        if template!=None:
            if template.get("use_as_class",False)==True:
                new_element['style_class'] = new_element.get('style_name')        

        if "gravity_horizontal" in template:
            new_element["gravity_horizontal"] = get_key(gravity_elements,template["gravity_horizontal"])   

        if "BackgroundColor" in template:
            new_element["BackgroundColor"] = template["BackgroundColor"] 

        if "TextSize" in template:
            new_element["TextSize"] = template["TextSize"] 

        if "TextColor" in template:
            new_element["TextColor"] = template["TextColor"]     

        if "TextBold" in template:
            new_element["TextBold"] = template["TextBold"]     

        if "TextItalic" in template:
            new_element["TextItalic"] = template["TextItalic"]     

        if "drawable" in template:
            new_element["drawable"] = template["drawable"] 

        if "NumberPrecision" in template:
            new_element["NumberPrecision"] = template["NumberPrecision"]          

        if "weight" in template:
            new_element["weight"] = template["weight"] 

        if not "weight" in template:
            new_element["weight"] = 0     

        if "width" in template:
            if get_key(scale_elements,template["width"])=="manual":
                if len(template["width_value"])>0:
                    width = int(template["width_value"])
                else:    
                    width = 0
            else:
                width  = get_key(scale_elements,template["width"])

            new_element["width"]    = width
            new_element["width_value"]    = template["width"]
            
        if "height" in template:
            if get_key(scale_elements,template["height"])=="manual":
                if len(template["height_value"])>0:
                    width = int(template["height_value"])
                else:    
                    width = 0
            else:
                width  = get_key(scale_elements,template["height"])

            new_element["height"]    = width
            new_element["height_value"]    = template["height"]    


    
    if 'Elements' in root:
        new_element['Elements'] = []
        for element in root['Elements']:
            el = get_operation_elemets(element)

            if not "weight" in el:
                el["weight"] = "0" 

            if not "height" in el:
                el["height"] = "wrap_content" 

            if not "width" in el:
                el["width"] = "wrap_content"  
                
            if "width" in el:
                if get_key(scale_elements,el["width"])=="manual":
                    if "width_value" in el:
                        if len(el["width_value"])>0:
                            width = int(el["width_value"])
                        else:    
                            width = 0
                    else:
                        width = 0        
                else:
                    width  = get_key(scale_elements,el["width"])

                el["width"]    = width
                el["width_value"]    = el["width"]
            
            if "height" in el:
                if get_key(scale_elements,el["height"])=="manual":
                    if "height_value" in el:
                        if len(el["height_value"])>0:
                            width = int(el["height_value"])
                        else:    
                            width = 0
                    else:
                        width = 0
                        
                else:
                    width  = get_key(scale_elements,el["height"])

                el["height"]    = width
                el["height_value"]    = el["height"]     
                
            new_element['Elements'].append(el)

    return new_element        

def init(hashMap,_files=None,_data=None):

    hashMap.put("GetCookies","")
    return hashMap


def configuration_open(hashMap,_files=None,_data=None):    

    #_configuration  = json.loads(hashMap.get("configuration"))

   
    hashMap.put("host_uid",session["host_uid"]) 
    hashMap.put("Launch_elements",captions_start_screen_elements)

    hashMap.put("HTMLHead",'<code-input required id="HTMLHead" style="resize: both; overflow: hidden; width: 100%;" lang="HTML" placeholder="Write some script!"></code-input>')
    hashMap.put("HTMLdocument_ready",'<code-input required id="HTMLdocument_ready" style="resize: both; overflow: hidden; width: 100%;" lang="JavaScript" placeholder="Write some JavaScript!"></code-input>')
    hashMap.put("PyGeneral",'<code-input required id="PyGeneral" style="resize: both; overflow: hidden; width: 100%;" lang="Python" placeholder="Write some Python!"></code-input>')
    hashMap.put("PelicanInit",'<code-input required id="PelicanInit" style="resize: both; overflow: hidden; width: 100%;" lang="JSON"></code-input>')
    
    for prop in configuration_properties_list:
        hashMap.put(prop,session["configuration"]['ClientConfiguration'].get(prop,""))
        if prop == "Launch":
            hashMap.put(prop,get_synonym(start_screen_elements,session["configuration"]['ClientConfiguration'].get(prop,"")))
        elif prop == "HTMLHead":

            txt = base64.b64decode(session["configuration"]['ClientConfiguration'].get(prop,"")).decode("utf-8")

            text =  '<code-input required id="HTMLHead" style="resize: both; overflow: hidden; width: 100%;" lang="HTML" placeholder="Write some script!">'+txt+'</code-input>'
            
            hashMap.put(prop,text)    
        
        elif prop == "HTMLdocument_ready":
            
            txt = base64.b64decode(session["configuration"]['ClientConfiguration'].get(prop,"")).decode("utf-8")

            text =  '<code-input required id="HTMLdocument_ready" style="resize: both; overflow: hidden; width: 100%;" lang="JavaScript" placeholder="Write some JavaScript!">'+txt+'</code-input>'
            
            hashMap.put(prop,text) 

        elif prop == "PyGeneral":
            
            txt = base64.b64decode(session["configuration"]['ClientConfiguration'].get(prop,"")).decode("utf-8")

            text =  '<code-input required id="PyGeneral" style="resize: both; overflow: hidden; width: 100%;" lang="Python" placeholder="Write some Python!">'+txt+'</code-input>'
            
            hashMap.put(prop,text) 
            
        elif prop == "PelicanInit":
            
            txt = session["configuration"]['ClientConfiguration'].get(prop,"")

            text =  '<code-input required id="PelicanInit" style="resize: both; overflow: hidden; width: 100%;" lang="JSON">'+txt+'</code-input>'
            
            hashMap.put(prop,text) 


    if "ConfigurationSettings" in  session["configuration"]['ClientConfiguration']:
        for prop in configuration_settings_list:
            hashMap.put(prop,session["configuration"]['ClientConfiguration']["ConfigurationSettings"].get(prop,""))


    #if filename!=None:
    
    filename = session["host_uid"]+".ui"

    link = WS_URL+":"+str(WSPORT)+"/get_conf_text?filename="+session["host_uid"]+".ui"

    jqr = {
            "RawConfigurationURL":link,
            "RawConfigurationServiceAuth": "",
            "RawConfigurationServiceON": True,
            "OnlineSplitMode": True,
            }

    img = qrcode.make(json.dumps(jqr)) 
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    hashMap.put("qr",img_str)  
    

    hashMap.put("url_configuration",'<html><body>URL конфигурации: <a href="'+link+'">' +link+ '</a></body></html>')  
    
    if "ConfigurationFileName" in session["configuration"]['ClientConfiguration']:
        hashMap.put("download_configuration",'Файл конфигурации можно скачать тут: <a href="/download_file?filename='+Path(filename).name+'" target="_blank" download="'+ session["configuration"]['ClientConfiguration']['ConfigurationFileName']+ '">скачать конфигурацию</a>')     
    elif session["filename_base"]!=None:
        hashMap.put("download_configuration",'Файл конфигурации можно скачать тут: <a href="/download_file?filename='+Path(filename).name+'" target="_blank" download="'+ session["filename_base"]+ '">скачать конфигурацию</a>')     
    else:    
        hashMap.put("download_configuration",'Файл конфигурации можно скачать тут: <a href="/download_file?filename='+Path(filename).name+'" target="_blank" ">скачать конфигурацию</a>')     

    return hashMap


def update_configuration_properties(write_file=True):

    isPython = False
    isOnline = False
    isCV=False

    if 'PyHandlers' in session["configuration"]['ClientConfiguration']:
        if len(session["configuration"]['ClientConfiguration']['PyHandlers'])>0:
            isPython=True
  
    if 'DefServiceConfiguration' in session["configuration"]['ClientConfiguration']:
        if len(session["configuration"]['ClientConfiguration']['DefServiceConfiguration'])>0:
            isPython=True  

    if 'OnlineServiceConfiguration' in session["configuration"]['ClientConfiguration']:
        if len(session["configuration"]['ClientConfiguration']['OnlineServiceConfiguration'])>0:
            isOnline=True            
            

    if 'Processes' in session["configuration"]['ClientConfiguration']:        
        for process in session["configuration"]['ClientConfiguration']['Processes']:
            if process['type']=='Process' and 'Operations' in process:
                for operation in process['Operations']:
                    if len(operation.get('PythonOnCreate',''))>0 or len(operation.get('PythonOnInput',''))>0 or len(operation.get('DefOnCreate',''))>0 or len(operation.get('DefOnInput',''))>0 :
                        isPython=True
                        if len(operation.get('PythonOnCreate',''))>0 or len(operation.get('DefOnCreate',''))>0:
                            operation['send_when_opened']=True
                    if len(operation.get('DefOnlineOnCreate',''))>0  :
                        operation['onlineOnStart']=True
                        operation['send_when_opened']=True
                        isOnline=True
                    else:
                        operation['onlineOnStart']=False 

                    if len(operation.get('DefOnAfterCreate',''))>0  :
                        isPython=True
                        if len(operation.get('DefOnAfterCreate',''))>0:
                            operation['send_after_opened']=True
                    if len(operation.get('DefOnlineOnAfterCreate',''))>0  :
                        operation['onlineOnAfterStart']=True
                        operation['send_after_opened']=True
                        isOnline=True
                    else:
                        operation['onlineOnAfterStart']=False      
                          
                    if len(operation.get('DefOnlineOnInput',''))>0 :
                        operation['onlineOnInput']=True
                        isOnline=True    
                    else:    
                        operation['onlineOnInput']=False
            if process['type']=='CVOperation' and 'CVFrames' in process:
                for operation in process['CVFrames']:
                        isCV=True
                        if len(operation.get('CVFrameOnlineOnCreate',''))>0 or len(operation.get('CVFrameOnlineOnNewObject',''))>0 or len(operation.get('CVFrameOnlineAction',''))>0 or len(operation.get('CVFrameOnlineOnTouch',''))>0 :
                            operation['CVOnline']=True
                            isOnline=True
                        else:
                            operation['CVOnline']=False    
                        if len(operation.get('CVFrameDefOnCreate',''))>0 or len(operation.get('CVFrameDefOnNewObject',''))>0 or len(operation.get('CVFrameDefAction',''))>0 or len(operation.get('CVFrameDefOnTouch',''))>0  or len(operation.get('CVFramePythonOnCreate',''))>0 or len(operation.get('CVFramePythonOnNewObject',''))>0 or len(operation.get('CVFramePythonAction',''))>0 or len(operation.get('CVFramePythonOnTouch',''))>0 :
                            isPython=True
                           

    if isPython:
        session["configuration"]['ClientConfiguration']['RunPython']  =True   

            
    tags=[]
    if isPython:
        tags.append('Py') 
        tags.append('off-line')        
    if isOnline:
        tags.append('Online')        
    if isCV:
        tags.append('ActiveCV®')    

    session["configuration"]['ClientConfiguration']['ConfigurationTags']=",".join(tags) 


        

def save_configuration(configuration,hashMap,full=False):

    no_agent=False

    #configuration["ClientConfiguration"]["agent"] = hashMap.get("agent")
    if full:
        update_configuration_properties()
    filename = hashMap.get("base_path")+os.sep+"uploads"+os.sep+session["host_uid"]+".ui"

    FilePyHandlers = None
    FilePyFiles = None
    if configuration["ClientConfiguration"].get("agent") == True:
        if os.path.isfile(filename): 
            with open(filename, "r",encoding="utf-8") as file:
                old_configuration = json.load(file) 
                
                FilePyHandlers = old_configuration["ClientConfiguration"].get("PyHandlers")
                
                if "PyFiles" in old_configuration["ClientConfiguration"]:
                    FilePyFiles = old_configuration["ClientConfiguration"]["PyFiles"]



    
    new_configuration = copy.deepcopy(configuration)
    new_configuration['ClientConfiguration']['Processes'] =[]

    for process in session["processes_table"]:
        if process.get('type') == 'CVOperation':
            new_process = copy.deepcopy(process)
            new_process = remove_uid(new_process)
            new_process = remove_empty(new_process)
            
            new_process['CVFrames'] = []

            if 'CVFrames' in process:
                for frame in process['CVFrames']:
                    new_operation = copy.deepcopy(frame)
                    new_operation = remove_uid(new_operation)
                    new_operation = remove_empty(new_operation)
                    new_operation['CVOnline']=False

                    if 'RecognitionTemplate' in new_operation:
                        template = get_recognition_template(frame.get('RecognitionTemplate'))
                        if template!=None:
                            new_operation['VisionSettings'] = template
                    new_process['CVFrames'].append(new_operation)        
            
            new_configuration['ClientConfiguration']['Processes'].append(new_process)

        elif process.get('type') == 'Process':
            new_process = copy.deepcopy(process)
            new_process = remove_uid(new_process)
            new_process = remove_empty(new_process)
            
            new_process['Operations'] = []

            if 'Operations' in process:
                for operation in process['Operations']:
                    new_operation = copy.deepcopy(operation)
                    new_operation = remove_uid(new_operation)
                    new_operation = remove_empty(new_operation)
                    

                    
                    res = get_operation_elemets(operation)  
                    if 'Elements' in res:
                        new_operation['Elements']  = res['Elements']

                    new_process['Operations'].append(new_operation)      

            new_configuration['ClientConfiguration']['Processes'].append(new_process)

    uid = new_configuration["ClientConfiguration"].get('uid')
    if uid ==None:
        uid = str(uuid.uuid4().hex) 
        new_configuration["ClientConfiguration"]["uid"]=uid
    
    

    
    if full:
        hashMap.put("RefreshScreen","")
        #write handlers
        if "GitHubHandlers" in new_configuration["ClientConfiguration"]:
            handlers_url = new_configuration["ClientConfiguration"]["GitHubHandlers"]
            handlers_token = new_configuration["ClientConfiguration"]["GitHubToken"]

            if len(handlers_url)>0:

                handlers_txt = get_text_from_github(handlers_url,handlers_token)
                if handlers_txt!=None:
                    new_configuration["ClientConfiguration"]["PyHandlers"] = base64.b64encode(handlers_txt.encode('utf-8')).decode('utf-8')
                else:
                    hashMap.put("toast", "Ошибка получения данных из GitHub")

                if "PyFiles" in configuration["ClientConfiguration"]:
                    for filestr in configuration["ClientConfiguration"]["PyFiles"]:
                        if  len(filestr.get("PyFileLink",""))>0:
                            handlers_txt = get_text_from_github(filestr.get("PyFileLink",""),handlers_token)
                            if handlers_txt!=None:
                                filestr["PyFileData"] = base64.b64encode(handlers_txt.encode('utf-8')).decode('utf-8')
        elif new_configuration["ClientConfiguration"].get("agent") == True and not no_agent:
            if FilePyHandlers!=None:
                new_configuration["ClientConfiguration"]["PyHandlers"] = FilePyHandlers
            if FilePyFiles!=None:
                new_configuration["ClientConfiguration"]["PyFiles"] = FilePyFiles    

    session["configuration_file"] = new_configuration
    with open(filename, 'w',encoding="utf-8") as f:
        json.dump(new_configuration, f,ensure_ascii=False,indent=4)

    if full:
        if hashMap.containsKey("_cookies"):
            jcookie = json.loads(hashMap.get("_cookies"))

            if str(jcookie.get("ui_to_github")).lower()=="true":
                if new_configuration["ClientConfiguration"].get("ConfigurationFileName")!="" and new_configuration["ClientConfiguration"].get("ConfigurationFileName")!=None:
                    r = push_to_github(filename, jcookie.get("ui_repo"), jcookie.get("ui_branch"), jcookie.get("ui_token"),new_configuration["ClientConfiguration"]["ConfigurationFileName"],jcookie.get("ui_folder", ""))
                    if r==False:
                        hashMap.put("toast","Не получилось отправить на GitHub")
        
        

def push_to_github(filename, repo, branch, token,gitfilename,folder):

    if branch=="" or branch==None:
        branch="main"

    url="https://api.github.com/repos/"+repo+"/contents/"+folder+"/"+gitfilename

    base64content=base64.b64encode(open(filename,"rb").read())

    if token!="":
        r = requests.get(url+'?ref='+branch, headers = {"Authorization": "token "+token})
       
    else:    
        r = requests.get(url+'?ref='+branch)
        
    data = r.json()
    if r.status_code==401:
        return False

    if data.get("message") == "Not Found" or r.status_code=="404":
        message = json.dumps({"message":"Initial commit",
                                "branch": branch,
                                "content": base64content.decode("utf-8") ,
                               
                                })

        if token!="":
            resp=requests.put(url, data = message, headers = {"Content-Type": "application/json", "Authorization": "token "+token})
        else:    
            resp=requests.put(url, data = message)

        if resp.status_code>203:    
            print(resp.text) 
            return False  

    else:        
        sha = data['sha']

        if base64content.decode('utf-8')+"\n" != data['content']:
            message = json.dumps({"message":"update",
                                "branch": branch,
                                "content": base64content.decode("utf-8") ,
                                "sha": sha
                                })

            if token!="":
                resp=requests.put(url, data = message, headers = {"Content-Type": "application/json", "Authorization": "token "+token})
            else:    
                resp=requests.put(url, data = message)

           
        else:
            print("nothing to update") 
            return False  
             
    return True     

def configuration_input(hashMap,_files=None,_data=None):

    if hashMap.containsKey("set_configuration"):
        session["configuration"] = json.loads(hashMap.get("configuration"))
        session["filename"] = hashMap.get("filename")
        session["filename_base"] = hashMap.get("filename_base")

        hashMap.remove("set_configuration")
        hashMap.remove("configuration")
        hashMap.remove("filename")
        hashMap.remove("filename_base")
        
        if "host_uid" in session["configuration"]["ClientConfiguration"]:
            session["host_uid"] = session["configuration"]["ClientConfiguration"]["host_uid"]
        else:
            session["host_uid"] =  str(uuid.uuid4().hex)  
            session["configuration"]["ClientConfiguration"]["host_uid"] = session["host_uid"]

        session["processes_table"] = session["configuration"]["ClientConfiguration"]["Processes"] 

    if hashMap.get("listener") == "btn_upload":
        hashMap.put("GetCookies","")

        id = "configuration_file"
        hashMap.put("UploadFile",id)
    # elif hashMap.get("listener") == "btn_test":    
    #     var2 = hashMap.get("ConfigurationName")
    #     session["var1"] = hashMap.get("ConfigurationName")
    # elif hashMap.get("listener") == "btn_test2":    
    #     hashMap.put("toast","var1="+session["var1"]+", var2="+var2)
    elif hashMap.get("listener") == "btn_new_configuration":
        hashMap.put("GetCookies","")      

        #generating new uuid for SimpleUI configuration
        current_uid = uuid.uuid4().hex
            #create simple template of SimpleUi configuration
        session["configuration"]={"ClientConfiguration":
        {"ConfigurationName": 'Новая конфигурация',"ConfigurationDescription": "Создание новой конфигурации", "ConfigurationVersion": "0.0.1", "Processes":[
                            {
                        "type": "Process",
                        "ProcessName": "Новый процесс",
                        "Operations": [
                        {
                            "type": "Operation",
                            "Name": "Новый экран" ,
                            "Elements":[]
                        }
                       ]
                }
            ]
            ,
            "ConfigurationSettings":   {
                "uid": current_uid
            }
            }
            }

        session["host_uid"] =  str(uuid.uuid4().hex)  
        session["configuration"]["ClientConfiguration"]["host_uid"] = session["host_uid"] 

        session["processes_table"] = session["configuration"]["ClientConfiguration"]["Processes"] 

        save_configuration(session["configuration"],hashMap,True) 

        hashMap.put("RefreshScreen","")  
        
    elif hashMap.get("listener") == "upload_file":    
        

        session["filename"] =hashMap.get("base_path")+os.sep+"uploads"+os.sep+ hashMap.get("filename")
        session["filename_base"] = hashMap.get("filename")[21:]
        with open(session["filename"],encoding="utf-8") as conf_file:
            session["configuration"] = json.load(conf_file)

            hashMap.put("configuration",json.dumps(session["configuration"],ensure_ascii=False))
            hashMap.put("filename",session["filename_base"])
            hashMap.put("filename_base",json.dumps(session["configuration"],ensure_ascii=False))
            hashMap.put("set_configuration","")
            
            session["configuration"]["ClientConfiguration"]["ConfigurationFileName"] = session["filename_base"]

            if "host_uid" in session["configuration"]["ClientConfiguration"]:
                session["host_uid"] = session["configuration"]["ClientConfiguration"]["host_uid"]
            else:
                session["host_uid"] =  str(uuid.uuid4().hex)  
                session["configuration"]["ClientConfiguration"]["host_uid"] = session["host_uid"]
    
            session["processes_table"] = session["configuration"]["ClientConfiguration"]["Processes"] 

            save_configuration(session["configuration"],hashMap,True)
            hashMap.put("RefreshScreen","")
      
    elif hashMap.get("listener") == "btn_download":
        session["filename"] = session["host_uid"]+".ui" 
        hashMap.put("DownloadFile",session["filename"])  
            
    elif hashMap.get("listener") == "btn_upload_github":   
        url = 'https://api.github.com/repos/dvdocumentation/simple_editor/contents/_debug_template.py'
        req = requests.get(url)
        if req.status_code == requests.codes.ok:
            req = req.json()  # the response is a JSON
            # req is now a dict with keys: name, encoding, url, size ...
            # and content. But it is encoded with base64.
            content = base64.b64decode(req['content']).decode("utf-8")
        else:
            print('Content was not found.')

    elif hashMap.get("listener") == "btn_save_configuration": 
        for prop in configuration_properties_list:
            session["configuration"]['ClientConfiguration'][prop] = hashMap.get(prop)

            if prop == "Launch":
                session["configuration"]['ClientConfiguration'][prop] = get_key(start_screen_elements,hashMap.get(prop))

            if prop == "HTMLHead":
                section_string = hashMap.get(prop)    
                session["configuration"]['ClientConfiguration'][prop] = base64.b64encode(section_string.encode('utf-8')).decode('utf-8')

            if prop == "HTMLdocument_ready":
                section_string = hashMap.get(prop)    
                session["configuration"]['ClientConfiguration'][prop] = base64.b64encode(section_string.encode('utf-8')).decode('utf-8')    

            if prop == "PyGeneral":
                section_string = hashMap.get(prop)    
                session["configuration"]['ClientConfiguration'][prop] = base64.b64encode(section_string.encode('utf-8')).decode('utf-8')    

                
                
        if not 'ConfigurationSettings' in session["configuration"]['ClientConfiguration']: session["configuration"]['ClientConfiguration']['ConfigurationSettings']={}

        for prop in configuration_settings_list:
            session["configuration"]['ClientConfiguration']['ConfigurationSettings'][prop] = hashMap.get(prop)

            if hashMap.get("vendor_login")!=None and hashMap.get("vendor_login")!="":
                authstring =hashMap.get("vendor_login")+":"+ hashMap.get("vendor_password")
                session["configuration"]['ClientConfiguration']['ConfigurationSettings']['vendor_auth']=  'Basic '+   base64.b64encode(authstring.encode('utf-8')).decode('utf-8') 

            if hashMap.get("handler_login")!=None and hashMap.get("handler_login")!="":
                authstring =hashMap.get("handler_login")+":"+ hashMap.get("handler_password")
                session["configuration"]['ClientConfiguration']['ConfigurationSettings']['handler_auth']=  'Basic '+   base64.b64encode(authstring.encode('utf-8')).decode('utf-8')    

    
        save_configuration(session["configuration"],hashMap,True)
        hashMap.put("RefreshScreen","")

    return hashMap


session["current_process_name"] = ""

def get_synonym(elements,key):
    if key in elements:
        return  elements[key]
    else:
        return key    

def get_key(elements,value):
    for key, val in elements.items():
        if val == value:
            return key
    return value        

def get_title_list(elements):
    result =[]
    result.append("")
    for  val in elements.items():
        result.append(val[1])      
    return ";".join(result)

with open(locale_filename, 'r',encoding='utf-8') as file:
    data = file.read()
    
    jlocale  =json.loads(data)


#translation by current setting
def get_locale(key):
    if key in jlocale:
        return jlocale.get(key,key)
    else:    
        return key


#elements=["","LinearLayout","barcode","HorizontalGallery","voice","photo","photoGallery","signature","Vision","Cart","Tiles","ImageSlider","MenuItem","Tabs","Tab","fab"]

screen_elements = {"LinearLayout":get_locale("layout"),"barcode":get_locale("barcode"),"HorizontalGallery":get_locale("horizontal_gallery"),
"voice":get_locale("voice_input"),"photo":get_locale("camera_capture"),"photoGallery":get_locale("gallery"),"voice":get_locale("tts"),"signature":get_locale("signature"),
"Vision":get_locale("ocr"),"Cart":get_locale("cart"),"Tiles":get_locale("tiles"),"ImageSlider":get_locale("image_slider"),"MenuItem":get_locale("menu_item"),"Tabs":get_locale("Tabs"),"Tab":get_locale("Tab"),"fab":get_locale("fab")}
captions_screen_elements = get_title_list(screen_elements)

layout_elements = {"LinearLayout":get_locale("layout"),"Tabs":get_locale("Tabs"),"Tab":get_locale("Tab"),"TextView":get_locale("title"),"Button":get_locale("button"),
"EditTextText":get_locale("string_input"),"EditTextNumeric":get_locale("numeric_input"),"EditTextPass":get_locale("password_input"),"EditTextAuto":get_locale("event_input"),"EditTextAutocomplete":get_locale("autocompete_input"),
"ModernEditText":get_locale("modern_input"),"Picture":get_locale("picture"),"CheckBox":get_locale("checkbox"),"Gauge":get_locale("gauge"),"Chart":get_locale("chart"),"SpinnerLayout":get_locale("spinner"),"TableLayout":get_locale("table"),"CartLayout":get_locale("cart"),
"MultilineText":get_locale("multiline"),"CardsLayout":get_locale("cards"),"CButtons":get_locale("buttons_list"),"CButtonsHorizontal":get_locale("horizontal_buttons_list"),"DateField":get_locale("date_input"),"ProgressButton":get_locale("progress_button"),"html":get_locale("HTML"),"map":get_locale("map"),"file":get_locale("file"),"object":get_locale("object"),"camera":get_locale("camera")}
captions_layout_elements =get_title_list(layout_elements)

orientation_elements = {"vertical":get_locale("vertical"),"horizontal":get_locale("horizontal")}
captions_orientation_elements =get_title_list(orientation_elements)

scale_elements = {"match_parent":get_locale("mach_parent") ,"wrap_content":get_locale("wrap_content"),"manual":get_locale("manual")}
captions_scale_elements = get_title_list(scale_elements)

gravity_elements = {"left":get_locale("left"),"right":get_locale("right"),"center":get_locale("center")}
captions_gravity_elements = get_title_list(gravity_elements)

vertical_gravity_elements = {"top":get_locale("top"),"bottom":get_locale("bottom"),"center":get_locale("center")}
captions_vertical_gravity_elements = get_title_list(vertical_gravity_elements)

icon_elements = ['','forward','backward','run','cancel','edit','picture','info','settings','plus','save','search','send','done']

detector_elements = {"Barcode":get_locale("barcodes"),"OCR":get_locale("ocr"),"Objects_Full":get_locale("ocr_and_barcodes"),"Objects_OCR":get_locale("objects_ocr"),
"Objects_Barcode":get_locale("objects_barcode"),"Objects_f1":get_locale("face_detection"),"multiscanner":get_locale("multiscanner"),"globalmultiscanner":get_locale("globalmultiscanner"),"featurescanner":get_locale("featurescanner"),"object_opencv":get_locale("object_opencv"),"face_opencv":get_locale("face_opencv")}
captions_detector_elements = get_title_list(detector_elements)

visual_mode_elements = {"list_only":get_locale("list_only"),"green_and_grey":get_locale("green_and_grey"),"green_and_red":get_locale("green_and_red"),"list_and_grey":get_locale("list_and_grey")}
captions_visual_mode_elements = get_title_list(visual_mode_elements)

resolution_elements = ['','4K','2K','HD1080','HD720','VGA','QVGA']

start_screen_elements = {"Menu":get_locale("operations_menu"),"Tiles":get_locale("tiles_menu"),"Process":"process"}
captions_start_screen_elements  = get_title_list(start_screen_elements)

detector_mode_elements = {"train":get_locale("training") ,"predict":get_locale("prediction")}
captions_detector_mode_elements = get_title_list(detector_mode_elements)

camera_mode_elements = {"Back":get_locale("rear"),"Front":get_locale("front")}
captions_camera_mode_elements = get_title_list(camera_mode_elements)

event_elements_cv = {"OnCreate":get_locale("OnCreate"),"OnObjectDetected":get_locale("OnObjectDetected"),"OnTouch":get_locale("OnTouch"),"OnInput":get_locale("OnInput")}
captions_event_elements_cv = get_title_list(event_elements_cv)



def make_processes_table(processes_table):
    t = {
        "type": "table",
        "textsize": "20",
        "hidecaption": "false",
        "hideinterline": "false",

        "columns": [
           
        {
            "name": "ProcessName",
            "header": "Процесс",
            "weight": "2",
            "gravity":"left"
        }
        ]
        }   

    rows = []
    for p in processes_table:
        new_p = {}
        if "ProcessName" in p:
            new_p["ProcessName"] = p["ProcessName"]
        elif "CVOperationName" in p:
            new_p["ProcessName"] = p["CVOperationName"] 
        rows.append(new_p)    
    t['rows'] = rows

    return t

def make_mediafiles_table(table):
    t = {
        "type": "table",
        "textsize": "20",
        "hidecaption": "false",
        "hideinterline": "false",
        "columns": [
           
        {
            "name": "MediafileKey",
            "header": "Ключ",
            "weight": "2",
            "gravity":"left"
           
        },
        {
            "name": "MediafileExt",
            "header": "Расширение",
            "weight": "2",
            "gravity":"left"
           
        }
        ]
        }   

    t['rows'] = table

    return t


def make_onefield_table(table,field_name,field_caption):
    t = {
    "type": "table",
    "textsize": "20",
    "hidecaption": "false",
    "hideinterline": "false",
     "columns": [
       
    {
        "name": field_name,
        "header": field_caption,
        "weight": "2",
        "gravity":"left"
    }
    ]
    }  

    t['rows'] = table

    return t


def make_screenelements_table(layout_table):

    for s in layout_table:
        s["type_s"] = get_synonym(screen_elements,s["type"])

    t = {
    "type": "table",
    "textsize": "25",
    "hidecaption": "false",
    "hideinterline": "true",
    "columns": [
        
    {
        "name": "type_s",
        "header": "Тип элемента",
        "weight": "1",
        "gravity":"left"
    },
    {
        "name": "Value",
        "header": "Значение",
        "weight": "1",
        "gravity":"left"
    },
    {
        "name": "Variable",
        "header": "Переменная",
        "weight": "1",
        "gravity":"left"
    }
    ]
    }  

    t['rows'] = layout_table

    return t

def make_timers_table(_table):
    t = {
    "type": "table",
    "textsize": "25",
    "hidecaption": "false",
    "columns": [
       
        {
        "name": "PyTimerTaskKey",
        "header": "Ключ",
        "weight": "1",
        "gravity":"left"
    },
        {
        "name": "PyTimerTaskPeriod",
        "header": "Период",
        "weight": "1",
        "gravity":"left"
    },
        {
        "name": "PyTimerTaskDef",
        "header": "Метод/alias",
        "weight": "1",
        "gravity":"left"
    },
        {
        "name": "PyTimerTaskBuilIn",
        "header": "Built-in",
        "weight": "1",
        "gravity":"left"
    }

    ]
    }  

    t['rows'] = _table

    return t

def make_menu_table(_table):
    t = {
    "type": "table",
    "textsize": "25",
    "hidecaption": "false",
    "columns": [
       
        {
        "name": "MenuItem",
        "header": "Элемент",
        "weight": "1",
        "gravity":"left"
    },
        {
        "name": "MenuTitle",
        "header": "Заголовок",
        "weight": "1",
        "gravity":"left"
    },
        {
        "name": "MenuId",
        "header": "ID",
        "weight": "1",
        "gravity":"left"
    },
        {
        "name": "MenuTop",
        "header": "В тулбаре",
        "weight": "1",
        "gravity":"left"
    }

    ]
    }  

    t['rows'] = _table

    return t

def make_layoutelements_table(layout_table):

    for s in layout_table:
        s["type_s"] = get_synonym(layout_elements,s["type"])

    t = {
    "type": "table",
    "textsize": "25",
    "hidecaption": "false",
    "columns": [
    
        
    {
        "name": "type_s",
        "header": "Тип элемента",
        "weight": "2",
        "gravity":"left"
    },
     {
        "name": "Value",
        "header": "Значение",
        "weight": "2",
        "gravity":"left"
    },
     {
        "name": "Variable",
        "header": "Переменная",
        "weight": "2",
        "gravity":"left"
    }
    ]
    }  

    t['rows'] = layout_table

    return t


def make_handlers_table(table,use_alias):
    t = {
    "type": "table",
    "textsize": "20",
    "hidecaption": "false",
    "hideinterline": "false",
    "columns": [
       
    {
        "name": "event",
        "header": "Событие",
        "weight": "1",
        "gravity":"left"
    },
    {
        "name": "action",
        "header": "Действие",
        "weight": "1",
        "gravity":"left"
    },
    {
        "name": "listener",
        "header": "listener",
        "weight": "1",
        "gravity":"left"
    },
    {
        "name": "type",
        "header": "тип обработчика",
        "weight": "1",
        "gravity":"left"
    },
    {
        "name": "method",
        "header": "Метод",
        "weight": "2",
        "gravity":"left"
    }
    ,
    {
        "name": "postExecute",
        "header": "postExecute",
        "weight": "1",
        "gravity":"left"
    }
    ]
    }  

    if use_alias:
        t["columns"].append({
        "name": "alias",
        "header": "alias",
        "weight": "1",
        "gravity":"left"
    })

    ctable = copy.deepcopy(table)
    for line in ctable:
        if line.get("type")=='js' or line.get("type")=='pythonscript':
            line['method'] ="script..."
        pe = line.get("postExecute")
        postExecute=""
        if pe!=None and pe!="":
            jpe = json.loads(pe)
            if isinstance(jpe, list) :
                if len(jpe)>0:
                    postExecute =  pe    
                    
                    if jpe[0].get("type","")=="js": 
                        jpe[0]["method"]   ="script..."
                        postExecute = json.dumps(jpe,ensure_ascii=False)


        
        line['postExecute'] =postExecute    

    t['rows'] = ctable

    return t

def main_tab_selected(hashMap,_files=None,_data=None):

    CurrentTabKey = hashMap.get("CurrentTabKey")
    if CurrentTabKey in session["current_parent_dict"]:
        session["current_parent"] = session["current_parent_dict"][CurrentTabKey]
        session["current_element"] = session["current_parent"][0]

        if session["current_element"]!=None:
            if session["current_element"].get("type") == "Process" or "ProcessName" in session["current_element"]:
                session["processes_table_id"] = session["processes_table"].index(session["current_element"])
            elif session["current_element"].get("type") == "Operation":    
                if session["current_parent"][1]!=None:
                    if session["current_parent"][1][0]!=None:
                        if "Operations" in session["current_parent"][1][0]:
                            session["screens_table_id"] = session["current_parent"][1][0]["Operations"].index(session["current_element"])
    hashMap.put("RefreshScreen","")                

    return hashMap

def processes_open(hashMap,_files=None,_data=None):

    if session["processes_table"]!=None:
        
        hashMap.put("processes_table",json.dumps(make_processes_table(session["processes_table"]),ensure_ascii=False))
 
    return hashMap

def process_input(hashMap,_files=None,_data=None):

    if session["current_element"]==None:
        closeuid  =hashMap.get("process_uid")
    else:    
        closeuid = session["current_element"]['uid']

    if hashMap.get("listener")=="btn_save" or hashMap.get("listener")=="btn_add_screen" or hashMap.get("listener")=="btn_edit_screen":


        if session["processes_table_id"]==-1:
            session["processes_table"].append({
                                                    "ProcessName": hashMap.get("process_name"),
                                                    "PlanFactHeader": hashMap.get("PlanFactHeader"),
                                                    "hidden": hashMap.get("hidden"),
                                                    "DefineOnBackPressed": hashMap.get("DefineOnBackPressed"),
                                                    "login_screen": hashMap.get("login_screen"),
                                                    "SC": hashMap.get("SC"),
                                                    "type":"Process",                                                   
                                                    "uid": closeuid,
                                                    "Operations":[]
                                                
                                                })
            session["processes_table_id"]=len(session["processes_table"])-1

        else:   
            session["current_element"]["ProcessName"] =hashMap.get("process_name") 
            session["current_element"]["PlanFactHeader"] =hashMap.get("PlanFactHeader") 
            session["current_element"]["hidden"] =hashMap.get("hidden") 
            session["current_element"]["DefineOnBackPressed"] =hashMap.get("DefineOnBackPressed") 
            session["current_element"]["login_screen"] =hashMap.get("login_screen") 
            session["current_element"]["SC"] =hashMap.get("SC") 
            session["current_element"]["uid"] =closeuid 
          
        
        session["current_parent"] = (session["processes_table"][session["processes_table_id"]],None)
        session["current_element"] = session["current_parent"][0]
        session["current_parent_dict"][closeuid] = session["current_parent"]


    if hashMap.get("listener")=="btn_save" or hashMap.get("listener")=="btn_close":

        hashMap.put("CloseTab",closeuid)

        hashMap.put("processes_table",json.dumps(make_processes_table(session["processes_table"]),ensure_ascii=False))

        hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"main_screen", "key":"Процессы", "reopen":True},ensure_ascii=False))

        save_configuration(session["configuration"],hashMap)
     
    elif hashMap.get("listener")=="btn_add_screen":

        uid = str(uuid.uuid4().hex)
        hashMap.put("screen_uid",uid)

        hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"screen_form","key":uid,"reopen":True},ensure_ascii=False))  
        session["current_process_name"] = "Новый экран"
        hashMap.put("screen_name",session["current_process_name"])
        hashMap.put("Timer","")
        hashMap.put("hideToolBarScreen","")
        hashMap.put("noScroll","")
        hashMap.put("handleKeyUp","")
        hashMap.put("noConfirmation","")
        hashMap.put("hideBottomBarScreen","")
        hashMap.put("SetTitle","Новый экран - *")

        #блокировка
        #hashMap.put("BlockTabs","")

        session["screens_table_id"] = -1
        session["current_element"] = None 
        session["current_parent"] = (None,session["current_parent"])
        session["current_parent_dict"][uid] = session["current_parent"]   
    elif hashMap.get("listener")=="btn_edit_screen" or (hashMap.get("listener") == "TableDoubleClick"):
        session["screens_table_id"] = int(hashMap.get("selected_line_id"))

        row = session["current_element"]["Operations"][session["screens_table_id"]]
        if not 'uid' in row:
           row['uid'] = str(uuid.uuid4().hex)

        hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"screen_form","key":row['uid'],"reopen":True,"no_close":True},ensure_ascii=False))  
        current_screen_name = row.get("Name")
        hashMap.put("screen_name",current_screen_name)
        hashMap.put("SetTitle",current_screen_name)
        hashMap.put("Timer",row.get("Timer"))
        hashMap.put("hideToolBarScreen",row.get("hideToolBarScreen"))
        hashMap.put("noScroll",row.get("noScroll"))
        hashMap.put("handleKeyUp",row.get("handleKeyUp"))
        hashMap.put("noConfirmation",row.get("noConfirmation"))
        hashMap.put("hideBottomBarScreen",row.get("hideBottomBarScreen"))
        hashMap.put("layout_file",row.get("layout_file"))
        hashMap.put("screen_uid",row.get("uid"))

        #блокировка
        #hashMap.put("BlockTabs","")

        session["current_element"] = row  
        session["current_parent"] = (row,session["current_parent"]) 
        session["current_parent_dict"][row['uid']] = session["current_parent"]      
    elif hashMap.get("listener")=="btn_delete_screen":
        
        sel_line = 'selected_line_id'
        if hashMap.containsKey(sel_line):
                session["current_element"]['Operations'].pop(int(hashMap.get(sel_line)))
                hashMap.put("RefreshScreen","")
                hashMap.remove(sel_line) 
                save_configuration(session["configuration"],hashMap)   
    
    elif hashMap.get("listener")=="btn_up":
        if hashMap.containsKey("selected_line_id"):
            session["screens_table_id"] = int(hashMap.get("selected_line_id")) 
            if session["processes_table_id"]>0: 
                session["current_element"]['Operations'].insert(session["screens_table_id"]-1,session["current_element"]['Operations'].pop(session["screens_table_id"]))  
                save_configuration(session["configuration"],hashMap)    
                hashMap.put("RefreshScreen","") 

    elif hashMap.get("listener")=="btn_down":
        if hashMap.containsKey("selected_line_id"):
            session["screens_table_id"] = int(hashMap.get("selected_line_id")) 
            if session["screens_table_id"]<len(session["processes_table"]): 
                session["current_element"]['Operations'].insert(session["screens_table_id"]+1,session["current_element"]['Operations'].pop(session["screens_table_id"]))
            
            save_configuration(session["configuration"],hashMap) 
            hashMap.put("RefreshScreen","") 
    elif hashMap.get("listener")=="btn_paste":
        hashMap.put("ReadClipboard","")
    elif hashMap.get("listener")=="clipboard_result":    
        try:
            jelement = json.loads(hashMap.get("clipboard_result"))
            if "type" in jelement:
                session["current_element"]['Operations'].append(jelement)
                hashMap.put("RefreshScreen","")

        except:
            hashMap.put("toast","Ошибка буфера")    
        

    return hashMap

def get_recursively(search_dict, field):

    fields_found = [""]

    for key, value in search_dict.items():

        if key == field:
            if value!="" and value!=None:
                if field=="type":
                    fields_found.append(value)
                else:    
                    if search_dict.get("type")!="CardsLayout" and search_dict.get("type")!="TableLayout":
                        fields_found.append(value)

        elif isinstance(value, dict):
            results = get_recursively(value, field)
            for result in results:
                fields_found.append(result)

        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    more_results = get_recursively(item, field)
                    for another_result in more_results:
                        fields_found.append(another_result)

    return fields_found

def get_listener_html(val):
    listeners = get_recursively(session["current_element"],"Variable")
    listeners2 = get_recursively(session["current_element"],"type")
    for l in listeners2:
        if l=="CardsLayout" or l=="TableLayout":
            if not "CardsClick" in listeners:
                listeners.append("CardsClick")
                listeners.append("LayoutAction")
                 
        if l=="TableLayout":
            if not "TableClick" in listeners:
                listeners.append("TableClick")
           

    listener_html=   '<div class="container-horizontal"><p  style="text-align: left;;width:100%;margin: 3px">listener</p>   <input list="listeners" style="text-align: left;;width:100%;margin: 3px" name="listener" id="listener" value="'+val+'">  <datalist id="listeners"> '
    for l in listeners:
        if len(l)>0:
            listener_html+='<option value="'+l+'">'
    listener_html+=' </datalist> </div>'
    return listener_html

def screen_input(hashMap,_files=None,_data=None):

    session["layouts_edit"]=False

    closeuid = None

    if session["current_element"]==None:
        closeuid = hashMap.get("screen_uid")
    else:    
        closeuid = session["current_element"]['uid']

    if hashMap.get("listener")=="btn_save" or hashMap.get("listener")=="btn_add_element" or hashMap.get("listener") == "btn_add_handler":

        

        session["current_parent"] =session["current_parent"][1]
        session["current_element"] = session["current_parent"][0]

        if session["screens_table_id"]==-1:
            session["current_element"]['Operations'].append({
                                                    "type": "Operation",
                                                    "Name": hashMap.get("screen_name"),
                                                    "uid": closeuid,

                                                    "Timer": hashMap.get("Timer"),
                                                    "hideToolBarScreen": hashMap.get("hideToolBarScreen"),
                                                    "layout_file": hashMap.get("layout_file"),
                                                    "noScroll": hashMap.get("noScroll"),
                                                    "handleKeyUp": hashMap.get("handleKeyUp"),
                                                    "noConfirmation": hashMap.get("noConfirmation"),
                                                    "hideBottomBarScreen": hashMap.get("hideBottomBarScreen"),
                                                    
                                                    "Elements":[]
                                                
                                                }) 
            
            session["screens_table_id"]=len(session["current_element"]['Operations'])-1
            
            
        else:   
            session["current_element"]['Operations'][session["screens_table_id"]]["Name"] = hashMap.get("screen_name")
            session["current_element"]['Operations'][session["screens_table_id"]]["uid"] = closeuid

            session["current_element"]['Operations'][session["screens_table_id"]]["Timer"] = hashMap.get("Timer")
            session["current_element"]['Operations'][session["screens_table_id"]]["hideToolBarScreen"] = hashMap.get("hideToolBarScreen")
            session["current_element"]['Operations'][session["screens_table_id"]]["layout_file"] = hashMap.get("layout_file")
            session["current_element"]['Operations'][session["screens_table_id"]]["noScroll"] = hashMap.get("noScroll")
            session["current_element"]['Operations'][session["screens_table_id"]]["handleKeyUp"] = hashMap.get("handleKeyUp")
            session["current_element"]['Operations'][session["screens_table_id"]]["noConfirmation"] = hashMap.get("noConfirmation")
            session["current_element"]['Operations'][session["screens_table_id"]]["hideBottomBarScreen"] = hashMap.get("hideBottomBarScreen")
            
        
        session["current_parent"] = (session["current_element"]['Operations'][session["screens_table_id"]],session["current_parent"])
        session["current_parent_dict"][closeuid] = session["current_parent"]

        
        session["current_element"] = session["current_parent"][0]
        
    
        

    if hashMap.get("listener")=="btn_save" or hashMap.get("listener")=="btn_close":
 
        hashMap.put("CloseTab",closeuid)
        hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"process_form", "key":session["current_parent"][1][0]['uid'], "reopen":True},ensure_ascii=False))

        session["current_parent"] = session["current_parent"][1]
        process_table_id = session["processes_table"].index(session["current_parent"][0])
        session["current_element"] = session["current_parent"][0]

        save_configuration(session["configuration"],hashMap)

        #блокировка
        hashMap.put("UnblockTabs","")
 
    elif hashMap.get("listener")=="btn_add_element":

        

        uid = str(uuid.uuid4().hex)
        hashMap.put("element_uid",uid)

        if session["opened_element_uid"] != None:
                hashMap.put("toast","Может быть открыт только 1 элемент")
                return hashMap
            
        session["opened_element_uid"] = uid

        if session["layouts_edit"]:
            hashMap.put("OpenScreen",json.dumps({"process":"Контейнеры","screen":"element_form","key":uid,"reopen":True,"no_close":True},ensure_ascii=False))  
        else:    
            hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"element_form","key":uid,"reopen":True,"no_close":True},ensure_ascii=False))  
      

        hashMap.put("Show_layout_elements_table","-1")
        hashMap.put("Show_btns_table_elements","-1")
        hashMap.put("Show_layout_properties","-1")
        hashMap.put("Show_common_properties","-1")
        hashMap.put("Show_element_properties","-1")

        hashMap.put("Show_RecognitionTemplate","-1")
        hashMap.put("Show_RecognitionTemplate_div","-1")
        hashMap.put("Show_RecognitionTemplate_p","-1")

        hashMap.put("SetTitle","Новый элемент экрана - *")
        
                
        session["elements_table_id"] = -1
        session["current_element"] = None  

        session["current_parent"] = (session["current_element"],session["current_parent"])
        session["current_parent_dict"][uid] = session["current_parent"] 

    elif hashMap.get("listener")=="btn_edit_element" or (hashMap.get("listener") == "TableDoubleClick" and hashMap.get("table_id")=='screen_elements_table'):
        
        if hashMap.containsKey("selected_line_id"):
            session["elements_table_id"] = int(hashMap.get("selected_line_id"))
            row = session["current_element"]["Elements"][session["elements_table_id"]]
            
            if not 'uid' in row:
                row['uid'] = str(uuid.uuid4().hex)
            
            if session["opened_element_uid"] != None:
                hashMap.put("toast","Может быть открыт только 1 элемент")
                return hashMap
            
            session["opened_element_uid"] = row['uid']

            if session["layouts_edit"]:
                hashMap.put("OpenScreen",json.dumps({"process":"Контейнеры","screen":"element_form","key":row['uid'],"reopen":True,"no_close":True},ensure_ascii=False))  
            else:    
                hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"element_form","key":row['uid'],"reopen":True,"no_close":True},ensure_ascii=False))  
            #current_screen_name = row.get("Name")
            #hashMap.put("screen_name",current_screen_name)
            hashMap.put("SetTitle",row.get("type"))

            hashMap.put("element_uid",row.get("uid"))

            #parent_elelments_element = current_element

            session["current_parent"] = (row,session["current_parent"])
            session["current_parent_dict"][row['uid']] = session["current_parent"]

            session["current_element"] = row     

            hashMap.remove("selected_line_id")  

    elif hashMap.get("listener")=="btn_delete_element":
        sel_line = 'selected_line_id'
        if hashMap.containsKey(sel_line):
                session["current_element"]['Elements'].pop(int(hashMap.get(sel_line)))
                #hashMap.put("screens_table",json.dumps(jtable,ensure_ascii=False)) 
                #hashMap.put("SetValuesTable",json.dumps([{"screens_table":jtable}]) )       
                hashMap.put("RefreshScreen","")
                hashMap.remove(sel_line)    
    
    elif hashMap.get("listener")=="btn_copy":
        hashMap.put("WriteClipboard",json.dumps(session["current_element"],ensure_ascii=False))

    elif hashMap.get("listener") == "btn_add_handler":

      
        hashMap.put("listener",get_listener_html(""))
        
        hashMap.put("ShowDialogLayout",json.dumps(handler_layout_lang_screen,ensure_ascii=False))
        hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Обработчик"},ensure_ascii=False))
        hashMap.put("ShowDialog","")
        hashMap.put("ShowDialogActive","type;type_postExecute")
        

        
        hashMap.put("event","")
        hashMap.put("action","")
        hashMap.put("type","")

        

        hashMap.put("method","")
        #hashMap.put("listener","")

        hashMap.put("action_postExecute","")
        hashMap.put("type_postExecute","")
        hashMap.put("method_postExecute","")

        postExecute = ""
        session["edit_handler_mode"] = -1
    elif hashMap.get("listener") == "btn_edit_handler" or (hashMap.get("listener") == "TableDoubleClick"  and hashMap.get("table_id")=='handlers_table') or hashMap.get("listener") == "type" or hashMap.get("listener") == "type_postExecute":
        if hashMap.containsKey("selected_line_id") and hashMap.get("table_id")=='handlers_table':
            dialog_layout_str = json.dumps(handler_layout_lang_screen,ensure_ascii=False)
            session["edit_handler_mode"] = int(hashMap.get("selected_line_id"))
            
            handler_str = session["current_element"]['Handlers'][session["edit_handler_mode"]]

            if handler_str.get("type","")=="js":

                dialog_layout_str = dialog_layout_str.replace("#type_method","html")
                
                try:
                    m = base64.b64decode(handler_str.get("method","")).decode("utf-8")
                except:
                    m=handler_str.get("method","") 

                method =  '<code-input required id="method" class="line-numbers" style="resize: both; overflow: hidden; width: 100%;" lang="JavaScript" placeholder="Write some JavaScript!">'+m+'</code-input>'
                hashMap.put("method",method)
            elif handler_str.get("type","")=="pythonscript":
                dialog_layout_str = dialog_layout_str.replace("#type_method","html")
             
                try:
                    m = base64.b64decode(handler_str.get("method","")).decode("utf-8")
                except:
                    m=handler_str.get("method","") 

                method =  '<code-input required id="method" class="line-numbers" style="resize: both; overflow: hidden; width: 100%;" lang="Python" placeholder="Write some JavaScript!">'+m+'</code-input>'
                hashMap.put("method",method)    
            else:    
                dialog_layout_str = dialog_layout_str.replace("#type_method","MultilineText")
                
                hashMap.put("method",handler_str.get("method",""))
            
            hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Обработчик"},ensure_ascii=False))
            hashMap.put("ShowDialog","")
            hashMap.put("ShowDialogActive","type;type_postExecute")

            hashMap.put("alias",handler_str.get("alias",""))
            hashMap.put("event",handler_str.get("event",""))
            hashMap.put("action",handler_str.get("action",""))
            hashMap.put("type",handler_str.get("type",""))
             
            hashMap.put("listener",get_listener_html(handler_str.get("listener","")))

            hashMap.put("action_postExecute","")
            hashMap.put("type_postExecute","")
            hashMap.put("method_postExecute","")

            postExecute = ""
            pe = handler_str.get("postExecute")
            if pe!=None and pe!="":
                jpe = json.loads(pe)
                if isinstance(jpe, list) :
                    if len(jpe)>0:
                        postExecute =  pe    
                        
                        hashMap.put("action_postExecute",jpe[0].get("action",""))
                        hashMap.put("type_postExecute",jpe[0].get("type",""))
                        if jpe[0].get("type","")=="js":
                            dialog_layout_str = dialog_layout_str.replace("#_PE","html")
                            try:    
                                m = base64.b64decode(jpe[0].get("method","")).decode("utf-8")
                            except:
                                m=handler_str.get("method_postExecute","")    

                            method =  '<code-input required id="method_postExecute" class="line-numbers" style="resize: both; overflow: hidden; width: 100%;" lang="JavaScript" placeholder="Write some JavaScript!">'+m+'</code-input>'
                            hashMap.put("method_postExecute",method)
                        elif jpe[0].get("type","")=="pythonscript":
                            dialog_layout_str = dialog_layout_str.replace("#_PE","html")
                            try:    
                                m = base64.b64decode(jpe[0].get("method","")).decode("utf-8")
                            except:
                                m=handler_str.get("method_postExecute","")    

                            method =  '<code-input required id="method_postExecute" class="line-numbers" style="resize: both; overflow: hidden; width: 100%;" lang="Python" placeholder="Write some Python!">'+m+'</code-input>'
                            hashMap.put("method_postExecute",method)    
                        else:    
                            dialog_layout_str = dialog_layout_str.replace("#_PE","MultilineText")

                            hashMap.put("method_postExecute",jpe[0].get("method","")) 
                        #hashMap.put("method_postExecute",jpe[0].get("method",""))
            
            hashMap.put("ShowDialogLayout",dialog_layout_str)
            hashMap.remove("selected_line_id") 
        
        elif hashMap.containsKey("dialog_values"):
            dialog_layout_str = json.dumps(handler_layout_lang_screen,ensure_ascii=False)

            handler_str = list_to_dict(json.loads(hashMap.get("dialog_values"))) 
            if handler_str.get("type","")=="js":
                dialog_layout_str = dialog_layout_str.replace("#type_method","html")

                try:
                    m = base64.b64decode(handler_str.get("method","")).decode("utf-8")
                except:
                    m=handler_str.get("method","")    
                method =  '<code-input required id="method" class="line-numbers" style="resize: both; overflow: hidden; width: 100%;" lang="JavaScript" placeholder="Write some JavaScript!">'+m+'</code-input>'
                hashMap.put("method",method)
                
            elif handler_str.get("type","")=="pythonscript":
                dialog_layout_str = dialog_layout_str.replace("#type_method","html")

                try:
                    m = base64.b64decode(handler_str.get("method","")).decode("utf-8")
                except:
                    m=handler_str.get("method","")    

                method =  '<code-input required id="method" class="line-numbers" style="resize: both; overflow: hidden; width: 100%;" lang="Python" placeholder="Write some Python!">'+m+'</code-input>'
                hashMap.put("method",method)
                   
            else:    
                dialog_layout_str = dialog_layout_str.replace("#type_method","MultilineText")

                hashMap.put("method",handler_str.get("method",""))
            
            hashMap.put("listener",get_listener_html(handler_str.get("listener","")))
            hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Обработчик"},ensure_ascii=False))
            
            
            #hashMap.put("listener",handler_str.get("listener",""))

            if handler_str.get("type_postExecute","")=="js":
                dialog_layout_str = dialog_layout_str.replace("#_PE","html")
                try:    
                    m = base64.b64decode(handler_str.get("method_postExecute","")).decode("utf-8")
                except:
                    m=handler_str.get("method_postExecute","")    

                method =  '<code-input required id="method_postExecute" class="line-numbers" style="resize: both; overflow: hidden; width: 100%;" lang="JavaScript" placeholder="Write some JavaScript!">'+m+'</code-input>'
                hashMap.put("method_postExecute",method)
            elif handler_str.get("type_postExecute","")=="pythonscript":
                dialog_layout_str = dialog_layout_str.replace("#_PE","html")
                try:    
                    m = base64.b64decode(handler_str.get("method_postExecute","")).decode("utf-8")
                except:
                    m=handler_str.get("method_postExecute","")    

                method =  '<code-input required id="method_postExecute" class="line-numbers" style="resize: both; overflow: hidden; width: 100%;" lang="Python" placeholder="Write some Python!">'+m+'</code-input>'
                hashMap.put("method_postExecute",method)    
            else:    
                dialog_layout_str = dialog_layout_str.replace("#_PE","MultilineText")

                hashMap.put("method_postExecute",handler_str.get("method_postExecute",""))    


            hashMap.put("action_postExecute",handler_str.get("action_postExecute",""))
            hashMap.put("type_postExecute",handler_str.get("type_postExecute",""))
            #hashMap.put("method_postExecute",handler_str.get("method_postExecute",""))

            hashMap.put("ShowDialogLayout",dialog_layout_str)
            hashMap.put("ShowDialog","")
 

    elif hashMap.get("listener") == "btn_delete_handler":
        if hashMap.containsKey("selected_line_id"):
            pos = int(hashMap.get("selected_line_id"))   
            session["current_element"]['Handlers'].pop(pos)
            hashMap.put("RefreshScreen","")
            hashMap.remove("selected_line_id")      

    elif hashMap.get("listener") == "onResultPositive": 
        dialog_values = list_to_dict(json.loads(hashMap.get("dialog_values")))
        
        if dialog_values.get("type")=='js' or dialog_values.get("type")=='pythonscript':
            method = dialog_values.get('method')  
            method = base64.b64encode(method.encode('utf-8')).decode('utf-8')     
        else:    
            method = dialog_values.get('method')  

        if not "Handlers" in session["current_element"]:
            session["current_element"]['Handlers'] = []
        
        postExecute = ""
        if len(str(dialog_values.get("action_postExecute")))>0 and len(str(dialog_values.get("type_postExecute")))>0:
            if dialog_values.get("type_postExecute")=='js' or dialog_values.get("type_postExecute")=='pythonscript':
                methodPE = dialog_values.get('method_postExecute')  
                methodPE = base64.b64encode(methodPE.encode('utf-8')).decode('utf-8')
            else:    
                methodPE = dialog_values.get('method_postExecute')  

            

            postExecute =json.dumps( [{"action":dialog_values.get("action_postExecute",""),"type":dialog_values.get("type_postExecute",""),"method":methodPE}], ensure_ascii=False)

        if session["edit_handler_mode"] == -1 :
            session["current_element"]['Handlers'].append({"event":dialog_values.get("event",""),"action":dialog_values.get("action",""),"listener":dialog_values.get("listener",""),"type":dialog_values.get("type",""),"method":method,"postExecute":postExecute,"alias":dialog_values.get("alias","")}) 
        else:
            session["current_element"]['Handlers'][session["edit_handler_mode"]] = {"event":dialog_values.get("event",""),"action":dialog_values.get("action",""),"listener":dialog_values.get("listener",""),"type":dialog_values.get("type",""),"method":method,"postExecute":postExecute,"alias":dialog_values.get("alias","")} 

        hashMap.put("RefreshScreen","")
        hashMap.put("callSelectTab","Обработчики")
        hashMap.put("SelectTab","Обработчики")

        save_configuration(session["configuration"],hashMap)

    return hashMap




def element_input(hashMap,_files=None,_data=None):
    
    if session["current_element"]==None:
        closeuid = hashMap.get("element_uid")
    else:    
        closeuid = session["current_element"]['uid']

    if hashMap.get("listener")=="btn_save" or hashMap.get("listener")=="btn_add_element" or  hashMap.get("listener")=="btn_edit_element":
        session["current_parent"] =session["current_parent"][1]
        if session["current_parent"]!=None:
            session["current_element"] = session["current_parent"][0]

            if session["current_element"].get("type") == "Operation":
                element_base = screen_elements
            else:
                element_base = layout_elements 
            row = session["current_element"]['Elements']     
        else:         
            element_base = layout_elements  
            if not "Layouts" in session["configuration"]["ClientConfiguration"]:
                session["configuration"]["ClientConfiguration"]["Layouts"]=[]
            #current_element = configuration["ClientConfiguration"]["Layouts"]
            row = session["configuration"]["ClientConfiguration"]['Layouts'] 
        

        if get_key(scale_elements,hashMap.get("width"))=="manual":
            if len(hashMap.get("width_value"))>0:
                width = int(hashMap.get("width_value"))
            else:    
                width = 0
        else:
            width  = get_key(scale_elements,hashMap.get("width"))

        if get_key(scale_elements,hashMap.get("height"))=="manual":
            if len(hashMap.get("height_value"))>0:
                height = int(hashMap.get("height_value"))
            else:    
                height = 0
        else:
            height  = get_key(scale_elements,hashMap.get("height"))    


        if session["elements_table_id"]==-1:
                  
            
            d = {
                        "type":get_key(element_base,hashMap.get("type")),
                        "orientation":get_key(orientation_elements,hashMap.get("orientation")),
                        "gravity_vertical":get_key(vertical_gravity_elements,hashMap.get("gravity_vertical")),
                        "height":height,
                        "width":width,
                        "drawable":get_key(element_base,hashMap.get("drawable")),
                        "gravity_horizontal":get_key(gravity_elements,hashMap.get("gravity_horizontal")),
                        
                        "Value":hashMap.get("Value"),
                        "Variable":hashMap.get("Variable"),
                        "BackgroundColor":hashMap.get("BackgroundColor"),
                        "StrokeWidth":hashMap.get("StrokeWidth"),
                        "Padding":hashMap.get("Padding"),
                        "Radius":hashMap.get("Radius"),
                        "weight":hashMap.get("weight"),
                        
                        "TextSize":hashMap.get("TextSize"),
                        "TextColor":hashMap.get("TextColor"),
                        "TextBold":hashMap.get("TextBold"),
                        "TextItalic":hashMap.get("TextItalic"),
                        "NumberPrecision":hashMap.get("NumberPrecision"),
                        "RecognitionTemplate":hashMap.get("RecognitionTemplate"),
                        "style_name":hashMap.get("style_name"),

                        "uid": closeuid
                    }
            
            if width == "manual":
                d["width_value"] = hashMap.get("width_value")
            if height == "manual":
                d["height_value"] = hashMap.get("height_value")    
                
            if get_key(scale_elements,hashMap.get("width"))=="manual":
                d["width_value"] = int(hashMap.get("width_value"))   
                d["width"]="manual"
            if get_key(scale_elements,hashMap.get("height"))=="manual":
                d["height_value"] = int(hashMap.get("height_value")) 
                d["height"]="manual"    


            if get_key(element_base,hashMap.get('type')) == 'LinearLayout' or get_key(element_base,hashMap.get('type')) == 'Tab' or get_key(element_base,hashMap.get('type')) == 'Tabs':
                d["Elements"] =[]

            row.append(d) 
            session["elements_table_id"] = len(row) - 1
             
        else:   
            row[session["elements_table_id"]]['type'] = get_key(element_base,hashMap.get("type"))

            row[session["elements_table_id"]]['orientation'] = get_key(orientation_elements,hashMap.get("orientation"))
            row[session["elements_table_id"]]['gravity_vertical'] = get_key(vertical_gravity_elements,hashMap.get("gravity_vertical"))
            row[session["elements_table_id"]]['drawable'] = hashMap.get("drawable")
            row[session["elements_table_id"]]['gravity_horizontal'] = get_key(gravity_elements,hashMap.get("gravity_horizontal"))
            row[session["elements_table_id"]]['height'] = height
            row[session["elements_table_id"]]['width'] = width
            row[session["elements_table_id"]]['Value'] = hashMap.get("Value")
            row[session["elements_table_id"]]['Variable'] = hashMap.get("Variable")
            row[session["elements_table_id"]]['BackgroundColor'] = hashMap.get("BackgroundColor")
            row[session["elements_table_id"]]['StrokeWidth'] = hashMap.get("StrokeWidth")
            row[session["elements_table_id"]]['Padding'] = hashMap.get("Padding")
            row[session["elements_table_id"]]['Radius'] = hashMap.get("Radius")
            row[session["elements_table_id"]]['height_value'] = hashMap.get("height_value")
            row[session["elements_table_id"]]['width_value'] = hashMap.get("width_value")
            row[session["elements_table_id"]]['weight'] = hashMap.get("weight")
            row[session["elements_table_id"]]['TextSize'] = hashMap.get("TextSize")
            row[session["elements_table_id"]]['TextColor'] = hashMap.get("TextColor")
            row[session["elements_table_id"]]['TextBold'] = hashMap.get("TextBold")
            row[session["elements_table_id"]]['TextItalic'] = hashMap.get("TextItalic")
            row[session["elements_table_id"]]['NumberPrecision'] = hashMap.get("NumberPrecision")
            row[session["elements_table_id"]]['RecognitionTemplate'] = hashMap.get("RecognitionTemplate")
            row[session["elements_table_id"]]['style_name'] = hashMap.get("style_name")


            row[session["elements_table_id"]]['uid'] = closeuid

            if get_key(scale_elements,hashMap.get("width")) == "manual":
                row[session["elements_table_id"]]["width_value"] = hashMap.get("width_value")
                row[session["elements_table_id"]]["width"] = "manual"
            else:
                if "width_value" in session["current_element"]:
                    del row[session["elements_table_id"]]["width_value"]    
            
            if get_key(scale_elements,hashMap.get("height")) == "manual":
                row[session["elements_table_id"]]["height_value"] = hashMap.get("height_value")  
                row[session["elements_table_id"]]["height"] = "manual"
            else:
                if "height_value" in session["current_element"]:
                    del row[session["elements_table_id"]]["height_value"]


        session["current_parent"] =(row[session["elements_table_id"]],session["current_parent"])

        session["current_element"] = session["current_parent"][0]
        session["current_parent_dict"][closeuid] = session["current_parent"]
        


    if hashMap.get("listener")=="btn_close":
        if session["current_parent"]!=None:
            session["current_parent"] =session["current_parent"][1]
            if session["current_parent"]!=None:
                session["current_element"] = session["current_parent"][0]
            
                session["current_parent_dict"][closeuid] = session["current_parent"]
    
    if hashMap.get("listener")=="btn_save" :

        
        hashMap.put("CloseTab",closeuid)
        hashMap.put("Show_RecognitionTemplate_div","-1")
        hashMap.put("Show_RecognitionTemplate","-1")
        hashMap.put("Show_RecognitionTemplate_p","-1")

        if session["current_parent"][1]==None:
            hashMap.put("layouts_table",json.dumps(make_onefield_table(session["configuration"]["ClientConfiguration"]['Layouts'],"Variable","Переменная"),ensure_ascii=False))
            hashMap.put("OpenScreen",json.dumps({"process":"Контейнеры","screen":"main_form", "key":"Контейнеры", "reopen":True},ensure_ascii=False))
        else:    
            if session["current_parent"][1][0].get("type") == "Operation":
                hashMap.put("screen_elements_table",json.dumps(make_screenelements_table(session["current_parent"][1][0]['Elements']),ensure_ascii=False))
                hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"screen_form", "key":session["current_parent"][1][0]['uid'], "reopen":True},ensure_ascii=False))
            else:    

                if session["current_element"].get("type") == 'LinearLayout' or session["current_element"].get("type") == 'Tab' or session["current_element"].get("type") == 'Tabs' :
                        hashMap.put("Show_layout_elements_table","1")
                        hashMap.put("Show_btns_table_elements","1")
                        hashMap.put("Show_layout_properties","1")
                        hashMap.put("Show_common_properties","1")
                        
                        hashMap.put("Show_element_properties","-1")
                        
            
                else:    
                        hashMap.put("Show_layout_elements_table","-1")
                        hashMap.put("Show_btns_table_elements","-1")
                        hashMap.put("Show_layout_properties","-1")
                        hashMap.put("Show_common_properties","1")

                        hashMap.put("Show_element_properties","1") 

                        if session["current_element"].get("type") == 'Vision':
                            hashMap.put("Show_RecognitionTemplate_div","1")  
                            hashMap.put("Show_RecognitionTemplate_p","1") 
                            hashMap.put("Show_RecognitionTemplate","1")   
                            

                
                hashMap.put("layout_elements_table",json.dumps(make_layoutelements_table(session["current_parent"][1][0]['Elements']),ensure_ascii=False))
                hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"element_form", "key":session["current_parent"][1][0]['uid'], "reopen":True},ensure_ascii=False))

        session["current_parent"] = session["current_parent"][1]
          
        
        if session["current_parent"]==None:
            pass

        else:    
            if session["current_parent"][0].get("type") == "Operation":
                session["screens_table_id"] = session["current_parent"][1][0]['Operations'].index(session["current_parent"][0])
            else:    
                if session["current_parent"][1]==None:
                    session["elements_table_id"] = session["configuration"]['ClientConfiguration']['Layouts'].index(session["current_parent"][0]) 
                else:    
                    session["elements_table_id"] = session["current_parent"][1][0]['Elements'].index(session["current_parent"][0]) 

            session["current_element"] = session["current_parent"][0] 

        save_configuration(session["configuration"],hashMap) 

        session["opened_element_uid"] = None    

    if  hashMap.get("listener")=="btn_close":

        session["opened_element_uid"] = None 

        hashMap.put("CloseTab",closeuid)

        hashMap.put("Show_RecognitionTemplate_div","-1")
        hashMap.put("Show_RecognitionTemplate","-1")
        hashMap.put("Show_RecognitionTemplate_p","-1")

        if session["current_parent"]==None:
            hashMap.put("layouts_table",json.dumps(make_onefield_table(session["configuration"]["ClientConfiguration"]['Layouts'],"Variable","Переменная"),ensure_ascii=False))
            hashMap.put("OpenScreen",json.dumps({"process":"Контейнеры","screen":"main_form", "key":"Контейнеры", "reopen":True},ensure_ascii=False))
        else:  
            if session["current_element"].get("type") == "Operation":
                hashMap.put("screen_elements_table",json.dumps(make_screenelements_table(session["current_element"]['Elements']),ensure_ascii=False))
                hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"screen_form", "key":session["current_parent"][0]['uid'], "reopen":True},ensure_ascii=False))
            else:    

                if session["current_element"].get("type") == 'LinearLayout' or session["current_element"].get("type") == 'Tab' or session["current_element"].get("type") == 'Tabs':
                        hashMap.put("Show_layout_elements_table","1")
                        hashMap.put("Show_btns_table_elements","1")
                        hashMap.put("Show_layout_properties","1")
                        hashMap.put("Show_common_properties","1")
                        
                        hashMap.put("Show_element_properties","-1")
                        
            
                else:    
                        hashMap.put("Show_layout_elements_table","-1")
                        hashMap.put("Show_btns_table_elements","-1")
                        hashMap.put("Show_layout_properties","-1")
                        hashMap.put("Show_common_properties","1")

                        hashMap.put("Show_element_properties","1")    

                        if session["current_element"].get("type") == 'Vision':
                            hashMap.put("Show_RecognitionTemplate_div","1")  
                            hashMap.put("Show_RecognitionTemplate_p","1")
                            hashMap.put("Show_RecognitionTemplate","1") 

                hashMap.put("layout_elements_table",json.dumps(make_layoutelements_table(session["current_parent"][0]['Elements']),ensure_ascii=False))
                hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"element_form", "key":session["current_parent"][0]['uid'], "reopen":True},ensure_ascii=False))

            
            
            if session["current_parent"][0].get("type") == "Operation":
                session["screens_table_id"] = session["current_parent"][1][0]['Operations'].index(session["current_parent"][0])
            else:    
                session["elements_table_id"] = session["current_parent"][1][0]['Elements'].index(session["current_parent"][0]) 

        
             

    elif hashMap.get("listener")=="btn_add_element":

        uid = str(uuid.uuid4().hex)
        hashMap.put("element_uid",uid)

        hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"element_form","key":uid,"reopen":True,"no_close":True},ensure_ascii=False))  
        
        hashMap.put("Show_layout_elements_table","-1")
        hashMap.put("Show_btns_table_elements","-1")
        hashMap.put("Show_layout_properties","-1")
        hashMap.put("Show_common_properties","-1")
        hashMap.put("Show_element_properties","-1")
        hashMap.put("Show_RecognitionTemplate_div","-1")
        hashMap.put("Show_RecognitionTemplate_p","-1")
        hashMap.put("Show_RecognitionTemplate","-1")

        hashMap.put("SetTitle","Новый элемент контейнера- *")

                    
        

                
        session["elements_table_id"] = -1
        session["current_element"] = None   

        session["current_parent"] = (session["current_element"],session["current_parent"]) 
        
        session["current_parent_dict"][uid] = session["current_parent"]

    elif hashMap.get("listener")=="btn_edit_element" or (hashMap.get("listener") == "TableDoubleClick"):

        session["elements_table_id"] = int(hashMap.get("selected_line_id"))
        row = session["current_element"]["Elements"][session["elements_table_id"]]
        
        if not 'uid' in row:
           row['uid'] = str(uuid.uuid4().hex)
        
        hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"element_form","key":row['uid'],"reopen":True,"no_close":True},ensure_ascii=False))  
        hashMap.put("SetTitle",row.get("type"))

        hashMap.put("element_uid",row.get("uid"))
        
        #parent_elelments_element = current_element
        session["current_parent"] = (row,session["current_parent"])
        session["current_element"] = row 

        session["current_parent_dict"][row['uid']] = session["current_parent"]

    elif hashMap.get("listener")=="btn_delete_element":
        sel_line = 'selected_line_id'
        if hashMap.containsKey(sel_line):
                session["current_element"]['Elements'].pop(int(hashMap.get(sel_line)))
                #hashMap.put("screens_table",json.dumps(jtable,ensure_ascii=False)) 
                #hashMap.put("SetValuesTable",json.dumps([{"screens_table":jtable}]) )       
                hashMap.put("RefreshScreen","")
                hashMap.remove(sel_line)  
    elif hashMap.get("listener")=="btn_up":
        if hashMap.containsKey("selected_line_id"):
            session["elements_table_id"] = int(hashMap.get("selected_line_id")) 
            if session["elements_table_id"]>0: 
                session["current_element"]['Elements'].insert(session["elements_table_id"]-1,session["current_element"]['Elements'].pop(session["elements_table_id"]))  
                save_configuration(session["configuration"],hashMap)    
                hashMap.put("RefreshScreen","") 

    elif hashMap.get("listener")=="btn_down":
        if hashMap.containsKey("selected_line_id"):
            session["elements_table_id"] = int(hashMap.get("selected_line_id")) 
            if session["elements_table_id"]<len(session["current_element"]['Elements']): 
                session["current_element"]['Elements'].insert(session["elements_table_id"]+1,session["current_element"]['Elements'].pop(session["elements_table_id"]))
            
            save_configuration(session["configuration"],hashMap) 

            hashMap.put("RefreshScreen","") 
    elif hashMap.get("listener")=="btn_copy":
        hashMap.put("WriteClipboard",json.dumps(session["current_element"],ensure_ascii=False))
    elif hashMap.get("listener")=="btn_paste":
        hashMap.put("ReadClipboard","")
    elif hashMap.get("listener")=="clipboard_result":    
        try:
            jelement = json.loads(hashMap.get("clipboard_result"))
            if "type" in jelement:
                session["current_element"]['Elements'].append(jelement)
                hashMap.put("RefreshScreen","")

        except:
            hashMap.put("toast","Ошибка буфера")    
    if hashMap.get("listener")=="type":

        if session["current_parent"][1][0].get("type") == "Operation":
                element_base = screen_elements
        else:
                element_base = layout_elements    

        hashMap.put("SetShow_RecognitionTemplate_div","-1") 
        hashMap.put("SetShow_RecognitionTemplate_p","-1") 
        hashMap.put("SetShow_RecognitionTemplate","-1")  
        if get_key(element_base,hashMap.get('type')) == 'LinearLayout' or get_key(element_base,hashMap.get('type')) == 'Tab' or get_key(element_base,hashMap.get('type')) == 'Tabs':
            hashMap.put("SetShow_layout_elements_table","1")
            hashMap.put("SetShow_btns_table_elements","1")
            hashMap.put("SetShow_layout_properties","1")
            hashMap.put("SetShow_common_properties","1")
            hashMap.put("SetShow_element_properties","-1")
     
        elif get_key(element_base,hashMap.get('type')) == 'Vision':
            
            hashMap.put("SetShow_RecognitionTemplate_div","1")  
            hashMap.put("SetShow_RecognitionTemplate_p","1")
            hashMap.put("SetShow_RecognitionTemplate","1") 


            hashMap.put("SetShow_layout_elements_table","-1")
            hashMap.put("SetShow_btns_table_elements","-1")
            hashMap.put("SetShow_layout_properties","-1")
            hashMap.put("SetShow_common_properties","1")
            
            if session["current_parent"][1][0].get("type") == "Operation":
                hashMap.put("SetShow_element_properties","-1")  
                hashMap.put("SetShow_common_properties","-1")
            else:
                hashMap.put("SetShow_element_properties","1")  
                hashMap.put("SetShow_common_properties","1")    
   

        elif get_key(element_base,hashMap.get('type')) == '':
            hashMap.put("SetShow_layout_elements_table","-1")
            hashMap.put("SetShow_btns_table_elements","-1")
            hashMap.put("SetShow_layout_properties","-1")
            hashMap.put("SetShow_common_properties","-1")
            hashMap.put("SetShow_element_properties","-1")  
            
        else:    
            hashMap.put("SetShow_layout_elements_table","-1")
            hashMap.put("SetShow_btns_table_elements","-1")
            hashMap.put("SetShow_layout_properties","-1")
            hashMap.put("SetShow_common_properties","1")
            
            if session["current_parent"][1][0].get("type") == "Operation":
                hashMap.put("SetShow_element_properties","-1")  
                hashMap.put("SetShow_common_properties","-1")
            else:
                hashMap.put("SetShow_element_properties","1")      
                hashMap.put("SetShow_common_properties","1")

                if get_key(element_base,hashMap.get('type')) == 'ModernEditText':
                    if hashMap.get("Value")=="" or hashMap.get("Value")==None:
                        template = json.dumps({"hint":"Имя поля", "default_text":"default_value"},ensure_ascii=False)
                        hashMap.put("SetValuesEdit",json.dumps([{"Value":template}])) 
                        hashMap.put("Value",template) 
                        #hashMap.put("toast",template)

  

    return hashMap


def process_open(hashMap,_files=None,_data=None):

    if not session["current_element"] == None:
        hashMap.put("screens_table",json.dumps(make_onefield_table(session["current_element"]["Operations"],"Name","Экран"),ensure_ascii=False))
    else:
        hashMap.put("screens_table",json.dumps(make_onefield_table([],"Name","Экран"),ensure_ascii=False))
   
    return hashMap

def screen_open(hashMap,_files=None,_data=None):
    hashMap.put("common_events",";".join(events_screen))
    hashMap.put("handler_types",";".join(handler_types))
    hashMap.put("action_types",";".join(action_types))

    recognition_templates = []
    recognition_templates.append("")
    if "RecognitionTemplates" in session["configuration"]['ClientConfiguration']:
        for t in session["configuration"]['ClientConfiguration']["RecognitionTemplates"]:
            recognition_templates.append(t.get('name'))
    hashMap.put("recognition_templates",";".join(recognition_templates)) 

    xml_files = []
    xml_files.append("")
    if "Mediafile" in session["configuration"]['ClientConfiguration']:
        for t in session["configuration"]['ClientConfiguration']["Mediafile"]:
            if t.get("MediafileExt") == "xml":
                xml_files.append(t.get('MediafileKey'))
    hashMap.put("xml_files",";".join(xml_files)) 

    style_templates = []
    style_templates.append("")
    if "StyleTemplates" in session["configuration"]['ClientConfiguration']:
        for t in session["configuration"]['ClientConfiguration']["StyleTemplates"]:
            style_templates.append(t.get('name'))
    hashMap.put("style_templates",";".join(style_templates))        

    if not session["current_element"] == None:
        if "Elements" in session["current_element"]:
            hashMap.put("screen_elements_table",json.dumps(make_screenelements_table(session["current_element"]["Elements"]),ensure_ascii=False))
        else:    
            hashMap.put("screen_elements_table",json.dumps(make_screenelements_table([]),ensure_ascii=False))
    
        if  "Handlers" in session["current_element"]:
            hashMap.put("handlers_table",json.dumps(make_handlers_table(session["current_element"]["Handlers"],True),ensure_ascii=False))
        else:
            hashMap.put("handlers_table",json.dumps(make_handlers_table([],True),ensure_ascii=False))    

    else:
        hashMap.put("screen_elements_table",json.dumps(make_screenelements_table([]),ensure_ascii=False))
        hashMap.put("handlers_table",json.dumps(make_handlers_table([],True),ensure_ascii=False))
   
    return hashMap


def post_open_screen(hashMap,_files=None,_data=None):
    
    if hashMap.containsKey("callSelectTab"):
        hashMap.put("SelectTab",hashMap.get("callSelectTab"))
        hashMap.remove("callSelectTab")

    return hashMap

def element_open(hashMap,_files=None,_data=None):

    hashMap.put("orientation_elements",captions_orientation_elements)
    hashMap.put("height_elements",captions_scale_elements)
    hashMap.put("width_elements",captions_scale_elements)
    hashMap.put("drawable_elements",";".join(icon_elements))
    hashMap.put("gravity_horizontal_elements",captions_gravity_elements)
    hashMap.put("vertical_gravity_elements",captions_vertical_gravity_elements)

    
    if session["current_parent"] != None:
        element_base = layout_elements  
        if session["current_parent"][1]!=None:
            par = session["current_parent"][1][0]
            if par.get("type") == "Operation":
                hashMap.put("screen_elements",captions_screen_elements)
                element_base = screen_elements
            else:
                hashMap.put("screen_elements",captions_layout_elements)
                
                element_base = layout_elements  

        if session["current_element"]!=None:
            if "Elements" in session["current_element"]:
                hashMap.put("layout_elements_table",json.dumps(make_layoutelements_table(session["current_element"]["Elements"]),ensure_ascii=False))    
   
    if session["current_parent"] == (None,None):
        hashMap.put("type", get_synonym(element_base,"LinearLayout"))
        hashMap.put("screen_elements",captions_layout_elements)

    if not session["current_element"] == None:
        hashMap.put("type", get_synonym(element_base,session["current_element"].get("type")))
        
        hashMap.put("orientation", get_synonym(orientation_elements,session["current_element"].get("orientation")))
        hashMap.put("gravity_vertical", get_synonym(vertical_gravity_elements,session["current_element"].get("gravity_vertical")))
        hashMap.put("gravity_horizontal", get_synonym(gravity_elements,session["current_element"].get("gravity_horizontal")))
        
        if "height_element" in session["current_element"]:
            hashMap.put("height", get_synonym(scale_elements,session["current_element"].get("manual")))
        else:    
            hashMap.put("height", get_synonym(scale_elements,session["current_element"].get("height")))

        if "width_element" in session["current_element"]:
            hashMap.put("width", get_synonym(scale_elements,session["current_element"].get("manual")))
        else:    
            hashMap.put("width", get_synonym(scale_elements,session["current_element"].get("width")))    
        
        

        hashMap.put("drawable", session["current_element"].get("drawable"))
        hashMap.put("Value", session["current_element"].get("Value",""))
        hashMap.put("Variable", session["current_element"].get("Variable",""))
        hashMap.put("BackgroundColor", session["current_element"].get("BackgroundColor",""))
        hashMap.put("StrokeWidth", session["current_element"].get("StrokeWidth",""))
        hashMap.put("Padding", session["current_element"].get("Padding",""))
        hashMap.put("Radius", session["current_element"].get("Radius",""))
        hashMap.put("height_value", session["current_element"].get("height_value",""))
        hashMap.put("width_value", session["current_element"].get("width_value",""))
        hashMap.put("weight", session["current_element"].get("weight",""))
        hashMap.put("BackgroundColor", session["current_element"].get("BackgroundColor",""))
        hashMap.put("TextSize", session["current_element"].get("TextSize",""))
        hashMap.put("TextColor", session["current_element"].get("TextColor",""))
        hashMap.put("TextBold", session["current_element"].get("TextBold",""))
        hashMap.put("TextItalic", session["current_element"].get("TextItalic",""))
        hashMap.put("NumberPrecision", session["current_element"].get("NumberPrecision",""))
        hashMap.put("RecognitionTemplate", session["current_element"].get("RecognitionTemplate",""))
        hashMap.put("style_name", session["current_element"].get("style_name",""))

        if type(session["current_element"].get("height"))==int or str(session["current_element"].get("height")).isnumeric():
            hashMap.put("height", get_synonym(scale_elements,"manual"))
            hashMap.put("height_value", str(session["current_element"].get("height")))
        
        if type(session["current_element"].get("width"))==int or str(session["current_element"].get("width")).isnumeric():
            hashMap.put("width", get_synonym(scale_elements,"manual"))
            hashMap.put("width_value", str(session["current_element"].get("width")))   

        if "Elements" in session["current_element"]:
            hashMap.put("layout_elements_table",json.dumps(make_layoutelements_table(session["current_element"]["Elements"]),ensure_ascii=False))
        else:    
            hashMap.put("layout_elements_table",json.dumps(make_layoutelements_table([]),ensure_ascii=False))
    else:
        hashMap.put("layout_elements_table",json.dumps(make_layoutelements_table([]),ensure_ascii=False))
        if  session["current_parent"] != (None,None):
            hashMap.put("type", "")
        hashMap.put("orientation", "")
        hashMap.put("gravity_horizontal", "")
        hashMap.put("gravity_vertical", "")
        hashMap.put("height", "")
        hashMap.put("width", "")
        hashMap.put("drawable", "")
        hashMap.put("Value", "")
        hashMap.put("Variable", "")
        hashMap.put("BackgroundColor", "")
        hashMap.put("StrokeWidth", "")
        hashMap.put("Padding", "")
        hashMap.put("Radius", "")
        hashMap.put("height_value", "")
        hashMap.put("width_value", "")
        hashMap.put("weight", "")
        hashMap.put("BackgroundColor", "")
        hashMap.put("TextSize", "")
        hashMap.put("TextColor", "")
        hashMap.put("TextBold", "")
        hashMap.put("TextItalic", "")
        hashMap.put("NumberPrecision", "")
        hashMap.put("RecognitionTemplate", "")
        hashMap.put("style_name", "")



    is_new_element = session["current_element"] == None

    if is_new_element:
        hashMap.put("orientation", get_synonym(orientation_elements,"vertical"))
        hashMap.put("height", get_synonym(scale_elements,"match_parent"))
        hashMap.put("width", get_synonym(scale_elements,"match_parent"))
        hashMap.put("weigth", 0)
    

    hashMap.put("Show_RecognitionTemplate_div","-1") 
    hashMap.put("Show_RecognitionTemplate_p","-1") 
    hashMap.put("Show_RecognitionTemplate","-1")  
    if is_new_element and not session["current_parent"][1]==None:
             hashMap.put("Show_layout_elements_table","-1")
             hashMap.put("Show_btns_table_elements","-1")
             hashMap.put("Show_layout_properties","-1")
             hashMap.put("Show_common_properties","-1")
            
             hashMap.put("Show_element_properties","-1")
    else:        

        if get_key(element_base,hashMap.get('type')) == 'LinearLayout' or get_key(element_base,hashMap.get('type')) == 'Tab' or get_key(element_base,hashMap.get('type')) == 'Tabs':
            hashMap.put("Show_layout_elements_table","1")
            hashMap.put("Show_btns_table_elements","1")
            hashMap.put("Show_layout_properties","1")
            hashMap.put("Show_common_properties","1")
            hashMap.put("Show_element_properties","-1")
        elif get_key(element_base,hashMap.get('type')) == 'Vision':
            
            hashMap.put("Show_RecognitionTemplate_div","1")  
            hashMap.put("Show_RecognitionTemplate_p","1")
            hashMap.put("Show_RecognitionTemplate","1") 


            hashMap.put("Show_layout_elements_table","-1")
            hashMap.put("Show_btns_table_elements","-1")
            hashMap.put("Show_layout_properties","-1")
            hashMap.put("Show_common_properties","-1")
            
            if session["current_parent"][1][0].get("type") == "Operation":
                hashMap.put("Show_element_properties","-1")  
                hashMap.put("Show_common_properties","-1")
            else:
                hashMap.put("Show_element_properties","1")  
                hashMap.put("Show_common_properties","1")    


        elif get_key(element_base,hashMap.get('type')) == '':
            hashMap.put("Show_layout_elements_table","-1")
            hashMap.put("Show_btns_table_elements","-1")
            hashMap.put("Show_layout_properties","-1")
            hashMap.put("Show_common_properties","-1")
            hashMap.put("Show_element_properties","-1")  
            
        else:    
            hashMap.put("Show_layout_elements_table","-1")
            hashMap.put("Show_btns_table_elements","-1")
            hashMap.put("Show_layout_properties","-1")
            hashMap.put("Show_common_properties","1")
            
            if session["current_parent"][1][0].get("type") == "Operation":
                hashMap.put("Show_element_properties","-1")  
                hashMap.put("Show_common_properties","-1")
            else:
                hashMap.put("Show_element_properties","1")      
                hashMap.put("Show_common_properties","1")

    return hashMap


def element_post_open(hashMap,_files=None,_data=None):

     


    return hashMap

def processes_input(hashMap,_files=None,_data=None):
  
    if hashMap.get("listener")=="btn_add_process":

        session["processes_table_id"] = -1
        uid = str(uuid.uuid4().hex)
        hashMap.put("process_uid",uid)
        hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"process_form", "key":uid, "reopen":True},ensure_ascii=False))  
        session["current_process_name"] = "Новый процесс"
        hashMap.put("process_name",session["current_process_name"])
        hashMap.put("SetTitle",session["current_process_name"]+" - *")

        hashMap.put("hidden","")
        hashMap.put("DefineOnBackPressed","")
        hashMap.put("login_screen","")
        hashMap.put("SC","")
        hashMap.put("PlanFactHeader","")
       
        session["current_element"] = None
        session["current_parent"] =(None,None)

    elif hashMap.get("listener")=="btn_add_processcv":

        session["processes_table_id"] = -1
        uid = str(uuid.uuid4().hex)
        hashMap.put("process_uid",uid)
        hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"activecv_process_form", "key":uid, "reopen":True},ensure_ascii=False))  
        session["current_process_name"] = "Новый ActiveCV"
        hashMap.put("process_name",session["current_process_name"])
        hashMap.put("SetTitle",session["current_process_name"]+" - *")

        hashMap.put("hidden","")
      
       
        session["current_element"] = None
        session["current_parent"] =(None,None)    


    elif hashMap.get("listener")=="btn_edit_process" or hashMap.get("listener")=="TableDoubleClick":
        
        if hashMap.containsKey("selected_line_id"):
         
            session["processes_table_id"] = int(hashMap.get("selected_line_id"))
            row = session["processes_table"][session["processes_table_id"]]

            if not 'uid' in row:
                row['uid'] = str(uuid.uuid4().hex)

            if row.get("type") == "Process":   

                hashMap.put("process_uid",session["processes_table"][session["processes_table_id"]].get("uid"))
                hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"process_form", "key":session["processes_table"][session["processes_table_id"]].get("uid"), "reopen":True},ensure_ascii=False))  
                session["current_process_name"] = row.get("ProcessName","")
                hashMap.put("process_name",session["current_process_name"])
                hashMap.put("SetTitle",session["current_process_name"])

                hashMap.put("hidden",row.get("hidden"))
                hashMap.put("DefineOnBackPressed",row.get("DefineOnBackPressed"))
                hashMap.put("login_screen",row.get("login_screen"))
                hashMap.put("SC",row.get("SC"))
                hashMap.put("PlanFactHeader",row.get("PlanFactHeader",""))

                session["current_element"] = row
                session["current_parent"] = (row,None)
                session["current_parent_dict"][session["processes_table"][session["processes_table_id"]].get("uid")] = session["current_parent"]
            elif row.get("type") == "CVOperation":    
                hashMap.put("process_uid",session["processes_table"][session["processes_table_id"]].get("uid"))
                hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"activecv_process_form", "key":session["processes_table"][session["processes_table_id"]].get("uid"), "reopen":True},ensure_ascii=False))  
                session["current_process_name"] = row.get("CVOperationName","")
                hashMap.put("process_name",session["current_process_name"])
                hashMap.put("SetTitle",session["current_process_name"])

                hashMap.put("hidden",row.get("hidden"))
              
                session["current_element"] = row
                session["current_parent"] = (row,None)
                session["current_parent_dict"][session["processes_table"][session["processes_table_id"]].get("uid")] = session["current_parent"]

            hashMap.remove("selected_line_id")

    elif hashMap.get("listener")=="btn_delete_process":
        
        sel_line = 'selected_line_id'
        if hashMap.containsKey(sel_line):
            session["processes_table"].pop(int(hashMap.get(sel_line)))
            
            hashMap.put("RefreshScreen","")
            hashMap.remove(sel_line)
    elif hashMap.get("listener")=="btn_paste":
        hashMap.put("ReadClipboard","")
    elif hashMap.get("listener")=="clipboard_result":
        jprocess = json.loads(hashMap.get("clipboard_result"))
        session["processes_table"].append(jprocess)

        save_configuration(session["configuration"],hashMap) 

        hashMap.put("RefreshScreen","")
        
    elif hashMap.get("listener")=="btn_copy":
        if hashMap.containsKey("selected_line_id"):
            session["processes_table_id"] = int(hashMap.get("selected_line_id"))
            row = session["processes_table"][session["processes_table_id"]]
            hashMap.put("WriteClipboard",json.dumps(row,ensure_ascii=False))    
    elif hashMap.get("listener")=="btn_up":
        if hashMap.containsKey("selected_line_id"):
            session["processes_table_id"] = int(hashMap.get("selected_line_id"))  
            if session["processes_table_id"]>0: 
                session["processes_table"].insert(session["processes_table_id"]-1,session["processes_table"].pop(session["processes_table_id"]))  
                save_configuration(session["configuration"],hashMap)    
                hashMap.put("RefreshScreen","") 
    elif hashMap.get("listener")=="btn_down":
        if hashMap.containsKey("selected_line_id"):
            session["processes_table_id"] = int(hashMap.get("selected_line_id")) 
            if session["processes_table_id"]<len(session["processes_table"]): 
                session["processes_table"].insert(session["processes_table_id"]+1,session["processes_table"].pop(session["processes_table_id"]))
            
            save_configuration(session["configuration"],hashMap) 
            hashMap.put("RefreshScreen","") 
    
    return hashMap   

def common_handlers_dialog_on_start(hashMap,_files=None,_data=None):

    hashMap.put("common_events",";".join(events_common))
    hashMap.put("handler_types",";".join(handler_types))
    hashMap.put("action_types",";".join(action_types))
    
    if  "CommonHandlers" in session["configuration"]["ClientConfiguration"]:
        hashMap.put("handlers_table",json.dumps(make_handlers_table(session["configuration"]["ClientConfiguration"]["CommonHandlers"],True),ensure_ascii=False))
    else:
        hashMap.put("handlers_table",json.dumps(make_handlers_table([],True),ensure_ascii=False))

   
    return hashMap

def list_to_dict(lst):
    res = {}
    for el in lst:
        keys = list(el.keys())
        res[keys[0]] =el[keys[0]]
    return res

def common_handlers_input(hashMap,_files=None,_data=None):

    if hashMap.get("listener") == "btn_add_handler":
        hashMap.put("ShowDialogLayout",json.dumps(handler_layout_lang,ensure_ascii=False))
        hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Обработчик"},ensure_ascii=False))
        hashMap.put("ShowDialog","")
        hashMap.put("ShowDialogActive","type;type_postExecute")

        
        
        hashMap.put("method","")


        hashMap.put("alias","")
        hashMap.put("event","")
        hashMap.put("action","")
        hashMap.put("type","")
        
        hashMap.put("listener","")

        hashMap.put("action_postExecute","")
        hashMap.put("type_postExecute","")
        hashMap.put("method_postExecute","")

        postExecute = ""
        session["edit_handler_mode"] = -1
    elif hashMap.get("listener") == "btn_edit_handler" or hashMap.get("listener") == "TableDoubleClick" or hashMap.get("listener") == "type" or hashMap.get("listener") == "type_postExecute" :
        if hashMap.containsKey("selected_line_id"):
            dialog_layout_str = json.dumps(handler_layout_lang,ensure_ascii=False)
            session["edit_handler_mode"] = int(hashMap.get("selected_line_id"))

            handler_str = session["configuration"]["ClientConfiguration"]["CommonHandlers"][session["edit_handler_mode"]]

            if handler_str.get("type","")=="js":

                dialog_layout_str = dialog_layout_str.replace("#type_method","html")
                
                try:
                    m = base64.b64decode(handler_str.get("method","")).decode("utf-8")
                except:
                    m=handler_str.get("method","") 

                method =  '<code-input required id="method" class="line-numbers" style="resize: both; overflow: hidden; width: 100%;" lang="JavaScript" placeholder="Write some JavaScript!">'+m+'</code-input>'
                hashMap.put("method",method)
            elif handler_str.get("type","")=="pythonscript":
                dialog_layout_str = dialog_layout_str.replace("#type_method","html")
             
                try:
                    m = base64.b64decode(handler_str.get("method","")).decode("utf-8")
                except:
                    m=handler_str.get("method","") 

                method =  '<code-input required id="method" class="line-numbers" style="resize: both; overflow: hidden; width: 100%;" lang="Python" placeholder="Write some JavaScript!">'+m+'</code-input>'
                hashMap.put("method",method)    
            else:    
                dialog_layout_str = dialog_layout_str.replace("#type_method","MultilineText")
                
                hashMap.put("method",handler_str.get("method",""))
            
            hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Обработчик"},ensure_ascii=False))
            hashMap.put("ShowDialog","")
            hashMap.put("ShowDialogActive","type;type_postExecute")

            hashMap.put("alias",handler_str.get("alias",""))
            hashMap.put("event",handler_str.get("event",""))
            hashMap.put("action",handler_str.get("action",""))
            hashMap.put("type",handler_str.get("type",""))
            
            hashMap.put("listener",handler_str.get("listener",""))

            hashMap.put("action_postExecute","")
            hashMap.put("type_postExecute","")
            hashMap.put("method_postExecute","")

            postExecute = ""
            pe = handler_str.get("postExecute")
            if pe!=None and pe!="":
                jpe = json.loads(pe)
                if isinstance(jpe, list) :
                    if len(jpe)>0:
                        postExecute =  pe    
                        
                        hashMap.put("action_postExecute",jpe[0].get("action",""))
                        hashMap.put("type_postExecute",jpe[0].get("type",""))
                        if jpe[0].get("type","")=="js":
                            dialog_layout_str = dialog_layout_str.replace("#_PE","html")
                            try:    
                                m = base64.b64decode(jpe[0].get("method","")).decode("utf-8")
                            except:
                                m=handler_str.get("method_postExecute","")    

                            method =  '<code-input required id="method_postExecute" class="line-numbers" style="resize: both; overflow: hidden; width: 100%;" lang="JavaScript" placeholder="Write some JavaScript!">'+m+'</code-input>'
                            hashMap.put("method_postExecute",method)
                        elif jpe[0].get("type","")=="pythonscript":
                            dialog_layout_str = dialog_layout_str.replace("#_PE","html")
                            try:    
                                m = base64.b64decode(jpe[0].get("method","")).decode("utf-8")
                            except:
                                m=handler_str.get("method_postExecute","")    

                            method =  '<code-input required id="method_postExecute" class="line-numbers" style="resize: both; overflow: hidden; width: 100%;" lang="Python" placeholder="Write some Python!">'+m+'</code-input>'
                            hashMap.put("method_postExecute",method)    
                        else:    
                            dialog_layout_str = dialog_layout_str.replace("#_PE","MultilineText")

                            hashMap.put("method_postExecute",jpe[0].get("method","")) 
                        #hashMap.put("method_postExecute",jpe[0].get("method",""))
            
            hashMap.put("ShowDialogLayout",dialog_layout_str)
            hashMap.remove("selected_line_id")  
        elif hashMap.containsKey("dialog_values"):
            dialog_layout_str = json.dumps(handler_layout_lang,ensure_ascii=False)

            handler_str = list_to_dict(json.loads(hashMap.get("dialog_values"))) 
            if handler_str.get("type","")=="js":
                dialog_layout_str = dialog_layout_str.replace("#type_method","html")

                try:
                    m = base64.b64decode(handler_str.get("method","")).decode("utf-8")
                except:
                    m=handler_str.get("method","")    
                method =  '<code-input required id="method" class="line-numbers" style="resize: both; overflow: hidden; width: 100%;" lang="JavaScript" placeholder="Write some JavaScript!">'+m+'</code-input>'
                hashMap.put("method",method)
            elif handler_str.get("type","")=="pythonscript":
                dialog_layout_str = dialog_layout_str.replace("#type_method","html")

                try:
                    m = base64.b64decode(handler_str.get("method","")).decode("utf-8")
                except:
                    m=handler_str.get("method","")    

                method =  '<code-input required id="method" class="line-numbers" style="resize: both; overflow: hidden; width: 100%;" lang="Python" placeholder="Write some Python!">'+m+'</code-input>'
                hashMap.put("method",method)    
            else:    
                dialog_layout_str = dialog_layout_str.replace("#type_method","MultilineText")

                hashMap.put("method",handler_str.get("method",""))
            
            hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Обработчик"},ensure_ascii=False))
            
            
            hashMap.put("listener",handler_str.get("listener",""))

            if handler_str.get("type_postExecute","")=="js":
                dialog_layout_str = dialog_layout_str.replace("#_PE","html")
                try:    
                    m = base64.b64decode(handler_str.get("method_postExecute","")).decode("utf-8")
                except:
                    m=handler_str.get("method_postExecute","")    

                method =  '<code-input required id="method_postExecute" class="line-numbers" style="resize: both; overflow: hidden; width: 100%;" lang="JavaScript" placeholder="Write some JavaScript!">'+m+'</code-input>'
                hashMap.put("method_postExecute",method)
            elif handler_str.get("type_postExecute","")=="pythonscript":
                dialog_layout_str = dialog_layout_str.replace("#_PE","html")
                try:    
                    m = base64.b64decode(handler_str.get("method_postExecute","")).decode("utf-8")
                except:
                    m=handler_str.get("method_postExecute","")    

                method =  '<code-input required id="method_postExecute" class="line-numbers" style="resize: both; overflow: hidden; width: 100%;" lang="Python" placeholder="Write some Python!">'+m+'</code-input>'
                hashMap.put("method_postExecute",method)    
            else:    
                dialog_layout_str = dialog_layout_str.replace("#_PE","MultilineText")

                hashMap.put("method_postExecute",handler_str.get("method_postExecute",""))    


            hashMap.put("action_postExecute",handler_str.get("action_postExecute",""))
            hashMap.put("type_postExecute",handler_str.get("type_postExecute",""))
            #hashMap.put("method_postExecute",handler_str.get("method_postExecute",""))

            hashMap.put("ShowDialogLayout",dialog_layout_str)
            hashMap.put("ShowDialog","")

            #postExecute = ""
            #pe = handler_str.get("postExecute")
            #if pe!=None and pe!="":
            #    jpe = json.loads(pe)
            #    if isinstance(jpe, list) :
            #        if len(jpe)>0:
            #            postExecute =  pe    
                        
            #            hashMap.put("action_postExecute",jpe[0].get("action",""))
            #            hashMap.put("type_postExecute",jpe[0].get("type",""))
            #            hashMap.put("method_postExecute",jpe[0].get("method",""))

    elif hashMap.get("listener") == "btn_delete_handler":
        if hashMap.containsKey("selected_line_id"):
            pos = int(hashMap.get("selected_line_id"))   
            session["configuration"]["ClientConfiguration"]["CommonHandlers"].pop(pos)
            hashMap.put("RefreshScreen","")
            hashMap.remove("selected_line_id")      

    elif hashMap.get("listener") == "onResultPositive": 
        dialog_values = list_to_dict(json.loads(hashMap.get("dialog_values")))
        
        if dialog_values.get("type")=='js' or dialog_values.get("type")=='pythonscript':
            method = dialog_values.get('method')  
            method = base64.b64encode(method.encode('utf-8')).decode('utf-8')     
        else:    
            method = dialog_values.get('method')  

        

        if not "CommonHandlers" in session["configuration"]["ClientConfiguration"]:
            session["configuration"]["ClientConfiguration"]["CommonHandlers"] = []
        
        postExecute = ""
        if len(str(dialog_values.get("action_postExecute")))>0 and len(str(dialog_values.get("type_postExecute")))>0:
            if dialog_values.get("type_postExecute")=='js' or dialog_values.get("type_postExecute")=='pythonscript':
                methodPE = dialog_values.get('method_postExecute')  
                methodPE = base64.b64encode(methodPE.encode('utf-8')).decode('utf-8')
            else:    
                methodPE = dialog_values.get('method_postExecute')  

            

            postExecute =json.dumps( [{"action":dialog_values.get("action_postExecute",""),"type":dialog_values.get("type_postExecute",""),"method":methodPE}], ensure_ascii=False)

        if session["edit_handler_mode"] == -1 :
            session["configuration"]["ClientConfiguration"]["CommonHandlers"].append({"event":dialog_values.get("event",""),"action":dialog_values.get("action",""),"listener":dialog_values.get("listener",""),"type":dialog_values.get("type",""),"method":method,"postExecute":postExecute,"alias":dialog_values.get("alias","")}) 
        else:
            session["configuration"]["ClientConfiguration"]["CommonHandlers"][session["edit_handler_mode"]] ={"event":dialog_values.get("event",""),"action":dialog_values.get("action",""),"listener":dialog_values.get("listener",""),"type":dialog_values.get("type",""),"method":method,"postExecute":postExecute,"alias":dialog_values.get("alias","")} 
                    
        hashMap.put("RefreshScreen","")
        save_configuration(session["configuration"],hashMap)

    return hashMap

session["mediafiles_table_id"] = -1
def mediafiles_input(hashMap,_files=None,_data=None):
  
    if hashMap.get("listener")=="btn_add_mediafile":
        session["mediafiles_table_id"] = -1
        hashMap.put("ShowDialogLayout",json.dumps(mediafile_layout,ensure_ascii=False))
        hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Добавление медиафайла"},ensure_ascii=False))
        hashMap.put("ShowDialog","")
        hashMap.put("key","")

    
    elif hashMap.get("listener") == "onResultPositive": 
        if session["mediafiles_table_id"] == -1:
            dialog_values = list_to_dict(json.loads(hashMap.get("dialog_values")))

            if not "Mediafile" in session["configuration"]["ClientConfiguration"]:
                session["configuration"]["ClientConfiguration"]["Mediafile"] = []
            
            if 'base64' in dialog_values:
                filename,ext = os.path.splitext(dialog_values.get("file"))

                session["configuration"]["ClientConfiguration"]["Mediafile"].append({"MediafileKey":dialog_values.get("key"),"MediafileExt":ext[1:],"MediafileData":dialog_values.get("base64")}) 
                hashMap.put("RefreshScreen","")
                save_configuration(session["configuration"],hashMap)
     

    elif hashMap.get("listener")=="btn_delete_mediafile":
        
        sel_line = 'selected_line_id'
        if hashMap.containsKey(sel_line):
            session["configuration"]["ClientConfiguration"]["Mediafile"].pop(int(hashMap.get(sel_line)))
            
            hashMap.put("RefreshScreen","")
            save_configuration(session["configuration"],hashMap)
            hashMap.remove(sel_line)

    
    return hashMap 

def mediafiles_open(hashMap,_files=None,_data=None):

    if "Mediafile" in session["configuration"]["ClientConfiguration"]:
        hashMap.put("mediafiles_table",json.dumps(make_mediafiles_table(session["configuration"]["ClientConfiguration"]["Mediafile"]),ensure_ascii=False))
    else:    
        hashMap.put("mediafiles_table",json.dumps(make_mediafiles_table([]),ensure_ascii=False))
 
    return hashMap

def activecv_process_open(hashMap,_files=None,_data=None):

    if not session["current_element"] == None:
        hashMap.put("steps_table",json.dumps(make_onefield_table(session["current_element"]["CVFrames"],"Name","Шаг ActiveCV"),ensure_ascii=False))
    else:
        hashMap.put("steps_table",json.dumps(make_onefield_table([],"Name","Шаг ActiveCV"),ensure_ascii=False))
   
    return hashMap

def activecv_process_input(hashMap,_files=None,_data=None):

    if session["current_element"]==None:
        closeuid  =hashMap.get("process_uid")
    else:    
        closeuid = session["current_element"]['uid']

    if hashMap.get("listener")=="btn_save" or hashMap.get("listener")=="btn_add_step" or hashMap.get("listener")=="btn_edit_step":



  

        if session["processes_table_id"]==-1:
            session["processes_table"].append({
                                                    "CVOperationName": hashMap.get("process_name"),
                                                    "type":"CVOperation",
                                                    "uid": closeuid,
                                                    "CVFrames":[]
                                                
                                                })
            session["processes_table_id"]=len(session["processes_table"])-1

        else:   
            session["current_element"]["ProcessName"] =hashMap.get("process_name") 
            session["current_element"]["hidden"] =hashMap.get("hidden") 
            session["current_element"]["uid"] =closeuid 

        session["current_parent"] = (session["processes_table"][session["processes_table_id"]],None)
        session["current_element"] = session["current_parent"][0]
        session["current_parent_dict"][closeuid] = session["current_parent"]

    if hashMap.get("listener")=="btn_save" or hashMap.get("listener")=="btn_close":

        hashMap.put("CloseTab",closeuid)

        hashMap.put("processes_table",json.dumps(make_processes_table(session["processes_table"]),ensure_ascii=False))

        hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"main_screen", "key":"Процессы", "reopen":True},ensure_ascii=False))

        save_configuration(session["configuration"],hashMap)

        #hashMap.put("UnblockTabs","")

     
    elif hashMap.get("listener")=="btn_add_step":

        uid = str(uuid.uuid4().hex)
        hashMap.put("step_uid",uid)

        hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"step_form","key":uid,"reopen":True},ensure_ascii=False))  
        hashMap.put("step_name","Новый шаг")

        hashMap.put("CVDetector","")
        hashMap.put("CVResolution","")
        hashMap.put("CVMode","")
        hashMap.put("CVActionButtons","")
        hashMap.put("CVAction","")
        hashMap.put("CVInfo","")
        hashMap.put("CVCameraDevice","")
        hashMap.put("CVDetectorMode","")
        hashMap.put("CVMask","")
        hashMap.put("CVInfo","")
        hashMap.put("RecognitionTemplate","")

        hashMap.put("SetTitle","Новый шаг - *")

        #блокировка
        #hashMap.put("BlockTabs","")

                
        session["screens_table_id"] = -1
        session["current_element"] = None 
        session["current_parent"] = (None,session["current_parent"])
        session["current_parent_dict"][uid] = session["current_parent"]   
    elif hashMap.get("listener")=="btn_edit_step" or hashMap.get("listener") == "TableDoubleClick":
        session["screens_table_id"] = int(hashMap.get("selected_line_id"))
        row = session["current_element"]["CVFrames"][session["screens_table_id"]]
        if not 'uid' in row:
           row['uid'] = str(uuid.uuid4().hex)

        hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"step_form","key":row['uid'],"reopen":True,"no_close":True},ensure_ascii=False))  
        current_screen_name = row.get("Name")
        hashMap.put("step_name",current_screen_name)
        hashMap.put("SetTitle",current_screen_name)

        hashMap.put("CVDetector",get_synonym(detector_elements,row.get("CVDetector")))
        hashMap.put("CVResolution",row.get("CVResolution"))
        hashMap.put("CVMode",get_synonym(visual_mode_elements,row.get("CVMode")))
        hashMap.put("CVActionButtons",row.get("CVActionButtons"))
        hashMap.put("CVAction",row.get("CVAction"))
        hashMap.put("CVInfo",row.get("CVInfo"))
        hashMap.put("CVCameraDevice",get_synonym(camera_mode_elements,row.get("CVCameraDevice")))
        hashMap.put("CVDetectorMode",get_synonym(detector_mode_elements,row.get("CVDetectorMode")))
        hashMap.put("CVMask",row.get("CVMask"))
        hashMap.put("CVInfo",row.get("CVInfo"))
        hashMap.put("RecognitionTemplate",row.get("RecognitionTemplate"))

        hashMap.put("screen_uid",row.get("uid"))

        #блокировка
        #hashMap.put("BlockTabs","")

        session["current_element"] = row  
        session["current_parent"] = (row,session["current_parent"]) 
        session["current_parent_dict"][row['uid']] = session["current_parent"]      
    elif hashMap.get("listener")=="btn_delete_step":
        
        sel_line = 'selected_line_id'
        if hashMap.containsKey(sel_line):
                session["current_element"]['CVFrames'].pop(int(hashMap.get(sel_line)))
                #hashMap.put("screens_table",json.dumps(jtable,ensure_ascii=False)) 
                #hashMap.put("SetValuesTable",json.dumps([{"screens_table":jtable}]) )       
                hashMap.put("RefreshScreen","")
                hashMap.remove(sel_line)    

    return hashMap
 
def step_open(hashMap,_files=None,_data=None):
    hashMap.put("common_events",captions_event_elements_cv)
    hashMap.put("handler_types",";".join(handler_types))
    hashMap.put("action_types",";".join(action_types))

    hashMap.put("CVDetector_elements",captions_detector_elements)
    hashMap.put("CVResolution_elements",";".join(resolution_elements))
    hashMap.put("CVMode_elements",captions_visual_mode_elements)
    hashMap.put("CVCameraDevice_elements",captions_detector_mode_elements)
    hashMap.put("CVDetectorMode_elements",captions_camera_mode_elements)

    recognition_templates = []
    recognition_templates.append("")
    if "RecognitionTemplates" in session["configuration"]['ClientConfiguration']:
        for t in session["configuration"]['ClientConfiguration']["RecognitionTemplates"]:
            recognition_templates.append(t.get('name'))
    hashMap.put("recognition_templates",";".join(recognition_templates)) 

    if not session["current_element"] == None:
        if  "Handlers" in session["current_element"]:
            hashMap.put("handlers_table",json.dumps(make_handlers_table(session["current_element"]["Handlers"],True),ensure_ascii=False))
        else:
            hashMap.put("handlers_table",json.dumps(make_handlers_table([],True),ensure_ascii=False))    
    else:
         hashMap.put("handlers_table",json.dumps(make_handlers_table([],True),ensure_ascii=False))
   
    return hashMap

def step_input(hashMap,_files=None,_data=None):

    closeuid = None

    if session["current_element"]==None:
        closeuid = hashMap.get("step_uid")
    else:    
        closeuid = session["current_element"]['uid']

    if hashMap.get("listener")=="btn_save" or hashMap.get("listener")=="btn_add_handler":

        

        session["current_parent"] =session["current_parent"][1]
        session["current_element"] = session["current_parent"][0]

        if session["screens_table_id"]==-1:
            session["current_element"]['CVFrames'].append({
                                                    "type": "CVFrame",
                                                    "Name": hashMap.get("step_name"),
                                                    "uid": closeuid,

                                                    "CVDetector": get_key(detector_elements,hashMap.get("CVDetector")),
                                                    "CVResolution": hashMap.get("CVResolution"),
                                                    "CVMode": get_key(visual_mode_elements,hashMap.get("CVMode")),
                                                    "CVActionButtons": hashMap.get("CVActionButtons"),
                                                    "CVAction": hashMap.get("CVAction"),
                                                    "CVInfo": hashMap.get("CVInfo"),
                                                    "CVCameraDevice": get_key(camera_mode_elements,hashMap.get("CVCameraDevice")),
                                                    "CVDetectorMode": get_key(detector_mode_elements,hashMap.get("CVDetectorMode")),
                                                    "CVMask": hashMap.get("CVMask"),
                                                    "CVOnline": False,
                                                    "RecognitionTemplate": hashMap.get("RecognitionTemplate"),
                                                    
                                                
                                                }) 
            
            session["screens_table_id"]=len(session["current_element"]['CVFrames'])-1
            
            
        else:   
            session["current_element"]['CVFrames'][session["screens_table_id"]]["Name"] = hashMap.get("step_name")
            session["current_element"]['CVFrames'][session["screens_table_id"]]["uid"] = closeuid

            session["current_element"]['CVFrames'][session["screens_table_id"]]["CVDetector"] = get_key(detector_elements,hashMap.get("CVDetector"))
            session["current_element"]['CVFrames'][session["screens_table_id"]]["CVResolution"] = hashMap.get("CVResolution")
            session["current_element"]['CVFrames'][session["screens_table_id"]]["CVMode"] = get_key(visual_mode_elements,hashMap.get("CVMode"))
            session["current_element"]['CVFrames'][session["screens_table_id"]]["CVActionButtons"] = hashMap.get("CVActionButtons")
            session["current_element"]['CVFrames'][session["screens_table_id"]]["CVAction"] = hashMap.get("CVAction")
            session["current_element"]['CVFrames'][session["screens_table_id"]]["CVInfo"] = hashMap.get("CVInfo")
            session["current_element"]['CVFrames'][session["screens_table_id"]]["CVCameraDevice"] = get_key(camera_mode_elements,hashMap.get("CVCameraDevice"))
            session["current_element"]['CVFrames'][session["screens_table_id"]]["CVDetectorMode"] = get_key(detector_mode_elements,hashMap.get("CVDetectorMode"))
            session["current_element"]['CVFrames'][session["screens_table_id"]]["CVMask"] = hashMap.get("CVMask")
            session["current_element"]['CVFrames'][session["screens_table_id"]]["RecognitionTemplate"] = hashMap.get("RecognitionTemplate")
               
        
        session["current_parent"] = (session["current_element"]['CVFrames'][session["screens_table_id"]],session["current_parent"])
        session["current_parent_dict"][closeuid] = session["current_parent"]

        
        session["current_element"] = session["current_parent"][0]
        


    if hashMap.get("listener")=="btn_save" or hashMap.get("listener")=="btn_close":
 
        hashMap.put("CloseTab",closeuid)
        hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"activecv_process_form", "key":session["current_parent"][1][0]['uid'], "reopen":True},ensure_ascii=False))

        session["current_parent"] = session["current_parent"][1]
        process_table_id = session["processes_table"].index(session["current_parent"][0])
        session["current_element"] = session["current_parent"][0]

        save_configuration(session["configuration"],hashMap)

        #блокировка
        #hashMap.put("UnblockTabs","")
 
   
    elif hashMap.get("listener") == "btn_add_handler":
        hashMap.put("ShowDialogLayout",json.dumps(handler_layout_lang,ensure_ascii=False))
        hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Обработчик"},ensure_ascii=False))
        hashMap.put("ShowDialog","")
        hashMap.put("ShowDialogActive","type;type_postExecute")

        hashMap.put("alias","")
        hashMap.put("event","")
        hashMap.put("action","")
        hashMap.put("type","")
        hashMap.put("method","")
        hashMap.put("listener","")

        hashMap.put("action_postExecute","")
        hashMap.put("type_postExecute","")
        hashMap.put("method_postExecute","")
       
        postExecute = ""
        session["edit_handler_mode"] = -1

    elif hashMap.get("listener") == "btn_edit_handler" or hashMap.get("listener") == "type" or hashMap.get("listener") == "type_postExecute" or (hashMap.get("listener") == "TableDoubleClick"  and hashMap.get("table_id")=='handlers_table'):
        if hashMap.containsKey("selected_line_id") and hashMap.get("table_id")=='handlers_table':
            dialog_layout_str = json.dumps(handler_layout_lang,ensure_ascii=False)
            
            session["edit_handler_mode"] = int(hashMap.get("selected_line_id"))

            handler_str = session["current_element"]['Handlers'][session["edit_handler_mode"]]

            

            if handler_str.get("type","")=="js":

                dialog_layout_str = dialog_layout_str.replace("#type_method","html")
                
                try:
                    m = base64.b64decode(handler_str.get("method","")).decode("utf-8")
                except:
                    m=handler_str.get("method","") 

                method =  '<code-input required id="method" class="line-numbers" style="resize: both; overflow: hidden; width: 100%;" lang="JavaScript" placeholder="Write some JavaScript!">'+m+'</code-input>'
                hashMap.put("method",method)
            elif handler_str.get("type","")=="pythonscript":
                dialog_layout_str = dialog_layout_str.replace("#type_method","html")
             
                try:
                    m = base64.b64decode(handler_str.get("method","")).decode("utf-8")
                except:
                    m=handler_str.get("method","") 

                method =  '<code-input required id="method" class="line-numbers" style="resize: both; overflow: hidden; width: 100%;" lang="Python" placeholder="Write some JavaScript!">'+m+'</code-input>'
                hashMap.put("method",method)    
            else:    
                dialog_layout_str = dialog_layout_str.replace("#type_method","MultilineText")
                
                hashMap.put("method",handler_str.get("method",""))
            
            hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Обработчик"},ensure_ascii=False))
            hashMap.put("ShowDialog","")
            hashMap.put("ShowDialogActive","type;type_postExecute")

            hashMap.put("alias",handler_str.get("alias",""))
            hashMap.put("event",handler_str.get("event",""))
            hashMap.put("action",handler_str.get("action",""))
            hashMap.put("type",handler_str.get("type",""))
            
            hashMap.put("listener",handler_str.get("listener",""))

            hashMap.put("action_postExecute","")
            hashMap.put("type_postExecute","")
            hashMap.put("method_postExecute","")

            postExecute = ""
            pe = handler_str.get("postExecute")
            if pe!=None and pe!="":
                jpe = json.loads(pe)
                if isinstance(jpe, list) :
                    if len(jpe)>0:
                        postExecute =  pe    
                        
                        hashMap.put("action_postExecute",jpe[0].get("action",""))
                        hashMap.put("type_postExecute",jpe[0].get("type",""))
                        if jpe[0].get("type","")=="js":
                            dialog_layout_str = dialog_layout_str.replace("#_PE","html")
                            try:    
                                m = base64.b64decode(jpe[0].get("method","")).decode("utf-8")
                            except:
                                m=handler_str.get("method_postExecute","")    

                            method =  '<code-input required id="method_postExecute" class="line-numbers" style="resize: both; overflow: hidden; width: 100%;" lang="JavaScript" placeholder="Write some JavaScript!">'+m+'</code-input>'
                            hashMap.put("method_postExecute",method)
                        elif jpe[0].get("type","")=="pythonscript":
                            dialog_layout_str = dialog_layout_str.replace("#_PE","html")
                            try:    
                                m = base64.b64decode(jpe[0].get("method","")).decode("utf-8")
                            except:
                                m=handler_str.get("method_postExecute","")    

                            method =  '<code-input required id="method_postExecute" class="line-numbers" style="resize: both; overflow: hidden; width: 100%;" lang="Python" placeholder="Write some Python!">'+m+'</code-input>'
                            hashMap.put("method_postExecute",method)    
                        else:    
                            dialog_layout_str = dialog_layout_str.replace("#_PE","MultilineText")

                            hashMap.put("method_postExecute",jpe[0].get("method","")) 
                        #hashMap.put("method_postExecute",jpe[0].get("method",""))
            
            hashMap.put("ShowDialogLayout",dialog_layout_str)
            hashMap.remove("selected_line_id")  
        elif hashMap.containsKey("dialog_values"):
            dialog_layout_str = json.dumps(handler_layout_lang,ensure_ascii=False)

            handler_str = list_to_dict(json.loads(hashMap.get("dialog_values"))) 
            if handler_str.get("type","")=="js":
                dialog_layout_str = dialog_layout_str.replace("#type_method","html")

                try:
                    m = base64.b64decode(handler_str.get("method","")).decode("utf-8")
                except:
                    m=handler_str.get("method","")    
                method =  '<code-input required id="method" class="line-numbers" style="resize: both; overflow: hidden; width: 100%;" lang="JavaScript" placeholder="Write some JavaScript!">'+m+'</code-input>'
                hashMap.put("method",method)
            elif handler_str.get("type","")=="pythonscript":
                dialog_layout_str = dialog_layout_str.replace("#type_method","html")

                try:
                    m = base64.b64decode(handler_str.get("method","")).decode("utf-8")
                except:
                    m=handler_str.get("method","")    

                method =  '<code-input required id="method" class="line-numbers" style="resize: both; overflow: hidden; width: 100%;" lang="Python" placeholder="Write some Python!">'+m+'</code-input>'
                hashMap.put("method",method)    
            else:    
                dialog_layout_str = dialog_layout_str.replace("#type_method","MultilineText")

                hashMap.put("method",handler_str.get("method",""))
            
            hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Обработчик"},ensure_ascii=False))
            
            
            hashMap.put("listener",handler_str.get("listener",""))

            if handler_str.get("type_postExecute","")=="js":
                dialog_layout_str = dialog_layout_str.replace("#_PE","html")
                try:    
                    m = base64.b64decode(handler_str.get("method_postExecute","")).decode("utf-8")
                except:
                    m=handler_str.get("method_postExecute","")    

                method =  '<code-input required id="method_postExecute" class="line-numbers" style="resize: both; overflow: hidden; width: 100%;" lang="JavaScript" placeholder="Write some JavaScript!">'+m+'</code-input>'
                hashMap.put("method_postExecute",method)
            elif handler_str.get("type_postExecute","")=="pythonscript":
                dialog_layout_str = dialog_layout_str.replace("#_PE","html")
                try:    
                    m = base64.b64decode(handler_str.get("method_postExecute","")).decode("utf-8")
                except:
                    m=handler_str.get("method_postExecute","")    

                method =  '<code-input required id="method_postExecute" class="line-numbers" style="resize: both; overflow: hidden; width: 100%;" lang="Python" placeholder="Write some Python!">'+m+'</code-input>'
                hashMap.put("method_postExecute",method)    
            else:    
                dialog_layout_str = dialog_layout_str.replace("#_PE","MultilineText")

                hashMap.put("method_postExecute",handler_str.get("method_postExecute",""))    


            hashMap.put("action_postExecute",handler_str.get("action_postExecute",""))
            hashMap.put("type_postExecute",handler_str.get("type_postExecute",""))
            #hashMap.put("method_postExecute",handler_str.get("method_postExecute",""))

            hashMap.put("ShowDialogLayout",dialog_layout_str)
            hashMap.put("ShowDialog","")

           
            

    elif hashMap.get("listener") == "btn_delete_handler":
        if hashMap.containsKey("selected_line_id"):
            pos = int(hashMap.get("selected_line_id"))   
            session["current_element"]['Handlers'].pop(pos)
            hashMap.put("RefreshScreen","")
            hashMap.remove("selected_line_id")      

    elif hashMap.get("listener") == "onResultPositive": 
        dialog_values = list_to_dict(json.loads(hashMap.get("dialog_values")))
        
        if dialog_values.get("type")=='js' or dialog_values.get("type")=='pythonscript':
            method = dialog_values.get('method')  
            method = base64.b64encode(method.encode('utf-8')).decode('utf-8')     
        else:    
            method = dialog_values.get('method')  

        

        if not "Handlers" in session["current_element"]:
            session["current_element"]['Handlers'] = []
        
        postExecute = ""
        if len(str(dialog_values.get("action_postExecute")))>0 and len(str(dialog_values.get("type_postExecute")))>0:
            if dialog_values.get("type_postExecute")=='js' or dialog_values.get("type_postExecute")=='pythonscript':
                methodPE = dialog_values.get('method_postExecute')  
                methodPE = base64.b64encode(methodPE.encode('utf-8')).decode('utf-8')
            else:    
                methodPE = dialog_values.get('method_postExecute')  

            

            postExecute =json.dumps( [{"action":dialog_values.get("action_postExecute",""),"type":dialog_values.get("type_postExecute",""),"method":methodPE}], ensure_ascii=False)

        if session["edit_handler_mode"] == -1 :
            session["current_element"]['Handlers'].append({"event":dialog_values.get("event",""),"action":dialog_values.get("action",""),"listener":dialog_values.get("listener",""),"type":dialog_values.get("type",""),"method":method,"postExecute":postExecute,"alias":dialog_values.get("alias","")}) 
        else:
            session["current_element"]['Handlers'][session["edit_handler_mode"]] ={"event":dialog_values.get("event",""),"action":dialog_values.get("action",""),"listener":dialog_values.get("listener",""),"type":dialog_values.get("type",""),"method":method,"postExecute":postExecute,"alias":dialog_values.get("alias","")} 
                    
        hashMap.put("RefreshScreen","")
        save_configuration(session["configuration"],hashMap)


    return hashMap


ocr_layout =  {
            "Value": "",
            "Variable": "",
            "type": "LinearLayout",
            "weight": "0",
            "height": "match_parent",
            "width": "match_parent",
            "orientation": "vertical",
            "Elements": [
                {
                    "type": "EditTextText",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Название варианта|@name",
                    "Variable": "name",
                    "gravity_horizontal": "left"
                },
                {
                    "type": "TextView",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Вариант: опорная выборка - SQL",
                    "gravity_horizontal": "left"
                },
                {
                    "type": "EditTextText",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "SQL запрос|@query",
                    "Variable": "query",
                    "gravity_horizontal": "left"
                },
                {
                    "type": "EditTextText",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Контрольное поле|@control_field",
                    "Variable": "control_field",
                    "gravity_horizontal": "left"
                },
                {
                    "type": "TextView",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Вариант: опорная выборка - список значений/обработчик",
                    "Variable": "query",
                    "gravity_horizontal": "left"
                },
                {
                    "type": "EditTextText",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Список значений|@values_list",
                    "Variable": "values_list",
                    "gravity_horizontal": "left"
                },
                {
                    "type": "TextView",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "",
                    "Variable": "query",
                    "gravity_horizontal": "left"
                },
                {
                    "type": "EditTextNumeric",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Минимальная длина|@min_length",
                    "Variable": "min_length",
                    "gravity_horizontal": "left"
                },
                {
                    "type": "EditTextNumeric",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Максимальная длина|@max_length",
                    "Variable": "max_length",
                    "gravity_horizontal": "left"
                },
                {
                    "type": "CheckBox",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Заменить O на 0",
                    "Variable": "ReplaceO",
                    "gravity_horizontal": "left"
                },
                {
                    "type": "CheckBox",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Преобразовать к верхнему регистру",
                    "Variable": "ToUpcase",
                    "gravity_horizontal": "left"
                } ,
                {
                    "type": "EditTextNumeric",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Количество измерений|@mesure_qty",
                    "Variable": "mesure_qty",
                    "gravity_horizontal": "left"
                },
                {
                    "type": "EditTextNumeric",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Минимальная частота (0-100)|@min_freq",
                    "Variable": "min_freq",
                    "gravity_horizontal": "left"
                }
                ,

                {
                    "type": "CheckBox",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Только числа (для Мультисканер)|@OnlyNumbers",
                    "Variable": "OnlyNumbers",
                    "gravity_horizontal": "left"
                }
            ],
            "BackgroundColor": "",
            "StrokeWidth": "",
            "Padding": ""
        }

date_layout =  {
            "Value": "",
            "Variable": "",
            "type": "LinearLayout",
            "weight": "0",
            "height": "match_parent",
            "width": "match_parent",
            "orientation": "vertical",
            "Elements": [

                {
                    "type": "EditTextText",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Название варианта|@name",
                    "Variable": "name",
                    "gravity_horizontal": "left"
                },         
               {
                    "type": "EditTextText",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Поле результат|@result_field",
                    "Variable": "result_field ",
                    "gravity_horizontal": "left"
                }
            ]
        }
number_layout =  {
            "Value": "",
            "Variable": "",
            "type": "LinearLayout",
            "weight": "0",
            "height": "match_parent",
            "width": "match_parent",
            "orientation": "vertical",
            "Elements": [

                {
                    "type": "EditTextText",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Название варианта|@name",
                    "Variable": "name",
                    "gravity_horizontal": "left"
                },         
               {
                    "type": "EditTextText",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Поле результат|@result_field",
                    "Variable": "result_field ",
                    "gravity_horizontal": "left"
                },
                {
                    "type": "EditTextNumeric",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Количество циклов измерений|@count_objects",
                    "Variable": "count_objects",
                    "gravity_horizontal": "left"
                }
            ]
        }
platenumber_layout =  {
            "Value": "",
            "Variable": "",
            "type": "LinearLayout",
            "weight": "0",
            "height": "match_parent",
            "width": "match_parent",
            "orientation": "vertical",
            "Elements": [

                {
                    "type": "EditTextText",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Название варианта|@name",
                    "Variable": "name",
                    "gravity_horizontal": "left"
                },         
               {
                    "type": "EditTextText",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Поле результат|@result_field",
                    "Variable": "result_field ",
                    "gravity_horizontal": "left"
                }
            ]
        }
    

session["recognition_table_id"] = -1
def recognition_input(hashMap,_files=None,_data=None):
 
    if hashMap.get("listener")=="btn_add_ocr":
        session["recognition_table_id"]  = -1
        hashMap.put("ShowDialogLayout",json.dumps(ocr_layout,ensure_ascii=False))
        hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Добавление Распознавание текста"},ensure_ascii=False))
        hashMap.put("ShowDialog","")

        
        hashMap.put("name","")
        hashMap.put("query","")
        hashMap.put("control_field","")
        hashMap.put("values_list","")
        hashMap.put("min_length","")
        hashMap.put("max_length","")
        hashMap.put("ReplaceO","")
        hashMap.put("ToUpcase","")
        hashMap.put("mesure_qty","")
        hashMap.put("OnlyNumbers","")

    elif hashMap.get("listener")=="btn_add_date":
        session["recognition_table_id"]  = -2
        hashMap.put("ShowDialogLayout",json.dumps(date_layout,ensure_ascii=False))
        hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Добавление Распознавание дат"},ensure_ascii=False))
        hashMap.put("ShowDialog","")

       
        hashMap.put("name","")
        hashMap.put("result_field","")
    
    elif hashMap.get("listener")=="btn_add_number":
        session["recognition_table_id"]  = -3
        hashMap.put("ShowDialogLayout",json.dumps(number_layout,ensure_ascii=False))
        hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Добавление Распознавание чисел"},ensure_ascii=False))
        hashMap.put("ShowDialog","")

        hashMap.put("name","")
        hashMap.put("result_field","")
        hashMap.put("count_objects","")
    
    elif hashMap.get("listener")=="btn_add_platenumbers":
        session["recognition_table_id"]  = -4
        hashMap.put("ShowDialogLayout",json.dumps(platenumber_layout,ensure_ascii=False))
        hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Добавление Распознавание автомобильных номеров"},ensure_ascii=False))
        hashMap.put("ShowDialog","")

        hashMap.put("name","")
        hashMap.put("result_field","")

    elif hashMap.get("listener")=="btn_edit_recognition" or hashMap.get("listener") == "TableDoubleClick":
        if hashMap.containsKey("selected_line_id"):
            session["recognition_table_id"]  = int(hashMap.get("selected_line_id"))
            row = session["configuration"]['ClientConfiguration']["RecognitionTemplates"][session["recognition_table_id"] ]     
            if row.get("DateRecognition") == True:
                hashMap.put("ShowDialogLayout",json.dumps(date_layout,ensure_ascii=False))
                hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Распознавание дат"},ensure_ascii=False))
                hashMap.put("ShowDialog","")

                hashMap.put("name",row.get("name"))
                hashMap.put("result_field",row.get("result_field"))
                hashMap.put("count_objects",row.get("count_objects")) 
            elif row.get("PlateNumberRecognition") == True:
                hashMap.put("ShowDialogLayout",json.dumps(platenumber_layout,ensure_ascii=False))
                hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Распознавание чисел"},ensure_ascii=False))
                hashMap.put("ShowDialog","")

                hashMap.put("name",row.get("name"))
                hashMap.put("result_field",row.get("result_field"))
                hashMap.put("count_objects",row.get("count_objects"))    
            elif row.get("NumberRecognition") == True:
                hashMap.put("ShowDialogLayout",json.dumps(number_layout,ensure_ascii=False))
                hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Распознавание автомобильных номеров"},ensure_ascii=False))
                hashMap.put("ShowDialog","")

                hashMap.put("name",row.get("name"))
                hashMap.put("result_field",row.get("result_field"))
              
            else:
                hashMap.put("ShowDialogLayout",json.dumps(ocr_layout,ensure_ascii=False))
                hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Распознавание автомобильных номеров"},ensure_ascii=False))
                hashMap.put("ShowDialog","")

                hashMap.put("name",row.get("name"))
                hashMap.put("query",row.get("query"))
                hashMap.put("control_field",row.get("control_field"))
                hashMap.put("values_list",row.get("values_list"))
                hashMap.put("ReplaceO",row.get("ReplaceO"))
                hashMap.put("ToUpcase",row.get("ToUpcase"))
                hashMap.put("mesure_qty",row.get("mesure_qty"))
                hashMap.put("OnlyNumbers",row.get("OnlyNumbers"))
                hashMap.put("max_length",row.get("max_length"))
                hashMap.put("min_length",row.get("min_length"))
          
    
    elif hashMap.get("listener") == "onResultPositive": 
        dialog_values = list_to_dict(json.loads(hashMap.get("dialog_values")))
        
        if not "RecognitionTemplates" in session["configuration"]['ClientConfiguration']:
                session["configuration"]['ClientConfiguration']["RecognitionTemplates"] = []

        
        if session["recognition_table_id"]  == -1:
            session["configuration"]['ClientConfiguration']["RecognitionTemplates"].append(
                {"name":dialog_values.get("name"),
                 "query":dialog_values.get("query"),
                 "control_field":dialog_values.get("control_field"),
                 "values_list":dialog_values.get("values_list"),
                 "ReplaceO":dialog_values.get("ReplaceO"),
                 "ToUpcase":dialog_values.get("ToUpcase"),
                 "mesure_qty":dialog_values.get("mesure_qty"),
                 "OnlyNumbers":dialog_values.get("OnlyNumbers"),
                 "max_length":dialog_values.get("max_length"),
                 "min_length":dialog_values.get("min_length")})         
        elif session["recognition_table_id"]  == -2:
            session["configuration"]['ClientConfiguration']["RecognitionTemplates"].append(
                {"name":dialog_values.get("name"),
                 "DateRecognition":  True,                 
                 "result_field":dialog_values.get("result_field"),
                 })             
        elif session["recognition_table_id"]  == -3:
            session["configuration"]['ClientConfiguration']["RecognitionTemplates"].append(
                {"name":dialog_values.get("name"),
                 "NumberRecognition":  True,                 
                 "result_field":dialog_values.get("result_field"),
                 "count_objects":dialog_values.get("count_objects"),
                 })             
        elif session["recognition_table_id"]  == -4:
            session["configuration"]['ClientConfiguration']["RecognitionTemplates"].append(
                {"name":dialog_values.get("name"),
                 "PlateNumberRecognition":  True,                 
                 "result_field":dialog_values.get("result_field"),
                 })  
        else:
            if hashMap.containsKey("selected_line_id"):

                pos = int(hashMap.get("selected_line_id"))
                row = session["configuration"]['ClientConfiguration']["RecognitionTemplates"][pos]     
                if row.get("DateRecognition") == True:
                    row["name"] = dialog_values.get("name")
                    row["result_field"] = dialog_values.get("result_field")
                elif row.get("PlateNumberRecognition") == True:
                    row["name"] = dialog_values.get("name")
                    row["result_field"] = dialog_values.get("result_field")  
                elif row.get("NumberRecognition") == True:
                    row["name"] = dialog_values.get("name")
                    row["result_field"] = dialog_values.get("result_field")        
                    row["count_objects"] = dialog_values.get("count_objects")
                else:
                    row["name"] = dialog_values.get("name")
                    row["query"] = dialog_values.get("query")
                    row["control_field"] = dialog_values.get("control_field")
                    row["values_list"] = dialog_values.get("values_list")
                    row["ReplaceO"] = dialog_values.get("ReplaceO")
                    row["ToUpcase"] = dialog_values.get("ToUpcase")
                    row["mesure_qty"] = dialog_values.get("mesure_qty")
                    row["OnlyNumbers"] = dialog_values.get("OnlyNumbers")
                    row["max_length"] = dialog_values.get("max_length")
                    row["min_length"] = dialog_values.get("min_length")
                       
          

        if hashMap.containsKey("selected_line_id"):
            hashMap.remove("selected_line_id")

        hashMap.put("RefreshScreen","")
        save_configuration(session["configuration"],hashMap)       
     

    elif hashMap.get("listener")=="btn_delete_recognition":
        
        sel_line = 'selected_line_id'
        if hashMap.containsKey(sel_line):
            session["configuration"]['ClientConfiguration']["RecognitionTemplates"].pop(int(hashMap.get(sel_line)))
            
            hashMap.put("RefreshScreen","")
            hashMap.remove(sel_line)
            save_configuration(session["configuration"],hashMap)

    
    return hashMap 

def recognition_open(hashMap,_files=None,_data=None):

    if "RecognitionTemplates" in session["configuration"]['ClientConfiguration']:
        hashMap.put("recognition_table",json.dumps(make_onefield_table(session["configuration"]['ClientConfiguration']["RecognitionTemplates"],"name","Имя"),ensure_ascii=False))
    else:    
        hashMap.put("recognition_table",json.dumps(make_onefield_table([],"name","Имя"),ensure_ascii=False))
 
    return hashMap

style_layout =  {
            "Value": "",
            "Variable": "",
            "type": "LinearLayout",
            "weight": "0",
            "height": "match_parent",
            "width": "match_parent",
            "orientation": "vertical",
            "Elements": [

                {
                    "type": "EditTextText",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Название варианта|@name",
                    "Variable": "name",
                    "gravity_horizontal": "left"
                },

                  {
                    "type": "LinearLayout",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "",
                    "Variable": "",
                    "orientation": "horizontal",
                    "Elements": [
                        {
                            "type": "SpinnerLayout",
                            "height": "wrap_content",
                            "width": "wrap_content",
                            "weight": "0",
                            "Value": "Высота|@height_elements",
                            "Variable": "height",
                            "gravity_horizontal": "left"
                        },
                        {
                            "type": "EditTextNumeric",
                            "height": "wrap_content",
                            "width": "wrap_content",
                            "weight": "0",
                            "Value": "Значение|@height_value",
                            "Variable": "height_value",
                            "gravity_horizontal": "left"
                        }
                    ],
                    "BackgroundColor": "",
                    "StrokeWidth": "",
                    "Padding": "",
                    "gravity_horizontal": "left"
                },
                {
                    "type": "LinearLayout",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "",
                    "Variable": "",
                    "orientation": "horizontal",
                    "Elements": [
                        {
                            "type": "SpinnerLayout",
                            "height": "wrap_content",
                            "width": "wrap_content",
                            "weight": "0",
                            "Value": "Ширина|@width_elements",
                            "Variable": "width",
                            "gravity_horizontal": "left"
                        },
                        {
                            "type": "EditTextNumeric",
                            "height": "wrap_content",
                            "width": "wrap_content",
                            "weight": "0",
                            "Value": "Значение|@width_value",
                            "Variable": "width_value",
                            "gravity_horizontal": "left"
                        }
                    ],
                    "BackgroundColor": "",
                    "StrokeWidth": "",
                    "Padding": "",
                    "gravity_horizontal": "left"
                },
                {
                    "type": "EditTextNumeric",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Вес|@weight",
                    "Variable": "weight",
                    "gravity_horizontal": "left",
                    "TextSize": "",
                    "NumberPrecision": "0",
                    "width_value": "50"
                },
                {
                    "type": "SpinnerLayout",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Выравнивание по горизонтали|@gravity_horizontal_elements",
                    "Variable": "gravity_horizontal",
                    "gravity_horizontal": "left"
                },
                {
                    "type": "EditTextText",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Цвет фона|@BackgroundColor",
                    "Variable": "BackgroundColor",
                    "gravity_horizontal": "left"
                },
                {
                    "type": "EditTextText",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Размер текста|@TextSize",
                    "Variable": "TextSize",
                    "gravity_horizontal": "left"
                },
                {
                    "type": "EditTextText",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Цвет текста|@TextColor",
                    "Variable": "TextColor",
                    "gravity_horizontal": "left"
                },
                {
                    "type": "CheckBox",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Жирный",
                    "Variable": "TextBold",
                    "gravity_horizontal": "left"
                },
                {
                    "type": "CheckBox",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Наклонный",
                    "Variable": "TextItalic",
                    "gravity_horizontal": "left"
                },
                {
                    "type": "EditTextNumeric",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Количество знаков|@NumberPrecision",
                    "Variable": "NumberPrecision",
                    "gravity_horizontal": "left"
                },
                {
                    "type": "CheckBox",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Использовать как класс",
                    "Variable": "use_as_class",
                    "gravity_horizontal": "left"
                }
                ,
                {
                    "type": "MultilineText",
                    "height": "wrap_content",
                    "width": "match_parent",
                    "weight": "0",
                    "Value": "@row",
                    "Variable": "row",
                    "gravity_horizontal": "left"
                }

            ]
        }




session["styles_table_id"] = -1
def styles_input(hashMap,_files=None,_data=None):

    element_base = screen_elements
  
    if hashMap.get("listener")=="btn_add_style":
        session["styles_table_id"] = -1
        hashMap.put("ShowDialogLayout",json.dumps(style_layout,ensure_ascii=False))
        hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Добавление шаблона стиля"},ensure_ascii=False))
        hashMap.put("ShowDialog","")

        
        hashMap.put("name","")
        hashMap.put("name","")


        hashMap.put("gravity_horizontal", "")
        hashMap.put("height", "")
        hashMap.put("width", "")    

        hashMap.put("BackgroundColor", "")
        hashMap.put("StrokeWidth", "")
        hashMap.put("Padding", "")
        hashMap.put("Radius", "")
        hashMap.put("height_value", "")
        hashMap.put("width_value", "")
        hashMap.put("weight", "")
        hashMap.put("BackgroundColor", "")
        hashMap.put("TextSize", "")
        hashMap.put("TextColor", "")
        hashMap.put("TextBold", "")
        hashMap.put("TextItalic", "")
        hashMap.put("NumberPrecision", "")
        hashMap.put("use_as_class", "")
        hashMap.put("row", "")
   
   
    elif hashMap.get("listener")=="btn_edit_style" or hashMap.get("listener") == "TableDoubleClick":
        if hashMap.containsKey("selected_line_id"):
            session["styles_table_id"] = int(hashMap.get("selected_line_id"))
            session["current_element"] = session["configuration"]['ClientConfiguration']["StyleTemplates"][session["styles_table_id"]]     
            
            hashMap.put("ShowDialogLayout",json.dumps(style_layout,ensure_ascii=False))
            hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Редактирование таймера"},ensure_ascii=False))
            hashMap.put("ShowDialog","")

            hashMap.put("name",session["current_element"].get("name"))

            #hashMap.put("gravity_vertical", get_synonym(element_base,current_element.get("gravity_vertical")))
            hashMap.put("gravity_horizontal", get_synonym(element_base,session["current_element"].get("gravity_horizontal")))
            
            if "height_element" in session["current_element"]:
                hashMap.put("height", get_synonym(element_base,session["current_element"].get("manual")))
            else:    
                hashMap.put("height", get_synonym(element_base,session["current_element"].get("height")))

            if "width_element" in session["current_element"]:
                hashMap.put("width", get_synonym(element_base,session["current_element"].get("manual")))
            else:    
                hashMap.put("width", get_synonym(element_base,session["current_element"].get("width")))    
            
            

            hashMap.put("BackgroundColor", session["current_element"].get("BackgroundColor",""))
            hashMap.put("StrokeWidth", session["current_element"].get("StrokeWidth",""))
            hashMap.put("Padding", session["current_element"].get("Padding",""))
            hashMap.put("Radius", session["current_element"].get("Radius",""))
            hashMap.put("height_value", session["current_element"].get("height_value",""))
            hashMap.put("width_value", session["current_element"].get("width_value",""))
            hashMap.put("weight", session["current_element"].get("weight",""))
            hashMap.put("BackgroundColor", session["current_element"].get("BackgroundColor",""))
            hashMap.put("TextSize", session["current_element"].get("TextSize",""))
            hashMap.put("TextColor", session["current_element"].get("TextColor",""))
            hashMap.put("TextBold", session["current_element"].get("TextBold",""))
            hashMap.put("TextItalic", session["current_element"].get("TextItalic",""))
            hashMap.put("NumberPrecision", session["current_element"].get("NumberPrecision",""))
            hashMap.put("use_as_class", session["current_element"].get("use_as_class",""))
            hashMap.put("row", session["current_element"].get("row",""))
            
          
    
    elif hashMap.get("listener") == "onResultPositive": 
        dialog_values = list_to_dict(json.loads(hashMap.get("dialog_values")))

        if get_key(scale_elements,dialog_values.get("width"))=="manual":
            if len(hashMap.get("width_value"))>0:
                width = int(dialog_values.get("width_value"))
            else:    
                width = 0
        else:
            width  = get_key(scale_elements,dialog_values.get("width"))

        if get_key(scale_elements,dialog_values.get("height"))=="manual":
            if len(dialog_values.get("height_value"))>0:
                height = int(dialog_values.get("height_value"))
            else:    
                height = 0
        else:
            height  = get_key(scale_elements,dialog_values.get("height"))    
        
        if not "StyleTemplates" in session["configuration"]['ClientConfiguration']:
                session["configuration"]['ClientConfiguration']["StyleTemplates"] = []

        
        if session["styles_table_id"] == -1:
            d =  {"name":dialog_values.get("name"),
                #"gravity_vertical":get_key(element_base,dialog_values.get("gravity_vertical")),
                "height":height,
                "width":width,
                "drawable":dialog_values.get("drawable"),
                "gravity_horizontal":get_key(gravity_elements,dialog_values.get("gravity_horizontal")),
                "BackgroundColor":dialog_values.get("BackgroundColor"),
                "StrokeWidth":dialog_values.get("StrokeWidth"),
                "Padding":dialog_values.get("Padding"),
                "Radius":dialog_values.get("Radius"),
                "weight":dialog_values.get("weight"),
                "TextSize":dialog_values.get("TextSize"),
                "TextColor":dialog_values.get("TextColor"),
                "TextBold":dialog_values.get("TextBold"),
                "TextItalic":dialog_values.get("TextItalic"),
                "NumberPrecision":dialog_values.get("NumberPrecision"),
                "use_as_class":dialog_values.get("use_as_class"),
                "row":dialog_values.get("row"),
 
                }
            if dialog_values.get("use_as_class")==True:
                d["style_class"] = dialog_values.get("name")
            session["configuration"]['ClientConfiguration']["StyleTemplates"].append(d)
        else:
           session["configuration"]['ClientConfiguration']["StyleTemplates"][session["styles_table_id"]]["name"] =  dialog_values.get("name")
           if dialog_values.get("use_as_class")==True:
                session["configuration"]['ClientConfiguration']["StyleTemplates"][session["styles_table_id"]]["style_class"] = dialog_values.get("name")
           
           #configuration["StyleTemplates"][recognition_table_id]['gravity_vertical'] = get_key(element_base,hashMap.get("gravity_vertical"))
           session["configuration"]['ClientConfiguration']["StyleTemplates"][session["styles_table_id"]]['gravity_horizontal'] = get_key(gravity_elements,dialog_values.get("gravity_horizontal"))
           session["configuration"]['ClientConfiguration']["StyleTemplates"][session["styles_table_id"]]['height'] = height
           session["configuration"]['ClientConfiguration']["StyleTemplates"][session["styles_table_id"]]['width'] = width
           session["configuration"]['ClientConfiguration']["StyleTemplates"][session["styles_table_id"]]['BackgroundColor'] = dialog_values.get("BackgroundColor")
           session["configuration"]['ClientConfiguration']["StyleTemplates"][session["styles_table_id"]]['StrokeWidth'] = dialog_values.get("StrokeWidth")
           session["configuration"]['ClientConfiguration']["StyleTemplates"][session["styles_table_id"]]['Padding'] = dialog_values.get("Padding")
           session["configuration"]['ClientConfiguration']["StyleTemplates"][session["styles_table_id"]]['Radius'] = dialog_values.get("Radius")
           session["configuration"]['ClientConfiguration']["StyleTemplates"][session["styles_table_id"]]['height_value'] = dialog_values.get("height_value")
           session["configuration"]['ClientConfiguration']["StyleTemplates"][session["styles_table_id"]]['width_value'] = dialog_values.get("width_value")
           session["configuration"]['ClientConfiguration']["StyleTemplates"][session["styles_table_id"]]['weight'] = dialog_values.get("weight")
           session["configuration"]['ClientConfiguration']["StyleTemplates"][session["styles_table_id"]]['TextSize'] = dialog_values.get("TextSize")
           session["configuration"]['ClientConfiguration']["StyleTemplates"][session["styles_table_id"]]['TextColor'] = dialog_values.get("TextColor")
           session["configuration"]['ClientConfiguration']["StyleTemplates"][session["styles_table_id"]]['TextBold'] = dialog_values.get("TextBold")
           session["configuration"]['ClientConfiguration']["StyleTemplates"][session["styles_table_id"]]['TextItalic'] = dialog_values.get("TextItalic")
           session["configuration"]['ClientConfiguration']["StyleTemplates"][session["styles_table_id"]]['NumberPrecision'] = dialog_values.get("NumberPrecision") 
           session["configuration"]['ClientConfiguration']["StyleTemplates"][session["styles_table_id"]]['use_as_class'] = dialog_values.get("use_as_class")
           session["configuration"]['ClientConfiguration']["StyleTemplates"][session["styles_table_id"]]['row'] = dialog_values.get("row")
                       
          

        if hashMap.containsKey("selected_line_id"):
            hashMap.remove("selected_line_id")

        hashMap.put("RefreshScreen","")  
        save_configuration(session["configuration"],hashMap)     
     

    elif hashMap.get("listener")=="btn_delete_style":
        
        sel_line = 'selected_line_id'
        if hashMap.containsKey(sel_line):
            session["configuration"]['ClientConfiguration']["StyleTemplates"].pop(int(hashMap.get(sel_line)))
            
            hashMap.put("RefreshScreen","")
            hashMap.remove(sel_line)
            save_configuration(session["configuration"],hashMap)

    
    return hashMap 

def styles_open(hashMap,_files=None,_data=None):

    hashMap.put("height_elements",captions_scale_elements)
    hashMap.put("width_elements",captions_scale_elements)
    hashMap.put("drawable_elements",";".join(icon_elements))
    hashMap.put("gravity_horizontal_elements",captions_gravity_elements)
    hashMap.put("vertical_gravity_elements",captions_vertical_gravity_elements)


    if "StyleTemplates" in session["configuration"]['ClientConfiguration']:
        hashMap.put("styles_table",json.dumps(make_onefield_table(session["configuration"]['ClientConfiguration']["StyleTemplates"],"name","Имя"),ensure_ascii=False))
    else:    
        hashMap.put("styles_table",json.dumps(make_onefield_table([],"name","Имя"),ensure_ascii=False))
 
    return hashMap

timers_layout =  {
            "Value": "",
            "Variable": "",
            "type": "LinearLayout",
            "weight": "0",
            "height": "match_parent",
            "width": "match_parent",
            "orientation": "vertical",
            "Elements": [

                {
                    "type": "EditTextText",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Ключ|@PyTimerTaskKey",
                    "Variable": "PyTimerTaskKey",
                    "gravity_horizontal": "left"
                },
                 {
                    "type": "EditTextNumeric",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Период|@PyTimerTaskPeriod",
                    "Variable": "PyTimerTaskPeriod",
                    "gravity_horizontal": "left",
                    "TextSize": "",
                    "NumberPrecision": "0",
                    "width_value": "50"
                },
              
                {
                    "type": "EditTextText",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Функция/alias|@PyTimerTaskDef",
                    "Variable": "PyTimerTaskDef",
                    "gravity_horizontal": "left"
                },
                
                {
                    "type": "CheckBox",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Buil-in",
                    "Variable": "PyTimerTaskBuilIn",
                    "gravity_horizontal": "left"
                }

            ]
        }

menu_layout =  {
            "Value": "",
            "Variable": "",
            "type": "LinearLayout",
            "weight": "0",
            "height": "match_parent",
            "width": "match_parent",
            "orientation": "vertical",
            "Elements": [

                {
                    "type": "SpinnerLayout",
                    "height": "wrap_content",
                    "width": "match_parent",
                    "weight": "0",
                    "Value": "Элемент|@main_menu_elements",
                    "Variable": "MenuItem",
                    "gravity_horizontal": "left"
                },
                 {
                    "type": "EditTextText",
                    "height": "wrap_content",
                    "width": "match_parent",
                    "weight": "0",
                    "Value": "Заголовок|@MenuTitle",
                    "Variable": "MenuTitle",
                    "gravity_horizontal": "left",
                    "TextSize": "",
                    "NumberPrecision": "0",
                    "width_value": "50"
                },
              
                {
                    "type": "EditTextNumeric",
                    "height": "wrap_content",
                    "width": "match_parent",
                    "weight": "0",
                    "Value": "ID|@MenuId",
                    "Variable": "MenuId",
                    "gravity_horizontal": "left"
                },
                
                {
                    "type": "CheckBox",
                    "height": "wrap_content",
                    "width": "match_parent",
                    "weight": "0",
                    "Value": "В тулбаре",
                    "Variable": "MenuTop",
                    "gravity_horizontal": "left"
                }

            ]
        }



session["timers_table_id"] = -1
def timers_input(hashMap,_files=None,_data=None):
  
    if hashMap.get("listener")=="btn_add_timer":
        session["timers_table_id"] = -1
        hashMap.put("ShowDialogLayout",json.dumps(timers_layout,ensure_ascii=False))
        hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Добавление таймера"},ensure_ascii=False))
        hashMap.put("ShowDialog","")
        
        hashMap.put("PyTimerTaskKey","")
        hashMap.put("PyTimerTaskDef","")
        hashMap.put("PyTimerTaskPeriod","")
        hashMap.put("PyTimerTaskBuilIn","")
  
   
    elif hashMap.get("listener")=="btn_edit_timer" or hashMap.get("listener") == "TableDoubleClick":
        if hashMap.containsKey("selected_line_id"):
            session["timers_table_id"] = int(hashMap.get("selected_line_id"))
            session["current_element"] = session["configuration"]["ClientConfiguration"]["PyTimerTask"][session["timers_table_id"]]     
            
            hashMap.put("ShowDialogLayout",json.dumps(timers_layout,ensure_ascii=False))
            hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Редактирование таймера"},ensure_ascii=False))
            hashMap.put("ShowDialog","")

            hashMap.put("PyTimerTaskKey",session["current_element"].get("PyTimerTaskKey"))
            hashMap.put("PyTimerTaskDef",session["current_element"].get("PyTimerTaskDef"))
            hashMap.put("PyTimerTaskPeriod",session["current_element"].get("PyTimerTaskPeriod"))
            hashMap.put("PyTimerTaskBuilIn",session["current_element"].get("PyTimerTaskBuilIn"))
    
    elif hashMap.get("listener") == "onResultPositive": 
        dialog_values = list_to_dict(json.loads(hashMap.get("dialog_values")))
        
        if not "PyTimerTask" in session["configuration"]["ClientConfiguration"]:
                session["configuration"]["ClientConfiguration"]["PyTimerTask"] = []
        
        if session["timers_table_id"] == -1:
            d =  {"PyTimerTaskKey":dialog_values.get("PyTimerTaskKey"),
             "PyTimerTaskDef":dialog_values.get("PyTimerTaskDef"),
             "PyTimerTaskPeriod":dialog_values.get("PyTimerTaskPeriod"),
             "PyTimerTaskBuilIn":dialog_values.get("PyTimerTaskBuilIn")
                }

            session["configuration"]["ClientConfiguration"]["PyTimerTask"].append(d)
        else:
           session["configuration"]["ClientConfiguration"]["PyTimerTask"][session["timers_table_id"]]["PyTimerTaskKey"] =  dialog_values.get("PyTimerTaskKey")
           session["configuration"]["ClientConfiguration"]["PyTimerTask"][session["timers_table_id"]]["PyTimerTaskDef"] =  dialog_values.get("PyTimerTaskDef")
           session["configuration"]["ClientConfiguration"]["PyTimerTask"][session["timers_table_id"]]["PyTimerTaskPeriod"] =  dialog_values.get("PyTimerTaskPeriod")
           session["configuration"]["ClientConfiguration"]["PyTimerTask"][session["timers_table_id"]]["PyTimerTaskBuilIn"] =  dialog_values.get("PyTimerTaskBuilIn")
                      
          

        if hashMap.containsKey("selected_line_id"):
            hashMap.remove("selected_line_id")

        hashMap.put("RefreshScreen","")  
        save_configuration(session["configuration"],hashMap)     
     

    elif hashMap.get("listener")=="btn_delete_timer":
        
        sel_line = 'selected_line_id'
        if hashMap.containsKey(sel_line):
            session["configuration"]["ClientConfiguration"]["PyTimerTask"].pop(int(hashMap.get(sel_line)))
            
            hashMap.put("RefreshScreen","")
            hashMap.remove(sel_line)
            save_configuration(session["configuration"],hashMap)

    
    return hashMap 

def timers_open(hashMap,_files=None,_data=None):

    if "PyTimerTask" in session["configuration"]["ClientConfiguration"]:
        hashMap.put("timers_table",json.dumps(make_timers_table(session["configuration"]["ClientConfiguration"]["PyTimerTask"]),ensure_ascii=False))
    else:    
        hashMap.put("timers_table",json.dumps(make_timers_table([]),ensure_ascii=False))
 
    return hashMap

module_layout =     {
            "Value": "",
            "Variable": "",
            "type": "LinearLayout",
            "weight": "0",
            "height": "match_parent",
            "width": "match_parent",
            "orientation": "vertical",
            "Elements": [
                {
                    "type": "EditTextText",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Ключ|@key",
                    "Variable": "key",
                    "gravity_horizontal": "left"
                },
                {
                    "type": "EditTextText",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "Url GitHub|@url",
                    "Variable": "url",
                    "gravity_horizontal": "left"
                },
                {
                    "type": "file",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "@file",
                    "Variable": "file"
                }
            ],
            "BackgroundColor": "",
            "StrokeWidth": "",
            "Padding": ""
   }

session["modules_table_id"] = -1
session["handlers_file_type"] = -1
def modules_input(hashMap,_files=None,_data=None):

  
    if hashMap.get("listener")=="btn_add_file":
        session["modules_table_id"]  = -1
        hashMap.put("ShowDialogLayout",json.dumps(module_layout,ensure_ascii=False))
        hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Добавление модуля"},ensure_ascii=False))
        hashMap.put("ShowDialog","")
        hashMap.put("key","")

    
    elif hashMap.get("listener") == "onResultPositive": 
        if session["modules_table_id"]  == -1:
            dialog_values = list_to_dict(json.loads(hashMap.get("dialog_values")))

            if not "PyFiles" in session["configuration"]["ClientConfiguration"]:
                    session["configuration"]["ClientConfiguration"]["PyFiles"] = []
            
            if 'base64' in dialog_values:
                

                filename,ext = os.path.splitext(dialog_values.get("file"))

                if ext[1:]=='py':
                    session["configuration"]["ClientConfiguration"]["PyFiles"].append({"PyFileKey":dialog_values.get("key"),"PyFileData":dialog_values.get("base64")}) 
                
            else:

                if len(dialog_values.get("url",""))>0:
                    session["configuration"]["ClientConfiguration"]["PyFiles"].append({"PyFileKey":dialog_values.get("key"),"PyFileLink":dialog_values.get("url")})     
                else:    
                    session["configuration"]["ClientConfiguration"]["PyFiles"].append({"PyFileKey":dialog_values.get("key")})     

        hashMap.put("RefreshScreen","")
        

    elif hashMap.get("listener")=="btn_delete_file":
        
        sel_line = 'selected_line_id'
        if hashMap.containsKey(sel_line):
            session["configuration"]["ClientConfiguration"]["PyFiles"].pop(int(hashMap.get(sel_line)))
            
            hashMap.put("RefreshScreen","")
            hashMap.remove(sel_line)

    elif hashMap.get("listener")=="btn_load_handlers" and hashMap.containsKey("handlers_file"):
        if ".py" in hashMap.get("handlers_file"):
            session["handlers_file_type"] =1
            hashMap.put("UploadFile","handlers_file")
    elif     hashMap.get("listener")=="upload_file":

        filename = hashMap.get("base_path")+os.sep+"uploads"+os.sep+ hashMap.get("filename")

        #if session["handlers_file_type"] ==1:
        if True:
            with open(filename, 'r',encoding='utf-8') as file:
                data = file.read()

            base64file  = base64.b64encode(data.encode('utf-8')).decode('utf-8') 
            session["configuration"]["ClientConfiguration"]["PyHandlers"]=base64file
    elif hashMap.get("listener")=="btn_handlers_save":        
        session["configuration"]["ClientConfiguration"]["GitHubHandlers"] = hashMap.get("handlers_url")
        session["configuration"]["ClientConfiguration"]["GitHubToken"] = hashMap.get("handlers_token")
        

        

      

    
    return hashMap 

def modules_open(hashMap,_files=None,_data=None):

    

    header1 = """<!DOCTYPE html>
<html>
<head>

</head>
<body>
<h3 style="font-size:14px; ">Самый простой способ работать с обработчиками python - pythonscript, не требует привязки к дополнительным файлам. Но если все таки требуется вести разработку во внешнем IDE то привязать внешние файлы к проекту Simple можно через GitHub</h3>
<h3 style="font-size:14px; "><u>Можно использовать GitHub приватный или публичный.</u></h3>
<ol>
  <li style="font-size:12px; ">Укажите URL основного файла обработчиков на GitHub в таком виде:
<b>https://api.github.com/repos/ваш гитхаб/ваше репо/contents/имя_файла.py</b>
</li>
  <li style="font-size:12px; ">При необходимости(если не публичный GitHub) сгенерируйте и укажите токен (Settings - Developer settings - Personal access tokens – Tokens (classic) – Generate new token)</li>
  <li style="font-size:12px; ">При необходимости дополнительных модулей укажите ключ и url файла дополнительного модуля</li>
  <li style="font-size:12px; ">После коммита изменений на GitHub при сохранении конфигурации измененные тексты модулей будут применены в конфигурации</li>
</ol>  
</body>
</html>"""
    
    hashMap.put("header1",header1)

    header2 = """<!DOCTYPE html>
<html>
<body>
 
</body>
</html>
"""

    link = WS_URL+":"+str(WSPORT)

    t = Template(header2)
    docdata = { 'url': link, 'uid': session["host_uid"] }
   


    res = t.render(docdata=docdata)

    hashMap.put("header2",res)
    hashMap.put("handlers_url",session["configuration"]["ClientConfiguration"].get("GitHubHandlers",""))
    hashMap.put("handlers_token",session["configuration"]["ClientConfiguration"].get("GitHubToken",""))
    hashMap.put("agent",session["configuration"]["ClientConfiguration"].get("agent",""))

    if "PyFiles" in session["configuration"]["ClientConfiguration"]:
        hashMap.put("modules_table",json.dumps(make_onefield_table(session["configuration"]["ClientConfiguration"]["PyFiles"],"PyFileKey","file"),ensure_ascii=False))
    else:    
        hashMap.put("modules_table",json.dumps(make_onefield_table([],"PyFileKey","file"),ensure_ascii=False))
 
    return hashMap


def layouts_open(hashMap,_files=None,_data=None):
    


 
    if "Layouts" in session["configuration"]["ClientConfiguration"]:
        hashMap.put("layouts_table",json.dumps(make_onefield_table(session["configuration"]["ClientConfiguration"]["Layouts"],"Variable","Переменная"),ensure_ascii=False))
    else:    
        hashMap.put("layouts_table",json.dumps(make_onefield_table([],"Variable","Переменная"),ensure_ascii=False))
 
    return hashMap

def layouts_input(hashMap,_files=None,_data=None):

    session["layouts_edit"] = True
 
    if hashMap.get("listener")=="btn_add_element":

        

        uid = str(uuid.uuid4().hex)
        hashMap.put("element_uid",uid)

        hashMap.put("OpenScreen",json.dumps({"process":"Контейнеры","screen":"element_form","key":uid,"reopen":True,"no_close":True},ensure_ascii=False))  
      

        hashMap.put("Show_layout_elements_table","-1")
        hashMap.put("Show_btns_table_elements","-1")
        hashMap.put("Show_layout_properties","-1")
        hashMap.put("Show_common_properties","-1")
        hashMap.put("Show_element_properties","-1")

        hashMap.put("Show_RecognitionTemplate","-1")
        hashMap.put("Show_RecognitionTemplate_div","-1")
        hashMap.put("Show_RecognitionTemplate_p","-1")

        hashMap.put("SetTitle","Новый элемент экрана - *")
        
                
        session["elements_table_id"] = -1
        session["current_element"] = None  

        session["current_parent"] = (session["current_element"],None)
        session["current_parent_dict"][uid] = session["current_parent"] 

    elif hashMap.get("listener")=="btn_edit_element" or hashMap.get("listener") == "TableDoubleClick":
        
        if hashMap.containsKey("selected_line_id"):
            session["elements_table_id"] = int(hashMap.get("selected_line_id"))
            row = session["configuration"]["ClientConfiguration"]["Layouts"][session["elements_table_id"]]
            
            if not 'uid' in row:
                row['uid'] = str(uuid.uuid4().hex)
            
            hashMap.put("OpenScreen",json.dumps({"process":"Контейнеры","screen":"element_form","key":row['uid'],"reopen":True,"no_close":True},ensure_ascii=False))  
            #current_screen_name = row.get("Name")
            #hashMap.put("screen_name",current_screen_name)
            hashMap.put("SetTitle",row.get("type"))

            hashMap.put("element_uid",row.get("uid"))

            #parent_elelments_element = current_element

            session["current_parent"] = (row,None)
            session["current_parent_dict"][row['uid']] = session["current_parent"]

            session["current_element"] = row     

            hashMap.remove("selected_line_id")  

    elif hashMap.get("listener")=="btn_delete_element":
        sel_line = 'selected_line_id'
        if hashMap.containsKey(sel_line):
                session["configuration"]["ClientConfiguration"]["Layouts"].pop(int(hashMap.get(sel_line)))
                hashMap.put("RefreshScreen","")
                hashMap.remove(sel_line)    

     

            


    return hashMap


def info_on_start(hashMap,_files=None,_data=None):


    htmlstring = """


<p>Этот конструктор предназначен для создания конфигураций для SimpleUI(Android устройства) и SimpleWEB (десктоп) и представляет из себя конфигурацию на SimpleWEB. </p>
<div style="background-color: Azure;  padding-top: 10px;  padding-bottom: 10px;">

<p><font style="font-size: 20px !important;">GitHub этого конструктора <a href="https://github.com/dvdocumentation/web_simple_editor" target="_blank">https://github.com/dvdocumentation/web_simple_editor </a></font></p>

<p><font style="font-size: 20px !important;">GitHub SimpleWEB <a href="https://github.com/dvdocumentation/simpleweb" target="_blank">https://github.com/dvdocumentation/simpleweb</a></font></p>

<p><font style="font-size: 20px !important;">Статья на Habr о Simple <a href="https://habr.com/ru/articles/720610/">https://habr.com/ru/articles/720610/</a></font></p> 

<p><font style="font-size: 20px !important;">Телеграмм канал <a href="https://t.me/devsimpleui" target="_blank">https://t.me/devsimpleui</a></font></p>

<p><font style="font-size: 20px !important;">Сайт <a href="http://simpleui.ru/" target="_blank">http://simpleui.ru/</a></font></p>

<p><font style="font-size: 20px !important;">Мои статьи на Инфостарт <a href="https://infostart.ru/profile/129563/public/" target="_blank">https://infostart.ru/profile/129563/public/</a></font></p>

</div>

<p>(c) Dmitry Votontsov, 2023 </p>

"""




    
    hashMap.put("html",htmlstring)
    
 
    return hashMap


def source_code(hashMap,_files=None,_data=None):

    
    if "configuration_file" in session:
        source = json.dumps(session["configuration_file"],ensure_ascii=False,indent=4,separators=(',', ': '))
    else:    
        source = json.dumps(session["configuration"],ensure_ascii=False,indent=4,separators=(',', ': '))

    #<body><span style="white-space: pre-wrap">"""+source+"""</span></body>
    edit =  '<code-input required id="source_code"  style="resize: both; overflow: hidden; width: 100%;" lang="JSON">'+source+'</code-input>'
    htmlstring = """
    <!DOCTYPE html>
<html>
<body> """+edit+""" </body>
</html>
"""
    
    hashMap.put("html", htmlstring)  

    return hashMap

def source_code_save(hashMap,_files=None,_data=None):

    source = hashMap.get("source_code")

    try:
        session["configuration"] = json.loads(source)
        session["configuration_file"] = session["configuration"]

        hashMap.put("configuration",json.dumps(session["configuration"],ensure_ascii=False))
        hashMap.put("set_configuration","")
        
        
        if "host_uid" in session["configuration"]["ClientConfiguration"]:
            session["host_uid"] = session["configuration"]["ClientConfiguration"]["host_uid"]
        else:
            session["host_uid"] =  str(uuid.uuid4().hex)  
            session["configuration"]["ClientConfiguration"]["host_uid"] = session["host_uid"]

        session["processes_table"] = session["configuration"]["ClientConfiguration"]["Processes"] 

        save_configuration(session["configuration"],hashMap,True)

        hashMap.put("toast", "Конфигурация обновлена")  
    except:
        hashMap.put("toast", "Ошибка обновления!")  

    return hashMap

def menu_open(hashMap,_files=None,_data=None):
    hashMap.put("main_menu_elements",";".join(main_menu_elements))

    if "MainMenu" in session["configuration"]["ClientConfiguration"]:
        hashMap.put("menu_table",json.dumps(make_menu_table(session["configuration"]["ClientConfiguration"]["MainMenu"]),ensure_ascii=False))
    else:    
        hashMap.put("menu_table",json.dumps(make_menu_table([]),ensure_ascii=False))
 
    return hashMap

session["menu_table_id"] = -1
def menu_input(hashMap,_files=None,_data=None):

  
  
    if hashMap.get("listener")=="btn_add_menu":
        session["menu_table_id"] = -1
        hashMap.put("ShowDialogLayout",json.dumps(menu_layout,ensure_ascii=False))
        hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Добавление меню"},ensure_ascii=False))
        hashMap.put("ShowDialog","")
        
        hashMap.put("MenuItem","")
        hashMap.put("MenuTitle","")
        hashMap.put("MenuId","")
        hashMap.put("MenuTop","")
  
   
    elif hashMap.get("listener")=="btn_edit_menu" or hashMap.get("listener") == "TableDoubleClick":
        if hashMap.containsKey("selected_line_id"):
            session["menu_table_id"] = int(hashMap.get("selected_line_id"))
            session["current_element"] = session["configuration"]["ClientConfiguration"]["MainMenu"][session["menu_table_id"]]     
            
            hashMap.put("ShowDialogLayout",json.dumps(menu_layout,ensure_ascii=False))
            hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Редактирование меню"},ensure_ascii=False))
            hashMap.put("ShowDialog","")

            hashMap.put("MenuItem",session["current_element"].get("MenuItem"))
            hashMap.put("MenuTitle",session["current_element"].get("MenuTitle"))
            hashMap.put("MenuId",session["current_element"].get("MenuId"))
            hashMap.put("MenuTop",session["current_element"].get("MenuTop"))
    
    elif hashMap.get("listener") == "onResultPositive": 
        dialog_values = list_to_dict(json.loads(hashMap.get("dialog_values")))
        
        if not "MainMenu" in session["configuration"]["ClientConfiguration"]:
                session["configuration"]["ClientConfiguration"]["MainMenu"] = []
        
        if session["menu_table_id"] == -1:
            d =  {"MenuItem":dialog_values.get("MenuItem"),
             "MenuTitle":dialog_values.get("MenuTitle"),
             "MenuId":dialog_values.get("MenuId"),
             "MenuTop":dialog_values.get("MenuTop")
                }

            session["configuration"]["ClientConfiguration"]["MainMenu"].append(d)
        else:
           session["configuration"]["ClientConfiguration"]["MainMenu"][session["menu_table_id"]]["MenuItem"] =  dialog_values.get("MenuItem")
           session["configuration"]["ClientConfiguration"]["MainMenu"][session["menu_table_id"]]["MenuTitle"] =  dialog_values.get("MenuTitle")
           session["configuration"]["ClientConfiguration"]["MainMenu"][session["menu_table_id"]]["MenuId"] =  dialog_values.get("MenuId")
           session["configuration"]["ClientConfiguration"]["MainMenu"][session["menu_table_id"]]["MenuTop"] =  dialog_values.get("MenuTop")
                      
          

        if hashMap.containsKey("selected_line_id"):
            hashMap.remove("selected_line_id")

        hashMap.put("RefreshScreen","")  
        save_configuration(session["configuration"],hashMap)     
     

    elif hashMap.get("listener")=="btn_delete_memu":
        
        sel_line = 'selected_line_id'
        if hashMap.containsKey(sel_line):
            session["configuration"]["ClientConfiguration"]["MainMenu"].pop(int(hashMap.get(sel_line)))
            
            hashMap.put("RefreshScreen","")
            hashMap.remove(sel_line)
            save_configuration(session["configuration"],hashMap)

    
    return hashMap 

def load_configurations_github(hashMap):
    t = {
    "type": "table",
    "textsize": "25",
    "hidecaption": "false",
    "useDatatable": "true",
    "columns": [
       
        {
        "name": "name",
        "header": "название",
        "weight": "1",
        "gravity":"left"
    },
        {
        "name": "path",
        "header": "Путь",
        "weight": "1",
        "gravity":"left"
    }

    ]
    }  

    folder = ""    
    if hashMap.containsKey("ui_folder"):
        folder = hashMap.get("ui_folder")

    repo = hashMap.get("ui_repo")

    url="https://api.github.com/repos/"+repo+"/contents/"+folder

    if hashMap.get("ui_token")!="":
        data = requests.get(url, headers = {"Authorization": "token "+hashMap.get("ui_token")}).json()
    else:    
        data = requests.get(url).json()

    _table = []
    if isinstance(data,list):
        for f in data:
            if ".ui" in f.get("path"):
                _table.append({"name":f.get("name"),"path":f.get("path")})


   

    t['rows'] = _table

    return t


def user_open(hashMap,_files=None,_data=None):
   
   
    if hashMap.containsKey("_cookies"):
        jcookies = json.loads(hashMap.get("_cookies"))
        hashMap.put("ui_to_github", jcookies.get("ui_to_github", "false"))
        hashMap.put("ui_repo", jcookies.get("ui_repo", ""))
        hashMap.put("ui_token", jcookies.get("ui_token", ""))
        hashMap.put("ui_branch", jcookies.get("ui_branch", ""))
        hashMap.put("ui_folder", jcookies.get("ui_folder", ""))

        hashMap.put("github_table", json.dumps(load_configurations_github(hashMap),ensure_ascii=False))
   
    else:
        hashMap.put("GetCookies","")
        hashMap.put("toast","Переоткройте вкладку")

    return hashMap

def user_input(hashMap,_files=None,_data=None):

    if hashMap.get("listener") == "btn_save":

        jcookies = [{"key":"ui_to_github", "value":str(hashMap.get("ui_to_github")),"expires":30},{"key":"ui_repo", "value":str(hashMap.get("ui_repo")),"expires":30},{"key":"ui_token", "value":str(hashMap.get("ui_token")),"expires":30},
                    {"key":"ui_branch", "value":str(hashMap.get("ui_branch")),"expires":30},{"key":"ui_folder", "value":str(hashMap.get("ui_folder")),"expires":30}]
        
        hashMap.put("SetCookie", json.dumps(jcookies,ensure_ascii=False))

        _jcookies = {
            "ui_to_github":str(hashMap.get("ui_to_github")),
            "ui_repo":str(hashMap.get("ui_repo")),
            "ui_token":str(hashMap.get("ui_token")),
            "ui_branch":str(hashMap.get("ui_branch")),
            "ui_folder":str(hashMap.get("ui_folder")),
        }   

        hashMap.put("_cookies", json.dumps(_jcookies,ensure_ascii=False))
    elif hashMap.get("listener") == "btn_load":
        hashMap.put("GetCookies","")
        hashMap.put("RefreshScreen","")

    elif hashMap.get("listener") == "btn_reload":
        hashMap.put("github_table", json.dumps(load_configurations_github(hashMap),ensure_ascii=False))
        hashMap.put("RefreshScreen","1")
    elif hashMap.get("listener") == "btn_set_configuration":  
         if hashMap.containsKey("selected_line_id"):
            table_id = int(hashMap.get("selected_line_id"))
            jtable = json.loads(hashMap.get("github_table"))
            current_element = jtable["rows"][table_id]   

            path = current_element["path"]

            url="https://api.github.com/repos/"+hashMap.get("ui_repo")+"/contents/"+path

            if hashMap.get("ui_token")!="":
                req = requests.get(url, headers = {"Authorization": "token "+hashMap.get("ui_token")}).json()
            else:    
                req = requests.get(url).json()

            content = base64.b64decode(req['content']).decode("utf-8")
            session["filename"] =hashMap.get("base_path")+os.sep+"uploads"+os.sep+ current_element["name"]
            session["filename_base"] = current_element["name"]
            
            session["configuration"] = json.loads(content)

            hashMap.put("configuration",json.dumps(session["configuration"],ensure_ascii=False))
            hashMap.put("filename",current_element["name"])
            hashMap.put("filename_base",current_element["name"])
            hashMap.put("set_configuration","")
            
            session["configuration"]["ClientConfiguration"]["ConfigurationFileName"] = session["filename_base"]

            if "host_uid" in session["configuration"]["ClientConfiguration"]:
                session["host_uid"] = session["configuration"]["ClientConfiguration"]["host_uid"]
            else:
                session["host_uid"] =  str(uuid.uuid4().hex)  
                session["configuration"]["ClientConfiguration"]["host_uid"] = session["host_uid"]
    
            session["processes_table"] = session["configuration"]["ClientConfiguration"]["Processes"] 

            save_configuration(session["configuration"],hashMap,True)
            hashMap.put("RefreshScreen","")



    return hashMap


#Отладка
def debug_open(hashMap,_files=None,_data=None):
    
    if 'sid' in session:
        img = qrcode.make(json.dumps({"url": WS_URL+":"+str(WSPORT)+"/debug","sid":session["sid"]})) 
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        hashMap.put("qr",img_str)         

    return hashMap

def debug_next(hashMap,_files=None,_data=None):
    hashMap.put("next_"+session["sid"],"")   

    return hashMap
def debug_add(hashMap,_files=None,_data=None):
    hashMap.put("TableAddRow","StackTable")   

    return hashMap
def debug_edit(hashMap,_files=None,_data=None):
    jtable = json.loads(hashMap.get("StackTable"))
    jselline = json.loads(hashMap.get("selected_line"))
    
    if hashMap.get("selected_line_id") == "-1":
        jtable["rows"].append(jselline)
    else:    
        jtable["rows"][int(hashMap.get("selected_line_id"))]["value"] = jselline.get("value")
        jtable["rows"][int(hashMap.get("selected_line_id"))]["variable"] = jselline.get("variable")
    hashMap.put("StackTable",json.dumps(jtable,ensure_ascii=False)) 

    hashMap.put("RefreshScreen","")  

    return hashMap


#Векторный редактор
class Cell():
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0
    color=None
    fillcolor=None
    address=""

class Line():
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0
    color=None
    strock_size=None
    def __init__(self,x1,y1,x2,y2,strock_size):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.strock_size = strock_size

class Label():
    x = 0
    y = 0
    text = 0
    size = 0
    
    def __init__(self,x,y,text,size):
        self.x = x
        self.y = y
        self.text = text
        self.size = size        
      
class Rect():
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0
    color=None
    strock_size=None
    def __init__(self,x1,y1,x2,y2,strock_size):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.strock_size = strock_size  

class Row():
    def __init__(self, cells, num_rows, num_columns,cell_size,x,y):
        self.cells = cells
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.cell_size = cell_size
        self.x = x
        self.y = y


session["current_cell"] = None
session["current_line"] = None
session["current_rect"] = None
session["current_text"] = None
session["draw_mode"] = ""

CANVAS_H = 500
CANVAS_W = 500
GRIDSIZE = 21

STROCK_SIZE = 3

RATIO_STROCK = 60
RATIO_TEXT_SIZE = 5

cellsize = 25
rows = []
labels = []
rectangles = []
vectors = []

def redraw(hashMap):
    global cells

    draw_array = []

    


    for r in session["rows"]:
        for cell in r.cells :
            draw_array.append({"type":"cell","x1":cell.x1,"y1":cell.y1,"x2":cell.x2,"y2":cell.y2, "label":cell.address, "fill_color":"#c6f2f5"})

    for el in session["vectors"]:
        draw_array.append({"type":"line","x1":el.x1,"y1":el.y1,"x2":el.x2,"y2":el.y2, "color":"#0a1a45","strock_size":el.strock_size})        

    #hashMap.put("SetCanvas",json.dumps({"map":{"height":CANVAS_H,"width":CANVAS_W,"draw":draw_array}}))
    for el in session["rectangles"]:
        
        draw_array.append({"type":"rect","x1":el.x1,"y1":el.y1,"x2":el.x2,"y2":el.y2, "color":"#0a1a45","strock_size":el.strock_size,"fill_color":"#ffffff"})        
   
    for el in session["labels"]:
        draw_array.append({"type":"text","x":el.x,"y":el.y,"text":el.text, "color":"#0a1a45","size":el.size})        

    hashMap.put("SetCanvas",json.dumps({"map":{"height":CANVAS_H,"width":CANVAS_W,"draw":draw_array}}))

    return hashMap

def canvas_on_start(hashMap,_files=None,_data=None):
    hashMap.put("InitCanvas",json.dumps({"map":{"height":CANVAS_H,"width":CANVAS_W}}))
    hashMap.put("size","3")

    if hashMap.containsKey("sug_reload"):
        hashMap.remove("sug_reload")
        hashMap = redraw(hashMap)
    else:    
        session["cells"] = []
        session["rows"] = []
        session["labels"] = []
        session["rectangles"] = []
        session["vectors"] = []
    
    

    session["current_row"] = None
    session["current_line"] = None
    session["current_rect"] = None
    session["current_text"] = None
    
    
    

    return hashMap


dialog_row = {
                        "Value": "",
                        "Variable": "",
                        "type": "LinearLayout",
                        "weight": "0",
                        "height": "match_parent",
                        "width": "match_parent",
                        "orientation": "vertical",
                        "Elements": [
                            {
                                "type": "EditTextNumeric",
                                "height": "wrap_content",
                                "width": "match_parent",
                                "weight": "0",
                                "Value": "Количество столбцов|@columns",
                                "Variable": "columns",
                                "gravity_horizontal": "left"
                            },
                            {
                                "type": "EditTextNumeric",
                                "height": "wrap_content",
                                "width": "match_parent",
                                "weight": "0",
                                "Value": "Количество строк|@rows",
                                "Variable": "rows",
                                "gravity_horizontal": "left"
                            }
                            
                        ],
                        "BackgroundColor": "#fcd39d",
                        "StrokeWidth": "2",
                        "Padding": ""
        }

dialog_cell = {
                        "Value": "",
                        "Variable": "",
                        "type": "LinearLayout",
                        "weight": "0",
                        "height": "match_parent",
                        "width": "match_parent",
                        "orientation": "vertical",
                        "Elements": [
                            {
                                "type": "EditTextText",
                                "height": "wrap_content",
                                "width": "match_parent",
                                "weight": "0",
                                "Value": "Имя ячейки|@cell",
                                "Variable": "cell",
                                "gravity_horizontal": "left"
                            }
                            
                        ],
                        "BackgroundColor": "",
                        "StrokeWidth": "",
                        "Padding": ""
        }

dialog_text = {
                        "Value": "",
                        "Variable": "",
                        "type": "LinearLayout",
                        "weight": "0",
                        "height": "match_parent",
                        "width": "match_parent",
                        "orientation": "vertical",
                        "Elements": [
                            {
                                "type": "EditTextText",
                                "height": "wrap_content",
                                "width": "match_parent",
                                "weight": "0",
                                "Value": "Текст надписи|@text",
                                "Variable": "text",
                                "gravity_horizontal": "left"
                            }
                            
                        ],
                        "BackgroundColor": "",
                        "StrokeWidth": "",
                        "Padding": ""
        }



def mouse_input(hashMap,_files=None,_data=None):
    global rows
    global vectors
    global labels
    global rectangles

    data = json.loads(hashMap.get("map"))

    if len(rows)>0:
        for r in rows:
            session['rows'].append(r)
        rows = []
    if len(vectors)>0:
        for r in vectors:
            session['vectors'].append(r)
        vectors = []    
    if len(labels)>0:
        for r in labels:
            session['labels'].append(r)
        labels = [] 
    if len(rectangles)>0:
        for r in rectangles:
            session['rectangles'].append(r)
        rectangles = []  
    
    
    if data.get("type") == "mouseDown":
        if "draw_mode" in session:     
            if session["draw_mode"] == "address":
                session["current_row"]=None
                session["current_cell"]=None
                for r in session["rows"]:
                    for cell in r.cells :
                        if (data.get("x")>=cell.x1 and data.get("x")<=cell.x2) and (data.get("y")>=cell.y1 and data.get("y")<=cell.y2):
                            session["current_row"] = r
                            session["current_cell"] = cell
                            break
                
                if session["current_row"]!=None:
                    hashMap.put("ShowDialogLayout",json.dumps(dialog_cell,ensure_ascii=False))
                    hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Редактировнаие ячейки"},ensure_ascii=False))
                    hashMap.put("ShowDialog","") 

                    hashMap.put("StopCanvasEvents","")     

            elif session["draw_mode"] == "row":
                session["current_row"]=None
                for r in session["rows"]:
                    for cell in r.cells :
                        if (data.get("x")>=cell.x1 and data.get("x")<=cell.x2) and (data.get("y")>=cell.y1 and data.get("y")<=cell.y2):
                            session["current_row"] = r
                            break
                if session["current_row"]==None:
                    r = generate_row(data.get("x"),data.get("y"),STROCK_SIZE*RATIO_TEXT_SIZE,int(hashMap.get("rows")),int(hashMap.get("columns"))) 
                    session["rows"].append(r)   
                    



                
            elif session["draw_mode"] == "line": 
                for r in session["vectors"]:
                        if (data.get("x")>=min(r.x1,r.x2) and data.get("x")<=max(r.x2,r.x1)) and (data.get("y")>=min(r.y1,r.y2) and data.get("y")<=max(r.y2,r.y1)):
                            session["current_line"] = r
                            break
                if session["current_line"]==None:
                    r = Line(data.get("x"),data.get("y"),data.get("x"),data.get("y"),STROCK_SIZE)
                    session["vectors"].append(r)
                    session["current_line"]=r
            elif session["draw_mode"] == "rect": 
                session["current_rect"]=None
                for r in session["rectangles"]:
                        if (data.get("x")>=r.x1 and data.get("x")<=r.x2) and (data.get("y")>=r.y1 and data.get("y")<=r.y2):
                            session["current_rect"] = r
                            #session["edit_mode"] = True
                            break
                if session["current_rect"]==None:
                    session["edit_mode"] = False
                    r = Rect(data.get("x"),data.get("y"),data.get("x"),data.get("y"),STROCK_SIZE)
                    session["rectangles"].append(r)
                    session["current_rect"]=r        
            elif session["draw_mode"] == "text": 
                session["current_text"]=None
                for r in session["labels"]:
                        if (data.get("x")>=(r.x-5) and data.get("x")<=(r.x+10)) and (data.get("y")>=(r.y-5) and data.get("y")<=(r.y+5)):
                            session["current_text"] = r
                            session["edit_mode"] = True
                            break
                if session["current_text"]==None:
                    session["edit_mode"] = False
                    r = Label(data.get("x"),data.get("y"),session["label_text"],STROCK_SIZE*RATIO_TEXT_SIZE)
                    session["labels"].append(r)
                    session["current_text"]=r         
            elif session["draw_mode"] == "delete":
                for r in session["rows"]:
                    for cell in r.cells :
                        if (data.get("x")>=cell.x1 and data.get("x")<=cell.x2) and (data.get("y")>=cell.y1 and data.get("y")<=cell.y2):
                            session["rows"].remove(r)    
                            break    
                for r in session["vectors"]:
                        if (data.get("x")>=min(r.x1,r.x2) and data.get("x")<=max(r.x2,r.x1)) and (data.get("y")>=min(r.y1,r.y2) and data.get("y")<=max(r.y2,r.y1)):
                            session["vectors"].remove(r)    
                            break   
                for r in session["rectangles"]:
                        if (data.get("x")>=(r.x1-5) and data.get("x")<=(r.x2+5)) and (data.get("y")>=(r.y1-5) and data.get("y")<=(r.y2+5)):
                            session["rectangles"].remove(r)
                            break   
                for r in session["labels"]:
                        if (data.get("x")>=(r.x-5) and data.get("x")<=(r.x+10)) and (data.get("y")>=(r.y-5) and data.get("y")<=(r.y+5)):
                            session["labels"].remove(r)
                            break                    
            hashMap = redraw(hashMap)
    elif data.get("type") == "mouseMove" and  (not hashMap.get("AddressMode")==True) : 
        if "draw_mode" in session:
            if session["draw_mode"] == "row":   
                if session["current_row"]!=None:
                    session["current_row"] = update_row(session["current_row"],data.get("x"),data.get("y"))
                    hashMap = redraw(hashMap)
            elif session["draw_mode"] == "line":
                if session["current_line"]!=None:     
                    session["current_line"].x2 =data.get("x")
                    session["current_line"].y2 =data.get("y")
            
                    hashMap = redraw(hashMap)
            elif session["draw_mode"] == "rect":
                
                if session["current_rect"]!=None:  
                    print(session["edit_mode"])
                    if session["edit_mode"] == True:
                        offsetx = session["current_rect"].x1 - data.get("x")
                        offsety = session["current_rect"].y1 - data.get("y")

                        #session["current_rect"].x1 =  data.get("x")    
                        #session["current_rect"].y1 =  data.get("y")    
                        
                        session["current_rect"].x1 -=offsetx
                        session["current_rect"].x2 -=offsetx
                        session["current_rect"].y1 -=offsety
                        session["current_rect"].y2 -=offsety

                    else:      
                    
                        session["current_rect"].x2 =data.get("x")
                        session["current_rect"].y2 =data.get("y")
            
                    hashMap = redraw(hashMap)
            elif session["draw_mode"] == "text":
                if session["current_text"]!=None:  
                    if session["edit_mode"] == True:
                                            
                        session["current_text"].x =data.get("x")
                        session["current_text"].y =data.get("y")
                    

                    else:      
                        session["current_text"].x =data.get("x")
                        session["current_text"].y =data.get("y")
            
                    hashMap = redraw(hashMap)        

    elif data.get("type") == "mouseUp" and (not hashMap.get("AddressMode")==True):
        if "draw_mode" in session:
            if session["draw_mode"] == "row": 
                session["current_row"]=None 
            if session["draw_mode"] == "line": 
                session["current_line"]=None       
            if session["draw_mode"] == "rect": 
                session["current_rect"]=None 
            if session["draw_mode"] == "text": 
                session["current_text"]=None 
                                    
            
         

    return hashMap

def generate_row(x,y,cellsize,num_rows,num_columns):
    _cells = []
    
    caddr = 0
    offset_x = 0
    for j in range(num_columns):
        offset_y = 0
        for i in range(num_rows):
            c = Cell()
            c.x1 = x+offset_x
            c.x2 = c.x1 + cellsize
            c.y1 = y+offset_y
            c.y2 = c.y1 + cellsize
            caddr+=1
            c.address = str(caddr)

            _cells.append(c)

            offset_y+=cellsize
        offset_x +=cellsize

    r = Row(_cells,num_rows,num_columns,cellsize,x,y)  

    return r 

def update_row(r,x,y):
    offsetx = r.x -x
    offsety = r.y -y

    r.x = x
    r.y = y
    
    for c in r.cells:
        c.x1 -=offsetx
        c.x2 -=offsetx
        c.y1 -=offsety
        c.y2 -=offsety

    return r 
def update_row_cellsize(r,x,y,cellsize):
    
    ii=0
    offset_x = 0
    for j in range(r.num_columns):
        offset_y = 0
        for i in range(r.num_rows):
            c = r.cells[ii]
            ii+=1
            c.x1 = x+offset_x
            c.x2 = c.x1 + cellsize
            c.y1 = y+offset_y
            c.y2 = c.y1 + cellsize

            offset_y+=cellsize
        offset_x +=cellsize

    return r 

def cell_input(hashMap,_files=None,_data=None):
    global rows
    global vectors
    global labels
    global rectangles
    global GRIDSIZE
    global STROCK_SIZE

    if len(rows)>0:
        for r in rows:
            session['rows'].append(r)
        rows = []
    if len(vectors)>0:
        for r in vectors:
            session['vectors'].append(r)
        vectors = []    
    if len(labels)>0:
        for r in labels:
            session['labels'].append(r)
        labels = [] 
    if len(rectangles)>0:
        for r in rectangles:
            session['rectangles'].append(r)
        rectangles = []         
    
    if hashMap.get("listener") == "canvas_mouse_event":
        return hashMap    

    if hashMap.get("listener") == "btn_row":
        session["draw_mode"] = "row"

        if not hashMap.containsKey("rows"):
            hashMap.put("rows","1")
            hashMap.put("columns","1")

        hashMap.put("ShowDialogLayout",json.dumps(dialog_row,ensure_ascii=False))
        hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Добавления ряда ячеек"},ensure_ascii=False))
        hashMap.put("ShowDialog","") 

        hashMap.put("StopCanvasEvents","") 
    if hashMap.get("listener") == "btn_addr":
        session["draw_mode"] = "address"    
    if hashMap.get("listener") == "btn_line":
        session["draw_mode"] = "line"    
    if hashMap.get("listener") == "btn_rect":
        session["draw_mode"] = "rect"    
    if hashMap.get("listener") == "btn_text":
        session["label_text"] = ""
        session["draw_mode"] = "text"



        hashMap.put("ShowDialogLayout",json.dumps(dialog_text,ensure_ascii=False))
        hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Ввод текста"},ensure_ascii=False))
        hashMap.put("ShowDialog","") 

        hashMap.put("StopCanvasEvents","") 
    if hashMap.get("listener") == "btn_delete":
        session["draw_mode"] = "delete"     

    if hashMap.get("listener") == "size":
        STROCK_SIZE=int(hashMap.get("size"))
        if session["draw_mode"] == "text":
            if len(session["labels"])>0:
                session["labels"][len(session["labels"])-1].size = STROCK_SIZE*RATIO_TEXT_SIZE
                hashMap = redraw(hashMap)
        elif session["draw_mode"] == "line":
            if len(session["vectors"])>0:
                session["vectors"][len(session["vectors"])-1].strock_size = STROCK_SIZE
                hashMap = redraw(hashMap)
        elif session["draw_mode"] == "rect":
            if len(session["rectangles"])>0:
                session["rectangles"][len(session["rectangles"])-1].strock_size = STROCK_SIZE
                hashMap = redraw(hashMap)  
        elif session["draw_mode"] == "row":
            if len(session["rows"])>0:
                r = session["rows"][len(session["rows"])-1]
                r = update_row_cellsize(r,r.x,r.y,STROCK_SIZE*RATIO_TEXT_SIZE)
               
                hashMap = redraw(hashMap)                

    if hashMap.get("listener") == "onResultPositive": 
        if session["draw_mode"] == "address":
            dialog_values = list_to_dict(json.loads(hashMap.get("dialog_values")))
            
            session["current_cell"].address = dialog_values.get("cell")
            hashMap = redraw(hashMap)
            session["current_cell"] = None
            hashMap.put("StartCanvasEvents","") 
        if session["draw_mode"] == "row":
            


            dialog_values = list_to_dict(json.loads(hashMap.get("dialog_values")))
            hashMap.put("rows",str(dialog_values.get("rows")))
            hashMap.put("columns",str(dialog_values.get("columns")))
            hashMap.put("StartCanvasEvents","") 
            
        if session["draw_mode"] == "text":
            dialog_values = list_to_dict(json.loads(hashMap.get("dialog_values")))    
            session["label_text"] = dialog_values.get("text")

    elif hashMap.get("listener") == 'btn_upload':
        id = "sug_file"
        

        hashMap.put("UploadFile",id)
    elif hashMap.get("listener") == 'btn_new':
        hashMap.put("SetValuesEdit",json.dumps([{"file_h":"1050"},{"file_w":"1900"},{"size":"1"}],ensure_ascii=False))    
        session["rows"] = []
        session["vectors"] = []
        session["rectangles"] = []
        session["labels"] = []
        session["cells"] = []
        rows = []
        vectors = []
        labels = []
        rectangles = []

        hashMap.put("InitCanvas",json.dumps({"map":{"height":CANVAS_H,"width":CANVAS_W}}))
        

        
            
    elif hashMap.get("listener") == "upload_file":    
        session["rows"] = []
        session["vectors"] = []
        session["rectangles"] = []
        session["labels"] = []
        session["cells"] = []
        rows = []
        vectors = []
        labels = []
        rectangles = []


        session["filenamesug"] =hashMap.get("base_path")+os.sep+"uploads"+os.sep+ hashMap.get("filename")
        session["filenamesug_base"] = hashMap.get("filename")[21:]
        with open(session["filenamesug"],encoding="utf-8") as conf_file:
            jsug = json.load(conf_file)
            file_w = jsug.get("columncount")*jsug.get("gridsize")
            file_h = jsug.get("rowcount")*jsug.get("gridsize")

            hashMap.put("file_w",str(file_w))
            hashMap.put("file_h",str(file_h))



            
            hashMap.put("SetValuesEdit",json.dumps([{"file_h":hashMap.get("file_h")},{"file_w":hashMap.get("file_w")}],ensure_ascii=False))


            ratio = CANVAS_H/max(file_w,file_h)

            GRIDSIZE = jsug.get("gridsize")

            if 'rows' in jsug:
                jrows = json.loads(jsug['rows'])
                for obj in jrows['dataList']:
                    firstcell =  obj['cells'][0]
                    _cells = []
                   
                    for cell in obj['cells']:
                        c = Cell()
                        c.x1 = int(cell["x1"]*ratio)
                        c.x2 = int(cell["x2"]*ratio)
                        c.y1 = int(cell["y1"]*ratio)
                        c.y2 = int(cell["y2"]*ratio)
                        c.address = cell.get("address","")

                        _cells.append(c)

                    r = Row(_cells,obj['count_cells_in_row'],obj['count_columns'],int(firstcell['size']*ratio),int(firstcell['x1']*ratio),int(firstcell['y1']*ratio)) 
                    session["rows"].append(r)
                    rows.append(r)
            if 'vectors' in jsug:
                jelements = json.loads(jsug['vectors'])
                for obj in jelements['dataList']:
                    l =  Line(int(obj.get("x1")*ratio),int(obj.get("y1")*ratio),int(obj.get("x2")*ratio),int(obj.get("y2")*ratio),int(obj.get("strock_size")/RATIO_STROCK))
                    vectors.append(l) 
                    session['vectors'].append(l)
            if 'labels' in jsug:
                jelements = json.loads(jsug['labels'])
                for obj in jelements['dataList']:
                    l =  Label(int(obj.get("x")*ratio),int(obj.get("y")*ratio),obj.get("text"), int(obj.get("size")/RATIO_TEXT_SIZE))
                    labels.append(l)
                    session["labels"].append(l)                       
            if 'rects' in jsug:
                jelements = json.loads(jsug['rects'])
                for obj in jelements['dataList']: 
                    r = Rect(int(obj.get("x1")*ratio),int(obj.get("y1")*ratio),int(obj.get("x2")*ratio),int(obj.get("y2")*ratio),int(obj.get("strock_size")/RATIO_STROCK))
                    rectangles.append(r)                       
                    session["rectangles"].append(r)                       
            
            hashMap = redraw(hashMap)
            #hashMap = redraw(hashMap)
            #hashMap.put("RefreshScreen","")
            #hashMap.put('sug_reload',"")
            
    elif  hashMap.get("listener") == "btn_savesug":  
        if not "sug_uid" in session:
            session["sug_uid"] = str(uuid.uuid4().hex) 

        session["sugfilename"] = hashMap.get("base_path")+os.sep+"uploads"+os.sep+session["sug_uid"]+".sug" 
        
        file_w = hashMap.get("file_w")
        file_h = hashMap.get("file_h")
        if file_w == None or file_h==None:
            hashMap.put("toast","Не заданы размеры изображения")
            return hashMap
        elif  max(file_w,file_h)==0:
            hashMap.put("toast","Не заданы размеры изображения")
            return hashMap
        else:       
            ratio = CANVAS_H/max(int(file_w),int(file_h))
        
        json_out = {"columncount":int(int(file_w)/GRIDSIZE),"rowcount":int(int(file_h)/GRIDSIZE),"gridsize":GRIDSIZE}
        datalist = []
        if len(session["rows"]):
            for row in session["rows"]:
                row_out = {"count_cells_in_row":row.num_rows,"count_columns":row.num_columns,"orientation":1,"size":int(row.cell_size/ratio),"cells":[],"deleted":False}
                for cell in row.cells:
                    c = {"address":cell.address,"x1":int(cell.x1/ratio),"y1":int(cell.y1/ratio), "x2":int(cell.x2/ratio), "y2":int(cell.y2/ratio),"size":int(row.cell_size/ratio),"fillcolor":0,"entarnce_moved":False,"orientation":0,"entrance":{"color":3,"x1":cell.x1,"x2":cell.x1+GRIDSIZE,"y1":cell.y1,"y2":cell.y1+GRIDSIZE}}
                    row_out["cells"].append(c)
                datalist.append(row_out)    
        json_out["rows"] = json.dumps({"dataList":datalist},ensure_ascii=False)

        if len(session["labels"]):
            datalist = []
            for elem in session["labels"]:
                elem_out = {"x":int(elem.x/ratio),"y":int(elem.y/ratio),"size":elem.size*RATIO_TEXT_SIZE,"text":elem.text}
                
                datalist.append(elem_out)    
            json_out["labels"] = json.dumps({"dataList":datalist},ensure_ascii=False)
        if len(session["rectangles"]):
            datalist = []
            for elem in session["rectangles"]:
                elem_out = {"x1":int(elem.x1/ratio),"y1":int(elem.y1/ratio),"x2":int(elem.x2/ratio),"y2":int(elem.y2/ratio),"strock_size":elem.strock_size*RATIO_STROCK}
                
                datalist.append(elem_out)    
            json_out["rects"] = json.dumps({"dataList":datalist},ensure_ascii=False)  
        if len(session["vectors"]):
            datalist = []
            for elem in session["vectors"]:
                elem_out = {"x1":int(elem.x1/ratio),"y1":int(elem.y1/ratio),"x2":int(elem.x2/ratio),"y2":int(elem.y2/ratio),"strock_size":elem.strock_size*RATIO_STROCK}
                
                datalist.append(elem_out)    
            json_out["vectors"] = json.dumps({"dataList":datalist},ensure_ascii=False)        
        with open(session["sugfilename"] , 'w',encoding="utf-8") as f:
            json.dump(json_out, f,ensure_ascii=False,indent=4) 
            hashMap.put("download_sug",'sug-file тут: <a href="/download_file?filename='+Path(session["sugfilename"]).name+'" target="_blank" download="vector_drawable.sug">скачать sug-файл</a>')     
            hashMap.put("SetValues",json.dumps([{"download_sug":hashMap.get("download_sug")}],ensure_ascii=False))



        #hashMap.put("DownloadFile",session["filename"])  
        
    return hashMap
