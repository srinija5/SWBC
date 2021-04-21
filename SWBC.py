import tkinter
from tkinter import *
import math
import random
from threading import Thread 
from collections import defaultdict
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
import time
from tkinter import messagebox
import webbrowser

from Blockchain import *
from Block import *

global iot
global labels
global iot_x
global iot_y
global text
global canvas
global iot_list
global gw1,gw2,gw3
global line1,line2,line3
global window_list
global propose
global extension
global running_time

def calculateDistance(iot_x,iot_y,x1,y1):
    flag = False
    for i in range(len(iot_x)):
        dist = math.sqrt((iot_x[i] - x1)**2 + (iot_y[i] - y1)**2)
        if dist < 80:
            flag = True
            break
    return flag

def generate():
    global iot
    global labels
    global iot_x
    global iot_y
    iot = []
    iot_x = []
    iot_y = []
    labels = []
    canvas.update()
    x = 5
    y = 350
    iot_x.append(x)
    iot_y.append(y)
    name = canvas.create_oval(x,y,x+40,y+40, fill="blue")
    lbl = canvas.create_text(x+20,y-10,fill="darkblue",font="Times 7 italic bold",text="IOT Cloud")
    labels.append(lbl)
    iot.append(name)

    for i in range(1,20):
        run = True
        while run == True:
            x = random.randint(100, 450)
            y = random.randint(50, 600)
            flag = calculateDistance(iot_x,iot_y,x,y)
            if flag == False:
                iot_x.append(x)
                iot_y.append(y)
                run = False
                name = canvas.create_oval(x,y,x+40,y+40, fill="red")
                lbl = canvas.create_text(x+20,y-10,fill="darkblue",font="Times 8 italic bold",text="IOT "+str(i))
                labels.append(lbl)
                iot.append(name)
    

def SWBCThread(propose,running_time):
    
    class RunThread(Thread):
        global iot
        global labels
        global iot_x
        global iot_y
        global text
        global canvas
        global iot_list
        global window_list
        
        def __init__(self,propose,running_time):
            Thread.__init__(self)
            self.propose = propose
            self.running_time = running_time            
        def run(self):
            self.propose = 0
            self.running_time = 0
            blockchain = Blockchain()
            window_limit = int(window_list.get())
            num_transfer = int(iot_list.get())
            index = 0
            for i in range(0,num_transfer):
                iotID = random.randint(1,19)
                x = iot_x[iotID]
                y = iot_y[iotID]
                canvas.delete(labels[iotID])
                lbl = canvas.create_text(x+20,y-10,fill="red",font="Times 10 italic bold",text="IOT "+str(iotID))
                labels[iotID] = lbl                
                count = 'IoT'+str(iotID)+","+str(random.randint(25,45))
                text.insert(END,"Generated Data : "+count+"\n")
                enc = blockchain.encrypt(count)
                enc = str(base64.b64encode(enc),'utf-8')
                text.insert(END,"AES encrypted data : "+enc+". Mining pending will done after 10 blocks\n")
                blockchain.addPeer(enc)
                self.propose = self.propose + 1
                if len(blockchain.peer) >= 10:
                    for k in range(len(blockchain.peer)):
                        if len(blockchain.chain) == window_limit:
                            blck = blockchain.chain.pop(0)
                            name = time.strftime("%d-%m-%Y-%H-%M-%S") + ".txt"
                            with open('remove/remove_'+str(index)+'_'+name, 'wb') as output:
                                pickle.dump(blck, output, pickle.HIGHEST_PROTOCOL)
                            index = index + 1    
                        text.insert(END,"Window size exceed & saved old block to remove folder and maintain recent blocks\n")
                        starttime = time.time()
                        blockchain.add_new_transaction(blockchain.peer[k])
                        blockchain.mine()
                        finishtime = time.time()
                        self.running_time = self.running_time + (finishtime - starttime)
                    blockchain.peer.clear()
                text.insert(END,'Mining done and saved recent blocks to BC_DB.txt file\n')
                time.sleep(1)
                canvas.delete(labels[iotID])
                lbl = canvas.create_text(x+20,y-10,fill="darkblue",font="Times 10 italic bold",text="IOT "+str(iotID))
                labels[iotID] = lbl
            output = '<html><body><center><br/><br/><table align=center border=1><tr><th>Encrypted Packet</th><th>Decrypted Packet</th>'
            output+='<th>Previous Hash</th><th>Packet Index</th><th>Current Hash</th><th>Timestamp</th></tr>'
            for i in range(len(blockchain.chain)):
                if i > 0:
                    b = blockchain.chain[i]
                    data = b.transactions[0]
                    data = base64.b64decode(data)
                    decrypt = blockchain.decrypt(data)
                    text.insert(END,str(data)+" "+str(decrypt.decode("utf-8"))+" "+str(b.previous_hash)+" "+str(b.index)+" "+str(b.hash)+" "+str(datetime.fromtimestamp(b.timestamp)))
                    print(str(data)+" "+str(decrypt.decode("utf-8"))+" "+str(b.previous_hash)+" "+str(b.index)+" "+str(b.hash)+" "+str(datetime.fromtimestamp(b.timestamp)))
                    output+='<tr><td>'+str(data)+'</td><td>'+str(decrypt.decode("utf-8"))+'</td><td>'+str(b.previous_hash)+'</td>'
                    output+='<td>'+str(b.index)+'</td><td>'+str(b.hash)+'</td><td>'+str(datetime.fromtimestamp(b.timestamp))+'</td></tr>'
            canvas.delete(labels[0])
            x = iot_x[0]
            y = iot_y[0]
            lbl = canvas.create_text(x+20,y-10,fill="red",font="Times 7 italic bold",text="IOT Cloud")
            labels[0] = lbl
            time.sleep(2)
            lbl = canvas.create_text(x+20,y-10,fill="darkblue",font="Times 7 italic bold",text="IOT Cloud")
            labels[0] = lbl
            messagebox.showinfo("Propose Sliding Window Blockchain Simulation Completed","Total transfer packets are "+str(self.propose)+"\nTotal execution time : "+str(round(self.running_time,5))+" M.S for window size "+str(window_limit))
            f = open("table.html", "w")
            f.write(output)
            f.close()
            f = open("propose.txt", "w")
            f.write(str(self.propose))
            f.close()
            webbrowser.open("table.html",new=2)

    newthread = RunThread(propose,running_time) 
    newthread.start()
    


