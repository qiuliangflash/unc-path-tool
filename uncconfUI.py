import wx

class UncPathUpdateFrame(wx.Frame):
    def __init__(self, parent, configProvider, uncPathShowString = None, uncPath = None, username=None, password = None):
        if uncPathShowString == None:
            wx.Frame.__init__(self, None, id=-1, title="",
                         style=wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU, size=(350, 220))
        else:
            wx.Frame.__init__(self, None, id=-1, title=uncPathShowString,
                         style=wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU, size=(350, 220))

        self.parent = parent
        self.uncPathShowString = uncPathShowString
        self.configProvider = configProvider
        
        panel = wx.Panel(self, -1)
        
        showNameLabel = wx.StaticText(panel, -1, "Unc Path Name:")
        self.showNameText = wx.TextCtrl(panel, -1, uncPathShowString if uncPathShowString != None else "", size=(200, -1))

        uncPathLabel = wx.StaticText(panel, -1, "Unc Path:")
        self.uncPathText = wx.TextCtrl(panel, -1, uncPath if uncPath != None else "", size=(200, -1))
        
        usernameLabel = wx.StaticText(panel, -1, "Username:")
        self.usernameText = wx.TextCtrl(panel, -1, username if username != None else "", size=(200, -1))
            
        passwordLabel = wx.StaticText(panel, -1, "Password:")
        rePasswordLabel = wx.StaticText(panel, -1, "Press Password Again:")
        
        self.passwordText = wx.TextCtrl(panel, -1, password if password != None else "", size=(200, -1), style = wx.TE_PASSWORD)
        self.rePasswordText = wx.TextCtrl(panel, -1, password if password != None else "", size=(200, -1), style = wx.TE_PASSWORD)
              
        confSizer = wx.FlexGridSizer(cols= 2, hgap = 6, vgap = 6)
        confSizer.AddMany([showNameLabel, self.showNameText, uncPathLabel, self.uncPathText, usernameLabel, self.usernameText, passwordLabel, self.passwordText, rePasswordLabel, self.rePasswordText])
    
        saveButton = wx.Button(panel, -1, "Save",size=(100,-1))
        cancelButton = wx.Button(panel, -1, "Cancel",size=(100,-1))

        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer.Add((20,20),1)
        buttonSizer.Add(saveButton)
        buttonSizer.Add((20,20),1)
        buttonSizer.Add(cancelButton)
        buttonSizer.Add((20,20),1)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(confSizer, 0, wx.EXPAND|wx.ALL,10)
        sizer.Add(buttonSizer, 0, wx.EXPAND|wx.BOTTOM,10)
        panel.SetSizer(sizer)

        #Bind button event function
        self.Bind(wx.EVT_BUTTON, self.onSave, saveButton)
        self.Bind(wx.EVT_BUTTON, self.onCancel, cancelButton)

    def onSave(self, event):
        if self.uncPathShowString != self.showNameText.GetValue() and self.configProvider.hasUncPathShowName(self.showNameText.GetValue()):  
            wx.MessageBox('This Unc Path Name has in conf files!', "Duplicate Error", wx.YES_NO | wx.ICON_ERROR)
            return
        if self.passwordText.GetValue() != self.rePasswordText.GetValue():
            wx.MessageBox('Two password is different!', "Password Different Error", wx.YES_NO | wx.ICON_ERROR)
            return
        if self.uncPathShowString != self.showNameText.GetValue():
            self.configProvider.update((self.showNameText.GetValue(),
                                    self.uncPathText.GetValue(),
                                    self.usernameText.GetValue(),
                                    self.passwordText.GetValue()),
                                    self.uncPathShowString)

        self.parent.buildUncPathUI()
        
        self.Destroy()
    def onCancel(self, event):
        pass

