PY?=venv/bin/python
PELICAN?=venv/bin/pelican
PELICANOPTS=

BASEDIR=$(CURDIR)
INPUTDIR=$(BASEDIR)/content
OUTPUTDIR=$(BASEDIR)/output
CONFFILE=$(BASEDIR)/pelicanconf.py
PUBLISHCONF=$(BASEDIR)/publishconf.py

DEBUG ?= 0
ifeq ($(DEBUG), 1)
	PELICANOPTS += -D
endif

help:
	@echo 'Makefile for a pelican Web site                                        '
	@echo '                                                                       '
	@echo 'Usage:                                                                 '
	@echo '   make html                        (re)generate the web site          '
	@echo '   make clean                       remove the generated files         '
	@echo '   make regenerate                  regenerate files upon modification '
	@echo '   make publish                     generate using production settings '
	@echo '   make serve [PORT=8000]           serve site at http://localhost:8000'
	@echo '   make devserver [PORT=8000]       start/restart develop_server.sh    '
	@echo '   make stopserver                  stop local server                  '
	@echo '   make s3_upload                   upload the web site via S3         '
	@echo '                                                                       '
	@echo 'Set the DEBUG variable to 1 to enable debugging, e.g. make DEBUG=1 html'
	@echo '                                                                       '

html: theme/static/css/marx.min.css $(PELICAN)
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)

clean:
	[ ! -d $(OUTPUTDIR) ] || rm -rf $(OUTPUTDIR)

regenerate: $(PELICAN)
	$(PELICAN) -r $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)

serve: $(PELICAN)
ifdef PORT
	cd $(OUTPUTDIR) && $(PY) -m pelican.server $(PORT)
else
	cd $(OUTPUTDIR) && $(PY) -m pelican.server
endif

devserver: $(PELICAN)
ifdef PORT
	source venv/bin/activate && $(BASEDIR)/develop_server.sh restart $(PORT)
else
	source venv/bin/activate && $(BASEDIR)/develop_server.sh restart
endif

stopserver:
	kill -9 `cat pelican.pid`
	kill -9 `cat srv.pid`
	@echo 'Stopped Pelican and SimpleHTTPServer processes running in background.'

publish: $(PELICAN) theme/static/css/marx.min.css
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(PUBLISHCONF) $(PELICANOPTS)

venv/bin/pip:
	virtualenv -p python3 venv
	venv/bin/pip install markdown boto3 troposphere

$(PELICAN): venv/bin/pip
	venv/bin/pip install pelican markdown webassets cssmin

venv/bin/aws: venv/bin/pip
	venv/bin/pip install awscli

s3_upload: publish venv/bin/aws
	aws s3 sync $(OUTPUTDIR)/ s3://$(shell python stack.py traditionalmead.uk eu-west-2) --delete --acl public-read

.PHONY: html help clean regenerate serve devserver publish s3_upload github
