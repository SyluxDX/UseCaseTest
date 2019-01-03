""" Run use case on script """
import os
import json
import time
import argparse
import subprocess
import utils

# log/display results
def log_msg(level, msg):
    """ Log message to logger file """
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    level = (level+' '*5)[:5]
    msg = msg.replace('\r', '').replace('\n', '|')

    line = '[{}][{}]: {}\n'.format(now, level.upper(), msg)
    with open(CONFIG['reportFile'], 'a') as logfp:
        logfp.write(line)

def run_tests():
    """ Run use case tests """
    os.environ['WORKDIR'] = CONFIG['workdir']
    stdout = subprocess.DEVNULL
    if CONFIG['verbose']:
        stdout = None
    # cycle throught version
    total = 0
    valid = 0
    start = time.time()
    for version in utils.get_dirs(CONFIG['versionsFolder']):
        utils.copy_dir(os.path.join(CONFIG['versionsFolder'], version), CONFIG['workdir'], True)
        # cycle throught use case
        for usecase in utils.get_dirs(CONFIG['testsFolder']):
            print('UseCase test: {}'.format(usecase))
            log_msg('info', 'UseCase test: {}'.format(usecase))
            try:
                folder = os.path.join(CONFIG['testsFolder'], usecase)
                with open(os.path.join(folder, CONFIG['useConfig'])) as usefp:
                    jconfig = json.load(usefp)
                cmd = ['py', os.path.join(folder, jconfig['entrypoint'])]
                total += 1
                if jconfig['runType'] == 'single':
                    subprocess.run(cmd, stdout=stdout, stderr=subprocess.PIPE, check=True)
                else:
                    for step in range(jconfig['numRuns']):
                        print('\r   >Step {}/{}      '.format(step+1, jconfig['numRuns'])\
                            , end='', flush=True)
                        log_msg('info', 'Step {}/{}'.format(step+1, jconfig['numRuns']) )
                        subprocess.run(cmd, stdout=stdout, stderr=subprocess.PIPE, check=True)
                        if step+1 != jconfig['numRuns']:
                            time.sleep(jconfig['interval'])
            except subprocess.CalledProcessError as excp:
                print('Error msg:{}'\
                    .format(excp.stderr.decode().replace('\r', '').replace('\n', '|')))
                log_msg('error', excp.stderr.decode())
            else:
                valid += 1
                print('{}.....Passed'.format(usecase))
                log_msg('info', '{} Passed'.format(usecase))

    elapse = time.time()-start
    log_msg('info', 'Ran {} tests in {:.3f}a'.format(total, elapse))
    print('Ran {} tests in {:.3f}s'.format(total, elapse))
    return total-valid


if __name__ == "__main__":
    # load configurations
    with open('appconfig.json', 'r') as jfp:
        CONFIG = json.load(jfp)

    # comand arguments
    ARG_PARSER = argparse.ArgumentParser(description='Run UseCase tests')
    ARG_PARSER.add_argument('-v', '--verbose'\
        , help='Increase output Verbosity', action='store_true')
    # ARG_PARSER.add_argument('-q', '--quiet'\
    #     , help='Decrease output Verbosity', action='store_true')
    ARG_PARSER.add_argument('-p', '--path'\
        , help='Global script path')
    ARG_PARSER.add_argument('-w', '--workdir'\
        , help='Work directory, will be added to global path')
    ARG_PARSER.add_argument('-t', '--test'\
        , help='Use Case tests folder, will be added to global path')
    ARG_PARSER.add_argument('-vs', '--version'\
        , help='Scrips Versions folder, will be added to global path')
    ARG_PARSER.add_argument('-r', '--report'\
        , help='Result Report folder, will be added to global path')
    ARG_PARSER.add_argument('-u', '--useconfig'\
        , help='Use Case configuration name')

    ARGS = ARG_PARSER.parse_args()
    # update configs
    utils.overload_config(CONFIG, ARGS)
    # check folders existence
    utils.check_folders([CONFIG['workdir'], CONFIG['testsFolder']\
        , CONFIG['versionsFolder'], CONFIG['reportFolder']])
    run_tests()
