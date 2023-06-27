import pygame
pygame.init()
from network import Network
import pickle
pygame.font.init()
width=800
height=800
win=pygame.display.set_mode((width,height))
pygame.display.set_caption("Client_1")
background_image=pygame.image.load("logo.jpg").convert()
class Button:
	def __init__(self,text,x,y,color):
		self.text=text
		self.x=x
		self.y=y
		self.color=color
		self.width=150
		self.height=100
	def draw(self,win):
		pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.height))
		font=pygame.font.SysFont("Agency FB",40)
		text=font.render(self.text,1,(0,0,0))
		win.blit(text,(self.x+round(self.width/2)-round(text.get_width()/2),self.y+round(self.height/2)-round(text.get_height()/2))) #source surface on this surface
	def click(self,pos):
		x1=pos[0]
		y1=pos[1]
		if self.x<=x1<=self.x+self.width and self.y<=y1<=self.y+self.height:
			return True#to check proper score updation
		else:
			return False
def redrawWindow(wind,game,p):
	global text_1,text_2
	wind.fill((200,175,250))
	if not(game.connected()):
		font=pygame.font.SysFont("Agency FB",80)
		text=font.render("Waiting for the Player...",1,(255,255,255),True)
		wind.blit(text,(width/2-text.get_width()/2,height/2-text.get_height()/2))
	else:
		font=pygame.font.SysFont("Agency FB",60)
		text=font.render("You_Are",1,(255,255,255))
		wind.blit(text,(80,165))
		font=pygame.font.SysFont("Agency FB",60)
		text=font.render("Opponent_is ",1,(255,255,255))
		wind.blit(text,(380,165))
		if p==1 and (game.done_bat[0]==1):#p1 chase
			text_1=font.render("Batsman..", 1,(255,255,255))
			text_2=font.render("Bowler..", 1, (255,255,255))
		elif p==0 and (game.done_bat[0]==1):#p0 inn end
			text_1=font.render("Bowler..",1,(255,255,255))
			text_2=font.render("Batsman..",1,(255,255,255))
		elif p==1:#player 2 bat first
			text_1=font.render("Bowler..",1,(255, 255, 255))
			text_2=font.render("Batsman..",1,(255, 255, 255))
		elif p==0:#player 1 bat first
			text_1=font.render("Batsman..",1,(255, 255, 255))
			text_2=font.render("Bowler..",1,(255, 255, 255))
		wind.blit(text_1,(80,200))
		wind.blit(text_2,(380,200))
		move1=game.get_player_move(0)
		move2=game.get_player_move(1)
		if game.bothWent():#to display move by both players
			text_1=font.render(move1,1,(0,0,0))
			text_2=font.render(move2,1,(0,0,0))
		else:
			if game.p1Went and p==0:# move by p1
				text_1=font.render(move1,1,(0,0,0))
			elif game.p1Went:# p1 game is held
				text_1=font.render("Locked_In",1,(0,0,0))
			else:
				text_1=font.render(":)Waiting...",1,(0,0,0))
			if game.p2Went and p==1:
				text_2=font.render(move2,1,(0, 0, 0))
			elif game.p2Went:
				text_2=font.render("Locked_In",1,(0,0,0))
			else:
				text_2=font.render(":)Waiting...", 1, (0,0,0))
		score1=game.get_player_score(0)
		score2=game.get_player_score(1)
		if p==1:# 2nd player window score after every move
			wind.blit(text_2, (100,350))
			wind.blit(text_1, (400,350))
			t_score1=font.render(str(score2),1,(255,75,75))
			t_score2=font.render(str(score1),1,(255,75,75))
		else: # 1st player window score after every move
			wind.blit(text_1,(100,350))
			wind.blit(text_2,(400,350))
			t_score1=font.render(str(score1),1,(255,75,75))
			t_score2=font.render(str(score2),1,(255,75,75))
		wind.blit(t_score1,(100,250))
		wind.blit(t_score2,(400,250))
		if game.done_bat[0]==1 and game.done_bat[1]==1:
			pass
		elif game.done_bat[0]==1 and game.get_player_score(1)==0 and p==1: #1st player bat done and 2nd player ready to bat
			text0=font.render("OPPONENT_IS_OUT",1,(255,75,75))
			wind.blit(text0,(75,100))
		elif game.done_bat[0]==1 and game.get_player_score(1)==0 and p==0:
			text0=font.render("YOU_ARE_OUT",1,(255,75,75))
			wind.blit(text0,(75,100))
		if (game.done_bat[p]==1 and game.done_bat[1-p]==0):
			for btn in btns2:
				btn.draw(wind)
		elif(game.done_bat[1-p] == 1 and game.done_bat[p]==0):
			for btn in btns1:
				btn.draw(wind)
		elif p==1:
			for btn in btns2:
				btn.draw(wind)
		elif p==0:
			for btn in btns1:
				btn.draw(wind)
	pygame.display.update()  # include buttons
