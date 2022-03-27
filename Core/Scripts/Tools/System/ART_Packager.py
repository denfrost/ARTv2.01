# built-in
import os
import shutil
import filecmp


class ART_Packager():
    """
    Usage:
        import Tools.System.ART_Packager as ART_Packager
        reload(ART_Packager)
        inst = ART_Packager.ART_Packager()
        inst.package("C:/Users/jernst/Documents/artv2/ARTv2", "D:/ARTv2")
    """

    def __init__(self):

        self.ignore_types = [".pyc", ".psd", ".swatches", ".mayaSwatches", ".pickWalk", ".tps", ".picker", ".template",
                             ".weights", ".jno"]
        self.ignore_dirs = [".idea", "_private", "Projects", "github", ".mayaSwatches", "Pickers", "User",
                            "settings", "scripts"]
        self.filesToCopy = []
        self.directories = []

    def convert_path(self, path):
        separator = os.sep
        if separator != "/":
            path = path.replace(os.sep, "/")
        return path

    def package(self, inPath, outPath):
        # get the directory structure of the inPath
        self.returnContents(inPath)

        # copy pasta
        for path in self.filesToCopy:
            new_path = self.convert_path(path.replace(inPath, outPath))
            new_path_dir = os.path.dirname(new_path)

            if os.path.isfile(path):
                if not os.path.exists(new_path_dir):
                    os.makedirs(new_path_dir)
                shutil.copyfile(path, new_path)
            if os.path.isdir(path):
                if not os.path.exists(new_path):
                    os.makedirs(new_path)

    def find_diffs(self, pathA, pathB):
        """
        Usage:
        import Tools.System.ART_Packager as ART_Packager
        reload(ART_Packager)
        inst = ART_Packager.ART_Packager()
        inst.find_diffs("C:/path", "D:/path")
        """

        reportUniques = []
        reportDiffs = []

        self.dir_compare(pathA, pathB, reportUniques, reportDiffs)

        print "Unique Files:"
        for each in reportUniques:
            print each

        print "\n\nDifferent Files:"
        for each in reportDiffs:
            print each

    def dir_compare(self, pathA, pathB, reportUniques, reportDiffs):
        dir_compare = filecmp.dircmp(pathA, pathB)

        if dir_compare.left_only:
            for each in dir_compare.left_only:
                if os.path.splitext(each)[1] not in self.ignore_types:
                    reportUniques.append("Only in " + str(dir_compare.left) + ": " + each)

        if dir_compare.diff_files:
            for each in dir_compare.diff_files:
                reportDiffs.append(each + " is different! " + dir_compare.left + ", " + dir_compare.right)

        for sub_dcmp in dir_compare.subdirs.values():
            self.dir_compare(sub_dcmp.left, sub_dcmp.right, reportUniques, reportDiffs)

    def returnOnlyDirs(self, path, returnList):
        contents = os.listdir(self.convert_path(path))
        for each in contents:
            if os.path.isdir(each):
                if each not in self.ignore_dirs:
                    fullPath = self.convert_path(os.path.join(path, each))
                    returnList.append(fullPath)
                    self.returnOnlyDirs(fullPath, returnList)

    def returnContents(self, path):
        contents = os.listdir(self.convert_path(path))
        for each in contents:
            if each not in self.ignore_dirs:
                if os.path.splitext(each)[1] not in self.ignore_types:
                    fullPath = self.convert_path(os.path.join(path, each))
                    self.filesToCopy.append(fullPath)

                    if os.path.isdir(fullPath):
                        self.returnContents(fullPath)
