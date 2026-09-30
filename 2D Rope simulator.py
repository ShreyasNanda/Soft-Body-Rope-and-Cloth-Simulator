import pygame
import math

pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

# --- CONFIGURATION PARAMETERS ---
NUM_VERTICES = 35               # Change this to add more or fewer vertices
ROPE_LENGTH = 450               # Total length of the rope in pixels
CONSTRAINT_ITERATIONS = 15      # Higher numbers make high-vertex ropes stiffer
GRAVITY = 0.5                   # Downward acceleration force
CLICK_RADIUS = 20               # Mouse grab detection radius

SEGMENT_LENGTH = ROPE_LENGTH / (NUM_VERTICES - 1)

class Point:
    def __init__(self, x, y, pinned=False):
        self.x = x
        self.y = y
        self.old_x = x
        self.old_y = y
        self.pinned = pinned 

class Link:
    def __init__(self, point_a, point_b, length):
        self.point_a = point_a
        self.point_b = point_b
        self.length = length

# 1. Spawn vertices dynamically
points = []
for i in range(NUM_VERTICES):
    is_pinned = (i == 0)  # Pin the very first node to the ceiling
    x_pos = 400
    y_pos = 100 + (i * SEGMENT_LENGTH)
    points.append(Point(x_pos, y_pos, pinned=is_pinned))

# 2. Connect vertices dynamically with links
links = []
for i in range(len(points) - 1):
    links.append(Link(points[i], points[i+1], SEGMENT_LENGTH))

running = True
selected_point = None

while running:
    screen.fill((20, 20, 30)) 
    dt = clock.tick(60)
    
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            closest_point = None
            min_dist = CLICK_RADIUS
            
            for p in points:
                dist = math.hypot(p.x - mouse_x, p.y - mouse_y)
                if dist < min_dist:
                    min_dist = dist
                    closest_point = p
            
            if closest_point:
                selected_point = closest_point

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            selected_point = None

    # --- PHYSICS UPDATE ---
    
    # Force the grabbed vertex to lock to the mouse cursor
    if selected_point:
        selected_point.x = mouse_x
        selected_point.y = mouse_y
        selected_point.old_x = mouse_x
        selected_point.old_y = mouse_y

    # Step A: Apply gravity and calculate Verlet velocity
    for p in points:
        if not p.pinned and p != selected_point:
            vx = p.x - p.old_x
            vy = p.y - p.old_y
            
            p.old_x = p.x
            p.old_y = p.y
            
            p.x += vx
            p.y += vy + GRAVITY

    # Step B: Solve distance link constraints iteratively
    for _ in range(CONSTRAINT_ITERATIONS): 
        for link in links:
            dx = link.point_b.x - link.point_a.x
            dy = link.point_b.y - link.point_a.y
            distance = math.hypot(dx, dy)
            
            if distance == 0: 
                continue
                
            difference = link.length - distance
            percent = (difference / distance) / 2
            
            offset_x = dx * percent
            offset_y = dy * percent
            
            if not link.point_a.pinned and link.point_a != selected_point:
                link.point_a.x -= offset_x
                link.point_a.y -= offset_y
            if not link.point_b.pinned and link.point_b != selected_point:
                link.point_b.x += offset_x
                link.point_b.y += offset_y

    # --- DRAWING ---
    for link in links:
        pygame.draw.line(screen, (0, 255, 200), (link.point_a.x, link.point_a.y), (link.point_b.x, link.point_b.y), 3)

    for p in points:
        if p == selected_point:
            color = (0, 255, 0)       # Green when dragging
        elif p.pinned:
            color = (255, 0, 100)     # Pink for structural anchor
        else:
            color = (255, 255, 255)   # White for free vertices
            
        pygame.draw.circle(screen, color, (int(p.x), int(p.y)), 5)

    pygame.display.flip()

pygame.quit()
