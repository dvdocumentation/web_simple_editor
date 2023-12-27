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


filename = None
filename_base = None
processes_table_id = -1
screens_table_id = -1
elements_table_id = -1

current_element =None
parent_element = None
#parent_elelments_element = None

current_parent = (None,None)
current_parent_dict = {}

edit_handler_mode = -1
postExecute = ""
layouts_edit = False
host_uid = ""

WSPORT = "1555"

locale_filename = "ru_locale.json"


events_common = ["","onLaunch","onIntentBarcode","onBluetoothBarcode","onBackgroundCommand","onRecognitionListenerResult"]

events_screen = ["","onStart","onPostStart","onInput"]

opened_element_uid = None

main_menu_elements = ["","qr_settings","offline_exchange","documents","tasklist","product_log","store","save_settings","keyboard_test","ping_bt","update_configurations","Custom menu item"]

action_types = ["","run","runasync","runprogress"]
handler_types = ["","python","pythonargs","pythonbytes","online","http","sql","nosql","set"]

configuration = {"ClientConfiguration":{}}
processes_table = []

configuration_properties_list = ["ConfigurationName","ConfigurationVersion","ConfigurationDescription","agent","ForegroundService","StopForegroundServiceOnExit","BroadcastIntent","BroadcastVariable","FaceRecognitionURL","OnKeyboardMain","LaunchProcess","LaunchVar","MenuWebTemplate","Launch"]
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

handler_layout = {
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
                                "type": "MultilineText",
                                "height": "wrap_content",
                                "width": "match_parent",
                                "weight": "0",
                                "Value": "Метод|@method",
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
                                "type": "EditTextText",
                                "height": "wrap_content",
                                "width": "match_parent",
                                "weight": "0",
                                "Value": "Метод|@method_postExecute",
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




def get_text_from_ginthub(url,token):

  # send a request
  r = requests.get(
      url,
      headers={
          'accept': 'application/vnd.github.v3.raw',
          'authorization': 'token {}'.format(token)
              }
      )

  
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
    if 'RecognitionTemplates' in configuration['ClientConfiguration']:
        res = list(filter(lambda item: item['name'] == name, configuration['ClientConfiguration']['RecognitionTemplates']))
        if len(res)>0:
            return json.dumps(remove_empty(res[0]),ensure_ascii=False)
    return None

def get_style(name):
    if 'StyleTemplates' in configuration['ClientConfiguration']:
        res = list(filter(lambda item: item['name'] == name, configuration['ClientConfiguration']['StyleTemplates']))
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
                
            new_element['Elements'].append(el)

    return new_element        

def configuration_open(hashMap,_files=None,_data=None):    
    global configuration
    global host_uid
    #global filename
    
    hashMap.put("host_uid",host_uid) 
    hashMap.put("Launch_elements",captions_start_screen_elements)

    
    for prop in configuration_properties_list:
        hashMap.put(prop,configuration['ClientConfiguration'].get(prop,""))
        if prop == "Launch":
            hashMap.put(prop,get_synonym(start_screen_elements,configuration['ClientConfiguration'].get(prop,"")))

    if "ConfigurationSettings" in  configuration['ClientConfiguration']:
        for prop in configuration_settings_list:
            hashMap.put(prop,configuration['ClientConfiguration']["ConfigurationSettings"].get(prop,""))


    #if filename!=None:
    
    filename = host_uid+".ui"

    link = "http://"+ socket.gethostbyname(socket.gethostname())+":"+str(WSPORT)+"/get_conf_text?filename="+host_uid+".ui"

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
    if filename_base!=None:
        hashMap.put("download_configuration",'Файл конфигурации можно скачать тут: <a href="/download_file?filename='+Path(filename).name+'" target="_blank" download="'+ filename_base+ '">скачать конфигурацию</a>')     
    else:    
        hashMap.put("download_configuration",'Файл конфигурации можно скачать тут: <a href="/download_file?filename='+Path(filename).name+'" target="_blank" ">скачать конфигурацию</a>')     

    return hashMap


def update_configuration_properties(write_file=True):
    global configuration


    isPython = False
    isOnline = False
    isCV=False

    if 'PyHandlers' in configuration['ClientConfiguration']:
        if len(configuration['ClientConfiguration']['PyHandlers'])>0:
            isPython=True
  
    if 'DefServiceConfiguration' in configuration['ClientConfiguration']:
        if len(configuration['ClientConfiguration']['DefServiceConfiguration'])>0:
            isPython=True  

    if 'OnlineServiceConfiguration' in configuration['ClientConfiguration']:
        if len(configuration['ClientConfiguration']['OnlineServiceConfiguration'])>0:
            isOnline=True            
            

    if 'Processes' in configuration['ClientConfiguration']:        
        for process in configuration['ClientConfiguration']['Processes']:
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
        configuration['ClientConfiguration']['RunPython']  =True   

            
    tags=[]
    if isPython:
        tags.append('Py') 
        tags.append('off-line')        
    if isOnline:
        tags.append('Online')        
    if isCV:
        tags.append('ActiveCV®')    

    configuration['ClientConfiguration']['ConfigurationTags']=",".join(tags) 


        

def save_configuration(configuration,hashMap,full=False):
    global filename
    global host_uid

    no_agent=False

    #configuration["ClientConfiguration"]["agent"] = hashMap.get("agent")
    if full:
        update_configuration_properties()
    filename = hashMap.get("base_path")+os.sep+"uploads"+os.sep+host_uid+".ui"

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

    for process in processes_table:
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
        #write handlers
        if "GitHubHandlers" in new_configuration["ClientConfiguration"]:
            handlers_url = new_configuration["ClientConfiguration"]["GitHubHandlers"]
            handlers_token = new_configuration["ClientConfiguration"]["GitHubToken"]

            if len(handlers_url)>0:

                handlers_txt = get_text_from_ginthub(handlers_url,handlers_token)
                if handlers_txt!=None:
                    new_configuration["ClientConfiguration"]["PyHandlers"] = base64.b64encode(handlers_txt.encode('utf-8')).decode('utf-8')

                if "PyFiles" in configuration["ClientConfiguration"]:
                    for filestr in configuration["ClientConfiguration"]["PyFiles"]:
                        if  len(filestr.get("PyFileLink",""))>0:
                            handlers_txt = get_text_from_ginthub(filestr.get("PyFileLink",""),handlers_token)
                            if handlers_txt!=None:
                                filestr["PyFileData"] = base64.b64encode(handlers_txt.encode('utf-8')).decode('utf-8')
        elif new_configuration["ClientConfiguration"].get("agent") == True and not no_agent:
            if FilePyHandlers!=None:
                new_configuration["ClientConfiguration"]["PyHandlers"] = FilePyHandlers
            if FilePyFiles!=None:
                new_configuration["ClientConfiguration"]["PyFiles"] = FilePyFiles    

    with open(filename, 'w',encoding="utf-8") as f:
        json.dump(new_configuration, f,ensure_ascii=False,indent=4)

def configuration_input(hashMap,_files=None,_data=None):
    global configuration
    global filename
    global host_uid
    global processes_table
    global filename_base

    if hashMap.get("listener") == "btn_upload":
        id = "configuration_file"
        hashMap.put("UploadFile",id)

    elif hashMap.get("listener") == "btn_new_configuration":

        #generating new uuid for SimpleUI configuration
        current_uid = uuid.uuid4().hex
            #create simple template of SimpleUi configuration
        configuration={"ClientConfiguration":
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

        host_uid =  str(uuid.uuid4().hex)  
        configuration["ClientConfiguration"]["host_uid"] = host_uid 

        processes_table = configuration["ClientConfiguration"]["Processes"] 

        save_configuration(configuration,hashMap,True) 

        hashMap.put("RefreshScreen","")  
        
    elif hashMap.get("listener") == "upload_file":    
        filename =hashMap.get("base_path")+os.sep+"uploads"+os.sep+ hashMap.get("filename")
        filename_base = hashMap.get("filename")[21:]
        with open(filename,encoding="utf-8") as conf_file:
            configuration = json.load(conf_file)

            if "host_uid" in configuration["ClientConfiguration"]:
                host_uid = configuration["ClientConfiguration"]["host_uid"]
            else:
                host_uid =  str(uuid.uuid4().hex)  
                configuration["ClientConfiguration"]["host_uid"] = host_uid
    
            processes_table = configuration["ClientConfiguration"]["Processes"] 

            
            hashMap.put("RefreshScreen","")
      
    elif hashMap.get("listener") == "btn_download":
        filename = host_uid+".ui" 
        hashMap.put("DownloadFile",filename)  
            
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
            configuration['ClientConfiguration'][prop] = hashMap.get(prop)

            if prop == "Launch":
                configuration['ClientConfiguration'][prop] = get_key(start_screen_elements,hashMap.get(prop))

        if not 'ConfigurationSettings' in configuration['ClientConfiguration']: configuration['ClientConfiguration']['ConfigurationSettings']={}

        for prop in configuration_settings_list:
            configuration['ClientConfiguration']['ConfigurationSettings'][prop] = hashMap.get(prop)

            if hashMap.get("vendor_login")!=None and hashMap.get("vendor_login")!="":
                authstring =hashMap.get("vendor_login")+":"+ hashMap.get("vendor_password")
                configuration['ClientConfiguration']['ConfigurationSettings']['vendor_auth']=  'Basic '+   base64.b64encode(authstring.encode('utf-8')).decode('utf-8') 

            if hashMap.get("handler_login")!=None and hashMap.get("handler_login")!="":
                authstring =hashMap.get("handler_login")+":"+ hashMap.get("handler_password")
                configuration['ClientConfiguration']['ConfigurationSettings']['handler_auth']=  'Basic '+   base64.b64encode(authstring.encode('utf-8')).decode('utf-8')    

    
        save_configuration(configuration,hashMap,True)

    return hashMap


current_process_name = ""

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
"MultilineText":get_locale("multiline"),"CardsLayout":get_locale("cards"),"CButtons":get_locale("buttons_list"),"CButtonsHorizontal":get_locale("horizontal_buttons_list"),"DateField":get_locale("date_input"),"ProgressButton":get_locale("progress_button"),"html":get_locale("HTML"),"map":get_locale("map"),"file":get_locale("file"),"object":get_locale("object")}
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

resolution_elements = ['','HD1080','HD720','VGA','QVGA']

start_screen_elements = {"Menu":get_locale("operations_menu"),"Tiles":get_locale("tiles_menu")}
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

    t['rows'] = table

    return t

def main_tab_selected(hashMap,_files=None,_data=None):
    global current_parent_dict
    global current_parent
    global current_element
    global processes_table_id
    global screens_table_id

    CurrentTabKey = hashMap.get("CurrentTabKey")
    if CurrentTabKey in current_parent_dict:
        current_parent = current_parent_dict[CurrentTabKey]
        current_element = current_parent[0]

        if current_element!=None:
            if current_element.get("type") == "Process" or "ProcessName" in current_element:
                processes_table_id = processes_table.index(current_element)
            elif current_element.get("type") == "Operation":    
                if current_parent[1]!=None:
                    if current_parent[1][0]!=None:
                        if "Operations" in current_parent[1][0]:
                            screens_table_id = current_parent[1][0]["Operations"].index(current_element)

    return hashMap

def processes_open(hashMap,_files=None,_data=None):

    if processes_table!=None:
        
        hashMap.put("processes_table",json.dumps(make_processes_table(processes_table),ensure_ascii=False))
 
    return hashMap

def process_input(hashMap,_files=None,_data=None):

    global current_parent
    global current_parent_dict
    global processes_table
    global parent_element
    global processes_table_id
    global screens_table_id
    global current_element

    if current_element==None:
        closeuid  =hashMap.get("process_uid")
    else:    
        closeuid = current_element['uid']

    if hashMap.get("listener")=="btn_save" or hashMap.get("listener")=="btn_add_screen" or hashMap.get("listener")=="btn_edit_screen":


        if processes_table_id==-1:
            processes_table.append({
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
            processes_table_id=len(processes_table)-1

        else:   
            current_element["ProcessName"] =hashMap.get("process_name") 
            current_element["PlanFactHeader"] =hashMap.get("PlanFactHeader") 
            current_element["hidden"] =hashMap.get("hidden") 
            current_element["DefineOnBackPressed"] =hashMap.get("DefineOnBackPressed") 
            current_element["login_screen"] =hashMap.get("login_screen") 
            current_element["SC"] =hashMap.get("SC") 
            current_element["uid"] =closeuid 
          
        
        current_parent = (processes_table[processes_table_id],None)
        current_element = current_parent[0]
        current_parent_dict[closeuid] = current_parent


    if hashMap.get("listener")=="btn_save" or hashMap.get("listener")=="btn_close":

        hashMap.put("CloseTab",closeuid)

        hashMap.put("processes_table",json.dumps(make_processes_table(processes_table),ensure_ascii=False))

        hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"main_screen", "key":"Процессы", "reopen":True},ensure_ascii=False))

        save_configuration(configuration,hashMap)
     
    elif hashMap.get("listener")=="btn_add_screen":

        uid = str(uuid.uuid4().hex)
        hashMap.put("screen_uid",uid)

        hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"screen_form","key":uid,"reopen":True},ensure_ascii=False))  
        current_process_name = "Новый экран"
        hashMap.put("screen_name",current_process_name)
        hashMap.put("Timer","")
        hashMap.put("hideToolBarScreen","")
        hashMap.put("noScroll","")
        hashMap.put("handleKeyUp","")
        hashMap.put("noConfirmation","")
        hashMap.put("hideBottomBarScreen","")
        hashMap.put("SetTitle","Новый экран - *")

        #блокировка
        #hashMap.put("BlockTabs","")

        screens_table_id = -1
        current_element = None 
        current_parent = (None,current_parent)
        current_parent_dict[uid] = current_parent   
    elif hashMap.get("listener")=="btn_edit_screen" or (hashMap.get("listener") == "TableDoubleClick"):
        screens_table_id = int(hashMap.get("selected_line_id"))
        #row = parent_element["Operations"][screens_table_id]
        row = current_element["Operations"][screens_table_id]
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

        current_element = row  
        current_parent = (row,current_parent) 
        current_parent_dict[row['uid']] = current_parent      
    elif hashMap.get("listener")=="btn_delete_screen":
        
        sel_line = 'selected_line_id'
        if hashMap.containsKey(sel_line):
                current_element['Operations'].pop(int(hashMap.get(sel_line)))
                hashMap.put("RefreshScreen","")
                hashMap.remove(sel_line)    

    return hashMap


