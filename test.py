#!/usr/bin/env python
import spmda.entity
import spmda.message_handler
import spmda.world

def box_controller_action(cont, entity):
    if cont.listeners["msg_lstr_000"].get_state() == True:
        print "IT'S ALIVE!"
        raw_input("press enter to continue")
        entity.world.end_world()

def rock_controller_action(cont, entity):
    msg = spmda.message_handler.message(entity.entity_id,
                                  "box_000",
                                  "activate",
                                  None)
    entity.message_out.append(msg)

test_world = spmda.world.world()

box = spmda.entity.entity("box_000")
box_controller = spmda.entity.controller("box_cont_000",
                                   box_controller_action)
bc_listener = spmda.entity.message_listener("activate",
                                      "msg_lstr_000")
box_controller.add_listener(bc_listener)
box.add_controller(box_controller)
test_world.entity_handler.add_entity(box)

rock = spmda.entity.entity("rock_000")
rock_cont = spmda.entity.controller("rock_cont_000",
                              rock_controller_action)
rock.add_controller(rock_cont)
test_world.entity_handler.add_entity(rock)

test_world.start()
