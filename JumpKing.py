import pygame
import random

pygame.init()

screen = pygame.display.set_mode((800,750))

clock = pygame.time.Clock()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()


# class Player(pygame.Rect): #player class
#     def __init__(self, x, y):
#         super().__init__(x, y, 40, 40)  # Arbitrary values for player size
#         self.vy = 0  # Vertical velocity
#         self.vx = 0 #horizontal velocity
#         self.charge = 0  # charge jump
#         self.jumping = False  # To track if the player is in the middle of a jump
#         self.on_ground = False  # To track if the player is on the ground
#         self.gravity = 1  # Gravity force
#         self.max_charge = 25  # Max charge for jump
#         self.jump_force = 0  # Actual force applied after charging
#         self.orientation = 1 # facing right, -1 is left
#         self.charging = False #pressing space or not
#         self.original_height = 40  # Store original height
#
#     def draw(self, screen):
#         # Drawing the player
#         pygame.draw.rect(screen, 'black', self, 0)  # Fill
#         pygame.draw.rect(screen, 'white', self, 1)  # Outline
#
#
#     def handle_input(self, keys):
#         # Jump mechanic: Charge the jump while holding space, release to jump
#         if keys[pygame.K_SPACE] and self.on_ground:
#             if self.charge < self.max_charge:
#                 self.charge += 1  # Increase charge while space is held
#                 self.height -= 1  # Reduce height while charging
#                 self.y += 1
#             self.charging = True
#         elif not keys[pygame.K_SPACE] and self.charge > 0:
#             self.charging = False
#             self.y -= self.charge
#             # Release space to jump
#             self.height = self.original_height  # Reset height back to normal when jumping
#             if self.orientation == 1:
#                 self.vx = 5 #arbitrary horizontal velocity value
#             if self.orientation == -1:
#                 self.vx = -5
#             self.jump_force = -self.charge  # The higher the charge, the stronger the jump
#             self.vy = self.jump_force  # Set vertical velocity to jump force
#             self.jumping = True  # Now the player is in the air
#             self.on_ground = False  # Player is not on the ground anymore
#             self.charge = 0  # Reset the charge
#
#
#         # Horizontal movement (only allow left/right movement on the ground)
#         if self.on_ground:
#             self.vx = 0
#             self.orientation = 0
#             if keys[pygame.K_LEFT]:
#                 self.orientation = -1 #facing left
#             elif keys[pygame.K_RIGHT]:
#                 self.orientation = 1 #facing right
#
#         # Ensure player doesn't move off the screen horizontally
#         if self.x < 0:
#             self.x = 0
#         if self.x + self.width > screen.get_width():
#             self.x = screen.get_width() - self.width
#
#
#     def update(self):
#
#         # Apply gravity when the player is in the air
#         if not self.on_ground:
#             self.vy += self.gravity
#
#         # Move the player vertically & horizontally
#         self.y += self.vy
#         self.x += self.vx
#
#         # TODO: Check for collision with the ground (assuming ground is at a fixed y position)
#         if self.y + self.height >= screen.get_height():
#             self.y = screen.get_height() - self.height
#             self.vy = 0  # Stop vertical movement
#             self.on_ground = True  # The player has landed
#             self.jumping = False  # Reset jumping state
#
#         # Horizontal boundary checks (if needed)
#         if self.x < 0: #hits left of screen
#             self.x = 0
#             self.orientation = 1 #facing right now
#             self.vx = -self.vx #bouncing
#         if self.x + self.width > screen.get_width(): #hits right of screen
#             self.x = screen.get_width() - self.width
#             self.vx = -self.vx #bouncing
#             self.orientation = -1 #facing left now

class Player(pygame.Rect):  # player class
    def __init__(self, x, y, image_path, image_path_left):
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
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))  # Scale to the rect size

    def draw(self, screen):
        # Draw the player image
        screen.blit(self.image, (self.x, self.y))

    def handle_input(self, keys, image_path, image_path_left):
        # Jump mechanic: Charge the jump while holding space, release to jump
        if keys[pygame.K_SPACE] and self.on_ground:
            if self.charge < self.max_charge:
                self.charge += 1  # Increase charge while space is held
                self.height -= 1  # Reduce height while charging
                self.y += 1
            self.charging = True
        elif not keys[pygame.K_SPACE] and self.charge > 0:
            self.charging = False
            self.y -= self.charge
            # Release space to jump
            self.height = self.original_height  # Reset height back to normal when jumping
            if self.orientation == 1:
                self.vx = 5  # Arbitrary horizontal velocity value
            if self.orientation == -1:
                self.vx = -5
            self.jump_force = -self.charge  # The higher the charge, the stronger the jump
            self.vy = self.jump_force  # Set vertical velocity to jump force
            self.jumping = True  # Now the player is in the air
            self.on_ground = False  # Player is not on the ground anymore
            self.charge = 0  # Reset the charge

        # Horizontal movement (only allow left/right movement on the ground)
        if self.on_ground:
            self.vx = 0
            self.orientation = 0
            if keys[pygame.K_LEFT]:
                self.orientation = -1  # Facing left
                self.image = pygame.image.load(image_path_left)
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
            elif keys[pygame.K_RIGHT]:
                self.orientation = 1  # Facing right
                self.image = pygame.image.load(image_path)
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



# Define different screens with platforms
screens = [ # in order from bottom to top
    [Sand_Platform(400,300,100,50),Sand_Platform(600,400,100,80), Ice_Platform(0,600,150,20), Platform(0,710, 800,40),  Platform(650,600,200,20), Platform(650,600,20,150), Platform(300, 500, 200, 20), Platform(100, 240, 200, 20), Platform(100, 80, 200, 20), Ice_Platform(300,80,100,20),Ice_Platform(500,80,100,20), Platform(600,80,50,20)], #level one platforms
    [Platform(300, 650, 200, 20), Platform(150, 550, 300, 20), Platform(500, 300, 100, 20), Ice_Platform(600, 300, 100, 20), Sand_Platform(550,100,125,20), Platform(50, 180, 40, 20), Sand_Platform(90, 180, 120, 20),Platform(210, 180, 40, 20)], # level two platforms
    [Sand_Platform(550,650,125,20), Platform(100,700,60,20), Platform(400,600,60,20), Platform(500,550,60,20),Platform(400,500,60,20),Sand_Platform(500,450,60,20),Sand_Platform(600,400,60,20), Platform(740,300,60,20),Platform(400,120,100,20)]# Add more screens with different platform layouts
]

current_screen = 0

# Function to load the next screen
def load_next_screen():
    global current_screen
    if current_screen < 2:
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

    #platform collisions
    for platform in screens[current_screen]:
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
                        player.on_ground = False
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
    if player.top < 0 and current_screen < 2:
        load_next_screen()

    # Screen transition when player falls below the bottom of the screen (overlap)
    if player.bottom >= SCREEN_HEIGHT:  # Allow for 100-pixel overlap when transitioning
        load_previous_screen()


    screen.fill('light blue')  # Fill the display with a solid color

    # Render the graphics here.

    player.draw(screen)


    # Draw platforms for the current screen
    for platform in screens[current_screen]:
        platform.draw(screen)



    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)         # wait until next frame (at 60 FPS)
