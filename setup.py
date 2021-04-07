import os
import subprocess

path = os.path.abspath( os.getcwd() )
subprocess.call( ['cmd', '/c', path + '\init.vbs'] )