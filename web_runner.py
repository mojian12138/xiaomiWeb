# -*- coding: utf8 -*-
import uuid
import util.zepp_helper as zeppHelper

# Global token cache for the web runner
user_tokens = {}

class MiMotionRunner:
    def __init__(self, _user, _passwd):
        self.user_id = None
        self.device_id = str(uuid.uuid4())
        user = str(_user)
        password = str(_passwd)
        self.invalid = False
        self.log_str = ""
        if user == '' or password == '':
            self.error = "用户名或密码填写有误！"
            self.invalid = True
            pass
        self.password = password
        if (user.startswith("+86")) or "@" in user:
            user = user
        else:
            user = "+86" + user
        if user.startswith("+86"):
            self.is_phone = True
        else:
            self.is_phone = False
        self.user = user

    # 登录
    def login(self):
        # Check cache first
        user_token_info = user_tokens.get(self.user)
        if user_token_info is not None:
            # Simple check if we have tokens (logic simplified from main.py for web response speed)
            # In a real long-running app, we'd check expiry. 
            # Here we just try to use it or refresh if needed.
            app_token = user_token_info.get("app_token")
            login_token = user_token_info.get("login_token")
            self.device_id = user_token_info.get("device_id")
            self.user_id = user_token_info.get("user_id")
            
            ok, msg = zeppHelper.check_app_token(app_token)
            if ok:
                return app_token
            else:
                # Try to refresh
                app_token, msg = zeppHelper.grant_app_token(login_token)
                if app_token:
                     user_token_info["app_token"] = app_token
                     return app_token
        
        # If no cache or refresh failed, full login
        access_token, msg = zeppHelper.login_access_token(self.user, self.password)
        if access_token is None:
            self.log_str += "登录获取accessToken失败：%s" % msg
            return None
            
        login_token, app_token, user_id, msg = zeppHelper.grant_login_tokens(access_token, self.device_id, self.is_phone)
        if login_token is None:
            self.log_str += f"登录提取的 access_token 无效：{msg}"
            return None

        # Update cache
        user_token_info = dict()
        user_token_info["access_token"] = access_token
        user_token_info["login_token"] = login_token
        user_token_info["app_token"] = app_token
        user_token_info["user_id"] = user_id
        user_token_info["device_id"] = self.device_id
        user_tokens[self.user] = user_token_info
        
        self.user_id = user_id
        return app_token

    # 主函数
    def login_and_post_step(self, step):
        if self.invalid:
            return "账号或密码配置有误", False
        app_token = self.login()
        if app_token is None:
            return "登陆失败！" + self.log_str, False

        # Ensure step is a string for re.sub in zeppHelper
        step = str(step)
        ok, msg = zeppHelper.post_fake_brand_data(step, app_token, self.user_id)
        return f"修改步数（{step}）[" + msg + "]", ok
