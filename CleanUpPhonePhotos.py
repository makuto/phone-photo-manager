!/bin/python3

import os

photosPath = "/home/macoy/Camera S9 Test"
archivePhotosPath = "/home/macoy/Archive-Photos-Sync"

# One gibibyte max size
maxPhotosSize = 1024 * 1024 * 1024 * 1

def getAllFilesInPath(path):
    fileList = []
    for root, dirs, files in os.walk(path):
        for file in files:
            # if file.endswith(renderedContentExtensions):
            filePath = os.path.join(root, file)
            fileList.append(filePath)


def main():
    print("Checking Photos for cleanup...")
    
    # Is the folder too big?
    photosSize = os.path.getsize(photosPath)
    print("Photos folder size = {} GiB".format(photosSize / (1024 * 1024)))
    if photosSize < maxPhotosSize:
        print("Photos folder within size. Nothing to do")
        return
    
    # Build file lists
    photosFiles = getAllFilesInPath(photosPath)
    archivePhotosFiles = getAllFilesInPath(archivePhotosPath)

    print("Found {} photos and {} archive photos"
          .format(len(photosFiles), len(archivePhotosPath))
    # Sort photos by age
    # Are there any files we can delete?
    # Delete files

if __name__ == "__main__":
    main()
