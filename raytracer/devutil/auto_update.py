
import datetime
import glob
import os
import re
import shutil
import subprocess
import sys
import time
import unittest
import colorama

"""Script to automate update procedure. Checks for PEP8 compliance, runs
unit tests, generates documentation using Sphinx, updates GIT repository.

As well as Sphinx, this script requires autoep8 and the colorama module.
"""

colorama.init()

# Get all the required paths
auto_update_full_filepath = os.path.abspath(__file__)

# base_dir is the main project directory
base_dir = auto_update_full_filepath[
    :auto_update_full_filepath.find('devutil')]

python_executable = sys.executable
if '.exe' in python_executable:
    python_executable = python_executable[:-3]

# python_dir is the directory of the python executable
python_dir = python_executable[:python_executable.rfind(os.sep) + 1]

# script_dir is the directory python scripts such as pep8, autopep8, and
# the Sphinx executables are
script_dir = os.path.join(python_dir, "Scripts")

# unit_test_dir is the path to the unit tests
unit_test_dir = os.path.join(base_dir, "unit_tests")

# doc_dir is the path for project docmentation
doc_dir = os.path.join(base_dir, "docs")

# results in ../ or ..\ depending system
par_dir = os.path.join(os.pardir, "")

# results in .// or .\\ depending system
cur_dir = os.path.join(os.curdir, "")

sys.path.insert(0, base_dir)
sys.path.insert(0, script_dir)
sys.path.insert(0, unit_test_dir)
sys.path.insert(0, doc_dir)

# git_executable is the path to the git executable
os.chdir(base_dir)
git_executable = os.path.join(python_dir[0] + ":\\",
                              'git', 'cmd', 'git') + " "

git_executable = "C:\\Users\\jack-2\\AppData\\Local\\Programs\\git\\bin\\git"


def check_pep8():
    """Runs the PEP8 style checker.

    :return: True if no formatting problems, else False"""
    pep8_result =\
        subprocess.run(
            "%s %s" % (os.path.join(script_dir, "pep8"), cur_dir))

    pep8_pass = (pep8_result.returncode == 0)

    return pep8_pass


def get_repo_branches():
    """Retrieves git respository branch information"""
    print("%s%s\r\nChecking respository branches ...\r\n" %
          (colorama.Fore.BLUE, colorama.Style.BRIGHT))
    print(colorama.Style.RESET_ALL)
    os.chdir(base_dir)
    branch_result = subprocess.run("%s branch" % (git_executable),
                                   stdout=subprocess.PIPE)
    if branch_result.returncode > 0:
        return "Failed to fetch current repository branches"

    branches = branch_result.stdout.decode('utf-8').split('\n')
    branch_list = []
    current_branch = None
    for branch in branches:
        branch = branch.strip()
        if len(branch) > 0 and branch[0] == "*":
            branch = branch[2:]
            current_branch = branch
        print(branch)
        if len(branch) > 0:
            branch_list.append(branch)

    branch_list.sort()
    return {'branches': branch_list, 'current': current_branch}


