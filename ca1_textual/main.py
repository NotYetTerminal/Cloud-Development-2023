import os
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Select, ListView, ListItem, Label


class SwimApp(App):


    data_dict: dict = {}
    list_view: ListView = None


    def compose(self) -> ComposeResult:
        data_dict = self.gather_files_informations()

        yield Select((key, value) for key, value in data_dict.items())
        self.list_view = ListView()
        yield self.list_view

    @on(Select.Changed)
    def change_list_view(self, event: Select.Changed) -> None:
        self.list_view.clear()
        print(event.value)
        self.list_view.extend((ListItem(Label(file_data))) for file_data in event.value)
        return


    def gather_files_informations(self) -> dict:
        """
        Returns a dictionary of all of the file names.
        Structure: Name - Age: [list of distances and types]
        """
        data_dict: dict = {}

        for file_name in os.listdir("ca1_textual/swimdata"):
            if ".txt" in file_name:
                name, age, distance, swim_type = file_name.replace(".txt", "").split("-")
                if f"{name} - {age}" in data_dict.keys():
                    data_dict[f"{name} - {age}"].append(f"{swim_type} - {distance}")
                else:
                    data_dict[f"{name} - {age}"] = [f"{swim_type} - {distance}"]
        
        data_dict = self.sort_dict_by_keys(data_dict)

        for key, value in data_dict.items():
            data_dict[key].sort()

        return data_dict
    

    def sort_dict_by_keys(self: object, old_dict: dict) -> dict:
        """
        Sorts a dictionary by the keys.
        """
        return {key: old_dict[key] for key in sorted(list(old_dict.keys()))}


def main() -> None:
    swim_app: SwimApp = SwimApp()
    swim_app.run()

    return



if __name__ == "__main__":
    main()
