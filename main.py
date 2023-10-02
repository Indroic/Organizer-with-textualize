from pathlib import Path
from typing import Iterable
from textual.app import App, ComposeResult
from textual import Logger, on
from textual.events import Enter
from textual.widgets import Header, Footer, Button, Input, TabbedContent, TabPane, DirectoryTree, Select, Label, Log, Digits
from textual.containers import Vertical, Center, VerticalScroll, Horizontal
from organizer_api.file_handler import Filter, all_filters, FileCollector
from organizer_api.config_handler import Config








class FilteredDirectoryTree(DirectoryTree):
    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        return [path for path in paths if not "." in path.name and path.is_dir() ]
    
    def get_directory_selected(self):
        return self.path

class Main(App):
    
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        
        with TabbedContent(initial="organize"):
            with TabPane(title="Organize", id="organize"):
                with Vertical():
                    yield Center(Label("Organize Directory"), id="title")
                    
                    yield Label("Select Directory to Organize")
                    
                    yield Input(placeholder="Select a Directory or Write the Path", name="directory_input", id="directory_input")
                    
                    yield Label("Select Directory", id="directory_validate")
                    
                    yield FilteredDirectoryTree(path=Path.home(), id="directory_selection", name="directory_selection")
                    
                    yield Label("Select Filter")
                    
                    yield Select([(filter.name, filter) for filter in all_filters()], id="filters_select")
                    
                    yield Button(id="organize", label="Organize")
                   
                    
            with TabPane(title="Create Filter", id="create_filter"):
                yield Input()   
                Button(id="save_filter", label="Save")
                
        
        yield Footer()
    @on(Button.Pressed, "#organize")    
    def on_organize(self, event):
        directory = self.query_one("#directory_input", Input).value
        filter = self.query_one("#filters_select", Select).value
        FileCollector(directory, filter).move()

            
            
        
    @on(FilteredDirectoryTree.DirectorySelected)
    def directory_validate(self, event: FilteredDirectoryTree.DirectorySelected):
        input = self.query_one("#directory_input", Input)
        directory = str(event.path.absolute())
        input.value = directory
        

        
        
        
    
    def action_toggle_dark(self) -> None:
        self.dark = not self.dark
    
    
if __name__ == "__main__":
    app = Main()
    app.run()