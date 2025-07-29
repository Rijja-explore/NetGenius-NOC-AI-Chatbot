
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime
from zabbix_connector import fetch_network_metrics, generate_network_report
import os
import psutil
import socket
import platform
import time

app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_system_metrics():
    """Fetch detailed system metrics with error handling and platform compatibility."""
    try:
        uptime = time.time() - psutil.boot_time()
        boot_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(psutil.boot_time()))
        os_version = platform.platform()
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

        # Disk Usage
        disk_usage = {}
        for part in psutil.disk_partitions(all=False):
            try:
                usage = psutil.disk_usage(part.mountpoint)
                disk_usage[part.mountpoint] = f"{usage.percent}% used / {usage.free / (1024 ** 3):.2f} GB free"
            except Exception:
                continue
        total_disk = psutil.disk_usage('/')
        total_disk_str = f"{total_disk.percent}% used / {total_disk.free / (1024 ** 3):.2f} GB free"

        # Disk I/O
        disk_io = psutil.disk_io_counters()
        disk_read_speed = disk_io.read_bytes / 1024 / 1024 if disk_io.read_time > 0 else 0
        disk_write_speed = disk_io.write_bytes / 1024 / 1024 if disk_io.write_time > 0 else 0

        # Load Average (Unix only)
        try:
            load_avg = os.getloadavg()
        except AttributeError:
            load_avg = (0, 0, 0)  # Fallback for non-Unix systems like Windows/macOS

        # Process Count
        process_count = {"running": len([p for p in psutil.process_iter() if p.status() == 'running']),
                         "sleeping": len([p for p in psutil.process_iter() if p.status() == 'sleeping'])}

        # Top Resource-Consuming Processes
        top_processes = []
        for proc in sorted(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']),
                           key=lambda p: (p.info.get('cpu_percent', 0) or 0) + (p.info.get('memory_percent', 0) or 0), reverse=True)[:5]:
            try:
                top_processes.append(f"{proc.info['name']} (PID: {proc.info['pid']}): CPU {proc.info.get('cpu_percent', 0):.1f}%, Mem {proc.info.get('memory_percent', 0):.1f}%")
            except (psutil.NoSuchProcess, psutil.AccessDenied, KeyError):
                continue

        # Network Metrics
        net_io = psutil.net_io_counters()
        active_connections = len(psutil.net_connections(kind='all'))
        packet_errors = net_io.errin + net_io.errout
        bandwidth_util = (net_io.bytes_sent + net_io.bytes_recv) / (1024 ** 2)
        interfaces = {nic: status for nic, status in psutil.net_if_stats().items() if status.isup}

        # Security/Access (basic, no sensor data)
        login_attempts = {"successful": 0, "failed": 0}  # Requires log parsing, placeholder
        firewall_status = "Unknown"  # Requires firewall tool, placeholder
        open_ports = len(psutil.net_connections(kind='inet'))

        # Remove unsupported sensor data (e.g., temperature, fans, battery)
        cpu_temp = "N/A"  # Removed due to macOS incompatibility
        gpu_usage = "N/A"
        gpu_temp = "N/A"
        fan_speeds = {"N/A": "N/A"}
        battery_status = "N/A"

        return {
            "🔋 System Performance": {
                "Disk Usage (Total)": total_disk_str,
                "Disk Usage (Per Partition)": dict(disk_usage),
                "Disk I/O": f"Read: {disk_read_speed:.2f} MB/s, Write: {disk_write_speed:.2f} MB/s",
                "Load Average": f"1m: {load_avg[0]:.2f}, 5m: {load_avg[1]:.2f}, 15m: {load_avg[2]:.2f}",
                "Process Count": f"Running: {process_count['running']}, Sleeping: {process_count['sleeping']}",
                "Top Processes": top_processes if top_processes else ["N/A"]
            },
            "🌐 Network": {
                "Active Connections": active_connections,
                "Packet Error Rate": packet_errors,
                "Bandwidth Utilization": f"{bandwidth_util:.2f} MB",
                "Interface Status": {k: "UP" for k in interfaces.keys()}
            },
            "🔐 Security/Access": {
                "Login Attempts": f"Successful: {login_attempts['successful']}, Failed: {login_attempts['failed']}",
                "Firewall Status": firewall_status,
                "Open Ports": open_ports
            },
            "🌡️ Hardware Monitoring": {
                "CPU Temperature": cpu_temp,
                "GPU Usage/Temperature": f"Usage: {gpu_usage}, Temp: {gpu_temp}",
                "Fan Speeds": fan_speeds,
                "Battery Status": battery_status
            },
            "⏱️ System Uptime & Info": {
                "Uptime": f"{uptime // 3600:.0f}h {uptime % 3600 // 60:.0f}m",
                "Boot Time": boot_time,
                "OS Version": os_version,
                "Hostname": hostname,
                "IP Address": ip_address
            }
        }
    except Exception as e:
        print(f"Error in get_system_metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/network-status")
