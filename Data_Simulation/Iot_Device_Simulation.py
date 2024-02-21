import time
import json
from faker import Faker
from datetime import timedelta
from azure.iot.device import IoTHubDeviceClient, Message

# Replace with your Azure IoT Hub connection string
CONNECTION_STRING = "HostName=Project-iot-simulator.azure-devices.net;DeviceId=Device_Simuletor;SharedAccessKey=+fRWPLdkD4FBtWjxET1EXv223LikA2iLCAIoTMWOFPY="

# Replace with the name of your IoT device
DEVICE_ID = "Device_Simuletor"

def generate_fake_data():
    fake = Faker()

    # Generate random but consistent user_id and device_id
    user_id = f"u_{fake.random_int(1, 1000)}"
    device_id = f"d_{fake.random_int(1, 1000)}"
    first_name = fake.first_name()
    last_name = fake.last_name()
       

    # Generate fake data fields
    data = {
    "user_id": user_id,
    "user_name": f"{first_name} {last_name}",
    "device_id": device_id,
    "device_source": fake.random_element(["instagram", "facebook", "maps", "Chrome", 'WhatsApp', 'TikTok', 'Tinder', 'GoogleMaps']),
    "latitude": fake.pyfloat(left_digits=2, right_digits=6, positive=True),  # Adjust as needed
    "longitude": fake.pyfloat(left_digits=3, right_digits=6, positive=True),  # Adjust as needed
    "entry_time": fake.date_time_this_decade().strftime("%y-%m-%d %H:%M:%S"),
    "exit_time": (fake.date_time_this_decade() + timedelta(minutes=fake.random_int(15, 40))).strftime("%y-%m-%d %H:%M:%S"),
    "store_type": fake.random_element(["Coffee_shop", "Restaurant", "Electronics", "Shopping mall", "Cinema_theater", "Auditorium", "Game_zone",'Saloon','Wellness_center']),
    "bill_amount": fake.random_int(10, 500),  # Adjust as needed
    "payment_mode": fake.random_element(["Credit Card", "Debit Card", "Cash", "Mobile Payment"]),
    "review_to_store": fake.pyfloat(left_digits=1, right_digits=1, positive=True, max_value=5.0),  # Adjust as needed
}

    return json.dumps(data)

def send_data_to_iot_hub(device_client, data):
    message = Message(data)
    device_client.send_message(message)
    print(f"Sent message: {data}")

def main():
    try:
        # Create IoT Hub device client
        device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

        # Connect the device client
        device_client.connect()
        #current_seconds = 0
        while True:
            for _ in range(5):
                # Generate fake data
                fake_data = generate_fake_data()

                # Send fake data to IoT Hub
                send_data_to_iot_hub(device_client, fake_data)

                # Sleep for a specified interval (e.g., 1 second)
                time.sleep(1)
                #current_seconds += 1
            # Sleep for a specified interval between customers (e.g., 10 seconds)
            #time.sleep(24 * 60 * 60)
            #current_seconds += 24 * 60 * 60
    except KeyboardInterrupt:
        print("IoT Hub sender stopped by user")
    except Exception as ex:
        print(f"Error: {ex}")
    finally:
        # Disconnect the device client
        if device_client:
            device_client.disconnect()

if __name__ == "__main__":
    main()