def screen_input(hashMap,_files=None,_data=None):
    global current_parent
    global current_parent_dict
    global processes_table
    global parent_element
    global screens_table_id
    global elements_table_id
    global current_element
    global process_table_id

    global edit_handler_mode
    global layouts_edit
    global opened_element_uid

    layouts_edit=False

    closeuid = None

    if current_element==None:
        closeuid = hashMap.get("screen_uid")
    else:    
        closeuid = current_element['uid']

    if hashMap.get("listener")=="btn_save" or hashMap.get("listener")=="btn_add_element" or hashMap.get("listener") == "btn_add_handler":

        

        current_parent =current_parent[1]
        current_element = current_parent[0]

        if screens_table_id==-1:
            current_element['Operations'].append({
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
            
            screens_table_id=len(current_element['Operations'])-1
            
            
        else:   
            current_element['Operations'][screens_table_id]["Name"] = hashMap.get("screen_name")
            current_element['Operations'][screens_table_id]["uid"] = closeuid

            current_element['Operations'][screens_table_id]["Timer"] = hashMap.get("Timer")
            current_element['Operations'][screens_table_id]["hideToolBarScreen"] = hashMap.get("hideToolBarScreen")
            current_element['Operations'][screens_table_id]["layout_file"] = hashMap.get("layout_file")
            current_element['Operations'][screens_table_id]["noScroll"] = hashMap.get("noScroll")
            current_element['Operations'][screens_table_id]["handleKeyUp"] = hashMap.get("handleKeyUp")
            current_element['Operations'][screens_table_id]["noConfirmation"] = hashMap.get("noConfirmation")
            current_element['Operations'][screens_table_id]["hideBottomBarScreen"] = hashMap.get("hideBottomBarScreen")
            
        
        current_parent = (current_element['Operations'][screens_table_id],current_parent)
        current_parent_dict[closeuid] = current_parent

        
        current_element = current_parent[0]
        
    
        

    if hashMap.get("listener")=="btn_save" or hashMap.get("listener")=="btn_close":
 
        hashMap.put("CloseTab",closeuid)
        hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"process_form", "key":current_parent[1][0]['uid'], "reopen":True},ensure_ascii=False))

        current_parent = current_parent[1]
        process_table_id = processes_table.index(current_parent[0])
        current_element = current_parent[0]

        save_configuration(configuration,hashMap)

        #блокировка
        hashMap.put("UnblockTabs","")
 
    elif hashMap.get("listener")=="btn_add_element":

        

        uid = str(uuid.uuid4().hex)
        hashMap.put("element_uid",uid)

        if opened_element_uid != None:
                hashMap.put("toast","Может быть открыт только 1 элемент")
                return hashMap
            
        opened_element_uid = uid

        if layouts_edit:
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
        
                
        elements_table_id = -1
        current_element = None  

        current_parent = (current_element,current_parent)
        current_parent_dict[uid] = current_parent 

    elif hashMap.get("listener")=="btn_edit_element" or (hashMap.get("listener") == "TableDoubleClick" and hashMap.get("table_id")=='screen_elements_table'):
        
        if hashMap.containsKey("selected_line_id"):
            elements_table_id = int(hashMap.get("selected_line_id"))
            row = current_element["Elements"][elements_table_id]
            
            if not 'uid' in row:
                row['uid'] = str(uuid.uuid4().hex)
            
            if opened_element_uid != None:
                hashMap.put("toast","Может быть открыт только 1 элемент")
                return hashMap
            
            opened_element_uid = row['uid']

            if layouts_edit:
                hashMap.put("OpenScreen",json.dumps({"process":"Контейнеры","screen":"element_form","key":row['uid'],"reopen":True,"no_close":True},ensure_ascii=False))  
            else:    
                hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"element_form","key":row['uid'],"reopen":True,"no_close":True},ensure_ascii=False))  
            #current_screen_name = row.get("Name")
            #hashMap.put("screen_name",current_screen_name)
            hashMap.put("SetTitle",row.get("type"))

            hashMap.put("element_uid",row.get("uid"))

            #parent_elelments_element = current_element

            current_parent = (row,current_parent)
            current_parent_dict[row['uid']] = current_parent

            current_element = row     

            hashMap.remove("selected_line_id")  

    elif hashMap.get("listener")=="btn_delete_element":
        sel_line = 'selected_line_id'
        if hashMap.containsKey(sel_line):
                current_element['Elements'].pop(int(hashMap.get(sel_line)))
                #hashMap.put("screens_table",json.dumps(jtable,ensure_ascii=False)) 
                #hashMap.put("SetValuesTable",json.dumps([{"screens_table":jtable}]) )       
                hashMap.put("RefreshScreen","")
                hashMap.remove(sel_line)    

    elif hashMap.get("listener") == "btn_add_handler":
        hashMap.put("ShowDialogLayout",json.dumps(handler_layout,ensure_ascii=False))
        hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Обработчик"},ensure_ascii=False))
        hashMap.put("ShowDialog","")

        
        hashMap.put("event","")
        hashMap.put("action","")
        hashMap.put("type","")
        hashMap.put("method","")
        hashMap.put("listener","")

        hashMap.put("action_postExecute","")
        hashMap.put("type_postExecute","")
        hashMap.put("method_postExecute","")

        postExecute = ""
        edit_handler_mode = -1
    elif hashMap.get("listener") == "btn_edit_handler" or (hashMap.get("listener") == "TableDoubleClick" and hashMap.get("table_id")=='handlers_table'):
        if hashMap.containsKey("selected_line_id"):
            hashMap.put("ShowDialogLayout",json.dumps(handler_layout,ensure_ascii=False))
            hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Обработчик"},ensure_ascii=False))
            hashMap.put("ShowDialog","")

            edit_handler_mode = int(hashMap.get("selected_line_id"))

            handler_str = current_element['Handlers'][edit_handler_mode]

           
            hashMap.put("event",handler_str.get("event",""))
            hashMap.put("action",handler_str.get("action",""))
            hashMap.put("type",handler_str.get("type",""))
            hashMap.put("method",handler_str.get("method",""))
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
                        hashMap.put("method_postExecute",jpe[0].get("method",""))
            
            hashMap.remove("selected_line_id")  

    elif hashMap.get("listener") == "btn_delete_handler":
        if hashMap.containsKey("selected_line_id"):
            pos = int(hashMap.get("selected_line_id"))   
            current_element['Handlers'].pop(pos)
            hashMap.put("RefreshScreen","")
            hashMap.remove("selected_line_id")      

    elif hashMap.get("listener") == "onResultPositive": 
        if edit_handler_mode == -1:
            dialog_values = list_to_dict(json.loads(hashMap.get("dialog_values")))

            if not "Handlers" in current_element:
                current_element['Handlers'] = []
            
            postExecute = ""
            if len(str(hashMap.get("action_postExecute")))>0 and len(str(hashMap.get("type_postExecute")))>0:
                postExecute =json.dumps( [{"action":dialog_values.get("action_postExecute",""),"type":dialog_values.get("type_postExecute",""),"method":dialog_values.get("method_postExecute","")}], ensure_ascii=False)

            current_element['Handlers'].append({"event":dialog_values.get("event",""),"action":dialog_values.get("action",""),"listener":dialog_values.get("listener",""),"type":dialog_values.get("type",""),"method":dialog_values.get("method",""),"postExecute":postExecute,"alias":dialog_values.get("alias","")}) 
            hashMap.put("RefreshScreen","")
            hashMap.put("callSelectTab","Обработчики")
            hashMap.put("SelectTab","Обработчики")
            
        else:
            dialog_values = list_to_dict(json.loads(hashMap.get("dialog_values")))

            postExecute = ""
            if len(str(hashMap.get("action_postExecute")))>0 and len(str(hashMap.get("type_postExecute")))>0:
                postExecute = json.dumps( [{"action":dialog_values.get("action_postExecute",""),"type":dialog_values.get("type_postExecute",""),"method":dialog_values.get("method_postExecute","")}], ensure_ascii=False)

            current_element['Handlers'][edit_handler_mode] ={"event":dialog_values.get("event",""),"action":dialog_values.get("action",""),"listener":dialog_values.get("listener",""),"type":dialog_values.get("type",""),"method":dialog_values.get("method",""),"postExecute":postExecute,"alias":dialog_values.get("alias","")} 
            hashMap.put("RefreshScreen","")
            hashMap.put("callSelectTab","Обработчики")
            hashMap.put("SelectTab","Обработчики")
           
    

    return hashMap




