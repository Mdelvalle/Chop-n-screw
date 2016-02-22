# Purporize
My humble attempt at taking any song you want, and [chopping and screwing](http://en.wikipedia.org/wiki/Chopped_and_screwed) it with the help of the wicked cool [Echo Nest Remix!](http://echonest.github.io/remix/)
- Slows down the tempo
- Reduces the pitch
- Skips beats / repeats beats

Check out the web app [here](purporize.herokuapp.com)!

TODO:
-----
- Record scratching
- Stop-time

Local setup:
===========

Prep:
-----
If you want to run this program on your machine, you'll need:

1. Node.js version 5.0.0
2. Python 2.7.10 and Pip
3. An account and a developer key from [The Echo Nest](http://developer.echonest.com/raw_tutorials/register.html) + [key up](https://echonest.github.io/remix/keysetup.html).
4. FFMPEG

[Here's]() The Echo Nest instructions on the matter, just in case.

Installation/building:
---------------------
First:
<pre>pip install numpy==1.6.2</pre>
<pre>pip install git+https://github.com/Mdelvalle/remix.git</pre>

Then:
<pre>npm install</pre>

Finally:
<pre>node index.js</pre>

Go to 0.0.0.0:5000 to view.

Or:
=====
You can just use the python script by itself.

Usage:
------
<pre>python screw.py [input_filename] [output_filename]</pre>

Example: <pre>python screw.py song.mp3 end.mp3</pre>
