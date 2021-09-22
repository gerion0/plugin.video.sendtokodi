from .util import YoutubeDL, log

from xml.sax.saxutils import escape, quoteattr

class URL(str):
    def is_url():
        return True


class DASH(str):
    def is_url():
        return False


def _get_mime(video_ext, audio_ext):
    assert video_ext == "none" or audio_ext == "none"
    if video_ext != "none":
        return "video/" + video_ext
    if audio_ext != "none":
        return "audio/" + audio_ext


def _gen_dash(ydl_result):
    # proof of concept, oriented on
    # https://github.com/anxdpanic/script.module.tubed.api/blob/master/resources/lib/src/tubed_api/usher/lib/mpeg_dash.py
    mpd_list = ['<?xml version="1.0" encoding="UTF-8"?>\n'
                '<MPD xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                'xmlns="urn:mpeg:dash:schema:mpd:2011" '
                'xmlns:xlink="http://www.w3.org/1999/xlink" '
                'xsi:schemaLocation="urn:mpeg:dash:schema:mpd:2011 '
                'http://standards.iso.org/ittf/PubliclyAvailableStandards/'
                'MPEG-DASH_schema_files/DASH-MPD.xsd" '
                'minBufferTime="PT1.5S" mediaPresentationDuration="PT', str(ydl_result["duration"]),
                'S" type="static" profiles="urn:mpeg:dash:profile:isoff-main:2011">\n',
                '\t<Period>\n']
    for idx, entry in enumerate(ydl_result["requested_formats"]):
        mpd_list.append(''.join(['\t\t<AdaptationSet id="', str(idx),
                                 '" mimeType="', _get_mime(entry['video_ext'],
                                                           entry['audio_ext']), '" ']))

        if entry["language"] != "none":
            mpd_list.append(''.join(['lang="', entry["language"], '" ']))

        mpd_list.append(''.join(['subsegmentAlignment="true" subsegmentStartsWithSAP="1" '
                                 'bitstreamSwitching="true" default="true">\n']))

        mpd_list.append('\t\t\t<Role schemeIdUri="urn:mpeg:DASH:role:2011" '
                        'value="main"/>\n')

        if entry["acodec"] != "none":
            mpd_list.append(''.join(['\t\t\t<Representation id="audio" codecs="',
                                     entry["acodec"], '" bandwidth="',
                                     str(entry["tbr"]), '">\n']))

            mpd_list.append('\t\t\t\t<AudioChannelConfiguration '
                            'schemeIdUri="urn:mpeg:dash:23003:3:'
                            'audio_channel_configuration:2011" value="2"/>\n')
        if entry["vcodec"] != "none":
            mpd_list.append(''.join(['\t\t\t<Representation id="video" codecs="',
                                     str(entry["vcodec"]), '" startWithSAP="1" bandwidth="',
                                     str(entry["tbr"]), '" width="',
                                     str(entry["width"]), '" height="',
                                     str(entry["height"]), '" frameRate="',
                                     str(entry["fps"]), '">\n']))

        mpd_list.append(''.join(['\t\t\t\t<BaseURL>',
                                 escape(entry["url"]),
                                 '</BaseURL>\n']))

        mpd_list.append(''.join(['\t\t\t\t<SegmentBase indexRange="0-0">\n',
                                 '\t\t\t\t\t\t<Initialization range="0-0" />\n',
                                 '\t\t\t\t</SegmentBase>\n']))

        mpd_list.append('\t\t\t</Representation>\n')
        mpd_list.append('\t\t</AdaptationSet>\n')
    mpd_list.append('\t</Period>\n</MPD>\n')
    return ''.join(mpd_list)


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
    opts['youtube_include_dash_manifest'] = True

    ydl = YoutubeDL(opts)
    ydl.add_default_info_extractors

    with ydl:
        result = ydl.extract_info(url, download=False)
        import pprint
        del result["formats"]
        pprint.pprint(result)

        if "url" in result:
            return URL(result["url"])

        if "requested_formats" in result:
            return DASH(_gen_dash(result))
