import asyncio
import logging
import os
import sys
from typing_extensions import TypedDict, Unpack

from kasa import Discover

logging.basicConfig(handlers=[logging.StreamHandler(sys.stdout)],
                    encoding='utf-8',
                    level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S')


class _MainKwargs(TypedDict):
    username: str
    password: str
    threshold: float
    load_host: str
    switch_host: str


async def main(**kwargs: Unpack[_MainKwargs]):
    """
    Main Function - Turns off the heater if the threshold is exceeded.
    """
    username = kwargs['username']
    password = kwargs['password']
    threshold = kwargs['threshold']

    load_host = await Discover.discover_single(host=kwargs['load_host'], username=username, password=password)
    switch_host = await Discover.discover_single(host=kwargs['switch_host'], username=username, password=password)

    await switch_host.update()
    switch_state = switch_host.state_information['State']
    switch_current = switch_host.state_information['Current']

    logging.info('Switch device powered on: %s, current is: %s A', switch_state, switch_current)

    await load_host.update()
    load_state = load_host.state_information['State']
    load_current = load_host.state_information['Current']

    logging.info('Load device powered on: %s, current is: %s A', load_state, load_current)

    if load_current > threshold:
        logging.info('Load device is drawing more than %s A. Turning off the switch device.', 
                     threshold)
        await switch_host.turn_off()
    elif not switch_state and load_current < threshold:
        logging.info('Load device is drawing less than %s A. Turning on the switch device.', 
                     threshold)
        await switch_host.turn_on()

    await load_host.disconnect()
    await switch_host.disconnect()


if __name__ == "__main__":
    asyncio.run(main(username=os.environ['KASA_USERNAME'], 
                     password=os.environ['KASA_PASSWORD'], 
                     threshold=float(os.environ['KASA_THRESHOLD']),
                     load_host=os.environ['KASA_LOAD'],
                     switch_host=os.environ['KASA_SWITCH']))