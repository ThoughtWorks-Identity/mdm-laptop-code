import os
import jinja2

def templater(working_directory, template_file, values, output_file):
    print("----")
    templateLoader = jinja2.FileSystemLoader(searchpath=working_directory)
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(template_file)
    outputfile = open(output_file, 'w+')
    complete = template.render(values)
    outputfile.write(complete)
    outputfile.close()

def render_package_templates(packages):
    for package in packages:
        values = {"signing_id": os.environ.get("SIGNING_ID")}
        working_directory = package
        template_file = "build-info.template"
        output_file = working_directory + "/build-info.plist"
        templater(working_directory, template_file, values, output_file)


def main():
    current_dir = os.getcwd()

    #Render MunkiPkg build-info templates (effectively just adding a signing ID)
    munki_pkg_path = current_dir + "/munki_pkgs"
    os.chdir(munki_pkg_path)
    packages = next(os.walk('.'))[1]
    render_package_templates(packages)

    #Render Rolzog scripts for DEV and PROD
    scripts_dir = current_dir + "/user_scripts"
    rolzog_dev = {"url": os.environ.get("ROLZOG_DEV_URL")}
    rolzog_prod = {"url": os.environ.get("ROLZOG_PROD_URL")}
    templater(scripts_dir, "Rolzog.template", rolzog_dev, scripts_dir+"/"+"Dev-Rolzog.sh")
    templater(scripts_dir, "Rolzog.template", rolzog_prod, scripts_dir+"/"+"Prod-Rolzog.sh")

    #Render logging templates
    working_dir = munki_pkg_path + "/LoggingFrameworkDEV/payload/tmp"
    log_dev_values = {"host": os.environ.get("LOGGING_HOST"), "logging_dev_url": os.environ.get("LOGGING_DEV_URL")}
#    log_prod_values = {"host": os.environ.get("LOGGING_HOST"), "logging_dev_url": os.environ.get("LOGGING_PROD_URL")}
    templater(working_dir, "logtoSumo.py", log_dev_values, working_dir+"/"+"logtoSumo.py")
#    templater(scripts_dir, "logtoSumo.template", log_prod_values, scripts_dir+"/"+"Prod-logtoSumo.py")



if __name__ == "__main__":
    main()
