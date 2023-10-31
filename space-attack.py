import turtle as t
import time
import math
import random
SPEED = 4
SLEEP = 0.005
MUNICAO = 10
RECHARGE = 2
end = False
score = 0

def ccw(a,b,c):
    return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])

def intersect(a,b,c,d):
    return ccw(a,c,d) != ccw(b,c,d) and ccw(a,b,c) != ccw(a,b,d)

def draw_rectangle(x1,y1,x2,y2,color = False):
    if color:
        pen = t.Turtle()
        pen.color(color)
        pen.ht()
        pen.up()
        pen.goto(x1,y1)
        pen.down()
        pen.begin_fill()
        pen.goto(x2,y1)
        pen.goto(x2,y2)
        pen.goto(x1,y2)
        pen.goto(x1,y1)
        pen.end_fill()
    return ((x1,y1),(x2,y2))

def position_image(x,y,width,height,shape):
    pen = t.Turtle()
    pen.up()
    pen.goto(x,y)
    pen.shape(shape)
    return ((x - width / 2,y + height / 2),(x + width / 2,y - height / 2))

def draw_environment(screen):
    elements = []
    w,h = 1080,720
    screen.screensize(w,h)
    y1 = -h // 3
    y2 = y1 - h // 2
    elements.append(draw_rectangle(-w / 1.5,y2 + 1000,-w / 2,y2))
    elements.append(draw_rectangle(w / 2,y2 + 1000,w / 1.5,y2))
    elements.append(draw_rectangle(-w,y1,w,y2))
    elements.append(position_image(0,-175,400,110,'carro.gif'))
    return elements

def check_colisions(box,newbox,ambiente):
    v_colision,h_colision = False,False
    pointsnew = [*newbox,(newbox[0][0],newbox[1][1]),(newbox[1][0],newbox[0][1])]
    pointsold = [*box,(box[0][0],box[1][1]),(box[1][0],box[0][1])]
    for element in ambiente:
        for i,point in enumerate(pointsnew):
            if (element[0][0] < point[0] < element[1][0]) and (element[0][1] > point[1] > element[1][1]):
                oldpoint = pointsold[i]
                if (element[0][0] < oldpoint[0] < element[1][0]) and (element[0][1] > point[1] > element[1][1]):
                    v_colision = True
                if (element[0][0] < point[0] < element[1][0]) and (element[0][1] > oldpoint[1] > element[1][1]):
                    h_colision = True
                if not v_colision and not h_colision:
                    h_colision = True
        if v_colision and h_colision:
            break
    return v_colision,h_colision

def erase_bullet(bulet):
    bulet.clear()
    del(bulet)

def kill_enemy(enemy):
    enemy.ht()
    del(enemy)

def explode_enemy(enemy):
    enemy.shape('explosion.gif')
    t.ontimer(lambda: kill_enemy(enemy),500)

def blink(tr,done = 0):
    if done >= 10:
        tr.st()
        return
    if tr.isvisible():
        tr.ht()
    else:
        tr.st()
    t.ontimer(lambda: blink(tr,done + 1),50)

def clear_screen(screen):
    for turtle in screen.turtles():
        turtle.frozen = True
    Text(0,0,'Game Over',100,'red','center')
    with open('recorde','r') as f:
        recorde = int(f.read())
    if score > recorde:
        Text(0,-100,'Novo Recorde',100,'orange','center')
        with open('recorde','w') as f:
            f.write(str(score))
    global end
    end = True

def game_over(screen,player):
    player.shape('explosion.gif')
    player.frozen = True
    t.ontimer(lambda: clear_screen(screen),1000)

class Text(t.Turtle):
    def __init__(self,x,y,text,size,color,align):
        super().__init__()
        self.align = align
        self.font = ('Times New Roman',size,'bold')
        self.up()
        self.ht()
        self.goto(x,y)
        self.color(color)
        self.write(text,align = self.align,font = self.font)
    def update(self,text):
        self.clear()
        self.write(text,align = self.align,font = self.font)

