import bs4
from bs4 import BeautifulSoup as sp
import os
from xml.etree import ElementTree as ET

SOURCE_HTML_PATH = 'sourceHTML'
OUTPUT_HTML_PATH = 'outputHTML'
OUTPUT_XML_PATH = 'outputXML'
OUTPUT_XML_PATH_2 = 'outputXML2'

def indent(elem, level=0):
    i = "\n" + level*"\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

clean_list = [OUTPUT_HTML_PATH,OUTPUT_XML_PATH,OUTPUT_XML_PATH_2]

for item in clean_list:
    for file in os.listdir(item):
        os.remove(item+'/'+file)

for file in os.listdir(SOURCE_HTML_PATH):
    i = 1
    print(SOURCE_HTML_PATH+'/'+file)
    try:
        soup = sp(open(SOURCE_HTML_PATH+'/'+file))
    except:
        with open('log','a') as f:
            f.write('Error : '+SOURCE_HTML_PATH+'/'+file+'\n')
    root = ET.Element('po')
    root2 = ET.Element('po')
    id_list = []
    try:
        for child in soup.html.descendants:
            if isinstance(child,bs4.element.Tag):
                if child.name == 'head':
                    js_inc_tag = soup.new_tag("script",type="text/javascript",src="lang/b28n.js")
                    child.append(js_inc_tag)
                    js_lang_tag = soup.new_tag("script",language="javascript")
                    js_lang_tag.string="setLanguage('<%ejGet(webUILanguage)%>');\n\tButterlate.setTextDomain('{}');\n\t".format(file.split('.')[0])
                    child.append(js_lang_tag)
                # print(child)
                if (child.string != None) and (child.name not in (['script','None','style']) and child.name in ['button','datalist','option','input','span']):
                    try:
                        # print(child['id'])
                        ET.SubElement(root,'msg',{"id":child['id'],"str":child.get_text()+'222'})
                        ET.SubElement(root2,'msg',{"id":child['id'],"str":child.get_text()+'111'})
                        id_list.append('"'+child['id']+'"')
                    except:
                        child['id'] = file.split('.')[0]+str(i)
                        i = i + 1
                        ET.SubElement(root,'msg',{"id":child['id'],"str":child.get_text()+'222'})
                        ET.SubElement(root2,'msg',{"id":child['id'],"str":child.get_text()+'111'})
                        id_list.append('"'+child['id']+'"')
            elif isinstance(child,bs4.element.NavigableString):
                if child.parent.name not in ['script','span','button','datalist','option','input','None','style','title'] and type(child) != bs4.element.Comment \
                    and child.replace(' ','').replace('\t','').replace('\n','') != '' and child != u'\xa0' and child != '&nbsp' and child != '':
                    span_tag = child.wrap(soup.new_tag('span'))
                    span_tag['id'] = file.split('.')[0]+str(i)
                    i = i + 1
                    ET.SubElement(root,'msg',{"id":span_tag['id'],"str":span_tag.get_text()+'222'})
                    ET.SubElement(root2,'msg',{"id":span_tag['id'],"str":span_tag.get_text()+'111'})
                    id_list.append('"'+span_tag['id']+'"')
        init_id_func_tag = soup.new_tag("script",language="javascript")
        init_id_func_tag.string = 'function initTranslation() {{\n\tvar idArray = new Array({});\n\tsetAllIdValue(idArray);\n}}'.format(','.join(id_list))
        soup.head.append(init_id_func_tag)
        try:
            temp = soup.body['onLoad'] 
        except:
            try:
                temp = soup.body['onload']
            except:
                soup.body['onLoad'] = 'initTranslation()'
            else:
                soup.body['onload'] = soup.body['onload']+';initTranslation()'
        else:
            soup.body['onLoad'] = soup.body['onLoad']+';initTranslation()'
    except:
        with open('log','a') as f:
            f.write('Error : '+SOURCE_HTML_PATH+'/'+file+'\n')
    with open(OUTPUT_HTML_PATH+'/'+file,'w') as f:
        try:
            f.write(soup.prettify())
        except:
            with open('log','a') as f:
                f.write('Error : '+SOURCE_HTML_PATH+'/'+file+'\n')
    indent(root)
    indent(root2)
    tree = ET.ElementTree(root)
    tree2 = ET.ElementTree(root2)
    tree.write(OUTPUT_XML_PATH+'/'+file.split('.')[0]+'.xml','utf-8',True)
    tree2.write(OUTPUT_XML_PATH_2+'/'+file.split('.')[0]+'.xml','utf-8',True)