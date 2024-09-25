import pygame
import random
import string

pygame.mixer.quit()
pygame.init()

WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jefferson Cipher")

BACKGROUND_COLOR = (240, 248, 255)  # AliceBlue
DISK_COLOR = (176, 196, 222)  # LightSteelBlue
TEXT_COLOR = (25, 25, 112)  # MidnightBlue
HIGHLIGHT_COLOR = (119, 136, 153)  # LightSlateGray
LINE_COLOR = (70, 130, 180)  # SteelBlue (линия в центре)
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
        self.offset_x = 0
        self.disk_order = list(range(disk_count))
        self.encrypted_message = ""
        self.encrypted_order = ""

    def generate_disk(self):
        return ''.join(random.sample(string.ascii_uppercase, len(string.ascii_uppercase)))

    def get_disk_letter(self, disk_index, offset):
        pos = (self.current_positions[disk_index] + offset) % len(string.ascii_uppercase)
        return self.disks[disk_index][pos]

    def move_up(self, all_disks=False):
        if all_disks:
            self.current_positions = [(pos - 1) % len(string.ascii_uppercase) for pos in self.current_positions]
        else:
            self.current_positions[self.disk_order[self.selected_disk]] = (self.current_positions[self.disk_order[self.selected_disk]] - 1) % len(string.ascii_uppercase)

    def move_down(self, all_disks=False):
        if all_disks:
            self.current_positions = [(pos + 1) % len(string.ascii_uppercase) for pos in self.current_positions]
        else:
            self.current_positions[self.disk_order[self.selected_disk]] = (self.current_positions[self.disk_order[self.selected_disk]] + 1) % len(string.ascii_uppercase)

    def move_left(self):
        self.selected_disk = (self.selected_disk - 1) % self.disk_count

    def move_right(self):
        self.selected_disk = (self.selected_disk + 1) % self.disk_count

    def start_drag(self, disk_index, mouse_x):
        disk_width = WIDTH // self.disk_count - 30
        for i, disk_index in enumerate(self.disk_order):
            x_pos = i * (disk_width + 20) + 50
            if x_pos <= mouse_x <= x_pos + disk_width:
                self.dragging_disk = disk_index
                self.offset_x = mouse_x - x_pos
                break

    def stop_drag(self):
        if self.dragging_disk is not None:
            self.dragging_disk = None

    def drag(self, mouse_x):
        if self.dragging_disk is not None:
            
            disk_width = WIDTH // self.disk_count - 30
            new_index = (mouse_x - 50) // (disk_width + 20)
            new_index = max(0, min(new_index, self.disk_count - 1))

            if new_index != self.disk_order.index(self.dragging_disk):
                old_index = self.disk_order.index(self.dragging_disk)

                self.disk_order.pop(old_index)
                self.disk_order.insert(new_index, self.dragging_disk)

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

        is_selected = i == cipher.selected_disk
        color = HIGHLIGHT_COLOR if is_selected else DISK_COLOR

        if cipher.dragging_disk == cipher.disk_order[i]:
            color = (150, 150, 255)

        pygame.draw.rect(WINDOW, color, (x_pos, y_pos, disk_width, 200), border_radius=20)

        letter_y_pos_up = y_pos + 20
        letter_y_pos_current = y_pos + 90
        letter_y_pos_down = y_pos + 160

        letter_up = cipher.get_disk_letter(cipher.disk_order[i], -1)
        text_up = FONT.render(letter_up, True, TEXT_COLOR)
        WINDOW.blit(text_up, (x_pos + disk_width // 2 - text_up.get_width() // 2, letter_y_pos_up))

        letter_current = cipher.get_disk_letter(cipher.disk_order[i], 0)
        text_current = FONT.render(letter_current, True, TEXT_COLOR)
        WINDOW.blit(text_current, (x_pos + disk_width // 2 - text_current.get_width() // 2, letter_y_pos_current))

        letter_down = cipher.get_disk_letter(cipher.disk_order[i], 1)
        text_down = FONT.render(letter_down, True, TEXT_COLOR)
        WINDOW.blit(text_down, (x_pos + disk_width // 2 - text_down.get_width() // 2, letter_y_pos_down))

        disk_number_text = FONT.render(str(cipher.disk_order[i]), True, TEXT_COLOR)
        WINDOW.blit(disk_number_text, (x_pos + disk_width // 2 - disk_number_text.get_width() // 2, y_pos - 40))

        line_y_pos = y_pos + 90 + text_current.get_height() // 2
        line_surface = pygame.Surface((disk_width - 20, 4), pygame.SRCALPHA)
        line_surface.fill((LINE_COLOR[0], LINE_COLOR[1], LINE_COLOR[2], LINE_ALPHA))
        WINDOW.blit(line_surface, (x_pos + 10, line_y_pos))

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
                    if cipher.tab_pressed:
                        cipher.move_up(all_disks=True)
                    else:
                        cipher.move_up()
                elif event.key == pygame.K_DOWN:
                    if cipher.tab_pressed:
                        cipher.move_down(all_disks=True)
                    else:
                        cipher.move_down()

                elif event.key == pygame.K_LEFT:
                    cipher.move_left()
                elif event.key == pygame.K_RIGHT:
                    cipher.move_right()

                elif event.key == pygame.K_RETURN:
                    cipher.encrypt()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for index in range(cipher.disk_count):
                    disk_width = WIDTH // cipher.disk_count - 30
                    x_pos = index * (disk_width + 20) + 50
                    y_pos = HEIGHT // 2 - 100
                    if x_pos <= mouse_x <= x_pos + disk_width and y_pos <= mouse_y <= y_pos + 200:
                        cipher.start_drag(index, mouse_x)

            if event.type == pygame.MOUSEBUTTONUP:
                cipher.stop_drag()

            if event.type == pygame.MOUSEMOTION:
                if cipher.dragging_disk is not None:
                    cipher.drag(event.pos[0])

    pygame.quit()

if __name__ == "__main__":
    main()
