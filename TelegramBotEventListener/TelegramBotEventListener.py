
import appdaemon.plugins.hass.hassapi as hass
import re
 
class TelegramBot(hass.Hass):
 
    def initialize(self): 
    
        self._commanddict = {"/help": {"desc": "Help", "method": "self._cmd_help(user_id)"},
                             "/state_climate": {"desc": "State of climate", "method": "self._cmd_state_climates(user_id)"}}

        self.listen_event(self._receive_telegram_command, 'telegram_command')
    
    
    def _escape_markdown(self, msg):
        msg = msg.replace("`", "\\`")
        msg = msg.replace("*", "\\*")
        msg = msg.replace("_", "\\_")

        return msg
	
    def _receive_telegram_command(self, event_id, payload_event, *args):
        user_id = payload_event['user_id']
        chat_id = payload_event['chat_id']
        command = payload_event['command'].lower()
        
        #self.log(f"_receive_telegram_command, user_id: {user_id}, chat_id: {chat_id}, command: {command}")
        
        if command in self._commanddict:
            method = self._commanddict[command]['method']
            #self.log(f"self._commanddict[command]['method']: {method}")
            exec(method)
        else:
            msg = f"Unkown command {command}. Use /help to get a list of all available commands:\n"
            for command in self._commanddict:
                desc = self._commanddict[command]["desc"]
                msg += f"{command} : {desc}\n"
            self.call_service(
                'telegram_bot/send_message',
                target=user_id,
                message=self._escape_markdown(msg))
    
    def _cmd_help(self, user_id):
        msg = f"This is the list of all available commands:\n"
        for command in self._commanddict:
            desc = self._commanddict[command]['desc']
            msg += f"{command} : {desc}\n"
        self.log(f"msg {msg}")
        self.call_service(
            'telegram_bot/send_message',
            target=user_id,
            message=self._escape_markdown(msg))
    
    def _cmd_state_climates(self, user_id):
        climates = []
        for entity in self.get_state():
            if "climate" in entity:
                climates.append(entity)

        msg = f"This are the states of all available climates:\n"
        for climate in climates:
            all = self.get_entity(climate).get_state(attribute="all")
            atr = all["attributes"]
            state = all["state"]
            self.log(f"all: {all}")
            if "friendly_name" in atr:
                msg += f"{atr['friendly_name']}\n* state: {state}\n"
            else:
                msg += f"{climate}\n* state: {state}\n"

            if "current_temperature" in atr:
                msg += f"* act temp: {atr['current_temperature']}\n"
                
            if "temperature" in atr:
                msg += f"* set temp: {atr['temperature']}\n"

            if "fan_mode" in atr:
                msg += f"* fan_mode: {atr['fan_mode']}\n"

            if "preset_mode" in atr:
                msg += f"* preset_mode: {atr['preset_mode']}\n"

            if "swing_mode" in atr:
                msg += f"* swing_mode: {atr['swing_mode']}\n"

        self.call_service(
            'telegram_bot/send_message',
            target=user_id,
            message=self._escape_markdown(msg))
