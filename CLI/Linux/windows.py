import pytermgui as ptg
import time, json, crypto_cipher as c_r
from pynput.keyboard import Key, Controller

######################################################################
# COLORS #
##########

# green for the OK button - #32ba52 (label) #45ff70 (highlight)
# red for the CANCEL button - #c23232 (label) #ff4545 (highlight)

######################################################################

## Base of data ######################################################
# 
base = None
# 
######################################################################

class windowMenu():
    def __init__(self):
        self.key = c_r.load_key()
        # - initialization of window
        self.menu_window = ptg.Window()

        self.title = "[@#dec14e black bold] Password Manager"

        if base['datas'] == {}:
            # - if the data list is empty
            self.status_data = ptg.Label(" Tip: There is no data, try adding a new data block ")
            self.status_data.set_style("value", "[@lightblue black bold]{item}")

            for i in range(10):
                if i == 5:
                    self.menu_window.__add__(self.status_data)
                self.menu_window.__add__("")
        else:
            ## Display all data from the database ################################
            # 
            self.menu_window.__add__("")
            self.menu_window.__add__(ptg.Label("[@white black bold] Number " + "[@0] " + "[@#34507d white bold] Title " + "[@0] " + "[@#7d3434 white bold] Data ", parent_align=0))
            self.listOfData = ptg.Container() # a place to store data
            self.listOfData.set_style('border', '[#dec14e]{item}')
            self.listOfData.set_style('corner', '[#dec14e]{item}')
            self.listOfData.set_char("corner", ['╭─','─╮', '─╯', '╰─'])
            self.listOfData.height = 10
            self.listOfData.overflow = ptg.Overflow.SCROLL

            count = 1 # - start of count
            for key in base['datas']:
                self.listOfData.__add__(ptg.Label(f'[@white black bold] {count} ' + "[@0] " + f'[@#34507d white bold] {key} ' + "[@0] " + f'[@#7d3434 white bold] {" ".join(base["datas"][key])} ', parent_align=0)) # parent_align -- 1-(Center) 2-(Right) 3-(Left)
                self.listOfData.__add__(ptg.Label(""))
                count += 1
            self.menu_window.__add__(self.listOfData) 
            # 
            ######################################################################

        ## Buttons ###########################################################
        # 
        self.add_btn = ptg.Button(" Insert ", onclick=self.addBlockData)
        self.add_btn.set_style("label",'[@#32ba52 white]{item}')
        self.add_btn.set_style("highlight",'[@#45ff70 white bold]{item}')
        self.add_btn.on_release(self.add_btn)

        self.del_btn = ptg.Button(" Delete ", onclick=self.delBlockData)
        self.del_btn.set_style("label",'[@#ba3232 white]{item}')
        self.del_btn.set_style("highlight",'[@#ff4545 white bold]{item}')
        self.del_btn.on_release(self.del_btn)

        self.edit_btn = ptg.Button("  Edit  ", onclick=self.editBlockData)
        self.edit_btn.set_style("label", '[@#c26932 white]{item}')
        self.edit_btn.set_style("highlight", '[@#ff8c45 white bold]{item}')
        self.edit_btn.on_release(self.edit_btn)

        self.passGen_btn = ptg.Button("Password generator", onclick=self.passwordGenerator)
        self.passGen_btn.set_style("label", '[@#5b32c2 white]{item}')
        self.passGen_btn.set_style("highlight", '[@#9945ff white bold]{item}')
        self.passGen_btn.on_release(self.passGen_btn)

        self.exit_btn = ptg.Button("        Exit        ", onclick=self.ExitFromProgram)
        self.exit_btn.set_style("label", '[@#c23232 white]{item}')
        self.exit_btn.set_style("highlight", '[@#ff4545 white bold]{item}')
        self.exit_btn.on_release(self.exit_btn)
        # 
        ######################################################################

        ## Window properties #################################################
        # 
        # menu _______________________________________________________________

        self.menu = (self.add_btn, self.del_btn, self.edit_btn)
        self.menu_window.__add__("")
        self.menu_window.__add__(self.menu)
        self.menu_window.__add__("")
        self.menu_window.__add__((self.exit_btn, self.passGen_btn))

        # properties _________________________________________________________

        self.menu_window.center(0)
        self.menu_window.is_dirty = True
        self.menu_window.set_title(self.title)
        self.menu_window.width = 70
        self.menu_window.height = 18
        self.menu_window.min_width = 70
        # 
        ######################################################################

    ## Functions #########################################################
    # 
    # - finish the manager's work, exit the program
    def ExitFromProgram(self, _):
        c_r.encrypt('data.json', self.key)
        manager.stop()

    # - add a new data block to the database
    def addBlockData(self, _):
        manager.remove(self.menu_window)
        manager.add(windowAddBlock().block_window)

    # - edit a block of data from the database
    def editBlockData(self, _):
        def btnOk(_):
            manager.remove(dialogWindow)

        # - if there is no data, a dialog box with help
        if base['datas'] == {}:
            dialogWindow = ptg.Window()
            dialogWindow.center(0)

            btnOk = ptg.Button("    OK    ", onclick=btnOk)
            reference = ptg.Label("There is no data to delete.")

            dialogWindow.__add__(reference)
            dialogWindow.__add__("")
            dialogWindow.__add__(btnOk)
                
            manager.add(dialogWindow)
        # - if the data is available
        else:
            manager.remove(self.menu_window)
            manager.add(windowEditBlock().edit_window)

    # - deleting a block of data from the database
    def delBlockData(self, _):
        def btnOk(_):
            manager.remove(dialogWindow)

        # - if there is no data, a dialog box with help
        if base['datas'] == {}:
            dialogWindow = ptg.Window()
            dialogWindow.center(0)

            btnOk = ptg.Button("    OK    ", onclick=btnOk)
            reference = ptg.Label("There is no data to delete.")

            dialogWindow.__add__(reference)
            dialogWindow.__add__("")
            dialogWindow.__add__(btnOk)
            manager.add(dialogWindow)

        # - if the data is available
        else:
            manager.remove(self.menu_window)
            manager.add(windowDelBlock().del_window)
    
    # - generates a password
    def passwordGenerator(self, _):
        manager.remove(self.menu_window)
        manager.add(windowPasswordGenerator().passwordGenerator_window)
    # 
    ######################################################################

