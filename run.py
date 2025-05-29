 

import multiprocessing
import subprocess

# To run Jarvis
def startJarvis():
        # Code for process 1
        print("Process 1 is running.")
        from main_3 import start
        start()




    # Start both processes
if __name__ == '__main__':
        p1 = multiprocessing.Process(target=startJarvis)
        
        p1.start()
        
        