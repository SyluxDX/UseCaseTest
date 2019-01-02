""" Run use case on script """
import os
import json
import time
import argparse
import subprocess
import utils

# log/display results
def run_tests():
    """ Run use case tests """
    os.environ['WORKDIR'] = CONFIG['workdir']
    stdout = None
    if CONFIG['quiet']:
        stdout = subprocess.DEVNULL
    # cycle throught version
    for version in utils.get_dirs(CONFIG['versionsFolder']):
        utils.copy_dir(os.path.join(CONFIG['versionsFolder'], version), CONFIG['workdir'], True)
        # cycle throught use case
        for usecase in utils.get_dirs(CONFIG['testsFolder']):
            print('UseCase test: {}'.format(usecase))
            folder = os.path.join(CONFIG['testsFolder'], usecase)
            with open(os.path.join(folder, CONFIG['useConfig'])) as usefp:
                jconfig = json.load(usefp)
            # test jconfig
            # print(json.dumps(jconfig, indent=1))
            cmd = ['py', os.path.join(folder, jconfig['entrypoint'])]
            if jconfig['runType'] == 'single':
                subprocess.call(cmd, stdout=stdout)
            else:
                for step in range(jconfig['numRuns']):
                    print('\r   >Step {}/{}      '.format(step+1, jconfig['numRuns'])\
                        , end='', flush=True)
                    subprocess.call(cmd, stdout=stdout)
                    if step+1 != jconfig['numRuns']:
                        time.sleep(jconfig['interval'])


if __name__ == "__main__":
    # load configurations
    with open('appconfig.json', 'r') as jfp:
        CONFIG = json.load(jfp)

    # comand arguments
    ARG_PARSER = argparse.ArgumentParser(description='Run UseCase tests')
    ARG_PARSER.add_argument('-q', '--quiet', help='Decrease output Verbosity', action='store_true')
    ARG_PARSER.add_argument('-p', '--path', help='Global script path')
    ARG_PARSER.add_argument('-w', '--workdir', help='Work directory, will be added to global path')
    ARG_PARSER.add_argument('-t', '--test'\
        , help='Use Case tests folder, will be added to global path')
    ARG_PARSER.add_argument('-v', '--version'\
        , help='Scrips Versions folder, will be added to global path')
    ARG_PARSER.add_argument('-r', '--report'\
        , help='Result Report folder, will be added to global path')
    ARG_PARSER.add_argument('-u', '--useconfig', help='Use Case configuration name')
    # ARG_PARSER.add_argument('-s', '--startscript', help='Use Case start script')

    ARGS = ARG_PARSER.parse_args()
    # update configs
    utils.overload_config(CONFIG, ARGS)
    run_tests()
