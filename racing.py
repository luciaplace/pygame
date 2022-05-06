from pygame import mixer
mixer.init()
sound = mixer.Sound("pygame_Car/music/crash.wav")
sound.play()