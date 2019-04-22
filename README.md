# kckr


## Hardware

## Raspberry Pi 3
## GrovePi+ Shield

## Sensors
- http://wiki.seeedstudio.com/Grove-Loudness_Sensor/
- http://wiki.seeedstudio.com/Grove-Temperature_and_Humidity_Sensor_Pro/
- http://wiki.seeedstudio.com/Grove-Digital_Light_Sensor/
- http://wiki.seeedstudio.com/Grove-PIR_Motion_Sensor/

https://forum.dexterindustries.com/t/sound-sensor-readings/763/2?u=shoban



# Links

http://www.moserware.com/2010/03/computing-your-skill.html
https://www.microsoft.com/en-us/research/uploads/prod/2018/03/trueskill2.pdf
https://marketplace.visualstudio.com/items?itemName=MicrosoftIoT.WindowsIoTCoreProjectTemplatesforVS15

https://www.dexterindustries.com/howto/auto-run-python-programs-on-the-raspberry-pi/

# Install

```shell
sudo chmod +x setup.sh
sudo ./setup
```

pitfall: check for \r\n instead of \n

sudo apt install raspberrypi-ui-mods

https://www.raspifun.de/viewtopic.php?t=4

https://www.dexterindustries.com/GrovePi/get-started-with-the-grovepi/setting-software/

# Setup

copy `config.template.ini` to `config.ini` and set the config values.

# Remote debugging

We don't want to copy the files over for each change we do. So we create a network share on our dev machine and mount it.
## Windows
- Create Winows User `raspberry`
- Add network share for repository
    - Advanced Sharing > Permissions > add `raspberry`
    - Security > Edit > add `raspberry`

## Raspberry
- make sure `sudo apt-get install cifs-utils` is installed
- `sudo mount -t cifs //<dev-machine-ip>/kckr /mnt -o user=raspberry,password=<password>`

## VS Code
- see: https://code.visualstudio.com/docs/python/debugging#_remote-debugging

Config in `launch.json`
```json
{
    "name": "Python Attach (Remote Debug Raspberry Pi)",
    "type": "python",
    "request": "attach",
    "pathMappings": [
        {
            "localRoot": "${workspaceFolder}",
            "remoteRoot": "/mnt"
        }
    ],
    "port": 1337,
    "host": "<raspberrypi ip>"
}
```

**Issue:** Can't set breakpoint :( https://github.com/Microsoft/ptvsd/issues/1059
`pydev debugger: warning: trying to add breakpoint to file that does not exist`
