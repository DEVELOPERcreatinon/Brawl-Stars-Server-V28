import time
import logging
from collections import defaultdict

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Параметры защиты
MAX_REQUESTS_PER_10_SECONDS = 20  # Лимит запросов за 10 секунд
MAX_REQUESTS_PER_MINUTE = 100  # Лимит запросов за минуту
BLOCK_DURATION = 600  # Время блокировки в секундах (10 минут)

# Логи и блокированные IP
request_log = defaultdict(list)
blocked_ips = {}

# База данных "плохих" IP (например, можно использовать API для пополнения списка)
known_bad_ips = {"192.168.1.50", "203.0.113.0"}  # Пример плохих IP

# Функция проверки IP
def check_ip(ip_address):
    current_time = time.time()

    # Если IP уже в "чёрном списке"
    if ip_address in known_bad_ips:
        logging.warning(f"Запрос от известного плохого IP: {ip_address}")
        return False

    # Если IP временно заблокирован
    if ip_address in blocked_ips:
        if current_time - blocked_ips[ip_address] > BLOCK_DURATION:
            del blocked_ips[ip_address]  # Разблокируем после истечения времени
        else:
            logging.warning(f"IP {ip_address} временно заблокирован.")
            return False

    # Удаление старых записей (больше 1 минуты и 10 секунд)
    request_log[ip_address] = [req_time for req_time in request_log[ip_address] if current_time - req_time < 60]

    # Добавляем новый запрос в лог
    request_log[ip_address].append(current_time)

    # Проверка запросов за последние 10 секунд
    recent_requests = [req_time for req_time in request_log[ip_address] if current_time - req_time < 10]
    
    if len(recent_requests) > MAX_REQUESTS_PER_10_SECONDS:
        logging.warning(f"IP {ip_address} превысил лимит запросов за 10 секунд. Блокируем.")
        blocked_ips[ip_address] = current_time
        return False

    # Проверка запросов за последнюю минуту
    if len(request_log[ip_address]) > MAX_REQUESTS_PER_MINUTE:
        logging.warning(f"IP {ip_address} превысил лимит запросов за минуту. Блокируем.")
        blocked_ips[ip_address] = current_time
        return False

    return True

# Функция обработки запроса
def handle_request(ip_address):
    if check_ip(ip_address):
        logging.info(f"Запрос от {ip_address} успешно обработан")
    else:
        logging.info(f"Запрос от {ip_address} отклонён")

# Мониторинг подозрительной активности
def monitor_suspicious_activity():
    logging.info("Мониторинг активности начат...")
    while True:
        # Можно интегрировать с реальной системой мониторинга сетевого трафика.
        time.sleep(10)  # Периодический мониторинг

ips_to_test = ["192.168.1.10", "192.168.1.50", "203.0.113.0", "192.168.1.10"] # Айпи для тестирования
for ip in ips_to_test:
    handle_request(ip)
    time.sleep(0.2)  # Симулируем небольшой промежуток времени между запросами