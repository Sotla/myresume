# PA-CV

Academic CVs end up being quite unmanagable after some point. This is a Python and Latex project for the automatic generation of [my CV](https://github.com/p-ang/CV/blob/master/output/resume.pdf). 

Inspiration came from [James Keirstead](https://github.com/jkeirstead/jk-vita) and [Kusno Mudiarto](https://github.com/mudiarto/resume). The code used in this project was initially forked from the latter, but was modified to simplify and automate the build process, and allow for more streamlined template management.

# Instructions

While I normally use Windows, setting everything up there can get quite tedious. To generate my CV, I use an Ubuntu installation within the Windows Subsystem for Linux. This code assumes that you are operating with Python 3.x, although it should work with Python 2.x

## Setup

```
sudo apt-get install texlive-latex-base texlive-latex-extra texlive-latex-recommended xzdec
pip install cheetah3 tex pyyaml
tlmgr init-usertree
tlmgr option repository ftp://tug.org/historic/systems/texlive/2015/tlnet-final 
tlmgr install biblatex logreq
```