btns1=[Button("1",75,450,(255,255,255)),Button("2",275,450,(255,255,255)),Button("3",475,450,(255,255,255)),Button("4",75,575,(255,255,255)),Button("5",275,575,(255,255,255)),Button("6", 475, 575, (255, 255, 255)),Button("0",275,700,(255,255,255))]
btns2=[Button("1",75,450,(255,255,255)),Button("2",275,450,(255,255,255)),Button("3",475,450,(255,255,255)),Button("4",75,575,(255,255,255)),Button("5",275,575,(255,255,255)),Button("6",475,575,(255,255,255))]
def main():
	run=True
	clock=pygame.time.Clock() #to keep track of time
	n=Network()
	player=int(n.getP())
	print("You are player",player)
	while run:
		clock.tick(60)
		try:
			game=n.send("get")
		except:
			run=False
			print("Couldn't get game")
			break
		if game.bothWent():#start of game
			print("game.bothWent()=",game.bothWent())
			redrawWindow(win,game,player)
			try:
				game=n.send("score")
			except:
				run=False
				print("Couldn't get game for score")
				break
		if game.done_bat[0] and game.done_bat[1]: #both inn done
			print("result")
			redrawWindow(win,game,player)
			pygame.time.delay(500)
			try:
				game = n.send("reset")
			except:
				run=False
				print("Could not get game")
				break
			font=pygame.font.SysFont("comicsans", 90)
			if(game.winner()==1 and player==1) or(game.winner()==0 and player==0):
				text=font.render("You Won the game!",1,(255,75,75))
			elif game.winner()==-1:
				text=font.render("Tie Game!",1,(255,75,75))
			else:
				text=font.render("You Lost the game..",1,(255,75,75))
			win.blit(text,(220, 25))
			pygame.display.update()
			pygame.time.delay(3000)
		for event in pygame.event.get():
			if event.type==pygame.QUIT:#to quit
				run=False
				pygame.quit()
			pos = [0,0]
			if event.type==pygame.MOUSEBUTTONDOWN:
				pos=pygame.mouse.get_pos()
			if (game.done_bat[player] == 1 and game.done_bat[1 - player] == 0):
				for btn in btns2:
					if btn.click(pos) and game.connected():
						if not (game.p1Went):
							n.send(btn.text)
							print(btn.text)
			elif (game.done_bat[1 - player] == 1 and game.done_bat[player] == 0):
				for btn in btns1:
					if btn.click(pos) and game.connected():
						if not (game.p2Went):
							n.send(btn.text)
							print(btn.text)
			elif player == 1:
				for btn in btns2:
					if btn.click(pos) and game.connected():
						if not (game.p2Went):
							n.send(btn.text)
							print(btn.text)
			elif player == 0:
				for btn in btns1:
					if btn.click(pos) and game.connected():
						if not (game.p1Went):
							n.send(btn.text)
							print(btn.text)
		redrawWindow(win,game,player)
def menu_screen():
	run=True
	clock=pygame.time.Clock()
	while run:
		clock.tick(5)
		win.fill((255,255,255))
		font=pygame.font.SysFont("comicsans",60)
		text=font.render("Click screen to Play!",1,(0,0,0))
		win.blit(text, (220, 10))
		pygame.display.update()
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				run=False
			if event.type==pygame.MOUSEBUTTONDOWN:
				run=False
		win.blit(background_image,[70,100])
		pygame.display.update()
	main()
while True:
	menu_screen()
