import service
import userWindow
import multiprocessing

if __name__ == "__main__":
    Queue=multiprocessing.Queue()
    Queue2 = multiprocessing.Queue()
    ServiceObject=service.Service()
    UserWindowObject=userWindow.UserWindow(Queue,Queue2)
    Service=multiprocessing.Process(target=ServiceObject.run,args=(Queue,Queue2))
    Service.start()
    UserWindowObject.run()
