from myselenium import WebDriver


class ShimoLogin:
    def __init__(self):
        self.home_url = "https://shimo.im/"
        self.profile_url = "https://shimo.im/profile"
        self.w = WebDriver(
            username_xpath="//input[@name='mobileOrEmail']",
            password_xpath="//input[@name='password']",
            login_button_xpath="//button[contains(text(), '立即登录')]",
        )

    def run(self):
        self.w.open(self.home_url)
        self.w.sleep(3)
        self.w.wait_until_by_xpath("//button[contains(text(), '登录')]").click()
        self.w.sleep(3)
        self.w.login()
        self.w.sleep(3)
        self.w.open(self.profile_url)
        self.w.sleep(10)


def main():
    w = ShimoLogin()
    w.run()


if __name__ == '__main__':
    main()