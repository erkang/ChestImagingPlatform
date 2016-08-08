import os.path as path
from collections import OrderedDict
import xml.etree.ElementTree as et
from .chest_conventions_static import *

class ChestConventionsInitializer(object):
    #root_xml_path = "/Users/jonieva/Projects/CIP/Resources/ChestConventions/"
    root_xml_path = path.realpath(path.join(path.dirname(__file__), "..", "..", "Resources", "ChestConventions.xml"))
    __xml_conventions__ = None

    __chest_regions__ = None
    __chest_types__ = None
    __image_features__ = None
    __chest_regions_hierarchy__ = None
    __preconfigured_colors__ = None
    __body_composition_phenotype_names__ = None
    __parenchyma_phenotype_names__ = None
    __pulmonary_vasculature_phenotype_names__ = None

    @staticmethod
    def xml_root_conventions():
        if ChestConventionsInitializer.__xml_conventions__ is None:
            with open(ChestConventionsInitializer.root_xml_path, 'r+b') as f:
                xml = f.read()
                ChestConventionsInitializer.__xml_conventions__ = et.fromstring(xml)
        return ChestConventionsInitializer.__xml_conventions__

    @staticmethod
    def __loadCSV__(file_name):
        """ Return a "list of lists of strings" with all the rows read from a csv file
        Parameters
        ----------
        file_name: name of the file (including the extension). The full path will be concatenated with Root_Folder

        Returns
        -------
        Lists of lists (every row of the csv file will be a list of strings
        """
        import csv
        if not path.isdir(ChestConventionsInitializer.root_xml_path):
            raise AttributeError("The directory where all the csv files should be saved has not been found ({0})".
                                 format(ChestConventionsInitializer.root_xml_path))

        csv_file_path = path.join(ChestConventionsInitializer.root_xml_path, file_name)
        if not path.exists(csv_file_path):
            raise NameError("File {0} not found".format(csv_file_path))
        with open(csv_file_path, 'rb') as f:
            reader = csv.reader(f)
            # Return the concatenation of all the rows in a list
            return [row for row in reader]

    @staticmethod
    def chest_regions():
        if ChestConventionsInitializer.__chest_regions__ is None:
            root = ChestConventionsInitializer.xml_root_conventions()
            ChestConventionsInitializer.__chest_regions__ = OrderedDict()
            parent = root.find("ChestRegions")
            chest_regions_enum = ChestRegion.elems_as_dictionary()
            for xml_region in parent.findall("ChestRegion"):
                elem_id = int(xml_region.find("Id").text)
                if not chest_regions_enum.has_key(elem_id):
                    raise AttributeError("The key {0} in ChestRegions does not belong to the enumeration"
                                         .format(elem_id))
                ChestConventionsInitializer.__chest_regions__[elem_id] = (
                    xml_region.find("Code").text,
                    xml_region.find("Name").text,
                    map(lambda s: float(s), xml_region.find("Color").text.split(";"))
                )

        return ChestConventionsInitializer.__chest_regions__

    @staticmethod
    def chest_regions_hierarchy():
        if ChestConventionsInitializer.__chest_regions_hierarchy__ is None:
            root = ChestConventionsInitializer.xml_root_conventions()
            ChestConventionsInitializer.__chest_regions_hierarchy__ = {}
            parent = root.find("ChestRegionHierarchyMap")
            for hierarchy_node in parent.findall("Hierarchy"):
                p = eval("ChestRegion.{}".format(hierarchy_node.find("Parent").text))
                c = eval("ChestRegion.{}".format(hierarchy_node.find("Child").text))
                # ChestConventionsInitializer.__chest_regions_hierarchy__.append((c,p))
                ChestConventionsInitializer.__chest_regions_hierarchy__[c] = p
        return ChestConventionsInitializer.__chest_regions_hierarchy__



    @staticmethod
    def chest_types():
        if ChestConventionsInitializer.__chest_types__ is None:
            root = ChestConventionsInitializer.xml_root_conventions()
            ChestConventionsInitializer.__chest_types__ = OrderedDict()
            parent = root.find("ChestTypes")
            chest_types_enum = ChestType.elems_as_dictionary()
            for xml_type in parent.findall("ChestType"):
                elem_id = int(xml_type.find("Id").text)
                if not chest_types_enum.has_key(elem_id):
                    raise AttributeError("The key {0} in ChestTypes does not belong to the enumeration"
                                         .format(elem_id))
                try:
                    ChestConventionsInitializer.__chest_types__[elem_id] = (
                        xml_type.find("Code").text,
                        xml_type.find("Name").text,
                        map(lambda s: float(s), xml_type.find("Color").text.split(";"))

                    )
                except Exception as ex:
                    print "Error in {}".format(elem_id)
                    raise ex

        return ChestConventionsInitializer.__chest_types__

    @staticmethod
    def image_features():
        if ChestConventionsInitializer.__image_features__ is None:
            root = ChestConventionsInitializer.xml_root_conventions()
            ChestConventionsInitializer.__image_features__ = OrderedDict()
            parent = root.find("ImageFeatures")
            image_features_enum = ChestType.elems_as_dictionary()
            for xml_type in parent.findall("ImageFeature"):
                elem_id = int(xml_type.find("Id").text)
                if not image_features_enum.has_key(elem_id):
                    raise AttributeError("The key {0} in ImageFeatures does not belong to the enumeration"
                                         .format(elem_id))
                ChestConventionsInitializer.__image_features__[elem_id] = (
                    xml_type.find("Code").text,
                    xml_type.find("Name").text
                )
        return ChestConventionsInitializer.__image_features__

    @staticmethod
    def preconfigured_colors():
        if ChestConventionsInitializer.__preconfigured_colors__ is None:
            ChestConventionsInitializer.__preconfigured_colors__ = OrderedDict()
            rows = ChestConventionsInitializer.__loadCSV__("PreconfiguredColors.csv")
            for row in rows:
                region = eval('ChestRegion.' + row[0].strip())
                _type = eval('ChestType.' + row[1].strip())
                ChestConventionsInitializer.__preconfigured_colors__[(region, _type)] = \
                    (float(row[2].strip()), float(row[3].strip()), float(row[4].strip()))
        return ChestConventionsInitializer.__preconfigured_colors__

    @staticmethod
    def body_composition_phenotype_names():
        if ChestConventionsInitializer.__body_composition_phenotype_names__ is None:
                root = ChestConventionsInitializer.xml_root_conventions()
                ChestConventionsInitializer.__body_composition_phenotype_names__ = list()
                parent = root.find("BodyCompositionPhenotypeNames")
                map(lambda n: ChestConventionsInitializer.__body_composition_phenotype_names__.append(n.text),
                    parent.findall("Name"))
        return ChestConventionsInitializer.__body_composition_phenotype_names__

    @staticmethod
    def parenchyma_phenotype_names():
        if ChestConventionsInitializer.__parenchyma_phenotype_names__ is None:
            root = ChestConventionsInitializer.xml_root_conventions()
            ChestConventionsInitializer.__parenchyma_phenotype_names__ = list()
            parent = root.find("ParenchymaPhenotypeNames")
            map(lambda n: ChestConventionsInitializer.__parenchyma_phenotype_names__.append(n.text),
                parent.findall("Name"))
        return ChestConventionsInitializer.__parenchyma_phenotype_names__

    @staticmethod
    def pulmonary_vasculature_phenotype_names():
        if ChestConventionsInitializer.__pulmonary_vasculature_phenotype_names__ is None:
            root = ChestConventionsInitializer.xml_root_conventions()
            ChestConventionsInitializer.__pulmonary_vasculature_phenotype_names__ = list()
            parent = root.find("PulmonaryVasculaturePhenotypeNames")
            map(lambda n: ChestConventionsInitializer.__pulmonary_vasculature_phenotype_names__.append(n.text),
                parent.findall("Name"))
        return ChestConventionsInitializer.__pulmonary_vasculature_phenotype_names__

