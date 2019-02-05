Azure Pipeline to build and deploy packages and Code to AWS S3
----
The missing piece with all of this was being able to spin up a S3 bucket in an automated way. I've added some Azure magic to help do that.

The pipeline is defined in `azure-pipelines.yml` and there's additional `render_templates.py` code that takes environment variables from the Azure environment, and adds them to the munkipkg build files.

So - this builds and signs our packages - and clones and the copies all the relevant scripts to S3.

The pipeline also adds the correct dev or prod URL to the `Rolzog.sh` script - before moving everything to an S3 bucket using `aws s3 sync`

### Still to do...

For now this is only against the Dev bucket. Ideally I want to build DEV from a dev branch, and build PROD when that branch gets merged to Master.


Scripts/Packages deployed to laptops via InstallApplications
----

We're deploying some python scripts as root. Lots of these come from Erik Gomez's InstallApplications [demo](https://github.com/erikng/installapplicationsdemo)

### Scripts

* `Caffeinate.py` - prevents laptop sleep for 1200 seconds to allow the rest of the process to complete
* `high_sierra_vm_bless.py` - a script used in testing. Virtual machines crash after encryption unless the startup volume is set specifically using the `bless` command (this _isn't_ deployed to *real* laptops!)
* `Rolzog.sh` - run as the logged in user to trigger our Flask powered laptop registration web app.

### Packages

* Sophos Anti-Virus
* [DEPNotify](https://gitlab.com/Mactroll/DEPNotify)
* Notify - a lightweight Munki-pkg that delivers our custom icon to `/tmp` and sets up DEPNotify by echoing commands out to `/var/tmp/depnotify.log` during preinstall - then makes that file writeable by regular users during postinstall.
* Rolzog-Check - delivers a script and and a launchdaemon. Checks for a successful device registration process - and prompts the end user to reboot/quit accordingly.
