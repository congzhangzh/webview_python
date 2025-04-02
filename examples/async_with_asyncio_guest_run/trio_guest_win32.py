#
# Copyright 2020 Richard J. Sheridan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from asyncio_guest_run import asyncio_guest_run, schedule_on_asyncio
import sys

import example_tasks_asyncio

def global_excepthook(etype, value, tb):
    print(f"global excepthook: {etype} {value} {tb}")
    traceback.print_exception(etype, value, tb)
sys.excepthook = global_excepthook

import threading
def threading_excepthook(etype, value, tb):
    print(f"threading excepthook: {etype} {value} {tb}")
    traceback.print_exception(etype, value, tb)

threading.excepthook = threading_excepthook
import collections
import traceback

#import trio
import win32api
import win32con
import win32gui
import win32ui
from outcome import Error
from pywin.mfc import dialog

import example_tasks

TRIO_MSG = win32con.WM_APP + 3

trio_functions = collections.deque()


# @cffi.def_extern()  # if your mainloop is in C/C++
def do_trio():
    trio_functions.popleft()()


class Win32Host:
    def __init__(self, display):
        self.display = display
        self.mainthreadid = win32api.GetCurrentThreadId()
        # create event queue with null op
        win32gui.PeekMessage(
            win32con.NULL, win32con.WM_USER, win32con.WM_USER, win32con.PM_NOREMOVE
        )

    def run_sync_soon_threadsafe(self, func):
        """Use use PostThreadMessage to schedule a callback
        https://docs.microsoft.com/en-us/windows/win32/winmsg/about-messages-and-message-queues
        """
        win32api.PostThreadMessage(self.mainthreadid, TRIO_MSG, win32con.NULL, win32con.NULL)
        trio_functions.append(func)

    def run_sync_soon_not_threadsafe(self, func):
        """Use use PostMessage to schedule a callback
        https://docs.microsoft.com/en-us/windows/win32/winmsg/about-messages-and-message-queues
        This doesn't provide any real efficiency over threadsafe.
        """
        win32api.PostMessage(win32con.NULL, TRIO_MSG, win32con.NULL, win32con.NULL)
        trio_functions.append(func)

    def done_callback(self, outcome):
        """non-blocking request to end the main loop
        """
        print(f"Outcome: {outcome}")
        if isinstance(outcome, Error):
            exc = outcome.error
            traceback.print_exception(type(exc), exc, exc.__traceback__)
            exitcode = 1
        else:
            exitcode = 0
        self.display.dialog.PostMessage(win32con.WM_CLOSE, 0, 0)
        self.display.dialog.close()
        win32gui.PostQuitMessage(exitcode)

    def mainloop(self):
        while True:
            code, msg = win32gui.GetMessage(0, 0, 0)
            if not code:
                break
            if code < 0:
                error = win32api.GetLastError()
                raise RuntimeError(error)

            #######################################
            ### Trio specific part of main loop ###
            #######################################
            hwnd, msgid, lparam, wparam, time, point = msg
            if hwnd == win32con.NULL and msgid == TRIO_MSG:
                do_trio()
                continue
            ###############################
            ### Trio specific part ends ###
            ###############################

            win32gui.TranslateMessage(msg)
            win32gui.DispatchMessage(msg)


def MakeDlgTemplate():
    style = (
        win32con.DS_MODALFRAME
        | win32con.WS_POPUP
        | win32con.WS_VISIBLE
        | win32con.WS_CAPTION
        | win32con.WS_SYSMENU
        | win32con.DS_SETFONT
    )
    cs = win32con.WS_CHILD | win32con.WS_VISIBLE

    w = 300
    h = 21

    dlg = [
        ["...", (0, 0, w, h), style, None, (8, "MS Sans Serif")],
    ]

    s = win32con.WS_TABSTOP | cs

    dlg.append(
        [128, "Cancel", win32con.IDCANCEL, (w - 60, h - 18, 50, 14), s | win32con.BS_PUSHBUTTON]
    )

    return dlg


class PBarDialog(dialog.Dialog):
    def OnInitDialog(self):
        code = super().OnInitDialog()
        self.pbar = win32ui.CreateProgressCtrl()
        self.pbar.CreateWindow(
            win32con.WS_CHILD | win32con.WS_VISIBLE, (10, 10, 310, 24), self, 3000
        )
        return code

    def OnCancel(self):
        # also window close response
        self.cancelfn()


class Win32Display:
    def __init__(self):
        self.dialog = PBarDialog(MakeDlgTemplate())
        self.dialog.CreateWindow()
        # self.display.DoModal()

    def set_title(self, title):
        self.dialog.SetWindowText(title)

    def set_max(self, maximum):
        # hack around uint16 issue
        self.realmax = maximum
        self.dialog.pbar.SetRange(0, 65535)

    def set_value(self, downloaded):
        self.dialog.pbar.SetPos(int((downloaded / self.realmax * 65535)))

    def set_cancel(self, fn):
        self.dialog.cancelfn = fn


def main(task):
    display = Win32Display()
    host = Win32Host(display)
    asyncio_guest_run(
        task,
        display,
        run_sync_soon_threadsafe=host.run_sync_soon_threadsafe,
        run_sync_soon_not_threadsafe=host.run_sync_soon_not_threadsafe,
        done_callback=host.done_callback,
    )
    host.mainloop()


if __name__ == "__main__":
    print("Known bug: Dragging the window freezes everything.")
    print("For now only click buttons!")
    main(example_tasks_asyncio.count_with_try_except)
