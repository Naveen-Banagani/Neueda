# coding: utf-8
import socket
import os
import sys
import json
import dicttoxml
import threading

def send_converted_json_files_to_socket(socket, dir_name):
    file_names = os.listdir(dir_name)
    for file in file_names:
        if file.endswith('.json'):
            print(file)
            f = open(os.path.join(dir_name, file), 'r')
            data = json.load(f)
            xml = converttoxml(data)
            socket.send(format_sending_data(xml, file[0:-5]))
            print("sent", file)


def converttoxml(json):
    xml = dicttoxml.dicttoxml(json, root=False)
    return xml.decode('utf-8')

def format_sending_data(xml,filename):
    return bytes(filename +"|"+ str(len(xml)) +"|"+ xml + '\0', 'utf-8')

if __name__ == "__main__":
    print('started')
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.connect(("localhost",5000))
    send_converted_json_files_to_socket(socket,"./input")
    socket.close() 
