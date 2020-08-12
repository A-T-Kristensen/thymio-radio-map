# Automatic radio map construction for CSI-based fingerprinting with LTE

Fingerprint-based indoor localization methods require the construction of a radio map. This is a tool automating this tedious task, by having a robot follow a line, and stop every x cm to gather location-dependent characteristics (i.e. a fingerprint).

## Summary

Fingerprint-based indoor localization methods require the construction of a radio map. This is a tedious task which can be automated. The presented solution consists of a Software-Defined Radio (SDR) mounted on a wheeled-robot (Thymio II). The SDR is connected to a LTE tower. The robot follows a line, stopping every x cm to let the SDR gather characteristics (**Channel State Information** (CSI), **Received Signal Strength Indicator** (RSSI), **Reference Signal Receive Power** (RSRP), ...) from its communication with the LTE tower. Those characteristics are saved, along with the robot's location (estimated through dead-reckoning), and are ready to be used as fingerprints.

![](doc/img/thymio_running.gif)

---

## Requirements

- Thymio II
- USRP B200mini
- PC/SC reader with a SIM card

---

## How to install

-   Following instruction on how to install `srsLTE-modified` from [here](https://github.com/arthurgassner/srsLTE-modified)

> Make sure `SRSUE_FOLDERPATH` in `run.py` points to the correct location (of the `srsue` folder, from the `srsLTE-modified` installation)

-   Create conda environment and activate it:

`conda env create -f environment.yml -n thymio`

`conda activate thymio`

-   Install `dbus` and `gobject`:

`pip install dbus-python`

`pip install PyGObject`

> Somehow it does not work if it is in the `environment.yml`

-   Install **Aseba** from [here](http://wiki.thymio.org/en:linuxinstall)

---

## How to run

-   Connect by USB the Thymio II to the computer

-   Switch to the conda environment created in the above step

-   Open a shell and run `sudo asebamedulla "ser:name=Thymio-II"`

> The shell should display `Found Thymio-II on port /dev/ttyACM0` and then keep running.

-   Open another shell and run

```
sudo `which python` ./run.py
```

---

## How to handle the generated files 

Some python scripts were written to facilitate the data gathering step, i.e.:

-   `move_fingerprint.py`: - Move the files generated by `sudo srsue ue.conf` (i.e. `ce.txt`, `else.txt` and `info.txt`) into their own folders (`ce`, `else`, `info`) - Record the (x,y) coordinates where those files were gathered into a JSON file (i.e. `locations.json`)

-   `clean_fingerprints.py` - Clean the fingerprint files (i.e. `ce_0_raw.txt`, `else_0_raw.txt` and `info_0_raw.txt`) - Save the cleaned files, e.g.:
    * `ce_0_raw.txt` -> `ce_0.parquet`
    * `else_0_raw.txt` -> `else_0.pkl` 
    * `info_0_raw.txt` -> `info_0.pkl`

-   `plot_fingerprints.py` - Plot the amplitude and phase held in the cleaned `ce.txt` (e.g. `ce_0.parquet`) - Save the plot, e.g.: \* `ce_0.parquet` -> `ce_0.png`

---

## Misc

Tested with

-   Ubuntu 18.04
-   Aseba medulla 1.6.1