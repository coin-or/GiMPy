#============================================================================#
# This file is part of the GiMPy graph library                               #
#                                                                            #
# GiMPy is distributed under the Eclipse Public License as part of the       #
# COIN-OR repository (http://www.coin-or.org).                               #
#                                                                            #
# Authors: Ayukut Bulut, Lehigh University (ayb211@lehigh.edu)               #
#          Ted Ralphs, Lehigh University (ted@lehigh.edu)                    #
#                                                                            #
#                                                                            #
# Copyright (C) 2013, Lehigh University, Aykut Bulut, and Ted Ralphs         #
# All Rights Reserved.                                                       #
#============================================================================#

AUTOMAKE_OPTIONS = foreign

########################################################################
#                          Subdirectories                              #
########################################################################

SUBDIRS  = src/gimpy
SUBDIRS += src/blimpy

# We don't want to compile the test subdirectory, unless the test target is
# specified.  But we need to list it as subdirectory to make sure that it is
# included in the tarball

if ALWAYS_FALSE
  SUBDIRS += test
endif

########################################################################
#             Additional files to be included in tarball               #
########################################################################

# Here we need include all files that are not mentioned in other Makefiles
EXTRA_DIST = 

########################################################################
#                           Extra Targets                              #
########################################################################

test: all
	cd test; $(MAKE) test

unitTest: test

.PHONY: test unitTest 
