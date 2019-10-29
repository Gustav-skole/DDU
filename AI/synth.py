from synthesizer import Player, Synthesizer, Waveform

p = Player()
p.open_stream()

s = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)

i = 0
while(i<3):
	A = s.generate_constant_wave(88.0,1.0)
	p.play_wave(A)
	i += 1

