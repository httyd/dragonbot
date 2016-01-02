import sys
import os
import glob
import inspect
import pickle

from .skilltemplate import Skill

def load_skills(bot, skills_directory, data_file):

    """Load a list of skills (Python code) from a skills directory, create new
    instances of these skill classes, and restore previous data values of these
    skills from a data file if they exist."""

    skills = {}

    skills_directory = os.path.abspath(skills_directory)
    skill_list = glob.glob(os.path.join(skills_directory, "*.py"))
    sys.path.insert(0, skills_directory)

    data_file = os.path.abspath(data_file)

    try:

        with open(data_file, "rb") as f:
            data = pickle.load(f)

    except:

        data = {}

    for skill_file in skill_list:

        skill_name = os.path.basename(os.path.splitext(skill_file)[0])
        module = __import__(skill_name)

        for module_class in inspect.getmembers(module, inspect.isclass):

            if module_class[1] != Skill and issubclass(module_class[1], Skill):

                instance = module_class[1](bot)
                skills[module_class[0]] = instance

                if module_class[0] not in data:
                    continue

                for key, value in data[module_class[0]].items():

                    try:

                        old_attr = getattr(instance, key)

                        if callable(old_attr):
                            continue

                        setattr(instance, key, value)

                    except:

                        pass

    sys.path.pop(0)

    return skills


def save_skills(bot, skills, data_file):

    """Save skill data to disk in a specified data file."""

    data = {}

    for skill_name, skill in skills.items():

        data[skill_name] = {attribute: getattr(skill, attribute)
            for attribute in dir(skill)
            if not callable(getattr(skill, attribute)) \
                and attribute[0] != "_" and getattr(skill, attribute) != bot}

    data_file = os.path.abspath(data_file)

    with open(data_file, "wb") as f:
        pickle.dump(data, f)


def run_skills(skills, message):

    """Run each of the skills using the last message as input."""

    for skill_name, skill in skills.items():

        [getattr(skill, method)(message) for method in dir(skill)
            if callable(getattr(skill, method)) and method[0] != "_"]