def get_network_status():
    try:
        metrics = fetch_network_metrics()
        if "error" in metrics:
            raise HTTPException(status_code=500, detail=metrics["error"])
        return {"status": "success", "data": metrics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/system-metrics")
def get_system_metrics_data():
    try:
        metrics = get_system_metrics()
        return {"status": "success", "data": metrics}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve system metrics: {str(e)}")

@app.get("/network-status-pdf")
def get_network_status_pdf():
    try:
        metrics = fetch_network_metrics()
        if "error" in metrics:
            raise HTTPException(status_code=500, detail=metrics["error"])

        pdf_file_path = "network_status_report.pdf"
        doc = SimpleDocTemplate(pdf_file_path, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(name="Title", fontSize=18, textColor=colors.navy, spaceAfter=20, alignment=1)
        section_style = ParagraphStyle(name="Section", fontSize=14, textColor=colors.darkgreen, spaceBefore=10, spaceAfter=10)
        normal_style = styles["Normal"]

        elements.append(Paragraph("Network Status Report", title_style))
        elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:M:%S')}", normal_style))
        elements.append(Spacer(1, 40))

        elements.append(Paragraph("Network Metrics", section_style))
        data = [["Metric Name", "Value"]]
        for metric in metrics:
            name = str(metric.get("name", "Unknown"))
            value = str(metric.get("lastvalue", "N/A"))
            data.append([name, value])

        table = Table(data, colWidths=[3.5*inch, 2*inch])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.white),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        elements.append(table)

        doc.build(elements)
        return FileResponse(pdf_file_path, media_type="application/pdf", filename="network_status_report.pdf")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/generate-report")
def get_generate_report():
    try:
        metrics = fetch_network_metrics()
        if "error" in metrics:
            raise HTTPException(status_code=500, detail=metrics["error"])

        pdf_file_path = "network_operations_report.pdf"
        doc = SimpleDocTemplate(pdf_file_path, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(name="Title", fontSize=18, textColor=colors.navy, spaceAfter=20, alignment=1)
        section_style = ParagraphStyle(name="Section", fontSize=14, textColor=colors.darkgreen, spaceBefore=10, spaceAfter=10)
        normal_style = styles["Normal"]

        elements.append(Paragraph("Network Operations Report", title_style))
        elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:M:%S')}", normal_style))
        elements.append(Spacer(1, 40))

        try:
            report = generate_network_report()
            if "error" not in report:
                elements.append(Paragraph("Summary", section_style))
                elements.append(Paragraph(report.get("report", "No summary available.").replace("\n", "<br/>"), normal_style))
                elements.append(Spacer(1, 20))
        except:
            pass

        elements.append(Paragraph("Network Metrics", section_style))
        data_network = [["Metric Name", "Value"]]
        for metric in metrics:
            name = str(metric.get("name", "Unknown"))
            value = str(metric.get("lastvalue", "N/A"))
            data_network.append([name, value])

        table_network = Table(data_network, colWidths=[3.5*inch, 2*inch])
        table_network.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.white),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        elements.append(table_network)
        elements.append(Spacer(1, 20))

        elements.append(Paragraph("System Metrics", section_style))
        system_metrics = get_system_metrics()
        data_system = []
        for category, metrics in system_metrics.items():
            data_system.append([Paragraph(f"<b>{category}</b>", normal_style), ""])
            for name, value in metrics.items():
                if isinstance(value, dict):
                    for sub_name, sub_value in value.items():
                        data_system.append([f"{name}: {sub_name}", sub_value])
                elif isinstance(value, list):
                    for item in value:
                        data_system.append([f"{name}", item])
                else:
                    data_system.append([name, str(value)])

        table_system = Table(data_system, colWidths=[3.5*inch, 2*inch])
        table_system.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.white),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        elements.append(table_system)

        doc.build(elements)
        return FileResponse(pdf_file_path, media_type="application/pdf", filename="network_operations_report.pdf")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/system-metrics-pdf")
def get_system_metrics_pdf():
    try:
        system_metrics = get_system_metrics()
        pdf_file_path = "system_metrics_report.pdf"
        doc = SimpleDocTemplate(pdf_file_path, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(name="Title", fontSize=18, textColor=colors.navy, spaceAfter=20, alignment=1)
        section_style = ParagraphStyle(name="Section", fontSize=14, textColor=colors.darkgreen, spaceBefore=10, spaceAfter=10)
        normal_style = styles["Normal"]

        elements.append(Paragraph("System Metrics Report", title_style))
        elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:M:%S')}", normal_style))
        elements.append(Spacer(1, 40))

        for category, metrics in system_metrics.items():
            elements.append(Paragraph(category, section_style))
            data = []
            for name, value in metrics.items():
                if isinstance(value, dict):
                    for sub_name, sub_value in value.items():
                        data.append([f"{name}: {sub_name}", sub_value])
                elif isinstance(value, list):
                    for item in value:
                        data.append([f"{name}", item])
                else:
                    data.append([name, str(value)])

            table = Table(data, colWidths=[3.5*inch, 2*inch])
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 12),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]))
            elements.append(table)
            elements.append(Spacer(1, 20))

        doc.build(elements)
        return FileResponse(pdf_file_path, media_type="application/pdf", filename="system_metrics_report.pdf")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run with: uvicorn main:app --reload
