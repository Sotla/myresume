all: output/resume.pdf 

files=output/resume.pdf output/resume.tex resume.yaml

output/resume.tex: templates/resume.tex.tmpl resume.yaml genresumes.py
	./genresumes.py tex
	
output/resume.pdf: output/resume.tex res.cls
	pdflatex -interaction=batchmode -output-directory output $<


.PHONY: clean
clean:
	rm -rf output
	rm -f *.pyc
