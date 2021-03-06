import os
import time

from move_fingerprint import move_fingerprint
from record_fingerprint import record_fingerprint
from thymio import Thymio

STARTING_TIMER = 1 # Timer [s] before starting, in case you need to exit the room
SRSUE_CONF_FILEPATH = '../srsLTE-modified/srsue/ue-digital-lab.conf'
CE_FILEPATH = 'ce.txt'
CE_FILESIZE = 1 # Filesize [MB] above which the recording is stopped
N_STEPS = 100 # Amount of RPs to gather
DISTANCE_TO_TRAVEL = 1 # [cm] distance between each RP
THYMIO_POSITIONS_FILENAME = 'thymio_positions'
DEST_FOLDERPATH = 'dev'

INITIAL_POSITION = [0,0]

def run():
    last_position = INITIAL_POSITION # (x,y) coordinates of the position where the Thymio last stopped

    # Inspect {THYMIO_POSITIONS_FILENAME}.txt to infer the Thymio's absolute position    
    thymio_positions_filepath = os.path.join(DEST_FOLDERPATH, f'{THYMIO_POSITIONS_FILENAME}.txt')    
    positions = []

    if os.path.isfile(thymio_positions_filepath):
        with open(thymio_positions_filepath, 'r') as fp:
            positions = [line.rstrip() for line in fp.readlines()]
        last_position = eval(positions[-1])
        print('Already {} fingerprints found in {}/ \n'.format(len(positions), DEST_FOLDERPATH))

    print('Gathering {} fingerprints over {}cm \n'.format(N_STEPS, DISTANCE_TO_TRAVEL * N_STEPS))
    print(f'Wait {STARTING_TIMER}s before starting... \n')
    time.sleep(STARTING_TIMER)

    for step in range(N_STEPS):
        print('Fingerprint #{} in [{:.2f}, {:.2f}]'.format(step + len(positions), last_position[0], last_position[1]))
        print('\t- Record fingerprint')
        record_fingerprint(SRSUE_CONF_FILEPATH, CE_FILEPATH, CE_FILESIZE)

        print('\t- Move fingerprint')
        move_fingerprint(x=last_position[0],
                         y=last_position[1], 
                         src_folderpath='./',
                         dest_folderpath=DEST_FOLDERPATH,
                         verbose=False)

        print('\t- Move Thymio to ', end='')
        thymio = Thymio(initial_position=last_position, 
                        distance_to_travel=DISTANCE_TO_TRAVEL, 
                        positions_filename=THYMIO_POSITIONS_FILENAME,
                        dest_folderpath=DEST_FOLDERPATH)
        thymio.run()
        last_position = fetch_last_position(filepath=os.path.join(DEST_FOLDERPATH, f'{THYMIO_POSITIONS_FILENAME}.txt'))
        print('[{:.2f}, {:.2f}]'.format(last_position[0], last_position[1]))
        print('')


def fetch_last_position(filepath):
    """Inspect {filepath}.txt to infer the Thymio's last absolute position, i.e. the last one appended    

    Args:
        filepath (str): Name of the file holding the positions where the Thymio stopped

    Returns:
        [List of floats]: (x,y) absolute coordinates of the Thymio's last stop
    """

    positions = []
    with open(filepath, 'r') as fp:
        positions = [line.rstrip() for line in fp.readlines()]
    last_position = eval(positions[-1])
    return last_position


if __name__ == '__main__':
    run()