def update_git_repo(current_branch):
    # https://www.git-tower.com/blog/git-cheat-sheet/

    print("%s%s\r\nUpdating repository ...\r\n" %
          (colorama.Fore.BLUE, colorama.Style.BRIGHT))
    print(colorama.Style.RESET_ALL)

    print("%sStaging current changes ...%s" %
          (colorama.Style.BRIGHT, colorama.Style.RESET_ALL))
    stage_result = subprocess.run("%s add ." % (git_executable))
    if stage_result.returncode > 0:
        return "Failed to stage latest changes."

    print("%sCommitting changes ...%s" %
          (colorama.Style.BRIGHT, colorama.Style.RESET_ALL))

    msg = ''
    while msg.strip() == '':
        print("%s%s\r\nEnter a commit message. Use fullstop to indicate" %
              (colorama.Fore.BLUE, colorama.Style.BRIGHT) +
              "last line. Message cannot be blank.")
        print("%s%s" % (colorama.Fore.WHITE, colorama.Style.BRIGHT))

        done = False
        while not done:
            i = input()
            if i == '.':
                done = True
            msg = msg + i

    print("\r\n %s" % (colorama.Style.RESET_ALL))
    commit_result = subprocess.run('%s commit -m "%s"' %
                                   (git_executable, msg))
    if commit_result.returncode > 0:
        return "Failed to commit changes"

    print("%sChecking out local 'dev' branch ... %s" %
          (colorama.Style.BRIGHT, colorama.Style.RESET_ALL))
    checkout_result = subprocess.run("%s checkout dev" % (git_executable))
    if checkout_result.returncode > 0:
        return "Failed to checkout dev branch"

    print("%sMerging '%s' branch into 'dev' branch ...%s" %
          (colorama.Style.BRIGHT, current_branch, colorama.Style.RESET_ALL))
    merge_result = subprocess.run("%s merge %s" %
                                  (git_executable, current_branch))
    if merge_result.returncode > 0:
        return "Failed to merge '%s' branch into 'dev' branch" %\
               (current_branch)
        # TODO: add optional merge abort

    input_understood = False
    while not input_understood:
        msg = "%s\r\nWould you like to push 'dev' branch to origin? [n]: %s" %\
            (colorama.Style.BRIGHT, colorama.Style.RESET_ALL)

        print(msg, end="")
        push_input = input().strip().lower()
        if push_input == "":
            push_input == "n"

        if push_input == "y" or push_input == "n":
            input_understood = True
    print("\r\n")
    do_push = push_input == 'y'
    if do_push:
        print("%sPushing 'dev' branch to origin ...%s" %
              (colorama.Style.BRIGHT, colorama.Style.RESET_ALL))
        merge_result = subprocess.run("%s push origin dev" % (git_executable))

    new_branch = datetime.datetime.now().strftime("%d.%m.%Y_%H.%M")
    print("%sCreating new '%s' branch with 'dev' branch as head ...%s" %
          (colorama.Style.BRIGHT, new_branch, colorama.Style.RESET_ALL))

    merge_result = subprocess.run("%s branch %s " %
                                  (git_executable, new_branch))
    if merge_result.returncode > 0:
        return "Failed to create '%s' branch" % (new_branch)

    print("%sChecking out local '%s' branch ... %s" %
          (colorama.Style.BRIGHT, new_branch, colorama.Style.RESET_ALL))
    checkout_result = subprocess.run("%s checkout %s" %
                                     (git_executable, new_branch))
    if checkout_result.returncode > 0:
        return "Failed to checkout %s branch" % (new_branch)

    print("%s%s\r\nGIT repository updated successfully.\r\n" %
          (colorama.Fore.GREEN, colorama.Style.BRIGHT))
    print(colorama.Style.RESET_ALL)

    return True


def update_sphinx_docs():
    regex_warn_err = re.compile(".*(warning|error).*", re.I)

    # Generate documentation
    print("%s%s\r\nGenerating documentation ...\r\n" %
          (colorama.Fore.BLUE, colorama.Style.BRIGHT))
    print(colorama.Style.RESET_ALL)

    # Copy Sphinx executables
    print("Copying Sphinx executables to project documentation directory ...")
    sphinx_files = glob.glob(os.path.join(script_dir, "sphinx*"))
    for file in sphinx_files:
        shutil.copy(file, doc_dir)

    # Remove former .rst files
    print("Removing previous .rst files ...")
    rst_files = glob.glob(os.path.join(doc_dir, "docs", "*.rst"))
    for file in rst_files:
        os.remove(file)

    print("Running sphinx-apidoc to generate fresh .rst files ...\r\n")
    os.chdir(doc_dir)

    sphinx_apidoc_result = subprocess.run('sphinx-apidoc -o %s %s' %
                                          (os.path.join("docs", ""),
                                           os.path.join(par_dir)),
                                          stderr=subprocess.PIPE)
    if sphinx_apidoc_result.stderr is not None:
        sphinx_apidoc_stderr = \
            sphinx_apidoc_result.stderr.decode('utf-8').split('\n')
        print("\r\n".join(sphinx_apidoc_stderr))

    if sphinx_apidoc_result.returncode > 0:
        return "Sphinx documentation build error"
    sphinx_apidoc_stderr = \
        sphinx_apidoc_result.stderr.decode('utf-8').split('\n')
    for line in sphinx_apidoc_stderr:
        err = regex_warn_err.search(line)
        if err is not None:
            return "sphinx-apidoc produced warnings or errors"

    print("\r\nRunning sphinx-build to generate HTML documentation ...\r\n")

    # TODO: check stdout for warnings
    sphinx_build_result = \
        subprocess.run(
            "sphinx-build -b html %s -c %s %s" %
            (cur_dir, os.path.join('source', ''),
             os.path.join('build', 'html', '')),
            stderr=subprocess.PIPE)

    sphinx_build_stderr = \
        sphinx_build_result.stderr.decode('utf-8').split('\n')
    print("\r\n".join(sphinx_build_stderr))

    if sphinx_build_result.returncode > 0:
        return "Sphinx documentation build error"

    ok_warnings = \
        ["modules.rst:: WARNING: document isn't included in any toctree",
         "index.rst:: WARNING: document isn't included in any toctree",
         "html_static_path entry",
         "toctree contains reference to nonexisting document 'modules'"]

    for line in sphinx_build_stderr:
        err = regex_warn_err.search(line)
        if err is not None:
            err_msg = err.group()
            warning_OK = False
            for warning in ok_warnings:
                if warning in err.group():
                    warning_OK = True

            if not warning_OK:
                return "sphinx-apidoc produced warnings or errors " + \
                       "that need to be fixed"

    print("Removing Sphinx executables from project " +
          "documentation directory ...")
    copied_sphinx_files = glob.glob(os.path.join(doc_dir, "sphinx*"))
    for file in copied_sphinx_files:
        os.remove(file)

    os.chdir(base_dir)
    return True


