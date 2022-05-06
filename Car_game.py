
import pygame
import random
from time import sleep
from pygame import mixer


#스크린 크기 설정
Screenwidth=480
ScreenHeight=800


# 색 설정
BLACK=(0,0,0)
WHITE=(255,255,255)
GRAY = (150,150,150)
RED=(255,0,0)




#차 이미지 
class Car:
    image_Car=[ 
        'pygame_Car/images/RacingCar01.png','pygame_Car/images/RacingCar02.png','pygame_Car/images/RacingCar03.png',\
            'pygame_Car/images/RacingCar04.png','pygame_Car/images/RacingCar05.png','pygame_Car/images/RacingCar06.png','pygame_Car/images/RacingCar07.png',\
                'pygame_Car/images/RacingCar08.png','pygame_Car/images/RacingCar09.png','pygame_Car/images/RacingCar10.png','pygame_Car/images/RacingCar11.png',\
                    'pygame_Car/images/RacingCar12.png','pygame_Car/images/RacingCar13.png','pygame_Car/images/RacingCar14.png','pygame_Car/images/RacingCar15.png',\
                       'pygame_Car/images/RacingCar16.png','pygame_Car/images/RacingCar17.png','pygame_Car/images/RacingCar18.png','pygame_Car/images/RacingCar19.png',\
                           'pygame_Car/images/RacingCar20.png', 
    ]
    
    #init 함수 설정(초기화)
    def __init__(self, x=0,y=0,dx=0,dy=0):
        self.image =""
        self.x=x
        self.y=y
        self.dx=dx
        self.dy=dy
    
    #이미지 불러오기
    def load_image(self):
        self.image = pygame.image.load(random.choice(self.image_Car)) #차 이미지 20개중에서 랜덤으로 불러오기
        self.width = self.image.get_rect().size[0]
        self.height =self.image.get_rect().size[1]
    
    #이미지 게임판에 그리기
    def draw_image(self):
        screen.blit(self.image,[self.x, self.y]) #그릴 이미지와 좌표 입력
    
    #자동차 움직이기
    def move_x(self):
        self.x += self.dx #움직인만큼 x좌표에 더해주기
    
    def move_y(self):
        self.y += self.dy
    
    #가장자리 처리
    def check_out_of_Screen(self):
        if self.x+self.width>Screenwidth or self.x<0: #차의 x좌표가 스크린 너비보다 커지거나 0보다 작아지면,
            self.x -= self.dx #차의 x좌표 - 움직인 만큼의 x좌표
        
    #충돌 확인
    def check_crash(self, car):
        if(self.x+self.width>car.x) and (self.x<car.x+car.width) and (self.y< car.y + car.height) and(self.y+self.height>car.y):
            return True #충돌했다.
        else:
            return False
        
def draw_main_menu():
    draw_x = (Screenwidth/2)-200
    draw_y = ScreenHeight/2
    image_intro = pygame.image.load('pygame_Car/images/flag.png')
    screen.blit(image_intro,[draw_x, draw_y -250])
    font_40 = pygame.font.SysFont("Arial",40,True,False)
    font_30 = pygame.font.SysFont("Arial",30,True,False)
    text_title = font_40.render("Racing Game",True, BLACK)
    screen.blit(text_title, [draw_x +80, draw_y+10])
    text_score = font_40.render("Score :" + str(score),True,GRAY)
    screen.blit(text_score,[draw_x +105,draw_y+80])
    text_start = font_30.render("Press space key to Start", True, RED)
    screen.blit(text_start, [ draw_x +25 , draw_y+150])
    pygame.display.flip()
    
    
def draw_score():
    font_30 = pygame.font.SysFont("FixedSys",30,True,False)
    text_score = font_30.render("Score :" + str(score),True,BLACK)
    screen.blit(text_score,[15,15])
       

