import random
import string

class JeffersonCil:
    
    def __init__(self):
        self.disks = [self.generate_disk() for _ in range(36)]

    def generate_disk(self):
        return ''.join(random.sample(string.ascii_uppercase, len(string.ascii_uppercase)))

    def set_disks(self, disks):
        self.disks = disks

    def encrypt(self, text):
        text = text.upper().replace(' ', '')
        
        text = text.ljust((len(text) // 36 + 1) * 36, 'X')
        
        encrypted_text = []
        for i in range(0, len(text), 36):
            block = text[i:i+36]
            for j in range(36):
                encrypted_text.append(self.disks[j][string.ascii_uppercase.index(block[j])])
        
        return ''.join(encrypted_text)

    def decrypt(self, encrypted_text):
        
        decrypted_text = []
        for i in range(0, len(encrypted_text), 36):
            block = encrypted_text[i:i+36]
            for j in range(36):
                decrypted_text.append(string.ascii_uppercase[self.disks[j].index(block[j])])
        
        return ''.join(decrypted_text).rstrip('X')

def main():
    cipher = JeffersonCil()

    disks = [ ''.join(random.sample(string.ascii_uppercase, len(string.ascii_uppercase))) for _ in range(36) ]
    cipher.set_disks(disks)
    
    while True:
        print("\nВыберите опцию:")
        print("1. Зашифровать сообщение")
        print("2. Расшифровать сообщение")
        print("3. Выход")

        choice = input("Введите номер опции: ")

        if choice == '1':
            message = input(">> ")
            encrypted = cipher.encrypt(message)
            print(f"Зашифрованное сообщение: {encrypted}")
            
        elif choice == '2':
            encrypted_message = input(">> ")
            try:
                decrypted = cipher.decrypt(encrypted_message)
                print(f"Расшифрованное сообщение: {decrypted}")
            except ValueError as e:
                print(f"Ошибка: {e}")
                
        elif choice == '3':
            print("Выйти")
            break
        else:
            print("Something was going wrong")

if __name__ == "__main__":
    main()
