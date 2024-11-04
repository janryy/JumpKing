import pygame
import random

pygame.init()

screen = pygame.display.set_mode((800,750))

clock = pygame.time.Clock()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

# Load background image
background_image = pygame.image.load("background.png")
background_image_2 = pygame.image.load("background2.tiff")
background_image_3 = pygame.image.load("background3.tiff")
background_image_4 = pygame.image.load("background4.tiff")
background_image_4 = pygame.transform.scale(background_image_4, (SCREEN_WIDTH, SCREEN_HEIGHT))
easter_egg_background = pygame.image.load("easter_egg_background.jpg")
background_image_3 = pygame.transform.scale(background_image_3, (SCREEN_WIDTH, SCREEN_HEIGHT))

class Player(pygame.Rect):  # player class
    def __init__(self, x, y, image_path_right, image_path_left):
        super().__init__(x, y, 40, 40)  # Initial size will adjust to image
        self.vy = 0  # Vertical velocity
        self.vx = 0  # Horizontal velocity
        self.charge = 0  # Charge jump
        self.jumping = False  # To track if the player is in the middle of a jump
        self.on_ground = False  # To track if the player is on the ground
        self.gravity = 1  # Gravity force
        self.max_charge = 25  # Max charge for jump
        self.jump_force = 0  # Actual force applied after charging
        self.orientation = 1  # Facing right, -1 is left
        self.charging = False  # Pressing space or not
        self.original_height = 40  # Store original height

        # Load the player image
        self.image = pygame.image.load(image_path_right)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))  # Scale to the rect size

    def draw(self, screen):
        # Draw the player image
        screen.blit(self.image, (self.x, self.y))

    def handle_input(self, keys, image_path_right, image_path_left):
        # Jump mechanic: Charge the jump while holding space, release to jump
        if keys[pygame.K_SPACE] and self.on_ground:
            if self.charge < self.max_charge:
                self.charge += 1  # Increase charge while space is held
                self.height -= 1  # Reduce height while charging
                self.image = pygame.image.load(image_path_right)
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
                self.y += 1
            self.charging = True
        elif not keys[pygame.K_SPACE] and self.charge > 0:
            self.charging = False
            self.y -= self.charge
            # Release space to jump
            self.height = self.original_height  # Reset height back to normal when jumping
            if self.orientation == 1:
                self.vx = 5  # Arbitrary horizontal velocity value
                self.image = pygame.image.load(image_path_right)
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
            if self.orientation == -1:
                self.vx = -5
                self.image = pygame.image.load(image_path_left)
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
            if self.orientation == 0:
                self.image = pygame.image.load(image_path_right)
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
            self.jump_force = -self.charge  # The higher the charge, the stronger the jump
            self.vy = self.jump_force  # Set vertical velocity to jump force
            self.jumping = True  # Now the player is in the air
            self.on_ground = False  # Player is not on the ground anymore
            self.charge = 0  # Reset the charge
        if keys[pygame.K_l]:
            self.y -= 100

        # movement (only allow left/right movement on the ground)
        if self.on_ground:
            self.vx = 0
            self.orientation = 0
            if keys[pygame.K_LEFT]:
                self.orientation = -1  # Facing left
                self.image = pygame.image.load(image_path_left)
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
            elif keys[pygame.K_RIGHT]:
                self.orientation = 1  # Facing right
                self.image = pygame.image.load(image_path_right)
                self.image = pygame.transform.scale(self.image, (self.width, self.height))  # Scale to the rect size

        # Ensure player doesn't move off the screen horizontally
        if self.x < 0:
            self.x = 0
        if self.x + self.width > screen.get_width():
            self.x = screen.get_width() - self.width

    def update(self):
        # Apply gravity when the player is in the air
        if not self.on_ground:
            self.vy += self.gravity

        # Move the player vertically & horizontally
        self.y += self.vy
        self.x += self.vx

        # Check for collision with the ground (assuming ground is at a fixed y position)
        if self.y + self.height >= screen.get_height():
            self.y = screen.get_height() - self.height
            self.vy = 0  # Stop vertical movement
            self.on_ground = True  # The player has landed
            self.jumping = False  # Reset jumping state

        # Horizontal boundary checks (if needed)
        if self.x < 0:  # Hits left of screen
            self.x = 0
            self.orientation = 1  # Facing right now
            self.vx = -self.vx  # Bouncing
        if self.x + self.width > screen.get_width():  # Hits right of screen
            self.x = screen.get_width() - self.width
            self.vx = -self.vx  # Bouncing
            self.orientation = -1  # Facing left now


