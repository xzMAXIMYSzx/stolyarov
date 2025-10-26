# 1. Создаем класс транспортного средства: Vehicle, марка - name и пробег - mileage.
class Vehicle:
    def __init__(self, name, mileage):
        self.name = name
        self.mileage = mileage
# 2. Функция определения типа ТС.
    def get_vehicle_type(self, wheels):
        if wheels == 2:
            return f"Это мотоцикл марки {self.name}."
        elif wheels == 3:
            return f"Это трицикл марки {self.name}."
        elif wheels == 4:
            return f"Это автомобиль марки {self.name}."
        else:
            return f"Я не знаю таких ТС марки {self.name}."
# 3. Функция, которая дает совет по приобретению ТС (по количеству пробега у ТС).
    def get_vehicle_advice(self):
        if self.mileage < 50000:
            return f"Неплохо {self.name} можно брать."
        elif 50001 <= self.mileage <= 100000:
            return f"{self.name} надо внимательно проверить."
        elif 100001 <= self.mileage <= 150000:
            return f"{self.name} надо провести полную диагностику."
        else:
            return f"{self.name} лучше не покупать."


# 4. Создаем экземпляры класса с разными атрибутами
vehicle1 = Vehicle("BMW", 25000)
vehicle2 = Vehicle("Audi", 75000)
vehicle3 = Vehicle("Harley-Davidson", 120000)
vehicle4 = Vehicle("Toyota", 180000)
vehicle5 = Vehicle("Урал", 30000)  # дополнительный экземпляр

# 5. Тестируем методы для всех экземпляров
print("=== Тестирование метода get_vehicle_type ===")
print(vehicle1.get_vehicle_type(4))  # автомобиль
print(vehicle2.get_vehicle_type(4))  # автомобиль
print(vehicle3.get_vehicle_type(2))  # мотоцикл
print(vehicle4.get_vehicle_type(4))  # автомобиль
print(vehicle5.get_vehicle_type(3))  # трицикл
print(vehicle1.get_vehicle_type(6))  # неизвестное ТС

print("\n=== Тестирование метода get_vehicle_advice ===")
print(vehicle1.get_vehicle_advice())  # неплохо
print(vehicle2.get_vehicle_advice())  # внимательно проверить
print(vehicle3.get_vehicle_advice())  # полная диагностика
print(vehicle4.get_vehicle_advice())  # лучше не покупать
print(vehicle5.get_vehicle_advice())  # неплохо