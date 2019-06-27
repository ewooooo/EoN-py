class Train:        #열차 정보를 가지는 클레스
    def __init__(self,hourTime,minTime,startSubway,endSubway,trainType,siteCount):  #생성자로 열차의 정보를 받아 저장한다.
        self.hourTime = hourTime
        self.minTime = minTime
        self.startSubway = startSubway
        self.endSubway = endSubway
        self.trainType = trainType
        self.siteCount = siteCount
        
    def __str__(self):  #열차 정보의 출력을 위해 클래스의 이름을 출력시 열차 정보가 정형화 되어 출력되도록 한다.
        return self.hourTime+":"+self.minTime+" "+self.startSubway+"->"+self.endSubway+" "+self.trainType+" 잔여:"+self.siteCount



class MainProcess:      # 메인 프로세스 클래스로 프로그램의 동작을 나타낸다.
    def FileLoad(self):     #시작시 동작할 매소드로 TrainList.txt 에서 열차정보를 받아온다.
        try:
            inf = open('TrainList.txt','r')

            self.TrainList = []     #프로세스 클래스 안에서 모든 열차정보를 가지는 리스트이며 FileLoad 함수에서 최초선언하여 사용된다.
            self.myTrain = []       #프로세스 클래스 안에서 예약된 열차의 정보를 가지는 리스트이며 현 함수에서 최소선언하여 사용된다.
            allStringData = inf.readlines()     #메모장에 문자열 전체를 한줄씩 구분하여 리스트에 각각 저장한다.
            for s in allStringData :            #저장된 문자열을 한줄씩 s의 인가.
                if(s != "시간_출발_도착_열차종류_잔여좌석수\n"):   #첫 줄의 데이터를 비교하여 입력데이터가 맞는지 확인.
                    sdata = s.replace(':',' ').split()             #한줄의 문자열을 : 와 띄어쓰기로 잘라 sdata 리스트의 저장.
                    self.TrainList.append(Train(sdata[0],sdata[1],sdata[2],sdata[4],sdata[5],sdata[6]))
                    #Train 클래스를 생성하며 생성자를 이용하여 데이터를 저장한다. 생성된 객체를 TrainList의 추가 한다.
        except IOError:
            print("file load error")        #예외처리1 : 파일 접근
            return False
        except IndexError:
            print("file load error")        #예외처리2 : 리스트 인덱스 에러
            return False                        #파일 입출력 실패로 에러 발생시 false 리턴하여 프로그램이 실행하지 않도록한다.
        else:
            print("file load OK")           #정상 입력을 확인하고 true 반환하여 프로그램 실행
            return True
        
    def ShowTrain(self):                    #모든 열차 정보 출력 함수
        for train in self.TrainList :
            print(train)
    
    def FastSearch(self):                   #열차 빠른 예매 함수
        print("검색할 기차의 정보를 입력하세요")
        print("(입력한 시간의 가장 가까운 시간대의 열차정보가 출력됩니다)")
        print("[원하는시간(##:##) 출발역 도착역 열차종류 순으로 띄어 입력](뒤로가기 -1)")
        while(1):
            try:
                
                testIn = input("입력: ")
                if testIn is '-1':      #뒤로가기 기능
                    return
                testIn = testIn.replace(':',' ').split()    #입력된 문자열을 열차정보데이터의 형식으로 변환
                testHourTime = 24       #시간 비교를 위한 초기화 최대값 24시간
                testMinTime = 60        #시간 비교를 위한 초기회 최대값 60분
                testTrain = None        #검색 결과가 없을 시 사용할 변수
                for train in self.TrainList:    #열차정보 하나씩 확인
                    if train.startSubway == testIn[2] and train.endSubway == testIn[3] and train.trainType == testIn[4].upper():
                        #시간비교전 해당 열차가 맞는 출발지 도착지 열차종류 확인(대소문자 둘다가능)
                        if testHourTime > abs(int(train.hourTime) - int(testIn[0])):        #시간을 먼저확인
                            testHourTime = abs(int(train.hourTime) - int(testIn[0]))
                            testTrain = train
                        elif testHourTime == abs(int(train.hourTime) - int(testIn[0])):     #시간이 같으면 분도 확인
                            if testMinTime > abs(int(train.minTime) - int(testIn[1])):
                                testHourTime = abs(int(train.hourTime) - int(testIn[0]))
                                testMinTime = abs(int(train.minTime) - int(testIn[1]))
                                testTrain = train
                if(testTrain == None):      #검색결과가 없을 경우
                    print("\n검색결과가 없습니다")
                    return
                print("\n검색 결과:")
                print(testTrain)
            except ValueError:
                print("입력이 잘못되었습니다")    #자료형 변화에 의한 입력 오류 방지
            except IndexError:
                print("입력이 잘못되었습니다.")   #리스트 인덱스 접근 오류 방지
            else:
                break

        sel = "팽이는 바보"      #검색결과가 있는경우 잘못된 입력 시 반복을 위한 변수( break 있어서 사실 없어도됨 ^^)
        while(sel != 'y'):
            try:
                sel = input("예매하시겠습니까?(y/n):")
            except ValueError:
                print("입력이 잘못되었습니다")
            if sel == 'y':
                testTrain.siteCount = str(int(testTrain.siteCount)-1)   #열차정보의 잔여석을 하나 차감함
                if int(testTrain.siteCount) == 0:       #잔여석이 0 이되면 매진으로 표현
                    testTrain.siteCount = "매진"
                self.myTrain.append(testTrain)          #예약된 열차정보 저장.
                
                print("예매가 완료되었습니다",testTrain)
                break
            elif sel == 'n':
                print("예매가 취소되었습니다.")           #뒤로가기 기능.
                break
            else :
                print("잘못된 입력입니다.")
            
    def MyTrainList(self):          #예매된 열차정보를 출력하며 예매를 취소한다.
        print("예매 현황")
        print("예매 건(",len(self.myTrain),"건)")
        if len(self.myTrain) != 0:      #예약건이 없으면 실행하지 않는다.
            i = 1       #출력 번호와 인덱스 접근을 위한 변수
            for train in self.myTrain:      #열차정보를 하나씩 출력하며 앞에 번호를 1부터 붙여준다.
                print(i,train)
                i = i + 1
            while(1):
                try:
                    sel = int(input("예매 취소 하실 번호를 선택해주세요(뒤로가기 -1):"))
                    if sel != -1:       #뒤로가기 기능
                        self.myTrain[sel-1].siteCount = str(int(self.myTrain[sel-1].siteCount) + 1)     #예매가 취소되면 잔역석을 복구
                        print(self.myTrain[sel-1],"예매가 취소되었습니다")
                        self.myTrain.pop(sel-1)     #출력번호로 인덱스를 접근하여 데이터를 날림.
                except ValueError:
                    print("입력이 잘못되었습니다")    #예외처리1: 문자 입력 방지
                except IndexError:
                    print("입력이 잘못되었습니다.")   #예외처리1: 잘못된 입력으로 인덱스 접근 방지
                else:
                    break
                
            
                
            
    def Menu(self):
        print("1. 빠른시간 기차 검색 및 예매")
        print("2. 전체 기차 리스트 출력")
        print("3. 나의 예매 현환 출력 및 예매 취소")
        print("4. 프로그램 종료")
    def Start(self):
        while(1):       #UI 메뉴 구성.
            self.Menu()
            try:
                sel = int(input("입력: "))
            except ValueError:
                print("입력이 잘못되었습니다")    #예외처리 1:  문자 입력방지
                continue

            print("")
            if sel == 1:
                self.FastSearch();
            elif sel == 2:
                self.ShowTrain()
            elif sel == 3:
                self.MyTrainList();
            elif sel == 4:
                return
            else :
                print("입력이 잘못되었습니다.")
                continue
            print("")
                
        
        
#파이썬의 메인함수
if __name__ == "__main__":
    print("빠른시간 기차 예매 프로그램")
    print("ver 1.0.0")
    print("maker_ ewooooo\n")
    t1 = MainProcess()  #메인프로세스클래스 생성(프로그램의 동작을 모두 가지고 있다)
    if t1.FileLoad():   #파일 입출력 함수를 실행하여 .txt에서 입력을 받아오고
        print("")       #파일 입출력 함수의 파일 입출력 실패시 false를 반환하여 프로그램을 시작하지 않고 종료한다.
        t1.Start()      #프로그램의 시작점을 가리킨다.
    
