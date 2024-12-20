class MysqlCredentials:
    def __init__(self):
        self.db_host = 'localhost' 
        self.db_user = 'root'       
        self.db_password = 'Qsczse001205-='  
        self.db_name = 'stock_history'
    

    def get_host(self):
        return self.db_host
    
    def get_user(self):
        return self.db_user
    
    def get_password(self):
        return self.db_password
    
    def get_name(self):
        return self.db_name