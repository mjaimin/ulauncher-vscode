import subprocess
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.action.OpenAction import OpenAction
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

class OpenFileInGvimExtension(Extension):

    def __init__(self):
        super(OpenFileInGvimExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []
        query = event.get_argument() or ""
        
        # Adjust this command to search for files. This is a placeholder.
        # You might want to use something like `find` or `fd` for better performance.
        try:
            files = subprocess.check_output(["find", extension.preferences['file_path'], "-iname", f"*{query}*"]).decode().split('\n')
        except Exception as e:
            files = [str(e)]
        
        for file in files:
            if file:
                items.append(ExtensionResultItem(icon='images/icon.png',
                                                 name=file,
                                                 description='Open this file in GVim',
                                                 on_enter=OpenAction(f'gvim "{file}"')))
        
        return RenderResultListAction(items)

if __name__ == '__main__':
    OpenFileInGvimExtension().run()