def element_input(hashMap,_files=None,_data=None):
    global current_parent
    global current_parent_dict

    global processes_table
    
    #global parent_elelments_element
    global screens_table_id
    global current_element
    global elements_table_id
    global configuration
    global opened_element_uid

    if current_element==None:
        closeuid = hashMap.get("element_uid")
    else:    
        closeuid = current_element['uid']

    if hashMap.get("listener")=="btn_save" or hashMap.get("listener")=="btn_add_element" or  hashMap.get("listener")=="btn_edit_element":
        current_parent =current_parent[1]
        if current_parent!=None:
            current_element = current_parent[0]

            if current_element.get("type") == "Operation":
                element_base = screen_elements
            else:
                element_base = layout_elements 
            row = current_element['Elements']     
        else:         
            element_base = layout_elements  
            if not "Layouts" in configuration["ClientConfiguration"]:
                configuration["ClientConfiguration"]["Layouts"]=[]
            #current_element = configuration["ClientConfiguration"]["Layouts"]
            row = configuration["ClientConfiguration"]['Layouts'] 
        

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


        if elements_table_id==-1:
                  
            
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


            if get_key(element_base,hashMap.get('type')) == 'LinearLayout' or get_key(element_base,hashMap.get('type')) == 'Tab' or get_key(element_base,hashMap.get('type')) == 'Tabs':
                d["Elements"] =[]

            row.append(d) 
            elements_table_id = len(row) - 1
             
        else:   
            row[elements_table_id]['type'] = get_key(element_base,hashMap.get("type"))

            row[elements_table_id]['orientation'] = get_key(orientation_elements,hashMap.get("orientation"))
            row[elements_table_id]['gravity_vertical'] = get_key(vertical_gravity_elements,hashMap.get("gravity_vertical"))
            row[elements_table_id]['drawable'] = hashMap.get("drawable")
            row[elements_table_id]['gravity_horizontal'] = get_key(gravity_elements,hashMap.get("gravity_horizontal"))
            row[elements_table_id]['height'] = height
            row[elements_table_id]['width'] = width
            row[elements_table_id]['Value'] = hashMap.get("Value")
            row[elements_table_id]['Variable'] = hashMap.get("Variable")
            row[elements_table_id]['BackgroundColor'] = hashMap.get("BackgroundColor")
            row[elements_table_id]['StrokeWidth'] = hashMap.get("StrokeWidth")
            row[elements_table_id]['Padding'] = hashMap.get("Padding")
            row[elements_table_id]['height_value'] = hashMap.get("height_value")
            row[elements_table_id]['width_value'] = hashMap.get("width_value")
            row[elements_table_id]['weight'] = hashMap.get("weight")
            row[elements_table_id]['TextSize'] = hashMap.get("TextSize")
            row[elements_table_id]['TextColor'] = hashMap.get("TextColor")
            row[elements_table_id]['TextBold'] = hashMap.get("TextBold")
            row[elements_table_id]['TextItalic'] = hashMap.get("TextItalic")
            row[elements_table_id]['NumberPrecision'] = hashMap.get("NumberPrecision")
            row[elements_table_id]['RecognitionTemplate'] = hashMap.get("RecognitionTemplate")
            row[elements_table_id]['style_name'] = hashMap.get("style_name")


            row[elements_table_id]['uid'] = closeuid

            if width == "manual":
                row[elements_table_id]["width_value"] = hashMap.get("width_value")
            else:
                if "width_value" in current_element:
                    del row[elements_table_id]["width_value"]    
            
            if height == "manual":
                row[elements_table_id]["height_value"] = hashMap.get("height_value")  
            else:
                if "height_value" in current_element:
                    del row[elements_table_id]["height_value"] 


        current_parent =(row[elements_table_id],current_parent)

        current_element = current_parent[0]
        current_parent_dict[closeuid] = current_parent
        
        # if current_parent[1][0].get("type") == "Operation":
        #     screens_table_id = current_parent[1][0]['Operations'].index(current_element)
        # else:    
        #     elements_table_id = current_parent[1][0]['Elements'].index(current_element) 


    if hashMap.get("listener")=="btn_close":
        if current_parent!=None:
            current_parent =current_parent[1]
            if current_parent!=None:
                current_element = current_parent[0]

            
                current_parent_dict[closeuid] = current_parent
    
    if hashMap.get("listener")=="btn_save" :

        
        hashMap.put("CloseTab",closeuid)
        hashMap.put("Show_RecognitionTemplate_div","-1")
        hashMap.put("Show_RecognitionTemplate","-1")
        hashMap.put("Show_RecognitionTemplate_p","-1")

        if current_parent[1]==None:
            hashMap.put("layouts_table",json.dumps(make_onefield_table(configuration["ClientConfiguration"]['Layouts'],"Variable","Переменная"),ensure_ascii=False))
            hashMap.put("OpenScreen",json.dumps({"process":"Контейнеры","screen":"main_form", "key":"Контейнеры", "reopen":True},ensure_ascii=False))
        else:    
            if current_parent[1][0].get("type") == "Operation":
                hashMap.put("screen_elements_table",json.dumps(make_screenelements_table(current_parent[1][0]['Elements']),ensure_ascii=False))
                hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"screen_form", "key":current_parent[1][0]['uid'], "reopen":True},ensure_ascii=False))
            else:    

                if current_element.get("type") == 'LinearLayout' or current_element.get("type") == 'Tab' or current_element.get("type") == 'Tabs' :
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

                        if current_element.get("type") == 'Vision':
                            hashMap.put("Show_RecognitionTemplate_div","1")  
                            hashMap.put("Show_RecognitionTemplate_p","1") 
                            hashMap.put("Show_RecognitionTemplate","1")   
                            

                
                hashMap.put("layout_elements_table",json.dumps(make_layoutelements_table(current_parent[1][0]['Elements']),ensure_ascii=False))
                hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"element_form", "key":current_parent[1][0]['uid'], "reopen":True},ensure_ascii=False))

        current_parent = current_parent[1]
          
        
        if current_parent==None:
            pass
            #elements_table_id =current_parent[1][0]['Operations'].index(current_parent[0])
        else:    
            if current_parent[0].get("type") == "Operation":
                screens_table_id = current_parent[1][0]['Operations'].index(current_parent[0])
            else:    
                if current_parent[1]==None:
                    elements_table_id = configuration['ClientConfiguration']['Layouts'].index(current_parent[0]) 
                else:    
                    elements_table_id = current_parent[1][0]['Elements'].index(current_parent[0]) 

            current_element = current_parent[0] 

        save_configuration(configuration,hashMap) 

        opened_element_uid = None    

    if  hashMap.get("listener")=="btn_close":

        opened_element_uid = None 

        hashMap.put("CloseTab",closeuid)

        hashMap.put("Show_RecognitionTemplate_div","-1")
        hashMap.put("Show_RecognitionTemplate","-1")
        hashMap.put("Show_RecognitionTemplate_p","-1")

        if current_parent==None:
            hashMap.put("layouts_table",json.dumps(make_onefield_table(configuration["ClientConfiguration"]['Layouts'],"Variable","Переменная"),ensure_ascii=False))
            hashMap.put("OpenScreen",json.dumps({"process":"Контейнеры","screen":"main_form", "key":"Контейнеры", "reopen":True},ensure_ascii=False))
        else:  
            if current_element.get("type") == "Operation":
                hashMap.put("screen_elements_table",json.dumps(make_screenelements_table(current_element['Elements']),ensure_ascii=False))
                hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"screen_form", "key":current_parent[0]['uid'], "reopen":True},ensure_ascii=False))
            else:    

                if current_element.get("type") == 'LinearLayout' or current_element.get("type") == 'Tab' or current_element.get("type") == 'Tabs':
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

                        if current_element.get("type") == 'Vision':
                            hashMap.put("Show_RecognitionTemplate_div","1")  
                            hashMap.put("Show_RecognitionTemplate_p","1")
                            hashMap.put("Show_RecognitionTemplate","1") 

                hashMap.put("layout_elements_table",json.dumps(make_layoutelements_table(current_parent[0]['Elements']),ensure_ascii=False))
                hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"element_form", "key":current_parent[0]['uid'], "reopen":True},ensure_ascii=False))

            
            
            if current_parent[0].get("type") == "Operation":
                screens_table_id = current_parent[1][0]['Operations'].index(current_parent[0])
            else:    
                elements_table_id = current_parent[1][0]['Elements'].index(current_parent[0]) 

        
             

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

                    
        

                
        elements_table_id = -1
        current_element = None   

        current_parent = (current_element,current_parent) 
        
        current_parent_dict[uid] = current_parent

    elif hashMap.get("listener")=="btn_edit_element" or (hashMap.get("listener") == "TableDoubleClick"):

        elements_table_id = int(hashMap.get("selected_line_id"))
        row = current_element["Elements"][elements_table_id]
        
        if not 'uid' in row:
           row['uid'] = str(uuid.uuid4().hex)
        
        hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"element_form","key":row['uid'],"reopen":True,"no_close":True},ensure_ascii=False))  
        hashMap.put("SetTitle",row.get("type"))

        hashMap.put("element_uid",row.get("uid"))
        
        #parent_elelments_element = current_element
        current_parent = (row,current_parent)
        current_element = row 

        current_parent_dict[row['uid']] = current_parent

    elif hashMap.get("listener")=="btn_delete_element":
        sel_line = 'selected_line_id'
        if hashMap.containsKey(sel_line):
                current_element['Elements'].pop(int(hashMap.get(sel_line)))
                #hashMap.put("screens_table",json.dumps(jtable,ensure_ascii=False)) 
                #hashMap.put("SetValuesTable",json.dumps([{"screens_table":jtable}]) )       
                hashMap.put("RefreshScreen","")
                hashMap.remove(sel_line)  

    elif hashMap.get("listener")=="btn_copy":
        hashMap.put("WriteClipboard",json.dumps(current_element,ensure_ascii=False))
    elif hashMap.get("listener")=="btn_paste":
        hashMap.put("ReadClipboard","")
    elif hashMap.get("listener")=="clipboard_result":    
        try:
            jelement = json.loads(hashMap.get("clipboard_result"))
            if "type" in jelement:
                current_element['Elements'].append(jelement)
                hashMap.put("RefreshScreen","")

        except:
            hashMap.put("toast","Ошибка буфера")    
    if hashMap.get("listener")=="type":

        if current_parent[1][0].get("type") == "Operation":
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
            
            if current_parent[1][0].get("type") == "Operation":
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
            
            if current_parent[1][0].get("type") == "Operation":
                hashMap.put("SetShow_element_properties","-1")  
                hashMap.put("SetShow_common_properties","-1")
            else:
                hashMap.put("SetShow_element_properties","1")      
                hashMap.put("SetShow_common_properties","1")
  

    return hashMap


def process_open(hashMap,_files=None,_data=None):

    if not current_element == None:
        hashMap.put("screens_table",json.dumps(make_onefield_table(current_element["Operations"],"Name","Экран"),ensure_ascii=False))
    else:
        hashMap.put("screens_table",json.dumps(make_onefield_table([],"Name","Экран"),ensure_ascii=False))
   
    return hashMap

