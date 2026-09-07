from datetime import datetime
import re


class JarvisCore:

    def __init__(self):
        self.name = "JARVIS"
        self.version = "2.0"
        self.online = True

    def system_status(self):
        return {
            "name": self.name,
            "version": self.version,
            "online": self.online,
            "time": datetime.now().strftime("%I:%M %p"),
            "date": datetime.now().strftime("%d %B %Y")
        }

    def greet(self):
        hour = datetime.now().hour

        if hour < 12:
            greeting = "Good morning"
        elif hour < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"

        return f"{greeting}, Sir. JARVIS systems are online and ready."

    def think(self, command):
        command = command.strip()
        text = command.lower()

        if not command:
            return "I'm listening, Sir."

        # Greetings
        if re.search(r"\b(hello|hi|hey|namaste)\b", text):
            return self.greet()

        # Identity
        if "who are you" in text or "your name" in text:
            return (
                "I am JARVIS 2.0, your personal AI assistant. "
                "My core systems are online, Sir."
            )

        # Status
        if "status" in text or "systems" in text:
            s = self.system_status()
            return (
                f"All core systems are operational, Sir. "
                f"Current time is {s['time']}. "
                f"Date is {s['date']}."
            )

        # Time
        if "time" in text:
            return f"The current time is {datetime.now().strftime('%I:%M %p')}, Sir."

        # Date
        if "date" in text or "today" in text:
            return f"Today is {datetime.now().strftime('%A, %d %B %Y')}, Sir."

        # Help
        if "help" in text or "what can you do" in text:
            return (
                "At present I can handle basic commands, system status, "
                "time, date and conversation. "
                "Voice, web search, memory and Android controls are ready "
                "to be added to my systems."
            )

        # Shutdown request — safe response only
        if "shutdown yourself" in text or "turn yourself off" in text:
            return "I can prepare a shutdown command, but I require confirmation first, Sir."

        # Unknown command
        return (
            f"I've received your command, Sir. "
            f"The command router is active, but that capability has not "
            f"yet been connected to my tool system."
        )


jarvis = JarvisCore()
