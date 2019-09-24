from time import sleep
import datetime
import sys, getopt, os
sys.path.append('/usr/lib/python3.5/dist-packages') # temporary hack to import the piJuice module
from pijuice import PiJuice
from balena import Balena
from twilio.rest import Client

# Start the SDK
balena = Balena()
balena.auth.login_with_token(os.environ['BALENA_API_KEY'])

# Wait for device I2C device to start
while not os.path.exists('/dev/i2c-1'):
    print ("Waiting to identify PiJuice")
    time.sleep(0.1)

# Initiate PiJuice
pijuice = PiJuice(1,0x14)

# Get all parameters and return as a dictionary
def get_battery_paremeters(pijuice):

    juice = {}

    charge = pijuice.status.GetChargeLevel()
    juice['charge'] = charge['data'] if charge['error'] == 'NO_ERROR' else charge['error']

    # Temperature [C]
    temperature =  pijuice.status.GetBatteryTemperature()
    juice['temperature'] = temperature['data'] if temperature['error'] == 'NO_ERROR' else temperature['error']

    # Battery voltage  [V]
    vbat = pijuice.status.GetBatteryVoltage()
    juice['vbat'] = vbat['data']/1000 if vbat['error'] == 'NO_ERROR' else vbat['error']

    # Barrery current [A]
    ibat = pijuice.status.GetBatteryCurrent()
    juice['ibat'] = ibat['data']/1000 if ibat['error'] == 'NO_ERROR' else ibat['error']

    # I/O coltage [V]
    vio =  pijuice.status.GetIoVoltage()
    juice['vio'] = vio['data']/1000 if vio['error'] == 'NO_ERROR' else vio['error']

    # I/O current [A]
    iio = pijuice.status.GetIoCurrent()
    juice['iio'] = iio['data']/1000 if iio['error'] == 'NO_ERROR' else iio['error']

    # Get power input (if power connected to the PiJuice board)
    status = pijuice.status.GetStatus()
    juice['power_input'] = status['data']['powerInput'] if status['error'] == 'NO_ERROR' else status['error']

    # Get power input (if power connected to the Raspberry Pi board)
    status = pijuice.status.GetStatus()
    juice['power_input_board'] = status['data']['powerInput5vIo'] if status['error'] == 'NO_ERROR' else status['error']

    return juice

def update_tag(tag, variable):
    # update device tags
    balena.models.tag.device.set(os.environ['BALENA_DEVICE_UUID'], str(tag), str(variable))

def send_sms(to_number, from_number, message, client):
    msg = client.messages.create(to=twilio_number, from_=twilio_from_number,body=message)
    print(msg.sid)

# Change start tag
start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
update_tag("START_TIME", start_time)

# ======================[ TWILIO CODE ]================================
# The idea here is to send user one message every hour in case a device
if( os.environ.get('TWILIO_SID') != None and os.environ.get('TWILIO_TOKEN') != None and os.environ.get('TWILIO_NUMBER') != None and os.environ.get('TWILIO_FROM_NUMBER') != None):
    twilio_sid = os.environ['TWILIO_SID']
    twilio_token = os.environ['TWILIO_TOKEN']
    twilio_number = os.environ['TWILIO_NUMBER']
    twilio_from_number = os.environ['TWILIO_FROM_NUMBER']

    # Initiate twilio client
    client = Client(twilio_sid, twilio_token)
    twillio_active = True
    twillio_last_message = datetime.datetime.now()
# =====================================================================

# Initial variables
i = 0

while True:

    #Read battery data
    battery_data = get_battery_paremeters(pijuice)
    # Uncomment the line to display battery status on long
    # print(battery_data)

    # Case power is disconnedted, send twilio text message if twilio alarm is set to true
    if (os.environ.get('TWILIO_ALARM') != None):
        if (os.environ['TWILIO_ALARM'].lower() == "true" and battery_data['power_input'] == "NOT_PRESENT" and battery_data['power_input_board'] == "NOT_PRESENT"):
            # check if last message was over one hour from the last message
            time_difference = (datetime.datetime.now() - twillio_last_message ).total_seconds() / 3600
            if(time_difference >= 1):
                send_sms(twilio_number, twilio_from_number,"Your device just lost power...", client)
                twillio_last_message = datetime.datetime.now()

    # Change tags every minute
    if(i%12==0):
        # Update tags
        for key, value in battery_data.items():
            update_tag(key, value)

    i = i + 1
    sleep(5)