if __name__ == '__main__':
    pygame.init()
    
    screen=pygame.display.set_mode((Screenwidth,ScreenHeight))
    pygame.display.set_caption("jieun's racing game")
    clock = pygame.time.Clock()
    
    #음향넣기
    pygame.mixer.music.load('pygame_Car/music/race.wav')
    Sound_crash = mixer.Sound("pygame_Car/music/crash.wav")
    Sound_engine = mixer.Sound("pygame_Car/music/engine.wav")
    
    #내차 셋팅
    player = Car(Screenwidth/2,(ScreenHeight - 150),0,0)
    player.load_image()
    
    #상대편 차 만들기
    cars=[]
    car_count =3
    for i in range(car_count):
        x = random.randrange(0,Screenwidth-55)
        y = random.randrange(-150,50)
        car = Car(x,y,0,random.randint(5,10)) #상대편 자동차가 5-10 만큼의 속도로 달림. 
        car.load_image()
        cars.append(car)
        
    #주변 배경으로 하여금 움직이게 만들기(중앙차선 움직이게)
    lanes=[]
    lane_width =10
    lane_height =60
    lane_margin =15
    lane_count = 20
    lane_x = (Screenwidth - lane_width)/2
    lane_y = -10
    
    for i in range(lane_count):
        lanes.append([lane_x,lane_y])
        lane_y += lane_height +lane_margin
        
    score = 0
    crash = True
    game_on = True
    
    #게임 진행이벤트
    while game_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False
            
            #충돌시 스페이스 누르면 다시 시작   
            if crash:
                if event.type == pygame.KEYDOWN and event.key== pygame.K_SPACE:
                    crash = False
                    for i in range(car_count):
                        cars[i].x = random.randrange(0,Screenwidth-cars[i].width)
                        cars[i].y = random.randrange(-150,-50)
                        cars[i].load_image()
                        
                    player.load_image()
                    player.x = 175
                    player.dx =0
                    score =0
                    pygame.mouse.set_visible(False) #마우스 표시 안되게하기
                    Sound_engine.play()
                    sleep(5)
                    pygame.mixer.music.play(-1) #배경음 반복재생
                    
            #충돌하지 않았을때, 즉 게임중
            if not crash:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        player.dx =4
                    elif event.key == pygame.K_LEFT:
                        player.dx = -4
                        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        player.dx =0
                    elif event.key == pygame.K_LEFT:
                        player.dx =0
                        
                        
        screen.fill(WHITE)
        
        #충돌 안되었으면
        if not crash:
            #도로 차선 이동
            for i in range(lane_count):
                pygame.draw.rect(screen, BLACK, [lanes[i][0], lanes[i][1], lane_width, lane_height])
                lanes[i][1] +=10 #차선 속도
                if lanes[i][1] > ScreenHeight: #차선이 화면 길이를 넘어설경우
                    lanes[i][1] = -40-lane_height
                    
            player.draw_image()
            player.move_x()
            player.check_out_of_Screen()
            
            #스코어 300 넘을시에 플레이어 차도 속도 빨라지게함. 
            if score >300 :
                player.dy += 0.03
            
            #차 계속 그려주기
            for i in range(car_count):
                cars[i].draw_image()
                cars[i].y += cars[i].dy
                if cars[i].y > ScreenHeight:
                    score += 10
                    cars[i].x = random.randrange(0,Screenwidth - cars[i].width)
                    cars[i].y = random.randrange(-150, -50)
                    cars[i].dy = random.randint(5,10)
                    cars[i].load_image()

                #score 100 이 넘는경우 0.05씩 속도를 추가한다. 
                if score > 100:
                    cars[i].dy += 0.05
                    
            #충돌을 체크해준다.          
            for i in range(car_count):
                if player.check_crash(cars[i]):
                    crash=True
                    pygame.mixer.music.stop()
                    Sound_crash.play()
                    sleep(2)
                    pygame.mouse.set_visible(True)
                    break
                
            draw_score()
            pygame.display.flip()    
        else:
            draw_main_menu()
            
        clock.tick(60)
        
    pygame.quit()
    
            
                    
            
            
                        
                        
    
    
    
    

