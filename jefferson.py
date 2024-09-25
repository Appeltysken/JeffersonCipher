import pygame
import random
import string

pygame.mixer.quit()
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Шифр Джефферсона")

BACKGROUND_COLOR = (240, 248, 255)  # AliceBlue
DISK_COLOR = (176, 196, 222)  # LightSteelBlue
TEXT_COLOR = (25, 25, 112)  # MidnightBlue
HIGHLIGHT_COLOR = (119, 136, 153)  # LightSlateGray
LINE_COLOR = (70, 130, 180)  # SteelBlue
LINE_ALPHA = 150  # Прозрачность линии
FONT = pygame.font.SysFont('Courier', 36)

class JeffersonCipher:
    def __init__(self, disk_count=7):
        self.disk_count = disk_count
        self.disks = [self.generate_disk() for _ in range(disk_count)]
        self.current_positions = [0] * disk_count
        self.selected_disk = 0
        self.tab_pressed = False
        self.dragging_disk = None
        self.disk_order = list(range(disk_count))
        self.encrypted_message = ""
        self.encrypted_order = ""

    @staticmethod
    def generate_disk():
        return ''.join(random.sample(string.ascii_uppercase, len(string.ascii_uppercase)))

    def get_disk_letter(self, disk_index, offset):
        pos = (self.current_positions[disk_index] + offset) % len(string.ascii_uppercase)
        return self.disks[disk_index][pos]

    def move(self, direction, all_disks=False):
        if all_disks:
            self.current_positions = [(pos + direction) % len(string.ascii_uppercase) for pos in self.current_positions]
        else:
            self.current_positions[self.disk_order[self.selected_disk]] = (self.current_positions[self.disk_order[self.selected_disk]] + direction) % len(string.ascii_uppercase)

    def change_disk_selection(self, delta):
        self.selected_disk = (self.selected_disk + delta) % self.disk_count

    def start_drag(self, mouse_x):
        disk_width = WIDTH // self.disk_count - 30
        for i, disk_index in enumerate(self.disk_order):
            if 50 + i * (disk_width + 20) <= mouse_x <= 50 + i * (disk_width + 20) + disk_width:
                self.dragging_disk = disk_index
                break

    def stop_drag(self):
        self.dragging_disk = None

    def drag(self, mouse_x):
        if self.dragging_disk is not None:
            disk_width = WIDTH // self.disk_count - 30
            new_index = max(0, min((mouse_x - 50) // (disk_width + 20), self.disk_count - 1))
            old_index = self.disk_order.index(self.dragging_disk)

            if new_index != old_index:
                self.disk_order.insert(new_index, self.disk_order.pop(old_index))

    def encrypt(self):
        self.encrypted_message = ''.join(self.disks[self.disk_order[i]][self.current_positions[self.disk_order[i]]] for i in range(self.disk_count))
        self.encrypted_order = ', '.join(str(self.disk_order[i]) for i in range(self.disk_count))
        return self.encrypted_message, self.encrypted_order

def draw_window(cipher):
    WINDOW.fill(BACKGROUND_COLOR)

    for i in range(cipher.disk_count):
        disk_width = WIDTH // cipher.disk_count - 30
        x_pos = i * (disk_width + 20) + 50
        y_pos = HEIGHT // 2 - 100
        color = HIGHLIGHT_COLOR if i == cipher.selected_disk else DISK_COLOR

        if cipher.dragging_disk == cipher.disk_order[i]:
            color = (150, 150, 255)

        pygame.draw.rect(WINDOW, color, (x_pos, y_pos, disk_width, 200), border_radius=20)

        for j, offset in enumerate([-1, 0, 1]):
            letter = cipher.get_disk_letter(cipher.disk_order[i], offset)
            text = FONT.render(letter, True, TEXT_COLOR)
            WINDOW.blit(text, (x_pos + disk_width // 2 - text.get_width() // 2, y_pos + 20 + j * 70))

        disk_number_text = FONT.render(str(cipher.disk_order[i]), True, TEXT_COLOR)
        WINDOW.blit(disk_number_text, (x_pos + disk_width // 2 - disk_number_text.get_width() // 2, y_pos - 40))

        # Рисуем линию
        line_surface = pygame.Surface((disk_width - 20, 4), pygame.SRCALPHA)
        line_surface.fill((*LINE_COLOR, LINE_ALPHA))
        WINDOW.blit(line_surface, (x_pos + 10, y_pos + 90 + text.get_height() // 2))

    info_text = FONT.render(f"Зашифрованное сообщение: {cipher.encrypted_message}", True, TEXT_COLOR)
    order_text = FONT.render(f"Порядок дисков: {cipher.encrypted_order}", True, TEXT_COLOR)
    WINDOW.blit(info_text, (20, HEIGHT - 100))
    WINDOW.blit(order_text, (20, HEIGHT - 50))

    pygame.display.update()

def main():
    cipher = JeffersonCipher()
    running = True

    while running:
        draw_window(cipher)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    cipher.tab_pressed = True
                if event.key == pygame.K_UP:
                    cipher.move(-1, all_disks=cipher.tab_pressed)
                elif event.key == pygame.K_DOWN:
                    cipher.move(1, all_disks=cipher.tab_pressed)
                elif event.key == pygame.K_LEFT:
                    cipher.change_disk_selection(-1)
                elif event.key == pygame.K_RIGHT:
                    cipher.change_disk_selection(1)
                elif event.key == pygame.K_RETURN:
                    cipher.encrypt()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if HEIGHT // 2 - 100 <= mouse_y <= HEIGHT // 2 + 100:
                    cipher.start_drag(mouse_x)

            if event.type == pygame.MOUSEBUTTONUP:
                cipher.stop_drag()

            if event.type == pygame.MOUSEMOTION:
                if cipher.dragging_disk is not None:
                    cipher.drag(event.pos[0])

    pygame.quit()

if __name__ == "__main__":
    main()
