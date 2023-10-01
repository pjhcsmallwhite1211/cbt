import time

from transformers import pipeline
class Cmd(object):
    def __init__(self,cmd,run=lambda service,cmdStr,queue_send:None ):
        self.cmd=cmd
        self.run=run

def speak(service,cmdStr,queue_send):
    print("speak start")
    prompt=cmdStr.split("/")[1].split(',')[0]
    print(f"prompt:{prompt}")
    result=service._generateText(prompt)
    print(service.cmd,'return',result[0]['generated_text'])
    queue_send.put(result[0]['generated_text'])
    print("put ~")
def exit(service,cmdStr,queue_send):
    service.running=False
    print(service.cmd,'exit')

def start(service,cmdStr,queue_send):
    service.init()
    print(service.cmd,'start')
class Service(object):
    def __init__(self):
        self.running=True
        self.cmds={}
        self.cmds["start"]=Cmd("start",start)
        
        self.cmds["exit"]=Cmd("exit",exit)

        self.cmds["speak"]=Cmd("speak",speak)
    def init(self):
        self.model = 'gpt2'
        self._generateText = pipeline("text-generation", model=self.model)
    def run(self,queue,queue_send):
        while self.running:
            self.cmdStr=queue.get()
            self.cmd=self.cmdStr.split("/")[0]
            print("ok",time.time())
            if self.cmd not in self.cmds.keys():
                print("unknown cmd")
                continue
            self.cmds[self.cmd].run(self,self.cmdStr,queue_send)
            print(f"{self.cmd} end")
    def stop(self):
        pass

