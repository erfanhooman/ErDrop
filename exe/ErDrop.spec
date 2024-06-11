# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['../main.py'],
    pathex=[
        '/home/erfan/Desktop/Project/ErDrop',
        '/home/erfan/Desktop/Project/ErDrop/sender',
        '/home/erfan/Desktop/Project/ErDrop/sender/userInter_faces',
        '../receiver/downloadmanager/',
        '../receiver/startserver/',
        '../receiver/userInter_faces/',
        '../sender/choosefile/',
        '../sender/discovering_implementations/',
        '../sender/sending_file_implementations/',
    ],
    binaries=[],
    datas=[
        ('/home/erfan/Desktop/Project/ErDrop/Config.yaml', 'Config.yaml')
    ],
    hiddenimports=[
        'requests',
        'tqdm',
#       sender imports
        'sender.userInter_faces.GUIBase',
        'sender.userInter_faces.QtGUI',
        'sender.userInter_faces.TkinterGUI',

        'sender.sending_file_implementations.DefaultSendingFileImplementation',
        'sender.sending_file_implementations.SendingFIleBase',

        'sender.discovering_implementations.DefaultDiscoveringImplementation',
        'sender.discovering_implementations.DiscoverReceiverBase',

        'sender.choosefile.ChooseFIleBase',
        'sender.choosefile.TkinterFileChoose',

#        receiver imports
        'receiver.downloadmanager.DownloadManager',
        'receiver.downloadmanager.DownloadManagerBase',

        'receiver.startserver.DefaultStartServer',
        'receiver.startserver.StartServerBase',

        'receiver.userInter_faces.QtGUI',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ErDrop',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='icon.png',
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
