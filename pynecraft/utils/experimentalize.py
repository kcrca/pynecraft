import shutil
import zipfile

import amulet_nbt
from amulet_nbt import ListTag, StringTag


def extract(version, dir_x):
    return
    j = f'/Applications/MultiMC.app/Data/libraries/com/mojang/minecraft/{version}/minecraft-{version}-client.jar'
    with zipfile.ZipFile(j) as jar:
        print(j)
        for f in list(filter(lambda x: x.startswith('data/minecraft/datapacks'), jar.namelist())):
            jar.extract(f, dir_x)

def main():
    version = '1.19.3'
    dir = f'/Users/kcrca/clarity/home/saves/Restworld_{version}'
    dir_x = dir + '+x'

    shutil.rmtree(dir_x, ignore_errors=True)
    shutil.copytree(dir, dir_x)

    nbt(dir, dir_x)
    extract(version, dir_x)


def nbt(dir, dir_x):
    top = amulet_nbt.load(dir + '/level.dat')
    data = top.compound.get('Data')
    packs = data.get_compound('DataPacks')
    enabled = packs.get_list('Enabled')
    disabled = packs.get_list('Disabled')
    for s in disabled:
        enabled.append(s)
    disabled.clear()
    enabled_features = ListTag((StringTag(f'minecraft:{x}') for x in ('vanilla', 'update_1_20')))
    data['enabled_features'] = enabled_features
    top.save_to(dir_x + '/level.dat')


if __name__ == '__main__':
    main()