class windowPasswordGenerator(windowMenu):
    def __init__(self):
        # - initialization of window
        self.passwordGenerator_window = ptg.Window()
        self.passwordGenerator_window.center(0)
        self.passwordGenerator_window.set_title("[@white black bold] Password generator")
        self.passwordGenerator_window.width = 70
        self.passwordGenerator_window.height = 4
        self.passwordGenerator_window.min_width = 70

        ######################################################################
        # Containers 
        #
        self.fieldPasswordLength = ptg.Container()
        self.fieldPasswordLength.height = 3
        self.fieldPasswordLength.set_style('border', '[#dec14e]{item}')
        self.fieldPasswordLength.set_style('corner', '[#dec14e]{item}')
        self.fieldPasswordLength.set_char("corner", ['╭─','─╮', '─╯', '╰─'])
        self.fieldPasswordLength.set_char('border', ['│ ', '─', ' │', '─'])
        self.fieldPasswordLength.overflow = ptg.Overflow.SCROLL

        self.titleFieldNewPassword = ptg.Label("There is no new password.")
        self.titleFieldNewPassword.set_style("label", "[@white black bold]{item}")

        self.btn_cancel = ptg.Button("Cancel", onclick=self.on_cancel)
        self.btn_cancel.set_style('label', '[@#c23232 white]{item}')
        self.btn_cancel.set_style('highlight', '[@#ff4545 white bold]{item}')
        self.btn_cancel.on_release(self.btn_cancel)

        self.fieldNewPassword = ptg.Container()
        self.fieldNewPassword.height = 3
        self.fieldNewPassword.set_style('border', '[#dec14e]{item}')
        self.fieldNewPassword.set_style('corner', '[#dec14e]{item}')
        self.fieldNewPassword.set_char("corner", ['╭─','─╮', '─╯', '╰─'])
        self.fieldNewPassword.set_char('border', ['│ ', '─', ' │', '─'])
        self.fieldNewPassword.overflow = ptg.Overflow.SCROLL
        # 
        ######################################################################

        self.lenghtPassword = ptg.InputField(prompt="Enter the password length: ")
        self.lenghtPassword.set_style("prompt", "[white bold]{item}")
        self.lenghtPassword.set_style("value", "[white]{item}")

    def generator(self, _):
        import random as rm
        symbols = '1234567890qwertyuiopasdfghjklzxcvbnm,./;\'[]{}- \
        =_+<>?"!@#$%^&*()\\|QAWSEDRFTGYHUJIKOLPZXCVBNM'
        new_password = "".join([symbols[rm.randint(0, len(symbols)-1)] for i in range(self.lenghtPassword.value)])
        self.titleFieldNewPassword.value = new_password
    
    def on_cancel(self, _):
        manager.remove(self.passwordGenerator_window)
        manager.add(windowMenu().menu_window)