class Player(t.Turtle):
    def __init__(self):
        super().__init__()
        self.up()
        self.st()
        self.horizontal_speed = 0
        self.vertical_speed = 0
        self.width = 30
        self.height = 35
        self.angle_speed = 0
        self.locked = False
        self.frozen = False
        self.mira = t.Turtle()
        self.mira.up()
        self.mira.goto(100,0)
        self.mira.turtlesize(2,2)
        self.bullets = MUNICAO
        self.last_recharge = time.time()
    def update(self,ambiente):
        if self.frozen:
            return
        now = time.time()
        if now - self.last_recharge > RECHARGE:
            self.bullets += 1
            self.bullets = min(self.bullets,MUNICAO)
            self.last_recharge = now
        if self.vertical_speed > -SPEED * 10:
            self.vertical_speed -= (SPEED ** 2) / 25
        current_h_speed = self.horizontal_speed
        x,y = self.pos()
        newx,newy = x + self.horizontal_speed,y + self.vertical_speed
        box = self.box(x,y)
        newbox = self.box(newx,newy)
        v_colision,h_colision = check_colisions(box,newbox,ambiente)
        if v_colision:
            self.vertical_speed = 0
        if h_colision or self.locked:
            current_h_speed = 0
        mira_angle = self.mira.heading()
        new_angle = mira_angle + self.angle_speed
        new_mira_x,new_mira_y = x + math.cos(2 * math.pi * new_angle / 360) * 100,y + math.sin(2 * math.pi * new_angle / 360) * 100
        self.mira.seth(new_angle)
        self.mira.goto(new_mira_x,new_mira_y)
        self.goto(x + current_h_speed,y + self.vertical_speed)
        mira_x,mira_y = self.mira.pos()
        self.mira.goto(mira_x + current_h_speed,mira_y + self.vertical_speed)
    def box(self,x,y):
        return ((x - self.width / 2,y + self.height / 2),(x + self.width / 2,y - self.height / 2))
    def move_left(self):
        self.horizontal_speed = -SPEED
        self.angle_speed = SPEED
        self.shape('gunman_l.gif')
    def move_right(self):
        self.horizontal_speed = SPEED
        self.angle_speed = -SPEED
        self.shape('gunman_r.gif')
    def jump(self):
        if self.vertical_speed == 0:
            self.vertical_speed = SPEED * 5
    def stop_movement(self):
        self.horizontal_speed = 0
        self.angle_speed = 0
    def lock_position(self):
        self.locked = True
    def release_lock(self):
        self.locked = False
    def shot(self,enemy_set):
        if self.bullets > 0:
            bullet = t.Turtle()
            bullet.color('red')
            bullet.up()
            bullet.goto(*self.pos())
            bullet.seth(self.mira.heading())
            bullet.down()
            pointA = bullet.pos()
            bullet.forward(2000)
            pointB = bullet.pos()
            enemy_set.shot(pointA,pointB)
            t.ontimer(lambda: erase_bullet(bullet),100)
            self.bullets -= 1

class Enemy(t.Turtle):
    def __init__(self):
        super().__init__()
        self.up()
        self.speed = SPEED / 4
        self.hp = 2
        self.fly = True
        self.width = 200
        self.height = 200
        self.sh = 'alien1'
        self.vertical_speed = 0
        self.frozen = False
    def update(self,player,ambiente,screen):
        if self.frozen:
            return
        px,py = player.pos()
        x,y = self.pos()
        if (x - (self.width / 2) < px < x + (self.width / 2)) and (y - (self.height / 2) < py < y + (self.height / 2)):
            game_over(screen,player)
        if self.fly:
            dis = math.sqrt((px - x) ** 2 + (py - y) ** 2)
            h_speed,v_speed = self.speed * (px - x) / dis,self.speed * (py - y) / dis
        else:
            if (px - x) > 0:
                h_speed = self.speed
            elif (px - x) < 0:
                h_speed = -self.speed
            else:
                h_speed = 0
            v_speed = self.vertical_speed - (SPEED ** 2) / 25
        newx,newy = x + h_speed,y + v_speed
        box = self.box(x,y)
        newbox = self.box(newx,newy)
        v_colision,h_colision = check_colisions(box,newbox,ambiente)
        if v_colision:
            v_speed = 0
        if h_colision:
            h_speed = 0
        self.vertical_speed = v_speed
        self.goto(x + h_speed,y + v_speed)
        if h_speed > 0:
            self.shape(f'{self.sh}_r.gif')
        if h_speed < 0:
            self.shape(f'{self.sh}_l.gif')
    def box(self,x,y):
        return ((x - self.width / 2,y + self.height / 2),(x + self.width / 2,y - self.height / 2))
    
