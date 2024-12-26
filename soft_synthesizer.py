@ -0,0 +1,110 @@
import numpy as np
import matplotlib.pyplot as plt
import wave
OUTPUT_file="test_01.wav"
class Wave_make():
    def __init__(self):
        self.x=[]
        self.wave_data=[]
        self.sampling=44100#wavファイルのサンプリングレートが44.1Hz
        self.Attack_present=0
        self.Decay_present=0
        self.Sustain_present=0
        self.Relrase_present=0
    
    #ADSR_parestは事前に入力しておく
    #サイン波出力
    def wave_make_sin(self,start,stop,frequency):
        section_x = np.arange(start,stop,(1/self.sampling))
        t,c=self.ADSR_parest(section_x)
        y=self.make_sin(t,frequency,c)
        self.addr_wave(section_x,y)
    
    #矩形波出力
    def wave_make_square(self,start,stop,frequency):
        section_x = np.arange(start,stop,(1/self.sampling))
        t,c=self.ADSR_parest(section_x)
        y=self.make_square(t,frequency,c)
        self.addr_wave(section_x,y)
    
    #三角波出力
    def wave_make_triangle(self,start,stop,frequency):
        section_x = np.arange(start,stop,(1/self.sampling))
        t,c=self.ADSR_parest(section_x)
        y=self.make_triangle(t,frequency,c)
        self.addr_wave(section_x,y)

    
    #sin波
    def make_sin(self,section_x,Frequency,vo):
        y=vo*np.sin(np.sin(2 * np.pi * Frequency * section_x))
        return y

    #矩形波
    def make_square(self,section_x,Frequency,vo):
        y = vo*np.sign(np.sin(2 * np.pi * Frequency * section_x))
        return y
    
    #三角波出力
    def make_triangle(self,section_x,frequency,vo):
        y = vo*2*(np.abs(np.mod(section_x * frequency, 1.0) - 0.5) * 2.0)-0.5
        return y
        
    #ADSRの値を百分率にする事でフレキシブルに発音時間に対応させる
    def ADSR_set(self,attack,attack_level,decay,sutain,sutain_level,relrase):
        self.Attack_present=attack/100
        self.Attack_level=attack_level
        self.Decay_present=decay/100
        self.Sustain_present=sutain/100
        self.Sustain_level=sutain_level
        self.Relrase_present=relrase/100
    
    #ADSR各値を発音時間に当てはめる
    def ADSR_parest(self,section_x):
        attack=len(section_x)*(self.Attack_present)
        decay=len(section_x)*(self.Decay_present)
        sustain=len(section_x)*(self.Sustain_present)
        release=len(section_x)*(self.Relrase_present)
        return self.ADSR(attack,self.Attack_level,decay,sustain,self.Sustain_level,release)
    
    #ADSRを生成
    def ADSR(self,attack,attack_level,decay,sustain,sustain_level,release):
        Attack=np.linspace(0,attack_level,int(attack))
        Decay=np.linspace(attack_level,sustain_level,int(decay))
        Sustain=np.full(int(sustain),sustain_level)
        Relrase=np.linspace(sustain_level,0,int(release))
        # 全体のエンベロープを連結
        adsr_envelope = np.concatenate((Attack, Decay, Sustain, Relrase))
        t = np.linspace(0, attack + decay + sustain + release, len(adsr_envelope))
        return t,adsr_envelope
    
    
    #波形を連結
    def addr_wave(self,section_x,y):
        self.x=np.hstack((self.x, section_x))
        self.wave_data=np.hstack((self.wave_data,y))
    
    #おまけ機能として波形確認
    def wave_show(self):
        print(len(self.x))
        plt.plot(self.x,self.wave_data)
        plt.show()
    
    #波形をwav形式にする
    def Audio_make(self):
        self.wave_data = self.wave_data * np.iinfo(np.int16).max
        self.wave_data = self.wave_data.astype(np.int16)

        with wave.open(OUTPUT_file, "w") as wf:
            wf.setnchannels(1) 
            wf.setsampwidth(2)
            wf.setframerate(self.sampling)
            wf.writeframes(self.wave_data)
        
a=Wave_make()
a.ADSR_set(30,1,10,20,1,40)#例：ADSRのアタックを発音時間の３０％、アタックの目標が１、ディケイが発音時間の１０％、スタインが発音時間の２０％、スタイン時のレベルが1、リリースが発音時間の４０％
a.wave_make_sin(0,1,440)#０から１秒目まで440Hzを生成する
a.wave_make_sin(2,3,880)
a.wave_make_sin(4,5,440)
a.wave_make_sin(4,5,880)
a.Audio_make()