def screen_open(hashMap,_files=None,_data=None):
    hashMap.put("common_events",";".join(events_screen))
    hashMap.put("handler_types",";".join(handler_types))
    hashMap.put("action_types",";".join(action_types))

    recognition_templates = []
    recognition_templates.append("")
    if "RecognitionTemplates" in configuration['ClientConfiguration']:
        for t in configuration['ClientConfiguration']["RecognitionTemplates"]:
            recognition_templates.append(t.get('name'))
    hashMap.put("recognition_templates",";".join(recognition_templates)) 

    xml_files = []
    xml_files.append("")
    if "Mediafile" in configuration['ClientConfiguration']:
        for t in configuration['ClientConfiguration']["Mediafile"]:
            if t.get("MediafileExt") == "xml":
                xml_files.append(t.get('MediafileKey'))
    hashMap.put("xml_files",";".join(xml_files)) 

    style_templates = []
    style_templates.append("")
    if "StyleTemplates" in configuration['ClientConfiguration']:
        for t in configuration['ClientConfiguration']["StyleTemplates"]:
            style_templates.append(t.get('name'))
    hashMap.put("style_templates",";".join(style_templates))        

    if not current_element == None:
        if "Elements" in current_element:
            hashMap.put("screen_elements_table",json.dumps(make_screenelements_table(current_element["Elements"]),ensure_ascii=False))
        else:    
            hashMap.put("screen_elements_table",json.dumps(make_screenelements_table([]),ensure_ascii=False))
    
        if  "Handlers" in current_element:
            hashMap.put("handlers_table",json.dumps(make_handlers_table(current_element["Handlers"],True),ensure_ascii=False))
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

    
    if current_parent != None:
        element_base = layout_elements  
        if current_parent[1]!=None:
            par = current_parent[1][0]
            if par.get("type") == "Operation":
                hashMap.put("screen_elements",captions_screen_elements)
                element_base = screen_elements
            else:
                hashMap.put("screen_elements",captions_layout_elements)
                
                element_base = layout_elements  

        if current_element!=None:
            if "Elements" in current_element:
                hashMap.put("layout_elements_table",json.dumps(make_layoutelements_table(current_element["Elements"]),ensure_ascii=False))    
   
    if current_parent == (None,None):
        hashMap.put("type", get_synonym(element_base,"LinearLayout"))
        hashMap.put("screen_elements",captions_layout_elements)

    if not current_element == None:
        hashMap.put("type", get_synonym(element_base,current_element.get("type")))
        
        hashMap.put("orientation", get_synonym(orientation_elements,current_element.get("orientation")))
        hashMap.put("gravity_vertical", get_synonym(vertical_gravity_elements,current_element.get("gravity_vertical")))
        hashMap.put("gravity_horizontal", get_synonym(gravity_elements,current_element.get("gravity_horizontal")))
        
        if "height_element" in current_element:
            hashMap.put("height", get_synonym(scale_elements,current_element.get("manual")))
        else:    
            hashMap.put("height", get_synonym(scale_elements,current_element.get("height")))

        if "width_element" in current_element:
            hashMap.put("width", get_synonym(scale_elements,current_element.get("manual")))
        else:    
            hashMap.put("width", get_synonym(scale_elements,current_element.get("width")))    
        
        

        hashMap.put("drawable", current_element.get("drawable"))
        hashMap.put("Value", current_element.get("Value",""))
        hashMap.put("Variable", current_element.get("Variable",""))
        hashMap.put("BackgroundColor", current_element.get("BackgroundColor",""))
        hashMap.put("StrokeWidth", current_element.get("StrokeWidth",""))
        hashMap.put("Padding", current_element.get("Padding",""))
        hashMap.put("height_value", current_element.get("height_value",""))
        hashMap.put("width_value", current_element.get("width_value",""))
        hashMap.put("weight", current_element.get("weight",""))
        hashMap.put("BackgroundColor", current_element.get("BackgroundColor",""))
        hashMap.put("TextSize", current_element.get("TextSize",""))
        hashMap.put("TextColor", current_element.get("TextColor",""))
        hashMap.put("TextBold", current_element.get("TextBold",""))
        hashMap.put("TextItalic", current_element.get("TextItalic",""))
        hashMap.put("NumberPrecision", current_element.get("NumberPrecision",""))
        hashMap.put("RecognitionTemplate", current_element.get("RecognitionTemplate",""))
        hashMap.put("style_name", current_element.get("style_name",""))



        if "Elements" in current_element:
            hashMap.put("layout_elements_table",json.dumps(make_layoutelements_table(current_element["Elements"]),ensure_ascii=False))
        else:    
            hashMap.put("layout_elements_table",json.dumps(make_layoutelements_table([]),ensure_ascii=False))
    else:
        hashMap.put("layout_elements_table",json.dumps(make_layoutelements_table([]),ensure_ascii=False))
        if  current_parent != (None,None):
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



    is_new_element = current_element == None

    if is_new_element:
        hashMap.put("orientation", get_synonym(orientation_elements,"vertical"))
        hashMap.put("height", get_synonym(scale_elements,"match_parent"))
        hashMap.put("width", get_synonym(scale_elements,"match_parent"))
        hashMap.put("weigth", 0)
    

    hashMap.put("Show_RecognitionTemplate_div","-1") 
    hashMap.put("Show_RecognitionTemplate_p","-1") 
    hashMap.put("Show_RecognitionTemplate","-1")  
    if is_new_element and not current_parent[1]==None:
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
            
            if current_parent[1][0].get("type") == "Operation":
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
            
            if current_parent[1][0].get("type") == "Operation":
                hashMap.put("Show_element_properties","-1")  
                hashMap.put("Show_common_properties","-1")
            else:
                hashMap.put("Show_element_properties","1")      
                hashMap.put("Show_common_properties","1")

    return hashMap


def element_post_open(hashMap,_files=None,_data=None):

     


    return hashMap

def processes_input(hashMap,_files=None,_data=None):
    global current_parent
    global current_parent_dict
    

    global processes_table
    global current_process_name
    global processes_table_id
    global current_element
  
    if hashMap.get("listener")=="btn_add_process":
        #hashMap.put("TableAddRow","processes_table") 
        processes_table_id = -1
        uid = str(uuid.uuid4().hex)
        hashMap.put("process_uid",uid)
        hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"process_form", "key":uid, "reopen":True},ensure_ascii=False))  
        current_process_name = "Новый процесс"
        hashMap.put("process_name",current_process_name)
        hashMap.put("SetTitle",current_process_name+" - *")

        hashMap.put("hidden","")
        hashMap.put("DefineOnBackPressed","")
        hashMap.put("login_screen","")
        hashMap.put("SC","")
        hashMap.put("PlanFactHeader","")
       
        current_element = None
        current_parent =(None,None)

    elif hashMap.get("listener")=="btn_add_processcv":
        #hashMap.put("TableAddRow","processes_table") 
        processes_table_id = -1
        uid = str(uuid.uuid4().hex)
        hashMap.put("process_uid",uid)
        hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"activecv_process_form", "key":uid, "reopen":True},ensure_ascii=False))  
        current_process_name = "Новый ActiveCV"
        hashMap.put("process_name",current_process_name)
        hashMap.put("SetTitle",current_process_name+" - *")

        hashMap.put("hidden","")
      
       
        current_element = None
        current_parent =(None,None)    


    elif hashMap.get("listener")=="btn_edit_process" or hashMap.get("listener")=="TableDoubleClick":
        
        if hashMap.containsKey("selected_line_id"):
         
            processes_table_id = int(hashMap.get("selected_line_id"))
            row = processes_table[processes_table_id]

            if not 'uid' in row:
                row['uid'] = str(uuid.uuid4().hex)

            if row.get("type") == "Process":   

                hashMap.put("process_uid",processes_table[processes_table_id].get("uid"))
                hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"process_form", "key":processes_table[processes_table_id].get("uid"), "reopen":True},ensure_ascii=False))  
                current_process_name = row.get("ProcessName","")
                hashMap.put("process_name",current_process_name)
                hashMap.put("SetTitle",current_process_name)

                hashMap.put("hidden",row.get("hidden"))
                hashMap.put("DefineOnBackPressed",row.get("DefineOnBackPressed"))
                hashMap.put("login_screen",row.get("login_screen"))
                hashMap.put("SC",row.get("SC"))
                hashMap.put("PlanFactHeader",row.get("PlanFactHeader",""))

                current_element = row
                current_parent = (row,None)
                current_parent_dict[processes_table[processes_table_id].get("uid")] = current_parent
            elif row.get("type") == "CVOperation":    
                hashMap.put("process_uid",processes_table[processes_table_id].get("uid"))
                hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"activecv_process_form", "key":processes_table[processes_table_id].get("uid"), "reopen":True},ensure_ascii=False))  
                current_process_name = row.get("CVOperationName","")
                hashMap.put("process_name",current_process_name)
                hashMap.put("SetTitle",current_process_name)

                hashMap.put("hidden",row.get("hidden"))
              
                current_element = row
                current_parent = (row,None)
                current_parent_dict[processes_table[processes_table_id].get("uid")] = current_parent

            hashMap.remove("selected_line_id")

    elif hashMap.get("listener")=="btn_delete_process":
        
        sel_line = 'selected_line_id'
        if hashMap.containsKey(sel_line):
            processes_table.pop(int(hashMap.get(sel_line)))
            
            hashMap.put("RefreshScreen","")
            hashMap.remove(sel_line)
    elif hashMap.get("listener")=="btn_paste":
        hashMap.put("ReadClipboard","")
    elif hashMap.get("listener")=="clipboard_result":
        jprocess = json.loads(hashMap.get("clipboard_result"))
        processes_table.append(jprocess)

        save_configuration(configuration,hashMap) 

        hashMap.put("RefreshScreen","")
        
    elif hashMap.get("listener")=="btn_copy":
        if hashMap.containsKey("selected_line_id"):
            processes_table_id = int(hashMap.get("selected_line_id"))
            row = processes_table[processes_table_id]
            hashMap.put("WriteClipboard",json.dumps(row,ensure_ascii=False))    


    
    return hashMap   

