from pytripgui import __version__ as pytripgui_version
from pytrip import __version__ as pytrip_version

about_txt_en = ""
about_txt_en += "PyTRipGUI Version: " + pytripgui_version + "\n"
about_txt_en += "PyTRiP Version:" + pytrip_version + "\n"
about_txt_en += "\n"
about_txt_en += "(c) 2012 - 2019 PyTRiP98 Developers\n"
about_txt_en += "    Niels Bassler\n"
about_txt_en += "    Leszek Grzanka\n"
about_txt_en += "    Łukasz Jeleń\n"
about_txt_en += "\n"
about_txt_en += "Previous contributors:\n"
about_txt_en += "    Jakob Toftegaard\n"

InfoMessages_en = {
    "about": ["PyTRiPGUI", about_txt_en],
    "addNewPatient": ["Add new Patient", "Before continue, you should create or import Patient"],
    "loadCtxVdx": ["Load CTX and VDX file", "Before continue, you should have loaded CTX and VDX data"],
    "addOneField": ["Add at least one field", "Before continue, you should add at least one field to selected plan"],
    "configureKernelList":
    ["Add at least one kernel", "Before continue, you should add at least one kernel in Settings/Beam Kernel"],
    "configureTrip":
    ["Configure trip98 settings", "Before continue, you should configure Trip98 paths in Settings/Trip98 Config"],
    "kernelSisPath": ["Given kernel has no sis path", "Kernel selected by plan has no valid sis path"],
    "noTargetRoiSelected": ["No target ROI selected", "Please select TargetROI in 'Target' tab"]
}

InfoMessages = InfoMessages_en
