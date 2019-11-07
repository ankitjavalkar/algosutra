1. Go to the Directory which contains the course dir you downloaded from the Yaksh.

2. Run the command

   find ./Advanced_Python_Course_\(KV_October_2019\) -maxdepth 3 -mindepth 3 -not -type d > nlist # or any filename tha you prefer

3. Now open the Ipython / python console and run the following Python code to get the file names only

ff = open('nlist', 'r')
ll = ff.readlines()[:]
with open('reslist', 'w') as fo:
    for l in ll:
        fo.write('{0}{1}'.format(l.strip('\n').split('/')[-1], '\n'))

You can then use the file names to create a dictionary in the script and run the script to replace the video references

Before running the script;

1. Add the path of the downloaded course directory to PATH variable
2. Add the name of the directory which contains the videos to VID_DIR
3. VID_DIR must be at the same level as the level of the downloaded course directory.
4. Add key value pairs to LESSON_VID_MAP where the key is the lesson/module name and the value is the corresponding video file name
5. Now run the command

    python replacer.py