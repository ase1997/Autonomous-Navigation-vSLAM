import os

pth = "Examples/Stereo"
files = os.listdir(pth)
files = [os.path.join(pth, f) for f in files if ".cc" in f]

for f in files:
    with open(f, "r") as _f:
        content = _f.read()

    if "CV_LOAD_IMAGE_UNCHANGED" in content:
        print(f)
