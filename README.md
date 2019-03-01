## Balena Pi Juice

![](https://raw.githubusercontent.com/balena-io-playground/balena-pijuice/master/img/pijuice.jpg)

This is an example project demonstrating how to use a [PiJuice](https://uk.pi-supply.com/products/pijuice-standard) UPS board with a Rasperry Pi. 
The main idea of the UPS board is to keep your device up and running in case of an outage. If you would like to know more information about the board, click [here](https://uk.pi-supply.com/products/pijuice-standard).

![](https://raw.githubusercontent.com/balena-io-playground/balena-pijuice/master/img/dashboard.png)

### Features:
* Logs the state of the battery every 5 seconds.
* Create and update a list of tags that are easily visible from the dashboard. The tags are updated every minute.
* If configured, you can also receive one warning text message every hour from a third party service called twilio.


### Configuring Twilio
Go to [twilio](https://twilio.com) and create an account, and do a text message setup. You will then need to add these variables to `Device Environment Variables`.

* `TWILIO_ALARM` = `True`
* `TWILIO_FROM_NUMBER` = `+1...`
* `TWILIO_NUMBER` = `+1...`
* `TWILIO_SID` = `...`
* `TWILIO_TOKEN` = `...`

If you set `TWILIO_ALARM` to `True`, it means that once your device is disconnected from power, you will start receiving messages every hour until de power runs out.