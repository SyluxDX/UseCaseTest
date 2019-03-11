""" Auxiliar Functons """
import os
import time
import shutil


def get_files(path):
    """ List files in a folder, designed by path """
    files = list()
    for (_, __, filenames) in os.walk(path):
        files.extend(filenames)
        return files

def get_dirs(path):
    """ List folder in a folder, designed by path """
    folders = list()
    for (_, dirnames, __) in os.walk(path):
        folders.extend(dirnames)
        return folders

def check_folders(folders):
    """ Check folder existence and create if necessary """
    for path in folders:
        if not os.path.exists(path):
            os.makedirs(path)

def overload_config(configs, args):
    """ Overloads configurations with arguments inputs, and join global path to all folders """

    configs['verbose'] = args.verbose
    configs['quiet'] = args.quiet
    configs['clearWorkdir'] = args.keep_workdir

    if args.path:
        configs['path'] = args.path

    if args.workdir:
        configs['workdir'] = os.path.join(configs['path'], args.workdir)
    else:
        configs['workdir'] = os.path.join(configs['path'], configs['workdir'])

    if args.test:
        configs['testsFolder'] = os.path.join(configs['path'], args.test)
    else:
        configs['testsFolder'] = os.path.join(configs['path'], configs['testsFolder'])

    if args.version:
        configs['versionsFolder'] = os.path.join(configs['path'], args.version)
    else:
        configs['versionsFolder'] = os.path.join(configs['path'], configs['versionsFolder'])

    if args.report:
        configs['reportFolder'] = os.path.join(configs['path'], args.report)
    else:
        configs['reportFolder'] = os.path.join(configs['path'], configs['reportFolder'])
    # add report name
    configs['reportFile'] = os.path.join(configs['reportFolder']\
        , '{}.log'.format(time.strftime("%Y-%m-%d_%H%M%S", time.gmtime())))

    if args.useconfig:
        configs['useConfig'] = args.useconfig

def copy_dir(src, dst, clear=False):
    """ Copy files in folder src to folder dst """
    if clear:
        shutil.rmtree(dst)
        os.makedirs(dst)
        # for filename in get_files(dst):
        #     os.remove(os.path.join(dst, filename))
    for filename in get_files(src):
        shutil.copy(os.path.join(src, filename), dst)
