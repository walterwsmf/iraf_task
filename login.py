# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 16:02:11 2016

e-mail: walter at on.br
        waltersmartinsf at gmail.com

Load packages for exoplanet data reduction

A comparative login.cl to pyraf
"""
from pyraf import iraf

#load usefull packages for exoplanet reduction
iraf.stsdas()
iraf.toolbox()
iraf.noao()
iraf.astutil()
iraf.proto()
iraf.imred()
iraf.ccdred()
iraf.digiphot()
iraf.apphot()
iraf.images()
iraf.tv()
iraf.imutil()
iraf.headers()
iraf.immatch()
iraf.crutil()

#******************************************************************************
#******************** BEGIN CONFIGURATION *************************************
#******************************************************************************

#*********************************************************************** IMEXAM
#give the default conditions for imexamine
iraf.imexamine.unlearn()
iraf.imexamine.frame = 1
iraf.imexamine.nloutput = 101
iraf.imexamine.ncoutput = 101
iraf.imexamine.keeplog = 'no'
iraf.imexamine.defkey= "a"
iraf.imexamine.autoredraw = 'yes'
iraf.imexamine.allframes = 'no'
iraf.imexamine.nframes = 1
iraf.imexamine.ncstat = 100
iraf.imexamine.nlstat = 100
iraf.imexamine.wcs = "logical"
iraf.imexamine.graphics = "stdgraph"
iraf.imexamine.display = "display(image='$1',frame=$2)"
iraf.imexamine.use_display = 'yes'
iraf.imexamine.mode = "ql"

#***********************************************************************RIMEXAM 
#give the conditions for rimexam
iraf.rimexam.unlearn()
iraf.rimexam.banner = 'yes'
iraf.rimexam.xlabel = 'Radius'
iraf.rimexam.ylabel = 'Pixel Value'
iraf.rimexam.fitplot = 'yes'
iraf.rimexam.fittype = 'moffat'
iraf.rimexam.center = 'yes'
iraf.rimexam.background = 'yes'
iraf.rimexam.radius = 10.
iraf.rimexam.buffer= 4.
iraf.rimexam.width= 7.
iraf.rimexam.iterations = 5
iraf.rimexam.xorder = 0
iraf.rimexam.yorder = 0
iraf.rimexam.magzero = 25.
iraf.rimexam.beta = 'INDEF'
iraf.rimexam.rplot = 17.
iraf.rimexam.x1 = 'INDEF'
iraf.rimexam.x2 = 'INDEF'
iraf.rimexam.y1 = 'INDEF'
iraf.rimexam.y2 = 'INDEF'
iraf.rimexam.pointmode = 'yes'
iraf.rimexam.marker = 'plus'
iraf.rimexam.szmarker = 1.
iraf.rimexam.logx = 'no'
iraf.rimexam.logy = 'no'
iraf.rimexam.box = 'yes'
iraf.rimexam.ticklabels = 'yes'
iraf.rimexam.majrx = 5
iraf.rimexam.minrx = 5
iraf.rimexam.majry = 5
iraf.rimexam.minry = 5
iraf.rimexam.round = 'no'
iraf.rimexam.mode = 'ql'

#************************************************************************IMSTAT
iraf.imstat.unlearn()
iraf.imstat.fields = "image,npix,mean,stddev,min,max"
iraf.imstat.lower = 'INDEF'
iraf.imstat.upper = 'INDEF'
iraf.imstat.nclip = 0#give the conditions for hselect
iraf.hselect.unlearn()
iraf.hselect.fields = 'hjd'
iraf.hselect.expr = 'yes'
iraf.hselect.missing = 'INDEF'
iraf.hselect.mode = 'ql'
iraf.imstat.lsigma = 3.
iraf.imstat.usigma = 3.
iraf.imstat.binwidth = 0.1
iraf.imstat.format = 'yes'
iraf.imstat.cache = 'no'
#iraf.imstat.mode = 'ql

#*************************************************************************HEDIT
#give the conditions for hedit
iraf.hedit.unlearn()
iraf.hedit.value='1'
iraf.hedit.add = 'no'
iraf.hedit.addonly = 'no'
iraf.hedit.delete = 'no'
iraf.hedit.verify = 'no'
iraf.hedit.show = 'no'
iraf.hedit.update = 'yes'
iraf.hedit.mode = 'ql'

#***********************************************************************HSELECT
#give the conditions for hselect
iraf.hselect.unlearn()
iraf.hselect.fields = 'hjd'
iraf.hselect.expr = 'yes'
iraf.hselect.missing = 'INDEF'
iraf.hselect.mode = 'ql'

#*********************************************************************IMCOMBINE
#imcombine default
iraf.imcombine.unlearn()
iraf.imcombine.imcmb = '$I'
iraf.imcombine.logfile = 'STDOUT'
iraf.imcombine.combine = 'median'
iraf.imcombine.reject = 'avsigclip'
iraf.imcombine.project = 'no'
iraf.imcombine.outtype = 'real'
iraf.imcombine.offsets = 'none'
iraf.imcombine.masktype = 'none'
iraf.imcombine.maskvalue = 0.
iraf.imcombine.blank = 0.
iraf.imcombine.scale = 'none'
iraf.imcombine.zero = 'none'
iraf.imcombine.weight = 'none'
iraf.imcombine.statsec = '[100:1265,100:1265]'
iraf.imcombine.expname = 'exptime'
iraf.imcombine.lthreshold = 'INDEF'
iraf.imcombine.hthreshold = 'INDEF'
iraf.imcombine.nlow = 1
iraf.imcombine.nhigh = 1
iraf.imcombine.nkeep = 1
iraf.imcombine.mclip = 'yes'
iraf.imcombine.lsigma = 3.
iraf.imcombine.hsigma = 3.
iraf.imcombine.rdnoise = 5.7
iraf.imcombine.gain = 3.1
iraf.imcombine.snoise = 0.
iraf.imcombine.sigscale = 0.1
iraf.imcombine.pclip = 0.5
iraf.imcombine.grow = 0.
iraf.imcombine.mode = 'ql'

#**********************************************************************CCDHEDIT
#default for ccdhedit
iraf.ccdhedit.unlearn()
iraf.ccdhedit.parameter = 'filter'
iraf.ccdhedit.value = 'Schott-8612'
iraf.ccdhedit.type = 'string'
iraf.ccdhedit.mode = 'ql'

#***********************************************************************DISPLAY
#default for display
iraf.display.unlearn()
iraf.display.frame = 1
iraf.display.bpmask = 'BPM'
iraf.display.bpdisplay = 'none'
iraf.display.bpcolors = 'red'
iraf.display.ocolors = 'green'
iraf.display.erase = 'yes'
iraf.display.border_erase = 'no'
iraf.display.select_frame = 'yes'
iraf.display.repeat = 'no'
iraf.display.fill = 'no'
iraf.display.zscale = 'yes'
iraf.display.contrast = 0.25
iraf.display.zrange = 'yes'
iraf.display.zmask = ''
iraf.display.nsample = 1000
iraf.display.xcenter = 0.5
iraf.display.ycenter = 0.5
iraf.display.xsize = 1.
iraf.display.ysize = 1.
iraf.display.xmag = 0.75
iraf.display.ymag = 0.75
iraf.display.order = 0
iraf.display.z1 = 128.
iraf.display.z2 = 4000.
iraf.display.ztrans = 'linear'
iraf.display.lutfile = ''
iraf.display.mode = 'ql'

#********************************************************************SETAIRMASS
#default for setairmass
iraf.setairmass.unlearn()
iraf.setairmass.observatory = ')_.observatory'
iraf.setairmass.intype = 'beginning'
iraf.setairmass.outtype = 'effective'
iraf.setairmass.ra = 'ra'
iraf.setairmass.dec = 'dec'
iraf.setairmass.equinox = 'epoch'
iraf.setairmass.st = 'st'
iraf.setairmass.ut = 'ut'
iraf.setairmass.date = 'date-obs'
iraf.setairmass.exposure = 'exptime'
iraf.setairmass.airmass = 'airmass'
iraf.setairmass.utmiddle = 'utmiddle'
iraf.setairmass.scale = 750.
iraf.setairmass.show = 'yes'
iraf.setairmass.update = 'yes'
iraf.setairmass.override = 'yes'
iraf.setairmass.mode = 'ql'

#*************************************************************************SETJD
#default for setjd
iraf.setjd.unlearn()
iraf.setjd.observatory = ')_.observatory'
iraf.setjd.date = 'date-obs'
iraf.setjd.time = 'utmiddle'
iraf.setjd.ra = 'ra'
iraf.setjd.dec = 'dec'
iraf.setjd.epoch = 'epoch'
iraf.setjd.jd = 'jd'
iraf.setjd.hjd = 'hjd'
iraf.setjd.ljd = 'ljd'
iraf.setjd.utdate = 'yes'
iraf.setjd.uttime = 'yes'
iraf.setjd.listonly = 'no'
iraf.setjd.mode = 'ql'

#************************************************************************FIXPIX
#default for fixpix
iraf.fixpix.unlearn()
iraf.fixpix.masks = 'badpix.3x3.pl'
iraf.fixpix.linterp = 1
iraf.fixpix.cinterp = 2
iraf.fixpix.verbose = 'no'
iraf.fixpix.pixels = 'no'
iraf.fixpix.mode = 'ql'

#********************************************************************COSMICRAYS
#default for cosmicrays
iraf.cosmicrays.unlearn()
iraf.cosmicrays.answer = 'no'
iraf.cosmicrays.crmask = 'crmask'
iraf.cosmicrays.threshold = 20.
iraf.cosmicrays.fluxratio = 5.
iraf.cosmicrays.npasses = 500
iraf.cosmicrays.window = 7
iraf.cosmicrays.interactive = 'no'
iraf.cosmicrays.train = 'no'
iraf.cosmicrays.graphics = 'stdgraph'
iraf.cosmicrays.mode = 'ql'

#**********************************************************************DATAPARS
#default for datapars
iraf.datapars.unlearn()
iraf.datapars.scale = 1.
iraf.datapars.fwhmpsf = 4.
iraf.datapars.emission = 'yes'
iraf.datapars.sigma = 8.4
iraf.datapars.datamin = -60.
iraf.datapars.datamax = 150000.
iraf.datapars.noise = 'constant'
iraf.datapars.ccdread = 'rdnoise'
iraf.datapars.gain = 'gain'
iraf.datapars.readnoise = 'INDEF'
iraf.datapars.epadu = 'INDEF'
iraf.datapars.exposure = 'exptime'
iraf.datapars.airmass = 'airmass'
iraf.datapars.filter = 'filter'
iraf.datapars.obstime = 'hjd'
iraf.datapars.itime = 'INDEF'
iraf.datapars.xairmass = 'INDEF'
iraf.datapars.ifilter = 'INDEF'
iraf.datapars.otime = 'INDEF'
iraf.datapars.mode = 'ql'

#********************************************************************CENTERPARS
#default for centerpars
iraf.centerpars.unlearn()
iraf.centerpars.calgorithm = 'centroid'
iraf.centerpars.cbox = 16.
iraf.centerpars.cthreshold = 0.
iraf.centerpars.minsnratio = 1.
iraf.centerpars.maxshift = 0.05
iraf.centerpars.clean = 'no'
iraf.centerpars.rclean = 1.
iraf.centerpars.rclip = 2.
iraf.centerpars.kclean = 3.
iraf.centerpars.mkcenter = 'no'
iraf.centerpars.mode = 'ql'

#********************************************************************FITSKYPARS
#default for fitskypars
iraf.fitskypars.unlearn()
iraf.fitskypars.salgorithm = 'median'
iraf.fitskypars.annulus = 20.
iraf.fitskypars.dannulus = 10.
iraf.fitskypars.skyvalue = 0.
iraf.fitskypars.smaxiter = 10
iraf.fitskypars.sloclip = 0.
iraf.fitskypars.shiclip = 0.
iraf.fitskypars.snreject = 50
iraf.fitskypars.sloreject = 3.
iraf.fitskypars.shireject = 3.
iraf.fitskypars.khist = 3.
iraf.fitskypars.binsize = 0.1
iraf.fitskypars.smooth = 'no'
iraf.fitskypars.rgrow = 0.
iraf.fitskypars.mksky = 'no'
iraf.fitskypars.mode = 'ql'

#**********************************************************************PHOTPARS
#default for photpars
iraf.photpars.unlearn()
iraf.photpars.weighting = 'constant'
iraf.photpars.apertures = '16'
iraf.photpars.zmag = 23.2
iraf.photpars.mkapert = 'no'
iraf.photpars.mode = 'ql'

#**************************************************************************PHOT
#default for phot
iraf.phot.skyfile = 'xyfile'
iraf.phot.coords = 'xyfile'
iraf.phot.output = 'default'
iraf.phot.plotfile = ''
iraf.phot.datapars = ''
iraf.phot.centerpars = ''
iraf.phot.fitskypars = ''
iraf.phot.photpars = ''
iraf.phot.interactive = 'no'
iraf.phot.radplots = 'no'
iraf.phot.icommands = ''
iraf.phot.gcommands = ''
iraf.phot.wcsin = ')_.wcsin'
iraf.phot.wcsout = ')_.wcsout'
iraf.phot.cache = ')_.cache'
iraf.phot.verify = 'no'
iraf.phot.update = 'no'
iraf.phot.verbose = 'no'
iraf.phot.graphics = 'stdgraph'
iraf.phot.display = 'stdimage'
iraf.phot.mode = 'ql'

#************************************************************************TXDUMP
#default for txdump
iraf.txdump.unlearn()
#iraf.txdump.texfiles = ''
iraf.txdump.fields = 'image,xc,yc,ifilter,xairmass,otime,mag,merr'
iraf.txdump.expr = '(id==1)'
iraf.txdump.headers = 'yes'
iraf.txdump.parameters = 'yes'
iraf.txdump.mode = 'ql'

#******************************************************************************
#********************   END CONFIGURATION *************************************
#******************************************************************************