def common_handlers_dialog_on_start(hashMap,_files=None,_data=None):

    hashMap.put("common_events",";".join(events_common))
    hashMap.put("handler_types",";".join(handler_types))
    hashMap.put("action_types",";".join(action_types))
    
    if  "CommonHandlers" in configuration["ClientConfiguration"]:
        hashMap.put("handlers_table",json.dumps(make_handlers_table(configuration["ClientConfiguration"]["CommonHandlers"],True),ensure_ascii=False))
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
    global edit_handler_mode
    global configuration
    

    if hashMap.get("listener") == "btn_add_handler":
        hashMap.put("ShowDialogLayout",json.dumps(handler_layout,ensure_ascii=False))
        hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Обработчик"},ensure_ascii=False))
        hashMap.put("ShowDialog","")

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
        edit_handler_mode = -1
    elif hashMap.get("listener") == "btn_edit_handler" or hashMap.get("listener") == "TableDoubleClick":
        if hashMap.containsKey("selected_line_id"):
            hashMap.put("ShowDialogLayout",json.dumps(handler_layout,ensure_ascii=False))
            hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Обработчик"},ensure_ascii=False))
            hashMap.put("ShowDialog","")

            edit_handler_mode = int(hashMap.get("selected_line_id"))

            handler_str = configuration["ClientConfiguration"]["CommonHandlers"][edit_handler_mode]

            hashMap.put("alias",handler_str.get("alias",""))
            hashMap.put("event",handler_str.get("event",""))
            hashMap.put("action",handler_str.get("action",""))
            hashMap.put("type",handler_str.get("type",""))
            hashMap.put("method",handler_str.get("method",""))
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
                        hashMap.put("method_postExecute",jpe[0].get("method",""))
            
            hashMap.remove("selected_line_id")  

    elif hashMap.get("listener") == "btn_delete_handler":
        if hashMap.containsKey("selected_line_id"):
            pos = int(hashMap.get("selected_line_id"))   
            configuration["ClientConfiguration"]["CommonHandlers"].pop(pos)
            hashMap.put("RefreshScreen","")
            hashMap.remove("selected_line_id")      

    elif hashMap.get("listener") == "onResultPositive": 
        if edit_handler_mode == -1:
            dialog_values = list_to_dict(json.loads(hashMap.get("dialog_values")))

            if not "CommonHandlers" in configuration:
                configuration["ClientConfiguration"]["CommonHandlers"] = []
            
            postExecute = ""
            if len(str(hashMap.get("action_postExecute")))>0 and len(str(hashMap.get("type_postExecute")))>0:
                postExecute =json.dumps( [{"action":dialog_values.get("action_postExecute",""),"type":dialog_values.get("type_postExecute",""),"method":dialog_values.get("method_postExecute","")}], ensure_ascii=False)

            configuration["ClientConfiguration"]["CommonHandlers"].append({"event":dialog_values.get("event",""),"action":dialog_values.get("action",""),"listener":dialog_values.get("listener",""),"type":dialog_values.get("type",""),"method":dialog_values.get("method",""),"postExecute":postExecute,"alias":dialog_values.get("alias","")}) 
            hashMap.put("RefreshScreen","")
        else:
            dialog_values = list_to_dict(json.loads(hashMap.get("dialog_values")))

            postExecute = ""
            if len(str(hashMap.get("action_postExecute")))>0 and len(str(hashMap.get("type_postExecute")))>0:
                postExecute = json.dumps( [{"action":dialog_values.get("action_postExecute",""),"type":dialog_values.get("type_postExecute",""),"method":dialog_values.get("method_postExecute","")}], ensure_ascii=False)

            configuration["ClientConfiguration"]["CommonHandlers"][edit_handler_mode] ={"event":dialog_values.get("event",""),"action":dialog_values.get("action",""),"listener":dialog_values.get("listener",""),"type":dialog_values.get("type",""),"method":dialog_values.get("method",""),"postExecute":postExecute,"alias":dialog_values.get("alias","")} 
            hashMap.put("RefreshScreen","")

    return hashMap

mediafiles_table_id = -1
def mediafiles_input(hashMap,_files=None,_data=None):
    global mediafiles_table_id
    global configuration
  
    if hashMap.get("listener")=="btn_add_mediafile":
        mediafiles_table_id = -1
        hashMap.put("ShowDialogLayout",json.dumps(mediafile_layout,ensure_ascii=False))
        hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Добавление медиафайла"},ensure_ascii=False))
        hashMap.put("ShowDialog","")
        hashMap.put("key","")

    
    elif hashMap.get("listener") == "onResultPositive": 
        if mediafiles_table_id == -1:
            dialog_values = list_to_dict(json.loads(hashMap.get("dialog_values")))

            if not "Mediafile" in configuration["ClientConfiguration"]:
                configuration["ClientConfiguration"]["Mediafile"] = []
            
            if 'base64' in dialog_values:
                filename,ext = os.path.splitext(dialog_values.get("file"))

                configuration["ClientConfiguration"]["Mediafile"].append({"MediafileKey":dialog_values.get("key"),"MediafileExt":ext[1:],"MediafileData":dialog_values.get("base64")}) 
                hashMap.put("RefreshScreen","")
     

    elif hashMap.get("listener")=="btn_delete_mediafile":
        
        sel_line = 'selected_line_id'
        if hashMap.containsKey(sel_line):
            configuration["ClientConfiguration"]["Mediafile"].pop(int(hashMap.get(sel_line)))
            
            hashMap.put("RefreshScreen","")
            hashMap.remove(sel_line)

    
    return hashMap 

def mediafiles_open(hashMap,_files=None,_data=None):

    if "Mediafile" in configuration["ClientConfiguration"]:
        hashMap.put("mediafiles_table",json.dumps(make_mediafiles_table(configuration["ClientConfiguration"]["Mediafile"]),ensure_ascii=False))
    else:    
        hashMap.put("mediafiles_table",json.dumps(make_mediafiles_table([]),ensure_ascii=False))
 
    return hashMap

def activecv_process_open(hashMap,_files=None,_data=None):

    if not current_element == None:
        hashMap.put("steps_table",json.dumps(make_onefield_table(current_element["CVFrames"],"Name","Шаг ActiveCV"),ensure_ascii=False))
    else:
        hashMap.put("steps_table",json.dumps(make_onefield_table([],"Name","Шаг ActiveCV"),ensure_ascii=False))
   
    return hashMap

def activecv_process_input(hashMap,_files=None,_data=None):

    global current_parent
    global current_parent_dict

    global processes_table
    global parent_element
    global processes_table_id
    global screens_table_id
    global current_element

    if current_element==None:
        closeuid  =hashMap.get("process_uid")
    else:    
        closeuid = current_element['uid']

    if hashMap.get("listener")=="btn_save" or hashMap.get("listener")=="btn_add_step" or hashMap.get("listener")=="btn_edit_step":



  

        if processes_table_id==-1:
            processes_table.append({
                                                    "CVOperationName": hashMap.get("process_name"),
                                                    "type":"CVOperation",
                                                    "uid": closeuid,
                                                    "CVFrames":[]
                                                
                                                })
            processes_table_id=len(processes_table)-1

        else:   
            current_element["ProcessName"] =hashMap.get("process_name") 
            current_element["hidden"] =hashMap.get("hidden") 
            current_element["uid"] =closeuid 

        current_parent = (processes_table[processes_table_id],None)
        current_element = current_parent[0]
        current_parent_dict[closeuid] = current_parent

    if hashMap.get("listener")=="btn_save" or hashMap.get("listener")=="btn_close":

        hashMap.put("CloseTab",closeuid)

        hashMap.put("processes_table",json.dumps(make_processes_table(processes_table),ensure_ascii=False))

        hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"main_screen", "key":"Процессы", "reopen":True},ensure_ascii=False))

        save_configuration(configuration,hashMap)

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

                
        screens_table_id = -1
        current_element = None 
        current_parent = (None,current_parent)
        current_parent_dict[uid] = current_parent   
    elif hashMap.get("listener")=="btn_edit_step" or hashMap.get("listener") == "TableDoubleClick":
        screens_table_id = int(hashMap.get("selected_line_id"))
        row = current_element["CVFrames"][screens_table_id]
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

        current_element = row  
        current_parent = (row,current_parent) 
        current_parent_dict[row['uid']] = current_parent      
    elif hashMap.get("listener")=="btn_delete_step":
        
        sel_line = 'selected_line_id'
        if hashMap.containsKey(sel_line):
                current_element['CVFrames'].pop(int(hashMap.get(sel_line)))
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
    if "RecognitionTemplates" in configuration['ClientConfiguration']:
        for t in configuration['ClientConfiguration']["RecognitionTemplates"]:
            recognition_templates.append(t.get('name'))
    hashMap.put("recognition_templates",";".join(recognition_templates)) 

    if not current_element == None:
        if  "Handlers" in current_element:
            hashMap.put("handlers_table",json.dumps(make_handlers_table(current_element["Handlers"],True),ensure_ascii=False))
        else:
            hashMap.put("handlers_table",json.dumps(make_handlers_table([],True),ensure_ascii=False))    
    else:
         hashMap.put("handlers_table",json.dumps(make_handlers_table([],True),ensure_ascii=False))
   
    return hashMap

