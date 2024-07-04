import subprocess  # Импортируем модуль subprocess для выполнения системных команд.
import os # Импортируем модуль os для работы с ОС.

def check_package_exists_apt(package_name):
    try:
        result = subprocess.run(['apt-cache', 'show', package_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # стандартный вывод и стандартный вывод ошибок команды будут перенаправлены в каналы, что позволяет получить их содержимое в переменной result
        return True
    # ловим исключения, которые могут возникнуть, если команда zypper завершится с ненулевым статусом возврата    
    except subprocess.CalledProcessError:
        return False

def check_package_exists_yum(package_name):
    try:
        result = subprocess.run(['yum', 'info', package_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True 
    except subprocess.CalledProcessError:
        return False

def check_package_exists_zypper(package_name):
    try:
        result = subprocess.run(['zypper', 'info', package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8').lower()
        if 'not found' in output or 'no package found' in output:
            return False
        return True
    except subprocess.CalledProcessError:
        return False

def detect_package_manager():
    if os.path.exists('/usr/bin/apt-cache'):
        return 'apt'
    elif os.path.exists('/usr/bin/yum'):
        return 'yum'
    elif os.path.exists('/usr/bin/zypper'):
        return 'zypper'
    else:
        raise EnvironmentError('Не удалось найти поддерживаемый менеджер пакетов (apt, yum или zypper).')

def main():
    package_manager = detect_package_manager()

    if package_manager == 'apt':
        check_package_exists = check_package_exists_apt
    elif package_manager == 'yum':
        check_package_exists = check_package_exists_yum
    elif package_manager == 'zypper':
        check_package_exists = check_package_exists_zypper

    with open('packagelist.txt', 'r') as file:
        packages = file.readlines()
    
    with open('result.txt', 'w') as result_file:
        for package in packages:
            package = package.strip() # Убираем лишние пробелы и символы новой строки.
            if check_package_exists(package):
                result_file.write(package + '\n') # Записываем имя пакета в файл, если он найден.

if __name__ == "__main__":
    main()