def runSWBC():
    global propose
    global running_time
    propose = 0
    running_time = 0
    text.delete('1.0', END)
    SWBCThread(propose,running_time)

    


def SWBCExtensionThread(extension):
    
    class ExtensionThread(Thread):
        global iot
        global labels
        global iot_x
        global iot_y
        global text
        global canvas
        global iot_list
        global window_list
        
        def __init__(self,extension):
            Thread.__init__(self)
            self.extension = extension
                        
        def run(self):
            extension_time = 0
            self.extension = 0
            datalist = []
            blockchain = Blockchain()
            window_limit = int(window_list.get())
            num_transfer = int(iot_list.get())
            index = 0
            for i in range(0,num_transfer):
                iotID = random.randint(1,19)
                value = random.randint(25,45) #generating IOT data randomly
                if value not in datalist:
                    datalist.append(value)
                    x = iot_x[iotID]
                    y = iot_y[iotID]
                    canvas.delete(labels[iotID])
                    lbl = canvas.create_text(x+20,y-10,fill="red",font="Times 10 italic bold",text="IOT "+str(iotID))
                    labels[iotID] = lbl                
                    count = 'IoT'+str(iotID)+","+str(value)
                    text.insert(END,"Generated Data : "+count+"\n")
                    enc = blockchain.encrypt(count) #encryting data
                    enc = str(base64.b64encode(enc),'utf-8')
                    text.insert(END,"AES encrypted data : "+enc+". Mining pending will done after 10 blocks\n")
                    blockchain.addPeer(enc) #adding data to block chain
                    self.extension = self.extension + 1
                    if len(blockchain.peer) >= 10:
                        for k in range(len(blockchain.peer)):
                            if len(blockchain.chain) == window_limit: #checking sliding window size and if exceed
                                blck = blockchain.chain.pop(0) #then pop or remove first old block
                                name = time.strftime("%d-%m-%Y-%H-%M-%S") + ".txt"
                                with open('remove/remove_'+str(index)+'_'+name, 'wb') as output:
                                    pickle.dump(blck, output, pickle.HIGHEST_PROTOCOL)
                                index = index + 1    
                            text.insert(END,"Window size exceed & saved old block to remove folder and maintain recent blocks\n")
                            starttime = time.time()
                            blockchain.add_new_transaction(blockchain.peer[k])
                            blockchain.mine()
                            finishtime = time.time()
                            extension_time = extension_time + (finishtime - starttime)
                            #print(extension_time)
                        blockchain.peer.clear()
                    text.insert(END,'Mining done and saved recent blocks to BC_DB.txt file\n')
                    time.sleep(1)
                    canvas.delete(labels[iotID])
                    lbl = canvas.create_text(x+20,y-10,fill="darkblue",font="Times 10 italic bold",text="IOT "+str(iotID))
                    labels[iotID] = lbl     
            for i in range(len(blockchain.chain)):
                if i > 0:
                    b = blockchain.chain[i]
                    data = b.transactions[0]
                    data = base64.b64decode(data)
                    decrypt = blockchain.decrypt(data)
                    text.insert(END,str(data)+" "+str(decrypt.decode("utf-8"))+" "+str(b.previous_hash)+" "+str(b.index)+" "+str(b.hash)+" "+str(datetime.fromtimestamp(b.timestamp)))
                    print(str(data)+" "+str(decrypt.decode("utf-8"))+" "+str(b.previous_hash)+" "+str(b.index)+" "+str(b.hash)+" "+str(datetime.fromtimestamp(b.timestamp)))
            canvas.delete(labels[0])
            x = iot_x[0]
            y = iot_y[0]
            lbl = canvas.create_text(x+20,y-10,fill="red",font="Times 7 italic bold",text="IOT Cloud")
            labels[0] = lbl
            time.sleep(2)
            lbl = canvas.create_text(x+20,y-10,fill="darkblue",font="Times 7 italic bold",text="IOT Cloud")
            labels[0] = lbl
            messagebox.showinfo("Extension without duplicate packets Sliding Window Blockchain Simulation Completed","Total transfer packets are "+str(self.extension)+"\nTotal extension execution time : "+str(round(extension_time,5))+" M.S for window size "+str(window_limit))
            f = open("extension.txt", "w")
            f.write(str(self.extension))
            f.close()
    newthread = ExtensionThread(extension) 
    newthread.start()


