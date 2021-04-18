# WallpaperEnhancer
Follow these steps:
<ol>
    <li> Place your clone under your <code>%USERPROFILE%</code>:
    the path to <code>enhancer.py</code> should look like
    <code>C:/Users/%USERNAME%/WallpaperEnhancer/enhancer.py</code></li>
    <li> Inside <code>enhancer.py</code>, line 86, place your own coordinates inside <code>Sun( lat, lon )</code>
    <li>If you want, change the pictures inside <code>./Wallpapers</code>: the file extension has
    to be <code>.jpeg</code> and the name of each file should match the <code>hhmmss</code> format, where:
        <ul>
            <li><code>hh</code> is the activation hour</li>
            <li><code>mm</code> is the activation minute</li>
            <li><code>ss</code> is the activation second</li>
        </ul>
    </li>
    <li> Run <code>pip install -r requirements.txt</code> </li>
    <li> Execute <code>python setup.py</code> </li>
</ol>
