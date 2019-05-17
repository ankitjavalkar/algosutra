#!/usr/bin/env python3
import json
import os
import textwrap
import argparse
import html
import re
import time

import requests
from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
from markdown import markdown
import praw


CUR_DIR = os.getcwd()

# Reddit API Access Details
CLIENT_ID='PERSONAL_USE_SCRIPT_14_CHARS',
CLIENT_SECRET='SECRET_KEY_27_CHARS ',
USER_AGENT='YOUR_APP_NAME',
USERNAME='YOUR_REDDIT_USER_NAME',
PASSWORD='YOUR_REDDIT_LOGIN_PASSWORD',

IMG_SIZE_WIDTH = 990
IMG_SIZE_HEIGHT = 100

TEXT_BOX_WIDTH = 900

PADDING = 30
WRAP_WIDTH = 130

REGULAR_FONT_FILE = 'NotoSans-Regular.ttf'
BOLD_FONT_FILE = 'NotoSans-Bold.ttf'

BODY_FONT_SIZE = 15
HEADER_FONT_SIZE = 12
FOOTER_FONT_SIZE = 12


def convert_epoch_to_pretty_timestamp(time):
    from datetime import datetime
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(second_diff // 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff // 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff // 7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff // 30) + " months ago"
    return str(day_diff // 365) + " years ago"

def prettify_number(number):
    if number > 1000:
        pretty_number = '{:.1f}k'.format(number/1000)
    else:
        pretty_number = '{}'.format(number)
    return pretty_number

def split_to_fit(text, wrap_width=WRAP_WIDTH):
    raw_wrapped_text = textwrap.wrap(text, width=wrap_width)
    return '\n'.join(raw_wrapped_text)

def markdown_to_text(markdown_string):
    """ Converts a markdown string to plaintext """

    # md -> html -> text since BeautifulSoup can extract text cleanly

    clean_markdown_string = html.unescape(markdown_string)

    html_text = markdown(clean_markdown_string)

    # remove code snippets
    html_text = re.sub(r'<pre>(.*?)</pre>', ' ', html_text)
    html_text = re.sub(r'<code>(.*?)</code>', ' ', html_text)

    # extract text
    soup = BeautifulSoup(html_text, "html.parser")
    text = ''.join(soup.findAll(text=True))

    return text


def _typeset(image, elements):
    draw = ImageDraw.Draw(image)
    for elem in elements:
        draw.text(
            (elem['x_pos'], elem['y_pos']),
            elem['text'],
            font=elem['font'],
            fill=elem['fill_color']
        )

    return image


def create_post_image(post_data):
    # Set dummy image to calculate Title text box height
    box_height_calc_img = ImageText(
        (IMG_SIZE_WIDTH, IMG_SIZE_WIDTH),
        background=(255, 255, 255, 200)
    )

    # Create post header element
    pretty_date = convert_epoch_to_pretty_timestamp(post_data['created_utc'])
    header_text = '{0}  \u00b7  Posted by u/{1}  \u00b7  {2}'.format(
        post_data['subreddit_name'], post_data['author'], pretty_date
    )

    # Set x and y positions
    header_x_pos = 10
    header_y_pos = 10

    # Set font details
    header_font_file = REGULAR_FONT_FILE
    header_font_size = 12

    header_element = {
        'x_pos': header_x_pos,
        'y_pos': header_y_pos,
        'text': header_text ,
        'fill_color': (129, 131, 132), #(0, 0, 0), # black
        'font': ImageFont.truetype(header_font_file, header_font_size),
    }

    # Create comment body element
    title_text = split_to_fit(markdown_to_text(post_data.get('title'))) if post_data.get('title') else ''

    # Set x and y positions
    title_x_pos = 10
    title_y_pos = header_y_pos + header_font_size + 10 # padding between title and header of 10 px

    # Set font details
    title_font_file = BOLD_FONT_FILE
    title_font_size = 17

    title_element = {
        'x_pos': title_x_pos,
        'y_pos': title_y_pos,
        'text': title_text ,
        'fill_color': (215, 218, 220), # (0, 0, 0), # black
        'font': ImageFont.truetype(title_font_file, title_font_size),
    }

    box_width, title_text_box_height = box_height_calc_img.write_text_box(
        10, 30,
        title_text,
        box_width=TEXT_BOX_WIDTH,
        font_filename=title_font_file, 
        font_size=title_font_size,
        color=(0, 0, 0),
    )

    # Create comment body element
    body_text = split_to_fit(markdown_to_text(post_data.get('body'))) if post_data.get('body') else ''

    # Set x and y positions
    body_x_pos = 10
    body_y_pos = title_y_pos + title_text_box_height + 10 # padding between body and title text of 10 px

    # Set font details
    body_font_file = REGULAR_FONT_FILE
    body_font_size = 15

    body_element = {
        'x_pos': body_x_pos,
        'y_pos': body_y_pos,
        'text': body_text ,
        'fill_color': (215, 218, 220), # (0, 0, 0), # black
        'font': ImageFont.truetype(body_font_file, body_font_size),
    }

    # Set dummy image to calculate body text box height
    box_height_calc_img = ImageText(
        (IMG_SIZE_WIDTH, IMG_SIZE_WIDTH),
        background=(255, 255, 255, 200)
    )

    box_width, body_text_box_height = box_height_calc_img.write_text_box(
        10, 30,
        body_text,
        box_width=TEXT_BOX_WIDTH,
        font_filename=body_font_file, 
        font_size=body_font_size,
        color=(0, 0, 0),
    )

    # Create comment footer element
    pretty_comment_number = prettify_number(int(post_data['comment_number']))
    footer_text = '{0} Comments  Share  Report  Save'.format(pretty_comment_number)

    # Set x and y positions
    footer_x_pos = 10
    footer_y_pos = body_y_pos + body_text_box_height + 10 # padding between body and header text of 10 px

    # Set font details
    footer_font_file = BOLD_FONT_FILE
    footer_font_size = 12

    footer_element = {
        'x_pos': footer_x_pos,
        'y_pos': footer_y_pos,
        'text': footer_text ,
        'fill_color': (129, 131, 132), # (0, 0, 0), # black
        'font': ImageFont.truetype(footer_font_file, footer_font_size),
    }

    image_size_height = footer_y_pos + footer_font_size + 20 # bottom padding of 20 px

    img = Image.new('RGBA', (IMG_SIZE_WIDTH, image_size_height), (58, 58, 60))

    return _typeset(img, [header_element, title_element, body_element, footer_element])

def create_comment_image(comment_data):
    # Set dummy image to calculate body text box height
    box_height_calc_img = ImageText(
        (IMG_SIZE_WIDTH, IMG_SIZE_WIDTH),
        background=(255, 255, 255, 200)
    )

    # Create comment header element
    pretty_date = convert_epoch_to_pretty_timestamp(comment_data['created_utc'])
    header_text = '{0}  {1} points  \u00b7  {2}'.format(
        comment_data['author'], prettify_number(comment_data['score']), pretty_date
    )

    # Set x and y positions
    header_x_pos = 10
    header_y_pos = 10

    # Set font details
    header_font_file = REGULAR_FONT_FILE
    header_font_size = 12

    header_element = {
        'x_pos': header_x_pos,
        'y_pos': header_y_pos,
        'text': header_text ,
        'fill_color': (129, 131, 132), #(0, 0, 0), # black
        'font': ImageFont.truetype(header_font_file, header_font_size),
    }

    # Create comment body element
    body_text = split_to_fit(markdown_to_text(comment_data.get('body'))) if comment_data.get('body') else ''

    # Set x and y positions
    body_x_pos = 10
    body_y_pos = header_y_pos + header_font_size + 10

    # Set font details
    body_font_file = REGULAR_FONT_FILE
    body_font_size = 15

    body_element = {
        'x_pos': body_x_pos,
        'y_pos': body_y_pos,
        'text': body_text ,
        'fill_color': (215, 218, 220), # (0, 0, 0), # black
        'font': ImageFont.truetype(body_font_file, body_font_size),
    }

    box_width, body_text_box_height = box_height_calc_img.write_text_box(
        10, 30,
        body_text,
        box_width=TEXT_BOX_WIDTH,
        font_filename=body_font_file, 
        font_size=body_font_size,
        color=(0, 0, 0),
    )

    # Create comment footer element
    footer_text = 'Share  Report  Save'

    # Set x and y positions
    footer_x_pos = 10
    footer_y_pos = body_y_pos + body_text_box_height + 10 # padding between body and header text of 10 px

    # Set font details
    footer_font_file = BOLD_FONT_FILE
    footer_font_size = 12

    footer_element = {
        'x_pos': footer_x_pos,
        'y_pos': footer_y_pos,
        'text': footer_text ,
        'fill_color': (129, 131, 132), # (0, 0, 0), # black
        'font': ImageFont.truetype(footer_font_file, footer_font_size),
    }

    image_size_height = footer_y_pos + footer_font_size + 20 # bottom padding of 20 px

    img = Image.new('RGBA', (IMG_SIZE_WIDTH, image_size_height), (58, 58, 60))

    return _typeset(img, [header_element, body_element, footer_element])

def save_image(filename, image):
    image.save(filename)

def get_thread(url, stub='', target=CUR_DIR):
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT,
        username=USERNAME,
        password=PASSWORD,
    )
    thread_json = []

    submission = reddit.submission(url=url)
    post_data = {
        'title': submission.title, 
        'body': submission.selftext,
        'subreddit_name': submission.subreddit_name_prefixed,
        'author': submission.author.name if submission.author else '',
        'score': submission.score if submission.score else 0,
        'comment_number': submission.num_comments,
        'created_utc': int(submission.created_utc),
    }
    filename = 'post.png'
    filename_stub = stub if stub else ''
    absolute_file = os.path.join(target, '_'.join((filename_stub, filename)))
    save_image(absolute_file, create_post_image(post_data))
    thread_json.append(post_data)

    submission.comments.replace_more(limit=0, threshold=0)
    print(len(submission.comments))
    for ix, comment in enumerate(submission.comments):
        comment_data = {
            'body': comment.body,
            'author': comment.author.name if comment.author else '',
            'score': comment.score if comment.score else 0,
            'created_utc': int(comment.created_utc),
        }
        filename = '{}.png'.format(ix)
        filename_stub = stub
        absolute_file = os.path.join(target, '_'.join((filename_stub, filename)))
        save_image(absolute_file, create_comment_image(comment_data))
        thread_json.append(comment_data)

    # write the json to file
    filename = 'data.json'
    filename_stub = stub
    absolute_file = os.path.join(target, '_'.join((filename_stub, filename)))
    thread_json_dump = json.dumps(thread_json)
    with open(absolute_file, 'w') as f:
        f.write(thread_json_dump)


class ImageText(object):
    def __init__(self, filename_or_size, mode='RGBA', background=(0, 0, 0, 0),
                 encoding='utf8'):
        if isinstance(filename_or_size, str):
            self.filename = filename_or_size
            self.image = Image.open(self.filename)
            self.size = self.image.size
        elif isinstance(filename_or_size, (list, tuple)):
            self.size = filename_or_size
            self.image = Image.new(mode, self.size, color=background)
            self.filename = None
        self.draw = ImageDraw.Draw(self.image)
        self.encoding = encoding

    def save(self, filename=None):
        self.image.save(filename or self.filename)

    def get_font_size(self, text, font, max_width=None, max_height=None):
        if max_width is None and max_height is None:
            raise ValueError('You need to pass max_width or max_height')
        font_size = 1
        text_size = self.get_text_size(font, font_size, text)
        if (max_width is not None and text_size[0] > max_width) or \
           (max_height is not None and text_size[1] > max_height):
            raise ValueError("Text can't be filled in only (%dpx, %dpx)" % \
                    text_size)
        while True:
            if (max_width is not None and text_size[0] >= max_width) or \
               (max_height is not None and text_size[1] >= max_height):
                return font_size - 1
            font_size += 1
            text_size = self.get_text_size(font, font_size, text)

    def write_text(self, x, y, text, font_filename, font_size=11,
                   color=(0, 0, 0), max_width=None, max_height=None):
        # if isinstance(text, str):
        #     text = text.decode(self.encoding)
        if font_size == 'fill' and \
           (max_width is not None or max_height is not None):
            font_size = self.get_font_size(text, font_filename, max_width,
                                           max_height)
        text_size = self.get_text_size(font_filename, font_size, text)
        font = ImageFont.truetype(font_filename, font_size)
        if x == 'center':
            x = (self.size[0] - text_size[0]) / 2
        if y == 'center':
            y = (self.size[1] - text_size[1]) / 2
        self.draw.text((x, y), text, font=font, fill=color)
        return text_size

    def get_text_size(self, font_filename, font_size, text):
        font = ImageFont.truetype(font_filename, font_size)
        return font.getsize(text)

    def write_text_box(self, x, y, text, box_width, font_filename,
                       font_size=11, color=(0, 0, 0), place='left',
                       justify_last_line=False):
        lines = []
        line = []
        words = text.split()
        for word in words:
            new_line = ' '.join(line + [word])
            size = self.get_text_size(font_filename, font_size, new_line)
            text_height = size[1]
            if size[0] <= box_width:
                line.append(word)
            else:
                lines.append(line)
                line = [word]
        if line:
            lines.append(line)
        lines = [' '.join(line) for line in lines if line]
        height = y
        for index, line in enumerate(lines):
            height += text_height
            if place == 'left':
                self.write_text(x, height, line, font_filename, font_size,
                                color)
            elif place == 'right':
                total_size = self.get_text_size(font_filename, font_size, line)
                x_left = x + box_width - total_size[0]
                self.write_text(x_left, height, line, font_filename,
                                font_size, color)
            elif place == 'center':
                total_size = self.get_text_size(font_filename, font_size, line)
                x_left = int(x + ((box_width - total_size[0]) / 2))
                self.write_text(x_left, height, line, font_filename,
                                font_size, color)
            elif place == 'justify':
                words = line.split()
                if (index == len(lines) - 1 and not justify_last_line) or \
                   len(words) == 1:
                    self.write_text(x, height, line, font_filename, font_size,
                                    color)
                    continue
                line_without_spaces = ''.join(words)
                total_size = self.get_text_size(font_filename, font_size,
                                                line_without_spaces)
                space_width = (box_width - total_size[0]) / (len(words) - 1.0)
                start_x = x
                for word in words[:-1]:
                    self.write_text(start_x, height, word, font_filename,
                                    font_size, color)
                    word_size = self.get_text_size(font_filename, font_size,
                                                    word)
                    start_x += word_size[0] + space_width
                last_word_size = self.get_text_size(font_filename, font_size,
                                                    words[-1])
                last_word_x = x + box_width - last_word_size[0]
                self.write_text(last_word_x, height, words[-1], font_filename,
                                font_size, color)
        return (box_width, height - y)


if __name__=="__main__":
    parser = argparse.ArgumentParser(prog='thread2img', description='Pull Post and Comments from a Reddit Thread and convert them to images')
    parser.add_argument('url')
    parser.add_argument('--target')
    parser.add_argument('--stub')

    args = parser.parse_args() 
    url = args.url
    stub = args.stub if args.stub else ''
    target = args.target if args.target else CUR_DIR
    get_thread(url, stub=stub, target=target)