#############################
# CHEST CONVENTIONS
#############################
class ChestConventions(object):
    ChestRegionsCollection = ChestConventionsInitializer.chest_regions()      # 1: "WHOLELUNG", "WholeLung", [0.42, 0.38, 0.75]
    ChestRegionsHierarchyCollection = ChestConventionsInitializer.chest_regions_hierarchy()     # LEFTSUPERIORLOBE, LEFTLUNG
    ChestTypesCollection = ChestConventionsInitializer.chest_types()          # 1:, "NORMALPARENCHYMA", "NormalParenchyma", [0.99, 0.99, 0.99]
    ImageFeaturesCollection = ChestConventionsInitializer.image_features()    # 1: "CTARTIFACT", "CTArtifact"
    # PreconfiguredColors = ChestConventionsInitializer.preconfigured_colors()
    #
    BodyCompositionPhenotypeNames = ChestConventionsInitializer.body_composition_phenotype_names()   # List of strings
    ParenchymaPhenotypeNames = ChestConventionsInitializer.parenchyma_phenotype_names()   # List of strings
    PulmonaryVasculaturePhenotypeNames = ChestConventionsInitializer.pulmonary_vasculature_phenotype_names()   # List of strings

    @staticmethod
    def GetNumberOfEnumeratedChestRegions():
        return len(ChestConventions.ChestRegionsCollection)

    @staticmethod
    def GetNumberOfEnumeratedChestTypes():
        return len(ChestConventions.ChestTypesCollection)

    @staticmethod
    def GetNumberOfEnumeratedImageFeatures():
        return len(ChestConventions.ImageFeaturesCollection)

    @staticmethod
    def CheckSubordinateSuperiorChestRegionRelationship(subordinate, superior):
        if subordinate == superior:
            return True

        if ChestRegion.UNDEFINEDREGION in (subordinate, superior):
            return False

        while subordinate in ChestConventions.ChestRegionsHierarchyCollection:
            subordinate = ChestConventions.ChestRegionsHierarchyCollection[subordinate]
            if subordinate == superior:
                return True

        return False

    @staticmethod
    def GetChestRegionFromValue(value):
        return 255 & value  # Less significant byte

    @staticmethod
    def GetChestTypeFromColor(color):
        for key, value in ChestConventions.ChestTypesCollection.iteritems():
            if value[1] == color[0] and value[2] == color[1] and value[3] == color[2]:
                return key
        # Not found
        return ChestType.UNDEFINEDTYPE

    @staticmethod
    def GetChestRegionFromColor(color):
        for key, value in ChestConventions.ChestRegionsCollection.iteritems():
            if value[1] == color[0] and value[2] == color[1] and value[3] == color[2]:
                return key
        # Not found
        return ChestRegion.UNDEFINEDREGION

    @staticmethod
    def GetChestTypeFromValue(value):
        return value >> 8   # Most significant byte


    @staticmethod
    def GetChestWildCardName():
        return "WildCard"

    @staticmethod
    def GetChestTypeName(whichType):
        if not ChestConventions.ChestTypesCollection.has_key(whichType):
            raise IndexError("Key {0} is not a valid ChestType".format(whichType))
        return ChestConventions.ChestTypesCollection[whichType][1]

    @staticmethod
    def GetChestTypeColor(whichType, color=None):
        """ Get the color for a ChestType.
        If color has some value, it will suppose to be a list where the color will be stored (just for compatibility purposes).
        In any case, the color will be returned as the result of the function
        Parameters
        ----------
        whichType
        color

        Returns
        -------
        3-Tuple with the color

        """
        if not ChestConventions.ChestTypesCollection.has_key(whichType):
            raise IndexError("Key {0} is not a valid ChestType".format(whichType))
        col = ChestConventions.ChestTypesCollection[whichType][1:4]
        if color is not None:
            color[0] = col[0]
            color[1] = col[1]
            color[2] = col[2]
        return col


    @staticmethod
    def GetChestRegionColor(whichRegion, color=None):
        """ Get the color for a ChestRegion.
        If color has some value, it will suppose to be a list where the color will be stored (just for compatibility purposes).
        In any case, the color will be returned as the result of the function
        Parameters
        ----------
        whichRegion
        color

        Returns
        -------
        3-Tuple with the color
        """
        if not ChestConventions.ChestRegionsCollection.has_key(whichRegion):
            raise IndexError("Key {0} is not a valid ChestRegion".format(whichRegion))
        col = ChestConventions.ChestRegionsCollection[whichRegion][1:4]
        if color is not None:
            color[0] = col[0]
            color[1] = col[1]
            color[2] = col[2]
        return col

    @staticmethod
    def GetColorFromChestRegionChestType(whichRegion, whichType, color=None):
        """ Get the color for a particular Region-Type.
        It can be preconfigured, a single region/type or the mean value.
        If color has some value, it will suppose to be a list where the color will be stored (just for compatibility purposes).
        In any case, the color will be returned as the result of the function
        Parameters
        ----------
        whichRegion
        whichType
        color

        Returns
        -------
        3-Tuple with the color
        """
        # TODO: override color in preconfigured combination (csv file)
        # Check first if the combination is preconfigured
        if ChestConventions.PreconfiguredColors.has_key((whichRegion, whichType)):
            col = ChestConventions.PreconfiguredColors[(whichRegion, whichType)]
        elif whichRegion == ChestRegion.UNDEFINEDREGION:
            col = ChestConventions.GetChestTypeColor(whichType)
        elif whichType == ChestType.UNDEFINEDTYPE:
            col = ChestConventions.GetChestRegionColor(whichRegion)
        else:
            reg_color = ChestConventions.GetChestRegionColor(whichRegion)
            type_color = ChestConventions.GetChestTypeColor(whichType)
            col = ((reg_color[0] + type_color[0]) / 2.0,
                   (reg_color[1] + type_color[1]) / 2.0,
                   (reg_color[2] + type_color[2]) / 2.0)

        if color is not None:
            color[0] = col[0]
            color[1] = col[1]
            color[2] = col[2]
        return col


    @staticmethod
    def GetChestRegionName(whichRegion):
        """
        Given an unsigned char value corresponding to a chest region, this method will return the string name equivalent
        Args:
            whichRegion:

        Returns:

        """
        if not ChestConventions.ChestRegionsCollection.has_key(whichRegion):
            raise IndexError("Key {0} is not a valid ChestRegion".format(whichRegion))
        return ChestConventions.ChestRegionsCollection[whichRegion][1]

    @staticmethod
    def GetChestRegionNameFromValue(value):
        """ C++ compatibility
        """
        return ChestConventions.GetChestRegionName(value)


    @staticmethod
    def GetChestTypeNameFromValue(value):
        return ChestConventions.ChestTypesCollection[value][1]

    @staticmethod
    def GetValueFromChestRegionAndType(region, type):
        return (type << 8) + region

    @staticmethod
    def GetChestRegionValueFromName(regionString):
        for key,value in ChestConventions.ChestRegionsCollection.iteritems():
            if value[1].lower() == regionString.lower():
                return key
        raise KeyError("Region not found: " + regionString)

    @staticmethod
    def GetChestTypeValueFromName(typeString):
        for key, value in ChestConventions.ChestTypesCollection.iteritems():
            if value[1].lower() == typeString.lower():
                return key
        raise KeyError("Type not found: " + typeString)

    @staticmethod
    def GetChestRegion(i):
        """C++ compatibility"""
        return i

    @staticmethod
    def GetChestType(i):
        """C++ compatibility"""
        return i

    @staticmethod
    def GetImageFeature(i):
        """C++ compatibility"""
        return i

    @staticmethod
    def GetImageFeatureName(whichFeature):
        if not ChestConventions.ImageFeaturesCollection.has_key(whichFeature):
            raise IndexError("Key {0} is not a valid Image Feature".format(whichFeature))
        return ChestConventions.ImageFeaturesCollection[whichFeature][1]

    @staticmethod
    def IsBodyCompositionPhenotypeName(pheno):
        return pheno in ChestConventions.BodyCompositionPhenotypeNames

    @staticmethod
    def IsParenchymaPhenotypeName(pheno):
        return pheno in ChestConventions.ParenchymaPhenotypeNames

    @staticmethod
    def IsPulmonaryVasculaturePhenotypeName(pheno):
        return pheno in ChestConventions.PulmonaryVasculaturePhenotypeNames

    @staticmethod
    def IsHistogramPhenotypeName(pheno):
        return False    # Not used so far

    # In case there are more phenotypes lists, they should be added in the GetPhenotypeNamesLists() function

    @staticmethod
    def IsPhenotypeName(pheno):
        for l in ChestConventions.GetPhenotypeNamesLists():
            if pheno in l: return True
        return False

    @staticmethod
    def IsChestType(chestType):
        return chestType in ChestConventions.ChestTypesCollection

    @staticmethod
    def IsChestRegion(chestRegion):
        return chestRegion in ChestConventions.ChestRegionsCollection

    @staticmethod
    def GetPhenotypeNamesLists():
        return [ChestConventions.BodyCompositionPhenotypeNames, ChestConventions.ParenchymaPhenotypeNames,
                ChestConventions.PulmonaryVasculaturePhenotypeNames]



