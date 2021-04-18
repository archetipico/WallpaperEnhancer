import ctypes
import os
import subprocess
import pythoncom as pc
import pywintypes as pw
import time
import win32gui as w32g

from datetime import datetime, timezone
from suntime import Sun
from typing import List
from win32com.shell import shell, shellcon

# https://stackoverflow.com/a/56974396
def make_filter(class_name: str, title: str):
    def enum_windows( handle: int, handle_list: list ):
        if not ( class_name or title ):
            handle_list.append( handle )
        if class_name and class_name not in w32g.GetClassName( handle ):
            return True
        if title and title not in w32g.GetWindowText( handle ):
            return True

        handle_list.append( handle )

    return enum_windows

def find_handles( p: int = None, window_class: str = None, title: str = None ) -> List[int]:
    cb = make_filter( window_class, title )

    try:
        handle_list = []
        if p:
            w32g.EnumChildWindows( p, cb, handle_list )
        else:
            w32g.EnumWindows( cb, handle_list )
        return handle_list
    except pw.error:
        return []

def set_wallpaper( path: str ) -> None:
    pc.CoInitialize()

    args = (0x52c, 0, 0, 0, 500, None)
    ctypes.windll.user32.SendMessageTimeoutW(
        find_handles( window_class='Progman' )[0],
        *args
    )

    ad = pc.CoCreateInstance(
        shell.CLSID_ActiveDesktop,
        None,
        pc.CLSCTX_INPROC_SERVER,
        shell.IID_IActiveDesktop
    )

    ad.SetWallpaper( path, 0 )
    ad.ApplyChanges( shellcon.AD_APPLY_ALL )
    ctypes.windll.user32.UpdatePerUserSystemParameters( 1 )

def get_time() -> str:
    date = time.ctime( time.time() )
    date_splitted = date.split()
    hms = date_splitted[3]
    return hms.replace( ':', '' )

def get_wallpaper( path: str, name: str ) -> str:
    return r'{}\{}{}'.format(
        path,
        name,
        '.jpeg'
    )

def set_theme( values: List[str] ) -> None:
    base = ['reg.exe', 'add', 'HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize', '/v']
    system = base + ['SystemUsesLightTheme', '/t', 'REG_DWORD', '/d', values[0], '/f']
    apps = base + ['AppsUseLightTheme', '/t', 'REG_DWORD', '/d', values[1], '/f']
    windows = base + ['WindowsUseLightTheme', '/t', 'REG_DWORD', '/d', values[2], '/f']

    subprocess.run( system, stdout=subprocess.DEVNULL )
    subprocess.run( apps, stdout=subprocess.DEVNULL )
    subprocess.run( windows, stdout=subprocess.DEVNULL )

if __name__ == '__main__':
    # prepare for theme
    sun = Sun( 45.4, 9.1 )
    sunrise = sun.get_sunrise_time().strftime( '%H:%M:%S' )
    sunset = sun.get_sunset_time().strftime( '%H:%M:%S' )
    do_light, do_dark = True, True

    theme = {
        "light": [
            '1',
            '1',
            '0'
        ],
        "dark": [
            '0',
            '0',
            '0'
        ]
    }

    # prepare for wallpapers
    path = r'{}\WallpaperEnhancer\Wallpapers'.format( os.environ['USERPROFILE'] )
    files = os.listdir( path )
    images_str = [x.replace( '.jpeg', '' ) for x in files]
    images = [int( x ) for x in images_str]

    diff = [abs( x - int( get_time() ) ) for x in images]
    first = images[diff.index( min( diff ) )]

    wallpaper = get_wallpaper( path, str( first ) )
    if os.path.isfile( wallpaper ):
        set_wallpaper( wallpaper )

    while True:
        utc_time = datetime.now( timezone.utc ).strftime( '%H:%M:%S' )
        wallpaper = get_wallpaper( path, get_time() )
        
        if os.path.isfile( wallpaper ):
            set_wallpaper( wallpaper )

        if utc_time > sunrise and utc_time < sunset and do_light:
            set_theme( theme["light"] )
            do_light = not do_light
            do_dark = True

        elif ( utc_time <= sunrise or utc_time >= sunset ) and do_dark:
            set_theme( theme["dark"] )
            do_light = True
            do_dark = not do_dark
        
        time.sleep( 1 )