class Platform(pygame.Rect): #platform class
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, 'dark green', self)  # Draw the platform as a green rectangle
        pygame.draw.rect(screen, 'black', pygame.Rect(self.x, self.y, 5, self.height))
        pygame.draw.rect(screen, 'black', pygame.Rect(self.x+self.width - 5, self.y, 5, self.height))


class Ice_Platform(Platform): #platform with no friction
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
    def draw(self, screen):
        pygame.draw.rect(screen, 'white', self)  # Draw the platform as a green rectangle

class Sand_Platform(Platform): #platform with no friction
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
    def draw(self, screen):
        pygame.draw.rect(screen, 'tan', self)  # Draw the platform as a green rectangle

class Reward(pygame.Rect):
    def __init__(self, x, y, width, height, image_path):
        super().__init__(x, y, width, height)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width,height))
    def draw(self, screen):
        # Draw the player image
        screen.blit(self.image, (self.x, self.y))


# Define different screens with platforms
screens = [ # in order from bottom to top
    [Sand_Platform(400,300,100,50),Sand_Platform(600,400,100,80), Ice_Platform(0,600,150,20), Platform(0,710, 800,40),  Platform(650,600,200,20), Platform(650,600,20,150), Platform(300, 500, 200, 20), Platform(100, 240, 200, 20), Platform(100, 80, 200, 20), Ice_Platform(300,80,100,20),Ice_Platform(500,80,100,20), Platform(600,80,50,20)], #level one platforms
    [Platform(300, 650, 200, 20), Platform(150, 550, 300, 20), Platform(500, 300, 100, 20), Ice_Platform(600, 300, 100, 20), Sand_Platform(550,100,125,20), Platform(50, 180, 40, 20), Sand_Platform(90, 180, 120, 20),Platform(210, 180, 40, 20)], # level two platforms
    [Sand_Platform(550,650,125,20), Platform(100,700,60,20), Platform(400,600,60,20), Platform(500,550,60,20),Platform(400,500,60,20),Sand_Platform(500,450,60,20),Sand_Platform(600,400,60,20), Platform(740,300,60,20),Platform(439,100,100,20)]# Add more screens with different platform layouts
]
easter_egg_screens = [
    Ice_Platform(400, 300, 100, 50), Ice_Platform(600, 400, 100, 80), Ice_Platform(0, 600, 150, 20),
    Ice_Platform(0, 710, 800, 40), Ice_Platform(650, 600, 200, 20) , Ice_Platform(300, 500, 200, 20),
    Ice_Platform(100, 240, 200, 20), Ice_Platform(100, 80, 200, 20), Ice_Platform(300, 80, 100, 20),
    Ice_Platform(500, 80, 100, 20), Ice_Platform(600, 80, 50, 20), Ice_Platform(0,0,800,20)
]

current_screen = 0
generated_screen = 2