#############################
# SANITY CHECKS
#############################
# def test_chest_conventions():
#    import CppHeaderParser     # Import here in order not to force the CppHeaderParser module to use ChestConventions (it's just needed for testing and it's not a standard module)

# p = "/Users/jonieva/Projects/CIP/Common/cipChestConventions.h"
# cppHeader = CppHeaderParser.CppHeader(p)
# c_chest_conventions = cppHeader.classes["ChestConventions"]

# def compare_c_python_enum(enum_name, c_enum, p_enum):
#     """ Make sure that all the values in a C++ enumeration are the same in Python
#     Parameters
#     ----------
#     enum_name: name of the enumeration
#     c_enum: C++ enumeration
#     p_enum: Python enumeration
#     """
#     for elem in c_enum:
#         name = elem['name']
#         int_value = elem['value']
#         if not p_enum.has_key(int_value):
#             raise Exception("Error in {0}: Key {1} was found in C++ object but not in Python".format(enum_name, int_value))
#         if p_enum[int_value] != name:
#             raise Exception("Error in {0}: {0}[{1}] (C++) = {2}, but {0}[{1}] (Python) = {3}".format(
#                 enum_name, int_value, name, p_enum[int_value]))
#
# def compare_python_c_enum(enum_name, p_enum, c_enum):
#     """ Make sure that all the values in a Python enumeration are the same in C++
#     Parameters
#     ----------
#     enum_name: name of the enumeration
#     p_enum: Python enumeration
#     c_enum: C++ enumeration
#     """
#     for int_value, description in p_enum.iteritems():
#         found = False
#         for item in c_enum:
#             if item['value'] == int_value:
#                 found = True
#                 if item['name'] != description:
#                     raise Exception("Error in {0}. {0}[{1}} (Python) = {2}, but {0}[{1}] (C++) = {3}".format(
#                         enum_name, int_value, description, item['name']))
#                 break
#         if not found:
#             raise Exception("Error in {0}. Elem '{1}' does not exist in C++".format(enum_name, description))
#
# def compare_python_c_methods(p_methods, c_methods):
#     """ Make sure all the python methods in ChestConventions are the same in Python that in C++
#     Parameters
#     ----------
#     p_methods: Python methods
#     c_methods: C++ methods
#     """
#     for p_method in p_methods:
#         found = False
#         p_name = p_method.func_name
#         for c_method in c_methods:
#             c_name = c_method["name"]
#             if c_name == p_name:
#                 # Matching method found in C++. Check the parameters
#                 found = True
#                 p_args = p_method.func_code.co_varnames
#                 c_args = c_method["parameters"]
#                 if len(p_args) != len(c_args):
#                     raise Exception ("Method '{0}' has {1} parameters in Python and {2} in C++".format(p_name,
#                                                                                             len(p_args), len(c_args)))
#                 for i in range(len(p_args)):
#                     if p_args[i] != c_args[i]["name"]:
#                         raise Exception("The parameter number {0} in Python method '{1}' is '{2}', while in C++ it's '{3}'".
#                                         format(i, p_name, p_args[i], c_args[i]["name"]))
#                 break
#         if not found:
#             raise Exception("Python method '{0}' was not found in C++".format(p_name))
#
# def compare_c_python_methods(c_methods, p_methods):
#     """ Make sure all the python methods in ChestConventions are the same in Python that in C++
#     Parameters
#     ----------
#     c_methods: C++ methods
#     p_methods: Python methods
#     """
#     for c_method in c_methods:
#         if c_method["destructor"] or c_method["constructor"]:
#             continue
#         found = False
#         c_name = c_method["name"]
#         for p_method in p_methods:
#             p_name = p_method.func_name
#             if c_name == p_name:
#                 # Matching method found in Python. Check the parameters
#                 found = True
#                 c_args = c_method["parameters"]
#                 p_args = p_method.func_code.co_varnames
#                 if len(p_args) != len(c_args):
#                     raise Exception ("Method '{0}' has {1} parameters in Python and {2} in C++".format(p_name,
#                                                                                             len(p_args), len(c_args)))
#                 for i in range(len(p_args)):
#                     if p_args[i] != c_args[i]["name"]:
#                         raise Exception("The parameter number {0} in Python method '{1}' is '{2}', while in C++ it's '{3}'".
#                                         format(i, p_name, p_args[i], c_args[i]["name"]))
#                 break
#         if not found:
#             raise Exception("C++ method '{0}' was not found in Python".format(c_name))

# def total_checking():
#     # Go through all the enumerations in C++ and make sure we have the same values in Python
#     for i in range(len(cppHeader.enums)):
#         c_enum = cppHeader.enums[i]["values"]
#         enum_name = cppHeader.enums[i]['name']
#         p_enum = eval("{0}.elems_as_dictionary()".format(enum_name))
#         compare_c_python_enum(enum_name, c_enum, p_enum)
#         compare_python_c_enum(enum_name, p_enum, c_enum)
#         print(cppHeader.enums[i]['name'] + "...OK")
#
#     # Make sure that all the methods in ChestConventions in C++ are implemented in Python and viceversa
#     p_methods = [f[1] for f in inspect.getmembers(ChestConventions, inspect.isfunction)]
#     c_methods = c_chest_conventions.get_all_methods()
#
#     compare_c_python_methods(c_methods, p_methods)
#     print("C++ --> Python checking...OK")
#
#     compare_python_c_methods(p_methods, c_methods)
#     print("Python --> C++ checking...OK")
#