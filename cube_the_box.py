#This is the easy script to convert cuboid map which is not cube to cube one
#idea behind it was to use tomography maps as a models in Relion which required cube maps
#Scripts detects which axis is different and expands the map from both sides with mean volume value.
#written and tested by Dawid Zyla


import easygui
import mrcfile
import numpy as np

file = easygui.fileopenbox()

#file = 'your mrc volume file'

xy, xz, yz = 0,0,0

def nothing(x):
    pass

with mrcfile.open(file) as volume:

        mrcs_file = volume.data
        z, x, y = volume.data.shape

        #chceck for the dimensions of the map
        if x != y or x != z or y != z:
            print('Different sizes of axes detected!  ('+str((x,y,z))+')')
            print()

            if x == y:
                xy = 1
            elif x == z:
                xz = 1
            elif y == z:
                yz = 1

            if (xy, xz, yz) == (1, 0, 0):
                print('z axis different!')
                print('z axis different!')
                missing_volume = np.zeros((int(abs(x - z) / 2), x, y))
                print('missing volume size is:' + str((int(abs(x - z) / 2), x, y)))
                missing_volume.fill(np.mean(mrcs_file))
                new_volume = np.concatenate(([missing_volume, mrcs_file]), axis=0)
                new_volume = np.concatenate(([new_volume, missing_volume]), axis=0)
                new_volume = np.array(new_volume, dtype=np.float32)
            elif (xy, xz, yz) == (0, 1, 0):
                print('y axis different!')
                print('y axis different!')
                missing_volume = np.zeros((z, x, int(abs(x - y) / 2)))
                print('missing volume size is:' + str((z, x, int(abs(x - y)))))
                missing_volume.fill(np.mean(mrcs_file))
                new_volume = np.concatenate(([missing_volume, mrcs_file]), axis=2)
                new_volume = np.concatenate(([new_volume, missing_volume]), axis=2)
                new_volume = np.array(new_volume, dtype=np.float32)
            elif (xy, xz, yz) == (0, 0, 1):
                print('x axis different!')
                missing_volume = np.zeros((z, int(abs(x-y)/2), y))
                print('missing volume size is:'+str((z, int(abs(x-y)), y)))
                missing_volume.fill(np.mean(mrcs_file))
                new_volume = np.concatenate(([missing_volume, mrcs_file]), axis=1)
                new_volume = np.concatenate(([new_volume, missing_volume]), axis=1)
                new_volume = np.array(new_volume, dtype=np.float32)


            with mrcfile.new('Cubed'+file) as mrc:
                mrc.set_data(new_volume)
                print('Your map was converted to cube!')
        else:
            print('Your MRC map is a cube. Nothing to do here.')