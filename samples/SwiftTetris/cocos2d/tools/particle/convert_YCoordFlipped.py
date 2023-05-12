#!/usr/bin/python
#ConvertYCoordFlipped.py

import plistlib
import os.path
import argparse
import glob
import shutil

#keys in dictionary
metaDataKey = 'metaData'
yCoordFlippedConvertedKey = 'yCoordFlippedConverted'
yCoordFlippedKey = 'yCoordFlipped'

#check if the particle file has been converted
def checkFlippedConvertFlag(plistDict):
    if not plistDict.has_key(metaDataKey):
        return False
    metaDict = plistDict.get(metaDataKey)
    return (
        False
        if (not metaDict.has_key(yCoordFlippedConvertedKey))
        else metaDict.get(yCoordFlippedConvertedKey) is 1
    )

#write flag to indicate to file has been converted
def writeFlippedConvertFlag(plistDict):
    metaDict = {}
    metaDict.update(yCoordFlippedConverted = 1)
    plistDict.update(metaData = metaDict)

#process file
def processConvertFile(filename):
    #print a line to seperate files
    print ('')
    if (not os.path.isfile(filename)):
        print(f'{filename} dose not exist!')
        return
    print(f'Begin process particle file: {filename}')
    fp = open(filename, 'r')
    pl = plistlib.readPlist(fp) 

    if (not pl.has_key(yCoordFlippedKey)):
        print(f'Skip plist file: {filename} for there is no key for yCoordFlipped,')
    elif checkFlippedConvertFlag(pl):
        print(f'Skip a converted file {filename}')

    else:
        backupFileName = f'{filename}.backup'
        print(f'Write backup file to {backupFileName}')
        shutil.copyfile(filename,backupFileName)
        print('converting...')
        pl[yCoordFlippedKey] = -pl[yCoordFlippedKey]
        writeFlippedConvertFlag(pl)
        print('converted...')
        print(f'Write new plist file to {filename}')
        plistlib.writePlist(pl,filename)

# -------------- entrance --------------
if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument("file", nargs = "+",help = "specify a file or a patten")
    #argparser.add_argument("-r", "--recursive",action = "store_true", help = "recursive folder or not")
    args = argparser.parse_args()

    for file in args.file:
        processConvertFile(file)
