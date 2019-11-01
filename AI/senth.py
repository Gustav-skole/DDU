from pyo import *
import time, math

s = Server().boot()
s.start()

lfd = Sine([1.4,.3], mul=.2, add=.5)
#saw = SuperSaw(freq=[49,50], detune=lfd, bal=0.7, mul=0.2).out()
sin = Sine(freq=500, mul=0.2).out()

i = 0
baseFreq = 500
tMod = 0

while(i < 200):

	sin.setFreq(i+baseFreq+math.sin(tMod)*10)

	i += 0.1

	tMod += 0.1*pi
	if tMod > 2*pi:
		tMod = 0

	time.sleep(0.01)

s.stop()