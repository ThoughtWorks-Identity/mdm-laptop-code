import os
import jinja2

rolzog_dev_url = os.environ.get("ROLZOG_DEV_URL")
rolzog_prod_url = os.environ.get("ROLZOG_PROD_URL")

logging_host = os.environ.get("LOGGING_HOST")



def templater(working_directory, template_file, values, output_file):
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

#def render_rolzog_template(rolzog_url, rolzog_dir, output_file_name):
#    values = {"rolzog_url": rolzog_url}
#    os.chdir(rolzog_dir)
#    working_directory = "."
#    template_file = "Rolzog.template"
#    output_file = working_directory + "/" + output_file_name + ".sh"
#    templater(working_directory, template_file, values, output_file)

#def render_script_template(url, scripts_dir, input_file_name, output_file_name):
#    values = {"url": url}
#    os.chdir(scripts_dir)
#    working_directory = "."
#    template_file = input_file_name
#    output_file = working_directory + "/" + output_file_name
#    templater(working_directory, template_file, values, output_file)

def main():
    current_dir = os.getcwd()
    munki_pkg_path = current_dir + "/munki_pkgs"
    os.chdir(munki_pkg_path)
    packages = next(os.walk('.'))[1]
    render_package_templates(packages)

    scripts_dir = current_dir + "/user_scripts"
    rolzog_dev = {"url": os.environ.get("ROLZOG_DEV_URL")}
    rolzog_prod = {"url": os.environ.get("ROLZOG_PROD_URL")}
    templater(scripts_dir, "Rolzog.template", rolzog_dev, "Dev-Rolzog.sh")
    templater(scripts_dir, "Rolzog.template", rolzog_prod, "Prod-Rolzog.sh")

    log_dev_values = {"host": os.environ.get("LOGGING_HOST"), "logging_dev_url": os.environ.get("LOGGING_DEV_URL")}
    log_prod_values = {"host": os.environ.get("LOGGING_HOST"), "logging_dev_url": os.environ.get("LOGGING_PROD_URL")}
    templater(scripts_dir, "logtoSumo.template", log_dev_values, "Dev-logtoSumo.py")
    templater(scripts_dir, "logtoSumo.template", log_prod_values, "Prod-logtoSumo.py")


    #render_script_template(rolzog_dev_url, scripts_dir, "Rolzog.template", "Dev-Rolzog.sh")
    #render_script_template(rolzog_prod_url, scripts_dir, "Rolzog.template", "Prod-Rolzog.sh")

    #render_script_template(logging_dev_url, scripts_dir, "logtoSumo.template", "Dev-logtoSumo.py")
    #render_script_template(logging_prod_url, scripts_dir, "logtoSumo.template", "Prod-logtoSumo.py")





if __name__ == "__main__":
    main()
