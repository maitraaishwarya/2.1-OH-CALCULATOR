import cv2
import HandLandMarkModule as hlm
import HandStatusModule as hsm
import InputCheckerModule as icm
import BinaryListMakerModule as blm
import time


pt = 0
cam = cv2.VideoCapture(0)
detector = hlm.HandDetect()
HandStat = hsm.HandStatus()
Input = icm.inputbinary()
Blist = blm.BinaryListMaker()
bl = []

op = ''
label = ''
count, v1, v2, text, res, o1, o2 = 0, 0, 0, '', 0, '', ''
while True:
    count += 1
    value = 0
    op = ''
    ret, img = cam.read()
    img = cv2.flip(img, 1)                      #editable
    img = cv2.resize(img, (960, 540))        #editable
    if not ret:
        continue
    img = detector.findhands(img)
    lmlist = detector.findpos(img)
    if len(lmlist) != 0:
        x1 = lmlist[4][1]
        x2 = lmlist[17][1]
        label = HandStat.label(x1, x2)
        bl = Blist.BinaryList(lmlist, label)    # Fing value
        value, op = Input.statusprocessing(bl)    # operator

        if op != '':
            o1 = op
        if (count % 40 == 0) :
            if o1 == '':
                v1 = v1*10 + value
                text = str(v1)
            elif o1 == '=':
                res = Input.operation(v1, v2, o2)
                if v2 != 0:
                    text = str(v1) + str(o2) + str(v2) + str(o1) + str(res)
                else:
                    text = str(v1) + str(o2) + str(o1) + str(res)
            else:
                v2 = v2*10 + value
                o2 = o1
                text = str(v1) + str(o2) + str(v2)
            # print(v1, o1, v2, res)

    if len(lmlist) == 0:
        text, v1, v2, o1, o2, res = '', 0, 0, '', '', 0


    # print(label)
    ct = time.time()
    fps = 1 / (ct - pt)
    pt = ct
    cv2.putText(img, f'{"fps="+str(int(fps))}', (0, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    cv2.putText(img, str(int(value)), (50, 500), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    cv2.putText(img, str(text), (100, 120), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 5)

    cv2.imshow("image", img)
    if cv2.waitKey(1) == ord("q"):
        break
cam.release()
cv2.destroyAllWindows()
