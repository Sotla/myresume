On WSL Bash:

To initiate tlmgr (Tex Live package manager)

sudo apt-get install texlive-latex-base texlive-latex-extra texlive-latex-recommended xzdec
tlmgr init-usertree
tlmgr option repository ftp://tug.org/historic/systems/texlive/2015/tlnet-final 
tlmgr install biblatex logreq