import time # Import library time
from pandas_ods_reader import read_ods # Untuk baca file ods
import numpy as np # Untuk membantu rekayasa array
import os # Import library operation system / os

# Class = cetak biru/ blue print
class fuzzy:
    # Cunstroctor 
    def __init__(self):
        super().__init__()

    # Membuat Bintang
    def bintang(self, angka):
        self.angka = angka 
        for i in range(angka):
            print("*", end=" ")
        print("") 

    # Pemberitahuan Error pada inputan
    def errorCodeMsg(self):
        raise ValueError("Error di inputan: CODE")   
    def errorPredMsg(self):
        raise ValueError("Error di inputan: PREDECESSORS")
    def errorFuzzyMsg(self):
        raise ValueError("Error di inputan: FUZZY")
        
    # Memindai data jika code di predecessors and succesors ada
    # di dalam list pada tugas code
    def getTaskCode(self, data, code):
        self.data = data 
        self.code = code 
        x = 0 
        flag = 0 # Bool nilai False
        for i in data["CODE"]:
            if(i==code):
                flag=1 # 1 bernilai True pada boolean
                break # Berhenti   
            x += 1 # Increament
        
        # Jika nilai tersebut ada, maka akan kembali ke variabel x
        if(flag==1):
            return x
        else:
            self.errorCodeMsg() # Kalau Error atau tidak ada
                                # nanti keluar ini
    
    # Function Forward Pass dengan metode Trapezoidal Fuzzy Critical Path
    # EF = Earliest Finish
    # ES = Earliest Start
    def forwardpass(self, data):
        self.data = data 
        ntask = data.shape[0] # Untuk mengetahui berapa array yang dibutuhkan

        ES = np.zeros(ntask, dtype=np.uint8) # (Object dari variabel ntask, type data tersebut int8)
        EF = np.zeros(ntask, dtype=np.uint8) # (Object dari variabel ntask, type data tersebut int8)
        ES1 = np.zeros(ntask, dtype=np.uint8) # (Object dari variabel ntask, type data tersebut int8)
        EF1 = np.zeros(ntask, dtype=np.uint8) # (Object dari variabel ntask, type data tersebut int8)
        ES2 = np.zeros(ntask, dtype=np.uint8) # (Object dari variabel ntask, type data tersebut int8)
        EF2 = np.zeros(ntask, dtype=np.uint8) # (Object dari variabel ntask, type data tersebut int8)
        temp = [] # Wadah
        temp1 = [] # Wadah
        temp2 = [] # Wadah


        # Rumus mencari ES dan EF dengan metode forward
        for i in range(ntask):
            if(data['PREDECESSORS'][i]==None):
                ES[i] = 0
                ES1[i] = 0
                ES2[i] = 0
                try:
                    EF[i] = ES[i] + data['A'][i]
                    EF1[i] = ES1[i] + data['B'][i]
                    EF2[i] = ES2[i] + data['C'][i]
                except:
                    self.errorFuzzyMsg()
            else:
                for j in data['PREDECESSORS'][i]:
                    index = self.getTaskCode(data,j)
                    temp.append(EF[index])
                    temp1.append(EF1[index])
                    temp2.append(EF2[index])

                    if(index==i):
                        self.errorPredMsg()
                    else:
                        temp.append(EF[index])
                        temp1.append(EF1[index])
                        temp2.append(EF2[index])
                
                ES[i] = max(temp) # Untuk menentukan element terbesar
                ES1[i] = max(temp1) # Untuk menentukan element terbesar
                ES2[i] = max(temp2) # Untuk menentukan element terbesar
                try:
                    EF[i] = ES[i] + data['A'][i]
                    EF1[i] = ES1[i] + data['B'][i]
                    EF2[i] = ES2[i] + data['C'][i]
                except:
                    self.errorFuzzyMsg()
            
            # Mereset variable temp
            temp = []
            temp1 = []
            temp2 = []

        # Merubah dataFrame
        data['ES'] = ES
        data['ES1'] = ES1
        data['ES2'] = ES2
        data['EF'] = EF       
        data['EF1'] = EF1   
        data['EF2'] = EF2      
       
        return data
    
    # Function Backward Pass dengan metode Trapezoidal Fuzzy Critical Path
    # LS = Latest Start
    # LF = Latest Finish
    def backwardpass(self, data):
        self.data = data 
        ntask = data.shape[0] # Untuk mengetahui berapa array yang dibutuhkan
        temp = [] # Wadah
        temp1 = [] # Wadah
        temp2 = [] # Wadah
        LS = np.zeros(ntask, dtype=np.int8) # (Object dari variabel ntask, type data tersebut int8)
        LF = np.zeros(ntask, dtype=np.int8) # (Object dari variabel ntask, type data tersebut int8)
        LS1 = np.zeros(ntask, dtype=np.int8) # (Object dari variabel ntask, type data tersebut int8)
        LF1 = np.zeros(ntask, dtype=np.int8) # (Object dari variabel ntask, type data tersebut int8)
        LS2 = np.zeros(ntask, dtype=np.int8) # (Object dari variabel ntask, type data tersebut int8)
        LF2 = np.zeros(ntask, dtype=np.int8) # (Object dari variabel ntask, type data tersebut int8)
        SUCCESSORS = np.empty(ntask, dtype=object) # (Object dari variabel ntask, type data dari object)

        # Membuat kolom successor
        for i in range(ntask-1,-1,-1):
            if(data['PREDECESSORS'][i] != None):
                for j in data['PREDECESSORS'][i]:
                    index=self.getTaskCode(data,j)
                    if(SUCCESSORS[index] !=None):
                        SUCCESSORS[index] += data['CODE'][i]
                    else:
                        SUCCESSORS[index] = data['CODE'][i]
        
        # Menggabungkan kolom ke data frame
        data['SUCCESSORS'] = SUCCESSORS

        # Menghitung LF dan LS
        for i in range(ntask-1,-1,-1):
            if(data['SUCCESSORS'][i] == None):
                LF[i] = np.max(data['EF'])
                LF1[i] = np.max(data['EF1'])
                LF2[i] = np.max(data['EF2'])
                
                LS[i] = LF[i] - data['A'][i]
                LS1[i] = LF1[i] - data['B'][i]
                LS2[i] = LF2[i] - data['C'][i]
            else:
                for j in data['SUCCESSORS'][i]:
                    index = self.getTaskCode(data,j)
                    temp.append(LS[index])
                    temp1.append(LS1[index])
                    temp2.append(LS2[index])
                    
                
                LF[i] = min(temp) # Mencari nilai terkecil dari LF
                LF1[i] = min(temp1) # Mencari nilai terkecil dari LF
                LF2[i] = min(temp2) # Mencari nilai terkecil dari LF
                
                LS[i] = LF[i] - data['A'][i]
                LS1[i] = LF1[i] - data['B'][i]
                LS2[i] = LF2[i] - data['C'][i]
                

                # Mereset list temp
                temp = []
                temp1 = []
                temp2 = []
                
        
        # Menggabungkan LF dan LS ke data frame
        data['LS'] = LS
        data['LS1'] = LS1
        data['LS2'] = LS2

        data['LF'] = LF
        data['LF1'] = LF1
        data['LF2'] = LF2


        return data
    
    # Function untuk menghitung nilai Slack dan keadaan kritis
    def slack(self, data):
        self.data = data    
        ntask = data.shape[0]
        SLACK=np.zeros(shape=ntask,dtype=np.int8)
        SLACK1=np.zeros(shape=ntask,dtype=np.int8)
        SLACK2=np.zeros(shape=ntask,dtype=np.int8)
        CRITICAL=np.empty(shape=ntask,dtype=object)

        for i in range(ntask):
            SLACK[i]=data['LS'][i] - data['ES'][i]
            SLACK1[i]=data['LS1'][i] - data['ES1'][i]
            SLACK2[i]=data['LS2'][i] - data['ES2'][i]      
            if(SLACK[i]==0 and SLACK1[i]==0 ):
                CRITICAL[i] = "YES"
            else:
                CRITICAL[i] = "NO"

        
        # Menggabungkan SLACK dan CRITICAL ke data frame
        data['SLACK'] = SLACK
        data['SLACK1'] = SLACK1
        data['SLACK2'] = SLACK2
        data['CRITICAL'] = CRITICAL

        # Menggabungkan kembali kolom di dataframe
        data=data.reindex(columns=['DESCR','CODE','PREDECESSORS',
                'SUCCESSORS','DAYS','ES','EF','LS','LF','SLACK','CRITICAL'])
        
        return data

    # Function pembungkus(?)
    def compute(self, mydata):
        self.mydata = mydata # Constructor Parameter

        mydata=self.forwardpass(mydata) # Untuk memanggil function forward pass
        mydata=self.backwardpass(mydata) # Untuk memanggil function backward pass
        mydata=self.slack(mydata) # Untuk memanggil function slack
        return mydata # Nilai kembali

    def printTask(self, mydata):
        self.mydata = mydata # Constructor Parameter
        print("TRINGULAR FUZZY CRITICAL PATH METHOD NUMERICAL CALCULATOR") # Judul
        self.bintang(90)
        print("ES=Earliest Start; EF=Earliest Finish; LS=Latest Start, LF=Latest Finish") # Keterangan
        self.bintang(90)
        print(mydata) # Data yang sudah diolah 
        self.bintang(90)
    
    # Function untuk mengetahui lajur kritisnya
    def cp(self, data, ntask):
        self.data = data
        self.ntask = ntask
       
        cp = []
        for i in range(ntask):
            if(data['SLACK'][i]==0):
                cp.append(data['CODE'][i])
        print("Lajur Critisnya adalah: "+ ' - '.join(cp))

    # Function untuk mengetahui durasi
    def durasi(self, data, ntask):
        start_time=time.time()
        self.data = data
        self.ntask = ntask
        lst = []
        x =0
        #jmlh = 0
        for i in range(ntask):
            if(data['SLACK'][i]==0):
                x = x+data['A'][i]

        x1 = 0
        for i in range(ntask):
            if(data['SLACK'][i]==0):
                x1 = x1+data['B'][i]
        
        x2 = 0
        for i in range(ntask):
            if(data['SLACK'][i]==0):
                x2 = x2+data['C'][i]      

        lst.append(x) # Memasukan nilai x ke list lst
        lst.append(x1) # Memasukan nilai x1 ke list lst
        lst.append(x2) # Memasukan nilai x2 ke list lst 

        print('Total durasi project dalam fuzzy: ',lst,' unit time')
    
    # Untuk mengeluarkan hasil
    def main(self):
        
        nama = input("Ketik tempat file excel yang akan dieksekusi(Ektension: .ods): ")
        sheet = input("Ketik nama sheet yang mau di eksekusi: ")
        
        # Membaca file excel
        data = read_ods(nama, sheet)
        self.bintang(90)
        print(data) # Mengeluarkan file excel ke compile
        self.bintang(90)
        os.system('pause') # Menghentikan sementara
        os.system('cls') # Membersihkan layar sebelumnya
        self.compute(data) # Memanggil function compute dengan parameter data
        self.printTask(data) # Memanggil function printTask dengan parameter data

        ntask = data.shape[0]
        self.cp(data,ntask) # Mengeluarkan function critical path 
        self.durasi(data, ntask) # Mengeluarkan function durasi
        
if __name__ == '__main__':
    x = fuzzy() # Object yang akan dipanggil dengan inisialisasi variabel x

    x.main() # Memanggil function main()
