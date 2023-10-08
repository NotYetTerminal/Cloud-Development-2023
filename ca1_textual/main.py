import os
from textual.app import App


class SwimApp(App):
    pass


def gather_files_informations() -> dict:
    data_dict: dict = {}

    for file_name in os.listdir("ca1_textual/swimdata"):
        if ".txt" in file_name:
            name, age, distance, swim_type = file_name.replace(".txt", "").split("-")
            if f"{name}-{age}" in data_dict.keys():
                data_dict[f"{name}-{age}"].append((distance, swim_type))
            else:
                data_dict[f"{name}-{age}"] = [(distance, swim_type)]
    
    return data_dict


def main() -> None:
    data_dict: dict = gather_files_informations()
    
    swim_app: SwimApp = SwimApp()
    swim_app.run()

    return



if __name__ == "__main__":
    main()
