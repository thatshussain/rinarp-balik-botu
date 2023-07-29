import tkinter as tk
from threading import Thread
import cv2
import time
import random
from pynput.keyboard import Key, Controller
import pyautogui
import requests
import datetime
import uuid
import webbrowser
def get_username():
    import os
    if os.name == 'nt':
        return os.getlogin()
    else:
        import pwd
        return pwd.getpwuid(os.getuid()).pw_name
class FishingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DEVEYE SORMUSLAR")
        self.root.configure(bg="#1a1a1a")
        self.create_widgets()
        self.cap = None
        self.allowed_macs = self.get_allowed_macs_from_web()
        self.open_github_page()
        self.open_youtube_channel()
    def create_widgets(self):
        title_font = ("Helvetica", 24, "bold")
        label_font = ("Helvetica", 12)

        self.status_label = tk.Label(self.root, text="Kamera bağlantısı başarısız.", fg="red", bg="#1a1a1a", font=label_font)
        self.status_label.pack(pady=5)

        self.start_button = tk.Button(self.root, text="Balık Tutmayı Başlat", command=self.start_fishing, font=label_font)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(self.root, text="Balık Tutmayı Durdur", command=self.stop_fishing, state=tk.DISABLED, font=label_font)
        self.stop_button.pack(pady=5)

        self.fish_count_label = tk.Label(self.root, text="Yakalanan Balık Sayısı: 0", fg="green", bg="#1a1a1a", font=label_font)
        self.fish_count_label.pack(pady=5)

        self.fishing_status_label = tk.Label(self.root, text="", fg="black", bg="#1a1a1a", font=label_font)
        self.fishing_status_label.pack(pady=5)
    def start_fishing(self):
        authorized = self.is_valid_user()
        if authorized:
            self.status_label.config(text="Lisanslı kullanıcı giriş yaptı.", fg="green")
        else:
            self.log_access_attempt(authorized=False)
            self.status_label.config(text="MAC adresi izin verilmedi.", fg="red")
            return
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.fish_count = 0
        self.cap = cv2.VideoCapture(0)
        self.fishing_thread = Thread(target=self.fishing_loop)
        self.fishing_thread.start()
        self.log_access_attempt(authorized=True)
    def stop_fishing(self):
        self.status_label.config(text="Balık tutma durduruldu.", fg="red")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        if self.cap:
            self.cap.release()
            cv2.destroyAllWindows()
    def fishing_loop(self):
        messages = [
            "- developed by quecy -",
            "- https://github.com/thatsquecy -",
        ]
        random_messages_thread = Thread(target=self.print_random_messages, args=(messages,))
        random_messages_thread.start()
        keyboard = Controller()
        consecutive_green_frames = 0
        green_detection_threshold = 5
        fish_count = 0
        last_green_detected_time = time.time()
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Kamera bağlantısı başarısız.")
                break
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            green_lower = (40, 100, 100)
            green_upper = (80, 255, 255)
            mask = cv2.inRange(hsv, green_lower, green_upper)
            mask = cv2.GaussianBlur(mask, (5, 5), 0)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) > 0:
                consecutive_green_frames += 1
                last_green_detected_time = time.time()
                if consecutive_green_frames >= green_detection_threshold:
                    fish_count += 1
                    self.fish_count_label.config(text=f"Yakalanan Balık Sayısı: {fish_count}", fg="green")
                    self.fishing_status_label.config(text=f"Balık Yakalandı ({fish_count} adet).", fg="green")
                    keyboard.press('x')
                    keyboard.release('x')
                    consecutive_green_frames = 0
                    time.sleep(3)
                    self.fishing_status_label.config(text="Olta Tekrardan Atılıyor.", fg="green")
                    keyboard.press('x')
                    keyboard.release('x')
            else:
                consecutive_green_frames = 0
                current_time = time.time()
                if current_time - last_green_detected_time >= 40:
                    self.fishing_status_label.config(text="40 saniye boyunca balık algılanmadı.", fg="red")
                    keyboard.press('x')
                    keyboard.release('x')
                    last_green_detected_time = current_time
            cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
            cv2.imshow("YATTIM ALLAH KALDIR BENI | QUECY", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
            if fish_count >= 10:
                self.fishing_status_label.config(text="10 balık yakalandı! Balıklar Otomatik Olarak Aktarılıyor.", fg="blue")
                for _ in range(15):
                    self.click_at_coordinates(918, 440)
                    time.sleep(0.1)
                    self.click_at_coordinates(950, 573)
                    time.sleep(0.1)
                self.fishing_status_label.config(text="Bagaja aktarım döngüsü bitti.", fg="blue")
                fish_count = 0
        self.cap.release()
        cv2.destroyAllWindows()
    def print_random_messages(self, messages):
        while True:
            message = random.choice(messages)
            print(message)
            time.sleep(15)
    def is_valid_user(self):
        current_mac = self.get_mac_address()
        return current_mac in self.allowed_macs
    def get_allowed_macs_from_web(self):
        try:
            url = "https://thatsquecy.github.io/izin-verdigim-mac-adresleri/allowed_macs.json"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return data.get("allowed_macs", [])
            else:
                print(f"Web sitesine bağlanırken hata oluştu: {response.status_code}")
                return []
        except Exception as e:
            print(f"Web sitesine bağlanırken hata oluştu: {e}")
            return []
    def get_mac_address(self):
        mac = ':'.join(("%012X" % uuid.getnode())[i:i + 2] for i in range(0, 12, 2))
        return mac
    def click_at_coordinates(self, x, y):
        pyautogui.moveTo(x, y)
        pyautogui.click()
    def send_discord_message(self, message):
        discord_webhook_url = "lisansli_lisanssiz_giris_loglarinin_tutulacagi_webhook"
        data = {
            "content": message
        }
        requests.post(discord_webhook_url, json=data)
    def log_access_attempt(self, authorized):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        allowed_macs = ", ".join(self.allowed_macs)
        current_mac = self.get_mac_address()
        username = get_username()
        if authorized:
            message = f":white_check_mark: **Lisanslı Giriş**\n" \
                      f"`Tarih:` {current_time}\n" \
                      f"`Lisanslı Mac Adresleri:` {allowed_macs}\n" \
                      f"`Kullanıcı Adı:` {username}\n"
        else:
            message = f":x: **Lisanssız Giriş**\n" \
                      f"`Tarih:` {current_time}\n" \
                      f"`İzin Verilen Mac Adresleri:` {allowed_macs}\n" \
                      f"`İzinsiz Giriş Yapmaya Çalışan Mac Adresi:` {current_mac}\n" \
                      f"`Kullanıcı Adı:` {username}\n"
        self.send_discord_message(message)
    def open_github_page(self):
        webbrowser.open("https://github.com/thatsquecy")
    def open_youtube_channel(self):
        webbrowser.open("https://www.youtube.com/channel/UCGeuXunV2oZ9tS0s2y6esRw")
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x200")
    root.configure(bg="#1a1a1a")
    app = FishingApp(root)
    root.mainloop()
