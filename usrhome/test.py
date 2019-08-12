#sample code runnig space
import datetime

def generate_order_id():
    return str(datetime.date.today().year) + str(
        datetime.date.today().month).zfill(2)+ str(
        datetime.date.today().day).zfill(2) + str(
        datetime.datetime.now().strftime('%H%M%S%f'))


