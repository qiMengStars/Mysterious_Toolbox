from typing import override

from win32more.Microsoft.UI.Xaml import FrameworkElement, Window
from win32more.Microsoft.UI.Xaml.Controls import Frame, NavigationView, NavigationViewItem, Page
from win32more.Microsoft.UI.Xaml.Markup import XamlReader
from win32more.Windows.UI.Xaml.Interop import TypeKind

from win32more.winui3 import XamlApplication, XamlType, xaml_typename

from pathlib import Path
from win32more.Microsoft.UI.Xaml import Application, Window
from win32more.Microsoft.UI.Xaml.Controls import Button,TextBlock,ComboBox,TextBox
from win32more.Microsoft.UI.Xaml.Markup import IComponentConnector
from win32more.Windows.Foundation import Uri

from win32more import ComClass

from win32more.winui3 import XamlApplication



import lib

import tkinter.messagebox as messagebox



with open('main.xaml', 'r',encoding='utf8') as f:
    xaml_window = f.read()
with open('simple.xaml', 'r',encoding='utf8') as f:
    xaml_home = f.read()
with open('about.xaml', 'r',encoding='utf8') as f:
    xaml_about=f.read()



class MainWindow(ComClass, Window, IComponentConnector):
    def __init__(self):
        super().__init__(own=True)
        self.InitializeComponent()

    def InitializeComponent(self):
        # ms-appx:///foo.xaml is relative to python.exe.
        # Use absolute path.
        # mx-appx:///C:/Full/Path/To/My.xaml
        # NOTE: According to documentation, LoadComponent() takes relative location.
        self.ExtendsContentIntoTitleBar=True
        
        xaml_path = Path(__file__).with_name("main.xaml").absolute().as_posix()
        resource_locator = Uri(f"ms-appx:///{xaml_path}")
        Application.LoadComponent(self, resource_locator)
    # def Connect(self, connectionId, target):
    #     print(connectionId, target)
    #     if connectionId == 1:
    #         self.Button1 = target.as_(Button)
    #         self.Button1.Click += self.Button1_Click
    #     elif connectionId == 2:
    #         self.Button2     = target.as_(Button)
    # def Button1_Click(self, sender, e):
    #     text = self.Button1.Content.as_(str)
    #     self.Button1.Content = f"[{text}]"
class App(XamlApplication):
    @override
    def OnLaunched(self, args):
        win = MainWindow()

        self.ContentFrame = win.Content.as_(FrameworkElement).FindName("ContentFrame").as_(Frame)

        self.NavView = win.Content.as_(FrameworkElement).FindName("NavView").as_(NavigationView)

        # Setup event handler
        self.NavView.SelectionChanged += self.NavView_SelectionChanged

        # Select first item
        self.NavView.SelectedItem = self.NavView.MenuItems[0]

        win.Activate()

    # Return XamlType for navigation.
    @override
    def GetXamlTypeByFullName(self, typename):
        if typename == "App.Simple":
            return XamlType("App.Simple", TypeKind.Custom, activate_instance=Home)
        elif typename == "App.Advanced":
            return XamlType("App.Advanced", TypeKind.Custom, activate_instance=Page2)
        elif typename == "App.About":
            return XamlType("App.About", TypeKind.Custom, activate_instance=lambda: XamlReader.Load(xaml_about))
        return super().GetXamlTypeByFullName(typename)

    def NavView_SelectionChanged(self, navigation_view, args):
        item = args.SelectedItem.as_(NavigationViewItem)
        typename = item.Tag.as_(str)

        # Navigate() implies GetXamlTypeByFullName() querying.
        self.ContentFrame.Navigate(xaml_typename(typename, TypeKind.Custom))


class Home(Page):
    def __init__(self):
        # Application.LoadComponent() should probably be used.
        super().__init__(move=XamlReader.Load(xaml_home))
        self.FindName("ConvertButton").as_(Button).Click += self.ConvertButton_Click
    def ConvertButton_Click(self, sender, e):
        print(1)
        from_combo=self.FindName("FromBaseCombo").as_(ComboBox).SelectedIndex
        to_combo=self.FindName("ToBaseCombo").as_(ComboBox).SelectedIndex
        from_combo_as_int=int(from_combo)+2
        to_combo_as_int=int(to_combo)+2
        input_text=self.FindName("InputBox").as_(TextBox).Text 

        try:
            if(int(input_text)<0):
                messagebox.showerror("错误","输入的数字不能小于0")
                return
            result=lib.convert_base(input_text,from_combo_as_int,to_combo_as_int)
        except Exception as e:
            messagebox.showerror("错误",str(e))
            result="错误"
        result_box=self.FindName("ResultBox").as_(TextBox)
        result_box.Text=str(result)

        
class Page2(Page):
    def __init__(self):
        # Application.LoadComponent() should probably be used.
        super().__init__(move=XamlReader.Load(xaml_home))
        self.FindName("ConvertButton").as_(Button).Click += self.ConvertButton_Click
        self.FindName("Title").as_(TextBlock).Text="进制转换-高级"
    def ConvertButton_Click(self, sender, e):
        print(1)
        from_combo=self.FindName("FromBaseCombo").as_(ComboBox).SelectedIndex
        to_combo=self.FindName("ToBaseCombo").as_(ComboBox).SelectedIndex
        from_combo_as_int=int(from_combo)+2
        to_combo_as_int=int(to_combo)+2
        input_text=self.FindName("InputBox").as_(TextBox).Text 

        try:
            result=lib.convert_base(input_text,from_combo_as_int,to_combo_as_int)
        except Exception as e:
            messagebox.showerror("错误",str(e))
            result="错误"
        result_box=self.FindName("ResultBox").as_(TextBox)
        result_box.Text=str(result)
    




XamlApplication.Start(App)
