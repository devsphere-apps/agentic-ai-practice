class LogAnalyzer:

    def __init__(self):
        
        self.logs=[]

    def add_log(self,message:str,severity:str):
        log = {
            "message":message,
            "severity":severity
        }
        self.logs.append(log)
    
    def get_critical(self):
        critical_logs =[]

        for log in self.logs:

            if log["severity"] == "critical":
                critical_logs.append(log["message"])

        return critical_logs
    
    def __str__(self):
        
        return f"Total Logs: {len(self.logs)}"

analyzer = LogAnalyzer()

analyzer.add_log("Login failed", "critical")
analyzer.add_log("Port scan detected", "high")
analyzer.add_log("File accessed", "low")


print(analyzer)

print(analyzer.get_critical())