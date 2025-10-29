# Класс беспроводной мыши (WirelessMouse)
class WirelessMouse:
    def __init__(self, connection_type, dpi, battery_level=100):
        self.connection_type = connection_type  # Тип подключения
        self.dpi = dpi  # Чувствительность (DPI)
        self.battery_level = battery_level  # Уровень заряда батареи %
        self.is_on = True  # Состояние мышки (вкл/выкл)

    def move_cursor(self, direction, distance):
        """Перемещает курсор в указанном направлении"""
        if not self.is_on:
            print("Мышь выключена! Можете пользоваться.")
            return

        if self.battery_level <= 0:
            print("Батарея разряжена! Зарядите мышь.")
            return

        print(f"Перемещаю курсор {direction} на расстояние {distance} пикселей")
        self.battery_level -= 0.5  # Расход энергии на перемещение

    def scroll_content(self, direction, speed=1):
        """Прокручивает содержимое"""
        if not self.is_on:
            print("Мышь выключена! Можете пользоваться.")
            return

        if self.battery_level <= 0:
            print("Батарея разряжена! Зарядите мышь.")
            return

        scroll_direction = "вверх" if direction == "up" else "вниз"
        print(f"Прокрутка {scroll_direction} со скоростью {speed}")
        self.battery_level -= 0.3  # Расход энергии на прокрутку

    def save_energy(self):
        """Экономит энергию (режим энергосбережения)"""
        if self.battery_level < 20:
            self.is_on = False
            print("Режим энергосбережения активирован. Мышь переведена в спящий режим.")
        else:
            print(f"Уровень заряда: {self.battery_level}%. Энергосбережение не требуется.")

    def charge_battery(self, charge_amount):
        """Заряжает батарею"""
        self.battery_level = min(100, self.battery_level + charge_amount)
        self.is_on = True
        print(f"⚡ Зарядка... Текущий уровень: {self.battery_level}%")

    def power_on_off(self):
        """Включает/выключает мышь"""
        self.is_on = not self.is_on
        status = "включена" if self.is_on else "выключена"
        print(f"Мышь {status}")

    def get_status(self):
        """Показывает статус мыши"""
        status = "включена" if self.is_on else "выключена"
        return (f"   Статус мыши:\n"
                f"   Тип подключения: {self.connection_type}\n"
                f"   Чувствительность: {self.dpi} DPI\n"
                f"   Заряд батареи: {self.battery_level}%\n"
                f"   Состояние: {status}")


# Демонстрация работы класса
print("=== ТЕСТИРОВАНИЕ БЕСПРОВОДНОЙ МЫШИ ===\n")

# Создаем экземпляры мышек с разными параметрами
mouse1 = WirelessMouse("Bluetooth", 1600, 85)
mouse2 = WirelessMouse("RF 2.4 GHz", 2400, 15)
mouse3 = WirelessMouse("USB Receiver", 3200, 100)

# Тестируем методы
mouse = [mouse1, mouse2, mouse3]

for i, mouse in enumerate(mouse, 1):
    print(f"\n--- Мышь #{i} ---")
    print(mouse.get_status())

    # Тестируем основные функции
    mouse.move_cursor("вправо", 150)
    mouse.scroll_content("up", 2)

    # Проверяем энергосбережение
    mouse.save_energy()

    # Если батарея низкая - заряжаем
    if mouse.battery_level < 20:
        mouse.charge_battery(50)

    print(mouse.get_status())