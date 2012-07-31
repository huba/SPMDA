#message_handler.py
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

class message:
    def __init__(self,
                 sender_id,
                 receiver_id,
                 message_subject,
                 message_content):
        
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.subject = message_subject
        self.content = message_content
        self.delivered = False
        self.valid_receiver = True

    def is_delivered(self):
        return self.delivered

class message_bus:
    def __init__(self, owner):
        self.message_array = []
        self.owner = owner

    def pick_up(self, message):
        self.message_array.append(message)
    
    def deliver(self):
        for message in self.message_array:
            target_id = message.receiver_id
            target = self.owner.entity_handler.get_entity(target_id)

            if target:
                target.receive_message(message)

    def clean_up(self):
        for message in self.message_array:
            if message.is_delivered():
                self.message_array.pop(self.message_array.index(message))