def extension():
    global extension
    extension = 0
    text.delete('1.0', END)
    SWBCExtensionThread(extension)  

def graph():
    propose = 0
    extension = 0
    with open("propose.txt", "r") as file:
        for line in file:
            propose = line
    file.close()
    with open("extension.txt", "r") as file:
        for line in file:
            extension = line
    file.close()
    print(propose)
    print(extension)
    
    height = [int(propose),int(extension)]
    bars = ('Propose Packets Transfer','Extension Packets Transfer')
    y_pos = np.arange(len(bars))
    plt.bar(y_pos, height)
    plt.xticks(y_pos, bars)
    plt.show()

def Main():
    global window_list
    global text
    global canvas
    global iot_list
    root = tkinter.Tk()
    root.geometry("1300x1200")
    root.title("Sliding Window Blockchain Architecture for Internet of Things")
    root.resizable(True,True)
    font1 = ('times', 12, 'bold')

    canvas = Canvas(root, width = 800, height = 700)
    canvas.pack()

    l1 = Label(root, text='Packet Transfer:')
    l1.config(font=font1)
    l1.place(x=820,y=10)

    mid = []
    for i in range(15,30):
        mid.append(str(i))
    iot_list = ttk.Combobox(root,values=mid,postcommand=lambda: iot_list.configure(values=mid))
    iot_list.place(x=970,y=10)
    iot_list.current(0)
    iot_list.config(font=font1)

    l2 = Label(root, text='Window Size:')
    l2.config(font=font1)
    l2.place(x=820,y=60)

    window = []
    window.append(5)
    window.append(10)
    window.append(15)
    window_list = ttk.Combobox(root,values=window,postcommand=lambda: window_list.configure(values=window))
    window_list.config(font=font1)
    window_list.place(x=970,y=60)
    window_list.current(0)

    createButton = Button(root, text="Create Smart Home IOT Network", command=generate)
    createButton.place(x=820,y=110)
    createButton.config(font=font1)

    swbcButton = Button(root, text="Run SWBC Simulation", command=runSWBC)
    swbcButton.place(x=820,y=160)
    swbcButton.config(font=font1)

    extensionButton = Button(root, text="Run SWBC Simulation Extension Algorithm", command=extension)
    extensionButton.place(x=820,y=210)
    extensionButton.config(font=font1)

    graphButton = Button(root, text="Comparison Graph", command=graph)
    graphButton.place(x=820,y=260)
    graphButton.config(font=font1)


    text=Text(root,height=20,width=60)
    scroll=Scrollbar(text)
    text.configure(yscrollcommand=scroll.set)
    text.place(x=820,y=310)
    
    
    root.mainloop()
   
 
if __name__== '__main__' :
    Main ()
    
