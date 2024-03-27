import pytermgui as ptg
import config, time, json
  
attempt = 10

# base of data
with open('data.json', 'r') as file:
    base = json.load(file)    
# base of data

class windowMenu():
    def __init__(self):

        self.loader = ptg.YamlLoader()
        self.namespace = self.loader.load(config.CONFIG_MENU)
        self.menu_window = ptg.Window()

        self.status_data = ptg.Label("")
        if base['datas'] == {}:
            self.status_data.value = "Tip: There is no data, try adding a new data block"    

        self.listOfData = ptg.Container()
        self.listOfData.height = 10
        self.listOfData.overflow = ptg.Overflow.SCROLL

        count = 1
        for key in base['datas']:
            self.listOfData.__add__(ptg.Label(f'{count}| {key}: {" ".join(base["datas"][key])}'))
            count += 1

        self.add_btn = ptg.Button(" Insert ", onclick=self.addBlock)
        self.show_btn = ptg.Button("  Show  ")
        self.del_btn = ptg.Button(" Delete ")
        self.edit_btn = ptg.Button("  Edit  ")
        self.exit_btn = ptg.Button("    Exit    ", onclick=self.on_exit)

        self.menu = (self.add_btn, self.show_btn, self.del_btn, self.edit_btn)

        self.menu_window.__add__(self.listOfData) 
        self.menu_window.__add__(self.status_data)
        self.menu_window.__add__(self.menu)
        self.menu_window.__add__("")
        self.menu_window.__add__(self.exit_btn)

        self.menu_window.center(0)
        self.menu_window.is_noresize = True 
        self.menu_window.set_title("[bold]Password Manager")
        self.menu_window.width = 70
        self.menu_window.min_width = 70

    def on_exit(self, inx):
        manager.stop()

    def addBlock(self, inx):
        manager.remove(self.menu_window)
        manager.add(windowAddBlock().block_window, animate=True)

class windowAddBlock(windowMenu):
    def __init__(self):

        self.blockTitle = ptg.InputField(prompt="Name for the block: ")
        self.blockData = ptg.InputField(prompt="Data for this block name: ")
        self.btnOk = ptg.Button("Ok", onclick=self.on_ok)
        self.btnCancel = ptg.Button("Cancel", onclick=self.on_cancel)
        self.caution = ptg.Label('')

        self.block_window = ptg.Window(
            "",
            self.blockTitle,
            "",
            self.blockData,
            "","",self.caution,"",
            (self.btnOk, self.btnCancel)
        )
        self.block_window.center(0)
        self.block_window.set_title("[bold]New block")
        self.block_window.width = 70
        self.block_window.height = 12
        self.block_window.min_width = 70

    def on_ok(self, inx):
        if self.blockTitle.value == '' or self.blockData.value == '':
            self.caution.value = '[1 bold]The block name or/and block data cannot be empty'
        else:
            base['datas'][self.blockTitle.value] = []
            base['datas'][self.blockTitle.value] = self.blockData.value.strip().split()
            with open('data.json', 'w') as file:
                json.dump(base, file)
            manager.remove(self.block_window)
            manager.add(windowMenu().menu_window, animate=True)

    def on_cancel(self, inx):
        manager.remove(self.block_window)
        manager.add(windowMenu().menu_window, animate=True)

class windowRegister(windowMenu):
    def __init__(self):

        self.loader = ptg.YamlLoader()
        self.namespace = self.loader.load(config.CONFIG_REGLOGWINDOW)

        self.input_password = ptg.InputField(prompt="Come up with a password: ")
        self.btnReady = ptg.Button("   Ready   ", onclick=self.on_ready)
        self.reg_window = ptg.Window(
            "",
            self.input_password,
            "",
            self.btnReady,
            ""
        )
        self.reg_window.center(0)
        self.reg_window.set_title("Registration")
        self.reg_window.width = 60
        self.reg_window.min_width = 60
        self.reg_window.height = 7

    def on_ready(self, inx):
        if self.input_password.value:
            base['password'] = self.input_password.value.strip()
            with open('data.json', 'w') as file:
                json.dump(base, file)
            manager.remove(self.reg_window)
            manager.add(windowMenu().menu_window, animate=True)
            manager.on_resize(70, 13)

        else:
            label = ptg.Label('[1]The password cannot be empty')
            self.reg_window.__add__(label)
            time.sleep(1.5)
            self.reg_window.remove(label)
            self.reg_window.height = 7 

class windowLogin(windowMenu):
    def __init__(self):

        self.attempt = 10
        self.loader = ptg.YamlLoader()
        self.namespace = self.loader.load(config.CONFIG_REGLOGWINDOW)

        self.inputPassword = ptg.InputField(prompt="Password: ")
        self.btn_log = ptg.Button("   Login   ", onclick=self.on_sigin)
        self.attempts = ptg.Label(f'[8]{self.attempt} Attempts before deletion')
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
        self.log_window.set_title("[bold]Sign in")
        self.log_window.width = 60
        self.log_window.min_width = 60
        self.log_window.height = 9

    def on_sigin(self, inx):
        # password correct
        if self.inputPassword.value.strip() == base['password']:
            manager.remove(self.log_window)
            manager.add(windowMenu().menu_window)
            
        # incorrect password
        else:
            self.attempts.value = "[@red black bold] Incorrect code words! "
            time.sleep(1.5)
            self.attempt -= 1
            self.attempts.value = f'[8]{self.attempt} Attempts before deletion'

with ptg.WindowManager() as manager:

    winLogin = windowLogin()
    winRegistration = windowRegister()

    if base['password'] == '':
        manager.add(winRegistration.reg_window, animate=True)
    else:
        manager.add(winLogin.log_window, animate=True)

    
