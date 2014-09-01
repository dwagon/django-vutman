from vutman.models import EmailAlias


def generate_vut_to_file(filename):
    with open(filename, 'w') as output_fh:
        generate_vut_to_filehandle(output_fh)


def generate_vut_to_filehandle(output_fh):
    alias_list = EmailAlias.objects.all().iterator()
    for alias in alias_list:
        output_fh.write("%s: %s@%s\n"
                        % (alias, alias.username, alias.username.email_server))
