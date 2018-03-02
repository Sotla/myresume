# PA-CV

Academic CVs end up being quite unmanagable after some point. This is a Python/Latex toolchain that I use to generate [mine](https://www.imperial.ac.uk/people/p.angeloudis/cv/CV-Angeloudis.pdf). 

Inspiration came from [James Keirstead](https://github.com/jkeirstead/jk-vita), [Brandon Amos](https://github.com/bamos/cv) and [David Hu](https://github.com/divad12/resume). The code used in this project was forked from the latter, but was modified heavily to simplify and automate the build process, and allow for more streamlined template management.

# Instructions

I normally use Windows, but setting everything up there can become quite tedious. Instead, I use Ubuntu within the Windows Subsystem for Linux. This code assumes that you are operating with Python 3.x.

## Setup

```
sudo apt-get install texlive-latex-base texlive-latex-extra texlive-latex-recommended xzdec
pip install cheetah3 tex pyyaml
tlmgr init-usertree
tlmgr option repository ftp://tug.org/historic/systems/texlive/2015/tlnet-final 
tlmgr install biblatex logreq
```