import os

os.chdir(
    os.path.join(
        os.path.split(__file__)[0],
        "..",
    )
)
print(os.getcwd())
