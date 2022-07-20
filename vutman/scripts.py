import os
from vutman.models import EmailAlias


def generate_vut_to_file(filename):
    "Generate the VUT file to the provided filename"
    tmp_filename = f"{filename}.tmp"
    expected_alias_count = EmailAlias.objects.all().count()
    # print("Writing %d aliases out to %s" % (expected_alias_count, filename))
    written_count = 0
    alias_list = EmailAlias.objects.all().iterator()
    with open(tmp_filename, "w", encoding="utf-8") as output_fh:
        for alias in alias_list:
            written_count += 1
            output_fh.write(
                f"{alias}: {alias.username}@{alias.username.email_server}\n"
            )

    assert written_count == expected_alias_count
    assert os.path.exists(tmp_filename)
    os.popen(f"mv {tmp_filename} {filename}").read()
    assert os.path.exists(filename)
    assert not os.path.exists(tmp_filename)
