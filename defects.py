"""Class for generating random defect combinations based
on the types of defects enabled.
"""

import math
import random
import numpy as np


class Defects:

    def __init__(self,
                 missing_teeth_en : bool = False,
                 bent_teeth_en : bool = False,
                 warping_en : bool = False,
                 ejector_marks_en : bool = False,
                 gloss_en : bool = False,
                 discoloration_en : bool = False,
                 contamination_en : bool = False,
                 cloudy_en : bool = False,
                 splay_en : bool = False,
                 num_ejector_marks : int = 2):

        # List of all the enabled defects
        self.__defects_enabled = []

        if missing_teeth_en:
            self.__defects_enabled.append("missing_teeth")
        if bent_teeth_en:
            self.__defects_enabled.append("bent_teeth")
        if warping_en:
            self.__defects_enabled.append("warping")
        if ejector_marks_en:
            self.__defects_enabled.append("ejector_marks")
        if gloss_en:
            self.__defects_enabled.append("gloss")
        if discoloration_en:
            self.__defects_enabled.append("discoloration")

        if contamination_en or cloudy_en or splay_en:
            self.__defects_enabled.append("texture")

        # List of all of the enabled texture defects
        self.__tex_defects_enabled = []

        if contamination_en:
            self.__tex_defects_enabled.append("contamination")
        if cloudy_en:
            self.__tex_defects_enabled.append("cloudy")
        if splay_en:
            self.__tex_defects_enabled.append("splay")

        if (num_ejector_marks == 2 or num_ejector_marks == 3):
            self.__num_ejector_marks = num_ejector_marks
        else:
            raise ValueError("Invalid number of ejector marks.")

        self.updateDefectCombination()


    def __meanDefects(self) -> float:
        """Returns the expected number of defects an object should have."""

        mean_num_defects = 1.75 - 2.25/max(float(len(self.__defects_enabled)), 2.25)

        return mean_num_defects


    def __calcNumDefects(self) -> int:
        """Returns the number of defects the next object should have, chosen randomly from a Poisson distribution."""

        rand = np.random.poisson(self.__meanDefects())
        rand = min(len(self.__defects_enabled), rand)

        return rand


    def updateDefectCombination(self):
        """Update the state of the defects to a new random state depending on the enabled defects."""

        num_defects = self.__calcNumDefects()

        defects = random.sample(self.__defects_enabled, num_defects)

        # Update states
        self.missing_teeth = defects.count("missing_teeth") > 0
        self.bent_teeth = defects.count("bent_teeth") > 0
        self.warping = defects.count("warping") > 0
        self.ejector_marks = self.__num_ejector_marks if defects.count("ejector_marks") > 0 else 0
        self.gloss = defects.count("gloss") > 0
        self.discoloration = defects.count("discoloration") > 0

        # The texture defects are mutually exclusive
        self.tex_defect = None
        if defects.count("texture") != 0:
            defects.remove("texture")
            self.tex_defect = random.sample(self.__tex_defects_enabled, 1)[0]
            defects.append(self.tex_defect)

        self.contamination = defects.count("contamination") > 0
        self.cloudy = defects.count("cloudy") > 0
        self.splay = defects.count("splay") > 0