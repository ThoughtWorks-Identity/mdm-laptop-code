import subprocess
import sys
from sys import argv
import os
import time
import shutil
import platform

control_file = '/private/var/tmp/depnotify.log'
launchdpath = '/Library/LaunchDaemons/com.thoughtworks.rolzogcheck.plist'
launchdidentifier = 'com.thoughtworks.rolzogcheck'
checkscript = '/Library/Application Support/RolzogCheck/RolzogCheck.py'
directory = '/Library/Application Support/RolzogCheck/'

#Borrowed from Erik Gomez -
def depnotify(text, control_file):
    with open(control_file, 'a+') as depnotify:
        depnotify.write(text + '\n')

def tidy_up(control_file, launchdpath, launchdidentifier, checkscript, directory):

    try:
        os.remove(control_file)
    except:
        pass

    #remove launchdaemon
    try:
        os.remove(launchdpath)
    except:  # noqa
        pass

    #remove RolzogCheck script
    try:
        os.remove(checkscript)
    except:
        pass

    #Remove RolzogCheck folder
    try:
        shutil.rmtree(directory)
    except:  # noqa
        pass

    #unload LaunchD
    try:
        launchd_removal_command = ["launchctl","remove","com.thoughtworks.rolzogcheck"]
        subprocess.check_output(launchd_removal_command)
    except:
        pass


def encryption_status():
    """Three possible statuses - On, Off, or Off and Deferred"""
    fv_check_command = ['fdesetup','status']
    fv_status = subprocess.check_output(fv_check_command).strip()
    if "Deferred" in fv_status:
        return ("Deferred")
    elif "On" in fv_status:
        return("On")
    else:
        return("Off")


def number_of_simplemdm_profiles_installed():
    check_profiles = ["profiles","-C"]
    profiles = subprocess.check_output(check_profiles)
    return profiles.count("com.unwiredmdm")

def activate_window(control_file):
    activate_command = ("Command: WindowStyle: Activate")
    depnotify(activate_command, control_file)

def getOSVersion():
    """Return OS version."""
    return platform.mac_ver()[0]

def check_for_filevault_profile():
    """Use newer profiles syntax to check for existence of a
    filevault profile. Fall back to the older syntax if the newer
    command fails"""
    check_for_filevault_profile = ['profiles','show','-all']
    try:
        output = subprocess.check_output(check_for_filevault_profile)
        if "FileVault" in output:
            return True
    except:
        legacy_filevault_check = ['profiles','-C','-v']
        output = subprocess.check_output(legacy_filevault_check)
        if "FileVault" in output:
            return True
    return False

def notify(status="", activate=False, command="", tidy=False):
    if activate == True:
        activate_window(control_file)
    status = ("Status: {}".format(status))
    depnotify(status, control_file)
    if command != "":
        command = ("Command: {}".format(command))
        depnotify(command, control_file)
    if tidy == True:
        tidy_up(control_file, launchdpath, launchdidentifier, checkscript, directory)

def main():

    if (check_for_filevault_profile() == True and
            encryption_status() == "On"):
        notify(
            status="Setup/Registration Complete",
            activate=True,
            command="Quit: All done - thanks for registering this laptop with ThoughtWorks!",
            tidy=True
        )

    elif (check_for_filevault_profile() == True and
            encryption_status() == "Deferred"):
        notify(
            status="Setup/Registration Complete",
            activate=True,
            command="Logout: All done - Hit Logout to reboot and start the encryption process",
            tidy=True
        )

    else:
        status = ("Status: Registration not complete yet...")
        depnotify(status, control_file)

        #Scope to add additional checks/re-launch Rolzog here...


if __name__ == '__main__':
    main()