""" simple test """
import os
import subprocess

print('simple run')
CMD = ['py', os.path.join(os.environ['WORKDIR'], 'stuff.py')]
subprocess.call(CMD)
print()
