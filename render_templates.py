import os
import jinja2



def templater(working_directory, template_file, values, output_file):
    templateLoader = jinja2.FileSystemLoader(searchpath=working_directory)
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(template_file)
    outputfile = open(output_file, 'w+')
    complete = template.render(values)
    outputfile.write(complete)
    outputfile.close()

#create a dictionary of find/replaces - feed that into your function, and add code to unpack your dictionary and feed it into your template

# so we'd feed stage and signing id into the packages?
# and we'd feed the URL into the Rolzog.sh file...

def main():
    current_dir = os.getcwd()
    print(current_dir)
    munki_pkg_path = current_dir + "/munki_pkgs"
    print(munki_pkg_path)
    os.chdir(munki_pkg_path)
    packages = next(os.walk('.'))[1]
    for package in packages:
        values = {"signing_id": os.environ.get("SIGNING_ID"), "stage": os.environ.get("STAGE")}
        working_directory = package
        template_file = "build-info.template"
        output_file = working_directory + "/build-info.plist"
        templater(working_directory, template_file, values, output_file)

    os.chdir(current_dir + "/user_scripts")
    print(os.getcwd())
    values = {"rolzog_url": os.environ.get("ROLZOG_URL")}
    working_directory = "."
    template_file = "Rolzog.template"
    output_file = working_directory + "/Rolzog.sh"
    templater(working_directory, template_file, values, output_file)








if __name__ == "__main__":
    main()
