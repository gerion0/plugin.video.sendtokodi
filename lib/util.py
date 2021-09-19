try:
    import xbmc
    import xbmcaddon

    class KodiLogger:
        def __init__(self):
            addon = xbmcaddon.Addon()
            self.addon_id = addon.getAddonInfo('id')

        def _log(self, msg, level):
            xbmc.log(f'{self.addon_id}: {msg}', level)

        def debug(self, msg):
            log(msg, xbmc.LOGDEBUG)

        def info(self, msg):
            log(msg, xbmc.LOGINFO)

        def warning(self, msg):
            log(msg, xbmc.LOGWARNING)

        def error(self, msg):
            log(msg, xbmc.LOGERROR)

        def critical(self, msg):
            log(msg, xbmc.LOGFATAL)
    log = KodiLogger()

    # fixes python caching bug in youtube-dl, borrowed from
    # https://forum.kodi.tv/showthread.php?tid=112916&pid=2914578#pid2914578
    def patchYoutubeDL():
        import datetime

        # fix for datatetime.strptime returns None
        class proxydt(datetime.datetime):
            @staticmethod
            def strptime(date_string, format):
                import time
                return datetime.datetime(*(time.strptime(date_string,
                                                         format)[0:6]))

        datetime.datetime = proxydt
    patchYoutubeDL()

except ImportError:
    import logging
    log = logging.getLogger("test")

from .yt_dlp.yt_dlp import YoutubeDL