def rect_intersect_buffer(rect1, rect2, buffer_x=0, buffer_y=0, corner_buffer=0):
    rect1_inflated = pygame.Rect(
        rect1.left - corner_buffer,
        rect1.top - corner_buffer,
        rect1.width + 2 * corner_buffer,
        rect1.height + 2 * corner_buffer
    )
    # Step 2: Check if the inflated rectangle intersects rect2 just within the corner range
    if rect1_inflated.colliderect(rect2):
        return True  # No intersection at all
    # Step 3: Create rectangles for horizontal and vertical buffers
    # Expand rect1 only vertically (keeping width the same)
    rect1_vertical_expanded = pygame.Rect(
        rect1.left,  # Same left position
        rect1.top - buffer_y,  # Expand upwards
        rect1.width,  # Keep width the same
        rect1.height + 2 * buffer_y  # Expand downwards
    )
    # Expand rect1 only horizontally (keeping height the same)
    rect1_horizontal_expanded = pygame.Rect(
        rect1.left - buffer_x,  # Expand left
        rect1.top,  # Same top position
        rect1.width + 2 * buffer_x,  # Expand right
        rect1.height  # Keep height the same
    )
    # Step 4: Check for intersection with the vertical expanded rectangle
    if rect1_vertical_expanded.colliderect(rect2):
        return True
    # Step 5: Check for intersection with the horizontal expanded rectangle
    if rect1_horizontal_expanded.colliderect(rect2):
        return True
    return False

# Function to load the next screen
def load_next_screen():
    global current_screen
    current_screen+= 1
    player.y = SCREEN_HEIGHT - player.height - 1  # Move player to bottom of new screen, 100px overlap

# Function to load the previous screen (optional)
def load_previous_screen():
    global current_screen
    current_screen -= 1
    if current_screen < 0:
        current_screen = 0  # Stay on the first screen
    player.y = 0  # Move player to top of the previous screen, 100px overlap
    player.on_ground = False


# function to randomly generate a new screen
def generate_next_screen():
    while True:
        global generated_screen
        random_integer = random.randint(3, 9)
        newScreen = []
        i = 0
        while i < random_integer:
            width = random.randint(60, 300)
            newScreen.append(Platform(random.randint(10, 790 - width), random.randint(60, 690), width, 20))
            for j in range(i):
                if rect_intersect_buffer(newScreen[j], newScreen[i], 30, 48, 10):
                    del newScreen[-1]
                    i -= 1
                    break
            i += 1
        sorts_platform = (sorted(screens[-1], key=lambda plat: plat.top, reverse=True))[-1]
        elevated_platform = Platform(sorts_platform.left, sorts_platform.top + 750, sorts_platform.width,
                                     sorts_platform.height)
        new_list = [elevated_platform]
        new_list.extend(newScreen)
        if is_screen_traversable(new_list):
            screens.append(newScreen)
            break


def is_screen_traversable(
        platforms):  # make last indŻx the one that you are expected to end upon!! (if you have time, will still 99% work otherwise)
    # Sort platforms from lowest to highest by their vertical position
    sort_platforms = sorted(platforms, key=lambda plat: plat.top, reverse=True)
    # Define a recursive function to try and reach the top
    if sort_platforms[-1].top > 100:
        return False

    def can_reach_top(index, sorted_platforms):
        # Base case: If at the highest platform, check if it's within 20 pixels of the top of the screen
        if index == len(sorted_platforms) - 1:
            return True

        # Recursive step: Check if the current platform can reach the next one
        for next_index in range(index + 1, len(sorted_platforms)):
            # Check if the current platform can reach the next platform
            if can_jump_between_platforms(sorted_platforms[index], sorted_platforms[next_index], sorted_platforms):
                if can_reach_top(next_index, sort_platforms):
                    return True
        return False

    # Start recursion from the bottom-most platform
    return can_reach_top(0, sort_platforms)