class windowEditBlock(windowMenu):
    def __init__(self):
        # - initialization of window
        self.edit_window = ptg.Window()

        ######################################################################
        # - window to edit current block

        self.current_block = 0
        self.editing_specific_data_window = ptg.Window()
        self.editing_specific_data_window.center(0)
        self.editing_specific_data_window.set_title("[@white black bold] Editing a data block")
        self.editing_specific_data_window.width = 70
        self.editing_specific_data_window.height = 4
        self.editing_specific_data_window.min_width = 70

        self.btnOK = ptg.Button("    OK    ", onclick=self.on_edit_save)
        self.btnOK.set_style('label', '[@#32ba52 white]{item}')
        self.btnOK.set_style('highlight', '[@#45ff70 white bold]{item}')
        self.btnOK.on_release(self.btnOK)

        self.btnCancel = ptg.Button("  Cancel  ", onclick=self.on_cancel)
        self.btnCancel.set_style('label', '[@#c23232 white]{item}')
        self.btnCancel.set_style('highlight', '[@#ff4545 white bold]{item}')
        self.btnCancel.on_release(self.btnCancel)

            ######################################################################
            # Containers 
            # - for new title
        self.newTitleContainer = ptg.Container()
        self.newTitleContainer.height = 3
        self.newTitleContainer.set_style('border', '[#dec14e]{item}')
        self.newTitleContainer.set_style('corner', '[#dec14e]{item}')
        self.newTitleContainer.set_char("corner", ['╭─','─╮', '─╯', '╰─'])
        self.newTitleContainer.set_char('border', ['│ ', '─', ' │', '─'])
        self.newTitleContainer.overflow = ptg.Overflow.SCROLL

            # - for new title
        self.newDataContainer = ptg.Container()
        self.newDataContainer.height = 3
        self.newDataContainer.set_style('border', '[#dec14e]{item}')
        self.newDataContainer.set_style('corner', '[#dec14e]{item}')
        self.newDataContainer.set_char("corner", ['╭─','─╮', '─╯', '╰─'])
        self.newDataContainer.set_char('border', ['│ ', '─', ' │', '─'])
        self.newDataContainer.overflow = ptg.Overflow.SCROLL
            # 
            ######################################################################

        self.newTitle = ptg.InputField(prompt="New name for the block: ").set_style("value", "[white]{item}").set_style("prompt", "[white bold]{item}")
        self.newData = ptg.InputField(prompt="New data for the block: ").set_style("value", "[white]{item}").set_style("prompt", "[white bold]{item}")

        self.oldTitle = ptg.Label("")
        self.oldData = ptg.Label("")
        self.hint = ptg.Label("", parent_aling=1)

        self.newTitleContainer._add_widget(self.newTitle)
        self.newDataContainer._add_widget(self.newData)

        self.editing_specific_data_window.__add__(self.oldTitle)
        self.editing_specific_data_window.__add__(self.newTitleContainer)
        self.editing_specific_data_window.__add__(self.oldData)
        self.editing_specific_data_window.__add__(self.newDataContainer)
        self.editing_specific_data_window.__add__(self.hint)
        self.editing_specific_data_window.__add__("")
        self.editing_specific_data_window.__add__((self.btnOK, self.btnCancel))

        # - window to edit
        ######################################################################

        ## Display all data from the database ################################
        # 
        self.data_to_edit = ptg.Container() # a place to store data
        self.data_to_edit.set_style('border', '[#dec14e]{item}')
        self.data_to_edit.set_style('corner', '[#dec14e]{item}')
        self.data_to_edit.set_char("corner", ['╭─','─╮', '─╯', '╰─'])
        self.data_to_edit.set_char('border', ['│ ', '─', ' │', '─'])
        # - properties 
        self.data_to_edit.height = 10
        self.data_to_edit.overflow = ptg.Overflow.SCROLL
        count = 1 # - start of count
        for key in base['datas']:
            self.data_to_edit.__add__(ptg.Label(f'[@white black bold] {count} ' + "[@0] " + f'[@#34507d white bold] {key} ' + "[@0] " + f'[@#7d3434 white bold] {" ".join(base["datas"][key])} ', parent_align=0)) # parent_align -- 1-(Center) 2-(Right) 3-(Left)
            self.data_to_edit.__add__(ptg.Label(""))
            count += 1
        # 
        ######################################################################
            
        ## Attributes ########################################################
        # 
        self.NumOfDataToEdit = ptg.InputField(prompt="The number of data to edit: ")
        self.NumOfDataToEdit.set_style('prompt', '[white bold]{item}')

        self.btnEdit = ptg.Button("    Edit    ", onclick=self.on_edit)
        self.btnEdit.set_style("label", '[@#c26932 white]{item}')
        self.btnEdit.set_style("highlight", '[@#ff8c45 white bold]{item}')
        self.btnEdit.on_release(self.btnEdit)

        self.btnLeave = ptg.Button("   Cancel   ", onclick=self.on_leave)
        self.btnLeave.set_style('label', '[@#c23232 white]{item}')
        self.btnLeave.set_style('highlight', '[@#ff4545 white bold]{item}')
        self.btnLeave.on_release(self.btnLeave)

        self.NameHint = ptg.Label("[#90ee90 bold]Write down the data number to edit.",parent_align=1)
        #
        ######################################################################

        ## Window properties #################################################
        # 
        # menu _______________________________________________________________
        self.edit_window.__add__(self.data_to_edit) 
        self.edit_window.__add__(self.NameHint)
        self.edit_window.__add__("")
        self.edit_window.__add__(self.NumOfDataToEdit)
        self.edit_window.__add__("")
        self.edit_window.__add__((self.btnEdit, self.btnLeave))
        # properties _________________________________________________________
        self.edit_window.center(0)
        self.edit_window.set_title("[@white black bold] Editing a data block ")
        self.edit_window.width = 70
        self.edit_window.height = 18
        self.edit_window.min_width = 70
        # 
        ######################################################################
    
    ## Functions #########################################################
    # 
    def on_cancel(self, _):
        manager.remove(self.editing_specific_data_window)
        manager.add(windowMenu().menu_window)    

    def on_edit_save(self, _):
        if self.newTitle.value == "" and self.newData.value == "":
            manager.remove(self.editing_specific_data_window)
            manager.add(windowMenu().menu_window)
        elif self.newTitle.value and not(self.newData.value):
            count = 1 # - start of count
            for key in base['datas']:
                if self.current_block == count:
                    data_of_old_key = base['datas'][key]
                    del base['datas'][key]
                    base['datas'][self.newTitle.value.strip()] = data_of_old_key
                    with open('data.json', 'w') as file:
                        json.dump(base, file)
                    break
                count += 1
            manager.remove(self.editing_specific_data_window)
            manager.add(windowMenu().menu_window)
        elif not(self.newTitle.value) and self.newData.value:
            count = 1 # - start of count
            for key in base['datas']:
                if self.current_block == count:
                    base['datas'][key] = self.newData.value.strip().split()
                    with open('data.json', 'w') as file:
                        json.dump(base, file)
                    break
                count += 1
            manager.remove(self.editing_specific_data_window)
            manager.add(windowMenu().menu_window)
        else:
            count = 1 # - start of count
            for key in base['datas']:
                if self.current_block == count:
                    del base['datas'][key]
                    base['datas'][self.newTitle.value] = self.newData.value.strip().split()
                    with open('data.json', 'w') as file:
                        json.dump(base, file)
                    break
                count += 1
            manager.remove(self.editing_specific_data_window)
            manager.add(windowMenu().menu_window)

    def on_edit(self, _):
        try:
            if self.NumOfDataToEdit.value:
                old_title = ""
                old_data = ""
                count = 1 # - start of count
                # - old values and fix them
                for key in base['datas']:
                    if int(self.NumOfDataToEdit.value.strip()) == count:
                        old_title = key
                        old_data = base['datas'][key]
                        break
                    count += 1
                self.current_block = count
                if old_title:
                    # - fix them
                    self.oldTitle.value = "[@#10b33c white] Old version " + "[@0] " + f'[@0 white bold]{old_title}'
                    self.oldTitle.parent_align = 0
                    self.oldData.value = "[@#10b33c white] Old version " + "[@0] " + f'[@0 white bold]{" ".join(old_data)}'
                    self.oldData.parent_align = 0
                    # - fix them
                    manager.remove(self.edit_window)
                    manager.add(self.editing_specific_data_window)
                else:
                    self.NameHint.value = "[@1 white bold] Unavailable values for the block number "
                    time.sleep(1)
                    self.NameHint.value = '[#90ee90 bold]Write down the data number to edit.'
            else:
                self.NameHint.value = "[@1 white bold] Unavailable values for the block number "
                time.sleep(1)
                self.NameHint.value = '[#90ee90 bold]Write down the data number to edit.'
        except TypeError:
            self.NameHint.value = "[@1 white bold] Unavailable values for the block number "
            time.sleep(1)
            self.NameHint.value = '[#90ee90 bold]Write down the data number to edit.'

    def on_leave(self, _):
        manager.remove(self.edit_window)
        manager.add(windowMenu().menu_window)
    # 
    ######################################################################

