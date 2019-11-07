from bs4 import BeautifulSoup
import os


PATH = '/home/arj/arj_projects/imp_dump/kv_advanced/course_material/Advanced_Python_Course_(KV_October_2019)'

VID_DIR = 'advanced_videos'

LESSON_VID_MAP = {
# 'AD_-_Decorators_2': '29B_Decorators.webm',
# 'AD_-_Introduction': '01_Introduction.webm',
# 'AD_-_Exercise1': '04_Exercise_1.webm',
# 'AD_-_Exercise5': '08_Exercise_5.webm',
}

def dir_walk(path):
    """ Use to walk through all objects in a directory."""
    for f in os.listdir(path):
        yield os.path.join(path, f)

def walker(path):
    flist = []
    reslist = _walker(path, flist)
    return reslist

def _walker(dirpath, flist):
    for f in os.listdir(dirpath):
        fpath = os.path.join(dirpath, f)
        if os.path.isfile(fpath):
            flist.append(fpath)
        else:
            _walker(fpath, flist)
    return flist

def get_soup(filepath):
    with open(filepath, 'r') as f:
        html = f.read()

    return BeautifulSoup(html, 'html.parser')

def write_soup(filepath, soup):
    with open(filepath, 'w') as f:
        f.write(str(soup))

def check_iframe(filepath):
    soup = get_soup(filepath)
    return soup.iframe

def replace(filepath, video_dir, video_name):
    soup = get_soup(filepath)

    new_vid_tag = soup.new_tag('video')
    new_vid_tag['width'] = "560"
    new_vid_tag['height'] = "315"
    new_vid_tag['controls'] = None

    src_tag = soup.new_tag('source')
    src_tag['src'] = "../../../{0}/{1}".format(video_dir, video_name)
    src_tag['type'] = "video/mp4"

    new_vid_tag.append(src_tag)

    soup.iframe.replace_with(new_vid_tag)
    write_soup(filepath, soup)


if __name__ == '__main__':
    reslist = walker(PATH)
    for f in reslist:
        fpath, fname = os.path.split(f)
        if 'html' in fname:
            fn, fext = fname.split('.')
        else:
            print("NON HTML File: ", fname)
            continue
        if fn in LESSON_VID_MAP and check_iframe(f):
            vid_name = LESSON_VID_MAP.get(fn)
            if vid_name:
                replace(f, VID_DIR, vid_name)
                print("REPLACED: Video: ", vid_name)
            else:
                print("NO VIDEO FOUND: File: ", fname)
        else:
            print("Unknown FILE or NO IFRAME")
