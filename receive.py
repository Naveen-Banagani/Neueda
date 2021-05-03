
import socket
import sys
import threading
import os
import json


def read_data(client_socket, stop_characters):
    string = ""
    print("started")
    l = [bytes(el, encoding='utf-8') for el in stop_characters]
    while True:
        try:
            ch = client_socket.recv(1)

            if ch in l or ch == b'':
                break
            string = string + ch.decode("utf-8") 

        except socket.error:
            print("Error Occured.")
            return None

    print(string)
    return string

def handle_client(client_socket,client_addr):
    print('Connected by', client_addr)

    while True:
        filename = read_data(client_socket, ["|"])

        if filename == "":
            break

        length = read_data(client_socket, ["|"])
        data = read_data(client_socket, ["\0"])

        print('writing to xml')
        write_to_xml('./received', filename, data)

    print("done")

def write_to_xml(target_dir, filename, xml):
    file_path = os.path.join(target_dir, filename+".xml")
    f = open(file_path, 'w')
    f.write(xml)
    f.close()


if __name__ == "__main__":
    # loadconfig()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", 5000))
    s.listen(1)
    print("receiver started")
    while True:
        conn, addr = s.accept()
        client_handler = threading.Thread(target=handle_client,args=(conn,addr))
        client_handler.start()
    conn.close()
    print('receive side')
