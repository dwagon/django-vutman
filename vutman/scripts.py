from vutman.models import EmailAlias


def generate_vut_to_file(filename):
    "Generate the VUT file to the provided filename"
    alias_list = EmailAlias.objects.all().iterator()
    with open(filename, 'w') as output_fh:
        for alias in alias_list:
            output_fh.write("%s: %s@%s\n" %
                            (alias, alias.username,
                             alias.username.email_server))
