"""
Stretchy IK Limb Node
"""

import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

NODE_NAME = "ARTv2_Stretchy_IK"
NODE_ID = OpenMaya.MTypeId(0x8700B)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class stretchIK(OpenMayaMPx.MPxNode):

    # input connections needed
    startMatrix = OpenMaya.MObject()
    endMatrix = OpenMaya.MObject()
    upInitLength = OpenMaya.MObject()
    downInitLength = OpenMaya.MObject()
    poleVectorMatrix = OpenMaya.MObject()

    # node attributes
    stretch = OpenMaya.MObject()
    slide = OpenMaya.MObject()
    globalScale = OpenMaya.MObject()
    poleVectorLock = OpenMaya.MObject()

    # node outputs
    upScale = OpenMaya.MObject()
    downScale = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    def creator(self):
        return OpenMayaMPx.asMPxPtr(stretchIK())

    def initialize(self):

        # attribute function sets
        numFn = OpenMaya.MFnNumericAttribute()
        matrixFn = OpenMaya.MFnMatrixAttribute()

        # input matrices
        stretchIK.startMatrix = matrixFn.create("startMatrix", "stm")
        matrixFn.setStorable(True)
        matrixFn.setKeyable(True)
        stretchIK.addAttribute(stretchIK.startMatrix)

        stretchIK.endMatrix = matrixFn.create("endMatrix", "enm")
        matrixFn.setStorable(True)
        matrixFn.setKeyable(True)
        stretchIK.addAttribute(stretchIK.endMatrix)

        stretchIK.poleVectorMatrix = matrixFn.create("poleVectorMatrix", "pvm")
        matrixFn.setStorable(True)
        matrixFn.setKeyable(True)
        stretchIK.addAttribute(stretchIK.poleVectorMatrix)

        # input values
        stretchIK.upInitLength = numFn.create("upInitLength", "uil", OpenMaya.MFnNumericData.kDouble, 0.0)
        numFn.setStorable(True)
        numFn.setKeyable(True)
        stretchIK.addAttribute(stretchIK.upInitLength)

        stretchIK.downInitLength = numFn.create("downInitLength", "dil", OpenMaya.MFnNumericData.kDouble, 0.0)
        numFn.setStorable(True)
        numFn.setKeyable(True)
        stretchIK.addAttribute(stretchIK.downInitLength)

        stretchIK.globalScale = numFn.create("globalScale", "gls", OpenMaya.MFnNumericData.kDouble, 1.0)
        numFn.setStorable(True)
        numFn.setKeyable(True)
        numFn.setMin(0.001)
        stretchIK.addAttribute(stretchIK.globalScale)

        stretchIK.poleVectorLock = numFn.create("poleVectorLock", "pvl", OpenMaya.MFnNumericData.kDouble, 0.0)
        numFn.setStorable(True)
        numFn.setKeyable(True)
        numFn.setMin(0.0)
        numFn.setMax(1.0)
        stretchIK.addAttribute(stretchIK.poleVectorLock)

        stretchIK.stretch = numFn.create("stretch", "str", OpenMaya.MFnNumericData.kDouble, 0.0)
        numFn.setStorable(True)
        numFn.setKeyable(True)
        numFn.setMin(0.0)
        numFn.setMax(1.0)
        stretchIK.addAttribute(stretchIK.stretch)

        stretchIK.slide = numFn.create("slide", "sld", OpenMaya.MFnNumericData.kDouble, 0.0)
        numFn.setStorable(True)
        numFn.setKeyable(True)
        numFn.setMin(-1.0)
        numFn.setMax(1.0)
        stretchIK.addAttribute(stretchIK.slide)

        # outputs
        stretchIK.upScale = numFn.create("upScale", "ups", OpenMaya.MFnNumericData.kDouble, 1.0)
        numFn.setWritable(False)
        stretchIK.addAttribute(stretchIK.upScale)

        stretchIK.downScale = numFn.create("downScale", "dws", OpenMaya.MFnNumericData.kDouble, 1.0)
        numFn.setWritable(False)
        stretchIK.addAttribute(stretchIK.downScale)

        # attribute affects for notifying dag refresh
        stretchIK.attributeAffects(stretchIK.startMatrix, stretchIK.upScale)
        stretchIK.attributeAffects(stretchIK.endMatrix, stretchIK.upScale)
        stretchIK.attributeAffects(stretchIK.stretch, stretchIK.upScale)
        stretchIK.attributeAffects(stretchIK.slide, stretchIK.upScale)
        stretchIK.attributeAffects(stretchIK.globalScale, stretchIK.upScale)
        stretchIK.attributeAffects(stretchIK.poleVectorLock, stretchIK.upScale)
        stretchIK.attributeAffects(stretchIK.poleVectorMatrix, stretchIK.upScale)
        stretchIK.attributeAffects(stretchIK.upInitLength, stretchIK.upScale)

        stretchIK.attributeAffects(stretchIK.startMatrix, stretchIK.downScale)
        stretchIK.attributeAffects(stretchIK.endMatrix, stretchIK.downScale)
        stretchIK.attributeAffects(stretchIK.stretch, stretchIK.downScale)
        stretchIK.attributeAffects(stretchIK.slide, stretchIK.downScale)
        stretchIK.attributeAffects(stretchIK.globalScale, stretchIK.downScale)
        stretchIK.attributeAffects(stretchIK.poleVectorLock, stretchIK.downScale)
        stretchIK.attributeAffects(stretchIK.poleVectorMatrix, stretchIK.downScale)
        stretchIK.attributeAffects(stretchIK.downInitLength, stretchIK.downScale)

    def compute(self, plug, data):

        if plug == stretchIK.downScale or plug == stretchIK.upScale:

            # get input matrix
            startMatrixV = data.inputValue(stretchIK.startMatrix).asMatrix()
            endMatrixV = data.inputValue(stretchIK.endMatrix).asMatrix()
            pvMatrixV = data.inputValue(stretchIK.poleVectorMatrix).asMatrix()

            # get initial length inputs
            upInitLenV = data.inputValue(stretchIK.upInitLength).asDouble()
            downInitLenV = data.inputValue(stretchIK.downInitLength).asDouble()

            # check for negative translate values
            invertUp = False
            if upInitLenV < 0:
                invertUp = True
                upInitLenV = abs(upInitLenV)

            invertDn = False
            if downInitLenV < 0:
                invertDn = True
                downInitLenV = abs(downInitLenV)

            # get parameter inputs
            stretchV = data.inputValue(stretchIK.stretch).asDouble()
            slideV = data.inputValue(stretchIK.slide).asDouble()
            lockV = data.inputValue(stretchIK.poleVectorLock).asDouble()
            globalScaleV = data.inputValue(stretchIK.globalScale).asDouble()

            # compute total length
            chainLength = upInitLenV + downInitLenV

            # compute the bone vectors
            startVector = OpenMaya.MVector(startMatrixV(3, 0), startMatrixV(3, 1), startMatrixV(3, 2))
            endVector = OpenMaya.MVector(endMatrixV(3, 0), endMatrixV(3, 1), endMatrixV(3, 2))
            currentLengthVector = endVector - startVector

            # compute length
            chainLength = chainLength * globalScaleV
            currentLength = currentLengthVector.length()

            # create output variables
            upScaleOut = upInitLenV
            downScaleOut = downInitLenV

            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # COMPUTE STRETCH
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # if are stretch value is not zero, compute the stretch
            if stretchV > 0.001:
                ratio = currentLength/chainLength
                if ratio > 1:
                    ratio = ((ratio - 1) * stretchV) + 1
                    # ratio - 1 gives us the scale factor (1.5 - 1 = 0.5). Multiply that by how much stretch should
                    # apply, then add the 1 back in for the final value
                else:
                    ratio = 1

                # multiply up and down scale outs by this stretch factor ratio
                upScaleOut = upScaleOut * ratio
                downScaleOut = downScaleOut * ratio

            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # COMPUTE SLIDE
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # slideRatio is a multiplier that takes into account the proportions of the bone length.
            # for example, if you wanted to know 30% of the bone length, and then subtract 70% from the other bone,
            # unless these bones are the same length, you will not get proper results.
            # ex: if total length is 8, and upper bone is 3, then if slide were all the way at 1.0, 3 would need to
            # scale 2.6 times. That's what the slide ratio gives you. The delta variable is for linear interpolation
            # for when the slide value is not 0, 1, or -1.
            if slideV > 0:
                slideRatio = chainLength / (upInitLenV * globalScaleV)
                delta = (slideRatio - 1) * slideV
                upScaleOut = upScaleOut * (delta + 1)
                downScaleOut = downScaleOut * (1 - slideV)
            else:
                slideRatio = chainLength / (downInitLenV * globalScaleV)
                delta = (slideRatio - 1) * -slideV
                downScaleOut = downScaleOut * (delta + 1)
                upScaleOut = upScaleOut * (1 + slideV)

            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # COMPUTE ELBOW LOCK
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            if lockV > 0.001:
                pvPos = OpenMaya.MVector(pvMatrixV(3, 0), pvMatrixV(3, 1), pvMatrixV(3, 2))

                # compute the length of the vector needed to snap to the pole vector
                startPole = pvPos - startVector
                endPole = endVector - pvPos
                startPoleLength = startPole.length()/globalScaleV
                endPoleLength = endPole.length()/globalScaleV

                # interp between the two values
                # i = percent difference * A + percent * B
                # example: 1 - .4 = 0.6.   0.6 * 10 = 6.0.  15 * .4 = 6     6 + 6 = 12. 12 is 40% of 15.
                upScaleOut = (upScaleOut * (1 - lockV)) + (startPoleLength * lockV)
                downScaleOut = (downScaleOut * (1 - lockV)) + (endPoleLength * lockV)

            # account for negative translate values
            if invertUp:
                upScaleOut = upScaleOut * -1
            if invertDn:
                downScaleOut = downScaleOut * -1

            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # set output values
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            data.outputValue(stretchIK.downScale).setDouble(downScaleOut)
            data.outputValue(stretchIK.downScale).setClean()

            data.outputValue(stretchIK.upScale).setDouble(upScaleOut)
            data.outputValue(stretchIK.upScale).setClean()

        else:
            return OpenMaya.kUnknownParameter


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Plugin Main
def initializePlugin(obj):

    plugin = OpenMayaMPx.MFnPlugin(obj, "Jeremy Ernst", "1.0", "Any")
    try:
        plugin.registerNode(NODE_NAME, NODE_ID, stretchIK().creator, stretchIK().initialize)

    except Exception:
        sys.stderr.write("Failed to register node: %s" % NODE_NAME)
        raise


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def uninitializePlugin(obj):

    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(NODE_ID)
    except Exception:
        sys.stderr.write("Failed to deregister node: %s" % NODE_NAME)