class windowDelBlock(windowMenu):
    def __init__(self):
        # - initialization of window
        self.del_window = ptg.Window()

        ## Display all data from the database ################################
        # 
        self.data_to_delete = ptg.Container() # a place to store data
        self.data_to_delete.set_style('border', '[#dec14e]{item}')
        self.data_to_delete.set_style('corner', '[#dec14e]{item}')
        self.data_to_delete.set_char("corner", ['╭─','─╮', '─╯', '╰─'])
        self.data_to_delete.set_char('border', ['│ ', '─', ' │', '─'])
        self.data_to_delete.height = 10
        self.data_to_delete.overflow = ptg.Overflow.SCROLL
        count = 1 # - start of count
        for key in base['datas']:
            self.data_to_delete.__add__(ptg.Label(f'[@white black bold] {count} ' + "[@0] " + f'[@#34507d white bold] {key} ' + "[@0] " + f'[@#7d3434 white bold] {" ".join(base["datas"][key])} ', parent_align=0)) # parent_align -- 1-(Center) 2-(Right) 3-(Left)
            self.data_to_delete.__add__(ptg.Label(""))
            count += 1
        # 
        ######################################################################
            
        ## Attributes ########################################################
        # 
        self.NumOfDataToDelete = ptg.InputField(prompt="The number of data to delete: ")
        self.NumOfDataToDelete.set_style('prompt', '[white bold]{item}')
        self.NumOfDataToDelete.set_style('value', '[white]{item}')

        self.btnDelete = ptg.Button("    Delete    ", onclick=self.on_delete)
        self.btnDelete.set_style('label', '[@#c23232 white]{item}')
        self.btnDelete.set_style('highlight', '[@#ff4545 white bold]{item}')
        self.btnDelete.on_release(self.btnDelete)

        self.btnLeave = ptg.Button("    Cancel    ", onclick=self.on_leave)
        self.btnLeave.set_style('label', '[@#32ba52 white]{item}')
        self.btnLeave.set_style('highlight', '[@#45ff70 white bold]{item}')
        self.btnLeave.on_release(self.btnLeave)

        self.NameHint = ptg.Label("[#90ee90 bold]Write down the data number to delete.",parent_align=1)
        #
        ######################################################################

        ## Window properties #################################################
        # 
        # menu _______________________________________________________________
        self.del_window.__add__(self.data_to_delete) 
        self.del_window.__add__("")
        self.del_window.__add__(self.NameHint)
        self.del_window.__add__("")
        self.del_window.__add__(self.NumOfDataToDelete)
        self.del_window.__add__("")
        self.del_window.__add__((self.btnDelete, self.btnLeave))
        # properties _________________________________________________________
        self.del_window.center(0)
        self.del_window.set_title("[@white black bold] Deleting a data block")
        self.del_window.width = 70
        self.del_window.height = 18
        self.del_window.min_width = 70
        # 
        ######################################################################

    ## Functions #########################################################
    # 
    def on_delete(self, _):
        try:
            if self.NumOfDataToDelete.value:
                count = 1 # - start of count
                blockStatus = False
                for key in base['datas']:
                    if int(self.NumOfDataToDelete.value) == count:
                        del base['datas'][key]
                        blockStatus = True
                        break
                    count += 1
                if blockStatus:
                    self.del_window.__add__(self.data_to_delete) 
                    with open('data.json', 'w') as file:
                        json.dump(base, file)
                    manager.remove(self.del_window)
                    manager.add(windowMenu().menu_window)
                else:
                    self.NameHint.value = "[@1 white bold] Unavailable values for the block number "
                    time.sleep(1)
                    self.NameHint.value = "[#90ee90 bold]Write down the data number to delete."
            else:
                self.NameHint.value = "[@1 white bold] Unavailable values for the block number "
                time.sleep(1)
                self.NameHint.value = "[#90ee90 bold]Write down the data number to delete."
        except:
            self.NameHint.value = "[@1 white bold] Unavailable values for the block number "
            time.sleep(1)
            self.NameHint.value = "[#90ee90 bold]Write down the data number to delete."

    def on_leave(self, _):
        manager.remove(self.del_window)
        manager.add(windowMenu().menu_window)
    # 
    ######################################################################