def can_jump_between_platforms(start_plat, end_plat,
                               platforms):  # DEFINE JUMP_DISTANCE, and JUMP_HEIGHT, and testing only goes up blocks
    # Calculate horizontal and vertical distances & check if jump is even physically possible
    dxL = end_plat.left - start_plat.left
    dxR = end_plat.right - start_plat.right
    dy = start_plat.top - end_plat.top
    left = False
    right = False
    if (abs(dxL) < 205 - 5 or dy < 210 - 3):
        if (dxL > 0):  # left side of the end plat is to the right of left side start plat
            left = True
        if (dxR < 0):  # right side of the end plat is to the left of right side start plat
            right = True
        if not (left or right):
            return False
    else:
        return False
    if left:
        start_x = start_plat.left + 4
        end_x = start_plat.right + 36

        for x in range(start_x, end_x + 5, 5):  # also do the end_x
            if x > end_x:
                x = end_x

            for initial_vy in range(1, 21):  # Testing different initial vertical velocities
                pos_x = x
                pos_y = start_plat.top

                # Simulate the trajectory until it reaches or falls below the end platform level
                while True:
                    # Update position based on initial velocities and gravity
                    pos_x += 5  # Horizontal step per loop iteration
                    pos_y -= initial_vy
                    initial_vy -= 1
                    # Check if the trajectory has peaked and begun descending
                    if initial_vy < 1:
                        # Begin checking for landings only after the trajectory starts going down
                        if end_plat.top <= pos_y <= end_plat.bottom:
                            if end_plat.left + 3 < pos_x < end_plat.right + 37:
                                return True
                            else:
                                break
                        elif pos_y > end_plat.bottom:
                            break
                    # check for any extra collisions
                    collides = False
                    for platform in platforms:
                        if platform.colliderect(pygame.Rect(pos_x - 40, pos_y - 40, 40, 40)):
                            collides = True
                            break
                    if collides:
                        break
    if right:
        start_x = start_plat.right - 4
        end_x = start_plat.left - 36

        for x in range(start_x, end_x - 5, -5):
            if x < end_x:
                x = end_x

            for initial_vy in range(1, 21):  # Testing different initial vertical velocities
                pos_x = x
                pos_y = start_plat.top

                # Simulate the trajectory until it reaches or falls below the end platform level
                while True:
                    # Update position based on initial velocities and gravity
                    pos_x -= 5  # Horizontal step per loop iteration
                    pos_y -= initial_vy
                    initial_vy -= 1
                    # Check if the trajectory has peaked and begun descending
                    if initial_vy < 1:
                        # Begin checking for landings only after the trajectory starts going down
                        if end_plat.top <= pos_y <= end_plat.bottom:
                            if end_plat.left - 37 < pos_x < end_plat.right - 3:
                                return True
                            else:
                                break
                        elif pos_y > end_plat.bottom:
                            break
                    # check for any extra collisions
                    collides = False
                    for platform in platforms:
                        if platform.colliderect(pygame.Rect(pos_x, pos_y - 40, 40, 40)):
                            collides = True
                            break
                    if collides:
                        break
    return False

#loading easter egg screens
def load_easter_egg_screen():
    global current_screen
    current_screen = "easter_egg"
    player.x, player.y = 650, 650   # Place player on the ice platform

def normal_screen():
    global current_screen
    current_screen = 0
    player.x, player.y = 50, 650   # Place player on the ice platform

#making player
player = Player(screen.get_width()/2 - 50, screen.get_height() - 100, "Doodleguy.png", "Doodleguyleft.png")


