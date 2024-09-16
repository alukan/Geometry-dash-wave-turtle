import turtle as t
import random
import keyboard


def gen_obstacle(start, place):
    return [BuiltLine, BuiltMount][random.randint(0, 1)](start, place)


class BuiltMount:
    def __init__(self, start, place):
        self.start = start
        self.place = place
        self.length = random.randint(windowWidth // 3, windowWidth * 2)
        if place < 0:
            self.height = place + random.randint(80, windowHeight // 3)
        else:
            self.height = place - random.randint(80, windowHeight // 2)

    def draw(self):
        t.goto(self.start, self.place)
        t.goto(self.start + self.length // 2, self.height)
        t.goto(self.start + self.length, self.place)
        if (self.start < 0) and self.start + self.length // 2 > 0:
            if self.place < 0:
                y = (0 - self.start) * (self.height - self.place) / (self.length / 2)
                y = self.place + y
            else:
                y = (0 - self.start) * (self.place - self.height) / (self.length / 2)
                y = self.place - y
        elif self.start + self.length > 0 and self.start + self.length // 2 < 0:
            if self.place < 0:
                y = (0 - (self.start + self.length / 2)) * (self.height - self.place) / (self.length / 2)
                y = self.height - y
            else:
                y = (0 - (self.start + self.length / 2)) * (self.place - self.height) / (self.length / 2)
                y = self.height + y
        else:
            y = 0
        return y, self.start + self.length


class BuiltLine:
    def __init__(self, start, place):
        self.start = start
        self.length = random.randint(windowWidth, windowWidth * 3)
        if place < 0:
            self.place = place + random.randint(50, windowHeight // 4)
        else:
            self.place = place - random.randint(50, windowHeight // 4)

    def draw(self):
        t.goto(max(x_left, self.start), self.place)
        t.goto(min(x_right, self.start + self.length), self.place)
        if self.start < 0 and self.start + self.length:
            y = self.place
        else:
            y = 0
        return y, self.start + self.length


def drawWay(way, right):
    t.penup()
    t.goto(-right, way[0])
    t.pendown()
    t.color("red")
    for i in range(1, len(way)):
        t.goto(i - right, way[i])


def main(speed, speed_ARROW, acceleration, enableWay):
    screen = t.Screen()
    screen.setup(1200, 600)

    t.speed(0)
    t.tracer(0)
    screen.bgcolor('black')

    t.hideturtle()

    windowWidth = screen.window_width()
    windowHeight = screen.window_height()

    x_left = -windowWidth // 2
    x_right = windowWidth // 2
    y_top = windowHeight // 2 - 10
    y_bottom = -windowHeight // 2 + 10
    arr_y = 0
    mx = y_top
    mn = y_bottom
    gravity = 1
    score = 0

    obstacles_top = []
    obstacles_top.append(gen_obstacle(x_left, y_top))
    obstacles_top.append(gen_obstacle(obstacles_top[0].start + obstacles_top[0].length + 1, y_top))
    obstacles_top.append(gen_obstacle(obstacles_top[1].start + obstacles_top[1].length + 1, y_top))
    obstacles_top.append(gen_obstacle(obstacles_top[2].start + obstacles_top[2].length + 1, y_top))

    obstacles_bottom = []
    obstacles_bottom.append(gen_obstacle(x_left, y_bottom))
    obstacles_bottom.append(gen_obstacle(obstacles_bottom[0].start + obstacles_bottom[0].length + 1, y_bottom))
    obstacles_bottom.append(gen_obstacle(obstacles_bottom[1].start + obstacles_bottom[1].length + 1, y_bottom))
    obstacles_bottom.append(gen_obstacle(obstacles_bottom[2].start + obstacles_bottom[2].length + 1, y_bottom))

    way = [0 for i in range(x_right - 1)]
    while True:

        score += speed
        t.color("green")
        t.penup()
        x = x_left
        t.goto(x, y_top)
        t.pendown()
        while x < x_right:
            if (score) % 10000 > (x_right + score) % 10000 and score >= 10000 - windowWidth \
                    and (score // 10000) % 2 == 0:
                t.color('blue')
                prev_pos = t.pos()
                x_port = 10000 - (score % 10000)
                t.penup()
                t.goto(x_port, y_top)
                t.pendown()
                t.goto(x_port, 0)
                t.penup()
                t.goto(prev_pos)
                t.pendown()
                t.color('green')
            if (obstacles_top[0].start + obstacles_top[0].length < x_left) and len(obstacles_top) > 1:
                obstacles_top = obstacles_top[1:]
                obstacles_top.append(gen_obstacle(obstacles_top[2].start + obstacles_top[2].length + 1, y_top))

            for j in range(len(obstacles_top)):
                if j >= len(obstacles_top):
                    break
                [val, x] = obstacles_top[j].draw()
                obstacles_top[j].start -= speed
                if val != 0:
                    mx = val
            if x >= x_right:
                break
        t.penup()
        t.color("red")
        x = x_left
        t.goto(x, y_bottom)
        t.pendown()
        while x < x_right:
            if (score) % 10000 > (x_right + score) % 10000 and score >= 10000 - windowWidth \
                    and (score // 10000) % 2 == 1:
                t.color('blue')
                prev_pos = t.pos()
                x_port = 10000 - (score % 10000)
                t.penup()
                t.goto(x_port, y_bottom)
                t.pendown()
                t.goto(x_port, 0)
                t.penup()
                t.goto(prev_pos)
                t.pendown()
                t.color('red')
                
            if (obstacles_bottom[0].start + obstacles_bottom[0].length < x_left) and len(obstacles_bottom) > 1:
                obstacles_bottom = obstacles_bottom[1:]
                obstacles_bottom.append(
                    gen_obstacle(obstacles_bottom[2].start + obstacles_bottom[2].length + 1, y_bottom))

            for j in range(len(obstacles_bottom)):
                if j >= len(obstacles_bottom):
                    break
                [val, x] = obstacles_bottom[j].draw()
                obstacles_bottom[j].start -= speed
                if val != 0:
                    mn = val
            if x >= x_right:
                break
        t.penup()
        if enableWay:
            drawWay(way, x_right)
            way = way[1:] + [arr_y]
        if keyboard.is_pressed("up arrow") or keyboard.is_pressed("w"):
            arr_y += speed_ARROW * gravity
            t.setheading(45 * gravity)
        else:
            arr_y -= speed_ARROW * gravity
            t.setheading(-45 * gravity)

        t.goto(0, int(arr_y))
        t.showturtle()
        t.penup()
        t.color("red")

        if score % 5000 <= speed:
            speed += acceleration
            speed_ARROW += acceleration
        if (((int(score) // 10000) % 2 == 1 and arr_y > 0)
            or ((int(score) // 10000) % 2 == 0 and arr_y <= 0)) and score % 10000 <= speed and score >= 10000:
            gravity *= -1
        if arr_y > mx or arr_y < mn:
            pos = t.pos()
            t.goto(0, 0)
            t.write("GAME OVER \n YOUR SCORE IS: " + str(int(score)) + "\n Press enter to restart",
                    align='left', font=('Arial', 18, 'normal'))
            t.goto(pos)
            break
        else:
            screen.update()
            t.clear()


print("Input horisontal speed")
SPEED = float(input())
print("Input vertical speed")
SPEED_ARROW = float(input())
print("Input acceleration")
ACCELERATION = float(input())
print("Do you want to turn on way? 1 for yes, 0 for no")
way = int(input())

screen = t.Screen()
screen.setup(1400, 600)

t.speed(0)
t.tracer(0)
screen.bgcolor('black')

t.hideturtle()

windowWidth = screen.window_width()
windowHeight = screen.window_height()

x_left = -windowWidth // 2
x_right = windowWidth // 2
y_top = windowHeight // 2 - 10
y_bottom = -windowHeight // 2 + 10

def is_outside_screen(x, y):
    """Check if a point (x, y) is outside the screen boundaries."""
    if x < -windowWidth or x > windowWidth or y < -windowHeight or y > windowHeight:
        return True
    return False

t.color("yellow")
t.write("Press enter to start", align='left', font=('Arial', 18, 'normal'))
while True:
    if keyboard.is_pressed("enter"):
        main(SPEED, SPEED_ARROW, ACCELERATION, way)
    else:
        screen.update()