class windowAddBlock(windowMenu):
    def __init__(self):

        ## Attributes ########################################################
        # 
        # - title 
        self.blockTitleContainer = ptg.Container()
        self.blockTitleContainer.height = 3
        self.blockTitleContainer.set_style('border', '[#dec14e]{item}')
        self.blockTitleContainer.set_style('corner', '[#dec14e]{item}')
        self.blockTitleContainer.set_char("corner", ['╭─','─╮', '─╯', '╰─'])
        self.blockTitleContainer.set_char('border', ['│ ', '─', ' │', '─'])
        self.blockTitleContainer.overflow = ptg.Overflow.SCROLL
        self.blockTitle = ptg.InputField(prompt="Name for the data block: ")
        self.blockTitleContainer._add_widget(self.blockTitle)
        self.blockTitle.set_style("prompt", "[white bold]{item}")
        self.blockTitle.set_style("value", "[white]{item}")

        # - data
        self.blockDataContainer = ptg.Container()
        self.blockDataContainer.height = 3
        self.blockDataContainer.set_style('border', '[#dec14e]{item}')
        self.blockDataContainer.set_style('corner', '[#dec14e]{item}')
        self.blockDataContainer.set_char("corner", ['╭─','─╮', '─╯', '╰─'])
        self.blockDataContainer.set_char('border', ['│ ', '─', ' │', '─'])
        self.blockDataContainer.overflow = ptg.Overflow.SCROLL
        self.blockData = ptg.InputField(prompt="Data for this block name: ")
        self.blockDataContainer._add_widget(self.blockData)
        self.blockData.set_style("prompt", "[white bold]{item}")
        self.blockData.set_style("value", "[white]{item}")

        self.btnOK = ptg.Button("    OK    ", onclick=self.on_ok)
        self.btnOK.set_style('label', '[@#32ba52 white]{item}')
        self.btnOK.set_style('highlight', '[@#45ff70 white bold]{item}')
        self.btnOK.on_release(self.btnOK)

        self.btnCancel = ptg.Button("  Cancel  ", onclick=self.on_cancel)
        self.btnCancel.set_style('label', '[@#c23232 white]{item}')
        self.btnCancel.set_style('highlight', '[@#ff4545 white bold]{item}')
        self.btnCancel.on_release(self.btnCancel)

        self.caution = ptg.Label('')
        #
        ######################################################################

        ## Window properties #################################################
        # 
        self.block_window = ptg.Window(
            self.blockTitleContainer,
            self.blockDataContainer,
            self.caution,"",
            (self.btnOK, self.btnCancel)
        )
        self.block_window.center(0)
        self.block_window.overflow = ptg.Overflow.SCROLL
        self.block_window.set_title("[@white black bold] New block")
        self.block_window.width = 70
        self.block_window.height = 12
        self.block_window.min_width = 70
        # 
        ######################################################################

    ## Functions #########################################################
    # 
    def on_ok(self, _):
        if self.blockTitle.value == '' or self.blockData.value == '':
            self.caution.value = '[@1 white bold] The block name or/and block data cannot be empty '
            time.sleep(1)
            self.caution.value = ""
        else:
            base['datas'][self.blockTitle.value] = []
            base['datas'][self.blockTitle.value] = self.blockData.value.strip().split()
            with open('data.json', 'w') as file:
                json.dump(base, file)
            manager.remove(self.block_window)
            manager.add(windowMenu().menu_window)

    def on_cancel(self, _):
        manager.remove(self.block_window)
        manager.add(windowMenu().menu_window)
    # 
    ######################################################################

