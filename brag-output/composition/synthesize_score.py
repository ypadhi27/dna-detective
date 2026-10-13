"""Original deterministic 24-second ambient score; no sampled music."""
import numpy as np, wave
from pathlib import Path
sr=44100; duration=24; mix=np.zeros((sr*duration,2)); beat=60/110
chords=[[50,57,62,65],[46,53,58,62],[48,55,60,64],[45,52,57,60]]
def note(start,midi,length,level,pan=0):
 n=min(int(length*sr),len(mix)-int(start*sr)); t=np.arange(n)/sr
 f=440*2**((midi-69)/12)
 env=(1-np.exp(-t*28))*np.exp(-t*2.0)*np.minimum(1,(length-t)*5)
 sig=(np.sin(2*np.pi*f*t)+.22*np.sin(2*np.pi*2*f*t)+.09*np.sin(2*np.pi*3*f*t))*env*level
 i=int(start*sr);mix[i:i+n,0]+=sig*(1-pan*.3);mix[i:i+n,1]+=sig*(1+pan*.3)
for k in range(88):
 start=k*beat/2
 if start>=23:break
 c=chords[(k//16)%4]; note(start,c[[0,2,1,3,2,1,3,1][k%8]]+12,2,.08,(-1)**k*.6)
for k in range(11):
 start=k*beat*4
 if start<23: note(start,chords[k%4][0]-12,3,.11)
fade=np.minimum(1,np.arange(len(mix))/sr/.5)*np.minimum(1,(duration-np.arange(len(mix))/sr)/2)
mix*=fade[:,None];mix/=max(1,np.max(np.abs(mix))/.7)
with wave.open(str(Path(__file__).parent/'assets/score.wav'),'w') as f:
 f.setnchannels(2);f.setsampwidth(2);f.setframerate(sr);f.writeframes((mix*32767).astype('<i2').tobytes())