class Alien2(Enemy):
    def __init__(self):
        super().__init__()
        self.hp = 3
        self.speed = SPEED / 5
        self.fly = False
        self.width = 200
        self.height = 200
        self.sh = 'alien2'

class Alien3(Enemy):
    def __init__(self):
        super().__init__()
        self.hp = 1
        self.speed = SPEED / 3
        self.width = 100
        self.height = 100
        self.sh = 'alien3'

class EnemySet():
    def __init__(self):
        self.enemies = []
        self.time_to_spawn = 5.0
        self.enemy_types = [Enemy,Alien2,Alien3]
        self.last_spawn = time.time()
    def update(self,player,ambiente,screen):
        now = time.time()
        if (now - self.last_spawn) > self.time_to_spawn:
            new_enemy = random.choice(self.enemy_types)()
            if not new_enemy.fly:
                x,y = random.choice((-1000,1000)),1000
            else:
                x,y = random.randint(-1000,1000),1000
            new_enemy.goto(x,y)
            self.enemies.append(new_enemy)
            self.last_spawn = now
            self.time_to_spawn = self.time_to_spawn - .1 if self.time_to_spawn > 1 else self.time_to_spawn
        for enemy in self.enemies:
            enemy.update(player,ambiente,screen)
    def shot(self,pointA,pointB):
        global score
        alive = []
        for enemy in self.enemies:
            box = enemy.box(*enemy.pos())
            points = [*box,(box[0][0],box[1][1]),(box[1][0],box[0][1])]
            segs = (points[0],points[2]),(points[0],points[3]),(points[1],points[2]),(points[1],points[3])
            for seg in segs:
                if intersect(*seg,pointA,pointB):
                    enemy.hp -= 1
                    if enemy.hp > 0:
                        blink(enemy)
                    break
            if enemy.hp > 0:
                alive.append(enemy)
            else:
                explode_enemy(enemy)
                score += 1
        self.enemies = alive

if __name__ == '__main__':
    screen = t.Screen()
    screen.tracer(0)
    screen.bgpic("background.gif")
    screen.register_shape('gunman_l.gif')
    screen.register_shape('gunman_r.gif')
    screen.register_shape('alien1_l.gif')
    screen.register_shape('alien2_l.gif')
    screen.register_shape('alien3_l.gif')
    screen.register_shape('alien1_r.gif')
    screen.register_shape('alien2_r.gif')
    screen.register_shape('alien3_r.gif')
    screen.register_shape('carro.gif')
    screen.register_shape('explosion.gif')
    ambiente = draw_environment(screen)
    player = Player()
    player.shape('gunman_l.gif')
    enemies = EnemySet()
    bullets = Text(-500,-350,f'Munição: {MUNICAO}',25,'black','left')
    kills = Text(200,-350,f'Inimigos Derrotados: {score}',25,'black','left')

    screen.listen()
    t.onkeypress(lambda: player.move_left(),'Left')
    t.onkeyrelease(lambda: player.stop_movement(),'Left')
    t.onkeypress(lambda: player.move_right(),'Right')
    t.onkeyrelease(lambda: player.stop_movement(),'Right')
    t.onkeypress(lambda: player.jump(),'Up')
    t.onkeypress(lambda: player.lock_position(),'Down')
    t.onkeyrelease(lambda: player.release_lock(),'Down')
    t.onkeypress(lambda: player.shot(enemies),'space')

    def update_screen():
        player.update(ambiente)
        enemies.update(player,ambiente[2:],screen)
        screen.update()
        bullets.update(f'Munição: {player.bullets}')
        kills.update(f'Inimigos Derrotados: {score}')
    
    while not end:
        begin = time.time()
        update_screen()
        delay = time.time() - begin
        if delay < SLEEP:
            time.sleep(SLEEP - delay)
    screen.mainloop()