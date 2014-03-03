rhcloud:
	@git clean -fd openshift
	@cp -rf app.py templates openshift/wsgi
