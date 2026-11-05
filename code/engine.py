import pygame
import json
from pathlib import Path
from main import game
from battle import BattleSystem

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Monster Mons")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Load Events
with (Path(__file__).parent / "data" / "events.json").open(encoding="utf-8") as file:
    events_data = json.load(file)

class GameEngine:
    def __init__(self):
        self.state = "DIALOGUE" # States: DIALOGUE, STARTER_SELECT, OVERWORLD, BATTLE
        self.running = True
        self.current_event = events_data["town_1_intro"]
        self.dialogue_index = 0
        self.active_battle = None
        self.starters = ["Pica", "Grassy", "Flamer"]
        

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if self.state == "DIALOGUE":
                    if event.key == pygame.K_SPACE:
                        self.advance_dialogue()

                    elif self.state == "STARTER_SELECT":
                        choice = None
                        if event.key == pygame.K_1: choice = 0
                        elif event.key == pygame.K_2: choice = 1
                        elif event.key == pygame.K_3: choice = 2

                        if choice is not None:
                            starter_name = self.starters[choice]
                            starter_mon = game.get_mon_info(starter_name, level=5, hp=20)
                            
                            # Add a default move based on valid moves
                            valid_moves = starter_mon.valid_moves()
                            if valid_moves:
                                starter_mon.learn_move(valid_moves[0]["name"])
                                
                            game.perform_action(game.add_mon, starter_mon)
                            self.state = "OVERWORLD"

    def advance_dialogue(self):
        self.dialogue_index += 1
        if self.dialogue_index >= len(self.current_event):
            if len(game.player["mons"]) == 0:
                self.state = "STARTER_SELECT"
            else:
                self.state = "OVERWORLD"
            self.dialogue_index = 0

    def draw(self):
        screen.fill((30, 30, 30)) # Dark gray background

        if self.state == "DIALOGUE":
            # Draw Text Box
            pygame.draw.rect(screen, (255, 255, 255), (50, 400, 700, 150), border_radius=10)
            text_surface = font.render(self.current_event[self.dialogue_index], True, (0, 0, 0))
            screen.blit(text_surface, (70, 420))
            
            hint_surface = font.render("Press SPACE to continue", True, (150, 150, 150))
            screen.blit(hint_surface, (70, 500))

        elif self.state == "STARTER_SELECT":
            title = font.render("Press 1, 2, or 3 to choose your starter:", True, (255, 255, 255))
            screen.blit(title, (100, 100))
            
            for i, mon_name in enumerate(self.starters):
                # Draw 3 choice boxes
                box_y = 200 + (i * 100)
                pygame.draw.rect(screen, (100, 100, 200), (100, box_y, 600, 60), border_radius=5)
                choice_text = font.render(f"[{i + 1}] {mon_name}", True, (255, 255, 255))
                screen.blit(choice_text, (120, box_y + 15))

        elif self.state == "BATTLE" and self.active_battle:
            # Draw Battle UI
            player_hp = f"Player HP: {self.active_battle.player_mon['hp']}"
            enemy_hp = f"Enemy HP: {self.active_battle.enemy_mon['hp']}"
            
            screen.blit(font.render(enemy_hp, True, (255, 100, 100)), (500, 100))
            screen.blit(font.render(player_hp, True, (100, 255, 100)), (100, 300))
            
            if self.active_battle.turn_log:
                log_text = font.render(self.active_battle.turn_log[-1], True, (255, 255, 255))
                screen.blit(log_text, (100, 500))

        elif self.state == "OVERWORLD":
            screen.blit(font.render("Overworld (Press SPACE to simulate battle)", True, (255, 255, 255)), (100, 300))
            # Next step: Add grid movement drawing here

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            clock.tick(60)
        
        # Save game on exit
        game.save_change()
        pygame.quit()

if __name__ == "__main__":
    engine = GameEngine()
    engine.run()