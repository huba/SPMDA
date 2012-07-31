#world.py
#This file is part of the SPMDA project
#Created by Huba Nagy 23.07.12
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

import message_handler
import entity

class world:
    def __init__(self):
        self.setup()

    def setup(self):
        self.message_bus = message_handler.message_bus(self)
        self.exit = False
        self.entity_handler = entity.entity_handler()
        self.entity_handler.add_owner(self)

    def end_world(self):
        self.exit = True

    def start(self):
        while not self.exit:
            self.entity_handler.update()
            self.entity_handler.clean_up()
            
            self.message_bus.deliver()
            self.message_bus.clean_up()
