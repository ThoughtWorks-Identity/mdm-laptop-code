import os
import jinja2

rolzog_dev_url = os.environ.get("ROLZOG_DEV_URL")
rozlog_prod_url = os.environ.get("ROLZOG_PROD_URL")

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

def render_rolzog_template(rolzog_url, rolzog_dir, output_file_name):
    values = {"rolzog_url": rolzog_url}
    working_directory = rolzog_dir
    template_file = "Rolzog.template"
    output_file = working_directory + output_file_name
    templater(working_directory, template_file, values, output_file)

#create a dictionary of find/replaces - feed that into your function, and add code to unpack your dictionary and feed it into your template

# so we'd feed stage and signing id into the packages?
# and we'd feed the URL into the Rolzog.sh file...

def main():
    current_dir = os.getcwd()
    munki_pkg_path = current_dir + "/munki_pkgs"
    os.chdir(munki_pkg_path)
    packages = next(os.walk('.'))[1]
    render_package_templates(packages)

    rolzog_dir = os.chdir(current_dir + "/user_scripts")
    render_rolzog_template(rolzog_dev_url, rolzog_dir, "Dev-Rolzog.sh")
    render_rolzog_template(rolzog_prod_url, rolzog_dir, "Prod-Rolzog.sh")



if __name__ == "__main__":
    main()
