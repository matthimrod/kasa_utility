# Kasa Utility

A utility that uses two Kasa Smart Plugs with current monitoring to monitor one device for usage and use it to trigger a different device to turn off.

My use case is to automatically turn off a space heater when my husband uses our treadmill so that the heater doesn't cause the circuit breaker to trip.

## Usage

Environment Variables:

* `KASA_USERNAME` - the username to use for authentication
* `KASA_PASSWORD` - the password to use for authentication
* `KASA_THRESHOLD` - the threshold in amps
* `KASA_LOAD` - the hostname or IP address of the smart device to monitor
* `KASA_SWITCH` - the hostname or IP address of the smart device to turn off

Crontab:

The script will check the devices and change states once and then exit. The intended use case is a crontab entry that runs the script every minute during the hours when treadmill useage is likey. (Otherwise, it can be run every minute perpetually.)

Example:

```crontab
 * 8-23 * * *   . /root/kasa_utility/.venv/bin/activate && KASA_USERNAME=user@mail.com KASA_PASSWORD=my_password KASA_THRESHOLD=2.0 KASA_LOAD=192.168.1.2 KASA_SWITCH=192.168.1.3 python /root/kasa_utility/kasa_utility.py
```

This will check every minute from 8:00 AM to 11:00 PM.