while True:
    # Process player inputs.
    keys = pygame.key.get_pressed()  # Get the state of all keys
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    # Handle player input for jump charging and release
    player.handle_input(keys, "Doodleguy.png","Doodleguyleft.png")  # Process jump charge and release based on space bar


    # Do logical updates here.

    player.update()  # Update player position first

    # Check if player is in the bottom left corner of the first screen
    if current_screen == 0 and player.x <= 50 and player.y >= SCREEN_HEIGHT - 100:
        load_easter_egg_screen()
    if current_screen == "easter_egg" and player.x >= 700 and player.y >= SCREEN_HEIGHT - 100:
        normal_screen()

    #If within two of a new screen, generate a new screen
    if current_screen != "easter_egg" and current_screen + 2 > generated_screen:
        generated_screen = current_screen + 2
        generate_next_screen()

    # Platform collisions
    for platform in screens[current_screen] if current_screen != "easter_egg" else easter_egg_screens:
        # Horizontal collision (sides)
        if player.vx > 0:  # Moving right
            if (platform.left < player.right < platform.left + 10 and player.left < platform.right and
                    player.bottom > platform.top and player.top < platform.bottom):
                player.right = platform.left  # Place player to the left side of the platform
                player.orientation = -1
                player.vx = -player.vx  # Bounce to the left

        if player.vx < 0:  # Moving left
            if (platform.right - 10 < player.left < platform.right and player.right > platform.left and
                    player.bottom > platform.top and player.top < platform.bottom):
                player.left = platform.right  # Place player to the right side of the platform
                player.orientation = 1
                player.vx = -player.vx  # Bounce to the right

        # Vertical collision (top and bottom)
        if player.colliderect(platform):
            if player.vy < 0:  # Moving up (hitting the bottom of the platform)
                if player.top < platform.bottom and player.bottom > platform.bottom:  # Ensure player is hitting the bottom
                    player.top = platform.bottom  # Place player at the bottom of the platform
                    player.vy = 0  # Stop vertical movement (no bounce in this case)

            elif player.vy > 0:  # Falling down (landing on the top of the platform)
                if player.bottom > platform.top and player.top < platform.top:  # Ensure player is landing on top
                    if type(platform).__name__ == "Ice_Platform":
                        player.bottom = platform.top  # Land on top of the platform
                        player.vy = 0  # Stop vertical movement
                        if player.vx < 0:
                            player.on_ground = False
                            player.vx += 0.2
                        if player.vx > 0:
                            player.on_ground = False
                            player.vx -= 0.2
                        if -0.2 <= player.vx <= 0.2:
                            player.vx = 0
                            player.on_ground = True
                    elif type(platform).__name__ == "Sand_Platform":
                        player.vy = 1
                        player.on_ground = True
                    elif type(platform).__name__ == "Platform":
                        player.bottom = platform.top  # Land on top of the platform
                        player.vy = 0  # Stop vertical movement
                        player.on_ground = True
                elif player.bottom < platform.bottom:
                    if type(platform).__name__ == "Sand_Platform":
                        player.vy = 1
                        player.on_ground = False

    # Screen transition when player goes above the top of the screen (overlap)
    if current_screen != "easter_egg" and player.top < 0 and current_screen < 2:
        load_next_screen()

    # Screen transition when player falls below the bottom of the screen (overlap)
    if current_screen != "easter_egg" and player.bottom >= SCREEN_HEIGHT:
        load_previous_screen()

    #platform collisions
    #for platform in screens[current_screen]:





    # Screen transition when player goes above the top of the screen (overlap)
    if player.top < 0:
        load_next_screen()

    # Screen transition when player falls below the bottom of the screen (overlap)
    if player.bottom >= SCREEN_HEIGHT:  # Allow for 100-pixel overlap when transitioning
        load_previous_screen()

        # Draw the background if current_screen is 0
    if current_screen == 0:
        screen.blit(background_image, (0, 0))
        pygame.draw.rect(screen, 'brown', pygame.Rect(0,650,50,60))
        pygame.draw.circle(screen, 'gold', (30,680), 5)
    elif current_screen == 1:
        screen.blit(background_image_2, (0,0))
    elif current_screen == 2:
        screen.blit(background_image_3, (0, 0))
    elif current_screen == "easter_egg":
        screen.blit(easter_egg_background, (0,0))
        pygame.draw.rect(screen, 'brown', pygame.Rect(750, 650, 50, 60))
        pygame.draw.circle(screen, 'gold', (770, 680), 5)
        # making award
        award = Reward(200,40,40,40, "easter_egg_reward.tiff")
        award.draw(screen)
        if player.colliderect(award):
            current_screen = 1
            player.x = 600
            player.y = 200
    elif current_screen.is_integer() and current_screen > 2:
        screen.blit(background_image_4, (0, 0))


    # Render the graphics here.

    player.draw(screen)


    # Draw platforms for the current screen
    # for platform in screens[current_screen]:
    #     platform.draw(screen)
    for platform in screens[current_screen] if current_screen != "easter_egg" else easter_egg_screens:
        platform.draw(screen)



    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)         # wait until next frame (at 60 FPS)
