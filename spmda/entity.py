#entity.py
#This file is part of the SPMDA project
#Created by Huba Nagy 21.07.12
#  and is released under the MIT Licence.
#
#Copyright (c) 2012 Huba Z. Nagy
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

def toggle(boolean):
    return not boolean

class message_listener:
    def __init__(self,
                 message_subject,
                 message_listener_id,
                 toggle = False,
                 invert = False,
                 sender_id = None):
        
        self.message_subject = message_subject
        self.listener_id = message_listener_id
        self.messages= []
        self.toggle = toggle
        self.invert = invert
        
        self.state = False
        self.sender_id = sender_id
        self.content = {}

    def get_state(self):
        """This function returns the state of the listener, or the
        opposite if the invert value is set to true."""
        state = self.state
        
        if self.invert:
            state = not state

        return state

    def collect_messages(self, entity):      
        for message in entity.message_in:
            if message.subject == self.message_subject:
                if self.sender_id:
                    if message.sender_id == self.sender:
                        self.messages.append(entity.message_in.pop(message))

                else:
                    self.messages.append(entity.message_in.pop(entity.message_in.index(message)))

                if not self.toggle:
                    self.state = True

        if self.toggle:
            if len(self.messages) > 0:
                toggle(self.state)

    def read_messages(self):
        for message in self.messages:
            if message.subject == self.message_subject:
                if self.toggle:
                    self.state = toggle(self.state)

                else:
                    self.state = True

                content = message.content
                break

    def clean_up(self):
        self.messages = []
        self.content = {}
        
        if not self.toggle:
            self.state = False

    def update(self, entity):
        self.collect_messages(entity)
        self.read_messages()

class controller:
    def __init__(self, controller_id, function):
        self.function = function
        self.listeners = {}
        self.controller_id = controller_id

    def update_listeners(self, entity):
        for listener in self.listeners:
            self.listeners[listener].update(entity)
            
    def execute(self, entity):
        try:
            self.function(self, entity)

        except TypeError:
            return

    def clean_up(self):
        for listener in self.listeners:
            self.listeners[listener].clean_up()

    def update(self, entity):
        self.update_listeners(entity)
        self.execute(entity)

    def add_listener(self, listener):
        if not listener.listener_id in self.listeners:
            self.listeners[listener.listener_id] = listener
        
class entity(object):
    self.entity_id = ""
    message_in = []
    message_out = []
    controllers = {}
    world = None
    entity_handler = None
        
    def __init__(self, entity_id):
        self.entity_id = entity_id

    def receive_message(self, message):
        self.message_in.append(message)

    def post_messages(self):
        if self.world != None:
            for message in self.message_out:
                self.world.message_bus.pick_up(message)

    def set_owner(self, owner):
        self.entity_handler = owner
        self.world = owner.world

    def add_controller(self, controller):
        if not controller.controller_id in self.controllers:
            self.controllers[controller.controller_id] = controller

    def update(self):
        for controller in self.controllers:
            self.controllers[controller].update(self)

        self.post_messages()
            
    def clean_up(self):
        for controller in self.controllers:
            self.controllers[controller].clean_up()

class entity_handler:
    def __init__(self):
        self.world = None
        self.entity_array = {}

    def add_owner(self, owner):
        self.world = owner

    def add_entity(self, entity):
        if not entity.entity_id in self.entity_array:
            entity.set_owner(self)
            self.entity_array[entity.entity_id] = entity

    def get_entity(self, entity_id):
        return self.entity_array[entity_id]
        
    def update(self):
        for entity in self.entity_array:
            self.entity_array[entity].update()

    def clean_up(self):
        for entity in self.entity_array:
            self.entity_array[entity].clean_up()
