# This script generates a Python interface for an Apple Macintosh Manager.
# It uses the "bgen" package to generate C code.
# The function specifications are generated by scanning the mamager's header file,
# using the "scantools" package (customized for this particular manager).

#error missing SetActionFilter

import string

# Declarations that change for each manager
MODNAME = 'Mlte'				# The name of the module

# The following is *usually* unchanged but may still require tuning
MODPREFIX = MODNAME			# The prefix for module-wide routines
INPUTFILE = string.lower(MODPREFIX) + 'gen.py' # The file generated by the scanner
OUTPUTFILE = MODNAME + "module.c"	# The file generated by this program

from macsupport import *

# Create the type objects

includestuff = includestuff + """
#ifdef WITHOUT_FRAMEWORKS
#include <MacTextEditor.h>
#else
#include <xxxx.h>
#endif

/* For now we declare them forward here. They'll go to mactoolbox later */
staticforward PyObject *TXNObj_New(TXNObject);
staticforward int TXNObj_Convert(PyObject *, TXNObject *);
staticforward PyObject *TXNFontMenuObj_New(TXNFontMenuObject);
staticforward int TXNFontMenuObj_Convert(PyObject *, TXNFontMenuObject *);

// ADD declarations
#ifdef NOTYET_USE_TOOLBOX_OBJECT_GLUE
//extern PyObject *_CFTypeRefObj_New(CFTypeRef);
//extern int _CFTypeRefObj_Convert(PyObject *, CFTypeRef *);

//#define CFTypeRefObj_New _CFTypeRefObj_New
//#define CFTypeRefObj_Convert _CFTypeRefObj_Convert
#endif

/*
** Parse/generate ADD records
*/

"""

initstuff = initstuff + """
//	PyMac_INIT_TOOLBOX_OBJECT_NEW(xxxx);
"""
TXNObject = OpaqueByValueType("TXNObject", "TXNObj")
TXNFontMenuObject = OpaqueByValueType("TXNFontMenuObject", "TXNFontMenuObj")

TXNFrameID = Type("TXNFrameID", "l")
TXNVersionValue = Type("TXNVersionValue", "l")
TXNFeatureBits = Type("TXNFeatureBits", "l")
TXNInitOptions = Type("TXNInitOptions", "l")
TXNFrameOptions = Type("TXNFrameOptions", "l")
TXNContinuousFlags = Type("TXNContinuousFlags", "l")
TXNMatchOptions = Type("TXNMatchOptions", "l")
TXNFileType = OSTypeType("TXNFileType")
TXNFrameType = Type("TXNFrameType", "l")
TXNDataType = OSTypeType("TXNDataType")
TXNControlTag = OSTypeType("TXNControlTag")
TXNActionKey = Type("TXNActionKey", "l")
TXNTabType = Type("TXNTabType", "b")
TXNScrollBarState = Type("TXNScrollBarState", "l")
TXNOffset = Type("TXNOffset", "l")
TXNObjectRefcon = FakeType("(TXNObjectRefcon)0") # XXXX For now...
TXNErrors = OSErrType("TXNErrors", "l")
TXNTypeRunAttributes = OSTypeType("TXNTypeRunAttributes")
TXNTypeRunAttributeSizes = Type("TXNTypeRunAttributeSizes", "l")
TXNPermanentTextEncodingType = Type("TXNPermanentTextEncodingType", "l")
TXTNTag = OSTypeType("TXTNTag")
TXNBackgroundType = Type("TXNBackgroundType", "l")
DragReference = OpaqueByValueType("DragReference", "DragObj")
DragTrackingMessage = Type("DragTrackingMessage", "h")
RgnHandle = OpaqueByValueType("RgnHandle", "ResObj")
GWorldPtr = OpaqueByValueType("GWorldPtr", "GWorldObj")
MlteInBuffer = VarInputBufferType('void *', 'ByteCount', 'l')

# ADD object type here

execfile("mltetypetest.py")

# Our (opaque) objects

class TXNObjDefinition(GlobalObjectDefinition):
	def outputCheckNewArg(self):
		Output("if (itself == NULL) return PyMac_Error(resNotFound);")

class TXNFontMenuObjDefinition(GlobalObjectDefinition):
	def outputCheckNewArg(self):
		Output("if (itself == NULL) return PyMac_Error(resNotFound);")


# ADD object class here

# From here on it's basically all boiler plate...

# Create the generator groups and link them
module = MacModule(MODNAME, MODPREFIX, includestuff, finalstuff, initstuff)
TXNObject_object = TXNObjDefinition("TXNObject", "TXNObj", "TXNObject")
TXNFontMenuObject_object = TXNFontMenuObjDefinition("TXNFontMenuObject", "TXNFontMenuObj", "TXNFontMenuObject")

# ADD object here

module.addobject(TXNObject_object)
module.addobject(TXNFontMenuObject_object)
# ADD addobject call here

# Create the generator classes used to populate the lists
Function = OSErrWeakLinkFunctionGenerator
Method = OSErrWeakLinkMethodGenerator

# Create and populate the lists
functions = []
TXNObject_methods = []
TXNFontMenuObject_methods = []

# ADD _methods initializer here
execfile(INPUTFILE)


# add the populated lists to the generator groups
# (in a different wordl the scan program would generate this)
for f in functions: module.add(f)
for f in TXNObject_methods: TXNObject_object.add(f)
for f in TXNFontMenuObject_methods: TXNFontMenuObject_object.add(f)

# ADD Manual generators here

# generate output (open the output file as late as possible)
SetOutputFileName(OUTPUTFILE)
module.generate()

