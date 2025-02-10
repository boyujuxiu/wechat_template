import tkinter as tk

def add_drag_n_drop_support(widget):
    """为tkinter窗口添加拖放支持"""
    
    def _drag_enter(event):
        event.widget.focus_force()
        return event.action
    
    def _drag_leave(event):
        return event.action
    
    def _drop_position(event):
        return event.action
    
    widget.drop_target_register = lambda *args: None
    widget.dnd_bind = lambda *args: None
    
    try:
        widget.tk.eval('package require tkdnd')
        widget.drop_target_register = widget.tk.eval
        
        widget.dnd_bind = lambda event, callback: widget.bind(
            '<<' + event + '>>', callback
        )
        
        widget.tk.eval('''
        proc ::dnd::HandleXdndEnter {window drag_source typelist} {
            return "copy"
        }
        ''')
        
        widget.bind('<FocusIn>', _drag_enter)
        widget.bind('<FocusOut>', _drag_leave)
        widget.bind('<B1-Motion>', _drop_position)
        
    except tk.TclError:
        print("TkDND not available - drag and drop support disabled") 