class windowRegister(windowMenu):
    def __init__(self):
        ## Attributes ########################################################
        # 
        self.title = "[@white black bold] Registration"

        self.inputPassword = ptg.InputField(prompt="Come up with a password: ")
        self.inputPassword.set_style("prompt", "[white bold]{item}")
        self.inputPassword.set_style("value", "[white]{item}")

        self.btnReady = ptg.Button("   Ready   ", onclick=self.on_ready)
        self.btnReady.set_style('label', '[@white black]{item}')
        self.btnReady.set_style('highlight', '[@#90ee90 white bold]{item}')
        self.btnReady.on_release(self.btnReady)
        # 
        ######################################################################
        
        ## Window properties #################################################
        # 
        self.reg_window = ptg.Window(
            "",
            self.inputPassword,
            "",
            self.btnReady,
            ""
        )
        self.reg_window.center(0)
        self.reg_window.set_title(self.title)
        self.reg_window.width = 60
        self.reg_window.min_width = 60
        self.reg_window.height = 7
        # 
        ######################################################################

    ## Functions #########################################################
    # 
    # - registration - create a password to log in
    def on_ready(self, _):
        with open('data.json', 'r') as file:
            base = json.load(file) 
        if self.inputPassword.value:
            base['password'] = self.inputPassword.value.strip()
            with open('data.json', 'w') as file:
                json.dump(base, file)
            c_r.write_key()
            manager.remove(self.reg_window)
            manager.add(windowMenu().menu_window)
        else:
            label = ptg.Label('[1]The password cannot be empty')
            self.reg_window.__add__(label)
            time.sleep(1.5)
            self.reg_window.remove(label)
            self.reg_window.height = 7 
    # 
    ######################################################################

