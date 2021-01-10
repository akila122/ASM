from data_manipulation import fetch_and_write_csv, load_2018_dict, load_2019_dict, load_2020_dict, load_all_dict
from networks.build import build_and_write_all_networks


def main():
    fetch_and_write_csv()
    data_2018 = load_2018_dict()
    data_2019 = load_2019_dict()
    data_2020 = load_2020_dict()
    data_all = load_all_dict()
    build_and_write_all_networks(data_2018, data_2019, data_2020, data_all)


if __name__ == "__main__":
    main()