def step_input(hashMap,_files=None,_data=None):
    global current_parent
    global current_parent_dict

    global processes_table
    global parent_element
    global screens_table_id
   
    global current_element
   
    global process_table_id

    global edit_handler_mode

    closeuid = None

    if current_element==None:
        closeuid = hashMap.get("step_uid")
    else:    
        closeuid = current_element['uid']

    if hashMap.get("listener")=="btn_save" or hashMap.get("listener")=="btn_add_handler":

        

        current_parent =current_parent[1]
        current_element = current_parent[0]

        if screens_table_id==-1:
            current_element['CVFrames'].append({
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
            
            screens_table_id=len(current_element['CVFrames'])-1
            
            
        else:   
            current_element['CVFrames'][screens_table_id]["Name"] = hashMap.get("step_name")
            current_element['CVFrames'][screens_table_id]["uid"] = closeuid

            current_element['CVFrames'][screens_table_id]["CVDetector"] = get_key(detector_elements,hashMap.get("CVDetector"))
            current_element['CVFrames'][screens_table_id]["CVResolution"] = hashMap.get("CVResolution")
            current_element['CVFrames'][screens_table_id]["CVMode"] = get_key(visual_mode_elements,hashMap.get("CVMode"))
            current_element['CVFrames'][screens_table_id]["CVActionButtons"] = hashMap.get("CVActionButtons")
            current_element['CVFrames'][screens_table_id]["CVAction"] = hashMap.get("CVAction")
            current_element['CVFrames'][screens_table_id]["CVInfo"] = hashMap.get("CVInfo")
            current_element['CVFrames'][screens_table_id]["CVCameraDevice"] = get_key(camera_mode_elements,hashMap.get("CVCameraDevice"))
            current_element['CVFrames'][screens_table_id]["CVDetectorMode"] = get_key(detector_mode_elements,hashMap.get("CVDetectorMode"))
            current_element['CVFrames'][screens_table_id]["CVMask"] = hashMap.get("CVMask")
            current_element['CVFrames'][screens_table_id]["RecognitionTemplate"] = hashMap.get("RecognitionTemplate")
               
        
        current_parent = (current_element['CVFrames'][screens_table_id],current_parent)
        current_parent_dict[closeuid] = current_parent

        
        current_element = current_parent[0]
        


    if hashMap.get("listener")=="btn_save" or hashMap.get("listener")=="btn_close":
 
        hashMap.put("CloseTab",closeuid)
        hashMap.put("OpenScreen",json.dumps({"process":"Процессы","screen":"activecv_process_form", "key":current_parent[1][0]['uid'], "reopen":True},ensure_ascii=False))

        current_parent = current_parent[1]
        process_table_id = processes_table.index(current_parent[0])
        current_element = current_parent[0]

        save_configuration(configuration,hashMap)

        #блокировка
        #hashMap.put("UnblockTabs","")
 
   
    elif hashMap.get("listener") == "btn_add_handler":
        hashMap.put("ShowDialogLayout",json.dumps(handler_layout,ensure_ascii=False))
        hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Обработчик"},ensure_ascii=False))
        hashMap.put("ShowDialog","")

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
        edit_handler_mode = -1

    elif hashMap.get("listener") == "btn_edit_handler":
        if hashMap.containsKey("selected_line_id"):
            hashMap.put("ShowDialogLayout",json.dumps(handler_layout,ensure_ascii=False))
            hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Обработчик"},ensure_ascii=False))
            hashMap.put("ShowDialog","")

            edit_handler_mode = int(hashMap.get("selected_line_id"))

            handler_str = current_element['Handlers'][edit_handler_mode]

           
            hashMap.put("event",handler_str.get("event",""))
            hashMap.put("action",handler_str.get("action",""))
            hashMap.put("type",handler_str.get("type",""))
            hashMap.put("method",handler_str.get("method",""))
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
                        hashMap.put("method_postExecute",jpe[0].get("method",""))
            
            hashMap.remove("selected_line_id")  

    elif hashMap.get("listener") == "btn_delete_handler":
        if hashMap.containsKey("selected_line_id"):
            pos = int(hashMap.get("selected_line_id"))   
            current_element['Handlers'].pop(pos)
            hashMap.put("RefreshScreen","")
            hashMap.remove("selected_line_id")      

    elif hashMap.get("listener") == "onResultPositive": 
        if edit_handler_mode == -1:
            dialog_values = list_to_dict(json.loads(hashMap.get("dialog_values")))

            if not "Handlers" in current_element:
                current_element['Handlers'] = []
            
            postExecute = ""
            if len(str(hashMap.get("action_postExecute")))>0 and len(str(hashMap.get("type_postExecute")))>0:
                postExecute =json.dumps( [{"action":dialog_values.get("action_postExecute",""),"type":dialog_values.get("type_postExecute",""),"method":dialog_values.get("method_postExecute","")}], ensure_ascii=False)

            current_element['Handlers'].append({"event":dialog_values.get("event",""),"action":dialog_values.get("action",""),"listener":dialog_values.get("listener",""),"type":dialog_values.get("type",""),"method":dialog_values.get("method",""),"postExecute":postExecute,"alias":dialog_values.get("alias","")}) 
            hashMap.put("RefreshScreen","")
            
        else:
            dialog_values = list_to_dict(json.loads(hashMap.get("dialog_values")))

            postExecute = ""
            if len(str(hashMap.get("action_postExecute")))>0 and len(str(hashMap.get("type_postExecute")))>0:
                postExecute = json.dumps( [{"action":dialog_values.get("action_postExecute",""),"type":dialog_values.get("type_postExecute",""),"method":dialog_values.get("method_postExecute","")}], ensure_ascii=False)

            current_element['Handlers'][edit_handler_mode] ={"event":dialog_values.get("event",""),"action":dialog_values.get("action",""),"listener":dialog_values.get("listener",""),"type":dialog_values.get("type",""),"method":dialog_values.get("method",""),"postExecute":postExecute,"alias":dialog_values.get("alias","")} 
            hashMap.put("RefreshScreen","")
           


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
    

recognition_table_id = -1
def recognition_input(hashMap,_files=None,_data=None):
    global recognition_table_id
    global configuration
  
    if hashMap.get("listener")=="btn_add_ocr":
        recognition_table_id = -1
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
        recognition_table_id = -2
        hashMap.put("ShowDialogLayout",json.dumps(date_layout,ensure_ascii=False))
        hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Добавление Распознавание дат"},ensure_ascii=False))
        hashMap.put("ShowDialog","")

       
        hashMap.put("name","")
        hashMap.put("result_field","")
    
    elif hashMap.get("listener")=="btn_add_number":
        recognition_table_id = -3
        hashMap.put("ShowDialogLayout",json.dumps(number_layout,ensure_ascii=False))
        hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Добавление Распознавание чисел"},ensure_ascii=False))
        hashMap.put("ShowDialog","")

        hashMap.put("name","")
        hashMap.put("result_field","")
        hashMap.put("count_objects","")
    
    elif hashMap.get("listener")=="btn_add_platenumbers":
        recognition_table_id = -4
        hashMap.put("ShowDialogLayout",json.dumps(platenumber_layout,ensure_ascii=False))
        hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Добавление Распознавание автомобильных номеров"},ensure_ascii=False))
        hashMap.put("ShowDialog","")

        hashMap.put("name","")
        hashMap.put("result_field","")

    elif hashMap.get("listener")=="btn_edit_recognition" or hashMap.get("listener") == "TableDoubleClick":
        if hashMap.containsKey("selected_line_id"):
            recognition_table_id = int(hashMap.get("selected_line_id"))
            row = configuration['ClientConfiguration']["RecognitionTemplates"][recognition_table_id]     
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
        
        if not "RecognitionTemplates" in configuration['ClientConfiguration']:
                configuration['ClientConfiguration']["RecognitionTemplates"] = []

        
        if recognition_table_id == -1:
            configuration['ClientConfiguration']["RecognitionTemplates"].append(
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
        elif recognition_table_id == -2:
            configuration['ClientConfiguration']["RecognitionTemplates"].append(
                {"name":dialog_values.get("name"),
                 "DateRecognition":  True,                 
                 "result_field":dialog_values.get("result_field"),
                 })             
        elif recognition_table_id == -3:
            configuration['ClientConfiguration']["RecognitionTemplates"].append(
                {"name":dialog_values.get("name"),
                 "NumberRecognition":  True,                 
                 "result_field":dialog_values.get("result_field"),
                 "count_objects":dialog_values.get("count_objects"),
                 })             
        elif recognition_table_id == -4:
            configuration['ClientConfiguration']["RecognitionTemplates"].append(
                {"name":dialog_values.get("name"),
                 "PlateNumberRecognition":  True,                 
                 "result_field":dialog_values.get("result_field"),
                 })  
        else:
            if hashMap.containsKey("selected_line_id"):

                pos = int(hashMap.get("selected_line_id"))
                row = configuration['ClientConfiguration']["RecognitionTemplates"][pos]     
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
     

    elif hashMap.get("listener")=="btn_delete_recognition":
        
        sel_line = 'selected_line_id'
        if hashMap.containsKey(sel_line):
            configuration['ClientConfiguration']["RecognitionTemplates"].pop(int(hashMap.get(sel_line)))
            
            hashMap.put("RefreshScreen","")
            hashMap.remove(sel_line)

    
    return hashMap 

def recognition_open(hashMap,_files=None,_data=None):

    if "RecognitionTemplates" in configuration['ClientConfiguration']:
        hashMap.put("recognition_table",json.dumps(make_onefield_table(configuration['ClientConfiguration']["RecognitionTemplates"],"name","Имя"),ensure_ascii=False))
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
                    "Value": "@raw",
                    "Variable": "raw",
                    "gravity_horizontal": "left"
                }

            ]
        }




styles_table_id = -1
def styles_input(hashMap,_files=None,_data=None):
    global styles_table_id
    global configuration

    element_base = screen_elements
  
    if hashMap.get("listener")=="btn_add_style":
        styles_table_id = -1
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
        hashMap.put("raw", "")
   
   
    elif hashMap.get("listener")=="btn_edit_style" or hashMap.get("listener") == "TableDoubleClick":
        if hashMap.containsKey("selected_line_id"):
            styles_table_id = int(hashMap.get("selected_line_id"))
            current_element = configuration['ClientConfiguration']["StyleTemplates"][styles_table_id]     
            
            hashMap.put("ShowDialogLayout",json.dumps(style_layout,ensure_ascii=False))
            hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Редактирование таймера"},ensure_ascii=False))
            hashMap.put("ShowDialog","")

            hashMap.put("name",current_element.get("name"))

            #hashMap.put("gravity_vertical", get_synonym(element_base,current_element.get("gravity_vertical")))
            hashMap.put("gravity_horizontal", get_synonym(element_base,current_element.get("gravity_horizontal")))
            
            if "height_element" in current_element:
                hashMap.put("height", get_synonym(element_base,current_element.get("manual")))
            else:    
                hashMap.put("height", get_synonym(element_base,current_element.get("height")))

            if "width_element" in current_element:
                hashMap.put("width", get_synonym(element_base,current_element.get("manual")))
            else:    
                hashMap.put("width", get_synonym(element_base,current_element.get("width")))    
            
            

            hashMap.put("BackgroundColor", current_element.get("BackgroundColor",""))
            hashMap.put("StrokeWidth", current_element.get("StrokeWidth",""))
            hashMap.put("Padding", current_element.get("Padding",""))
            hashMap.put("height_value", current_element.get("height_value",""))
            hashMap.put("width_value", current_element.get("width_value",""))
            hashMap.put("weight", current_element.get("weight",""))
            hashMap.put("BackgroundColor", current_element.get("BackgroundColor",""))
            hashMap.put("TextSize", current_element.get("TextSize",""))
            hashMap.put("TextColor", current_element.get("TextColor",""))
            hashMap.put("TextBold", current_element.get("TextBold",""))
            hashMap.put("TextItalic", current_element.get("TextItalic",""))
            hashMap.put("NumberPrecision", current_element.get("NumberPrecision",""))
            hashMap.put("use_as_class", current_element.get("use_as_class",""))
            hashMap.put("raw", current_element.get("raw",""))
            
          
    
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
        
        if not "StyleTemplates" in configuration['ClientConfiguration']:
                configuration['ClientConfiguration']["StyleTemplates"] = []

        
        if styles_table_id == -1:
            d =  {"name":dialog_values.get("name"),
                #"gravity_vertical":get_key(element_base,dialog_values.get("gravity_vertical")),
                "height":height,
                "width":width,
                "drawable":dialog_values.get("drawable"),
                "gravity_horizontal":get_key(gravity_elements,dialog_values.get("gravity_horizontal")),
                "BackgroundColor":dialog_values.get("BackgroundColor"),
                "StrokeWidth":dialog_values.get("StrokeWidth"),
                "weight":dialog_values.get("weight"),
                "TextSize":dialog_values.get("TextSize"),
                "TextColor":dialog_values.get("TextColor"),
                "TextBold":dialog_values.get("TextBold"),
                "TextItalic":dialog_values.get("TextItalic"),
                "NumberPrecision":dialog_values.get("NumberPrecision"),
                "use_as_class":dialog_values.get("use_as_class"),
                "raw":dialog_values.get("raw"),
 
                }
            if dialog_values.get("use_as_class")==True:
                d["style_class"] = dialog_values.get("name")
            configuration['ClientConfiguration']["StyleTemplates"].append(d)
        else:
           configuration["StyleTemplates"][styles_table_id]["name"] =  dialog_values.get("name")
           if dialog_values.get("use_as_class")==True:
                configuration['ClientConfiguration']["StyleTemplates"][styles_table_id]["style_class"] = dialog_values.get("name")
           
           #configuration["StyleTemplates"][recognition_table_id]['gravity_vertical'] = get_key(element_base,hashMap.get("gravity_vertical"))
           configuration['ClientConfiguration']["StyleTemplates"][styles_table_id]['gravity_horizontal'] = get_key(gravity_elements,dialog_values.get("gravity_horizontal"))
           configuration['ClientConfiguration']["StyleTemplates"][styles_table_id]['height'] = height
           configuration['ClientConfiguration']["StyleTemplates"][styles_table_id]['width'] = width
           configuration['ClientConfiguration']["StyleTemplates"][styles_table_id]['BackgroundColor'] = dialog_values.get("BackgroundColor")
           configuration['ClientConfiguration']["StyleTemplates"][styles_table_id]['StrokeWidth'] = dialog_values.get("StrokeWidth")
           configuration['ClientConfiguration']["StyleTemplates"][styles_table_id]['Padding'] = dialog_values.get("Padding")
           configuration['ClientConfiguration']["StyleTemplates"][styles_table_id]['height_value'] = dialog_values.get("height_value")
           configuration['ClientConfiguration']["StyleTemplates"][styles_table_id]['width_value'] = dialog_values.get("width_value")
           configuration['ClientConfiguration']["StyleTemplates"][styles_table_id]['weight'] = dialog_values.get("weight")
           configuration['ClientConfiguration']["StyleTemplates"][styles_table_id]['TextSize'] = dialog_values.get("TextSize")
           configuration['ClientConfiguration']["StyleTemplates"][styles_table_id]['TextColor'] = dialog_values.get("TextColor")
           configuration['ClientConfiguration']["StyleTemplates"][styles_table_id]['TextBold'] = dialog_values.get("TextBold")
           configuration['ClientConfiguration']["StyleTemplates"][styles_table_id]['TextItalic'] = dialog_values.get("TextItalic")
           configuration['ClientConfiguration']["StyleTemplates"][styles_table_id]['NumberPrecision'] = dialog_values.get("NumberPrecision") 
           configuration['ClientConfiguration']["StyleTemplates"][styles_table_id]['use_as_class'] = dialog_values.get("use_as_class")
           configuration['ClientConfiguration']["StyleTemplates"][styles_table_id]['raw'] = dialog_values.get("raw")
                       
          

        if hashMap.containsKey("selected_line_id"):
            hashMap.remove("selected_line_id")

        hashMap.put("RefreshScreen","")       
     

    elif hashMap.get("listener")=="btn_delete_style":
        
        sel_line = 'selected_line_id'
        if hashMap.containsKey(sel_line):
            configuration['ClientConfiguration']["StyleTemplates"].pop(int(hashMap.get(sel_line)))
            
            hashMap.put("RefreshScreen","")
            hashMap.remove(sel_line)

    
    return hashMap 

