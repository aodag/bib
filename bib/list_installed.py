from distlib.database import DistributionPath


def list_installed():
    dist_path = DistributionPath()

    for dist in dist_path.get_distributions():
        print(dist)


if __name__ == '__main__':
    list_installed()
