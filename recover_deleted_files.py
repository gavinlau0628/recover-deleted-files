#!/usr/bin/env python

import argparse
import subprocess
import re
import os

# declare typecode
TYPECODES = ['\-', 'r', 'd', 'b', 'l', 'p', 's', 'w', 'v']
DESCRIPTIONS = [
    'unknown type',
    'regular file',
    'deleted file',
    'block device',
    'symbolic link',
    'named FIFO',
    'shadow file',
    'whiteout file',
    'TSK virtual file',
]

# declare dictionary 
TYPEDICT = dict(zip((tt.strip('\\') for tt in TYPECODES),  DESCRIPTIONS))

# declare parser explaination
parser = argparse.ArgumentParser(
    description='Recover files from a disk image file',
)
parser.add_argument(
    'image', type=str, nargs=1, help='path to disk image or mount point (generally a ".dmg" file)',
)
parser.add_argument(
    '-o', '--output', type=str, nargs='?', dest='output', default='recovered',
    help=('recover files to this directory [default=./recovered_files/]'),
)
parser.add_argument(
     '-v', '--verbose', dest='verbose', action='store_true',
    default=False, help=('print progress message while recovering'),
)


# main recovering method
def recover(imgpath, outpath, verbose=False):

    # check if we can open the disk image
    try:
        with open(imgpath, 'r'):
            pass
    # if not, print out error
    except IOError:
        print('Unable to open %s. Check that the path is correct, and that you have read permission.' % imgpath)
        return

    # if the output directory exists, check that it's writeable
    if os.path.isdir(outpath):
        if not os.access(outpath, os.W_OK):
            print('Output directory %s is not writeable - check permissions' % outpath)
            return
    # otherwise create it for storing the recovered files
    else:
        try:
           os.makedirs(outpath)
           print("./recovred_files created")
        except IOError:
           print('Could not create output directory %s - please check permissions' % outpath)
           return

    # command array
    command = ['fls', '-i', 'raw', '-p', '-r', imgpath]

    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    if p.returncode:
        print('Command "%s" failed:\n%s' % (' '.join(command), err))
        return

    # declare paths and arrays to store for recovering 
    ft = ''.join(TYPECODES)
    regex = '([%s])/([%s])\s+\*\s+(\d+):\s+(.*)' % (ft, ft)
    success = {}
    failure = {}
    skipped = {}

    # find all these in the paths of the disk image
    for ftype, mtype, inode, relpath in re.findall(regex, out):

        recpath = os.path.join(outpath, relpath)
        recdir, recname = os.path.split(recpath)
        item = {relpath:[imgpath, relpath]}

        # Do not recover directories
        if os.path.isdir(recpath):
            continue

        # only recover deleted files
        elif (ftype in ('r', 'd')) and (mtype in ('r', 'd')):
            if not os.path.isdir(recdir):
                if os.path.exists(recdir):
                    os.remove(recdir)
                os.makedirs(recdir)
            command = ['icat', '-i', 'raw', '-r', imgpath, inode]
            with open(recpath, 'wb', 4096) as outfile:
                err = subprocess.call(command, stdout=outfile, bufsize=4096)
            if err:
                msg = '[FAILED]'
                failure.update(item)
            else:
                msg = '[RECOVERED]'
                success.update(item)
            if verbose:
                if ftype != mtype:
                    realloc_msg = (
                        '[WARNING: file name structure (%s) '
                        'does not match metadata (%s)]'
                        % (TYPEDICT[ftype], TYPEDICT[mtype]))
                else:
                    realloc_msg = ''
                print('%s %s:%s --> %s %s'
                       % (msg, imgpath, inode, recpath, realloc_msg))
        else:
            # skip the unknown/other file types
            if verbose:
                print('[SKIPPED] %s:%s [%s / %s]'
                       % (imgpath, inode, TYPEDICT[ftype], TYPEDICT[mtype]))
            skipped.update(item)

    # print out the file path (success/skipped/failed)
    print('-' * 50)
    nsuccesses = len(success)
    nfailures = len(failure)
    nskipped = len(skipped)
    print('%i files successfully recovered to %s'
          % (len(success), outpath))
    print('%i files skipped' % nskipped)
    print('%i files could not be successfully recovered' % nfailures)
    if nfailures:
        print('\n'.join([(' * ' + pth) for pth in failure.keys()]))
    print('-' * 50)

# main
if __name__ == '__main__':
    args = parser.parse_args()
    imgpath = args.image[0]
    outpath = "./recovered_files"
    recover(imgpath, outpath, verbose=args.verbose)