def styles_open(hashMap,_files=None,_data=None):

    hashMap.put("height_elements",captions_scale_elements)
    hashMap.put("width_elements",captions_scale_elements)
    hashMap.put("drawable_elements",";".join(icon_elements))
    hashMap.put("gravity_horizontal_elements",captions_gravity_elements)
    hashMap.put("vertical_gravity_elements",captions_vertical_gravity_elements)


    if "StyleTemplates" in configuration['ClientConfiguration']:
        hashMap.put("styles_table",json.dumps(make_onefield_table(configuration['ClientConfiguration']["StyleTemplates"],"name","Имя"),ensure_ascii=False))
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



timers_table_id = -1
def timers_input(hashMap,_files=None,_data=None):
    global timers_table_id
    global configuration

   
  
    if hashMap.get("listener")=="btn_add_timer":
        timers_table_id = -1
        hashMap.put("ShowDialogLayout",json.dumps(timers_layout,ensure_ascii=False))
        hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Добавление таймера"},ensure_ascii=False))
        hashMap.put("ShowDialog","")
        
        hashMap.put("PyTimerTaskKey","")
        hashMap.put("PyTimerTaskDef","")
        hashMap.put("PyTimerTaskPeriod","")
        hashMap.put("PyTimerTaskBuilIn","")
  
   
    elif hashMap.get("listener")=="btn_edit_timer" or hashMap.get("listener") == "TableDoubleClick":
        if hashMap.containsKey("selected_line_id"):
            timers_table_id = int(hashMap.get("selected_line_id"))
            current_element = configuration["ClientConfiguration"]["PyTimerTask"][timers_table_id]     
            
            hashMap.put("ShowDialogLayout",json.dumps(timers_layout,ensure_ascii=False))
            hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Редактирование таймера"},ensure_ascii=False))
            hashMap.put("ShowDialog","")

            hashMap.put("PyTimerTaskKey",current_element.get("PyTimerTaskKey"))
            hashMap.put("PyTimerTaskDef",current_element.get("PyTimerTaskDef"))
            hashMap.put("PyTimerTaskPeriod",current_element.get("PyTimerTaskPeriod"))
            hashMap.put("PyTimerTaskBuilIn",current_element.get("PyTimerTaskBuilIn"))
    
    elif hashMap.get("listener") == "onResultPositive": 
        dialog_values = list_to_dict(json.loads(hashMap.get("dialog_values")))
        
        if not "PyTimerTask" in configuration["ClientConfiguration"]:
                configuration["ClientConfiguration"]["PyTimerTask"] = []
        
        if timers_table_id == -1:
            d =  {"PyTimerTaskKey":dialog_values.get("PyTimerTaskKey"),
             "PyTimerTaskDef":dialog_values.get("PyTimerTaskDef"),
             "PyTimerTaskPeriod":dialog_values.get("PyTimerTaskPeriod"),
             "PyTimerTaskBuilIn":dialog_values.get("PyTimerTaskBuilIn")
                }

            configuration["ClientConfiguration"]["PyTimerTask"].append(d)
        else:
           configuration["ClientConfiguration"]["PyTimerTask"][timers_table_id]["PyTimerTaskKey"] =  dialog_values.get("PyTimerTaskKey")
           configuration["ClientConfiguration"]["PyTimerTask"][timers_table_id]["PyTimerTaskDef"] =  dialog_values.get("PyTimerTaskDef")
           configuration["ClientConfiguration"]["PyTimerTask"][timers_table_id]["PyTimerTaskPeriod"] =  dialog_values.get("PyTimerTaskPeriod")
           configuration["ClientConfiguration"]["PyTimerTask"][timers_table_id]["PyTimerTaskBuilIn"] =  dialog_values.get("PyTimerTaskBuilIn")
                      
          

        if hashMap.containsKey("selected_line_id"):
            hashMap.remove("selected_line_id")

        hashMap.put("RefreshScreen","")       
     

    elif hashMap.get("listener")=="btn_delete_timer":
        
        sel_line = 'selected_line_id'
        if hashMap.containsKey(sel_line):
            configuration["ClientConfiguration"]["PyTimerTask"].pop(int(hashMap.get(sel_line)))
            
            hashMap.put("RefreshScreen","")
            hashMap.remove(sel_line)

    
    return hashMap 

def timers_open(hashMap,_files=None,_data=None):

    if "PyTimerTask" in configuration["ClientConfiguration"]:
        hashMap.put("timers_table",json.dumps(make_timers_table(configuration["ClientConfiguration"]["PyTimerTask"]),ensure_ascii=False))
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

modules_table_id = -1
handlers_file_type = -1
def modules_input(hashMap,_files=None,_data=None):
    global modules_table_id
    global handlers_file_type
    global configuration
  
    if hashMap.get("listener")=="btn_add_file":
        modules_table_id = -1
        hashMap.put("ShowDialogLayout",json.dumps(module_layout,ensure_ascii=False))
        hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Добавление модуля"},ensure_ascii=False))
        hashMap.put("ShowDialog","")
        hashMap.put("key","")

    
    elif hashMap.get("listener") == "onResultPositive": 
        if modules_table_id == -1:
            dialog_values = list_to_dict(json.loads(hashMap.get("dialog_values")))

            if not "PyFiles" in configuration["ClientConfiguration"]:
                    configuration["ClientConfiguration"]["PyFiles"] = []
            
            if 'base64' in dialog_values:
                

                filename,ext = os.path.splitext(dialog_values.get("file"))

                if ext[1:]=='py':
                    configuration["ClientConfiguration"]["PyFiles"].append({"PyFileKey":dialog_values.get("key"),"PyFileData":dialog_values.get("base64")}) 
                
            else:

                if len(dialog_values.get("url",""))>0:
                    configuration["ClientConfiguration"]["PyFiles"].append({"PyFileKey":dialog_values.get("key"),"PyFileLink":dialog_values.get("url")})     
                else:    
                    configuration["ClientConfiguration"]["PyFiles"].append({"PyFileKey":dialog_values.get("key")})     

        hashMap.put("RefreshScreen","")

    elif hashMap.get("listener")=="btn_delete_file":
        
        sel_line = 'selected_line_id'
        if hashMap.containsKey(sel_line):
            configuration["ClientConfiguration"]["PyFiles"].pop(int(hashMap.get(sel_line)))
            
            hashMap.put("RefreshScreen","")
            hashMap.remove(sel_line)

    elif hashMap.get("listener")=="btn_load_handlers" and hashMap.containsKey("handlers_file"):
        if ".py" in hashMap.get("handlers_file"):
            handlers_file_type=1
            hashMap.put("UploadFile","handlers_file")
    elif     hashMap.get("listener")=="upload_file":

        filename = hashMap.get("base_path")+os.sep+"uploads"+os.sep+ hashMap.get("filename")

        if handlers_file_type==1:
            with open(filename, 'r',encoding='utf-8') as file:
                data = file.read()

            base64file  = base64.b64encode(data.encode('utf-8')).decode('utf-8') 
            configuration["ClientConfiguration"]["PyHandlers"]=base64file
    elif hashMap.get("listener")=="btn_handlers_save":        
        configuration["ClientConfiguration"]["GitHubHandlers"] = hashMap.get("handlers_url")
        configuration["ClientConfiguration"]["GitHubToken"] = hashMap.get("handlers_token")
        

        

      

    
    return hashMap 

def modules_open(hashMap,_files=None,_data=None):

    

    header1 = """<!DOCTYPE html>
<html>
<head>

</head>
<body>
<h3 style="font-size:14px; ">Можно использовать 3 варианта работы с модулями python</h3>
<h3 style="font-size:14px; "><u>Вариант 1: Использовать GitHub приватный или публичный.</u></h3>
<ol>
  <li style="font-size:12px; ">Укажите URL основного файла обработчиков на GitHub в таком виде:
<b>https://api.github.com/repos/<ваш гитхаб>/<ваше репо>/contents/<имя файла.py></b>
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
<h3 style="font-size:14px; "><u>Вариант 2: Использовать программу-агент на локальном компьютере, которая будет отслеживать изменения в локальных файлах и передавать их в конфигурацию автоматически.</u></h3>
<ol>
  <li style="font-size:12px; ">Включите галочку Использовать агент на закладке Конфигурация и сохраните конфигурацию</li>
  <li style="font-size:12px; ">При необходимости укажите ключи дополнительных модулей, не указывая больше ничего</li>
  <li style="font-size:12px; ">Скачайте и запустите constructor_agent</li>
  <li style="font-size:12px; ">Укажите URL веб-конструктора и ID публикации: <a href="{{docdata.url}}">{{ docdata.url }}</a> и <b>{{docdata.uid}}</b></li>
  
  <a href="https://ibb.co/2WfVhxr"><img src="https://i.ibb.co/k5WbBjT/agent.png" alt="agent" border="0"></a>

  <li style="font-size:12px; ">Нажмите Connect (также при необходимости этой кнопкой можно обновить состав)</li>
  <li style="font-size:12px; ">Изменения отслеживаются каждую секунду, при сохранении конфигурации измененные тексты модулей будут применены в конфигурации</li>
</ol>  

<h3 style="font-size:14px; "><u>Вариант 3: просто указать файлы.</u></h3>
<ol>
  <li style="font-size:12px; ">Укажите файлы python модуля обработчиков, при необходимости дополнительных модулей и они применятся сразу же</li>
  <li style="font-size:12px; ">Изменения не отслеживаются. При изменениях в модулях требуется вручную повторить п.1</li>
</ol>  
</body>
</html>
"""

    link = "http://"+ socket.gethostbyname(socket.gethostname())+":"+str(WSPORT)

    t = Template(header2)
    docdata = { 'url': link, 'uid': host_uid }
   


    res = t.render(docdata=docdata)

    hashMap.put("header2",res)
    hashMap.put("handlers_url",configuration["ClientConfiguration"].get("GitHubHandlers",""))
    hashMap.put("handlers_token",configuration["ClientConfiguration"].get("GitHubToken",""))
    hashMap.put("agent",configuration["ClientConfiguration"].get("agent",""))

    if "PyFiles" in configuration["ClientConfiguration"]:
        hashMap.put("modules_table",json.dumps(make_onefield_table(configuration["ClientConfiguration"]["PyFiles"],"PyFileKey","file"),ensure_ascii=False))
    else:    
        hashMap.put("modules_table",json.dumps(make_onefield_table([],"PyFileKey","file"),ensure_ascii=False))
 
    return hashMap


