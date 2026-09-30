import pygame
import math
import copy

pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

# --- CONFIGURATION PARAMETERS ---
CLOTH_COLS = 24                 # Number of vertices horizontally
CLOTH_ROWS = 20                 # Number of vertices vertically
SPACING = 18                    # Distance between neighboring vertices (pixels)
CONSTRAINT_ITERATIONS = 12      # Higher numbers make the fabric stiffer
GRAVITY = 0.4                   # Downward acceleration force
CLICK_RADIUS = 18               # Mouse grab detection radius
TEAR_RADIUS = 15                # How close the scissor cursor must be to cut a link

class Point:
    def __init__(self, x, y, pinned=False):
        self.x = x
        self.y = y
        self.old_x = x
        self.old_y = y
        self.pinned = pinned
        
    def reset(self, x, y):
        self.x = x
        self.y = y
        self.old_x = x
        self.old_y = y

class Link:
    def __init__(self, point_a, point_b, length):
        self.point_a = point_a
        self.point_b = point_b
        self.length = length

# --- INITIALIZATION FUNCTION ---
# We package this up so we can call it again whenever the user triggers a restore
def setup_cloth():
    grid = []
    start_x = (800 - (CLOTH_COLS - 1) * SPACING) / 2
    start_y = 120

    for row in range(CLOTH_ROWS):
        row_points = []
        for col in range(CLOTH_COLS):
            x_pos = start_x + col * SPACING
            y_pos = start_y + row * SPACING
            
            # Pin every 4th node across the top row to anchor the fabric
            is_pinned = (row == 0 and col % 4 == 0)
            row_points.append(Point(x_pos, y_pos, pinned=is_pinned))
        grid.append(row_points)

    flat_points = [p for row in grid for p in row]

    mesh_links = []
    for row in range(CLOTH_ROWS):
        for col in range(CLOTH_COLS):
            if col < CLOTH_COLS - 1:
                mesh_links.append(Link(grid[row][col], grid[row][col+1], SPACING))
            if row < CLOTH_ROWS - 1:
                mesh_links.append(Link(grid[row][col], grid[row+1][col], SPACING))
                
    return grid, flat_points, mesh_links

# Build the cloth structure initially
points_grid, all_points, links = setup_cloth()

# Interactivity States
running = True
selected_point = None
tear_mode = False  

# Setup visual UI text font
font = pygame.font.SysFont("Arial", 20)

while running:
    screen.fill((15, 15, 25)) 
    clock.tick(60)
    
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.KEYDOWN:
            # Toggle Tear Mode using the 'T' key
            if event.key == pygame.K_t:
                tear_mode = not tear_mode
                if tear_mode:
                    selected_point = None
            
            # RESTORE FUNCTION: Reset mesh structure completely when 'R' is pressed
            elif event.key == pygame.K_r:
                selected_point = None
                points_grid, all_points, links = setup_cloth()
            
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not tear_mode:
                closest_point = None
                min_dist = CLICK_RADIUS
                for p in all_points:
                    dist = math.hypot(p.x - mouse_x, p.y - mouse_y)
                    if dist < min_dist:
                        min_dist = dist
                        closest_point = p
                if closest_point:
                    selected_point = closest_point

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            selected_point = None

    # --- TEAR MODE CUTTING LOGIC ---
    if tear_mode and pygame.mouse.get_pressed()[0]:
        active_links = []
        for link in links:
            mid_x = (link.point_a.x + link.point_b.x) / 2
            mid_y = (link.point_a.y + link.point_b.y) / 2
            
            if math.hypot(mid_x - mouse_x, mid_y - mouse_y) > TEAR_RADIUS:
                active_links.append(link)
        links = active_links

    # --- PHYSICS UPDATE ---
    if selected_point and not tear_mode:
        selected_point.x = mouse_x
        selected_point.y = mouse_y
        selected_point.old_x = mouse_x
        selected_point.old_y = mouse_y

    # Step A: Apply gravity and calculate Verlet velocity
    for p in all_points:
        if not p.pinned and p != selected_point:
            vx = p.x - p.old_x
            vy = p.y - p.old_y
            
            p.old_x = p.x
            p.old_y = p.y
            
            p.x += vx
            p.y += vy + GRAVITY

    # Step B: Solve Distance Constraints
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
    # Render threads
    for link in links:
        pygame.draw.line(screen, (70, 130, 180), (link.point_a.x, link.point_a.y), (link.point_b.x, link.point_b.y), 1)

    # Render anchors and nodes
    for p in all_points:
        if p == selected_point:
            pygame.draw.circle(screen, (0, 255, 0), (int(p.x), int(p.y)), 5)
        elif p.pinned:
            pygame.draw.circle(screen, (255, 60, 100), (int(p.x), int(p.y)), 4)

    # Draw UI text indicators onto screen
    status_text = "TEAR MODE (SCISSORS)" if tear_mode else "DRAG MODE (STRETCH)"
    status_color = (255, 60, 100) if tear_mode else (0, 255, 150)
    
    txt_surface = font.render(f"Mode: {status_text}", True, status_color)
    hint_surface = font.render("Press [T] to Toggle Mode | Press [R] to RESTORE Fabric Mesh", True, (200, 200, 200))
    
    screen.blit(txt_surface, (20, 20))
    screen.blit(hint_surface, (20, 45))

    pygame.display.flip()

pygame.quit()
