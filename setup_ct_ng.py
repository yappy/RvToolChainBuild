import os
import shutil
import subprocess

CTNG_WORK_DIR = 'ct-ng'
CTNG_VERSION = '1.24.0'
CTNG_NAME = 'crosstool-ng-{}'.format(CTNG_VERSION)
CTNG_TAR = '{}.tar.bz2'.format(CTNG_NAME)
CTNG_URL = 'http://crosstool-ng.org/download/crosstool-ng/{}'.format(CTNG_TAR)
CTNG_SHA512 = '{}.sha512'.format(CTNG_TAR)

os.makedirs(CTNG_WORK_DIR, exist_ok=True)
os.chdir(CTNG_WORK_DIR)

print("=== Download ===")
if not os.path.exists(CTNG_TAR):
	subprocess.run(['wget', CTNG_URL], check=True)

print()
print("=== Check sha512 ===")
shutil.copyfile('../{}'.format(CTNG_SHA512), CTNG_SHA512)
subprocess.run(['sha512sum', '-c', CTNG_SHA512])

print()
print("=== Extract ===")
if not os.path.exists(CTNG_NAME):
	subprocess.run(['tar', 'xf', CTNG_TAR])

print()
print('=== ./configure --enable-local ===')
os.chdir(CTNG_NAME)
subprocess.run(['./configure', '--enable-local'], check=True)

ncpu = len(os.sched_getaffinity(0))
print('=== make -j{} ==='.format(ncpu))
subprocess.run(['make', '-j{}'.format(ncpu)], check=True)

print()
print('=== Show help ===')
subprocess.run(['./ct-ng'], check=True)

print()
print('=== !!! OK !!! ===')
