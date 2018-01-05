# BRIT (Backup the Really Important Things)

Little tool with Qt GUI for backing up dedicated directories and files to zip files.

I start this project mainly as an exercise in Python. I follow these goals:
- Learn more about Python
- Learn more about Qt
- Learn more about github
- Get a tool for saving some files

On the idea of BRIT

It's not a real backup tool (there are a lot better tools for this around). The problem I want to solve is the following:

I need no full backup of my laptop: All relevant things are normally on the network (either in the company or in the cloud or on my private NAS). So when the disk crashes or a new installation is needed due to a virus attack, everything can be retrieved somehow.
But there are a few small things, that are not on the network and that I would like to have at a save place.
For example, I need not backup my browser, but I want to backup my favorites list. Another example is the configuration of Total Commander (a tool I use all the time).
Also when I an offline (e.g. when travelling), it's a good feeling to have the current work copied to a zip on a USK stick.

I know, there are also a lot of tools to do similar things, but see my goals 1 to 3.
Furthermore most of the tools I saw are intended to be used on Linux. I work on Windows, thus I cannot use things like tar etc. (I know, that I could use Cygwin). And I wanted to have an easy to use GUI.

Currently the tool is under development. Many things are still missing and I assume there are some errors. So do not use this for production...
 