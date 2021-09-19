from .util import YoutubeDL, log


def extract(url, with_dash=True, only_audio=False, opts=None):
    if opts is None:
        opts = {}

    if "format" not in opts:
        if only_audio:
            opts["format"] = "bestaudio"
        elif with_dash:
            opts["format"] = "bestvideo+bestaudio"
        else:
            opts["format"] = "best"

    opts["logger"] = log

    ydl = YoutubeDL(opts)
    ydl.add_default_info_extractors

    with ydl:
        result = ydl.extract_info(url, download=False)

    import pprint
    pprint.pprint(result)