def auto_update():
    os.chdir(base_dir)

    # Check the repository branch is not dev or master
    branch_data = get_repo_branches()

    # import pdb; pdb.set_trace();

    if branch_data['current'] == 'dev' or branch_data['current'] == 'master':
        return "The current git repository branch is '%s'. " % \
            (branch_data['current'], "This script should not be run " +
             "over the master or dev branches directly")

    branch_data['branches'].remove('dev')
    branch_data['branches'].remove('master')

    branches = {}
    latest = (None, 0)
    for branch in branch_data['branches']:
        current = (branch == branch_data['current'])
        timestamp = time.mktime(datetime.datetime.strptime(
            branch, "%d.%m.%Y_%H.%M").timetuple())

        branches[branch] = (timestamp, current)
        if latest[1] < timestamp:
            latest = (branch, timestamp)

    # Check the branch name with the latest time is the current branch
    if not branches[latest[0]][1]:
        return "The current git repository branch does not match the " +\
               "latest repository branch."

    # check for PEP8 violations
    print("%s%s\r\nChecking for PEP8 formatting ...\r\n" %
          (colorama.Fore.BLUE, colorama.Style.BRIGHT))
    print(colorama.Style.RESET_ALL)

    pep8_pass = check_pep8()

    # If there are PEP8 Violations, try fixing them
    if not pep8_pass:
        pep8_pass = False

        print("%s%s\r\nPEP8 Violations found, running autopep8, %s" %
              ("may take 5-10 minutes \r\n",
               colorama.Fore.YELLOW, colorama.Style.BRIGHT))
        print(colorama.Style.RESET_ALL)

        # Attempt to fix PEP8 issues using autopep8
        os.system("%s%s%s" %
                  (os.path.join(script_dir, "autopep8 "),
                   cur_dir,
                   " --recursive --in-place --pep8-passes 100 --verbose"))
        # Recheck for PEP8 viloations

        print("%s%s\r\nRe-checking for PEP8 formatting ...\r\n" %
              (colorama.Fore.BLUE, colorama.Style.BRIGHT))
        print(colorama.Style.RESET_ALL)

        pep8_pass = check_pep8()

    if not pep8_pass:
        return "\r\nCode is not PEP8 formatted.\r\n"
    else:
        print(("%s%s\r\nPEP8 format check successful. \r\n ") %
              (colorama.Fore.GREEN, colorama.Style.BRIGHT))

    # Run unit tests

    print("%s%s\r\nRunning unit tests ...\r\n" %
          (colorama.Fore.BLUE, colorama.Style.BRIGHT))
    print(colorama.Style.RESET_ALL)

    suite = unittest.TestLoader().discover('unit_tests\\')
    unit_test_result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not unit_test_result.wasSuccessful():
        return "\r\nUnit tests failed.\r\n"
    else:
        print(("%s%s\r\nUnit tests ran successfully. \r\n ") %
              (colorama.Fore.GREEN, colorama.Style.BRIGHT))
        print(colorama.Style.RESET_ALL)

    sphinx_result = update_sphinx_docs()
    if sphinx_result is not True:
        return sphinx_result

    # Send to GitHub
    git_result = update_git_repo(branch_data['current'])

    return git_result

if __name__ == '__main__':
    result = auto_update()
    if result is not True:
        print("%s%s\r\n%s\r\n" %
              (colorama.Fore.RED, colorama.Style.BRIGHT, result))
        print(colorama.Style.RESET_ALL)
        sys.exit(1)
    else:
        print("%s%s\r\nUpdate successful\r\n" %
              (colorama.Fore.GREEN, colorama.Style.BRIGHT))
        print(colorama.Style.RESET_ALL)
        sys.exit(0)
