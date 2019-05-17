thread2image.py
=================

thread2image.py is a script that scrapes a Reddit thread and converts all the top level comments to images.

How To Setup
*****************

1. Get your Reddit API Keys
----------------------------
	1. Sign up for a new Reddit Account or sign in to your existing account
	2. Go to the Preferences Page;
		>> If you are using the old Reddit interface, just click on Preferences in the top right corner, near your username, followed by clicking on the 'app' tab
		>> In case you are using the new Reddit redesign;
			* Click on the dropdown on your usename in the top right corner
			* Click on User Settings
			* Click on the Privacy and Security tab
			* Click on App Authorization
	3. On the preferences page (https://www.reddit.com/prefs/apps) click on the 'Create Another App' button
	4. In the Type of App section (Radio button options) select 'script' option (this is important do not select other options)
	5. Fill in the other details as necessary
	6. Click the 'Create App' button
	7. Note the 27 character Secret Key (shown in the 'secret' field) and the 14 character personal use script (right below the app name in the top left)

2. Install the dependencies
----------------------------
	1. Open the directory in which you have stored the script
	2. Run the command;
		pip3 install -r requirements.txt

3. Setup the Script
----------------------------
	In the thread2image.py script, Add the following data into the Reddit API Access details section;
		>> 4 character personal use script in the CLIENT_ID field
		>> 27 character Secret Key in the CLIENT_SECRET field
		>> The name of your app that you used in Section 1 above (Get your Reddit API Keys) in the USER_AGENT field
		>> Your Reddit account username in USERNAME field
		>> Your Reddit account password in PASSWORD field

4. Running the Script
----------------------------
	You are ready to run the script!

	Go to the folder containing the script,

	usage: python3 thread2img url [-h] [--target TARGET] [--stub STUB]

	positional arguments:
	  url

	optional arguments:
	  -h, --help       show this help message and exit
	  --target TARGET
	  --stub STUB

	################

	Example: 

	python3 thread2img https://www.reddit.com/r/AskReddit/comments/bn3ab7/atheists_of_reddit_what_is_one_thing_you_admire/ --target /home/myname/myimages --stub myredditimg

	################

	1. --target is used to set the folder where you would like to save all the images and data
	2. --stub is used to specify a filename stub for all files. By default all comments are named 0, 1, 2 etc, specifying a stub such as 'mythread' will set all names to mythread_0.png, mythread_1.png, mythread_2.png, mythread_3.png etc
	3. url is a mandatory positional argument, here you paste the complete Reddit thread URL that you wish to scrape

5. Changing the Fonts
----------------------------
	1. Font files (.ttf files) are stored in the same directory as the script
	2. The default font being used currently is the Noto Sans Regular and the Noto Sans Bold
	3. In case you wish to change the fonts that are being used, you need to;
		>> Download the fonts from a font website (such as https://www.fontsquirrel.com/)
		>> Place the regular font and the bold font (these are generally individual font sets) ttf files in the folder containing the script.
	4. In the thread2image.py script, add the regular font file name to the REGULAR_FONT_FILE variable and add the bold font file to the BOLD_FONT_FILE variable
