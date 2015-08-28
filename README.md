# Chop-n-screw
My humble attempt at taking any song you want, and [chopping and screwing](http://en.wikipedia.org/wiki/Chopped_and_screwed) it with the help of the wicked cool [Echo Nest Remix!](http://echonest.github.io/remix/)
- Slows down the tempo
- Reduces the pitch
- Skips beats / repeats beats

TODO:
-----
- Record scratching
- Stop-time

Prep:
-----
If you want to run this program on your machine, you'll need:
--
1. Python 2.7.5.
2. Install Echo Nest Remix with <pre>sudo pip install remix</pre> or <pre>sudo easy_install remix</pre>
3. Create an account and get a developer key from [The Echo Nest](http://developer.echonest.com/raw_tutorials/register.html)
4. Once you've got your key, read this [key install tutorial](https://echonest.github.io/remix/keysetup.html) for Windows, Mac or Linux.

Usage:
------
<pre>python screw.py [input_filename] [output_filename]</pre>

Example: <pre>python screw.py ATLiens.mp3 chopped-n-screwed.mp3</pre>
