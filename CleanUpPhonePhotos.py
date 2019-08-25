#!/bin/python3

import os
import Settings

# Don't actually do anything
softRun = True

def getAllFilesInPath(path):
    fileList = []
    for root, dirs, files in os.walk(path):
        # Ignore hidden folders (lazy programming detected!)
        # Note that this can mean thumbnails build up forever if they're still running google photos
        if "/." in root:
            continue
        for file in files:
            # if file.endswith(renderedContentExtensions):
            filePath = os.path.join(root, file)
            fileList.append(filePath)
    return fileList

# From https://stackoverflow.com/questions/1392413/calculating-a-directorys-size-using-python
def getFolderSize(path='.'):
    total = 0
    for entry in os.scandir(path):
        if entry.is_file():
            total += entry.stat().st_size
        elif entry.is_dir():
            total += getFolderSize(entry.path)
    return total

def makeRelativePath(fullPath, sourceDirectory):
    if sourceDirectory not in fullPath:
        print("ERROR: Path '{}' cannot be made relative.\n"
              "Make sure '{}' is an absolute path"
              .format(fullPath, sourceDirectory))
        exit(1)
    return fullPath[len(sourceDirectory):]

def bytesToKiBString(byteCount):
     return "{:,}".format(int(byteCount / 1024))

def bytesToMiBString(byteCount):
     return "{:,}".format(int(byteCount / 1024 / 1024))

def CleanUpFolder(photosPath, archivePhotosPath, maxPhotosSize):
    print("Checking folder {} against {} for cleanup..."
          .format(photosPath, archivePhotosPath))
    
    # Is the folder too big?
    photosSize = getFolderSize(photosPath)
    print("Folder size = {} MiB".format(bytesToMiBString(photosSize)))
    if photosSize < maxPhotosSize:
        print("Folder within size. Nothing to do")
        return

    print("Going to try to free up {} MiB"
          .format(bytesToMiBString(photosSize - maxPhotosSize)))
    
    # Build file lists
    photosFiles = getAllFilesInPath(photosPath)
    archivePhotosFilesList = getAllFilesInPath(archivePhotosPath)
    archivePhotosFilesDict = {}
    # For faster lookups
    for archivePhoto in archivePhotosFilesList:
        archivePhotosFilesDict[makeRelativePath(archivePhoto, archivePhotosPath)] = None

    print("Found {} photos and {} archive photos"
          .format(len(photosFiles), len(archivePhotosFilesList)))

    # Sort photos by age (oldest = first)
    photosFiles.sort(key=os.path.getmtime)
    
    sizeLeftToFree = photosSize - maxPhotosSize
    totalFreed = 0
    totalDeletedFiles = 0
    # Are there any files we can delete?
    for photoFile in photosFiles:
        if makeRelativePath(photoFile, photosPath) in archivePhotosFilesDict:
            # It's already archived. Delete it!
            photoSize = os.stat(photoFile).st_size
            sizeLeftToFree -= photoSize
            totalFreed += photoSize
            totalDeletedFiles += 1

            print("Deleting {}".format(photoFile))
            if not softRun:
                os.remove(photoFile)
            
            if sizeLeftToFree > 0:
                print("Removed {} KiB, {} MiB to go..."
                      .format(bytesToKiBString(photoSize), bytesToMiBString(sizeLeftToFree)))
            # Finished deleting!
            else:
                print("Removed {} KiB"
                      .format(bytesToKiBString(photoSize)))
                break
        else:
            # While I could do the copying here, I wanted this script to be for cleanup only
            print("WARNING: {} was not found in {}. It will not eligible for deletion."
                  .format(photoFile, archivePhotosPath))
            
    print("Deleted {} files, reclaiming {} MiB"
          .format(totalDeletedFiles, bytesToMiBString(totalFreed)))

    if sizeLeftToFree > 0:
        print("FAILED to free {} MiB".format(bytesToMiBString(sizeLeftToFree)))

if __name__ == '__main__':
    for cleanSetting in Settings.settings:
        CleanUpFolder(cleanSetting["folder"],
                      cleanSetting["archive"],
                      cleanSetting["maxSizeGiB"] * 1024 * 1024 * 1024)
