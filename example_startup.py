from dragonbot import DragonBot

def main(test_mode = True):

    """Example DragonBot configuration file."""

    bot = DragonBot()

    bot.set_name("Toothless")

    bot.admins(["StoickTheVast"])
    bot.devs(["Hiccup", "Astrid"])

    bot.skills("skills", "skills.dat")

    if not test_mode:

        bot.jabber_id("911356_6457606@chat.hipchat.com")
        bot.jabber_password("rgu4FzcgrDUZxtUxncGVkXMc")
        bot.jabber_port(5222)

        bot.jabber_rooms({
            "Room 1": "911356_room_1@conf.hipchat.com",
            "Room 2": "911356_room_2@conf.hipchat.com",
            "Room 3": "911356_room_3@conf.hipchat.com"
        })

        bot.start_client()

    else:

        bot.start_shell()


if __name__ == "__main__":

    main(test_mode = True)
