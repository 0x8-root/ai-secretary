'''Главный файл запуска ai-secretary. Здесь иницируется запуск, а также собираются функции'''
from notifier import notify

def main():
    print("AI Secretary запущен...")
    notify("Тест","Привет!")

if __name__ == '__main__':
    main()