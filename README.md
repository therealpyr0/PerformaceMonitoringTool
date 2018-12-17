# PerformaceMonitoringTool
A utility to monitor VMS, RSS and CPU utilization of A process.

Usage:
Written in Python 2.7
external packages required : psutil
Run the following command in cmd/terminal :
python PerformanceMonitoringTool.py --processname=<processname to be monitored> --hostname=<remote machine hostname to send data via post call> --identifier=<a unique identifier>

mandatory arguments :  processname
optional arguments : hostname , identifier

Notes :
saves data in json format in location : 
windows : %temp%/"PerformanceData"/<identifier>/<timeStamp>/data.json
mac : /tmp/"PerformanceData"/<identifier>/<timeStamp>/data.json
(timestamp is added to avoid overwrite data.json)
