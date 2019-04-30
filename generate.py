#!/usr/bin/env python

"""
Takes yaml resume input source, escapes it, and feeds it to the Cheetah
templating engine
"""

import functools
import glob
import os
import re
import shutil
from optparse import OptionParser
from shutil import copyfile

import tex
import yaml
from Cheetah.Template import Template

HYPERLINK_REGEX = re.compile(r'\[([^\]]*)\]\(([^)]*)\)')


def escape_tex(s):
    # s = HYPERLINK_REGEX.sub(r'\href{\2}{\1}', s)
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
    parser = OptionParser(usage="%prog <runtype>",
                          description="Fills in Cheetah templates from YAML source to " +
                                      "generate resume of the given <runtype> format." +
                                      "The default option is tex")

    options, extra_args = parser.parse_args()
    if len(extra_args) < 1:
        parser.print_help()
        extra_args = 'tex'
    else:
        extra_args = extra_args[0]

    return options, extra_args


def load_db():
    contents = dict()
    for fname in glob.glob('data/*.yaml'):
        contents.update(yaml.load(open(fname, 'r').read()))
    return contents


def latex_build():
    copyfile("data/publications.bib", "%s/publications.bib" % output_dir)
    copyfile("templates/res.cls", "%s/res.cls" % output_dir)
    os.chdir(output_dir)
    os.system("pdflatex resume.tex")
    os.system("bibtex resume")
    os.system("pdflatex resume.tex")
    os.system("pdflatex resume.tex")
    copyfile("resume.pdf", "Angeloudis-CV.pdf")


def prep_dirs():
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


if __name__ == '__main__':
    options, runtype = get_cmd_line_args()
    db_contents = load_db()

    templatefile = 'templates/resume.%s.tmpl' % str(runtype)
    output_dir = "output_%s" % runtype

    if runtype == "tex":
        db_contents = escape_leaves(escape_tex, db_contents)
    template = Template(file=templatefile, searchList=[db_contents])

    prep_dirs()

    filename = f'{output_dir}/resume.{runtype}'
    contents = str(template)
    open(filename, 'w').write(contents)

    if runtype == "tex":
        latex_build()
