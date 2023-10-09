import os
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Select, ListView, ListItem, Label, Button
import swim_utils
import webbrowser

class SwimApp(App):


    data_dict: dict = {}
    list_view: ListView = None
    selected_person_name: str = ""
    complete_file_name: str = ""
    generate_button: Button = None


    def compose(self) -> ComposeResult:
        data_dict = self.gather_files_informations()
        yield Select((key, f"{key}:{value}") for key, value in data_dict.items())

        self.list_view = ListView()
        yield self.list_view

        self.generate_button = Button("Generate Chart!", disabled = True)
        yield self.generate_button


    @on(Select.Changed)
    def change_list_view(self, event: Select.Changed) -> None:
        self.list_view.clear()
        self.generate_button.disabled = True
        if event.value != None:
            self.selected_person_name = event.value.split(":")[0]
            correct_data: list = event.value.split(":")[1].replace("[", "").replace("]", "").replace("'", "").split(", ")
            self.list_view.extend((ListItem(Label(file_data))) for file_data in correct_data)
        return
    
    @on(ListView.Selected)
    def save_file_name(self, event: ListView.Selected) -> None:
        file_value: str = event.item.displayed_children[0].renderable.plain
        file_value = f"{file_value.split(' - ')[1]} - {file_value.split(' - ')[0]}"
        self.complete_file_name: str = f"{self.selected_person_name}-{file_value}".replace(" ", "") + ".txt"
        self.generate_button.disabled = False
        return

    @on(Button.Pressed)
    def generate_chart(self, event: Button.Pressed) -> None:
        name, age, distance, stroke, times, converts, average = swim_utils.get_swimmers_data(self.complete_file_name)

        file_header: str = f"""<!DOCTYPE html>
<html>
    <head>
        <title>
            {name} (Under {age}) {distance} - {stroke}
        </title>
    </head>
    <body>
        <h3>{name} (Under {age}) {distance} - {stroke}</h3>"""


        file_footer: str = f"""<p>Average: {average}</p>
    </body>
</html>
        """

        with open(f"ca1_textual/charts/{name}-{age}-{distance}-{stroke}-Chart.html", "w+") as f:
            f.write(file_header)

            for time, convert in zip(times, converts):
                file_body: str = f"""
                <svg height="30" width="400">
                        <rect height="30" width="{swim_utils.convert2range(convert, min(converts) - 100, max(converts) + 100, 0, 400)}" style="fill:rgb(0,0,255);" />
                </svg>{time}<br />
"""
                f.write(file_body)

            f.write(file_footer)

        webbrowser.open(f"ca1_textual/charts/{name}-{age}-{distance}-{stroke}-Chart.html")
        return



    def gather_files_informations(self) -> dict:
        """
        Returns a dictionary of all of the file names.
        Structure: Name - Age: [list of distances and types]
        """
        data_dict: dict = {}

        for file_name in os.listdir(swim_utils.FOLDER):
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
