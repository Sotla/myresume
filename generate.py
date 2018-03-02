#!/usr/bin/env python

"""
Takes yaml resume input source, escapes it, and feeds it to the Cheetah
templating engine
"""

from Cheetah.Template import Template
from datetime import datetime
from optparse import OptionParser
import functools
import os
import sys
import yaml
import shutil
import glob
import tex
import re
from shutil import copyfile
import subprocess

HYPERLINK_REGEX = re.compile(r'\[([^\]]*)\]\(([^)]*)\)')

def escape_tex(s):
    s = HYPERLINK_REGEX.sub(r'\href{\2}{\1}', s)
    s = tex.escape_latex(s)
    s = s.replace('LaTeX', r'\LaTeX')
    # A bit of a hack... have to reverse some of tex.escape_latex escapes
    s = s.replace('\\textbackslash{}', '\\')
    s = s.replace('\\{', '{').replace('\\}', '}')
    return s

def escape_txt(s):
    # Replace all markdown-esque hyperlinks with just the link text
    s = HYPERLINK_REGEX.sub(r'\1', s)
    return s

def escape_leaves(escape_func, contents):
    """Escapes all leaves in the contents dict with escape_func"""
    if isinstance(contents, list):
        return map(functools.partial(escape_leaves, escape_func), contents)
    elif isinstance(contents, dict):
        return dict(map(lambda x: (x[0], escape_leaves(escape_func, x[1])),
            contents.items()))
    else:
        return escape_func(str(contents))

def get_cmd_line_args():
    parser = OptionParser(usage="%prog [options] <extension>",
        description="Fills in Cheetah templates from YAML source to " +
                    "generate resume of the given <extension> format."+
                    "The default option is tex")

    parser.add_option("-o", "--output_dir",
        default='output',
        help="Output directory of generated files. Defaults to output/")

    parser.add_option("-t", "--template",
        default='templates/resume.%s.tmpl',
        help="Filename of the output format template. Defaults to templates/resume.<extension>.tmpl")

    options, extra_args = parser.parse_args()
    if len(extra_args) < 1:
        parser.print_help()
        extra_args='tex'
        

    return options, extra_args

if __name__ == '__main__':
    options, extension = get_cmd_line_args()
    contents = dict()

    for fname in glob.glob('data/*.yaml'):
            contents.update(yaml.load(open(fname, 'r').read()))


    escaped_contents = escape_leaves(escape_tex, contents)
    template = Template(file=options.template % extension, searchList=[escaped_contents])

    output_dir = options.output_dir

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


    open('%s/resume.%s' % (output_dir, extension), 'w').write(str(template))
    copyfile("data/publications.bib","output/publications.bib")
    copyfile("templates/res.cls","output/res.cls")
    
    os.chdir("output")
    os.system("pdflatex resume.tex")
    os.system("bibtex resume")
    os.system("pdflatex resume.tex")
    os.system("pdflatex resume.tex")

    copyfile("resume.pdf","CV-Angeloudis.pdf")

    


    

