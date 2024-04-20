from socket import *
from datetime import datetime, timedelta


SIM_MODE = False
TEST_MODE = False


host = '192.168.11.2'
port = 12345
addr = (host, port)

if not SIM_MODE:
    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.connect(addr)


data_for_test = [
    'A010MP',
    'E888KX',
    'K404EK',
    'B001OP',
    'E555TB',
    # '',
    # '',
    # '',
]


def check_payment_required(response: str) -> bool:
    try:
        if response == 'car not found':
            return False
            
        time_parking_status = response.split(";")
        current_time_str, parking_time_str, payment_status = time_parking_status
        
        if payment_status == 'not paid':
            return True

        current_time = datetime.strptime(current_time_str, "%H:%M:%S")
        parking_time = datetime.strptime(parking_time_str, "%H:%M:%S")
        
        current_time = current_time.replace(year=2024, month=3, day=27)
        parking_time = parking_time.replace(year=2024, month=3, day=27)

        print(f"Cur time: {current_time}")
        print(f"Park time: {parking_time}")
        print(f"Payment status: {payment_status}")
        
        time_difference = current_time - parking_time
        
        if abs(time_difference) >= timedelta(minutes=15):
            print("More than 15 minutes")
            return True
        print("Less than 15 minutes")
        return False
    except Exception as e:
        print(f"Something went wrong in check_car_state func:\n{e}\n___")
        return False
    
    
def get_car_payment_status(car_plate_num: str, response_text: str = '') -> str:
    try:
        if not response_text:
            send_data = str.encode(car_plate_num)
            tcp_socket.send(send_data)
            response = tcp_socket.recv(1024)
            response_text = bytes.decode(response)
        print(f"Server response: {response_text}")
        payment_required = check_payment_required(response_text)
        print(f"_______")
        if payment_required:
            return 'not ticket'
        return 'ticket'

    except Exception as e:
        print(f"Something went wrong in check_car_payment func:\n{e}\n________")
        return 'not ticket'
    
    
if TEST_MODE:
    for num in data_for_test:
        if SIM_MODE:
            print(f"{num} res:", get_car_payment_status(num, response_text="10:15:30;14:45:20;paid"))
            print(f"{num} res:",get_car_payment_status(num, response_text="10:15:30;14:45:20;not paid"))
            print(f"{num} res:", get_car_payment_status(num, response_text="14:40:30;14:45:20;paid"))
            print(f"{num} res:", get_car_payment_status(num, response_text="14:40:30;14:45:20;not paid"))
        else:
            print(f"{num} res: {get_car_payment_status(num)}")