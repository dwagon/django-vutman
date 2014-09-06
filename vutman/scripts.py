from vutman.models import EmailAlias
import os


def generate_vut_to_file(filename):
    "Generate the VUT file to the provided filename"
    tmp_filename = "%s.tmp" % filename
    expected_alias_count = EmailAlias.objects.all().count()
    print("Writing %d aliases out to %s" % (expected_alias_count, filename))
    written_count = 0
    alias_list = EmailAlias.objects.all().iterator()
    with open(tmp_filename, 'w') as output_fh:
        for alias in alias_list:
            written_count += 1
            output_fh.write("%s: %s@%s\n" %
                            (alias, alias.username,
                             alias.username.email_server))

    assert written_count == expected_alias_count
    assert os.path.exists(tmp_filename)
    os.popen("mv %s %s" % (tmp_filename, filename)).read()
    assert os.path.exists(filename)
    assert not os.path.exists(tmp_filename)
