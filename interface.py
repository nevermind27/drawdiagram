import PySimpleGUI as sg
import pyalg


from selenium import webdriver

#add function that reads from file
def read_code(code,field,name,type,lang):
    if (lang=='Python' and type=='Функциональный'):
        pyalg.make_flowchart(code,field,name)
        driver = webdriver.Edge()
        driver.get("file:///C:/Users/user/PycharmProjects/trps_final/output.html")
        driver.find_element("link text",
                            "PNG - Click here to download current rendered flowchart as py" + name + ".png").click()
        driver.close()
    if lang=='C++' and type=='Функциональный':
        pyalg.analyzecpp(code,name)
    if (lang == 'Python' and type == 'Объектный'):
        pyalg.analyze_code_obj(code)


    return True
def read_file(filename,field,name,type,lang):
    with open(filename) as file:
        code = file.read()
        read_code(code,field,name,type,lang)