import cv2
import queue
import time
from threading import Thread
q = queue.Queue()


def Receive():
    print("start Reveive")
    cap = cv2.VideoCapture('rtsp://admin:123456789bit@10.110.0.37:554/11')
    ret, frame = cap.read()
    q.put(frame)
    while ret:
        ret, frame = cap.read()
        for i in range(2):
            q.put(frame)


def Display():
    time.sleep(3)
    while True:
        if q.empty() != True:
            frame = q.get()
            cv2.imshow("frame1", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


if __name__ == '__main__':

    t1 = Thread(target=Receive)
    t2 = Thread(target=Display)
    t1.setDaemon(True)
    t2.setDaemon(True)
    t1.start()
    t2.start()
    while True:
        pass