class windowLogin(windowMenu):
    def __init__(self):
        CONFIG_YAML = """
        config:
            Window:
                styles:
                    border: '[white]{item}'
                    corner: '[white]{item}'
        """
        loader = ptg.YamlLoader()
        namespace = loader.load(CONFIG_YAML)

        self.log_window = ptg.Window()
        ## Attributes ########################################################
        # 
        self.attempt_to_log_in = 10
        self.title = "[@white black bold] Sign in"

        self.inputPassword = ptg.InputField(prompt="Password:")
        self.inputPassword.set_style("prompt", "[white bold]{item}")
        self.inputPassword.set_style("value", "[0]{item}")

        self.btn_log = ptg.Button("   Login   ", onclick=self.on_sigin)
        self.btn_log.set_style('label', '[@#32ba52 white]{item}')
        self.btn_log.set_style('highlight', '[@#45ff70 white bold]{item}')
        self.btn_log.on_release(self.btn_log)

        self.attempts = ptg.Label(f'[8]{self.attempt_to_log_in} Attempts before deletion')
        # 
        ######################################################################

        ## Window properties #################################################
        # 
        
        self.log_window = ptg.Window(
            "",
            self.inputPassword,
            "",
            self.attempts,
            "",
            self.btn_log,
            ""
        )

        self.log_window.center(0)
        self.log_window.is_noresize = True
        self.log_window.set_title(self.title)
        self.log_window.width = 60
        self.log_window.min_width = 60
        self.log_window.height = 9
        #
        ######################################################################

    ## Functions #########################################################
    # 
    def on_sigin(self, _):
        # password correct
        global base
        key = c_r.load_key()
        c_r.decrypt('data.json', key)
        with open('data.json', 'r') as file:
            base = json.load(file) 
        if self.inputPassword.value.strip() == base['password']:
            manager.remove(self.log_window)
            manager.add(windowMenu().menu_window)   
        # incorrect password
        else:
            c_r.encrypt('data.json', key)
            self.attempts.value = "[@1 white bold] Incorrect code words! "
            time.sleep(1.5)
            self.attempt_to_log_in -= 1
            self.attempts.value = f'[8]{self.attempt_to_log_in} Attempts before deletion'
    # 
    ######################################################################
            
## Start window ######################################################
#
with ptg.WindowManager() as manager:

    try:
        # the file will be encrypted
        with open('data.json', 'r') as file:
            base = json.load(file) 
        # the password will not be read in 
        #the future as the file will be encrypted 
        #and will not be able to open
        if base['password'] == '':
            c_r.write_key()
            # - registration, password does not exist
            manager.add(windowRegister().reg_window)
        else:
            # - login, password exists
            manager.add(windowLogin().log_window)
    except Exception:
        manager.add(windowLogin().log_window)
# 
######################################################################
