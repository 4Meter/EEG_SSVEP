import pygame
import numpy as np
from PIL import Image
import math
import time

def load_maze(image_path):
    image = Image.open(image_path).convert('L')
    maze_array = np.array(image)
    threshold = 128
    binary_maze = (maze_array < threshold).astype(int)
    return binary_maze

def is_path_free(maze, position, radius, tile_size):
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            if dx*dx + dy*dy <= radius*radius:
                px = (position[0] + dx) // tile_size
                py = (position[1] + dy) // tile_size
                if px < 0 or px >= maze.shape[1] or py < 0 or py >= maze.shape[0] or maze[py, px] == 1:
                    return False
    return True

def check_if_at_edge(position, radius, maze_dimensions, tile_size):
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            if dx*dx + dy*dy <= radius*radius:
                px = (position[0] + dx) // tile_size
                py = (position[1] + dy) // tile_size
                if px <= 0 or px >= maze_dimensions[1] - 1 or py <= 0 or py >= maze_dimensions[0] - 1:
                    return True
    return False

def triangle_point(base_center, width, height, direction):
    offset = 100
    if direction == "down":
        center = (base_center[0], base_center[1] + offset)
        points = [center, (center[0] - width//2, center[1] - height), (center[0] + width//2, center[1] - height)]
    elif direction == "up":
        center = (base_center[0], base_center[1] - offset)
        points = [center, (center[0] - width//2, center[1] + height), (center[0] + width//2, center[1] + height)]
    elif direction == "right":
        center = (base_center[0] + offset, base_center[1])
        points = [center, (center[0] - height, center[1] - width//2), (center[0] - height, center[1] + width//2)]
    elif direction == "left":
        center = (base_center[0] - offset, base_center[1])
        points = [center, (center[0] + height, center[1] - width//2), (center[0] + height, center[1] + width//2)]
    return points

def main():
    pygame.init()
    image_path = 'map3.png'
    binary_maze = load_maze(image_path)

    # maze parameters
    TILE_SIZE = 1
    MOVE_STEP = 20
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BORDER_RATIO = 0.6
    maze_width = binary_maze.shape[1] * TILE_SIZE
    maze_height = binary_maze.shape[0] * TILE_SIZE
    screen_width = binary_maze.shape[1] * TILE_SIZE * (1 + BORDER_RATIO*2)
    screen_height = binary_maze.shape[0] * TILE_SIZE * (1 + BORDER_RATIO*2) + 50 
    maze_offset = (maze_width*BORDER_RATIO, maze_height*BORDER_RATIO)

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Maze Game")

    # triangles
    triangle_base = 200
    triangle_height = 100
    triangle_offset = 100
    frequency = [7, 9, 11, 13] # up, down, left, right
    POINTS = [
        triangle_point((maze_offset[0] + maze_width//2, maze_offset[1] - triangle_offset), triangle_base, triangle_height, 'up'),
        triangle_point((maze_offset[0] + maze_width//2, maze_offset[1] + maze_height + triangle_offset), triangle_base, triangle_height, 'down'),
        triangle_point((maze_offset[0] - triangle_offset, maze_offset[1] + maze_height//2), triangle_base, triangle_height, 'left'),
        triangle_point((maze_offset[0] + maze_width + triangle_offset, maze_offset[1] + maze_height//2), triangle_base, triangle_height, 'right'),
    ]
    start_time = time.time()

    maze_surf = pygame.Surface(binary_maze.shape[::-1])
    for y in range(binary_maze.shape[0]):
        for x in range(binary_maze.shape[1]):
            color = WHITE if binary_maze[y, x] == 0 else BLACK
            maze_surf.set_at((x, y), color)
    maze_surf = pygame.transform.scale(maze_surf, (maze_width, maze_height))

    player_radius = 10
    player_color = (255, 0, 0)
    center_position = (binary_maze.shape[1] // 2 * TILE_SIZE, binary_maze.shape[0] // 2 * TILE_SIZE)
    init_pos = [center_position[0], center_position[1] - 40]
    player_pos = init_pos

    victory = False
    font = pygame.font.Font(None, 36)
    victory_text = font.render('You Win! Press Enter to Restart', True, (0, 255, 0))
    clock = pygame.time.Clock()

    running = True
    while running:
        # keyboard control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if victory and event.key == pygame.K_RETURN:
                    player_pos = init_pos
                    victory = False
                elif not victory:
                    step = MOVE_STEP
                    while step > 0:
                        move = {
                            pygame.K_LEFT: (-TILE_SIZE*step, 0),
                            pygame.K_RIGHT: (TILE_SIZE*step, 0),
                            pygame.K_UP: (0, -TILE_SIZE*step),
                            pygame.K_DOWN: (0, TILE_SIZE*step),
                        }.get(event.key, (0, 0))
                        
                        next_pos = [player_pos[0] + move[0], player_pos[1] + move[1]]
                        
                        if is_path_free(binary_maze, next_pos, player_radius, TILE_SIZE):
                            player_pos = next_pos
                            break
                        else:
                            step -= 2

        if not victory and check_if_at_edge(player_pos, player_radius, binary_maze.shape, TILE_SIZE):
            victory = True

        screen.fill(WHITE)
        screen.blit(maze_surf, maze_offset)
        pygame.draw.circle(screen, player_color, (player_pos[0]+maze_offset[0], player_pos[1]+maze_offset[1]), player_radius)
        t = time.time() - start_time
        for i in range(4):
            color_value = int((math.sin(2 * math.pi * frequency[i] * t) + 1) / 2 * 255)
            color = (color_value, color_value, color_value)  # Convert to grayscale
            pygame.draw.polygon(screen, color, POINTS[i])

        if victory:
            screen.blit(victory_text, (screen_width // 2 - victory_text.get_width() // 2, screen_height - victory_text.get_height() * 1.5))

        # Calculate and display FPS
        fps = clock.tick(125)  # Limit to 60 FPS
        fps_text = font.render(f'FPS: {int(clock.get_fps())}', True, BLACK)
        screen.blit(fps_text, (10, 10))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
