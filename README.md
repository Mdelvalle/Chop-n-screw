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

1. Latest Node.js release
2. Python 2.7.10
3. Install NumPy 1.6.2, with <pre>pip install -Iv https://pypi.python.org/packages/source/n/numpy/numpy-1.6.2.tar.gz#md5=95ed6c9dcc94af1fc1642ea2a33c1bba</pre>
4. Install Echo Nest Remix 2.2.1 with <pre>pip install -Iv http://static.echonest.com/remix/packages/remix-2.2.1.tar.gz#md5=041b1af37800d638b626d627eee58acc</pre>
6. Create an account and get a developer key from [The Echo Nest](http://developer.echonest.com/raw_tutorials/register.html)
7. Once you've got your key, read this [key install tutorial](https://echonest.github.io/remix/keysetup.html) for Windows, Mac or Linux.

And then:
<pre>npm install</pre>

Or:
=====
You can also just use the python script by itself.

Usage:
------
<pre>python screw.py [input_filename] [output_filename]</pre>

Example: <pre>python screw.py ATLiens.mp3 chopped-n-screwed.mp3</pre>
