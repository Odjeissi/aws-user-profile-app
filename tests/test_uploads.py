from app import allowed_file


def test_allowed_file_accepts_valid_images():
    assert allowed_file("profile.jpg")
    assert allowed_file("profile.jpeg")
    assert allowed_file("profile.png")
    assert allowed_file("profile.gif")


def test_allowed_file_rejects_invalid_files():
    assert not allowed_file("malware.exe")
    assert not allowed_file("document.pdf")
    assert not allowed_file("noextension")