def layouts_open(hashMap,_files=None,_data=None):
    


 
    if "Layouts" in configuration["ClientConfiguration"]:
        hashMap.put("layouts_table",json.dumps(make_onefield_table(configuration["ClientConfiguration"]["Layouts"],"Variable","Переменная"),ensure_ascii=False))
    else:    
        hashMap.put("layouts_table",json.dumps(make_onefield_table([],"Variable","Переменная"),ensure_ascii=False))
 
    return hashMap

def layouts_input(hashMap,_files=None,_data=None):
    global current_parent
    global current_parent_dict
    

    global processes_table
    global parent_element

    global elements_table_id
    global current_element
    #global parent_elelments_element
    global process_table_id

    global edit_handler_mode
    global configuration
    global layouts_edit

    layouts_edit = True
 
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
        
                
        elements_table_id = -1
        current_element = None  

        current_parent = (current_element,None)
        current_parent_dict[uid] = current_parent 

    elif hashMap.get("listener")=="btn_edit_element" or hashMap.get("listener") == "TableDoubleClick":
        
        if hashMap.containsKey("selected_line_id"):
            elements_table_id = int(hashMap.get("selected_line_id"))
            row = configuration["ClientConfiguration"]["Layouts"][elements_table_id]
            
            if not 'uid' in row:
                row['uid'] = str(uuid.uuid4().hex)
            
            hashMap.put("OpenScreen",json.dumps({"process":"Контейнеры","screen":"element_form","key":row['uid'],"reopen":True,"no_close":True},ensure_ascii=False))  
            #current_screen_name = row.get("Name")
            #hashMap.put("screen_name",current_screen_name)
            hashMap.put("SetTitle",row.get("type"))

            hashMap.put("element_uid",row.get("uid"))

            #parent_elelments_element = current_element

            current_parent = (row,None)
            current_parent_dict[row['uid']] = current_parent

            current_element = row     

            hashMap.remove("selected_line_id")  

    elif hashMap.get("listener")=="btn_delete_element":
        sel_line = 'selected_line_id'
        if hashMap.containsKey(sel_line):
                configuration["ClientConfiguration"]["Layouts"].pop(int(hashMap.get(sel_line)))
                hashMap.put("RefreshScreen","")
                hashMap.remove(sel_line)    

    elif hashMap.get("listener") == "btn_add_handler":
        hashMap.put("ShowDialogLayout",json.dumps(handler_layout,ensure_ascii=False))
        hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Обработчик"},ensure_ascii=False))
        hashMap.put("ShowDialog","")

        
        hashMap.put("event","")
        hashMap.put("action","")
        hashMap.put("type","")
        hashMap.put("method","")
        hashMap.put("listener","")

        hashMap.put("action_postExecute","")
        hashMap.put("type_postExecute","")
        hashMap.put("method_postExecute","")

        postExecute = ""
        edit_handler_mode = -1
    elif hashMap.get("listener") == "btn_edit_handler" or hashMap.get("listener") == "TableDoubleClick":
        if hashMap.containsKey("selected_line_id"):
            hashMap.put("ShowDialogLayout",json.dumps(handler_layout,ensure_ascii=False))
            hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Обработчик"},ensure_ascii=False))
            hashMap.put("ShowDialog","")

            edit_handler_mode = int(hashMap.get("selected_line_id"))

            handler_str = current_element['Handlers'][edit_handler_mode]

           
            hashMap.put("event",handler_str.get("event",""))
            hashMap.put("action",handler_str.get("action",""))
            hashMap.put("type",handler_str.get("type",""))
            hashMap.put("method",handler_str.get("method",""))
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
                        hashMap.put("method_postExecute",jpe[0].get("method",""))
            
            hashMap.remove("selected_line_id")  

    elif hashMap.get("listener") == "btn_delete_handler":
        if hashMap.containsKey("selected_line_id"):
            pos = int(hashMap.get("selected_line_id"))   
            current_element['Handlers'].pop(pos)
            hashMap.put("RefreshScreen","")
            hashMap.remove("selected_line_id")      

    elif hashMap.get("listener") == "onResultPositive": 
        if edit_handler_mode == -1:
            dialog_values = list_to_dict(json.loads(hashMap.get("dialog_values")))

            if not "Handlers" in current_element:
                current_element['Handlers'] = []
            
            postExecute = ""
            if len(str(hashMap.get("action_postExecute")))>0 and len(str(hashMap.get("type_postExecute")))>0:
                postExecute =json.dumps( [{"action":dialog_values.get("action_postExecute",""),"type":dialog_values.get("type_postExecute",""),"method":dialog_values.get("method_postExecute","")}], ensure_ascii=False)

            current_element['Handlers'].append({"event":dialog_values.get("event",""),"action":dialog_values.get("action",""),"listener":dialog_values.get("listener",""),"type":dialog_values.get("type",""),"method":dialog_values.get("method",""),"postExecute":postExecute,"alias":dialog_values.get("alias","")}) 
            hashMap.put("RefreshScreen","")
            hashMap.put("callSelectTab","Обработчики")
            hashMap.put("SelectTab","Обработчики")
            
        else:
            dialog_values = list_to_dict(json.loads(hashMap.get("dialog_values")))

            postExecute = ""
            if len(str(hashMap.get("action_postExecute")))>0 and len(str(hashMap.get("type_postExecute")))>0:
                postExecute = json.dumps( [{"action":dialog_values.get("action_postExecute",""),"type":dialog_values.get("type_postExecute",""),"method":dialog_values.get("method_postExecute","")}], ensure_ascii=False)

            current_element['Handlers'][edit_handler_mode] ={"event":dialog_values.get("event",""),"action":dialog_values.get("action",""),"listener":dialog_values.get("listener",""),"type":dialog_values.get("type",""),"method":dialog_values.get("method",""),"postExecute":postExecute,"alias":dialog_values.get("alias","")} 
            hashMap.put("RefreshScreen","")
            hashMap.put("callSelectTab","Обработчики")
            hashMap.put("SelectTab","Обработчики")
           


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

<p><font style="font-size: 20px !important;">Мои статьи на Инфостарт <a href="https://infostart.ru/profile/129563/public/" target="_blank">http://simpleui.ru/</a></font></p>

</div>

<p>(c) Dmitry Votontsov, 2023 </p>

"""




    
    hashMap.put("html",htmlstring)
    
 
    return hashMap


def source_code(hashMap,_files=None,_data=None):

    
    source = json.dumps(configuration,ensure_ascii=False,indent=4,separators=(',', ': '))

    htmlstring = """
    <!DOCTYPE html>
<html>
<body><span style="white-space: pre-wrap">"""+source+"""</span></body>
</html>
"""

    hashMap.put("html", htmlstring)  

    return hashMap

def menu_open(hashMap,_files=None,_data=None):
    hashMap.put("main_menu_elements",";".join(main_menu_elements))

    if "MainMenu" in configuration["ClientConfiguration"]:
        hashMap.put("menu_table",json.dumps(make_menu_table(configuration["ClientConfiguration"]["MainMenu"]),ensure_ascii=False))
    else:    
        hashMap.put("menu_table",json.dumps(make_menu_table([]),ensure_ascii=False))
 
    return hashMap

menu_table_id = -1
def menu_input(hashMap,_files=None,_data=None):
    global menu_table_id
    global configuration

   
  
    if hashMap.get("listener")=="btn_add_menu":
        menu_table_id = -1
        hashMap.put("ShowDialogLayout",json.dumps(menu_layout,ensure_ascii=False))
        hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Добавление меню"},ensure_ascii=False))
        hashMap.put("ShowDialog","")
        
        hashMap.put("MenuItem","")
        hashMap.put("MenuTitle","")
        hashMap.put("MenuId","")
        hashMap.put("MenuTop","")
  
   
    elif hashMap.get("listener")=="btn_edit_menu" or hashMap.get("listener") == "TableDoubleClick":
        if hashMap.containsKey("selected_line_id"):
            menu_table_id = int(hashMap.get("selected_line_id"))
            current_element = configuration["ClientConfiguration"]["MainMenu"][menu_table_id]     
            
            hashMap.put("ShowDialogLayout",json.dumps(menu_layout,ensure_ascii=False))
            hashMap.put("ShowDialogStyle",json.dumps({"yes":"Сохранить","no":"Отмена","title":"Редактирование меню"},ensure_ascii=False))
            hashMap.put("ShowDialog","")

            hashMap.put("MenuItem",current_element.get("MenuItem"))
            hashMap.put("MenuTitle",current_element.get("MenuTitle"))
            hashMap.put("MenuId",current_element.get("MenuId"))
            hashMap.put("MenuTop",current_element.get("MenuTop"))
    
    elif hashMap.get("listener") == "onResultPositive": 
        dialog_values = list_to_dict(json.loads(hashMap.get("dialog_values")))
        
        if not "MainMenu" in configuration["ClientConfiguration"]:
                configuration["ClientConfiguration"]["MainMenu"] = []
        
        if menu_table_id == -1:
            d =  {"MenuItem":dialog_values.get("MenuItem"),
             "MenuTitle":dialog_values.get("MenuTitle"),
             "MenuId":dialog_values.get("MenuId"),
             "MenuTop":dialog_values.get("MenuTop")
                }

            configuration["ClientConfiguration"]["MainMenu"].append(d)
        else:
           configuration["ClientConfiguration"]["MainMenu"][menu_table_id]["MenuItem"] =  dialog_values.get("MenuItem")
           configuration["ClientConfiguration"]["MainMenu"][menu_table_id]["MenuTitle"] =  dialog_values.get("MenuTitle")
           configuration["ClientConfiguration"]["MainMenu"][menu_table_id]["MenuId"] =  dialog_values.get("MenuId")
           configuration["ClientConfiguration"]["MainMenu"][menu_table_id]["MenuTop"] =  dialog_values.get("MenuTop")
                      
          

        if hashMap.containsKey("selected_line_id"):
            hashMap.remove("selected_line_id")

        hashMap.put("RefreshScreen","")       
     

    elif hashMap.get("listener")=="btn_delete_memu":
        
        sel_line = 'selected_line_id'
        if hashMap.containsKey(sel_line):
            configuration["ClientConfiguration"]["MainMenu"].pop(int(hashMap.get(sel_line)))
            
            hashMap.put("RefreshScreen","")
            hashMap.remove(sel_line)

    
    return hashMap 
