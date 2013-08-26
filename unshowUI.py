import wx
import os
import uncconfUI
import uncpathConnect
from confProvider import *
     
class UncPathFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, id = -1, title = "Unc Path Quicker", style=wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU, size=(480,300))
        self.scroll = wx.ScrolledWindow(self, -1)
        self.scroll.SetScrollbars(1, 1, 1560, 600)
        self.SetBackgroundColour("white")
         #First create the controls
        topLabel = wx.StaticText(self.scroll, -1, "Unc Path List", size = (300,25))
        topLabel.SetFont(wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.BOLD))
        topLabel.SetForegroundColour('red')
        self.addButton = wx.Button(self.scroll, -1, "Add", size = (-1,30))
        self.Bind(wx.EVT_BUTTON, self.onAddClick, self.addButton)

        topSizer = wx.BoxSizer(wx.HORIZONTAL)

        topSizer.Add(topLabel)
        topSizer.Add((60, -1),1)
        topSizer.Add(self.addButton)

        self.configProvider = ConfigProvider()
        self.uncPathString = []
        self.uncPathEditButton = []
        self.uncPathLinkButton = []
        self.uncPathDeleteButton = []
        
        self.uncPathSizer = wx.FlexGridSizer(cols = 4, hgap = 10, vgap = 10) 
        self.uncPathShowString = self.configProvider.getAllUncPathShowString()
        
        if len(self.uncPathShowString) == 0:
            self.noConfText = wx.StaticText(self.scroll, -1, "No Unc Path now...", size = (300,25))
            self.noConfText.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL,wx.NORMAL))
            self.noConfText.SetForegroundColour('blue')
            self.uncPathSizer.Add(self.noConfText)
        else:
            for i in range(len(self.uncPathShowString)):
                self.uncPathString.append(wx.StaticText(self.scroll, -1,
                                                    self.uncPathShowString[i],
                                                    size = (300,25)))
                self.uncPathString[i].SetFont(wx.Font(14, wx.SWISS, wx.NORMAL,wx.BOLD))
                self.uncPathString[i].SetForegroundColour('blue')
                self.uncPathEditButton.append(wx.Button(self.scroll, -1, "Edit", size =(40,25)))
                self.uncPathLinkButton.append(wx.Button(self.scroll, -1, "Link", size =(40,25)))
                self.uncPathDeleteButton.append(wx.Button(self.scroll, -1, "Del", size =(40,25)))
                self.uncPathSizer.AddMany([self.uncPathString[i], self.uncPathLinkButton[i],
                                 self.uncPathEditButton[i], self.uncPathDeleteButton[i]])
                self.Bind(wx.EVT_BUTTON, self.onLinkClick, self.uncPathLinkButton[i])
                self.Bind(wx.EVT_BUTTON, self.onEditClick, self.uncPathEditButton[i])
                self.Bind(wx.EVT_BUTTON, self.onDeleteClick, self.uncPathDeleteButton[i])

                #if the mouse is in the "Link" button, show the unc path information
                self.Bind(wx.EVT_ENTER_WINDOW, self.onLinkMouseTouch, self.uncPathLinkButton[i])
            
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.mainSizer.Add(topSizer, 0, wx.ALL, 5)
        self.mainSizer.Add(wx.StaticLine(self.scroll), 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
        self.mainSizer.Add(self.uncPathSizer, 0, wx.EXPAND|wx.ALL, 10)
        self.scroll.SetSizer(self.mainSizer)

    def onLinkClick(self, event):
        for i in range(len(self.uncPathLinkButton)):
            if self.uncPathLinkButton[i].GetId() == event.GetId():
                uncPathStruct = self.configProvider.getSingleUncPath(self.uncPathShowString[i])
                if len(uncPathStruct) <= 2:
                    uncpathConnect.UncConnect(uncPathStruct[1])
                else:
                    uncpathConnect.UncConnect(uncPathStruct[1], uncPathStruct[2], uncPathStruct[3])
                break
    def onEditClick(self, event):
        for i in range(len(self.uncPathEditButton)):
            if self.uncPathEditButton[i].GetId() == event.GetId():
                uncPathStruct = self.configProvider.getSingleUncPath(self.uncPathShowString[i])
                if len(uncPathStruct) <= 2:
                    frame = uncconfUI.UncPathUpdateFrame(self, self.configProvider, uncPathStruct[0], uncPathStruct[1])
                else:
                    frame = uncconfUI.UncPathUpdateFrame(self,self.configProvider, uncPathStruct[0], uncPathStruct[1], uncPathStruct[2], uncPathStruct[3])
                frame.Show()
                break
    def onDeleteClick(self, event):
        for i in range(len(self.uncPathDeleteButton)):
            if self.uncPathDeleteButton[i].GetId() == event.GetId():
                self.configProvider.delete(self.uncPathShowString[i])
                self.buildUncPathUI()
                break
    def onAddClick(self, event):
        frame = uncconfUI.UncPathUpdateFrame(self, self.configProvider)
        frame.Show()

    def onLinkMouseTouch(self, event):
        for i in range(len(self.uncPathLinkButton)):
            if self.uncPathLinkButton[i].GetId() == event.GetId():
                uncPath = self.configProvider.getSingleUncPath(self.uncPathShowString[i])[1]
                pos = evt.GetPosition()
                
    def buildUncPathUI(self):
        if len(self.uncPathShowString) == 0:
            self.uncPathSizer.Detach(self.noConfText)
            self.noConfText.Destroy()
        else:
            for i in range(len(self.uncPathShowString)):      
                self.uncPathSizer.Detach(self.uncPathDeleteButton[i])
                self.uncPathSizer.Detach(self.uncPathLinkButton[i])
                self.uncPathSizer.Detach(self.uncPathEditButton[i])
                self.uncPathSizer.Detach(self.uncPathString[i])
                                  
                self.uncPathDeleteButton[i].Destroy()
                self.uncPathLinkButton[i].Destroy()
                self.uncPathEditButton[i].Destroy()
                self.uncPathString[i].Destroy()

        self.uncPathString = []
        self.uncPathDeleteButton = []
        self.uncPathEditButton = []
        self.uncPathLinkButton = []
        
        self.uncPathShowString = self.configProvider.getAllUncPathShowString()

        if len(self.uncPathShowString) == 0:
            self.noConfText = wx.StaticText(self.scroll, -1, "No Unc Path now...", size = (300,25))
            self.noConfText.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL,wx.NORMAL))
            self.noConfText.SetForegroundColour('blue')
            self.uncPathSizer.Add(self.noConfText)
        else:
            
            for i in range(len(self.uncPathShowString)):
                self.uncPathString.append(wx.StaticText(self.scroll, -1, self.uncPathShowString[i], size = (300,25)))
                self.uncPathString[i].SetFont(wx.Font(14, wx.SWISS, wx.NORMAL,wx.BOLD))
                self.uncPathString[i].SetForegroundColour('blue')
                self.uncPathEditButton.append(wx.Button(self.scroll, -1, "Edit", size =(40,25)))
                self.uncPathLinkButton.append(wx.Button(self.scroll, -1, "Link", size =(40,25)))
                self.uncPathDeleteButton.append(wx.Button(self.scroll, -1, "Del", size =(40,25)))
                self.uncPathSizer.AddMany([self.uncPathString[i], self.uncPathLinkButton[i],
                                 self.uncPathEditButton[i], self.uncPathDeleteButton[i]])
                self.Bind(wx.EVT_BUTTON, self.onLinkClick, self.uncPathLinkButton[i])
                self.Bind(wx.EVT_BUTTON, self.onEditClick, self.uncPathEditButton[i])
                self.Bind(wx.EVT_BUTTON, self.onDeleteClick, self.uncPathDeleteButton[i])   
        self.uncPathSizer.Layout()
        
if __name__ == '__main__':
    app = wx.App(False)
    frame = UncPathFrame()
    frame.Show()
    app.MainLoop()
