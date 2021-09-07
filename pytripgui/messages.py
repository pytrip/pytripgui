from pytripgui import __version__ as pytripgui_version
from pytrip import __version__ as pytrip_version

about_txt_en = """PyTRipGUI Version: {}
PyTRiP Version: {}
(c) 2010 - 2021 PyTRiP98 Developers
    Niels Bassler
    Leszek Grzanka
    Toke Printz
    Łukasz Jeleń
    Arkadiusz Ćwikła
    Joanna Fortuna
    Michał Krawczyk
    Mateusz Łaszczyk
""".format(pytripgui_version, pytrip_version)

InfoMessages_en = {
    "about": ["PyTRiPGUI", about_txt_en],
    "addNewPatient": ["Add new Patient", "Before continue, you should create or import Patient"],
    "loadCtxVdx": ["Load CTX and VDX file", "Before continue, you should have loaded CTX and VDX data"],
    "addOneField": ["Add at least one field", "Before continue, you should add at least one field to selected plan"],
    "configureKernelList":
    ["Add at least one kernel", "Before continue, you should add at least one kernel in Settings/Beam Kernel"],
    "configureTrip":
    ["Configure trip98 settings", "Before continue, you should configure TRiP98 paths in Settings/TRiP98 Config"],
    "kernelSisPath": ["Given kernel has no SIS path", "Kernel selected by plan has no valid SIS path"],
    "noTargetRoiSelected": ["No target ROI selected", "Please select TargetROI in 'Target' tab"]
}

InfoMessages = InfoMessages_en
